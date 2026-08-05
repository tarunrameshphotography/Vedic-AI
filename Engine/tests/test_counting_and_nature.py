"""Tests for counting, reference frames, benefic/malefic nature, and the
correlated negation that the "unless" clauses need.

Five capabilities land here, each demanded by a card that was blocked without
it. The tests are grouped by capability, and the ones that matter most are the
ones asserting what the engine refuses to do: it will not classify a graha the
books do not classify, it will not count an empty house, and it will not read
"unless he be lord of the 8th" as a question about the chart at large.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine, DoctrineError
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import FactSet, extract_facts, make_fact
from Engine.rules import evaluate, load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

FRAME = {"reference": "lagna", "varga": "D1", "house_system": "whole_sign"}

DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)


def facts(*specs) -> FactSet:
    return FactSet([make_fact(p, a, FRAME) for p, a in specs])


@pytest.fixture(scope="module")
def provider():
    return SwissEphemerisDLL()


@pytest.fixture(scope="module")
def chart(provider):
    return compute_chart(resolve_birth(DEMO, provider), provider)


@pytest.fixture(scope="module")
def doctrine():
    return Doctrine.from_cards(load_cards(RULES))


@pytest.fixture(scope="module")
def fs(chart, doctrine):
    return extract_facts(chart, doctrine)


# --- counting ----------------------------------------------------------------

def test_occupant_count_matches_the_placements(fs, chart):
    """The count is not a separate belief; it is the placements, tallied."""
    expected: dict[int, int] = {}
    for b in chart.bodies.values():
        expected[b.house] = expected.get(b.house, 0) + 1
    got = {f.args["house"]: f.args["n"] for f in fs.by_predicate("occupant_count")}
    assert got == expected
    assert sum(got.values()) == len(chart.bodies)


def test_no_count_is_emitted_for_an_empty_house(fs, chart):
    """A zero would let a counting verse speak about a house it never addressed.

    "As many women as the number of planets posited in the 7th" says nothing
    about a chart with an empty 7th, and binding the count to zero would turn
    that silence into a claim of none.
    """
    occupied = {b.house for b in chart.bodies.values()}
    for f in fs.by_predicate("occupant_count"):
        assert f.args["n"] >= 1
        assert f.args["house"] in occupied


def test_a_count_is_read_by_binding_it_not_by_comparing_it():
    """The whole of the arithmetic: a card learns the number, it cannot compute."""
    fs = facts(("occupant_count", {"house": 7, "n": 3}))
    ev = evaluate({"occupant_count": {"house": 7, "n": "?n"}}, fs)
    assert ev.satisfied
    assert ev.solutions[0].as_dict() == {"?n": "3"}
    # And a literal count still matches exactly, as "occupied by two planets"
    # requires.
    assert evaluate({"occupant_count": {"house": 7, "n": 3}}, fs).satisfied
    assert not evaluate({"occupant_count": {"house": 7, "n": 2}}, fs).satisfied


def test_conjunct_count_counts_companions_not_the_graha_itself(fs, chart):
    for f in fs.by_predicate("conjunct_count"):
        graha = f.args["graha"]
        same = [b.body for b in chart.bodies.values()
                if b.sign_index == chart.bodies[graha].sign_index
                and b.body != graha]
        assert f.args["n"] == len(same) >= 1
        assert graha not in f.evidence["companions"]


# --- reference frames --------------------------------------------------------

def test_graha_frame_counts_inclusively_from_the_reference(fs, chart):
    """The reference graha's own sign is the 1st from itself, so the 7th is six on."""
    for f in fs.by_predicate("in_house_from"):
        a = chart.bodies[f.args["graha"]]
        ref = chart.bodies[f.args["reference"]]
        assert f.args["house"] == ((a.sign_index - ref.sign_index) % 12) + 1


def test_graha_frame_emits_no_self_reference(fs):
    """`in_house_from(Mars, Mars, 1)` is true of every chart ever cast."""
    for f in fs.by_predicate("in_house_from"):
        assert f.args["graha"] != f.args["reference"]


def test_the_lagna_frame_and_a_graha_frame_are_different_frames(fs, chart):
    """The point of the capability: a rule in one frame is wrong in the other.

    PD.10.MarsSaturn.SeventhFromVenusMoon fired on the lagna frame before this
    landed, which is a different claim about a different pair of houses.
    """
    disagreements = 0
    for f in fs.by_predicate("in_house_from"):
        lagna_house = chart.bodies[f.args["graha"]].house
        if f.args["house"] != lagna_house:
            disagreements += 1
    assert disagreements > 0


# --- nature ------------------------------------------------------------------

def test_nature_comes_only_from_cards(fs):
    for f in fs.by_predicate("nature"):
        assert f.evidence["doctrine"], f.key
        assert f.args["nature"] in ("benefic", "malefic")


