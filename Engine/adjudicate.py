"""Stage 7: adjudication over activated claims and doctrine-backed facts.

What this module does is narrower than the word "adjudication" usually
promises, and the narrowness is the point. The rule store has carried
`contradicts`, `extends` and `parallel_of` links since chapter 1 was encoded
and **no code has ever read them**, so a consultation could print a verse and
the translator's explicit refutation of that verse as two unrelated
paragraphs -- and Part 3's lexical pass, seeing "ruler" un-negated in both,
would report them as agreeing. That is the concrete defect this module exists
to fix, and fixing it needs no weighting scheme at all: it needs the engine to
read a relationship the encoder already recorded.

So there is no score anywhere in this file. There is no authority ranking, no
confidence, no precedence table, and no mechanism by which the engine can
decide that one book is more correct than another. Where the source states a
precedence the engine applies it and says which sentence it applied; where the
source states none the result is `unresolved`, both statements stand, and the
reader is told exactly why no choice was made. `unresolved` is a finished
answer here, not a placeholder.

Adjudication is a layer *above* the claims and never edits them. Stage 6's
claim list is identical with this module present and absent; what changes is
that the relationships between claims become visible. "What did the source
say?" and "how did the reasoning layer reconcile those statements?" are
answered by two different objects, on purpose.
"""

from __future__ import annotations

from dataclasses import dataclass

from .activate import Claim
from .facts import FactSet
from .rules import RELATION_LINKS, RuleCard

# Every relationship this module can name, and nothing else. A pair the store
# links in some way not covered here is left alone rather than forced into the
# nearest label -- see `_relationship`, which returns None for exactly that.
CONTRADICTION = "contradiction"
QUALIFICATION = "qualification"
PARALLEL_AUTHORITY = "parallel_authority"
OVERRIDE = "override"

RELATIONSHIPS = (CONTRADICTION, QUALIFICATION, PARALLEL_AUTHORITY, OVERRIDE)

# Three outcomes, no fourth, and none of them is a number.
#
#   applied     the source itself states which claim gives way, and it was
#               applied; the reason names the sentence that says so.
#   unresolved  both claims stand and the corpus contains no doctrine that
#               ranks them. A finished answer.
#   recorded    the other side is in the store but is not a claim about this
#               chart -- doctrine the engine cannot test, or an authority
#               reported rather than encoded. Nothing to weigh, so nothing is.
APPLIED = "applied"
UNRESOLVED = "unresolved"
RECORDED = "recorded"

RESOLUTIONS = (APPLIED, UNRESOLVED, RECORDED)


@dataclass(frozen=True)
class Party:
    """One side of a relationship, carrying its own provenance.

    A party is a *card*, not a claim, because one side of a real relationship
    is frequently doctrine that never fires -- another authority the translator
    reports, or a condition the corpus states but does not resolve into
    anything testable. `claim_ids` is empty for those, and empty is meaningful:
    it says this side is on record without being asserted about this nativity.
    """

    card: str
    book: str
    chapter: int
    verse: str
    page_anchor: str | None
    # Whom the card attributes its statement to. Frequently the book's own
    # author (one encoded chapter marks which of its verses are its own
    # author's and which are the translator relaying earlier writers), and
    # sometimes a different book entirely. The renderer must not turn the
    # first into the second.
    authority: str
    statement: str            # the card's own words, as displayed
    # "active" | "reference" | "inert". A reference party is doctrine the
    # engine reads and never asserts, which is a different kind of silence
    # from a rule whose conditions simply did not match.
    activation: str = "active"
    claim_ids: tuple[str, ...] = ()

    @property
    def activated(self) -> bool:
        return bool(self.claim_ids)


@dataclass(frozen=True)
class Adjudication:
    """One relationship between source-backed statements, and its outcome.

    `parties` is ordered and every entry keeps its card id, book, chapter,
    verse, page anchor and original wording, so any conclusion here can be
    walked back to the printed page. There is deliberately no field in which a
    number could be recorded.
    """

    subject: str                    # what the relationship is about, in this chart's terms
    relationship: str               # one of RELATIONSHIPS
    resolution: str                 # one of RESOLUTIONS
    reason: str                     # why, naming the doctrine or naming its absence
    parties: tuple[Party, ...]
    # The computed facts the relationship rests on, so a reader can check it
    # against Part 1 without re-deriving anything.
    basis: tuple[str, ...] = ()
    # How the store declares the relationship: the link field names for a
    # card-to-card relationship, empty for one an extractor found while
    # deriving the facts. Kept apart from `basis` because they answer different
    # questions -- what the relationship is about, and how the engine knows of
    # it at all.
    declared_as: tuple[str, ...] = ()

    @property
    def claim_ids(self) -> tuple[str, ...]:
        seen: list[str] = []
        for p in self.parties:
            for cid in p.claim_ids:
                if cid not in seen:
                    seen.append(cid)
        return tuple(seen)


