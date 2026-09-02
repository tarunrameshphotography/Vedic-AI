"""Tests for the doctrine-backed extractors.

Three kinds, deliberately:

  * **Unit** tests build a tiny synthetic reference store and check each
    extractor's logic against it. They must not read the real corpus, so that
    a change in Phaladeepika cannot quietly repair a broken extractor.
  * **Golden chart** tests run the real store against a fixed nativity and
    assert exact values, worked out by hand from the encoded tables.
  * **Discipline** tests assert the property the whole design rests on: that
    no classical content is written in Python.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine, DoctrineError
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import extract_facts
from Engine.rules import load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)


# --- fixtures ---------------------------------------------------------------

@pytest.fixture(scope="module")
def provider():
    p = SwissEphemerisDLL()
    yield p
    p.close()


@pytest.fixture(scope="module")
def chart(provider):
    return compute_chart(resolve_birth(DEMO, provider), provider)


@pytest.fixture(scope="module")
def real_doctrine():
    return Doctrine.from_cards(load_cards(RULES))


@pytest.fixture(scope="module")
def facts(chart, real_doctrine):
    return extract_facts(chart, real_doctrine)


def synthetic(tmp_path, cards):
    """A minimal reference store on disk, loaded the ordinary way.

    Built through load_cards rather than by constructing RuleCards directly, so
    these tests exercise the same path the engine uses.
    """
    doc = {"book_id": "phaladeepika", "chapter": 1, "cards": []}
    for i, (relation, predicts) in enumerate(cards, start=1):
        doc["cards"].append({
            "id": f"XX.01.Synthetic{i:03d}", "schema": 1,
            "source": {"book_id": "phaladeepika", "chapter": 1, "verse": "1",
                       "page_anchor": None, "tier": 1, "quote": f"q{i}",
                       "quote_display": f"q{i}", "quote_sha256": "0" * 64,
                       "char_span": [0, 2], "span_trimmed": None},
            "scope": {}, "activation": "reference",
            "conditions": {"all": []},
            "predicts": {"relation": relation, **predicts},
            "timing": "natal", "weight": 1.0, "specificity": 1,
        })
    d = tmp_path / "synthetic"
    d.mkdir(parents=True, exist_ok=True)
    (d / "ch01.json").write_text(json.dumps(doc), encoding="utf-8")
    return Doctrine.from_cards(load_cards(tmp_path))


# --- unit: the doctrine layer -----------------------------------------------

def test_missing_doctrine_raises_rather_than_defaults(tmp_path):
    """A silently-defaulted table is indistinguishable from a sourced one."""
    doc = synthetic(tmp_path, [("sign_lord", {"sign": "Aries", "graha": "Mars"})])
    assert doc.sign_lord("Aries").value == "Mars"
    with pytest.raises(DoctrineError, match="does not say"):
        doc.sign_lord("Taurus")
    with pytest.raises(DoctrineError, match="has not been encoded"):
        doc.graha_classes()


def test_two_authorities_are_not_silently_reconciled(tmp_path):
    """Adjudication is Stage 7's job, and Stage 7 does not exist."""
    doc = synthetic(tmp_path, [
        ("sign_lord", {"sign": "Aries", "graha": "Mars"}),
        ("sign_lord", {"sign": "Aries", "graha": "Ketu"}),
    ])
    with pytest.raises(DoctrineError, match="cannot choose between authorities"):
        doc.sign_lord("Aries")


def test_every_lookup_names_the_cards_it_read(tmp_path):
    doc = synthetic(tmp_path, [("sign_lord", {"sign": "Aries", "graha": "Mars"})])
    value, cards = doc.sign_lord("Aries")
    assert value == "Mars"
    assert cards == ("XX.01.Synthetic001",)


# --- unit: lordship ---------------------------------------------------------

