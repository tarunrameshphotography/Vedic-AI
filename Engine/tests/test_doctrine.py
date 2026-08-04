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


def test_no_friendship_fact_is_emitted_at_all(facts):
    """The natural friendship table did not survive the scan."""
    got = {f.args["dignity"] for f in facts.by_predicate("dignity")}
    assert not got & {"friend", "neutral", "inimical", "enemy"}


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
    in this chart is exalted or debilitated."""
    got = {(f.args["graha"], f.args["dignity"])
           for f in facts.by_predicate("dignity")}
    assert got == {("Mars", "own"), ("Jupiter", "own")}


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
                 "aspects", "combust", "dignity"):
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
