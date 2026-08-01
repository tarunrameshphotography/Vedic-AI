"""Stage 7c/8: synthesis over activated claims.

The hard constraint on this module: it must draw threads together without
asserting any astrology of its own. It therefore synthesises only over things
that are *measurable in the activated passages themselves* --

  * where the applicable passages concentrate (which houses, which bodies),
  * which content words recur across two or more independent passages, and
    whether each occurrence is asserted or negated in its own sentence.

"Asserted" means the word stands un-negated in its passage. It does NOT mean
the passage is favourable: "troubled by the enemies" asserts *enemies*, and
that is bad news for the native. Lexical polarity is not benefit, and this
module does not attempt benefit.

Both are facts about the retrieved text, checkable by re-reading it. Neither
requires the engine to know what any word means astrologically. A recurring
term is reported with its passages attached so the texts, not this module,
carry the meaning.

What this deliberately does NOT do: weigh planets by strength, rank houses by
importance, resolve a tension between two passages, or decide that a theme is
"strong". Those need doctrine the rule store does not yet hold.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .activate import Claim

# Function words, plus the vocabulary every passage in a planet-in-house
# chapter shares ("native", "birth", "house", body names). Neither carries a
# theme, and leaving them in would make every chart look identical.
STOPWORDS = frozenset("""
a an and are as at be been being but by for from had has have he her here him his
if in into is it its of on or our she that the their them then there these they
this those to was were what when where which who will with would you your
also very such more most other others than then upon while whose about
native person born birth house houses bhava lagna ascendant chart horoscope
concerned himself herself become becomes becoming
sun moon mars mercury jupiter venus saturn rahu ketu planet planets
occupy occupies occupying occupied posited placed placement situated
first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth
make makes made making give gives given giving enable enables enabling
cause causes causing render renders declared declares happen happens
""".split())

# Cues that flip the sense of a nearby term. Linguistic, not astrological, and
# reported as a heuristic -- the quote itself is always shown alongside.
#
# This list is necessarily incomplete: English has no closed class of negating
# verbs. It was extended once already after "He will destroy his wealth" was
# read as asserting wealth. Treat any addition as evidence that the check is a
# reading aid and not a truth function.
NEGATION_CUES = frozenset("""
no not without devoid bereft deprived deprive deprives depriving lose loses lost
loss never nor seldom hardly little few destitute lacking lacks lack
destroy destroys destroying squander squanders squandering waste wastes
ruin ruins ruined denied deprivation
""".split())

NEGATION_WINDOW = 6      # tokens before the term
MIN_TERM_LEN = 4
MIN_CLAIMS_FOR_THEME = 2
GROUP_PREFIX = 5         # "wealth"/"wealthy" group; "longlived"/"longevity" do not

_TOKEN_RE = re.compile(r"[A-Za-z]+")


@dataclass(frozen=True)
class Occurrence:
    claim_id: str
    word: str            # the token as it appears in the passage
    negated: bool
    cue: str | None      # the negation cue that fired, if any


@dataclass(frozen=True)
class Theme:
    term: str                          # display form (shortest variant)
    variants: tuple[str, ...]
    occurrences: tuple[Occurrence, ...]

    @property
    def claim_ids(self) -> tuple[str, ...]:
        seen, out = set(), []
        for o in self.occurrences:
            if o.claim_id not in seen:
                seen.add(o.claim_id)
                out.append(o.claim_id)
        return tuple(out)

    @property
    def asserted(self) -> tuple[str, ...]:
        return tuple(o.claim_id for o in self.occurrences if not o.negated)

    @property
    def negated(self) -> tuple[str, ...]:
        return tuple(o.claim_id for o in self.occurrences if o.negated)

    @property
    def contested(self) -> bool:
        return bool(self.asserted) and bool(self.negated)


@dataclass(frozen=True)
class Concentration:
    house: int
    bodies: tuple[str, ...]
    claim_ids: tuple[str, ...]


@dataclass(frozen=True)
class SynthesisResult:
    concentrations: tuple[Concentration, ...]
    themes: tuple[Theme, ...]
    method_note: str
    total_claims: int


def _tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in _TOKEN_RE.finditer(text)]


def _negated_at(toks: list[str], i: int) -> tuple[bool, str | None]:
    lo = max(0, i - NEGATION_WINDOW)
    for j in range(i - 1, lo - 1, -1):
        if toks[j] in NEGATION_CUES:
            return True, toks[j]
    return False, None


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


def synthesise(claims: list[Claim]) -> SynthesisResult:
    """Measure recurrence and concentration across the activated passages."""
    # --- where the passages concentrate -------------------------------------
    by_house: dict[int, list[Claim]] = {}
    for c in claims:
        h = _house_of(c)
        if h is not None:
            by_house.setdefault(h, []).append(c)

    concentrations = tuple(
        Concentration(
            house=h,
            bodies=tuple(_body_of(c) for c in cs),
            claim_ids=tuple(c.claim_id for c in cs),
        )
        for h, cs in sorted(by_house.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        if len(cs) > 1
    )

    # --- which content words recur ------------------------------------------
    # group key -> variant -> occurrences
    groups: dict[str, dict[str, list[Occurrence]]] = {}
    for c in claims:
        toks = _tokens(c.passage["quote_display"])
        seen_here: set[str] = set()
        for i, t in enumerate(toks):
            if len(t) < MIN_TERM_LEN or t in STOPWORDS:
                continue
            key = t[:GROUP_PREFIX]
            # count a term once per passage, at its first occurrence
            if (key, c.claim_id) in seen_here:
                continue
            seen_here.add((key, c.claim_id))
            neg, cue = _negated_at(toks, i)
            groups.setdefault(key, {}).setdefault(t, []).append(
                Occurrence(c.claim_id, t, neg, cue)
            )

    themes: list[Theme] = []
    for key, variants in groups.items():
        occs = [o for vs in variants.values() for o in vs]
        if len({o.claim_id for o in occs}) < MIN_CLAIMS_FOR_THEME:
            continue
        display = min(variants, key=lambda v: (len(v), v))
        themes.append(Theme(
            term=display,
            variants=tuple(sorted(variants)),
            occurrences=tuple(sorted(occs, key=lambda o: o.claim_id)),
        ))

    # Contested themes first -- a disagreement between two passages is the most
    # informative thing a reading of this kind can surface.
    themes.sort(key=lambda t: (not t.contested, -len(t.claim_ids), t.term))

    note = (
        f"Recurrence is measured over the {len(claims)} passages activated for this "
        f"chart. A term is reported when it appears in at least "
        f"{MIN_CLAIMS_FOR_THEME} passages from different verses. Asserted/negated is "
        # sorted() BEFORE slicing. Slicing the frozenset first samples set
        # iteration order, which varies between processes -- the same chart
        # would render a different method note on every run.
        f"decided by negation cue words ({', '.join(sorted(NEGATION_CUES)[:6])}, …) "
        f"within {NEGATION_WINDOW} tokens before the term; it is a reading aid, and "
        f"the quoted passage is always authoritative."
    )
    return SynthesisResult(
        concentrations=concentrations,
        themes=tuple(themes),
        method_note=note,
        total_claims=len(claims),
    )


_ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th",
        7: "7th", 8: "8th", 9: "9th", 10: "10th", 11: "11th", 12: "12th"}


def _join(names) -> str:
    names = list(names)
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


def narrate(result: SynthesisResult) -> list[tuple[str, tuple[str, ...]]]:
    """Compose the synthesis as sentences, each carrying its claim ids.

    The connective language here ("two passages concern", "recurs across") is
    about the corpus, not about the chart. Every astrological word in the
    output belongs to a quoted passage.
    """
    out: list[tuple[str, tuple[str, ...]]] = []

    for con in result.concentrations:
        out.append((
            f"{len(con.claim_ids)} of the {result.total_claims} applicable passages "
            f"concern the {_ORD[con.house]} house, where {_join(con.bodies)} fall.",
            con.claim_ids,
        ))

    for theme in result.themes:
        variants = ("/".join(theme.variants)
                    if len(theme.variants) > 1 else theme.variants[0])
        if theme.contested:
            text = (
                f"“{variants}” recurs in {len(theme.claim_ids)} passages and the texts "
                f"do not agree: asserted in {len(theme.asserted)} "
                f"({', '.join(theme.asserted)}), negated in {len(theme.negated)} "
                f"({', '.join(theme.negated)})."
            )
        elif theme.negated:
            text = (
                f"“{variants}” is negated in all {len(theme.negated)} passages that "
                f"mention it ({', '.join(theme.negated)})."
            )
        else:
            text = (
                f"“{variants}” is asserted in all {len(theme.asserted)} passages that "
                f"mention it ({', '.join(theme.asserted)})."
            )
        out.append((text, theme.claim_ids))

    return out


def verify_synthesis(result: SynthesisResult, claims: list[Claim]) -> list[str]:
    """Prove the synthesis says nothing the passages do not contain.

    Every reported occurrence must be a word actually present in the passage it
    is attributed to, and every cited claim must exist. This is the synthesis
    counterpart of the quote-integrity check.
    """
    by_id = {c.claim_id: c for c in claims}
    problems: list[str] = []

    for theme in result.themes:
        for occ in theme.occurrences:
            claim = by_id.get(occ.claim_id)
            if claim is None:
                problems.append(f"theme '{theme.term}': unknown claim {occ.claim_id}")
                continue
            if occ.word not in _tokens(claim.passage["quote_display"]):
                problems.append(
                    f"theme '{theme.term}': word {occ.word!r} is not in {occ.claim_id}"
                )
            if occ.negated and occ.cue not in _tokens(claim.passage["quote_display"]):
                problems.append(
                    f"theme '{theme.term}': negation cue {occ.cue!r} not in {occ.claim_id}"
                )

    for con in result.concentrations:
        for cid in con.claim_ids:
            if cid not in by_id:
                problems.append(f"house {con.house}: unknown claim {cid}")
            elif _house_of(by_id[cid]) != con.house:
                problems.append(
                    f"house {con.house}: {cid} is not actually in that house"
                )
    return problems