def test_lordship_follows_the_lagna_not_a_fixed_table(tmp_path, chart):
    """A house has a lord only once the lagna fixes which sign it is."""
    doc = synthetic(tmp_path, [
        ("sign_lord", {"sign": s, "graha": g}) for s, g in [
            ("Capricorn", "Saturn"), ("Aquarius", "Saturn"), ("Pisces", "Jupiter"),
            ("Aries", "Mars"), ("Taurus", "Venus"), ("Gemini", "Mercury"),
            ("Cancer", "Moon"), ("Leo", "Sun"), ("Virgo", "Mercury"),
            ("Libra", "Venus"), ("Scorpio", "Mars"), ("Sagittarius", "Jupiter")]])
    fs = extract_facts(chart, doc)
    # Capricorn lagna: the 1st is Capricorn (Saturn), the 4th Aries (Mars).
    assert "lord_of_house(Saturn,1)" in fs
    assert "lord_of_house(Mars,4)" in fs
    assert "lord_of_house(Sun,8)" in fs        # 8th is Leo
    assert len(fs.by_predicate("lord_of_house")) == 12


# --- unit: aspects ----------------------------------------------------------

def test_special_full_aspects_override_the_general_glance(tmp_path, chart):
    doc = synthetic(tmp_path, [
        ("aspect", {"table": {"3": 0.25, "10": 0.25, "5": 0.5, "9": 0.5,
                              "4": 0.75, "8": 0.75, "7": 1.0}}),
        ("aspect_special", {"full": {"Saturn": [3, 10], "Jupiter": [5, 9],
                                     "Mars": [4, 8]}}),
    ])
    assert sorted(h for h, s in doc.aspect_offsets("Venus").value.items()
                  if s >= 1.0) == [7]
    assert sorted(h for h, s in doc.aspect_offsets("Mars").value.items()
                  if s >= 1.0) == [4, 7, 8]
    assert sorted(h for h, s in doc.aspect_offsets("Saturn").value.items()
                  if s >= 1.0) == [3, 7, 10]


def test_partial_glances_are_kept_in_evidence_not_asserted(tmp_path, chart):
    """Emitting quarter glances as `aspects` would make every rule fire."""
    doc = synthetic(tmp_path, [
        ("aspect", {"table": {"3": 0.25, "7": 1.0}}),
        ("aspect_special", {"full": {}}),
    ])
    fs = extract_facts(chart, doc)
    venus = chart.bodies["Venus"]
    seventh = ((venus.house - 1 + 6) % 12) + 1
    assert f"aspects(Venus,{seventh})" in fs
    third = ((venus.house - 1 + 2) % 12) + 1
    assert f"aspects(Venus,{third})" not in fs
    ev = fs.get(f"aspects(Venus,{seventh})").evidence
    assert ev["partial_glances"][3] == 0.25
    assert ev["interpretation"] == "full drishti only"


# --- unit: combustion -------------------------------------------------------

def test_combustion_uses_the_retrograde_orb_when_retrograde(tmp_path, chart):
    doc = synthetic(tmp_path, [
        ("combustion_orb", {"measured_from": "Sun",
                            "table": {"Mercury": 14, "Mercury_retrograde": 12}}),
    ])
    assert doc.combustion_orb("Mercury", False).value == 14
    assert doc.combustion_orb("Mercury", True).value == 12
    # A graha the table does not name has no orb, and absence is not zero.
    assert doc.combustion_orb("Rahu", False).value is None
    fs = extract_facts(chart, doc)
    assert "combust(Rahu)" not in fs


def test_combustion_is_measured_from_the_body_the_card_names(tmp_path, chart):
    """Even "the Sun" is doctrine; the engine must not assert it."""
    doc = synthetic(tmp_path, [
        ("combustion_orb", {"measured_from": "Moon", "table": {"Mars": 180}}),
    ])
    fs = extract_facts(chart, doc)
    # With an absurd orb measured from the Moon, Mars is combust by the Moon.
    assert "combust(Mars)" in fs
    assert fs.get("combust(Mars)").evidence["orb"] == 180


# --- unit: dignity ----------------------------------------------------------

def test_dignity_reports_exaltation_and_debilitation(tmp_path, chart):
    doc = synthetic(tmp_path, [
        ("exaltation", {"graha": "Mars", "exaltation_sign": "Aries",
                        "debilitation_sign": "Cancer"}),
    ])
    fs = extract_facts(chart, doc)
    # Mars is in Aries in this chart, so this synthetic table exalts it.
    assert "dignity(Mars,exalted)" in fs
    assert "dignity(Mars,debilitated)" not in fs