# --- card links -------------------------------------------------------------

def _card_links(cards: list[RuleCard]) -> dict[tuple[str, str], set[str]]:
    """Every declared relationship, read undirected.

    The store declares these one-sidedly about half the time -- six of the
    links in the corpus today are asymmetric, and which end carries the
    declaration is an accident of which card was encoded second. A relationship
    that is only visible from one end is a relationship the engine would miss
    on the charts where the other card is the one that fires, so both ends are
    treated as declaring it.
    """
    links: dict[tuple[str, str], set[str]] = {}
    by_id = {c.id: c for c in cards}
    for card in cards:
        for rel in RELATION_LINKS:
            for other in card.raw.get(rel) or ():
                if other not in by_id or other == card.id:
                    continue
                key = (min(card.id, other), max(card.id, other))
                links.setdefault(key, set()).add(rel)
    return links


def _party(card: RuleCard, claim_ids: tuple[str, ...]) -> Party:
    quote = card.quote_display
    if isinstance(quote, list):          # multi-span card: its parts, in order
        quote = " […] ".join(quote)
    return Party(
        card=card.id,
        book=card.book_id,
        chapter=card.chapter,
        verse=card.verse,
        page_anchor=card.page_anchor,
        authority=str(card.predicts.get("authority", "") or ""),
        statement=quote,
        activation=card.activation,
        claim_ids=claim_ids,
    )


def _relationship(rels: set[str], a: RuleCard, b: RuleCard) -> str | None:
    """Which relationship a declared link stands for, read off the cards.

    Nothing here is a judgement about the astrology. Each branch reads a field
    the encoder wrote down while looking at the printed page:

    `parallel_of` is the one that has to be handled carefully, because it is
    genuinely overloaded in the store. It links a card to another *authority's*
    statement of the same doctrine -- two other books' definitions of the same
    five yogas, reported by the translator -- and it also links sibling cards
    cut from a single sentence, three readings of one verse that cannot all be
    true of one chart. Reporting the second kind as though a
    second authority had spoken would be a manufactured corroboration, so a
    `parallel_of` link counts only when the other side names an authority in
    `predicts.authority` -- which is precisely the field that distinguishes the
    two groups in the store today. Same-passage siblings are skipped, not
    guessed at.

    Even for the authority-naming kind the label is `parallel_authority` and
    **not** corroboration: the link records that another named authority speaks
    to the same doctrine, and it does not record whether that authority agrees.
    One of these cards (PD.06.Vesi.AuthoritativeWorks) actually reports a
    *different* condition for the same yoga. Calling that agreement would be
    the engine asserting a concord the store never claims.
    """
    if "contradicts" in rels:
        # A dissent that narrows rather than denies is a qualification, and the
        # store says which it is: the encoder records `polarity: "qualified"`
        # on the card that does the narrowing.
        if any(c.predicts.get("polarity") == "qualified" for c in (a, b)):
            return QUALIFICATION
        return CONTRADICTION
    if "extends" in rels:
        return QUALIFICATION
    if "parallel_of" in rels:
        if a.predicts.get("authority") or b.predicts.get("authority"):
            return PARALLEL_AUTHORITY
        return None
    return None


def _same_condition(a: RuleCard, b: RuleCard) -> bool:
    return a.conditions == b.conditions


def _basis(parties: tuple[Party, ...],
           claims_by_id: dict[str, Claim]) -> tuple[str, ...]:
    """The computed facts the activated side of this relationship turned on.

    Read off the claims rather than re-derived, so what is reported here is
    exactly what Stage 6 matched -- the same keys already printed against the
    rule card in Part 2.
    """
    keys: list[str] = []
    for p in parties:
        for cid in p.claim_ids:
            claim = claims_by_id.get(cid)
            if not claim:
                continue
            for k in claim.derived["conditions_satisfied"]:
                if k not in keys:
                    keys.append(k)
    return tuple(keys)


def _subject(parties: tuple[Party, ...], basis: tuple[str, ...]) -> str:
    """What this relationship is about, named from the chart where possible."""
    if basis:
        return ", ".join(basis)
    for p in parties:
        return f"{p.book} {p.chapter}.{p.verse}"
    return "?"


