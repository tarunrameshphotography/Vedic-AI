"""Engine.pipeline.Result -> JSON.

Extends `Engine/cli.py`'s own `--json` trace (chart/facts/claims/coverage/
verification) to also cover adjudications, sentences/synthesis, the audit
text, and the mahadasa timeline -- the same dataclass-to-dict field
selection that adapter already uses, not a new serialization convention.

This module contains no astrology. It re-shapes what `Engine.pipeline.run`
already returned; every value here traces to a `Result` field or to
`Engine.dasa.chart_mahadasa_timeline`, which is itself Stage 9's own
window-re-derivation arithmetic, reused rather than duplicated.
"""

from __future__ import annotations

from dataclasses import asdict

from Engine.dasa import chart_mahadasa_timeline, jd_to_iso
from Engine.facts import FactSet
from Engine.pipeline import Result
from Engine.rules import RuleCard


def serialize_result(result: Result, cards: list[RuleCard]) -> dict:
    return {
        "chart": result.chart.to_dict(),
        "facts": _serialize_facts(result.facts),
        "claims": [asdict(c) for c in result.claims],
        "adjudications": [_serialize_adjudication(a) for a in result.adjudications],
        "sentences": [asdict(s) for s in result.sentences],
        "synthesis": asdict(result.synthesis),
        "coverage": result.coverage,
        "verification": {
            "ok": result.verification.ok,
            "checks": result.verification.checks,
            "failures": result.verification.failures,
        },
        "dasa_timeline": _serialize_timeline(result, cards),
        "consultation": result.consultation,
        "audit": result.audit,
    }


def _serialize_facts(facts: FactSet) -> dict:
    return {
        "items": [asdict(f) for f in facts],
        "doctrine": {
            "consulted": facts.doctrine.consulted,
            "skipped": facts.doctrine.skipped,
            "partial": facts.doctrine.partial,
            "conflicts": facts.doctrine.conflicts,
        },
    }


def _serialize_adjudication(a) -> dict:
    d = asdict(a)
    # `claim_ids` is a computed property (dedup over both parties' own claim
    # lists), not a stored field -- `asdict` only walks declared fields, so it
    # is added here rather than left for the frontend to re-derive.
    d["claim_ids"] = list(a.claim_ids)
    return d


def _serialize_timeline(result: Result, cards: list[RuleCard]) -> list[dict]:
    """The full nine-period sequence, each period's own claims attached.

    A claim is "attached" to the period whose window it exactly matches --
    the same window `Claim.window` already carries, promoted from the bound
    `mahadasa_lord` fact's evidence at claim-construction time (see
    `Engine.activate._claim`). Pure grouping over data the engine already
    produced; no astrology decision is made here.
    """
    claim_ids_by_window: dict[tuple[str, str], list[str]] = {}
    for c in result.claims:
        if c.window is not None:
            key = (c.window["start"], c.window["end"])
            claim_ids_by_window.setdefault(key, []).append(c.claim_id)

    timeline = []
    for p in chart_mahadasa_timeline(result.chart, cards):
        start, end = jd_to_iso(p.start_jd), jd_to_iso(p.end_jd)
        timeline.append({
            "graha": p.graha,
            "ordinal": p.ordinal,
            "years": p.years,
            "start": start,
            "end": end,
            "balance_at_birth": p.balance_at_birth,
            "claim_ids": claim_ids_by_window.get((start, end), []),
        })
    return timeline