def test_deep_exaltation_is_a_point_and_is_not_asserted_as_a_state(tmp_path, chart):
    """The texts give a degree, not an orb. No card may invent a range."""
    doc = synthetic(tmp_path, [
        ("exaltation", {"graha": "Mars", "exaltation_sign": "Aries",
                        "debilitation_sign": "Cancer"}),
        ("deep_exaltation", {"graha": "Mars", "exaltation_sign": "Aries",
                             "exaltation_degree": 28, "debilitation_sign": "Cancer",
                             "debilitation_degree": 28}),
    ])
    fs = extract_facts(chart, doc)
    assert not [f for f in fs.by_predicate("dignity")
                if "deep" in f.args["dignity"]]
    ev = fs.get("dignity(Mars,exalted)").evidence
    assert ev["deep_exaltation_degree"] == 28
    mars = chart.bodies["Mars"]
    assert ev["arc_from_deep_point"] == pytest.approx(abs(mars.deg_in_sign - 28), abs=1e-6)


def test_moolatrikona_respects_the_printed_portion(tmp_path, chart):
    """Mars sits at ~21 Aries; a 0-12 portion must not match it."""
    base = [("sign_lord", {"sign": "Aries", "graha": "Ketu"}),
            ("exaltation", {"graha": "Mars", "exaltation_sign": "Leo",
                            "debilitation_sign": "Aquarius"})]
    inside = synthetic(tmp_path / "a", base + [
        ("moolatrikona", {"graha": "Mars", "sign": "Aries", "portion": [0, 30],
                          "portion_resolved": True})])
    assert "dignity(Mars,moolatrikona)" in extract_facts(chart, inside)

    outside = synthetic(tmp_path / "b", base + [
        ("moolatrikona", {"graha": "Mars", "sign": "Aries", "portion": [0, 12],
                          "portion_resolved": True})])
    assert "dignity(Mars,moolatrikona)" not in extract_facts(chart, outside)


def test_an_unresolved_portion_asserts_nothing(tmp_path, chart):
    """The scan garbled Mars's row; a garbled row must not become a fact."""
    doc = synthetic(tmp_path, [
        ("exaltation", {"graha": "Mars", "exaltation_sign": "Leo",
                        "debilitation_sign": "Aquarius"}),
        ("moolatrikona", {"graha": "Mars", "sign": "Aries", "portion": [0, 30],
                          "portion_resolved": False})])
    assert "dignity(Mars,moolatrikona)" not in extract_facts(chart, doc)


# --- unit: natural friendship (dep.dignity-friendship) ----------------------

def test_friendship_reads_the_occupants_own_row_not_the_lords(tmp_path, chart):
    """"In the house of a friend" is the sign lord's standing in the
    occupant's row, not the occupant's standing in the lord's -- the two can
    disagree, and only one of them is what the verse asks for. Saturn sits in
    Scorpio in this chart; Scorpio's lord here is made Mars."""
    assert chart.bodies["Saturn"].sign == "Scorpio"
    doc = synthetic(tmp_path, [
        ("sign_lord", {"sign": "Scorpio", "graha": "Mars"}),
        ("natural_relationship", {"table": {
            "Saturn": {"friend": [], "neutral": ["Mars"], "enemy": []},
            "Mars": {"friend": [], "neutral": [], "enemy": ["Saturn"]},
        }}),
    ])
    fs = extract_facts(chart, doc)
    assert "dignity(Saturn,neutral)" in fs
    assert "dignity(Saturn,inimical)" not in fs


def test_a_graha_in_its_own_sign_gets_no_friendship_fact(tmp_path, chart):
    """Own-sign dignity is a different, already-sourced fact; this extractor
    must not duplicate it by inventing a self-relation the table never
    states. Mars sits in Aries, its own sign, in this chart."""
    assert chart.bodies["Mars"].sign == "Aries"
    doc = synthetic(tmp_path, [
        ("sign_lord", {"sign": "Aries", "graha": "Mars"}),
        ("natural_relationship", {"table": {
            "Mars": {"friend": ["Sun"], "neutral": ["Venus"], "enemy": ["Mercury"]},
        }}),
    ])
    fs = extract_facts(chart, doc)
    assert not [f for f in fs.by_predicate("dignity")
                if f.args["graha"] == "Mars" and f.args["dignity"] in
                ("friend", "neutral", "inimical")]