def _from_card_links(claims: list[Claim], cards: list[RuleCard]) -> list[Adjudication]:
    by_id = {c.id: c for c in cards}
    claims_by_id = {c.claim_id: c for c in claims}
    fired: dict[str, list[str]] = {}
    for c in claims:
        fired.setdefault(c.derived["rule_card"], []).append(c.claim_id)

    out: list[Adjudication] = []
    for (a_id, b_id), rels in sorted(_card_links(cards).items()):
        a, b = by_id[a_id], by_id[b_id]
        a_claims, b_claims = tuple(fired.get(a_id, ())), tuple(fired.get(b_id, ()))
        if not a_claims and not b_claims:
            # Neither side says anything about this nativity. The disagreement
            # is real and stays in the store; it is not a finding about this
            # chart and printing it here would pad the report with doctrine the
            # reading never touched.
            continue

        relationship = _relationship(rels, a, b)
        if relationship is None:
            continue

        # The activated side leads, so the reader meets the claim they already
        # read in Part 2 before the statement standing against it.
        pa, pb = _party(a, a_claims), _party(b, b_claims)
        parties = (pa, pb) if a_claims else (pb, pa)
        lead, other = parties

        if lead.activated and other.activated:
            resolution = UNRESOLVED
            reason = (
                "Both statements are activated by the same computed fact, and no "
                "card in the store gives either one precedence over the other. "
                "The engine does not choose between authorities, so both stand."
            )
            if relationship == QUALIFICATION and _same_condition(a, b):
                reason += (
                    " The qualifying statement carries no condition of its own "
                    "beyond the one it qualifies — it fires wherever that "
                    "statement fires — so the engine cannot test whether the "
                    "qualification is met on this chart. Reading it as met, or "
                    "as unmet, would both be inventions."
                )
        else:
            resolution = RECORDED
            reason = (
                f"`{other.card}` states doctrine the engine reads rather than a "
                f"rule that fires on a nativity"
                if other.activation == "reference"
                else f"`{other.card}`'s own conditions are not satisfied by this "
                     f"chart"
            ) + ", so it is not a claim here and there is nothing to weigh."

        basis = _basis(parties, claims_by_id)
        out.append(Adjudication(
            subject=_subject(parties, basis),
            relationship=relationship,
            resolution=resolution,
            reason=reason,
            parties=parties,
            basis=basis,
            declared_as=tuple(sorted(rels)),
        ))
    return out


# --- doctrine-backed facts --------------------------------------------------

def _cited(cards_by_id: dict[str, RuleCard], card_id: str,
           claim_ids: tuple[str, ...] = ()) -> Party | None:
    card = cards_by_id.get(card_id)
    return _party(card, claim_ids) if card else None


def _from_strength_facts(facts: FactSet, cards: list[RuleCard]) -> list[Adjudication]:
    """Relationships the strength extractor already resolved, made visible.

    Two shapes come out of `_strength`, and they are opposite outcomes of the
    same machinery. Where verse 4 prints its own override list -- weak "even
    though he may be posited in his sign of exaltation, in his own or a
    friend's sign" -- the extractor applies it and records which strong verdict
    gave way; that is an `applied` override, and the sentence authorising it is
    the source's, not the engine's. Where two verdicts collide with no such
    sentence, the extractor emits no fact at all. Both were already true before
    this module existed; neither was legible as a *relationship* in the output.
    """
    by_id = {c.id: c for c in cards}
    out: list[Adjudication] = []

    for f in sorted(facts.by_predicate("strength"), key=lambda x: x.key):
        overridden = f.evidence.get("overridden") or ()
        if not overridden:
            continue
        graha = f.args["graha"]
        winners = [a for a in f.evidence.get("authorities", ())]
        parties: list[Party] = []
        for a in winners:
            p = _cited(by_id, a.get("card", ""))
            if p:
                parties.append(p)
        for o in overridden:
            p = _cited(by_id, o.get("card", ""))
            if p:
                parties.append(p)
        if len(parties) < 2:
            continue
        gave_way = ", ".join(sorted(o.get("basis", "") for o in overridden))
        kept = ", ".join(sorted(a.get("basis", "") for a in winners))
        out.append(Adjudication(
            subject=f.key,
            relationship=OVERRIDE,
            resolution=APPLIED,
            reason=(
                f"The source states this precedence itself: the verse calling "
                f"{graha} weak ({kept}) says so of a graha that would otherwise "
                f"qualify as strong on the ground it names in its own sentence "
                f"({gave_way}). The engine applied the override the card carries "
                f"and nothing beyond it."
            ),
            parties=tuple(parties),
            basis=(f.key,),
        ))

    for record in facts.doctrine.conflicts_for("strength"):
        parties = [p for p in (_cited(by_id, cid) for cid in record["cards"]) if p]
        if not parties:
            continue
        out.append(Adjudication(
            subject=record["subject"],
            relationship=CONTRADICTION,
            resolution=UNRESOLVED,
            reason=record["reason"],
            parties=tuple(parties),
            basis=tuple(record.get("basis", ())),
        ))
    return out