def test_the_moon_is_classified_by_its_phase(fs, chart):
    """Doctrine, not a table: "The waning Moon ... malefic", "The waxing Moon ... benefic"."""
    moon = [f for f in fs.by_predicate("nature") if f.args["graha"] == "Moon"]
    assert len(moon) == 1
    elong = (chart.bodies["Moon"].lon - chart.bodies["Sun"].lon) % 360.0
    expected = "benefic" if elong < 180.0 else "malefic"
    assert moon[0].args["nature"] == expected
    assert moon[0].evidence["elongation"] == pytest.approx(elong, abs=1e-6)
    # The body the phase is measured from is doctrine and must be cited, not
    # assumed by the extractor.
    assert moon[0].evidence["measured_from"]


def test_mercury_is_classified_by_its_company(fs, chart):
    """"Mercury if associated with them becomes malefic." Its nature is relational."""
    merc = [f for f in fs.by_predicate("nature") if f.args["graha"] == "Mercury"]
    assert len(merc) == 1
    same_sign = {b.body for b in chart.bodies.values()
                 if b.sign_index == chart.bodies["Mercury"].sign_index
                 and b.body != "Mercury"}
    malefics = {f.args["graha"] for f in fs.by_predicate("nature")
                if f.args["nature"] == "malefic"}
    keeps_bad_company = bool(same_sign & malefics)
    assert merc[0].args["nature"] == ("malefic" if keeps_bad_company
                                      else "benefic")
    assert set(merc[0].evidence["companions"]) == same_sign


def test_jupiter_and_venus_are_left_unclassified_and_the_silence_is_reported(fs):
    """The most important assertion in this file.

    Chapter 2 names the malefics and adds the waxing Moon and Mercury as
    benefic. It never mentions Jupiter or Venus -- Phaladeepika states their
    nature in chapter 4, which is not encoded. "Not listed as malefic, therefore
    benefic" is an inference, and the engine does not get to make it.
    """
    classified = {f.args["graha"] for f in fs.by_predicate("nature")}
    assert "Jupiter" not in classified
    assert "Venus" not in classified
    reported = fs.doctrine.partial.get("nature", "")
    assert "Jupiter" in reported and "Venus" in reported


def test_a_benefic_clause_cannot_be_satisfied_by_an_unclassified_graha(fs):
    """The consequence of that silence: under-firing, never over-firing."""
    ev = evaluate({"all": [{"in_house": {"graha": "Jupiter", "house": 3}},
                           {"nature": {"graha": "Jupiter", "nature": "benefic"}}]},
                  fs)
    assert not ev.satisfied


def test_contradictory_nature_doctrine_raises_rather_than_picking(chart):
    """Two cards making one graha both benefic and malefic is not resolvable here.

    Adjudication is Stage 7 and does not exist, so the extractor refuses rather
    than silently preferring whichever card it read first.
    """
    class Contradictory:
        def graha_natures(self):
            rows = [{"nature": "malefic", "grahas": ["Mars"], "conditional": [],
                     "card": "X"},
                    {"nature": "benefic", "grahas": ["Mars"], "conditional": [],
                     "card": "Y"}]
            return rows, ("X", "Y")

    from Engine.facts import _resolve_nature, DoctrineReport
    with pytest.raises(DoctrineError):
        _resolve_nature(chart, Contradictory(), DoctrineReport())


def test_a_phase_condition_without_a_reference_body_raises(chart):
    """The extractor will not guess what a phase is measured against."""
    class NoReference:
        def graha_natures(self):
            rows = [{"nature": "malefic", "grahas": [],
                     "conditional": [{"graha": "Moon", "when": {"phase": "waning"}}],
                     "card": "X"}]
            return rows, ("X",)

    from Engine.facts import _resolve_nature, DoctrineReport
    with pytest.raises(DoctrineError):
        _resolve_nature(chart, NoReference(), DoctrineReport())


def test_an_unreadable_nature_condition_raises(chart):
    class Unknown:
        def graha_natures(self):
            rows = [{"nature": "malefic", "grahas": [],
                     "conditional": [{"graha": "Mars",
                                      "when": {"during_an_eclipse": True}}],
                     "card": "X"}]
            return rows, ("X",)

    from Engine.facts import _resolve_nature, DoctrineReport
    with pytest.raises(DoctrineError):
        _resolve_nature(chart, Unknown(), DoctrineReport())


# --- nature and occupancy together -------------------------------------------