def test_the_moon_mercury_contradiction_is_surfaced_not_resolved(tmp_path, chart):
    """The printed defect this table preserves: Mercury is both Moon's friend
    and neutral. The engine must not pick, and must say why not."""
    moon_sign = chart.bodies["Moon"].sign
    doc = synthetic(tmp_path, [
        ("sign_lord", {"sign": moon_sign, "graha": "Mercury"}),
        ("natural_relationship", {"table": {
            "Moon": {"friend": ["Mercury"], "neutral": ["Mercury"], "enemy": []},
        }}),
    ])
    with pytest.raises(DoctrineError, match="both friend and neutral"):
        doc.natural_relationship("Moon", "Mercury")
    # extract_facts must not propagate the raise: it is reported, not fatal.
    fs = extract_facts(chart, doc)
    assert not [f for f in fs.by_predicate("dignity") if f.args["graha"] == "Moon"]
    assert "contradicts itself" in fs.doctrine.partial.get("dignity_friendship", "")


def test_rahu_and_ketu_are_read_from_their_own_card(tmp_path):
    """Verse 35 gives the nodes one shared row in a different card shape from
    the seven-graha table; both must be readable without the engine choosing
    between them by hardcoding which shape wins."""
    doc = synthetic(tmp_path, [
        ("natural_relationship", {"graha": ["Rahu", "Ketu"],
                                  "friend": ["Venus"], "neutral": [], "enemy": []}),
    ])
    assert doc.natural_relationship("Rahu", "Venus").value == "friend"
    assert doc.natural_relationship("Ketu", "Venus").value == "friend"


def test_two_cards_claiming_the_same_graha_is_refused(tmp_path):
    """Overlapping coverage is exactly the ambiguity `_one` already refuses;
    a second table naming a graha the first one also names must not silently
    pick either."""
    doc = synthetic(tmp_path, [
        ("natural_relationship", {"table": {"Sun": {"friend": [], "neutral": [], "enemy": []}}}),
        ("natural_relationship", {"graha": ["Sun"], "friend": [], "neutral": [], "enemy": []}),
    ])
    with pytest.raises(DoctrineError, match="cannot choose between authorities"):
        doc.natural_relationship("Sun", "Moon")


# --- unit: compound friendship (dep.compound-friendship) --------------------

def test_temporary_relationship_houses_reads_the_house_lists(tmp_path):
    doc = synthetic(tmp_path, [
        ("temporary_relationship", {"friendly_houses": [2, 3, 4, 10, 11, 12],
                                    "inimical_houses": [1, 5, 6, 7, 8, 9]}),
    ])
    houses, cards = doc.temporary_relationship_houses()
    assert houses == {"friendly": (2, 3, 4, 10, 11, 12), "inimical": (1, 5, 6, 7, 8, 9)}
    assert cards == ("XX.01.Synthetic001",)


def test_temporary_relationship_ignores_a_restating_card_with_no_house_lists(tmp_path):
    """PD.02.Friendship.TemporaryNote restates the verse but carries no
    friendly_houses/inimical_houses of its own; it must not count as a second
    authority `_one` would refuse to choose between -- excluded by shape, not
    by name."""
    doc = synthetic(tmp_path, [
        ("temporary_relationship", {"friendly_houses": [2, 3, 4, 10, 11, 12],
                                    "inimical_houses": [1, 5, 6, 7, 8, 9]}),
        ("temporary_relationship", {"restates": "XX.01.Synthetic001"}),
    ])
    houses, cards = doc.temporary_relationship_houses()
    assert houses["friendly"] == (2, 3, 4, 10, 11, 12)
    assert cards == ("XX.01.Synthetic001",)


def test_temporary_relationship_houses_missing_raises(tmp_path):
    doc = synthetic(tmp_path, [("sign_lord", {"sign": "Aries", "graha": "Mars"})])
    with pytest.raises(DoctrineError, match="has not been encoded"):
        doc.temporary_relationship_houses()


