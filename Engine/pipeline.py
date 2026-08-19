"""Stage orchestration.

Each stage receives only its declared inputs. That isolation is what makes the
stages independently testable and what stops any later stage from acquiring
context it could invent from.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .activate import Claim, activate, verify_claims
from .chart import BirthRecord, ChartBundle, compute_chart, resolve_birth
from .ephemeris import EphemerisProvider, SwissEphemerisDLL
from .doctrine import Doctrine
from .facts import FactSet, extract_facts
from .overrides import apply_overrides
from .render import (
    QuotingSynthesizer,
    Sentence,
    Synthesizer,
    audit_view,
    consultation,
    synthesis_sentences,
)
from .rules import RuleCard, load_cards, verify_cards
from .synthesis import SynthesisResult, synthesise, verify_synthesis

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES = ROOT / "Rules"
DEFAULT_CORPUS = ROOT / "Knowledge"


class PipelineError(RuntimeError):
    pass


@dataclass
class Result:
    chart: ChartBundle
    facts: FactSet
    claims: list[Claim]
    sentences: list[Sentence]
    synthesis: SynthesisResult
    coverage: dict
    verification: object
    consultation: str
    audit: str


def _book_meta(rules_dir: Path) -> dict[str, dict]:
    meta: dict[str, dict] = {}
    for m in sorted(rules_dir.glob("*/manifest.json")):
        d = json.loads(m.read_text(encoding="utf-8"))
        meta[d["book_id"]] = d
    return meta


def _coverage(chart: ChartBundle, claims: list[Claim], report: dict) -> dict:
    """What the loaded corpus does *not* say about this chart.

    Silence is a first-class result, and this is the raw material of the gap
    log that governs whether the corpus freeze is ever lifted.
    """
    covered = set()
    for c in claims:
        for f in c.derived["facts"]:
            if f["key"].startswith("in_house("):
                inner = f["key"][len("in_house("):-1]
                graha, house = inner.split(",")
                covered.add((graha, int(house)))

    gaps = []
    for name, b in chart.bodies.items():
        if (name, b.house) not in covered:
            gaps.append(f"{name} in the {b.house}th house — no rule card in the store")

    out = dict(report)
    out["not_covered"] = gaps
    return out


def _scope(meta: dict[str, dict]) -> list[str]:
    """What doctrine is actually loaded, stated from the manifests.

    Abstention is a designed output. A reader must be able to see that a
    reading drawn from one chapter is a reading from one chapter.
    """
    lines = []
    for book in sorted(meta.values(), key=lambda m: m["book_id"]):
        chapters = book.get("chapters_extracted") or []
        which = ", ".join(f"ch. {c}" for c in chapters) if chapters else "none"
        lines.append(f"{book.get('title', book['book_id'])} — {which}")
    return lines


def run(
    record: BirthRecord,
    provider: EphemerisProvider | None = None,
    rules_dir: Path = DEFAULT_RULES,
    corpus_dir: Path = DEFAULT_CORPUS,
    ayanamsa: str = "lahiri",
    house_system: str = "whole_sign",
    synthesizer: Synthesizer | None = None,
) -> Result:
    own = provider is None
    provider = provider or SwissEphemerisDLL()
    try:
        # Build time: no card may enter the run unless its quote still matches.
        cards: list[RuleCard] = load_cards(rules_dir)
        if not cards:
            raise PipelineError(f"no rule cards found under {rules_dir}")
        problems = verify_cards(cards, corpus_dir)
        if problems:
            raise PipelineError(
                "rule store failed verification; refusing to run:\n  "
                + "\n  ".join(problems)
            )

        resolved = resolve_birth(record, provider)                    # Stage 0
        chart = compute_chart(resolved, provider, ayanamsa, house_system)  # Stage 1
        doctrine = Doctrine.from_cards(cards)
        facts = extract_facts(chart, doctrine)                        # Stage 2
        facts = apply_overrides(cards, doctrine, facts, chart)         # Stage 2b
        claims, report = activate(chart, facts, cards, _book_meta(rules_dir))  # Stage 6

        # Stage 7 is not implemented in this slice: with a single chapter there
        # is nothing to adjudicate between. Claims are ordered deterministically
        # by house then body so the report reads in a stable order.
        # A claim with no house of its own -- one keyed on the ascendant's sign
        # -- sorts to 0 and leads, matching how Stage 10 groups it.
        order = {b: i for i, b in enumerate(chart.bodies)}
        claims.sort(key=lambda c: (
            _house(c) or 0, order.get(_body(c), 99)
        ))

        # Stage 7c/8. Synthesis measures recurrence across the activated
        # passages; it introduces no claim of its own.
        synthesis = synthesise(claims)
        synthesizer = synthesizer or QuotingSynthesizer()
        sentences = synthesizer.compose(claims, chart) + synthesis_sentences(synthesis)

        verification = verify_claims(claims, facts, chart, cards, corpus_dir)  # Stage 9
        synth_problems = verify_synthesis(synthesis, claims)
        if synth_problems:
            verification.ok = False
            verification.failures.extend(synth_problems)
        verification.checks["synthesis_themes"] = len(synthesis.themes)
        verification.checks["synthesis_grounded"] = not synth_problems
        if not verification.ok:
            raise PipelineError(
                "groundedness verification failed; report not emitted:\n  "
                + "\n  ".join(verification.failures)
            )

        # Stage 9 also gates the prose: a sentence with no claim cannot ship.
        # This covers the synthesis sentences too -- if Part 3 ever says
        # something that does not trace to Part 2, the report does not exist.
        known = {c.claim_id for c in claims}
        for s in sentences:
            if not s.claim_ids or not set(s.claim_ids) <= known:
                raise PipelineError(f"unsourced sentence in output: {s.text[:80]!r}")
        verification.checks["sentences_all_sourced"] = len(sentences)

        meta = _book_meta(rules_dir)
        coverage = _coverage(chart, claims, report)
        coverage["loaded_doctrine"] = _scope(meta)
        return Result(                                                # Stage 10
            chart=chart, facts=facts, claims=claims, sentences=sentences,
            synthesis=synthesis, coverage=coverage, verification=verification,
            consultation=consultation(chart, facts, claims, sentences,
                                      synthesis, coverage),
            audit=audit_view(claims, chart, verification),
        )
    finally:
        if own:
            provider.close()


def _house(c: Claim) -> int | None:
    for f in c.derived["facts"]:
        if f["key"].startswith("in_house("):
            return int(f["key"].rstrip(")").split(",")[-1])
    return None


def _body(c: Claim) -> str:
    for f in c.derived["facts"]:
        if f["key"].startswith("in_house("):
            return f["key"].split("(")[1].split(",")[0]
    return ""
