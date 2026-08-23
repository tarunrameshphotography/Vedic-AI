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

import json
from pathlib import Path

import pytest

from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine, DoctrineError
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import FactSet, extract_facts, make_fact
from Engine.rules import build_predicate_index, evaluate, load_cards

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
def cards():
    return load_cards(RULES)


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


def test_jupiter_and_venus_are_classified_from_an_encoded_source(fs):
    """The most important assertion in this file, inverted in Milestone 20.

    It used to assert that Jupiter and Venus were *unclassified*, because the
    only encoded classification (chapter 2 of the first book) names the malefics
    and adds the waxing Moon and Mercury as benefic, and never mentions either of
    them. That silence was correct behaviour for the store as it then stood --
    "not listed as malefic, therefore benefic" is an inference the engine does
    not get to make -- but it was a production defect all the same: every rule
    about benefics under-fired, on every chart.

    It is now fixed the only way this project permits: not by teaching the engine
    that Jupiter and Venus are benefic, but by encoding a second book's verse that
    says so outright, and letting the same extractor read it. If this test ever
    fails because the classification is missing again, the fix is a card, never a
    Python constant.
    """
    natures = {f.args["graha"]: f for f in fs.by_predicate("nature")}
    assert natures["Jupiter"].args["nature"] == "benefic"
    assert natures["Venus"].args["nature"] == "benefic"
    # And the claim is attributed to the book that actually makes it.
    for graha in ("Jupiter", "Venus"):
        cards = natures[graha].evidence["doctrine"]
        assert cards, f"{graha} nature carries no doctrine citation"
        assert all(c.startswith("BJ.") for c in cards), cards
    # Nothing is reported as unclassified any more.
    assert "nature" not in fs.doctrine.partial


def test_nature_agreed_by_both_books_is_recorded_as_corroborated(fs):
    """The first cross-book corroboration the store has ever been able to make.

    Sun, Mars and Saturn are named malefic by both encoded books. The second
    authority must be recorded alongside the first rather than overwriting it --
    agreement between independent authorities is evidence, and discarding it as a
    duplicate would throw away the only signal the store has that a claim is not
    one translator's idiosyncrasy.
    """
    natures = {f.args["graha"]: f for f in fs.by_predicate("nature")}
    for graha in ("Sun", "Mars", "Saturn"):
        ev = natures[graha].evidence
        assert ev["corroborated"] is True, graha
        assert len(ev["books"]) == 2, (graha, ev["books"])
        assert len({a["card"] for a in ev["authorities"]}) == 2, graha


def test_a_graha_only_one_book_classifies_is_not_reported_as_corroborated(fs):
    """Corroboration must mean something, so it must be able to be false.

    Jupiter and Venus are classified by one book only; Rahu and Ketu by the
    other only. Marking either pair corroborated would make the flag decorative.
    """
    natures = {f.args["graha"]: f for f in fs.by_predicate("nature")}
    for graha in ("Jupiter", "Venus", "Rahu", "Ketu"):
        ev = natures[graha].evidence
        assert ev["corroborated"] is False, graha
        assert len(ev["books"]) == 1, (graha, ev["books"])


def test_a_benefic_clause_is_now_satisfiable_by_jupiter(fs):
    """The consequence of the fix, and the whole point of it.

    This is the assertion that would have caught the defect: a rule about a
    benefic in a house, with Jupiter in that house, must fire.
    """
    house = next(f.args["house"] for f in fs.by_predicate("in_house")
                 if f.args["graha"] == "Jupiter")
    ev = evaluate({"all": [{"in_house": {"graha": "Jupiter", "house": house}},
                           {"nature": {"graha": "Jupiter", "nature": "benefic"}}]},
                  fs)
    assert ev.satisfied


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


# --- always-candidate index (a purely negated card has no positive leaf) ----

def test_a_wholly_negated_card_is_still_offered_every_chart(cards):
    """PD.06.Kemadruma's condition is one `not` and nothing else: `_leaf_keys`
    skips every negated leaf by design, so it contributes no lookup key.
    Without ALWAYS_CANDIDATE such a card is never a candidate in `activate`
    no matter what the chart is, silently breaking this module's own
    contract ("every card whose conditions evaluate true is returned").
    PD.06.Subhamala and PD.06.Asubhamala (slice 3) have the same shape and
    were affected before this test existed."""
    from Engine.rules import ALWAYS_CANDIDATE
    index = build_predicate_index(cards)
    always = set(index.get(ALWAYS_CANDIDATE, ()))
    assert {"PD.06.Kemadruma", "PD.06.Subhamala", "PD.06.Asubhamala"} <= always


def test_kemadruma_runs_end_to_end_through_activate_without_crashing(chart, doctrine, cards):
    """Smoke test for the always-candidate path all the way through
    `activate`, not just the index. The golden chart's Ketu sits 2nd from
    the Moon, so the correct outcome is that the card is considered and
    correctly does not fire -- distinct from never being considered."""
    from Engine.activate import activate
    fs = extract_facts(chart, doctrine)
    claims, _ = activate(chart, fs, cards)
    assert not any(c.derived["rule_card"] == "PD.06.Kemadruma" for c in claims)


# --- Kemadruma (chapter 6 slice 4) -------------------------------------------