def test_compound_relationship_reads_all_six_printed_rows(tmp_path):
    """Every row of PD.02.Friendship.CompoundTable's own Note, matched
    exactly -- covering the whole finite input space (3 natural values x 2
    temporary values, the only two the house partition ever produces)."""
    doc = synthetic(tmp_path, [
        ("compound_relationship", {"table": [
            {"natural": "friend", "temporary": "friend", "result": "Adhimitra"},
            {"natural": "friend", "temporary": "enemy", "result": "Sama"},
            {"natural": "enemy", "temporary": "enemy", "result": "Adhishatru"},
            {"natural": "enemy", "temporary": "friend", "result": "Sama"},
            {"natural": "neutral", "temporary": "friend", "result": "Mitra"},
            {"natural": "neutral", "temporary": "enemy", "result": "Shatru"},
        ]}),
    ])
    assert doc.compound_relationship("friend", "friend").value == "Adhimitra"
    assert doc.compound_relationship("friend", "enemy").value == "Sama"
    assert doc.compound_relationship("enemy", "enemy").value == "Adhishatru"
    assert doc.compound_relationship("enemy", "friend").value == "Sama"
    assert doc.compound_relationship("neutral", "friend").value == "Mitra"
    assert doc.compound_relationship("neutral", "enemy").value == "Shatru"


def test_compound_relationship_has_no_row_for_a_temporary_neutral(tmp_path):
    """v. 23's own house partition covers all twelve houses between "friendly"
    and "inimical" and leaves no third case, so the printed table never needs
    a temporary-neutral row -- and none is invented for it here."""
    doc = synthetic(tmp_path, [
        ("compound_relationship", {"table": [
            {"natural": "friend", "temporary": "friend", "result": "Adhimitra"},
        ]}),
    ])
    with pytest.raises(DoctrineError, match="does not cover this combination"):
        doc.compound_relationship("friend", "neutral")


def test_compound_relationship_two_tables_is_refused(tmp_path):
    doc = synthetic(tmp_path, [
        ("compound_relationship", {"table": [
            {"natural": "friend", "temporary": "friend", "result": "Adhimitra"}]}),
        ("compound_relationship", {"table": [
            {"natural": "friend", "temporary": "friend", "result": "Mitra"}]}),
    ])
    with pytest.raises(DoctrineError, match="cannot choose between authorities"):
        doc.compound_relationship("friend", "friend")


def test_compound_friendship_extractor_reuses_the_graha_frame_offset(tmp_path, chart):
    """Wiring, not arithmetic: the extractor must not recompute the house
    offset itself, only read it off dep.graha-frame's own `in_house_from`
    facts (the same discipline `_dasa_disposition` already follows for
    dignity/combustion/house-class). Jupiter sits three signs on from Venus in
    this chart -- a temporary friend by the house partition -- and Jupiter is
    made Venus's natural neutral here on purpose, isolated from the real
    book's own table."""
    assert chart.bodies["Jupiter"].sign_index == 11
    assert chart.bodies["Venus"].sign_index == 9
    doc = synthetic(tmp_path, [
        ("temporary_relationship", {"friendly_houses": [2, 3, 4, 10, 11, 12],
                                    "inimical_houses": [1, 5, 6, 7, 8, 9]}),
        ("natural_relationship", {"table": {
            "Jupiter": {"friend": [], "neutral": ["Venus"], "enemy": []},
        }}),
        ("compound_relationship", {"table": [
            {"natural": "neutral", "temporary": "friend", "result": "Mitra"},
        ]}),
    ])
    fs = extract_facts(chart, doc)
    assert "compound_relationship(Jupiter,Venus,Mitra)" in fs
    ev = fs.get("compound_relationship(Jupiter,Venus,Mitra)").evidence
    assert ev["natural_relationship"] == "neutral"
    assert ev["temporary_relationship"] == "friend"
    assert ev["house_from_graha"] == 3
    assert any(cid.startswith("XX.01.") for cid in ev["doctrine"])
    # Venus's own row was never given, so the reverse direction is reported
    # incomplete rather than silently produced or silently dropped.
    assert "vs Jupiter" in fs.doctrine.partial.get("compound_friendship", "")


def test_compound_friendship_never_reports_a_graha_against_itself(tmp_path, chart):
    """dep.graha-frame emits no self-pairs, and this extractor draws its pairs
    from exactly those facts -- a graha cannot be asked whether it is its own
    Adhimitra."""
    doc = synthetic(tmp_path, [
        ("temporary_relationship", {"friendly_houses": [2, 3, 4, 10, 11, 12],
                                    "inimical_houses": [1, 5, 6, 7, 8, 9]}),
        ("natural_relationship", {"table": {
            g: {"friend": [g], "neutral": [], "enemy": []}
            for g in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
        }}),
        ("compound_relationship", {"table": [
            {"natural": "friend", "temporary": "friend", "result": "Adhimitra"},
        ]}),
    ])
    fs = extract_facts(chart, doc)
    assert all(f.args["graha"] != f.args["other"]
               for f in fs.by_predicate("compound_relationship"))


