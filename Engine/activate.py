"""Stage 6 (activation) and Stage 9 (groundedness verification).

Activation turns a chart into the exact set of rule cards the corpus has for
it. There is no top-k and no relevance threshold: every card whose conditions
evaluate true is returned, so the system knows precisely what its books say
about this chart.

Verification then re-does the work from scratch. Stage 6's answer is not
trusted -- conditions are re-evaluated and quotes are re-read from disk.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from .chart import ChartBundle
from .facts import FactSet
from .rules import ALWAYS_CANDIDATE, RuleCard, build_predicate_index, evaluate


@dataclass(frozen=True)
class Claim:
    """One supported assertion, with all four provenance links (arch. 6.2)."""

    claim_id: str
    # 1 - astronomical
    astronomical: dict
    # 2 - derived rule
    derived: dict
    # 3 - source book
    source: dict
    # 4 - passage
    passage: dict

    weight: float
    specificity: int
    tier: int
    stability: str
    text: str            # the quoted statement, as displayed


def activate(
    chart: ChartBundle,
    facts: FactSet,
    cards: list[RuleCard],
    book_titles: dict[str, dict] | None = None,
) -> tuple[list[Claim], dict]:
    """Return every claim the corpus supports for this chart, plus a report."""
    by_id = {c.id: c for c in cards}
    index = build_predicate_index(cards)

    # Exact keys, plus the wildcard entries that quantified cards index under.
    candidates: set[str] = set(index.get(ALWAYS_CANDIDATE, ()))
    for key in facts.keys():
        candidates.update(index.get(key, ()))
    for f in facts:
        candidates.update(index.get(f"{f.predicate}:*", ()))

    claims: list[Claim] = []
    inert: list[str] = []
    out_of_scope: list[str] = []
    reference: list[str] = []

    for cid in sorted(candidates):
        card = by_id[cid]

        # A card may be recorded ahead of the engine that could run it. Its
        # conditions are then an approximation of what the passage says -- the
        # closest the current predicate vocabulary can express -- and firing on
        # them would assert more than the book does. `inert` is the author's
        # declaration that this card is knowledge, not yet a rule, and it is
        # honoured here rather than left to depend on a condition happening not
        # to match.
        if card.activation == "inert":
            inert.append(f"{cid}: recorded but declared inert; does not fire")
            continue

        # A reference card carries doctrine the engine must *read* -- which
        # graha rules which sign, where each is exalted -- rather than a rule
        # that fires on a chart. It is not deferred and not blocked: it is the
        # table an extractor consults. It asserts nothing about a nativity, so
        # it never becomes a claim.
        if card.activation == "reference":
            reference.append(f"{cid}: reference datum, not a predictive rule")
            continue

        # A rule stated for one sex must not be applied to the other, and must
        # not be applied at all when the record does not say. Two such rules can
        # be identical in every other respect, so this is the only thing keeping
        # them apart.
        want_sex = card.scope.get("sex")
        if want_sex and want_sex != chart.resolved_birth.get("sex", "unknown"):
            out_of_scope.append(
                f"{cid}: stated for a {want_sex} nativity; "
                f"record says {chart.resolved_birth.get('sex', 'unknown')}")
            continue

        ev = evaluate(card.conditions, facts)
        if ev.missing:
            inert.append(f"{cid}: unknown predicate(s) {list(ev.missing)}")
            continue
        if not ev.satisfied:
            continue

        # A quantified rule -- "a planet in his sign of exaltation" -- is
        # satisfied once per graha that satisfies it, and each becomes its own
        # claim. Reporting one claim for the card would force the prose to say
        # "some planet", which is exactly the vagueness the store exists to
        # prevent.
        for solution in ev.solutions:
            claims.append(_claim(
                len(claims) + 1, card, solution, chart, facts, book_titles))

    report = {
        "cards_in_store": len(cards),
        "candidates_from_index": len(candidates),
        "claims_activated": len(claims),
        "inert_cards": inert,
        "out_of_scope": out_of_scope,
        "reference_cards": reference,
    }
    return claims, report


def _claim(n, card, solution, chart, facts, book_titles) -> Claim:
    # Resolve the astronomical quantities behind each satisfying fact.
    quantities = []
    stability = "stable"
    for key in solution.bindings:
        f = facts.get(key)
        if f is None:
            continue
        if f.stability != "stable":
            stability = f.stability
        graha = f.args.get("graha")
        if graha and graha in chart.bodies:
            b = chart.bodies[graha]
            quantities.append({
                "name": f"{graha}.lon_sidereal",
                "value": round(b.lon, 6),
                "unit": "deg",
                "sign": b.sign,
                "deg_in_sign": round(b.deg_in_sign, 6),
                "nakshatra": b.nakshatra,
                "pada": b.pada,
                "retrograde": b.retrograde,
            })
        else:
            quantities.append({
                "name": "Ascendant.lon_sidereal",
                "value": round(chart.ascendant, 6),
                "unit": "deg",
                "sign": chart.ascendant_sign,
                "deg_in_sign": round(chart.ascendant % 30.0, 6),
            })

    meta = (book_titles or {}).get(card.book_id, {})
    return Claim(
        claim_id=f"clm-{n:04d}",
        astronomical={
            "bundle_id": chart.bundle_id,
            "settings": chart.settings,
            "backend": chart.backend["name"] + " " + chart.backend["library_version"],
            "quantities": quantities,
        },
        derived={
            "facts": [
                {"key": k,
                 "frame": facts.get(k).frame if facts.get(k) else {},
                 "evidence": facts.get(k).evidence if facts.get(k) else {}}
                for k in solution.bindings
            ],
            "rule_card": card.id,
            "conditions_satisfied": list(solution.bindings),
            "variables": solution.as_dict(),
        },
        source={
            "book_id": card.book_id,
            "book_title": meta.get("title", card.book_id),
            "author": meta.get("author", ""),
            "translator": meta.get("translator", ""),
            "chapter": card.chapter,
            "verse": card.verse,
            "tier": card.tier,
        },
        passage={
            "quote": card.quote,
            "quote_display": card.quote_display,
            "corpus_file": f"Knowledge/{card.book_id}.md",
            "char_span": list(card.char_span),
            "spans": [list(x) for x in card.spans],
            "quote_sha256": card.quote_sha256,
            "page_anchor": card.page_anchor,
            "span_trimmed": card.span_trimmed,
        },
        weight=card.weight,
        specificity=card.specificity,
        tier=card.tier,
        stability=stability,
        text=card.quote_display,
    )



# --- Stage 9 ----------------------------------------------------------------

@dataclass
class VerificationResult:
    ok: bool
    checks: dict = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)


def verify_claims(
    claims: list[Claim],
    facts: FactSet,
    chart: ChartBundle,
    cards: list[RuleCard],
    corpus_dir: str | Path,
) -> VerificationResult:
    """Re-derive everything. Nothing from Stage 6 is taken on trust."""
    corpus_dir = Path(corpus_dir)
    by_id = {c.id: c for c in cards}
    corpora: dict[str, str] = {}
    failures: list[str] = []

    n_quote = n_cond = n_num = 0

    for claim in claims:
        card = by_id.get(claim.derived["rule_card"])
        if card is None:
            failures.append(f"{claim.claim_id}: rule card missing from store")
            continue

        # (3) quote integrity, re-read from disk -- every span, not just the
        # first, or a two-span card would be verified on half its evidence.
        book = card.book_id
        if book not in corpora:
            corpora[book] = (corpus_dir / f"{book}.md").read_bytes().decode("utf-8")
        text = corpora[book]
        if any(text[s:e] != part
               for (s, e), part in zip(card.spans, card.quote_parts)):
            failures.append(f"{claim.claim_id}: quote no longer matches corpus")
        elif hashlib.sha256(
            claim.passage["quote"].encode("utf-8")
        ).hexdigest() != claim.passage["quote_sha256"]:
            failures.append(f"{claim.claim_id}: quote hash mismatch")
        else:
            n_quote += 1

        # (4) conditions re-evaluated from scratch against the FactSet
        ev = evaluate(card.conditions, facts)
        want = set(claim.derived["conditions_satisfied"])
        if not ev.satisfied:
            failures.append(
                f"{claim.claim_id}: conditions of {card.id} do not hold on re-evaluation"
            )
        elif not any(set(s.bindings) == want for s in ev.solutions):
            # A quantified card has one solution per graha that satisfies it.
            # The claim must correspond to one of them exactly -- not merely to
            # the card having been satisfied by something.
            failures.append(
                f"{claim.claim_id}: no re-derived solution of {card.id} matches "
                f"its bindings {sorted(want)}"
            )
        else:
            n_cond += 1

        # (5) numeric grounding: every quantity must match the ChartBundle
        bad = False
        for q in claim.astronomical["quantities"]:
            body_name = q["name"].split(".")[0]
            if body_name == "Ascendant":
                expected = round(chart.ascendant, 6)
            else:
                b = chart.bodies.get(body_name)
                expected = round(b.lon, 6) if b else None
            if expected is None or abs(expected - q["value"]) > 1e-9:
                failures.append(
                    f"{claim.claim_id}: {q['name']} = {q['value']} is not in the ChartBundle"
                )
                bad = True
        if not bad:
            n_num += 1

    checks = {
        "claims": len(claims),
        "quote_integrity_passed": n_quote,
        "conditions_reevaluated_passed": n_cond,
        "numeric_grounding_passed": n_num,
    }
    return VerificationResult(ok=not failures, checks=checks, failures=failures)
