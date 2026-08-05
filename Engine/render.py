"""Stage 8 (composition) and Stage 10 (rendering).

The consultation is rendered in three parts that are never allowed to blur:

  Part 1  Objective chart facts      -- computed. No doctrine, no citation.
  Part 2  Activated classical rules  -- quoted. Every one cited to the page.
  Part 3  Synthesised interpretation -- measured over Part 2. Nothing new.

Part 3 is the only place the system speaks in its own voice, and even there
every astrological word belongs to a quoted passage; the system's own language
is confined to describing what the passages do.

Stage 8 uses no language model. `QuotingSynthesizer` composes by quotation, so
nothing can be invented. That is the seam where a model-backed synthesizer
drops in: same `compose` signature, and Stage 9 rejects any sentence that does
not carry the claim ids it derives from.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .activate import Claim
from .chart import ChartBundle
from .facts import VOCABULARY, FactSet
from .synthesis import SynthesisResult, narrate

ORDINAL = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th",
           7: "7th", 8: "8th", 9: "9th", 10: "10th", 11: "11th", 12: "12th"}

# Navigation labels only. These are NOT sourced from the corpus and are never
# used as a claim, a condition, or an input to synthesis -- they exist so a
# reader can find their way down the page. House significations proper are
# doctrine and would have to come from rule cards.
HOUSE_LABEL_UNSOURCED = {
    1: "1st house", 2: "2nd house", 3: "3rd house", 4: "4th house",
    5: "5th house", 6: "6th house", 7: "7th house", 8: "8th house",
    9: "9th house", 10: "10th house", 11: "11th house", 12: "12th house",
}


@dataclass(frozen=True)
class Sentence:
    text: str
    claim_ids: tuple[str, ...]
    part: str = "rules"          # "rules" | "synthesis"


class Synthesizer(Protocol):
    def compose(self, claims: list[Claim], chart: ChartBundle) -> list[Sentence]: ...


class QuotingSynthesizer:
    """Composes by quotation. Generates nothing, so invents nothing."""

    def compose(self, claims: list[Claim], chart: ChartBundle) -> list[Sentence]:
        return [Sentence(c.text, (c.claim_id,), "rules") for c in claims]


def synthesis_sentences(result: SynthesisResult) -> list[Sentence]:
    return [Sentence(t, ids, "synthesis") for t, ids in narrate(result)]


# --- helpers ----------------------------------------------------------------

def _dms(deg_in_sign: float) -> str:
    d = int(deg_in_sign)
    m = int(round((deg_in_sign - d) * 60))
    if m == 60:
        d, m = d + 1, 0
    return f"{d}°{m:02d}'"


def _citation(claim: Claim) -> str:
    s = claim.source
    who = ", ".join(x for x in (s.get("author"), s.get("translator")) if x)
    anchor = claim.passage.get("page_anchor") or ""
    page = anchor.split("/p")[-1].lstrip("0") if "/p" in anchor else "?"
    return (f"{s['book_title']} {s['chapter']}.{s['verse']}"
            f"{' — ' + who if who else ''} · printed p. {page}")


def _house_of(claim: Claim) -> int | None:
    for f in claim.derived["facts"]:
        if f["key"].startswith("in_house("):
            return int(f["key"].rstrip(")").split(",")[-1])
    return None


def _body_of(claim: Claim) -> str:
    for f in claim.derived["facts"]:
        if f["key"].startswith("in_house("):
            return f["key"].split("(")[1].split(",")[0]
    return "?"


# --- the consultation -------------------------------------------------------

def consultation(
    chart: ChartBundle,
    facts: FactSet,
    claims: list[Claim],
    sentences: list[Sentence],
    synthesis: SynthesisResult,
    coverage: dict,
) -> str:
    rb = chart.resolved_birth
    L: list[str] = []
    A = L.append

    A(f"# Consultation — {rb.get('place_name') or 'birth chart'}")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| Born | {rb['date']} {rb['time']} local ({rb['utc_offset']}, {rb['timezone']}) |")
    A(f"| UTC instant | {rb['utc_instant']} |")
    A(f"| Place | {rb['latitude']:.4f}, {rb['longitude']:.4f} |")
    A(f"| Time precision | {rb['time_precision']} (source: {rb['time_source']}) |")
    A("")
    for w in rb.get("warnings", []):
        A(f"> **Caution.** {w}")
        A("")

    # ---------------------------------------------------------------- Part 1
    A("---")
    A("")
    A("## Part 1 — Objective chart facts")
    A("")
    A("Computed from the ephemeris. Nothing here is doctrine and nothing here is "
      "interpreted; these are the quantities every later part is derived from.")
    A("")
    A(f"**Ascendant** {chart.ascendant_sign} {_dms(chart.ascendant % 30)} "
      f"({chart.ascendant:.4f}° sidereal)  ")
    A(f"**Ayanamsa** {chart.settings['ayanamsa']} "
      f"{chart.settings['ayanamsa_value']:.4f}° · "
      f"**Houses** {chart.houses['system'].replace('_', ' ')} · "
      f"**Nodes** {chart.settings['node_type']}")
    A("")
    A(f"> The ayanamsa and node type are engine choices, not doctrine — the "
      f"classical texts do not specify either. Recorded as "
      f"`{', '.join(chart.settings['unsourced_engine_choices'])}`.")
    A("")

    A("### Planetary positions")
    A("")
    A("| Body | Sidereal longitude | Sign | Deg. in sign | House | Nakshatra (pada) | Retro |")
    A("|---|---|---|---|---|---|---|")
    for b in chart.bodies.values():
        A(f"| {b.body} | {b.lon:.4f}° | {b.sign} | {_dms(b.deg_in_sign)} | {b.house} "
          f"| {b.nakshatra} ({b.pada}) | {'R' if b.retrograde else '—'} |")
    A("")

    A("### Houses")
    A("")
    A("| House | Sign | Occupants |")
    A("|---|---|---|")
    for i, sign in enumerate(chart.houses["signs"], start=1):
        occ = [b.body for b in chart.bodies.values() if b.house == i]
        A(f"| {i} | {sign} | {', '.join(occ) if occ else '—'} |")
    A("")

    A("### Derived facts")
    A("")
    A(f"{len(facts)} facts were derived from the positions above. These are the "
      f"exact keys the rule store is queried with — an exact-match lookup, so "
      f"\"Mars in the 7th\" can never be confused with \"Mars in the 8th\".")
    A("")
    A("<details><summary>All derived fact keys</summary>")
    A("")
    for pred in ("lagna_sign", "in_house", "in_sign", "in_nakshatra", "retrograde"):
        keys = [f.key for f in facts.by_predicate(pred)]
        if keys:
            A(f"- `{pred}` — " + ", ".join(f"`{k}`" for k in keys))
    A("")
    A("</details>")
    A("")
    A(f"**Invariants checked:** {', '.join(chart.invariants_checked)}")
    A("")

    # ---------------------------------------------------------------- Part 2
    A("---")
    A("")
    A("## Part 2 — Activated classical rules")
    A("")
    A(f"{coverage['cards_in_store']} rule cards are in the store. The predicate "
      f"index returned {coverage['candidates_from_index']} candidates for this "
      f"chart; after evaluating each card's full conditions, "
      f"**{coverage['claims_activated']}** rules apply.")
    A("")
    A("Each entry below is a passage printed in a classical text, activated because "
      "a computed fact satisfied its conditions. The words are the book's; nothing "
      "is paraphrased.")
    A("")

    by_id = {c.claim_id: c for c in claims}
    grouped: dict[int, list[Sentence]] = {}
    for s in sentences:
        if s.part != "rules":
            continue
        # A card keyed on the ascendant's sign rather than on a body in a house
        # has no house of its own. Grouping it at 0 renders it first, which is
        # also where a reading starts. Dropping it -- which is what happened
        # before chapter 9 gave the store its first such card -- would let an
        # activated rule vanish from the report while Stage 9 still passed.
        h = _house_of(by_id[s.claim_ids[0]])
        grouped.setdefault(0 if h is None else h, []).append(s)

    for house in sorted(grouped):
        if house == 0:
            A(f"### The Ascendant — {chart.ascendant_sign}")
        else:
            A(f"### {HOUSE_LABEL_UNSOURCED[house]} — {chart.houses['signs'][house - 1]}")
        A("")
        for s in grouped[house]:
            claim = by_id[s.claim_ids[0]]
            body = _body_of(claim)
            b = chart.bodies.get(body)
            p = claim.passage
            if b is None:
                A(f"**Ascendant** in {chart.ascendant_sign} "
                  f"{_dms(chart.ascendant % 30)}")
            else:
                A(f"**{body}** in {b.sign} {_dms(b.deg_in_sign)}"
                  f"{', retrograde' if b.retrograde else ''} "
                  f"→ house {house}")
            A("")
            A(f"> {s.text}")
            A("")
            A(f"- **Source** — {_citation(claim)}")
            A(f"- **Rule card** — `{claim.derived['rule_card']}` "
              f"(tier {claim.tier}), triggered by "
              f"{', '.join('`' + k + '`' for k in claim.derived['conditions_satisfied'])}")
            A(f"- **Page anchor** — `{p['page_anchor']}` · "
              f"`{p['corpus_file']}` chars {p['char_span'][0]}–{p['char_span'][1]}")
            A(f"- **Claim** — `{claim.claim_id}`")
            A("")

    # ---------------------------------------------------------------- Part 3
    A("---")
    A("")
    A("## Part 3 — Synthesised interpretation")
    A("")
    A("This is the only section in the system's own voice. It states nothing about "
      "the chart that Part 2 does not already say; it reports where the applicable "
      "passages concentrate and which of their terms recur, so the reading can be "
      "seen as a whole rather than as nine separate verdicts.")
    A("")

    if synthesis.concentrations:
        A("### Where the texts concentrate")
        A("")
        for s in sentences:
            if s.part == "synthesis" and "concern the" in s.text:
                A(f"- {s.text} `{'`, `'.join(s.claim_ids)}`")
        A("")

    contested = [t for t in synthesis.themes if t.contested]
    settled = [t for t in synthesis.themes if not t.contested]

    if contested:
        A("### Where the texts pull against each other")
        A("")
        A("These terms appear in more than one applicable passage, standing plain in "
          "some and negated in others. A tension of this kind is a finding, not an "
          "error: it is what an astrologer would have to weigh, and the system has "
          "no doctrine yet with which to weigh it.")
        A("")
        A("*“Asserted” means the word stands un-negated in its passage — not that "
          "the passage is favourable. “Troubled by the enemies” asserts* enemies.")
        A("")
        for t in contested:
            A(f"**“{'/'.join(t.variants)}”**")
            A("")
            for occ in t.occurrences:
                mark = "negated " if occ.negated else "asserted"
                cue = f" (cue: *{occ.cue}*)" if occ.cue else ""
                claim = by_id[occ.claim_id]
                A(f"- {mark} — {_body_of(claim)} in house {_house_of(claim)} · "
                  f"`{occ.claim_id}` · {_citation(claim)}{cue}")
            A("")

    if settled:
        A("### Terms that recur without contradiction")
        A("")
        for t in settled:
            ids = "`, `".join(t.claim_ids)
            verdict = "asserted" if t.asserted else "negated"
            A(f"- **“{'/'.join(t.variants)}”** — {verdict} in "
              f"{len(t.claim_ids)} passages: `{ids}`")
        A("")

    if not synthesis.themes and not synthesis.concentrations:
        A("No term recurs across two or more of the applicable passages, and no "
          "house carries more than one. This reading does not converge; the "
          "passages stand separately.")
        A("")

    A("> **Method.** " + synthesis.method_note)
    A("")

    # ---------------------------------------------------------------- scope
    A("---")
    A("")
    A("## Scope and silence")
    A("")
    A("**Doctrine loaded**")
    A("")
    for line in coverage.get("loaded_doctrine", []):
        A(f"- {line}")
    A("")
    # Derived, not asserted. This paragraph used to claim the reading covered
    # "only the placement of each body in a house", which stopped being true the
    # moment lordship, aspects, dignity and nature began producing facts. A
    # hardcoded description of the engine's reach goes stale silently, so the
    # reach is read off the FactSet instead.
    A("**What this reading was able to reason with**")
    A("")
    derived = sorted({f.predicate for f in facts})
    A(", ".join(f"`{p}`" for p in derived))
    A("")
    absent = sorted(set(VOCABULARY) - set(derived))
    if absent:
        A("**Not derived for this chart**")
        A("")
        A(", ".join(f"`{p}`" for p in absent))
        A("")
        A("A predicate is missing here either because this chart does not exhibit "
          "it or because no extractor can yet produce it at all. The two are not "
          "distinguished in this list; `Reports/PHASE3_BACKLOG.md` says which is "
          "which.")
        A("")

    if facts.doctrine.partial:
        A("**Doctrine read, but not complete**")
        A("")
        A("These extractors found their doctrine, read it, and it did not cover "
          "everything. This is the most easily missed kind of silence, because "
          "the extractor did not fail:")
        A("")
        for extractor, reason in sorted(facts.doctrine.partial.items()):
            A(f"- `{extractor}` — {reason}")
        A("")

    if facts.doctrine.skipped:
        A("**Doctrine absent, extractor skipped**")
        A("")
        for extractor, reason in sorted(facts.doctrine.skipped.items()):
            A(f"- `{extractor}` — {reason}")
        A("")

    A("Where this reading is silent, the texts have not been consulted — not that "
      "the texts are silent.")
    A("")
    if coverage.get("not_covered"):
        A("No rule card was found for:")
        A("")
        for gap in coverage["not_covered"]:
            A(f"- {gap}")
        A("")
    return "\n".join(L)


# --- audit ------------------------------------------------------------------

def audit_view(claims: list[Claim], chart: ChartBundle, verification) -> str:
    L: list[str] = []
    A = L.append
    A("# Audit view")
    A("")
    A(f"**Bundle** `{chart.bundle_id}`  ")
    A(f"**Engine** {chart.engine_version} · **Backend** "
      f"{chart.backend['name']} {chart.backend['library_version']} "
      f"({chart.backend['data_source']}) · ΔT {chart.backend['delta_t_seconds']:.3f}s  ")
    A(f"**Invariants** {', '.join(chart.invariants_checked)}")
    A("")
    A("## Stage 9 — verification")
    A("")
    A(f"- Result: **{'PASS' if verification.ok else 'FAIL'}**")
    for k, v in verification.checks.items():
        A(f"- {k}: {v}")
    for f in verification.failures:
        A(f"- FAIL {f}")
    A("")
    A("## Claims — the four provenance links")
    A("")
    for c in claims:
        A(f"### `{c.claim_id}` — rule card `{c.derived['rule_card']}`")
        A("")
        A("**1 · Astronomical**")
        for q in c.astronomical["quantities"]:
            extra = f", {q['nakshatra']} pada {q['pada']}" if "nakshatra" in q else ""
            A(f"- `{q['name']}` = {q['value']}° ({q['sign']} "
              f"{q['deg_in_sign']:.4f}°{extra})")
        A(f"- ayanamsa={c.astronomical['settings']['ayanamsa']} "
          f"({c.astronomical['settings']['ayanamsa_value']:.6f}°), "
          f"houses={c.astronomical['settings']['house_system']}")
        A("")
        A("**2 · Derived rule**")
        for f in c.derived["facts"]:
            A(f"- fact `{f['key']}` — frame {f['frame']}")
        A(f"- conditions satisfied: {list(c.derived['conditions_satisfied'])}")
        # What each variable stood for. For a quantified rule this names the
        # graha; for a counting rule the bound value *is* the number the verse
        # asks for, so leaving it out would hide the claim's whole content.
        if c.derived.get("variables"):
            A("- variables bound: " + ", ".join(
                f"`{k}` = {v}" for k, v in sorted(c.derived["variables"].items())))
        A("")
        A("**3 · Source book**")
        s = c.source
        A(f"- {s['book_title']}, ch. {s['chapter']}, v. {s['verse']} — "
          f"{s['author']}, tr. {s['translator']} (tier {s['tier']})")
        A("")
        A("**4 · Passage**")
        p = c.passage
        A(f"- `{p['corpus_file']}` chars {p['char_span'][0]}–{p['char_span'][1]}")
        A(f"- sha256 `{p['quote_sha256'][:32]}…`")
        A(f"- page anchor `{p['page_anchor']}`")
        if p.get("span_trimmed"):
            A(f"- span trimmed: {p['span_trimmed']}")
        A(f"- > {p['quote_display']}")
        A("")
    return "\n".join(L)