def test_compound_friendship_skipped_without_the_temporary_house_doctrine(tmp_path, chart):
    """No PD.02.Friendship.Temporary-shaped card at all: the extractor's own
    missing doctrine is reported as skipped, the same way `_combustion`
    reports a missing dep.combust source -- not swallowed locally inside the
    extractor."""
    doc = synthetic(tmp_path, [("sign_lord", {"sign": "Aries", "graha": "Mars"})])
    fs = extract_facts(chart, doc)
    assert not fs.by_predicate("compound_relationship")
    assert "has not been encoded" in fs.doctrine.skipped.get("compound_friendship", "")


# --- golden chart -----------------------------------------------------------
#
# 1987-03-14 04:22 Asia/Kolkata, Thanjavur. Capricorn lagna, so the houses run
# Capricorn, Aquarius, Pisces, Aries, Taurus, Gemini, Cancer, Leo, Virgo,
# Libra, Scorpio, Sagittarius. Every expectation below was worked out by hand
# from the tables encoded in chapters 1 and 2.

GOLDEN_LORDS = {1: "Saturn", 2: "Saturn", 3: "Jupiter", 4: "Mars", 5: "Venus",
                6: "Mercury", 7: "Moon", 8: "Sun", 9: "Mercury", 10: "Venus",
                11: "Mars", 12: "Jupiter"}


@pytest.mark.parametrize("house,graha", sorted(GOLDEN_LORDS.items()))
def test_golden_lordship(facts, house, graha):
    assert f"lord_of_house({graha},{house})" in facts


def test_golden_aspects_of_saturn(facts, chart):
    """Saturn in the 11th aspects the 1st, 5th and 8th by full drishti."""
    assert chart.bodies["Saturn"].house == 11
    got = sorted(f.args["target"] for f in facts.by_predicate("aspects")
                 if f.args["graha"] == "Saturn" and isinstance(f.args["target"], int))
    assert got == [1, 5, 8]
    # Venus is in the 1st and the Moon in the 8th, so both are aspected.
    assert "aspects(Saturn,Venus)" in facts
    assert "aspects(Saturn,Moon)" in facts


def test_golden_aspects_of_mars(facts, chart):
    """Mars in the 4th: full at its 4th, 7th and 8th -- houses 7, 10 and 11."""
    got = sorted(f.args["target"] for f in facts.by_predicate("aspects")
                 if f.args["graha"] == "Mars" and isinstance(f.args["target"], int))
    assert got == [7, 10, 11]
    assert "aspects(Mars,Saturn)" in facts


def test_golden_ordinary_graha_aspects_only_the_seventh(facts, chart):
    for graha in ("Sun", "Moon", "Mercury", "Venus"):
        got = [f.args["target"] for f in facts.by_predicate("aspects")
               if f.args["graha"] == graha and isinstance(f.args["target"], int)]
        assert len(got) == 1, f"{graha} should cast one full aspect, got {got}"
        assert got[0] == ((chart.bodies[graha].house - 1 + 6) % 12) + 1


def test_golden_combustion(facts, chart):
    """Jupiter is 9.84 degrees from the Sun, inside its encoded 11 degree orb."""
    assert "combust(Jupiter)" in facts
    ev = facts.get("combust(Jupiter)").evidence
    assert ev["orb"] == 11
    assert ev["separation_from_sun"] == pytest.approx(9.84, abs=0.01)
    combust = {f.args["graha"] for f in facts.by_predicate("combust")}
    assert combust == {"Jupiter"}


def test_golden_dignity(facts):
    """Mars in Aries and Jupiter in Pisces are in their own signs; nothing
    in this chart is exalted or debilitated. The rest are dep.dignity-
    friendship: each graha's own row in the natural-friendship table against
    the lord of the sign it occupies."""
    got = {(f.args["graha"], f.args["dignity"])
           for f in facts.by_predicate("dignity")}
    assert got == {
        ("Mars", "own"), ("Jupiter", "own"),
        ("Sun", "inimical"), ("Saturn", "inimical"), ("Rahu", "inimical"),
        ("Moon", "friend"), ("Venus", "friend"), ("Ketu", "friend"),
        ("Mercury", "neutral"),
    }


