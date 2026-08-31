"""Tests for Stage 7 -- adjudication over activated claims and derived facts.

The capability is a reader of relationships the rule store already declared,
not a scheme for deciding which book is right, and most of what follows exists
to keep it that way. The assertions that matter most are the refusals: that no
claim is added, removed or reworded by the layer above it; that a relationship
the corpus does not settle comes out `unresolved` rather than decided; that a
`parallel_of` link between two halves of one sentence is not reported as a
second authority; and that no number, score or ranking reaches the output.

The positive cases are three real ones, and each was found in the store rather
than constructed for the test:

  * `PD.09.Dignity.Exalted` against its own translator's note, the only
    claim-to-claim contradiction in the whole corpus and one that fires on any
    chart with an exalted graha;
  * the retrograde-and-combust collision inside the strength extractor
    (concept:retrograde-combust-collision), whose two sides are reference cards
    that never become claims at all;
  * `parallel_of` links to other books' definitions of the same five yogas.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.adjudicate import (
    APPLIED,
    CONTRADICTION,
    OVERRIDE,
    PARALLEL_AUTHORITY,
    QUALIFICATION,
    RECORDED,
    RELATIONSHIPS,
    RESOLUTIONS,
    UNRESOLVED,
    adjudicate,
    contested_claim_pairs,
    verify_adjudications,
)
from Engine.chart import BirthRecord
from Engine.pipeline import run
from Engine.rules import RELATION_LINKS, load_cards, verify_cards
from Engine.synthesis import synthesise

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"
CORPUS = ROOT / "Knowledge"


def _mumbai(date: str, time: str) -> BirthRecord:
    return BirthRecord(
        date=date, time=time, timezone="Asia/Kolkata",
        latitude=19.0760, longitude=72.8777, place_name="Mumbai",
        time_precision="minute", time_source="memory", sex="male")


# Mercury is retrograde here and counts as exalted by the retrograde-as-exalted
# override, so verse 14 and the translator's note on verse 14 both fire. Found
# by scanning 720 nativities; it is the smallest chart that exercises the only
# claim-to-claim contradiction the store contains.
EXALTED = _mumbai("1970-01-05", "02:15")

# Mercury is both retrograde and combust here, which is the collision the
# strength extractor refuses to resolve.
COLLISION = _mumbai("1985-03-29", "02:15")

# Mercury is exalted *and* combust here, which is the case verse 4 settles in
# its own sentence: weak "even though he may be posited in his sign of
# exaltation". The only `applied` resolution the corpus can currently produce,
# and the reason the state exists at all.
OVERRIDDEN = _mumbai("1960-09-13", "10:30")

# The project's standing demo nativity: no exalted graha, no collision. Used as
# the negative control -- relationships exist on it, but none is a conflict.
DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male")

# Saturn is exalted in Libra and in a kendra here, so PD.06.Sasa fires under
# Milestone 24's added v.9 strength gate -- the demo chart no longer does
# (PD.06.Ruchaka's Mars there is merely own-sign, which carries no strength
# verdict). Found by scanning; the smallest real instant that still exercises
# the parallel_of link to PD.06.PanchaMahapurusha.JatakaParijata now that the
# demo chart cannot.
MAHAPURUSHA = _mumbai("1960-05-16", "08:15")


@pytest.fixture(scope="module")
def cards():
    return load_cards(RULES)


@pytest.fixture(scope="module")
def exalted():
    return run(EXALTED)


@pytest.fixture(scope="module")
def collision():
    return run(COLLISION)


@pytest.fixture(scope="module")
def demo():
    return run(DEMO)


@pytest.fixture(scope="module")
def mahapurusha():
    return run(MAHAPURUSHA)


@pytest.fixture(scope="module")
def overridden():
    return run(OVERRIDDEN)


def _by_cards(adjs, *ids):
    want = set(ids)
    return [a for a in adjs if want <= {p.card for p in a.parties}]


# --- the layer must not touch what it reasons over --------------------------

def test_adjudication_adds_removes_and_rewords_no_claim(exalted, cards):
    """The whole architecture rests on this.

    Raw source claims stay authoritative and adjudication sits above them, so
    running the adjudicator must leave the claim list byte-identical. If this
    ever fails, "what did the source say?" and "how were those statements
    reconciled?" have stopped being separable answers.
    """
    before = [(c.claim_id, c.derived["rule_card"], c.text,
               tuple(c.derived["conditions_satisfied"])) for c in exalted.claims]
    adjudicate(exalted.claims, exalted.facts, cards)
    after = [(c.claim_id, c.derived["rule_card"], c.text,
              tuple(c.derived["conditions_satisfied"])) for c in exalted.claims]
    assert before == after


def test_adjudication_is_deterministic(exalted, cards):
    a = adjudicate(exalted.claims, exalted.facts, cards)
    b = adjudicate(exalted.claims, exalted.facts, cards)
    assert [(x.subject, x.relationship, x.resolution,
             tuple(p.card for p in x.parties)) for x in a] == \
           [(x.subject, x.relationship, x.resolution,
             tuple(p.card for p in x.parties)) for x in b]


def test_every_adjudication_is_grounded(exalted, collision, demo, cards):
    for result in (exalted, collision, demo):
        assert verify_adjudications(result.adjudications, result.claims, cards) == []
        assert result.verification.checks["adjudications_grounded"] is True


# --- contradiction: the one claim-to-claim case in the corpus ---------------

def test_the_exaltation_dispute_is_reported_and_not_decided(exalted):
    """Verse 14 and the note on verse 14 both fire, and neither is withdrawn.

    Before Stage 7 these were claims 23 and 24 in a list, with nothing saying
    they were about the same fact or that one denies the other -- while the
    store had carried a `contradicts` link between their cards since chapter 9
    was encoded.
    """
    hits = _by_cards(exalted.adjudications,
                     "PD.09.Dignity.Exalted", "PD.09.Dignity.Exalted.Notes")
    assert len(hits) == 1
    adj = hits[0]
    assert adj.resolution == UNRESOLVED
    assert adj.declared_as == ("contradicts",)
    # Both sides are claims about this chart, and both are still in Part 2.
    assert all(p.activated for p in adj.parties)
    fired = {c.derived["rule_card"] for c in exalted.claims}
    assert {"PD.09.Dignity.Exalted", "PD.09.Dignity.Exalted.Notes"} <= fired


def test_the_dissent_is_a_qualification_because_the_card_says_so(exalted):
    """`polarity: "qualified"` is the encoder's reading of the printed page.

    The note does not merely deny the verse; it states the conditions under
    which the verse's effect does obtain. Reading that as a flat contradiction
    would misreport the source in the opposite direction from ignoring it.
    """
    adj = _by_cards(exalted.adjudications,
                    "PD.09.Dignity.Exalted.Notes")[0]
    assert adj.relationship == QUALIFICATION


def test_an_unencodable_qualification_says_it_cannot_be_tested(exalted):
    """The honest half of the answer.

    The note's condition -- an auspicious house, free of malefic influence,
    supported by other combinations -- is not encoded, so the qualifying card
    carries no condition beyond the one it qualifies and fires wherever that
    one fires. The reason must say so; claiming the qualification is met, or
    that it is not, would both be inventions.
    """
    adj = _by_cards(exalted.adjudications, "PD.09.Dignity.Exalted.Notes")[0]
    assert "no condition of its own" in adj.reason
    assert "would both be inventions" in adj.reason


def test_the_dispute_names_the_computed_fact_both_sides_turn_on(exalted):
    adj = _by_cards(exalted.adjudications, "PD.09.Dignity.Exalted")[0]
    assert adj.basis
    for key in adj.basis:
        assert key in exalted.facts, key


# --- the chart-dependent collision ------------------------------------------

def test_the_retrograde_combust_collision_is_reported_as_a_relationship(collision):
    """concept:retrograde-combust-collision, promoted out of a prose aside.

    Both sides are reference cards that never become claims, so this is the
    case that proves adjudication cannot be defined over claims alone.
    """
    hits = _by_cards(collision.adjudications,
                     "PD.04.Strength.RetrogradeFive", "PD.04.Weakness.Combust")
    assert len(hits) == 1
    adj = hits[0]
    assert adj.relationship == CONTRADICTION
    assert adj.resolution == UNRESOLVED
    # Not declared between cards -- found while deriving the facts.
    assert adj.declared_as == ()
    assert all(not p.activated for p in adj.parties)


def test_the_collision_rests_on_facts_the_chart_actually_produced(collision):
    adj = _by_cards(collision.adjudications, "PD.04.Weakness.Combust")[0]
    assert set(adj.basis) == {"combust(Mercury)", "retrograde(Mercury)"}
    for key in adj.basis:
        assert key in collision.facts, key


def test_no_strength_verdict_is_emitted_for_the_collided_graha(collision):
    """Stage 7 reports the collision; it does not resolve it into a verdict.

    The refusal is the behaviour under test. An adjudication layer that made
    this graha strong or weak would have invented the precedence verse 4's own
    override list declines to state.
    """
    assert not [f for f in collision.facts.by_predicate("strength")
                if f.args["graha"] == "Mercury"]


def test_the_collision_appears_in_both_registers_without_being_decided(collision):
    """Coverage and relationship are different statements and both are true.

    "Mercury got no strength fact" belongs with the other silences; "these two
    verses disagree here" belongs with the other relationships, and only the
    second can carry the verses. Neither may imply a verdict was reached.
    """
    assert "strength" in collision.facts.doctrine.partial
    assert collision.facts.doctrine.conflicts_for("strength")
    text = collision.consultation
    assert "How the applicable passages stand to one another" in text
    assert "The engine emits no strength verdict for Mercury" in text


# --- parallel authorities ---------------------------------------------------

def test_another_books_definition_is_shown_without_asserting_agreement(mahapurusha):
    """`parallel_of` records that a second authority spoke, not that it agreed.

    One of these cards reports a *different* condition for the same yoga, so
    labelling the relation corroboration would manufacture a concord the store
    never claims. The relationship is that another named authority is on
    record; the reader compares the two statements.

    Uses the `mahapurusha` fixture, not `demo`: Milestone 24 added v.9's
    strength gate to all five Mahapurusha cards, and the demo chart's Mars
    (own sign, not exalted, not retrograde) no longer carries a strength
    verdict, so PD.06.Ruchaka no longer fires there and this relationship
    no longer appears on it.
    """
    hits = _by_cards(mahapurusha.adjudications, "PD.06.PanchaMahapurusha.JatakaParijata")
    assert hits
    adj = hits[0]
    assert adj.relationship == PARALLEL_AUTHORITY
    assert adj.resolution == RECORDED
    other = [p for p in adj.parties if not p.activated][0]
    assert other.authority          # the card names whose doctrine it reports
    assert other.activation == "reference"


SIBLINGS = ("PD.06.Varishtha", "PD.06.Sama", "PD.06.Adhama",
            "PD.06.Lakshmi", "PD.06.Gouri",
            "PD.06.Mahabhagya.Male", "PD.06.Mahabhagya.Female")


def test_siblings_of_one_sentence_name_no_authority(cards):
    """The discriminator's input: three readings of one verse are not three books.

    Varishtha, Sama and Adhama are `parallel_of` one another and are cut from
    a single sentence; so are Lakshmi/Gouri and the male/female pair. None
    names an authority, and neither does anything they point at -- which is
    what makes `predicts.authority` a sound test for "a second authority
    spoke" rather than a guess.
    """
    by_id = {c.id: c for c in cards}
    for cid in SIBLINGS:
        assert not by_id[cid].predicts.get("authority"), cid
        for target in by_id[cid].raw.get("parallel_of") or ():
            assert not by_id[target].predicts.get("authority"), (cid, target)


def test_no_parallel_authority_is_reported_without_a_named_authority(
        demo, exalted, collision, overridden):
    """The discriminator's *output*, which is the thing that can regress.

    A `parallel_of` link with no authority behind it must produce no
    relationship at all. Reporting one would be the engine manufacturing
    corroboration out of its own filing -- on the demo chart it would pair
    Adhama with Varishtha, two mutually exclusive readings of one sentence,
    and call the second a corroborating authority.
    """
    for result in (demo, exalted, collision, overridden):
        for adj in result.adjudications:
            if adj.relationship != PARALLEL_AUTHORITY:
                continue
            assert any(p.authority for p in adj.parties), \
                (adj.subject, [p.card for p in adj.parties])


def test_a_sibling_link_produces_no_relationship_at_all(demo, cards):
    """Checked on a chart that actually fires one of the siblings."""
    fired = {c.derived["rule_card"] for c in demo.claims}
    assert fired & set(SIBLINGS), "no sibling card fires on the demo chart"
    by_id = {c.id: c for c in cards}
    for adj in demo.adjudications:
        pair = {p.card for p in adj.parties}
        if len(pair & set(SIBLINGS)) == 2:
            raise AssertionError(
                f"two halves of one sentence reported as a relationship: {pair}")
        # A sibling paired with anything must be paired with a real authority.
        if pair & set(SIBLINGS):
            assert any(by_id[c].predicts.get("authority") for c in pair), pair


def test_a_relationship_touching_no_claim_is_not_reported(demo, cards):
    """Doctrine-level disputes stay in the store until a chart raises them.

    The three-way dispute over the nodes' exaltation signs is real and is
    linked with `contradicts`, but no side of it is a claim about any chart.
    Printing it in every consultation would pad the report with doctrine the
    reading never touched.
    """
    nodes = _by_cards(demo.adjudications,
                      "PD.01.Exaltation.RahuKetu.SarvarthChintamani")
    assert nodes == []


# --- what must never appear -------------------------------------------------

def test_no_adjudication_carries_a_number(exalted, collision, demo):
    """There is no field a score could live in, and none is smuggled into prose.

    The standing prohibition: the engine may not decide that one book is more
    correct than another, and an authority ranking expressed as a percentage in
    a `reason` string would be the same violation as a numeric field.
    """
    import re
    for result in (exalted, collision, demo):
        for adj in result.adjudications:
            assert not hasattr(adj, "weight")
            assert not hasattr(adj, "confidence")
            assert not hasattr(adj, "score")
            assert not re.search(r"\d+\s*%", adj.reason), adj.reason
            for banned in ("more reliable", "outranks", "confidence",
                           "stronger authority", "more authoritative"):
                assert banned not in adj.reason.lower(), (banned, adj.reason)


def test_the_consultation_states_that_nothing_is_ranked(exalted):
    text = exalted.consultation
    assert "no mechanism for preferring one authority to another" in text
    assert "carries a weight, a score or a rank" in text


def test_the_vocabularies_are_closed(exalted, collision, demo):
    for result in (exalted, collision, demo):
        for adj in result.adjudications:
            assert adj.relationship in RELATIONSHIPS
            assert adj.resolution in RESOLUTIONS
            assert len(adj.parties) >= 2
            assert adj.reason.strip()


def test_an_unknown_relationship_fails_verification(exalted, cards):
    """The closed vocabulary is enforced, not merely documented."""
    from dataclasses import replace
    adj = exalted.adjudications[0]
    bad = replace(adj, relationship="stronger_book")
    problems = verify_adjudications([bad], exalted.claims, cards)
    assert any("unknown relationship" in p for p in problems)


def test_a_party_that_is_not_a_card_fails_verification(exalted, cards):
    from dataclasses import replace
    adj = exalted.adjudications[0]
    ghost = replace(adj.parties[0], card="PD.99.DoesNotExist")
    bad = replace(adj, parties=(ghost,) + adj.parties[1:])
    problems = verify_adjudications([bad], exalted.claims, cards)
    assert any("is not in the rule store" in p for p in problems)


# --- the synthesis defect this milestone fixes ------------------------------

def test_a_verse_and_its_refutation_are_no_longer_reported_as_agreeing(exalted):
    """The concrete production defect Stage 7 was built to fix.

    Part 3 used to print the shared vocabulary of verse 14 and the note
    denying verse 14 under the heading "Terms that recur without contradiction",
    because the note's "cannot" is not one of the negation cue words. The cue
    list was never the real problem: the contradiction was declared in the
    store all along and nothing read it.
    """
    text = exalted.consultation
    settled = text.split("### Terms that recur without contradiction")[-1]
    ids = "`clm-0023`, `clm-0024`"
    for term in ("ruler", "shine", "vikramaditya"):
        assert f"**“{term}”** — asserted in 2 passages: {ids}" not in settled, term


def test_the_contested_theme_names_the_store_as_its_evidence(exalted):
    """Contested by doctrine, and the report must say which evidence it is.

    A theme flagged only by the store's link shows every occurrence marked
    "asserted"; without the note that reads as agreement, which is the very
    misreport this replaced.
    """
    text = exalted.consultation
    assert "Contested because the rule store links these passages' cards" in text
    contested = {t.term for t in exalted.synthesis.themes
                 if t.doctrinal_conflicts}
    assert {"ruler", "shine", "vikramaditya"} <= contested


def test_doctrinal_contest_is_supplied_not_measured():
    """Synthesis still asserts no astrology of its own.

    Called without Stage 7's pairs it finds no doctrinal conflict at all --
    the disagreement enters as a citation from the store, never as something
    this module inferred from the words.
    """
    result = run(EXALTED)
    plain = synthesise(result.claims)
    assert all(t.doctrinal_conflicts == () for t in plain.themes)
    withpairs = synthesise(result.claims,
                           contested_claim_pairs(result.adjudications))
    assert any(t.doctrinal_conflicts for t in withpairs.themes)


def test_only_genuine_disagreements_are_handed_to_synthesis(demo, collision):
    """A second authority on record is not a disagreement between claims.

    `contested_claim_pairs` must not sweep in `parallel_authority` (nothing is
    in conflict) or an `applied` override (the source settled it), or Part 3
    would start reporting agreement as contest.
    """
    # Milestone 25: the demo chart's Sarala claim now also links to three
    # Parashara cards (contradiction, qualification, parallel_authority), none
    # of which fire on this particular chart -- so every relationship here is
    # `recorded`, not `unresolved`, and none of them is a contest either.
    assert {a.relationship for a in demo.adjudications} == {
        PARALLEL_AUTHORITY, CONTRADICTION, QUALIFICATION,
    }
    assert all(a.resolution == RECORDED for a in demo.adjudications)
    assert contested_claim_pairs(demo.adjudications) == frozenset()
    # The collision is unresolved, but both its parties are reference cards
    # with no claims -- so it contributes no claim pair either, and Part 3 is
    # not told to contest anything on its account.
    collision_only = [a for a in collision.adjudications
                      if a.declared_as == () and a.resolution == UNRESOLVED]
    assert collision_only
    assert contested_claim_pairs(collision_only) == frozenset()


# --- the links themselves ---------------------------------------------------

def test_relationship_links_all_resolve(cards):
    """Now that Stage 7 reads them, a dangling link is a lost relationship.

    Before this milestone these fields were inert and a typo in one cost
    nothing. A consultation now silently fails to report a contradiction it was
    told about, so the build gate treats it like a stale quote.
    """
    known = {c.id for c in cards}
    for card in cards:
        for rel in RELATION_LINKS:
            for target in card.raw.get(rel) or ():
                assert target in known, f"{card.id}: {rel} -> {target}"
                assert target != card.id, f"{card.id}: {rel} names itself"


def test_a_dangling_link_fails_the_build(cards, tmp_path):
    """The gate is real, not decorative."""
    import copy
    broken = copy.copy(cards[0])
    object.__setattr__(broken, "raw", dict(cards[0].raw,
                                           contradicts=["PD.99.Nonexistent"]))
    problems = verify_cards([broken] + list(cards[1:]), CORPUS)
    assert any("PD.99.Nonexistent" in p for p in problems)


def test_links_are_read_undirected(cards):
    """Six links in the store are declared from one end only.

    Which end carries the declaration is an accident of encoding order, so a
    relationship must be found from either card. The exaltation dispute is one
    of the asymmetric ones -- only the Notes card declares it.
    """
    by_id = {c.id: c for c in cards}
    assert by_id["PD.09.Dignity.Exalted.Notes"].raw["contradicts"] == \
        ["PD.09.Dignity.Exalted"]
    assert not by_id["PD.09.Dignity.Exalted"].raw.get("contradicts")
    # And it is nonetheless found, from the side that does not declare it.
    from Engine.adjudicate import _card_links
    assert ("PD.09.Dignity.Exalted", "PD.09.Dignity.Exalted.Notes") \
        in _card_links(cards)


# --- what the corpus does and does not contain ------------------------------

def test_the_claim_to_claim_contradictions_are_catalogued(cards):
    """A finding recorded as a test, so a future encoding pass notices.

    Every `contradicts` link in the store used to have at least one side that
    never becomes a claim, except the single pair below -- which is why
    Milestone 23 built no machinery for weighing rival predictions. Milestone
    25 adds a second real cluster (chapter 6's Harsha/Sarala/Vimala vs.
    Parashara's nine-combination breakdown), still with no such machinery
    built: the source does not settle these either, so both sides simply
    stand, exactly as `Engine/adjudicate.py` already handles. Milestone 33
    adds a third cluster: v.24's unconditional 6th/8th/12th-lord misery dasa
    (PD.20.MiseryDasa.DusthanaLords) against vv.7/9/13's own strength-gated
    good-dasa cards for the same three house lords (PD.20.Strong.House6/.8/.12)
    -- neither verse states which governs a chart where a dusthana lord is
    both strong and its own mahadasa lord.
    """
    by_id = {c.id: c for c in cards}
    pairs = []
    for card in cards:
        for target in card.raw.get("contradicts") or ():
            a, b = sorted((card.id, target))
            if (a, b) in pairs:
                continue
            if by_id[a].activation == "active" and by_id[b].activation == "active":
                pairs.append((a, b))
    assert sorted(pairs) == sorted([
        ("PD.09.Dignity.Exalted", "PD.09.Dignity.Exalted.Notes"),
        ("PD.06.DusthanaLord.Harsha", "PD.06.Parashara.SixthLordInSixth"),
        ("PD.06.DusthanaLord.Harsha", "PD.06.Parashara.EighthLordInSixth"),
        ("PD.06.DusthanaLord.Harsha", "PD.06.Parashara.TwelfthLordInSixth"),
        ("PD.06.DusthanaLord.Sarala", "PD.06.Parashara.SixthLordInEighth"),
        ("PD.06.DusthanaLord.Sarala", "PD.06.Parashara.EighthLordInEighth.Weak"),
        ("PD.06.DusthanaLord.Vimala", "PD.06.Parashara.SixthLordInTwelfth"),
        ("PD.06.DusthanaLord.Vimala", "PD.06.Parashara.EighthLordInTwelfth"),
        ("PD.06.DusthanaLord.Vimala", "PD.06.Parashara.TwelfthLordInTwelfth"),
        ("PD.20.MiseryDasa.DusthanaLords", "PD.20.Strong.House6"),
        ("PD.20.MiseryDasa.DusthanaLords", "PD.20.Strong.House8"),
        ("PD.20.MiseryDasa.DusthanaLords", "PD.20.Strong.House12"),
    ])


def test_the_sakata_cancellation_needs_no_stage_seven_mechanism(cards):
    """Checked because the obvious cancellation case is already solved.

    The verse states the yoga and its cancellation in one sentence, so the
    cancelling clause is a negated conjunct inside the card's own condition and
    the card simply does not fire when the Moon is in a kendra. There is no
    second claim to cancel and nothing for an adjudicator to do. A cross-card
    cancellation mechanism built for this would have been architecture for a
    problem the encoding had already handled.
    """
    sakata = {c.id: c for c in cards}["PD.06.Sakata"]
    assert not sakata.raw.get("contradicts")
    conjuncts = sakata.conditions["all"]
    assert any("not" in c and c["not"] == {"in_house_class":
               {"graha": "Moon", "klass": "kendra"}} for c in conjuncts)


def test_a_source_stated_override_is_applied_and_attributed(overridden, cards):
    """`applied` exists, and only the source's own sentence may produce it.

    Verse 4 prints what its weakness overrides -- exaltation, own sign, a
    friend's sign -- so where a combust graha is also exalted the engine drops
    the strong verdict, emits the weak one, and names the sentence that told it
    to. This is the *only* precedence the corpus states and therefore the only
    one applied anywhere in the engine.
    """
    applied = [a for a in overridden.adjudications if a.resolution == APPLIED]
    assert applied, "the chart chosen for this test no longer exercises it"
    by_id = {c.id: c for c in cards}
    for adj in applied:
        assert adj.relationship == OVERRIDE
        assert "The source states this precedence itself" in adj.reason
        # Reachable only through a card that names what it overrides -- the
        # override list is the source's, never the engine's.
        assert any(by_id[p.card].predicts.get("overrides") for p in adj.parties)
    # And the verdict that survived is the one the override leaves standing.
    fact = [f for f in overridden.facts.by_predicate("strength")
            if f.args["graha"] == "Mercury"]
    assert [f.args["strength"] for f in fact] == ["weak"]
    assert fact[0].evidence["overridden"][0]["basis"] == "exalted"


def test_an_applied_override_is_not_handed_to_synthesis_as_a_contest(overridden):
    """A relationship the source settled is not a disagreement to report.

    If `applied` leaked into the contested pairs, Part 3 would start flagging
    resolved doctrine as a tension between passages.
    """
    applied = [a for a in overridden.adjudications if a.resolution == APPLIED]
    assert applied
    pairs = contested_claim_pairs(overridden.adjudications)
    for adj in applied:
        ids = adj.claim_ids
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                assert frozenset((a, b)) not in pairs