# --- entry point ------------------------------------------------------------

def adjudicate(claims: list[Claim], facts: FactSet,
               cards: list[RuleCard]) -> list[Adjudication]:
    """Every relationship between source-backed statements on this chart.

    Pure with respect to `claims` and `facts`: nothing is added, removed or
    rewritten, and running the pipeline without this call produces exactly the
    same claim list. Deterministic ordering -- unresolved relationships first,
    because a disagreement the corpus cannot settle is the most informative
    thing a reading of this kind can report, and it is the one an astrologer
    would have to weigh.
    """
    found = _from_card_links(claims, cards) + _from_strength_facts(facts, cards)
    order = {UNRESOLVED: 0, APPLIED: 1, RECORDED: 2}
    found.sort(key=lambda a: (order.get(a.resolution, 9), a.relationship, a.subject,
                              tuple(p.card for p in a.parties)))
    return found


def contested_claim_pairs(
    adjudications: list[Adjudication],
) -> frozenset[frozenset[str]]:
    """Claim pairs the *store* says pull against each other.

    Handed to Stage 7c so lexical recurrence cannot report a verse and its own
    refutation as agreeing. Before this existed the demo case did exactly that:
    a verse says the native will "shine like" a named king, the translator's
    note on that same verse says he "cannot shine like" him, the word "cannot"
    is not one of the negation cues, and Part 3 printed the king's name as
    *"asserted in 2 passages"* under a heading reading "Terms that recur
    without contradiction". The cue list was not the real problem and lengthening it
    would not have been the real fix: the contradiction was declared in the
    store all along and nothing read it.

    Only relationships that actually pull against each other are returned --
    a parallel authority is not a disagreement, and an override the source
    itself resolved is not one either.
    """
    out = set()
    for adj in adjudications:
        if adj.relationship not in (CONTRADICTION, QUALIFICATION):
            continue
        if adj.resolution != UNRESOLVED:
            continue
        ids = adj.claim_ids
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                out.add(frozenset((a, b)))
    return frozenset(out)


def verify_adjudications(adjudications: list[Adjudication],
                         claims: list[Claim],
                         cards: list[RuleCard]) -> list[str]:
    """Prove the adjudication layer invented nothing.

    The counterpart of Stage 9's quote check, and it exists for the same
    reason: an adjudication is a conclusion *about* sources, and a conclusion
    about sources that cannot be walked back to them is precisely the black box
    this project refuses to build. Every party must be a real card, every cited
    claim must exist and must belong to the card it is filed under, and every
    relationship and resolution must come from the closed vocabularies above --
    so a future extractor cannot quietly introduce a fifth outcome, or a score.
    """
    by_card = {c.id: c for c in cards}
    by_claim = {c.claim_id: c for c in claims}
    problems: list[str] = []

    for adj in adjudications:
        if adj.relationship not in RELATIONSHIPS:
            problems.append(
                f"{adj.subject}: unknown relationship {adj.relationship!r}")
        if adj.resolution not in RESOLUTIONS:
            problems.append(
                f"{adj.subject}: unknown resolution {adj.resolution!r}")
        if len(adj.parties) < 2:
            problems.append(
                f"{adj.subject}: {len(adj.parties)} part(y/ies); a relationship "
                f"needs at least two")
        if not adj.reason.strip():
            problems.append(f"{adj.subject}: no reason given")
        for p in adj.parties:
            card = by_card.get(p.card)
            if card is None:
                problems.append(
                    f"{adj.subject}: party {p.card} is not in the rule store")
                continue
            for cid in p.claim_ids:
                claim = by_claim.get(cid)
                if claim is None:
                    problems.append(
                        f"{adj.subject}: cites claim {cid}, which does not exist")
                elif claim.derived["rule_card"] != p.card:
                    problems.append(
                        f"{adj.subject}: claim {cid} is filed under {p.card} but "
                        f"was activated by {claim.derived['rule_card']}")
        # An unresolved relationship must rest on something this chart
        # produced, or it is a disagreement in the abstract being reported as a
        # finding about a nativity. There are two honest shapes and no third:
        # two activated claims pulling against each other, or doctrine that
        # collided on named chart facts (the retrograde-and-combust case, whose
        # parties are reference cards that never become claims). Requiring
        # activated claims alone would have rejected the second, which is the
        # case Stage 7 was built for.
        if adj.resolution == UNRESOLVED:
            activated = [p for p in adj.parties if p.activated]
            if len(activated) < 2 and not adj.basis:
                problems.append(
                    f"{adj.subject}: marked unresolved, but neither two of its "
                    f"parties are claims about this chart nor does it name the "
                    f"facts it rests on")
    return problems