def test_golden_friendship_facts_name_the_sign_lord_and_relation(facts, chart):
    """Every friendship-derived dignity fact records what put it there, the
    same provenance an astrologer would ask for: which sign, whose lordship,
    and what the table says the occupant thinks of that lord."""
    ev = facts.get("dignity(Moon,friend)").evidence
    assert ev["sign"] == chart.bodies["Moon"].sign
    assert ev["sign_lord"] == "Sun"
    assert ev["natural_relationship"] == "friend"
    assert any(cid.startswith("PD.02.Friendship") for cid in ev["doctrine"])


def test_golden_ketu_is_read_from_the_rahu_ketu_card(facts):
    """Ketu has no row in the seven-graha table at all -- it can only be
    classified through PD.02.Friendship.RahuKetu."""
    ev = facts.get("dignity(Ketu,friend)").evidence
    assert "PD.02.Friendship.RahuKetu" in ev["doctrine"]
    assert "PD.02.Friendship.NaturalTable" not in ev["doctrine"]


COMPOUND_CATEGORIES = {"Adhimitra", "Mitra", "Sama", "Shatru", "Adhishatru"}


def test_golden_compound_friendship_is_directional(facts, chart):
    """Jupiter classifies Venus its natural enemy while Venus classifies
    Jupiter neutral (an asymmetry PD.02.Friendship.NaturalTable's vv.21-22
    already state outright, not one this extractor introduces); both fall in
    a mutually temporary-friendly house pair here, so both directions resolve
    -- to two different compound tiers, computed independently."""
    assert chart.bodies["Jupiter"].sign == "Pisces"
    assert chart.bodies["Venus"].sign == "Capricorn"
    assert "compound_relationship(Jupiter,Venus,Sama)" in facts
    assert "compound_relationship(Venus,Jupiter,Mitra)" in facts
    fwd = facts.get("compound_relationship(Jupiter,Venus,Sama)").evidence
    rev = facts.get("compound_relationship(Venus,Jupiter,Mitra)").evidence
    assert fwd["natural_relationship"] == "enemy"
    assert rev["natural_relationship"] == "neutral"
    assert fwd["house_from_graha"] != rev["house_from_graha"]


def test_golden_compound_friendship_reports_the_printed_contradiction(facts):
    """The Moon/Mercury printed defect (PD.02.Friendship.NaturalTable: Mercury
    listed under both Friend and Neutral in the Moon's own row) blocks only
    the direction that reads the Moon's row. Mercury's own row is clean, so
    Mercury's classification of the Moon still resolves."""
    assert "compound_relationship(Mercury,Moon,Adhishatru)" in facts
    assert not [f for f in facts.by_predicate("compound_relationship")
               if f.args["graha"] == "Moon" and f.args["other"] == "Mercury"]
    reason = facts.doctrine.partial.get("compound_friendship", "")
    assert "Moon vs Mercury" in reason
    assert "both friend and neutral" in reason


def test_golden_compound_friendship_never_rates_a_node_as_seen_by_a_classical_graha(facts):
    """The seven-graha natural-relationship table (vv. 21-22) never names Rahu
    or Ketu inside any classical graha's own row -- so a classical graha's
    compound relationship *to* a node is not emitted, even though a node's
    own relationship *to* a classical graha is (its own row, v. 35, does cover
    them). Genuine asymmetric source coverage, not an engine guess filling in
    the gap either way."""
    assert not [f for f in facts.by_predicate("compound_relationship")
               if f.args["graha"] == "Mercury" and f.args["other"] in ("Rahu", "Ketu")]
    assert [f for f in facts.by_predicate("compound_relationship")
           if f.args["graha"] == "Rahu" and f.args["other"] == "Mercury"]


def test_golden_compound_friendship_never_invents_a_seventh_category(facts):
    """Anti-invention: only the five printed tiers ever appear as `category`,
    never a numeric score standing in for one."""
    rows = facts.by_predicate("compound_relationship")
    assert rows
    assert {f.args["category"] for f in rows} <= COMPOUND_CATEGORIES
    for f in rows:
        assert isinstance(f.args["category"], str)