def test_kemadruma_fires_when_no_graha_flanks_the_moon(cards):
    """PD.06.Kemadruma: the yoga's own condition, tested directly against a
    hand-built chart rather than the golden one, so the positive case is
    exercised and not just the golden chart's negative one."""
    card = next(c for c in cards if c.id == "PD.06.Kemadruma")
    fs = facts(
        ("in_house_from", {"graha": "Mars", "reference": "Moon", "house": 5}),
        ("in_house_from", {"graha": "Sun", "reference": "Moon", "house": 8}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_kemadruma_does_not_fire_when_a_graha_occupies_the_2nd_from_moon(cards):
    card = next(c for c in cards if c.id == "PD.06.Kemadruma")
    fs = facts(("in_house_from", {"graha": "Ketu", "reference": "Moon", "house": 2}))
    assert not evaluate(card.conditions, fs).satisfied


def test_kemadruma_does_not_fire_when_a_graha_occupies_the_12th_from_moon(cards):
    card = next(c for c in cards if c.id == "PD.06.Kemadruma")
    fs = facts(("in_house_from", {"graha": "Venus", "reference": "Moon", "house": 12}))
    assert not evaluate(card.conditions, fs).satisfied


def test_kemadruma_does_not_exclude_the_sun_or_nodes(cards):
    """Verse 5 states no exclusion, unlike Hora Sara's variant (deferred).
    A chart where the Sun alone occupies the 2nd from the Moon must not
    fire -- the Sun counts as a 'planet' here, same as any other graha."""
    card = next(c for c in cards if c.id == "PD.06.Kemadruma")
    fs = facts(("in_house_from", {"graha": "Sun", "reference": "Moon", "house": 2}))
    assert not evaluate(card.conditions, fs).satisfied


def test_kemadruma_jataka_parijata_variant_fires_on_unaspected_lagna_moon(cards):
    card = next(c for c in cards if c.id == "PD.06.Kemadruma.JatakaParijata1")
    fs = facts(("in_house", {"graha": "Moon", "house": 1}))
    assert evaluate(card.conditions, fs).satisfied


def test_kemadruma_jataka_parijata_variant_is_cancelled_by_jupiters_aspect(cards):
    card = next(c for c in cards if c.id == "PD.06.Kemadruma.JatakaParijata1")
    fs = facts(
        ("in_house", {"graha": "Moon", "house": 1}),
        ("aspects", {"graha": "Jupiter", "target": 1}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_kemadruma_jataka_parijata_variant_ignores_the_moon_elsewhere(cards):
    card = next(c for c in cards if c.id == "PD.06.Kemadruma.JatakaParijata1")
    fs = facts(("in_house", {"graha": "Moon", "house": 4}))
    assert not evaluate(card.conditions, fs).satisfied


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


# --- Vesi/Vasi/Ubhayachari, Kartari and Susubha (chapter 6 slice 5, v. 8-13) -

def test_subhavesi_fires_on_a_clean_mercury_second_from_the_sun(cards):
    """PD.06.Subhavesi: a benefic among the six-graha pool in the 2nd from
    the Sun. Mercury unassociated with malefics is the easiest benefic to
    produce without chapter 4, since Jupiter and Venus are never classified
    (concept:phaladeepika.nature-benefics)."""
    card = next(c for c in cards if c.id == "PD.06.Subhavesi")
    fs = facts(
        ("in_house_from", {"graha": "Mercury", "reference": "Sun", "house": 2}),
        ("nature", {"graha": "Mercury", "nature": "benefic"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_subhavesi_excludes_the_moon_even_when_the_moon_is_benefic(cards):
    """Verse 8 excludes the Moon by name from this yoga's pool, unlike
    Kemadruma's 'planets' at v.5. A waxing (benefic) Moon in the 2nd from
    the Sun must not satisfy Subhavesi."""
    card = next(c for c in cards if c.id == "PD.06.Subhavesi")
    fs = facts(
        ("in_house_from", {"graha": "Moon", "reference": "Sun", "house": 2}),
        ("nature", {"graha": "Moon", "nature": "benefic"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_subhavesi_excludes_the_nodes_even_if_they_were_benefic(cards):
    """Rahu/Ketu are always malefic in this store's own nature doctrine, so
    this is belt-and-braces: even a (hypothetically) benefic-tagged node
    must not satisfy the pool, because it is not one of the six named
    grahas verse 8 allows."""
    card = next(c for c in cards if c.id == "PD.06.Subhavesi")
    fs = facts(
        ("in_house_from", {"graha": "Rahu", "reference": "Sun", "house": 2}),
        ("nature", {"graha": "Rahu", "nature": "benefic"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_papavesi_fires_on_mars_second_from_the_sun(cards):
    """PD.06.Papavesi: named 'Papavesi' at v.8 and 'Asubhavesi' at v.10 for
    the same configuration; the card tests the condition regardless of
    which name is quoted for its effect."""
    card = next(c for c in cards if c.id == "PD.06.Papavesi")
    fs = facts(
        ("in_house_from", {"graha": "Mars", "reference": "Sun", "house": 2}),
        ("nature", {"graha": "Mars", "nature": "malefic"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_subhobhayachari_needs_both_houses_occupied(cards):
    """PD.06.Subhobhayachari: a benefic in the 2nd from the Sun alone is
    Subhavesi, not Subhobhayachari -- both the 2nd and 12th must be
    occupied by (not necessarily the same) benefic."""
    card = next(c for c in cards if c.id == "PD.06.Subhobhayachari")
    only_second = facts(
        ("in_house_from", {"graha": "Mercury", "reference": "Sun", "house": 2}),
        ("nature", {"graha": "Mercury", "nature": "benefic"}),
    )
    assert not evaluate(card.conditions, only_second).satisfied
    second_and_malefic_twelfth = facts(
        ("in_house_from", {"graha": "Mercury", "reference": "Sun", "house": 2}),
        ("nature", {"graha": "Mercury", "nature": "benefic"}),
        ("in_house_from", {"graha": "Saturn", "reference": "Sun", "house": 12}),
        ("nature", {"graha": "Saturn", "nature": "malefic"}),
    )
    # Saturn in the 12th is malefic, not benefic, so this still must not fire.
    assert not evaluate(card.conditions, second_and_malefic_twelfth).satisfied
    both_benefic = facts(
        ("in_house_from", {"graha": "Mercury", "reference": "Sun", "house": 2}),
        ("nature", {"graha": "Mercury", "nature": "benefic"}),
        ("in_house_from", {"graha": "Jupiter", "reference": "Sun", "house": 12}),
        ("nature", {"graha": "Jupiter", "nature": "benefic"}),
    )
    assert evaluate(card.conditions, both_benefic).satisfied


def test_subhakartari_reads_absolute_houses_from_the_lagna_not_the_sun(cards):
    """PD.06.Subhakartari: unlike the Vesi/Vasi family, this sentence carries
    no Sun-reference and no Moon/node exclusion -- it is benefics in the
    plain 2nd and 12th from the Lagna, on the full graha pool."""
    card = next(c for c in cards if c.id == "PD.06.Subhakartari")
    fs = facts(
        ("in_house", {"graha": "Moon", "house": 12}),
        ("nature", {"graha": "Moon", "nature": "benefic"}),
        ("in_house", {"graha": "Mercury", "house": 2}),
        ("nature", {"graha": "Mercury", "nature": "benefic"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_papakartari_does_not_fire_on_a_single_occupied_house(cards):
    card = next(c for c in cards if c.id == "PD.06.Papakartari")
    fs = facts(
        ("in_house", {"graha": "Saturn", "house": 2}),
        ("nature", {"graha": "Saturn", "nature": "malefic"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_susubha_fires_on_an_unaspected_benefic_in_the_second(cards):
    card = next(c for c in cards if c.id == "PD.06.Susubha")
    fs = facts(
        ("in_house", {"graha": "Mercury", "house": 2}),
        ("nature", {"graha": "Mercury", "nature": "benefic"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_susubha_is_cancelled_by_a_malefics_aspect_on_the_second(cards):
    """The cancellation is on the house, not on the graha occupying it --
    'without being aspected by malefics' targets the 2nd house itself."""
    card = next(c for c in cards if c.id == "PD.06.Susubha")
    fs = facts(
        ("in_house", {"graha": "Mercury", "house": 2}),
        ("nature", {"graha": "Mercury", "nature": "benefic"}),
        ("aspects", {"graha": "Saturn", "target": 2}),
        ("nature", {"graha": "Saturn", "nature": "malefic"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_amala_v12_is_a_citation_and_never_an_independent_claim(cards):
    """PD.06.Amala.V12 restates PD.06.Amala's own condition under a second
    verse number with different effect wording; it must carry no testable
    condition of its own, or the store would count one classical author
    saying the same thing once as two independent corroborating cards."""
    card = next(c for c in cards if c.id == "PD.06.Amala.V12")
    assert card.activation == "reference"
    assert card.conditions == {"all": []}


def test_subhavasi_fires_end_to_end_on_a_real_chart(provider):
    """Real-chart sanity check for this slice: 1990-06-01 06:15 IST at
    Thanjavur places Mercury, clean of malefic company, in the 12th house
    reckoned from the Sun -- PD.06.Subhavasi's condition -- via the actual
    ephemeris, not a hand-built FactSet."""
    from Engine.activate import activate
    rec = BirthRecord(
        date="1990-06-01", time="06:15", timezone="Asia/Kolkata",
        latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
        time_precision="minute", time_source="certificate", sex="male",
    )
    chart = compute_chart(resolve_birth(rec, provider), provider)
    cards = load_cards(RULES)
    doctrine = Doctrine.from_cards(cards)
    fs = extract_facts(chart, doctrine)
    claims, _ = activate(chart, fs, cards)
    fired = {c.derived["rule_card"] for c in claims}
    assert "PD.06.Subhavasi" in fired
    mercury_facts = {f.args["house"] for f in fs.by_predicate("in_house_from")
                      if f.args["graha"] == "Mercury" and f.args["reference"] == "Sun"}
    assert mercury_facts == {12}


# --- Srikantha/Srinatha/Virinchi and Maha/Dainya/Kahala (chapter 6 slice 6,
# vv. 28-34) ------------------------------------------------------------------

def test_srikantha_fires_when_lagna_lord_sun_and_moon_are_all_strong(cards):
    """PD.06.Srikantha: the Lagna lord, the Sun and the Moon each exalted,
    own, or in a friend's sign, each angular or trinal."""
    card = next(c for c in cards if c.id == "PD.06.Srikantha")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("dignity", {"graha": "Mars", "dignity": "own"}),
        ("in_house_class", {"graha": "Mars", "klass": "kendra"}),
        ("dignity", {"graha": "Sun", "dignity": "exalted"}),
        ("in_house_class", {"graha": "Sun", "klass": "trikona"}),
        ("dignity", {"graha": "Moon", "dignity": "friend"}),
        ("in_house_class", {"graha": "Moon", "klass": "kendra"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_srikantha_does_not_fire_if_only_two_of_the_three_qualify(cards):
    card = next(c for c in cards if c.id == "PD.06.Srikantha")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("dignity", {"graha": "Mars", "dignity": "own"}),
        ("in_house_class", {"graha": "Mars", "klass": "kendra"}),
        ("dignity", {"graha": "Sun", "dignity": "exalted"}),
        ("in_house_class", {"graha": "Sun", "klass": "trikona"}),
        # Moon present but with no dignity/angularity facts at all.
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_srinatha_tests_venus_the_9th_lord_and_mercury(cards):
    card = next(c for c in cards if c.id == "PD.06.Srinatha")
    fs = facts(
        ("dignity", {"graha": "Venus", "dignity": "own"}),
        ("in_house_class", {"graha": "Venus", "klass": "kendra"}),
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("dignity", {"graha": "Jupiter", "dignity": "exalted"}),
        ("in_house_class", {"graha": "Jupiter", "klass": "trikona"}),
        ("dignity", {"graha": "Mercury", "dignity": "own"}),
        ("in_house_class", {"graha": "Mercury", "klass": "kendra"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_virinchi_tests_jupiter_the_5th_lord_and_saturn(cards):
    card = next(c for c in cards if c.id == "PD.06.Virinchi")
    fs = facts(
        ("dignity", {"graha": "Jupiter", "dignity": "own"}),
        ("in_house_class", {"graha": "Jupiter", "klass": "kendra"}),
        ("lord_of_house", {"graha": "Venus", "house": 5}),
        ("dignity", {"graha": "Venus", "dignity": "friend"}),
        ("in_house_class", {"graha": "Venus", "klass": "trikona"}),
        ("dignity", {"graha": "Saturn", "dignity": "own"}),
        ("in_house_class", {"graha": "Saturn", "klass": "kendra"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_maha_fires_on_a_2nd_4th_exchange(cards):
    """Neither house is 3rd, 6th, 8th or 12th, so this is Maha."""
    card = next(c for c in cards if c.id == "PD.06.Maha")
    fs = facts(
        ("lord_of_house", {"graha": "Venus", "house": 2}),
        ("in_house", {"graha": "Venus", "house": 4}),
        ("lord_of_house", {"graha": "Mercury", "house": 4}),
        ("in_house", {"graha": "Mercury", "house": 2}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_dainya_fires_on_any_exchange_touching_6th_8th_or_12th(cards):
    """Verse 32: Dainya is 'caused by the lords of the 6th, 8th and 12th' --
    tested here for a 6th-Lagna pair, an 8th-9th pair, and a 6th-8th pair
    (both houses in the dusthana set at once)."""
    card = next(c for c in cards if c.id == "PD.06.Dainya")
    six_lagna = facts(
        ("lord_of_house", {"graha": "Saturn", "house": 6}),
        ("in_house", {"graha": "Saturn", "house": 1}),
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("in_house", {"graha": "Mars", "house": 6}),
    )
    assert evaluate(card.conditions, six_lagna).satisfied
    eight_nine = facts(
        ("lord_of_house", {"graha": "Saturn", "house": 8}),
        ("in_house", {"graha": "Saturn", "house": 9}),
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("in_house", {"graha": "Jupiter", "house": 8}),
    )
    assert evaluate(card.conditions, eight_nine).satisfied
    six_eight = facts(
        ("lord_of_house", {"graha": "Saturn", "house": 6}),
        ("in_house", {"graha": "Saturn", "house": 8}),
        ("lord_of_house", {"graha": "Mars", "house": 8}),
        ("in_house", {"graha": "Mars", "house": 6}),
    )
    assert evaluate(card.conditions, six_eight).satisfied


def test_kahala_fires_on_a_3rd_house_exchange_not_touching_a_dusthana(cards):
    card = next(c for c in cards if c.id == "PD.06.Kahala")
    fs = facts(
        ("lord_of_house", {"graha": "Mercury", "house": 3}),
        ("in_house", {"graha": "Mercury", "house": 11}),
        ("lord_of_house", {"graha": "Saturn", "house": 11}),
        ("in_house", {"graha": "Saturn", "house": 3}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_a_3rd_6th_exchange_is_dainya_not_kahala(cards):
    """Verse 32's own itemized Kahala list (p.69, intact) excludes 3rd-6th,
    3rd-8th and 3rd-12th pairs -- those are already Dainya, since a
    dusthana lord is involved. A pair touching both the 3rd and a dusthana
    must fire Dainya and must not fire Kahala or Maha."""
    dainya = next(c for c in cards if c.id == "PD.06.Dainya")
    kahala = next(c for c in cards if c.id == "PD.06.Kahala")
    maha = next(c for c in cards if c.id == "PD.06.Maha")
    fs = facts(
        ("lord_of_house", {"graha": "Mercury", "house": 3}),
        ("in_house", {"graha": "Mercury", "house": 6}),
        ("lord_of_house", {"graha": "Moon", "house": 6}),
        ("in_house", {"graha": "Moon", "house": 3}),
    )
    assert evaluate(dainya.conditions, fs).satisfied
    assert not evaluate(kahala.conditions, fs).satisfied
    assert not evaluate(maha.conditions, fs).satisfied


def test_maha_dainya_kahala_pair_sets_partition_all_66_exchanges(cards):
    """The three cards' literal house-pair enumerations were derived from
    verse 32's own stated arithmetic (66 = 30 + 8 + 28), not from the
    printed itemized list, which is independently confirmed defective.
    This is the arithmetic check: every one of the 66 possible house pairs
    must satisfy exactly one of the three cards' conditions."""
    import itertools
    maha = next(c for c in cards if c.id == "PD.06.Maha")
    dainya = next(c for c in cards if c.id == "PD.06.Dainya")
    kahala = next(c for c in cards if c.id == "PD.06.Kahala")
    counts = {"maha": 0, "dainya": 0, "kahala": 0, "none": 0, "multiple": 0}
    for h1, h2 in itertools.combinations(range(1, 13), 2):
        fs = facts(
            ("lord_of_house", {"graha": "A", "house": h1}),
            ("in_house", {"graha": "A", "house": h2}),
            ("lord_of_house", {"graha": "B", "house": h2}),
            ("in_house", {"graha": "B", "house": h1}),
        )
        hits = [name for name, card in
                (("maha", maha), ("dainya", dainya), ("kahala", kahala))
                if evaluate(card.conditions, fs).satisfied]
        if len(hits) == 0:
            counts["none"] += 1
        elif len(hits) > 1:
            counts["multiple"] += 1
        else:
            counts[hits[0]] += 1
    assert counts == {"maha": 28, "dainya": 30, "kahala": 8, "none": 0, "multiple": 0}


def test_vipareeta_raja_yoga_is_a_reference_card_contradicting_dainya(cards):
    """Uttarakalamrita's doctrine for the same 6th/8th/12th-lord
    configuration is explicitly 'quite reverse' of Phaladeepika's own
    Dainya effects; it must never fire and must record the contradiction,
    not silently agree or silently override."""
    card = next(c for c in cards if c.id == "PD.06.VipareetaRajaYoga.Uttarakalamrita")
    assert card.activation == "reference"
    assert card.conditions == {"all": []}
    assert "PD.06.Dainya" in card.raw.get("contradicts", [])


def test_maha_notes_list_defect_is_transcribed_exactly_as_printed():
    """Regression guard for the source defect discovered in this slice: the
    printed Maha Yogas Notes list is missing item (6) entirely and prints
    item (17) twice. If the corpus is ever re-converted and this defect
    disappears, PD.06.Maha's condition (derived from verse 32's own
    arithmetic, not from this list) must not be silently 'corrected' to
    match a repaired list without a human deciding that on purpose."""
    text = (ROOT / "Knowledge" / "phaladeepika.md").read_bytes().decode("utf-8")
    i = text.find("28. Maha Yogas:")
    j = text.find("30. Dainya Yogas:")
    assert i >= 0 and j > i
    maha_list = text[i:j]
    assert "(5) the Lord of the Lagna in the 10th" in maha_list
    assert "(6)" not in maha_list          # item (6) is genuinely absent
    assert maha_list.count("(17)") == 2    # item (17) is genuinely duplicated
    assert "(18)" not in maha_list         # item (18) is genuinely absent
    assert "(26)" not in maha_list         # item (26) is genuinely absent


def test_dainya_notes_list_truncations_are_transcribed_exactly_as_printed():
    text = (ROOT / "Knowledge" / "phaladeepika.md").read_bytes().decode("utf-8")
    i = text.find("30. Dainya Yogas:")
    j = text.find("8. Kahala Togas:")
    assert i >= 0 and j > i
    dainya_list = text[i:j]
    assert "(13) the lord of the 8th (14)" in dainya_list   # item 13 truncated
    assert "(28) the lord of 12th, (29)" in dainya_list      # item 28 truncated


def test_kahala_yoga_fires_end_to_end_on_a_real_chart(provider):
    """Real-chart sanity check: 1975-02-01 12:10 IST at Thanjavur places
    Mercury (3rd lord) in the 11th and Saturn (11th lord) in the 3rd,
    through the actual ephemeris -- a genuine Parivartana touching the 3rd
    house and no dusthana, i.e. PD.06.Kahala's condition."""
    from Engine.activate import activate
    rec = BirthRecord(
        date="1975-02-01", time="12:10", timezone="Asia/Kolkata",
        latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
        time_precision="minute", time_source="certificate", sex="male",
    )
    chart = compute_chart(resolve_birth(rec, provider), provider)
    cards = load_cards(RULES)
    doctrine = Doctrine.from_cards(cards)
    fs = extract_facts(chart, doctrine)
    claims, _ = activate(chart, fs, cards)
    fired = {c.derived["rule_card"] for c in claims}
    assert "PD.06.Kahala" in fired
    assert "PD.06.Dainya" not in fired
    assert "PD.06.Maha" not in fired
    kahala_claim = next(c for c in claims if c.derived["rule_card"] == "PD.06.Kahala")
    assert kahala_claim.derived["variables"] == {"?g1": "Mercury", "?g2": "Saturn"}


# --- Parvata and the dispositor-chain Kahala Yoga (chapter 6 slice 7, v.35-36)

def test_parvata_replicates_the_books_own_worked_example(cards):
    """Parvata Yoga: the lord of the Lagna's dispositor (the lord of the
    sign the Lagna lord occupies) is tested for dignity and angularity.
    Same numbers as the book's own example: Mars (lagna lord) in
    Sagittarius (9th); Jupiter (9th lord) exalted in the 4th, a kendra."""
    card = next(c for c in cards if c.id == "PD.06.Parvata")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("in_house", {"graha": "Mars", "house": 9}),
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("dignity", {"graha": "Jupiter", "dignity": "exalted"}),
        ("in_house_class", {"graha": "Jupiter", "klass": "kendra"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_parvata_does_not_fire_on_the_lagna_lord_alone(cards):
    """The Lagna lord's own placement is irrelevant to Parvata -- only its
    dispositor's dignity and angularity matter. A strong Lagna lord with no
    dispositor facts at all must not satisfy the condition."""
    card = next(c for c in cards if c.id == "PD.06.Parvata")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("dignity", {"graha": "Mars", "dignity": "own"}),
        ("in_house_class", {"graha": "Mars", "klass": "kendra"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_parvata_does_not_fire_if_the_dispositor_lacks_angularity(cards):
    card = next(c for c in cards if c.id == "PD.06.Parvata")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("in_house", {"graha": "Mars", "house": 9}),
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("dignity", {"graha": "Jupiter", "dignity": "exalted"}),
        # No in_house_class fact for Jupiter -- not angular.
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_kahala_dispositor_replicates_the_books_own_worked_example(cards):
    """PD.06.Kahala.Dispositor: the dispositor-chain Kahala Yoga of v.35,
    distinct from PD.06.Kahala (the Parivartana/exchange Kahala of v.32-34).
    Same numbers as the book's own example: Mars (lagna lord) in Leo (5th);
    Sun (5th lord) in Aquarius (1st); Saturn (Aquarius's lord) in the 7th,
    a kendra, dignified -- three hops, testing the third graha (Saturn),
    not the second (Sun)."""
    card = next(c for c in cards if c.id == "PD.06.Kahala.Dispositor")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("in_house", {"graha": "Mars", "house": 5}),
        ("lord_of_house", {"graha": "Sun", "house": 5}),
        ("in_house", {"graha": "Sun", "house": 1}),
        ("lord_of_house", {"graha": "Saturn", "house": 1}),
        ("dignity", {"graha": "Saturn", "dignity": "own"}),
        ("in_house_class", {"graha": "Saturn", "klass": "kendra"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_kahala_dispositor_does_not_fire_on_only_two_hops(cards):
    """Regression guard for the exact ambiguity this card's note documents:
    dignity/angularity on the SECOND graha in the chain (Sun, here) must
    not be enough on its own -- only a chain that actually reaches and
    tests the third graha may satisfy this card. This is what
    distinguishes PD.06.Kahala.Dispositor from a card that merely repeated
    PD.06.Parvata's two-hop test under a different name."""
    card = next(c for c in cards if c.id == "PD.06.Kahala.Dispositor")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("in_house", {"graha": "Mars", "house": 5}),
        ("lord_of_house", {"graha": "Sun", "house": 5}),
        ("dignity", {"graha": "Sun", "dignity": "exalted"}),
        ("in_house_class", {"graha": "Sun", "klass": "kendra"}),
        # Sun's own placement is never given, so no third hop can resolve.
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_kahala_dispositor_and_parivartana_kahala_are_independent_cards(cards):
    """The two Kahala Yogas share a name in the source (verse 32-34's
    Parivartana Kahala and verse 35's dispositor-chain Kahala) but are
    unrelated conditions and must be recorded as separate cards. Facts
    that satisfy the dispositor chain must not spuriously satisfy the
    exchange test, and vice versa."""
    dispositor = next(c for c in cards if c.id == "PD.06.Kahala.Dispositor")
    exchange = next(c for c in cards if c.id == "PD.06.Kahala")
    assert dispositor.id != exchange.id

    dispositor_facts = facts(
        ("lord_of_house", {"graha": "Mars", "house": 1}),
        ("in_house", {"graha": "Mars", "house": 5}),
        ("lord_of_house", {"graha": "Sun", "house": 5}),
        ("in_house", {"graha": "Sun", "house": 1}),
        ("lord_of_house", {"graha": "Saturn", "house": 1}),
        ("dignity", {"graha": "Saturn", "dignity": "own"}),
        ("in_house_class", {"graha": "Saturn", "klass": "kendra"}),
    )
    assert not evaluate(exchange.conditions, dispositor_facts).satisfied

    exchange_facts = facts(
        ("lord_of_house", {"graha": "Mercury", "house": 3}),
        ("in_house", {"graha": "Mercury", "house": 11}),
        ("lord_of_house", {"graha": "Saturn", "house": 11}),
        ("in_house", {"graha": "Saturn", "house": 3}),
    )
    assert not evaluate(dispositor.conditions, exchange_facts).satisfied


def test_kahala_dispositor_ambiguity_is_documented_not_silently_resolved(cards):
    """The two-vs-three-hop reading of verse 35's grammar is a genuine
    source ambiguity, not an engine defect. The card must say so rather
    than presenting its three-hop reading as the verse's only possible
    meaning."""
    card = next(c for c in cards if c.id == "PD.06.Kahala.Dispositor")
    assert "ambiguity" in card.raw["note"].lower() or "ambiguous" in card.raw["note"].lower()
    assert card.raw.get("exclusions")


def test_v35_kahala_definition_is_transcribed_exactly_as_printed():
    """Regression guard for the exact wording the two-vs-three-hop reading
    turns on: verse 35 names where the Lagna lord's dispositor 'is placed'
    before saying 'the lord of this sign', which is the textual basis for
    reading a third hop into the rule. If the corpus is ever re-converted,
    this exact clause must survive unchanged or the ambiguity analysis in
    PD.06.Kahala.Dispositor's note no longer applies to what is on the page."""
    text = (ROOT / "Knowledge" / "phaladeepika.md").read_bytes().decode("utf-8")
    assert (
        "and where the lord of the sign occupied by the lord of Lagna is "
        "placed. If the lord of this sign is in his sign of exaltation or "
        "own identical with kendra or trikona, the Yoga so formed is termed "
        "as Kahala Yoga"
    ) in text


def test_kahala_dispositor_worked_example_defect_is_transcribed_exactly():
    """Regression guard for the defect noted in PD.06.Kahala.Dispositor:
    the worked example's dignity phrase for Saturn is inconsistent with
    the houses the example itself states, and is quoted nowhere in the
    card -- deliberately, since the card's condition comes from the verse
    and the hop-count from the chain of grahas the example names, not from
    this specific dignity claim."""
    text = (ROOT / "Knowledge" / "phaladeepika.md").read_bytes().decode("utf-8")
    assert "Saturn, the lore, of Aquarius, is in 7th a kendra, in his own sign of exaltation" in text
    for card in load_cards(RULES):
        if card.id in ("PD.06.Kahala.Dispositor", "PD.06.Parvata"):
            assert "the lore, of Aquarius" not in card.quote


def test_parvata_and_kahala_dispositor_have_correct_provenance(cards):
    """Both cards must cite v.35-36 and the phaladeepika/p0071 or p0072
    page anchors, not be silently misattributed to a different verse."""
    for card_id in ("PD.06.Parvata", "PD.06.Kahala.Dispositor"):
        card = next(c for c in cards if c.id == card_id)
        assert card.verse == "35, 36"
        assert card.page_anchor in ("phaladeepika/p0071", "phaladeepika/p0072")
        assert card.chapter == 6
        assert card.book_id == "phaladeepika"


def test_kahala_dispositor_fires_end_to_end_on_a_real_chart(provider):
    """Real-chart sanity check: the golden 1987-03-14 04:22 IST chart at
    Thanjavur has Saturn (lagna lord) in the 11th, whose lord Mars sits in
    the 4th (a kendra) in Mars's own sign -- Mars is its own dispositor
    there, so the chain's third graha is Mars again. Both Parvata (tested
    at the second hop) and the dispositor Kahala (tested at the third,
    which happens to land back on the same graha here) must fire, and the
    exchange-based PD.06.Kahala must not."""
    from Engine.activate import activate
    rec = BirthRecord(
        date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
        latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
        time_precision="minute", time_source="certificate",
    )
    chart = compute_chart(resolve_birth(rec, provider), provider)
    cards = load_cards(RULES)
    doctrine = Doctrine.from_cards(cards)
    fs = extract_facts(chart, doctrine)
    claims, _ = activate(chart, fs, cards)
    fired = {c.derived["rule_card"] for c in claims}
    assert "PD.06.Parvata" in fired
    assert "PD.06.Kahala.Dispositor" in fired
    assert "PD.06.Kahala" not in fired
    parvata_claim = next(c for c in claims if c.derived["rule_card"] == "PD.06.Parvata")
    assert parvata_claim.derived["variables"]["?g1"] == "Saturn"
    assert parvata_claim.derived["variables"]["?g2"] == "Mars"
    dispositor_claim = next(c for c in claims if c.derived["rule_card"] == "PD.06.Kahala.Dispositor")
    assert dispositor_claim.derived["variables"]["?g3"] == "Mars"


# --- Raja Yoga and Shankha Yoga (chapter 6 slice 8, v.37-38) ----------------

def test_raja_yoga_fires_when_9th_and_10th_lords_share_an_auspicious_house():
    """Raja Yoga: the 9th lord and the 10th lord occupying, together, one
    house classed 'auspicious' (every house but the 6th, 8th and 12th, per
    PD.01.HouseClass.Auspicious -- v.37 does not say 'kendra or trikona')."""
    card = next(c for c in load_cards(RULES) if c.id == "PD.06.RajaYoga")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("lord_of_house", {"graha": "Saturn", "house": 10}),
        ("in_house", {"graha": "Jupiter", "house": 1}),
        ("in_house", {"graha": "Saturn", "house": 1}),
        ("house_class", {"house": 1, "klass": "auspicious"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_raja_yoga_does_not_fire_if_the_shared_house_is_not_auspicious():
    """The house the lords share must itself be classed 'auspicious'. A
    dusthana with no such classification fact must not satisfy the card."""
    card = next(c for c in load_cards(RULES) if c.id == "PD.06.RajaYoga")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("lord_of_house", {"graha": "Saturn", "house": 10}),
        ("in_house", {"graha": "Jupiter", "house": 8}),
        ("in_house", {"graha": "Saturn", "house": 8}),
        ("house_class", {"house": 8, "klass": "dusthana"}),
        # No house_class(8, auspicious) fact -- house 8 is not auspicious.
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_raja_yoga_does_not_fire_if_the_lords_are_not_together():
    """'Conjunction or association ... in any auspicious house' requires the
    two lords to occupy the *same* house, not merely two auspicious ones."""
    card = next(c for c in load_cards(RULES) if c.id == "PD.06.RajaYoga")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("lord_of_house", {"graha": "Saturn", "house": 10}),
        ("in_house", {"graha": "Jupiter", "house": 1}),
        ("in_house", {"graha": "Saturn", "house": 3}),
        ("house_class", {"house": 1, "klass": "auspicious"}),
        ("house_class", {"house": 3, "klass": "auspicious"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_shankha_yoga_fires_for_any_kendra_and_trikona_lord_pair():
    """Shankha Yoga: the general form of PD.06.RajaYoga -- any kendra lord
    and any trikona lord (not just the 10th and 9th specifically) together
    in an auspicious house."""
    card = next(c for c in load_cards(RULES) if c.id == "PD.06.Shankha")
    fs = facts(
        ("lord_of_house", {"graha": "Mars", "house": 4}),
        ("house_class", {"house": 4, "klass": "kendra"}),
        ("lord_of_house", {"graha": "Mercury", "house": 5}),
        ("house_class", {"house": 5, "klass": "trikona"}),
        ("in_house", {"graha": "Mars", "house": 2}),
        ("in_house", {"graha": "Mercury", "house": 2}),
        ("house_class", {"house": 2, "klass": "auspicious"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_shankha_yoga_can_be_satisfied_by_one_graha_lording_both_roles():
    """No distinctness constraint is placed on the kendra lord and the
    trikona lord (see PD.06.Shankha's note and PD.06.Lakshmi's precedent):
    a single graha that lords both a kendra and a trikona sign at once must
    still satisfy the card when it occupies an auspicious house."""
    card = next(c for c in load_cards(RULES) if c.id == "PD.06.Shankha")
    fs = facts(
        ("lord_of_house", {"graha": "Venus", "house": 10}),
        ("house_class", {"house": 10, "klass": "kendra"}),
        ("lord_of_house", {"graha": "Venus", "house": 5}),
        ("house_class", {"house": 5, "klass": "trikona"}),
        ("in_house", {"graha": "Venus", "house": 1}),
        ("house_class", {"house": 1, "klass": "auspicious"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_raja_yoga_is_a_specific_case_of_shankha_yoga():
    """The 9th is a trikona and the 10th a kendra, so every chart satisfying
    PD.06.RajaYoga's condition also satisfies PD.06.Shankha's -- the source
    states the specific case (9th/10th) alongside its own general case
    (any kendra/trikona pair) in the same verse, so both cards must fire
    together on such a chart; this is not treated as a duplicate."""
    cards = load_cards(RULES)
    raja = next(c for c in cards if c.id == "PD.06.RajaYoga")
    shankha = next(c for c in cards if c.id == "PD.06.Shankha")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 9}),
        ("house_class", {"house": 9, "klass": "trikona"}),
        ("lord_of_house", {"graha": "Saturn", "house": 10}),
        ("house_class", {"house": 10, "klass": "kendra"}),
        ("in_house", {"graha": "Jupiter", "house": 1}),
        ("in_house", {"graha": "Saturn", "house": 1}),
        ("house_class", {"house": 1, "klass": "auspicious"}),
    )
    assert evaluate(raja.conditions, fs).satisfied
    assert evaluate(shankha.conditions, fs).satisfied


def test_raja_and_shankha_have_correct_provenance():
    for card_id in ("PD.06.RajaYoga", "PD.06.Shankha"):
        card = next(c for c in load_cards(RULES) if c.id == card_id)
        assert card.verse == "37, 38"
        assert card.page_anchor == "phaladeepika/p0073"
        assert card.chapter == 6
        assert card.book_id == "phaladeepika"


# --- PD.08.Saturn.01 dignity split (chapter 8 verification, 2026-08-24) -----

def test_saturn_in_lagna_own_or_exalted_fires_only_the_favourable_card():
    """The quote states two mutually exclusive outcomes for Saturn in the
    Lagna, conditioned on its dignity there. Own/exaltation must fire
    .OwnOrExalted and must not fire .OtherSign."""
    cards = load_cards(RULES)
    good = next(c for c in cards if c.id == "PD.08.Saturn.01.OwnOrExalted")
    bad = next(c for c in cards if c.id == "PD.08.Saturn.01.OtherSign")
    fs = facts(
        ("in_house", {"graha": "Saturn", "house": 1}),
        ("dignity", {"graha": "Saturn", "dignity": "exalted"}),
    )
    assert evaluate(good.conditions, fs).satisfied
    assert not evaluate(bad.conditions, fs).satisfied


def test_saturn_in_lagna_other_sign_fires_only_the_unfavourable_card():
    """Saturn in the Lagna in any sign that is neither its own nor its
    exaltation sign must fire .OtherSign and must not fire .OwnOrExalted."""
    cards = load_cards(RULES)
    good = next(c for c in cards if c.id == "PD.08.Saturn.01.OwnOrExalted")
    bad = next(c for c in cards if c.id == "PD.08.Saturn.01.OtherSign")
    fs = facts(
        ("in_house", {"graha": "Saturn", "house": 1}),
        ("dignity", {"graha": "Saturn", "dignity": "neutral"}),
    )
    assert not evaluate(good.conditions, fs).satisfied
    assert evaluate(bad.conditions, fs).satisfied


def test_saturn_in_lagna_own_sign_also_fires_the_favourable_card():
    """'Sign of exaltation ... or in his own sign' -- own sign is the other
    half of the disjunction, not just exaltation."""
    card = next(c for c in load_cards(RULES) if c.id == "PD.08.Saturn.01.OwnOrExalted")
    fs = facts(
        ("in_house", {"graha": "Saturn", "house": 1}),
        ("dignity", {"graha": "Saturn", "dignity": "own"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_v37_raja_shankha_definition_is_transcribed_exactly_as_printed():
    """Regression guard for the exact source wording PD.06.RajaYoga's note
    relies on: the Shankha Yoga sentence, printed immediately after v.37's
    Raja Yoga sentence, is the book's own gloss of 'occupy together an
    auspicious house' -- if the corpus is ever re-converted, this clause
    must survive unchanged or that reading is no longer textually grounded."""
    text = (ROOT / "Knowledge" / "phaladeepika.md").read_bytes().decode("utf-8")
    assert (
        "37. The conjunction or association of the lords of 9th and the "
        "10th house in any auspicious house consitutes Raja Yoga."
    ) in text
    assert (
        "If the lords of a Kendra and Trikona are similarly placed (that "
        "is, they occupy together an auspicious house), the Yoga so formed "
        "is called Shankha Yoga."
    ) in text


def test_shankha_fires_end_to_end_on_a_real_chart(provider):
    """Real-chart sanity check: on the golden 1987-03-14 04:22 IST chart at
    Thanjavur, Venus lords both the 10th (a kendra, Libra) and the 5th (a
    trikona, Taurus), and sits in the 1st (an auspicious house) -- the same
    graha satisfying both the kendra-lord and trikona-lord roles at once,
    exactly the edge case PD.06.Shankha's note describes. PD.06.RajaYoga
    must not fire on this chart: the 9th and 10th lords are not together."""
    from Engine.activate import activate
    rec = BirthRecord(
        date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
        latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
        time_precision="minute", time_source="certificate",
    )
    chart = compute_chart(resolve_birth(rec, provider), provider)
    cards = load_cards(RULES)
    doctrine = Doctrine.from_cards(cards)
    fs = extract_facts(chart, doctrine)
    claims, _ = activate(chart, fs, cards)
    fired = {c.derived["rule_card"] for c in claims}
    assert "PD.06.Shankha" in fired
    assert "PD.06.RajaYoga" not in fired
    shankha_claim = next(c for c in claims if c.derived["rule_card"] == "PD.06.Shankha")
    assert shankha_claim.derived["variables"]["?g1"] == "Venus"
    assert shankha_claim.derived["variables"]["?g2"] == "Venus"


# --- Milestone 19: chapter 10 verification pass ------------------------------
#
# Phaladeepika 10 v.15 states four ways the lord of the 7th may be afflicted:
# "posited in his sign of debilitation, be in an inimical sign, be combust or be
# aspected by a malefic". The encoded condition carried only three of them --
# "be in an inimical sign" was missing -- so the card under-fired on a chart the
# verse plainly covers. These tests pin all four alternatives, and pin that the
# verse's second, conjoined requirement is still required.

def test_seventh_lord_in_an_inimical_sign_fires_the_loss_of_wife_card():
    """The alternative that was missing. dignity(?l,"inimical") is derivable via
    dep.dignity-friendship and is used by the sibling card from the same
    doctrine, so its absence here was an omission, not a capability gap."""
    cards = load_cards(RULES)
    card = next(c for c in cards if c.id == "PD.10.WifeLoss.Lord7Afflicted")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 7}),
        ("dignity", {"graha": "Jupiter", "dignity": "inimical"}),
        ("nature_occupancy", {"house": 7, "nature": "malefic"}),
    )
    assert evaluate(card.conditions, fs).satisfied


@pytest.mark.parametrize("affliction", [
    ("dignity", {"graha": "Jupiter", "dignity": "debilitated"}),
    ("dignity", {"graha": "Jupiter", "dignity": "inimical"}),
    ("combust", {"graha": "Jupiter"}),
])
def test_each_affliction_of_the_seventh_lord_fires_independently(affliction):
    """The verse's list is a disjunction: any one affliction suffices, provided
    the 7th house is itself afflicted."""
    cards = load_cards(RULES)
    card = next(c for c in cards if c.id == "PD.10.WifeLoss.Lord7Afflicted")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 7}),
        affliction,
        ("nature_occupancy", {"house": 7, "nature": "malefic"}),
    )
    assert evaluate(card.conditions, fs).satisfied


def test_afflicted_seventh_lord_alone_does_not_fire_without_an_afflicted_seventh():
    """"...and the 7th house be occupied or aspected by a malefic" is conjoined,
    not another alternative. An inimical 7th lord on its own must stay silent."""
    cards = load_cards(RULES)
    card = next(c for c in cards if c.id == "PD.10.WifeLoss.Lord7Afflicted")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 7}),
        ("dignity", {"graha": "Jupiter", "dignity": "inimical"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_unafflicted_seventh_lord_does_not_fire_on_an_afflicted_seventh_alone():
    """The other half of the conjunction: a malefic in the 7th proves nothing
    unless the 7th lord is itself afflicted one of the four stated ways."""
    cards = load_cards(RULES)
    card = next(c for c in cards if c.id == "PD.10.WifeLoss.Lord7Afflicted")
    fs = facts(
        ("lord_of_house", {"graha": "Jupiter", "house": 7}),
        ("nature_occupancy", {"house": 7, "nature": "malefic"}),
    )
    assert not evaluate(card.conditions, fs).satisfied


def test_any_is_a_literal_not_a_wildcard_so_stub_conditions_are_fail_safe():
    """Chapter 10 holds seven inert placeholder cards whose conditions are stubs
    like `lord_of_house(any, 7)`, kept until dep.strength / dep.varga / dep.dasa
    exist. Milestone 16's note on PD.01.Kalapurusha.Strength claimed such a leaf
    is "vacuously true ... every house always has a lord"; it is not. Only
    ?-prefixed arguments quantify, so "any" is matched by string equality and
    matches no fact. The leaf is vacuously FALSE, which makes every stub card
    fail-safe rather than a latent over-fire -- and means these cards must have
    their conditions rewritten when their dependency lands, not merely have
    `activation` flipped."""
    fs = facts(("lord_of_house", {"graha": "Jupiter", "house": 7}))
    assert evaluate({"all": [{"lord_of_house": {"graha": "?g", "house": 7}}]}, fs).satisfied
    assert not evaluate({"all": [{"lord_of_house": {"graha": "any", "house": 7}}]}, fs).satisfied


def test_chapter_ten_interpretive_cards_are_signed_off_except_the_one_holdout():
    """The chapter 10 verification batch. PD.10.Venus.VargaMarsSaturn is
    deliberately left unsigned: its varga branch does not encode "the Varga of
    Mars or Saturn" and repairing it requires deciding what "Varga" denotes,
    which belongs to whoever encodes the varga doctrine, not to a review pass."""
    import json
    doc = json.loads((RULES / "phaladeepika" / "ch10.json").read_text(encoding="utf-8"))
    unsigned = [c["id"] for c in doc["cards"]
                if not (c.get("extraction") or {}).get("verified_by")]
    assert unsigned == ["PD.10.Venus.VargaMarsSaturn"]


# --- Milestone 20: the Moon question, and the scope guard on chapter 4 -------
#
# Two books now classify grahas by nature. They agree everywhere they both
# speak, with one exception that is not an agreement or a disagreement so much
# as a question the project has deliberately refused to answer yet: what makes
# the Moon malefic. These tests pin the refusal, so that a later session cannot
# quietly resolve it by editing a card.

def test_the_moon_is_classified_by_one_book_only_and_the_other_does_not_touch_it():
    """The second book quotes a Moon clause but asserts nothing about the Moon.

    Its printed English glosses the Sanskrit क्षीण as "(within less than 72
    degrees distance from Sun)". The verse carries no numeral -- the figure is
    the translator's parenthetical. Encoding it as doctrine would manufacture a
    cross-book contradiction out of two renderings of one word; encoding it as
    the other book's "waning" would substitute that book's wording for what this
    page prints. The card does neither, so the first book's Moon doctrine
    governs the Moon unopposed and is not overwritten.
    """
    cards = load_cards(RULES)
    natures = [c for c in cards if c.predicts.get("relation") == "graha_nature"]
    second_book = [c for c in natures if c.book_id != "phaladeepika"]
    assert second_book, "expected a second book's nature cards in the store"
    for c in second_book:
        named = set(c.predicts.get("grahas", ()))
        conditional = {x["graha"] for x in c.predicts.get("conditional", ())}
        assert "Moon" not in named, c.id
        assert "Moon" not in conditional, c.id
        # ...but it must still quote the clause, or the card would be hiding it.
        assert "Moon" in c.quote, c.id


def test_the_moon_disagreement_is_registered_rather_than_resolved():
    """An open question must be visible in the backlog, not just in a comment."""
    registry = json.loads((RULES / "deferred.json").read_text(encoding="utf-8"))
    entry = next((e for e in registry["entries"]
                  if e["id"] == "concept:moon-nature-criterion"), None)
    assert entry is not None, "the Moon criterion question is not registered"
    assert entry["status"] == "deferred"
    assert "72" in entry["what"]


def test_the_moon_still_resolves_from_the_book_that_does_classify_it(fs):
    """Whatever the Moon's nature is on this chart, it comes from one authority."""
    moon = next(f for f in fs.by_predicate("nature") if f.args["graha"] == "Moon")
    assert moon.evidence["books"] == ["phaladeepika"]
    assert moon.evidence["corroborated"] is False
    assert "phase is" in moon.evidence["basis"]


def test_the_kala_bala_benefic_list_is_not_encoded_as_general_nature_doctrine():
    """Guard against over-applying a scoped statement.

    Chapter 4 of the first book also names Jupiter and Venus benefic -- inside
    its Kala Bala rules, whose following sentences scope Mercury's treatment to
    that computation explicitly and in open disagreement with chapter 2. Read as
    general doctrine it would also make the Moon unconditionally benefic and
    collide with chapter 2's phase rule. It was rejected as the source for that
    reason; this test fails if a later session encodes it as `graha_nature`.
    """
    cards = load_cards(RULES)
    for c in cards:
        if c.predicts.get("relation") == "graha_nature":
            assert c.chapter != 4, (
                f"{c.id} encodes chapter 4 as general nature doctrine; that "
                f"statement is scoped to Kala Bala -- see "
                f"concept:kala-bala-benefic-scope")


def test_the_kala_bala_scope_decision_is_registered():
    registry = json.loads((RULES / "deferred.json").read_text(encoding="utf-8"))
    entry = next((e for e in registry["entries"]
                  if e["id"] == "concept:kala-bala-benefic-scope"), None)
    assert entry is not None
    assert entry["status"] == "deferred"


def test_contradicting_authorities_still_refuse_to_be_adjudicated(chart):
    """Corroboration must not have quietly become conflict resolution.

    Recording a second agreeing authority is not the same as choosing between
    two disagreeing ones, and the engine must still refuse the latter. The error
    now has to name both sides, so an encoder can find the offending pair.
    """
    class Contradictory:
        def graha_natures(self):
            from Engine.doctrine import Sourced
            return Sourced([
                {"nature": "malefic", "grahas": ["Jupiter"], "conditional": [],
                 "card": "XX.01.A", "book": "book-one"},
                {"nature": "benefic", "grahas": ["Jupiter"], "conditional": [],
                 "card": "YY.01.B", "book": "book-two"},
            ], ("XX.01.A", "YY.01.B"))

    from Engine.facts import DoctrineReport, _resolve_nature
    with pytest.raises(DoctrineError) as exc:
        _resolve_nature(chart, Contradictory(), DoctrineReport())
    message = str(exc.value)
    assert "Jupiter" in message
    assert "XX.01.A" in message and "YY.01.B" in message
