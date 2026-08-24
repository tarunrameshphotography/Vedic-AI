"""Tests for the chapter 4 (strength) encoding.

Chapter 4 is the first chapter this project has encoded that prints two
strength doctrines by two different authorities and says so itself: eight pages
of the translator's survey of "the views of other ancients", carrying all the
familiar Shastyamsa arithmetic, and then Mantreswara's own 24 verses, which
name a *different* six balas and are almost entirely unquantified.

Nearly everything asserted here is a guard against the same class of mistake --
a later session reading the survey's numbers as Phaladeepika's own doctrine,
or reading the chapter's qualitative "strong" as its numeric one. The tests
that matter most are the ones asserting what the encoding refuses to do: it
does not merge the two authorities, it does not repair the arithmetic defect it
found, and it does not turn a component of strength into a verdict about it.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from Engine.rules import load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"


@pytest.fixture(scope="module")
def ch4():
    return [c for c in load_cards(RULES)
            if c.book_id == "phaladeepika" and c.chapter == 4]


@pytest.fixture(scope="module")
def by_id(ch4):
    return {c.id: c for c in ch4}


@pytest.fixture(scope="module")
def registry():
    return json.loads((RULES / "deferred.json").read_text(encoding="utf-8"))


# --- the two authorities ----------------------------------------------------

def test_every_chapter_four_card_names_the_authority_it_speaks_for(ch4):
    """The whole chapter turns on this and nothing else enforces it.

    The chapter's numbers belong to authorities it names only in passing. A
    card that does not say whose doctrine it carries is one a later reader will
    attribute to Mantreswara by default, which is exactly the error the
    encoding exists to prevent.
    """
    assert ch4, "chapter 4 is not in the store"
    for c in ch4:
        assert c.predicts.get("authority"), (
            f"{c.id} does not say which authority states it")


def test_the_survey_and_the_verses_are_kept_on_different_tiers(ch4):
    """Tier is the second, independent record of the same boundary.

    Every card drawn from the translator's survey or his Notes is tier 2;
    every card drawn from a numbered verse is tier 1. If the two ever agree
    less than perfectly, one of them has been mis-assigned.
    """
    for c in ch4:
        survey = c.predicts["authority"] != "Mantreswara"
        assert (c.tier == 2) == survey, (
            f"{c.id}: tier {c.tier} but authority "
            f"{c.predicts['authority'][:40]!r}")


def test_the_two_schemes_are_not_the_same_six_balas(by_id):
    """The finding that makes the whole separation necessary.

    A generic Shadbala implementation would take the survey's twelve-part Sthan
    Bala and its six-fold scheme as Phaladeepika's. They are not: Mantreswara
    promotes Uchcha Bala to a member in its own right and drops Drik and
    Naisargik from the six entirely.
    """
    survey = set(by_id["PD.04.Ancients.SixBalas"].predicts["kinds"])
    verses = set(by_id["PD.04.SixBalas.Order"].predicts["kinds"])
    assert "Uchcha" in verses and not any(k.startswith("Uchcha") for k in survey)
    assert any(k.startswith("Drik") for k in survey)
    assert not any(k.startswith("Drik") for k in verses)
    assert any(k.startswith("Naisargik") for k in survey)
    assert not any(k.startswith("Naisargik") for k in verses)


# --- the strength verdicts --------------------------------------------------

def test_strength_verdicts_come_only_from_the_verses_that_say_strong_or_weak(ch4):
    """Verses 4 and 5 state verdicts; nothing else in the chapter does.

    Every other strength statement in chapter 4 gives a *quantity* of one
    component -- so many Shastyamsa of Sthana Bala, a proportion of Dik Bala.
    Turning any of those into a strong/weak verdict would be inventing a scale
    the chapter never supplies. This test pins which cards are allowed to carry
    a verdict at all.
    """
    verdicts = {c.id: c.predicts.get("verdict") for c in ch4
                if c.predicts.get("relation") == "graha_strength"}
    assert verdicts == {
        "PD.04.DikBala.Houses": None,          # a component, not a verdict
        "PD.04.Strength.RetrogradeInDebilitation": "strong",
        "PD.04.Weakness.Combust": "weak",
        "PD.04.Strength.Exalted": "strong",
        "PD.04.Strength.RetrogradeFive": "strong",
        "PD.04.RahuKetu.StrongSigns": "strong",
    }
    verses = {c.verse for c in ch4
              if c.predicts.get("relation") == "graha_strength"
              and c.predicts.get("verdict")}
    assert verses == {"4", "5"}, (
        f"a strength verdict is being drawn from verse(s) {sorted(verses)}; "
        f"only verses 4 and 5 state one")


def test_having_dik_bala_is_not_being_strong(by_id):
    """The one graha_strength card that must never produce a verdict.

    Full Dik Bala is one of six components. A graha in the 10th house has it
    and may still be weak on every other count, so an extractor that read this
    table as 'strong' would call the Sun strong on roughly a twelfth of all
    charts for no defensible reason.
    """
    card = by_id["PD.04.DikBala.Houses"]
    assert card.predicts["verdict"] is None
    assert card.predicts["bala"] == "dik"


def test_the_numeric_criterion_for_strong_is_recorded_and_not_implemented(by_id):
    """Chapter 4's own definition of strong is the one we cannot compute.

    Verses 22-23 define strength as a Shadbala Pinda reaching a threshold. That
    is the chapter's formal criterion, and it is not what the engine's verdicts
    mean -- the components that would sum to a Pinda are quantified only in the
    other authorities' scheme, and three of those have their arithmetic
    explicitly withheld by the source. The card records the thresholds and
    asserts no verdict.
    """
    card = by_id["PD.04.BalaPinda.Thresholds"]
    assert card.activation == "reference"
    assert card.predicts["relation"] == "strength_threshold"
    assert "verdict" not in card.predicts
    assert card.predicts["table"]["Jupiter"] == 8.5
    assert "dep.strength" in card.raw["requires"]


def test_the_combustion_weakness_carries_the_override_the_verse_states(by_id):
    """The override is the source's, not the engine's.

    Verse 4 says a combust graha is weak 'even though he may be posited in his
    sign of exaltation, in his own or a friend's sign'. An extractor that
    applies that is following the book; one that decided it on its own would be
    adjudicating between cards, which this project does not do.
    """
    card = by_id["PD.04.Weakness.Combust"]
    assert card.predicts["verdict"] == "weak"
    assert card.predicts["overrides"] == ["exalted", "own", "friend"]


def test_the_retrograde_verdict_names_the_five_and_not_the_nodes(by_id):
    """'The other five non-luminous planets', spelled out.

    The nodes are retrograde on every chart the engine computes. Writing this
    verse as 'whatever is retrograde' would make Rahu and Ketu strong in every
    nativity ever cast, which the verse plainly does not say.
    """
    grahas = by_id["PD.04.Strength.RetrogradeFive"].predicts["grahas"]
    assert grahas == ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    assert "Rahu" not in grahas and "Ketu" not in grahas
    assert "Sun" not in grahas and "Moon" not in grahas


# --- defects preserved rather than repaired ---------------------------------

def test_the_mars_bala_pinda_row_is_preserved_as_printed(by_id):
    """A row that does not add up, kept as it is.

    Six of the seven rows sum exactly at 60 Shastyamsa to the Rupa. Mars's does
    not, and Saturn's otherwise-identical row does -- so one digit would repair
    it. The printed page was rendered and inspected; 1-16 is what is there.
    Preserving it is the same treatment the chapter 23 Ashtakavarga chart gets
    for totalling 44 bindus instead of 48.
    """
    table = by_id["PD.04.BalaPinda.OtherAuthorities"].predicts["table"]
    assert table["Mars"]["sthan"] == "1-16"
    assert table["Mars"]["total"] == "4-13"
    assert table["Saturn"]["sthan"] == "1-36"

    def rupas(cell):
        r, s = cell.split("-")
        return int(r) * 60 + int(s)

    parts = ("sthan", "dik", "chesta", "kala", "ayana")
    for graha, row in table.items():
        total = sum(rupas(row[p]) for p in parts)
        if graha == "Mars":
            assert total != rupas(row["total"]), (
                "the Mars row now sums -- if the corpus was corrected, "
                "concept:mars-bala-pinda-row must be revisited, not this test")
        else:
            assert total == rupas(row["total"]), f"{graha} row no longer sums"


def test_the_oja_yugma_list_records_the_four_grahas_that_are_printed(by_id):
    """'Amongst those five', naming four.

    The fifth is not supplied. Any candidate would come from outside this
    project's corpus, which is exactly the import the store forbids.
    """
    grahas = by_id["PD.04.Ancients.Sthana.OjaYugmaRasi"].predicts["grahas"]
    assert len(grahas) == 4
    assert grahas == ["Sun", "Mars", "Mercury", "Saturn"]


def test_the_enemy_sign_row_is_left_unquantified(by_id):
    """'Very little' is not a number and is not turned into one.

    The verse's other rows halve neatly -- 1, 3/4, 1/2, 1/4 -- so continuing
    the series to 1/8 would read entirely plausibly and would be invented.
    """
    p = by_id["PD.04.SthanaBala.ByDignity"].predicts
    assert "enemy" not in p["table"]
    assert p["unquantified"]["enemy"] == "very little"
    assert p["table"]["debilitated"] == 0.0 and p["table"]["combust"] == 0.0


def test_the_triped_sign_card_is_inert_for_the_ambiguity_not_a_capability(by_id):
    """The verse names a sign class this book never defines.

    'Triped' is confirmed as the printed word against the rendered page, and
    chapter 1's body-form table has no such class. Reading it as 'biped' would
    make the verse parallel to the survey's Bhava Dik Bala, which is precisely
    why a card must not make that substitution on its own.
    """
    card = by_id["PD.04.Lagna.TripedSign"]
    assert card.activation == "inert"
    assert card.raw["requires"] == ["dep.triped-sign-class"]
    assert "triped" in card.predicts["table"]


# --- disagreement preserved --------------------------------------------------

def test_the_two_kendra_rules_contradict_each_other_and_both_survive(by_id):
    """Verse 3 against verse 8, five verses apart in one chapter.

    A graha in the 4th house is worth one Rupa by verse 3 and a quarter by
    verse 8. The engine has no way to prefer one, and correctly does not try.
    """
    v3 = by_id["PD.04.SthanaBala.Kendradi"].predicts["table"]
    v8 = by_id["PD.04.SthanaBala.AmongKendras"].predicts["table"]
    assert v3["kendra"] == 1.0
    assert v8["4"] == 0.25
    assert "PD.04.SthanaBala.Kendradi" in \
        by_id["PD.04.SthanaBala.AmongKendras"].raw["contradicts"]


def test_the_retrograde_rescue_is_linked_to_the_chapter_nine_override(by_id):
    """Chapter 4 narrows what chapter 9 states unconditionally.

    Chapter 9 v. 20 makes retrogression alone equivalent to exaltation; this
    verse conditions the same rescue on the rays being unaffected as well. For
    a retrograde graha that is also combust the two disagree, and the pair is
    registered for a human rather than resolved here.
    """
    card = by_id["PD.04.Strength.RetrogradeInDebilitation"]
    assert card.raw["extends"] == ["PD.09.Retrograde.AsExalted"]
    assert card.predicts["when"]["not_combust"] is True


def test_the_naisargik_orderings_of_both_authorities_agree(by_id):
    """The chapter's cleanest cross-authority corroboration.

    Recorded as two authorities agreeing, never merged into one claim made
    twice as strongly -- the same discipline Milestone 20 established for
    cross-book agreement on graha nature.
    """
    numbers = by_id["PD.04.Ancients.NaisargikBala"].predicts["table"]
    order = by_id["PD.04.NaisargikBala.Order"].predicts["weakest_to_strongest"]
    assert sorted(numbers, key=numbers.get) == order


# --- scoping ----------------------------------------------------------------

def test_the_kala_bala_lists_are_scoped_and_are_not_nature_doctrine(ch4, by_id):
    """The statement Milestone 20 examined and rejected, now encoded properly.

    Chapter 4 names Jupiter and Venus benefic -- inside its Kala Bala rules,
    whose next sentences scope Mercury's treatment to that computation
    explicitly. Encoded under its own relation, it records the definition
    without promoting it to general doctrine.
    """
    for c in ch4:
        assert c.predicts.get("relation") != "graha_nature", (
            f"{c.id} encodes chapter 4 as general nature doctrine")
    benefics = by_id["PD.04.Ancients.KalaBala.BeneficList"].predicts
    assert benefics["relation"] == "kala_bala_benefic"
    assert benefics["scope"] == "the Kala Bala computation only"
    assert benefics["grahas"] == ["Moon", "Mercury", "Jupiter", "Venus"]
    malefics = by_id["PD.04.Ancients.KalaBala.MaleficList"].predicts
    assert malefics["relation"] == "kala_bala_malefic"


def test_the_ketu_clauses_the_engine_cannot_reach_are_not_asserted(by_id):
    """Quoted in full, asserted in part, and the difference is recorded.

    Verse 5 gives Ketu three whole signs, a half sign, and a condition on two
    upagrahas. Only the whole signs are asserted.
    """
    card = by_id["PD.04.RahuKetu.StrongSigns"]
    assert card.predicts["table"]["Ketu"] == ["Pisces", "Virgo", "Taurus"]
    assert "latter half of Sagittarius" in card.quote_display
    assert "Indrachapa" in card.quote_display


# --- the registry ------------------------------------------------------------

def test_the_chapter_is_marked_resolved_and_its_findings_registered(registry):
    """Encoding a chapter is only half the job; claiming what was left is the
    other half, and these are the questions this chapter produced."""
    entries = {e["id"]: e for e in registry["entries"]}
    assert entries["chapter:phaladeepika.04"]["status"] == "resolved"
    for cid in ("concept:strength-criterion-scope",
                "concept:mars-bala-pinda-row",
                "concept:oja-yugma-fifth-graha",
                "concept:retrograde-rescue-scope",
                "concept:kendra-positional-strength-conflict",
                "concept:special-aspect-parity",
                "concept:chandra-divisor-mismatch",
                "concept:ketu-strength-clauses"):
        assert entries[cid]["status"] == "deferred", f"{cid} missing or resolved"


def test_the_kala_bala_scope_question_stays_open(registry):
    """The card records the definition; the computation that would use it does
    not exist, so the deferral is not discharged by encoding it."""
    entries = {e["id"]: e for e in registry["entries"]}
    entry = entries["concept:kala-bala-benefic-scope"]
    assert entry["status"] == "deferred"
    assert "PD.04.Ancients.KalaBala.BeneficList" in entry["reason"]


def test_strength_is_still_an_outstanding_dependency(registry):
    """This milestone encoded the source of dep.strength; it did not build it.

    The extractor that reads these cards is the next milestone. Until it
    exists, no chart produces a strength fact and every card blocked on
    dep.strength stays blocked -- which is what this asserts, so that a
    half-built state cannot be mistaken for a finished one.
    """
    deps = registry["dependencies"]
    assert deps["dep.strength"].get("implemented", False) is False
    assert "chapter:phaladeepika.04" in deps["dep.strength"]["depends_on"]