def test_golden_compound_friendship_facts_name_their_reference_cards(facts):
    ev = facts.get("compound_relationship(Mercury,Moon,Adhishatru)").evidence
    assert any(cid.startswith("PD.02.Friendship") for cid in ev["doctrine"])


def test_golden_house_classes(facts):
    for house in (1, 4, 7, 10):
        assert f"house_class({house},kendra)" in facts
    for house in (5, 9):
        assert f"house_class({house},trikona)" in facts
    for house in (6, 8, 12):
        assert f"house_class({house},dusthana)" in facts
    # Venus is in the 1st, which is a kendra.
    assert "in_house_class(Venus,kendra)" in facts


def test_golden_graha_classes(facts):
    for graha in ("Mercury", "Ketu", "Saturn"):
        assert f"graha_class({graha},eunuch)" in facts
    for graha in ("Moon", "Rahu", "Venus"):
        assert f"graha_class({graha},female)" in facts
    for graha in ("Sun", "Mars", "Jupiter"):
        assert f"graha_class({graha},male)" in facts


def test_golden_sign_classes(facts):
    # Capricorn is movable, even and southern; the lagna is Capricorn.
    assert "house_sign_class(1,Moveable)" in facts
    assert "house_sign_class(1,Even)" in facts
    # Mars is in Aries, which is movable, fierce and odd.
    assert "in_sign_class(Mars,Moveable)" in facts
    assert "in_sign_class(Mars,Fierce)" in facts
    assert "in_sign_class(Mars,Odd)" in facts


# --- provenance and reporting ------------------------------------------------

def test_every_doctrine_fact_names_its_reference_cards(facts):
    doctrinal = ("lord_of_house", "aspects", "combust", "dignity",
                 "graha_class", "house_class", "in_house_class",
                 "in_sign_class", "house_sign_class")
    checked = 0
    for f in facts:
        if f.predicate in doctrinal:
            assert f.evidence.get("doctrine"), f"{f.key} has no doctrine trail"
            for cid in f.evidence["doctrine"]:
                assert cid.startswith("PD."), cid
            checked += 1
    assert checked > 100


def test_each_extractor_reports_what_it_consulted(facts):
    rep = facts.doctrine
    for name in ("lord_of_house", "sign_class", "house_class", "graha_class",
                 "aspects", "combust", "dignity", "dignity_friendship",
                 "compound_friendship"):
        assert rep.consulted.get(name), f"{name} reported no reference cards"
    assert not rep.skipped, rep.skipped
    assert len(rep.cards) >= 50


def test_consulted_cards_all_exist_and_are_reference_cards(facts):
    by_id = {c.id: c for c in load_cards(RULES)}
    for cid in facts.doctrine.cards:
        assert cid in by_id, cid
        assert by_id[cid].activation == "reference", cid


def test_extractors_are_absent_without_doctrine(chart):
    """Stage 2 without a store still works, and says so rather than guessing."""
    fs = extract_facts(chart)
    assert not fs.by_predicate("lord_of_house")
    assert not fs.by_predicate("aspects")
    assert fs.by_predicate("in_house")        # the chart-only facts survive


# --- discipline --------------------------------------------------------------

GRAHAS = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
          "Rahu", "Ketu"}
SIGNS = {"Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"}


def _docstrings(tree):
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            first = node.body[0] if node.body else None
            if (isinstance(first, ast.Expr)
                    and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                out.add(id(first.value))
    return out


@pytest.mark.parametrize("module", ["doctrine.py", "facts.py"])
def test_no_doctrinal_constant_is_written_in_python(module):
    """The property the whole rule store exists to guarantee.

    A graha or sign name appearing as a *value* in the reasoning layer means a
    table has been smuggled past the store, and a book that disagreed with it
    would become a code change. Docstrings are exempt; running code is not.
    """
    path = ROOT / "Engine" / module
    tree = ast.parse(path.read_text(encoding="utf-8"))
    exempt = _docstrings(tree)
    offenders = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in exempt
                and node.value in (GRAHAS | SIGNS)):
            offenders.append(f"{module}:{node.lineno} {node.value!r}")
    assert not offenders, offenders