def test_nature_occupancy_agrees_with_nature_and_placement(fs, chart):
    nature = {f.args["graha"]: f.args["nature"]
              for f in fs.by_predicate("nature")}
    expected: dict[tuple[int, str], int] = {}
    for b in chart.bodies.values():
        if b.body in nature:
            key = (b.house, nature[b.body])
            expected[key] = expected.get(key, 0) + 1
    got = {(f.args["house"], f.args["nature"]): f.args["n"]
           for f in fs.by_predicate("nature_count")}
    assert got == expected
    # Every count has a matching membership fact and vice versa.
    assert {(f.args["house"], f.args["nature"])
            for f in fs.by_predicate("nature_occupancy")} == set(expected)


def test_an_unclassified_graha_is_counted_by_neither_nature(fs, chart):
    """A house holding only Jupiter has no nature_occupancy fact at all."""
    nature = {f.args["graha"] for f in fs.by_predicate("nature")}
    for f in fs.by_predicate("nature_occupancy"):
        for graha in f.evidence["grahas"]:
            assert graha in nature


# --- correlated negation -----------------------------------------------------

def test_negation_sees_the_current_binding():
    """"Benefics in the 7th ... unless they happen to be lords of the 6th, 8th
    or 12th." The exclusion is about the graha that satisfied the first clause.
    """
    fs = facts(
        ("in_house", {"graha": "Jupiter", "house": 7}),
        ("in_house", {"graha": "Venus", "house": 7}),
        ("lord_of_house", {"graha": "Venus", "house": 8}),
    )
    cond = {"all": [
        {"in_house": {"graha": "?g", "house": 7}},
        {"not": {"any": [{"lord_of_house": {"graha": "?g", "house": 6}},
                         {"lord_of_house": {"graha": "?g", "house": 8}},
                         {"lord_of_house": {"graha": "?g", "house": 12}}]}},
    ]}
    ev = evaluate(cond, fs)
    assert ev.satisfied
    assert [s.as_dict() for s in ev.solutions] == [{"?g": "Jupiter"}]


def test_uncorrelated_negation_still_asks_whether_anything_satisfies_it():
    """A variable that is *not* bound outside stays local.

    This is what lets "if there is no planet in the Ascendant" mean what it
    says, and it must keep working now that binding is threaded through.
    """
    fs = facts(("in_house", {"graha": "Mars", "house": 5}))
    assert evaluate({"not": {"in_house": {"graha": "?g", "house": 1}}}, fs).satisfied
    assert not evaluate({"not": {"in_house": {"graha": "?g", "house": 5}}},
                        fs).satisfied


def test_binding_order_does_not_change_the_answer():
    """A conjunction binds left to right; the solution set must not depend on it."""
    fs = facts(
        ("in_house", {"graha": "Mars", "house": 7}),
        ("nature", {"graha": "Mars", "nature": "malefic"}),
        ("in_house", {"graha": "Moon", "house": 7}),
        ("nature", {"graha": "Moon", "nature": "benefic"}),
    )
    a = evaluate({"all": [{"in_house": {"graha": "?g", "house": 7}},
                          {"nature": {"graha": "?g", "nature": "malefic"}}]}, fs)
    b = evaluate({"all": [{"nature": {"graha": "?g", "nature": "malefic"}},
                          {"in_house": {"graha": "?g", "house": 7}}]}, fs)
    assert [s.as_dict() for s in a.solutions] == [s.as_dict() for s in b.solutions]


def test_an_unknown_predicate_in_a_later_branch_is_still_reported():
    """An early failure must not hide a typo further along the conjunction."""
    fs = facts(("in_house", {"graha": "Mars", "house": 5}))
    ev = evaluate({"all": [{"in_house": {"graha": "Mars", "house": 7}},
                           {"no_such_predicate": {"graha": "Mars"}}]}, fs)
    assert not ev.satisfied
    assert "no_such_predicate" in ev.missing


# --- the cards these capabilities were built for -----------------------------

def test_every_card_whose_dependencies_are_met_is_no_longer_inert():
    """The discipline that keeps the backlog honest.

    A card whose declared dependencies are all implemented but which is still
    inert claims to be executable while being unable to fire. Either the card
    is released or it declares what is really missing.
    """
    import json
    import sys
    sys.path.insert(0, str(ROOT / "Rules" / "tools"))
    from backlog import dependency_state

    registry = json.loads((RULES / "deferred.json").read_text(encoding="utf-8"))
    state = dependency_state(registry)
    stuck = [c.id for c in load_cards(RULES)
             if c.activation == "inert"
             and c.raw.get("requires")
             and all(state.get(d, False) for d in c.raw["requires"])]
    assert not stuck, stuck


def test_released_cards_use_no_placeholder_sentinels():
    """The old approximation marker must not survive in a firing card."""
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    yield from walk(v)
                else:
                    yield k, v
        elif isinstance(node, list):
            for x in node:
                yield from walk(x)

    for card in load_cards(RULES):
        if card.activation != "active":
            continue
        for key, value in walk(card.conditions):
            assert value not in ("any", "malefic_placeholder"), (card.id, key)
