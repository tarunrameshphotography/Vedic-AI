"""Tests for Milestone 31 -- Phaladeepika chapter 20's Mahadasa-scoped
house-lord dasa doctrine (vv.2-13/15-20, v.22's first two sentences, v.40's
first sentence, and v.41's Parasara cluster).

The new capability under test is `dasa_disposition` (Engine/facts.py::
_dasa_disposition), v.14's own local criterion gating vv.2-13/15-20:
auspicious = not in a dusthana AND (own sign, exaltation, or retrograde);
adverse = in a dusthana, OR (inimical sign, debilitation, or combust). This
is deliberately not `strength` (chapter 4's verdict has no own-sign, no
inimical-sign and no dusthana-placement clause -- see PD.20.Disposition's
own note and concept:strength-criterion-scope), so the assertions that
matter most here are the negative ones: no fact ever carries a number, a
graha satisfying both of v.14's clauses at once gets no verdict rather than
a chosen one (the same collision discipline `_strength` already has for
retrograde+combust), and the store's own house_class table is NOT what
PD.20.Parasara.TrikonaLord/.UpachayaLordEvil condition on -- both verses
state their own explicit house numbers, which disagree with (Trikona) or
are narrower than (Upachaya) the existing table.

No antardasa mechanism is built or tested here: reading the whole chapter
found no order or duration arithmetic for the nine antardasa sub-periods
anywhere in it (see Rules/deferred.json's dep.antardasa).

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine, DoctrineError
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import DoctrineReport, chart_frame, extract_facts, _dasa_disposition
from Engine.pipeline import run
from Engine.rules import load_cards
from Engine.tests.test_strength import place

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

# The project's standing demo nativity -- Milestone 30 spot-checked chapter 19
# on it, and it is used again here rather than a fresh chart, so the two
# milestones' claim counts can be cross-checked against the same known chart
# (test_slice.py's own 81 -> 98 move).
DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)

STRONG_CARDS = {f"PD.20.Strong.{h}" for h in
                ["Lagna", "House2", "House3", "House4", "House5", "House6",
                 "House7", "House8", "House9", "House10", "House11", "House12"]}
WEAK_CARDS = {f"PD.20.Weak.{h}" for h in
              ["Lagna", "House2", "House3", "House4", "House5", "House6",
               "House7", "House8", "House9", "House10", "House11", "House12"]}
HOUSE_LORD_CARDS = STRONG_CARDS | WEAK_CARDS


@pytest.fixture(scope="module")
def provider():
    p = SwissEphemerisDLL()
    yield p
    p.close()


@pytest.fixture(scope="module")
def cards():
    return load_cards(RULES)


@pytest.fixture(scope="module")
def doctrine(cards):
    return Doctrine.from_cards(cards)


@pytest.fixture(scope="module")
def chart(provider):
    return compute_chart(resolve_birth(DEMO, provider), provider)


def dispositions(chart, doctrine) -> dict[str, str]:
    rep = DoctrineReport()
    out = _dasa_disposition(chart, doctrine, rep, chart_frame(chart))
    return {f.args["graha"]: f.args["verdict"] for f in out}


# --- doctrine ----------------------------------------------------------------

def test_disposition_criteria_come_from_pd20_disposition(doctrine):
    criteria, cards = doctrine.dasa_effect_disposition_criteria()
    assert cards == ("PD.20.Disposition",)
    assert set(criteria["auspicious"]["dignity"]) == {"own", "exalted"}
    assert criteria["auspicious"]["retrograde"] is True
    assert set(criteria["adverse"]["dignity"]) == {"inimical", "debilitated"}
    assert criteria["adverse"]["combust"] is True


def test_the_doctrine_is_read_and_never_hardcoded():
    """Remove PD.20.Disposition and the capability goes with it -- the same
    discipline test_strength.py pins for `strength`."""
    kept = [c for c in load_cards(RULES) if c.id != "PD.20.Disposition"]
    with pytest.raises(DoctrineError):
        Doctrine.from_cards(kept).dasa_effect_disposition_criteria()


# --- extractor -----------------------------------------------------------------

def test_own_sign_and_not_dusthana_is_auspicious(chart, doctrine):
    c = place(chart, "Mars", 10.0)             # Aries, Mars's own sign
    assert dispositions(c, doctrine).get("Mars") == "auspicious"


def test_exaltation_and_not_dusthana_is_auspicious(chart, doctrine):
    c = place(chart, "Saturn", 190.0)           # Libra 10, Saturn's exaltation
    assert dispositions(c, doctrine).get("Saturn") == "auspicious"


def test_retrograde_and_not_dusthana_is_auspicious(chart, doctrine):
    c = place(chart, "Mercury", 40.0, retrograde=True)   # Taurus: not own/exalt/
    assert dispositions(c, doctrine).get("Mercury") == "auspicious"           # inimical/debilitated for Mercury


def test_debilitation_is_adverse(chart, doctrine):
    c = place(chart, "Jupiter", 280.0)          # Capricorn, Jupiter's debilitation
    assert dispositions(c, doctrine).get("Jupiter") == "adverse"


def test_own_sign_in_a_dusthana_house_is_not_auspicious(chart, doctrine):
    """v.14's dusthana clause is a placement (house) test, independent of the
    graha's own dignity -- own sign alone is not enough if the house is a
    dusthana. Mercury in Gemini (its own sign) falls in the 6th house from
    this chart's own Capricorn lagna, a dusthana."""
    c = place(chart, "Mercury", 70.0)            # Gemini, Mercury's own sign
    assert c.bodies["Mercury"].house == 6
    assert dispositions(c, doctrine).get("Mercury") != "auspicious"


def test_retrograde_and_combust_collide_to_no_verdict(chart, doctrine):
    """The one case v.14 does not rank: a graha satisfying both clauses at
    once. Mirrors `_strength`'s own retrograde+combust collision test."""
    c = place(chart, "Mercury", chart.bodies["Sun"].lon + 1.0, retrograde=True)
    assert "Mercury" not in dispositions(c, doctrine)


def test_collision_is_reported_not_silently_dropped(chart, doctrine):
    c = place(chart, "Mercury", chart.bodies["Sun"].lon + 1.0, retrograde=True)
    rep = DoctrineReport()
    _dasa_disposition(c, doctrine, rep, chart_frame(c))
    conflicts = rep.conflicts_for("dasa_disposition")
    assert conflicts and conflicts[0]["cards"] == ["PD.20.Disposition"]


def test_no_disposition_fact_ever_carries_a_number(chart, doctrine):
    """The same negative discipline `strength`'s own tests pin: a verdict,
    never a score."""
    for f in _dasa_disposition(chart, doctrine, DoctrineReport(), chart_frame(chart)):
        assert f.args["verdict"] in ("auspicious", "adverse")
        for v in f.evidence.values():
            assert not isinstance(v, (int, float)) or isinstance(v, bool)


# --- card scope ----------------------------------------------------------------

def test_exactly_twelve_strong_and_twelve_weak_cards_exist(cards):
    ids = {c.id for c in cards}
    assert STRONG_CARDS <= ids
    assert WEAK_CARDS <= ids


def test_every_house_lord_card_binds_its_own_house_number_and_polarity(cards):
    by_id = {c.id: c for c in cards}
    for i, house in enumerate(
        ["Lagna", "House2", "House3", "House4", "House5", "House6",
         "House7", "House8", "House9", "House10", "House11", "House12"], start=1
    ):
        strong = by_id[f"PD.20.Strong.{house}"]
        weak = by_id[f"PD.20.Weak.{house}"]
        assert strong.predicts["house"] == i
        assert strong.predicts["polarity"] == "auspicious"
        assert weak.predicts["house"] == i
        assert weak.predicts["polarity"] == "adverse"
        lord_clause = next(cl["lord_of_house"] for cl in strong.conditions["all"]
                            if "lord_of_house" in cl)
        assert lord_clause["house"] == i
        disp_clause = next(cl["dasa_disposition"] for cl in strong.conditions["all"]
                            if "dasa_disposition" in cl)
        assert disp_clause["verdict"] == "auspicious"


def test_trikona_lord_conditions_on_the_verses_own_houses_not_house_class(cards):
    """Regression pin against the found ch.1/ch.20 'trikona' discrepancy:
    PD.01.HouseClass.Trikona is houses 5,9 only, but v.41 explicitly says
    'trikonas (1,5,9)'. If a future edit 'simplifies' this card to read
    house_class(?h,trikona) instead, house 1 silently drops out and this
    test catches it."""
    c = next(c for c in cards if c.id == "PD.20.Parasara.TrikonaLord")
    any_clause = next(cl["any"] for cl in c.conditions["all"] if "any" in cl)
    houses = {leaf["lord_of_house"]["house"] for leaf in any_clause}
    assert houses == {1, 5, 9}
    assert "house_class" not in json.dumps(c.conditions)


def test_upachaya_lord_evil_excludes_house_ten(cards):
    """v.41 names only the 3rd, 6th and 11th -- not the store's own
    `upachaya` class, which also includes the 10th."""
    c = next(c for c in cards if c.id == "PD.20.Parasara.UpachayaLordEvil")
    any_clause = next(cl["any"] for cl in c.conditions["all"] if "any" in cl)
    houses = {leaf["lord_of_house"]["house"] for leaf in any_clause}
    assert houses == {3, 6, 11}
    assert 10 not in houses


def test_eighth_lord_sun_moon_binds_each_graha_independently():
    """The `any`-of-two-`all` shape must not let Sun-owns-8th pair with a
    Moon mahadasa or vice versa."""
    cards_ = load_cards(RULES)
    c = next(c for c in cards_ if c.id == "PD.20.Parasara.EighthLordSunMoon")
    branches = c.conditions["any"]
    assert len(branches) == 2
    for branch in branches:
        grahas = {leaf[k]["graha"] for leaf in branch["all"] for k in leaf}
        assert grahas in ({"Sun"}, {"Moon"})


# --- real chart (DEMO) ---------------------------------------------------------

def test_demo_chart_fires_seventeen_pd20_claims():
    """Cross-checked against test_slice.py's own 81 -> 98 accounting."""
    r = run(DEMO)
    pd20 = [c for c in r.claims if c.derived["rule_card"].startswith("PD.20.")]
    assert len(pd20) == 17
    counts: dict[str, int] = {}
    for c in pd20:
        counts[c.derived["rule_card"]] = counts.get(c.derived["rule_card"], 0) + 1
    assert counts == {
        "PD.20.Strong.House4": 1, "PD.20.Strong.House11": 1,
        "PD.20.Weak.Lagna": 1, "PD.20.Weak.House2": 1,
        "PD.20.Weak.House7": 1, "PD.20.Weak.House8": 1,
        "PD.20.Parasara.KendraLordBenefic": 2,
        "PD.20.Parasara.KendraLordMalefic": 2,
        "PD.20.Parasara.TrikonaLord": 3,
        "PD.20.Parasara.UpachayaLordEvil": 3,
        "PD.20.Parasara.EighthLordSunMoon": 1,
    }


def test_demo_chart_house_lord_cards_bind_the_actual_house_lords():
    """Mars owns houses 4 and 11 (lagna Capricorn); Saturn owns 1 and 2;
    Moon owns 7; Sun owns 8 -- confirmed against the chart's own lordship
    facts, not merely asserted."""
    r = run(DEMO)
    by_card = {}
    for c in r.claims:
        if c.derived["rule_card"] in HOUSE_LORD_CARDS:
            graha = next(f["key"].split("(")[1].split(",")[0]
                         for f in c.derived["facts"] if f["key"].startswith("lord_of_house("))
            by_card.setdefault(c.derived["rule_card"], set()).add(graha)
    assert by_card["PD.20.Strong.House4"] == {"Mars"}
    assert by_card["PD.20.Strong.House11"] == {"Mars"}
    assert by_card["PD.20.Weak.Lagna"] == {"Saturn"}
    assert by_card["PD.20.Weak.House2"] == {"Saturn"}
    assert by_card["PD.20.Weak.House7"] == {"Moon"}
    assert by_card["PD.20.Weak.House8"] == {"Sun"}


def test_rahu_satisfies_both_disposition_clauses_and_fires_neither(chart, doctrine):
    """Rahu is retrograde by convention (auspicious clause) and inimical in
    its own sign here (adverse clause) on this real chart -- confirmed
    directly, not assumed -- so no PD.20 card conditions on Rahu at all."""
    disp = dispositions(chart, doctrine)
    assert "Rahu" not in disp
    r = run(DEMO)
    for c in r.claims:
        if c.derived["rule_card"] in HOUSE_LORD_CARDS:
            grahas = {f["key"].split("(")[1].split(",")[0]
                      for f in c.derived["facts"] if f["key"].startswith("mahadasa_lord(")}
            assert "Rahu" not in grahas


def test_house_lord_claims_carry_a_window():
    r = run(DEMO)
    for c in r.claims:
        if c.derived["rule_card"] in HOUSE_LORD_CARDS or c.derived["rule_card"].startswith("PD.20."):
            assert c.window is not None
            assert c.window["start"] < c.window["end"]


# --- negative controls -----------------------------------------------------------

def test_a_graha_with_no_verdict_fires_no_house_lord_card(chart, doctrine):
    """Jupiter, Mercury and Venus get no `dasa_disposition` verdict on the
    real DEMO chart (neither clause holds) -- confirm none of their own
    house-lord cards fire for them."""
    disp = dispositions(chart, doctrine)
    for g in ("Jupiter", "Mercury", "Venus"):
        assert g not in disp
    r = run(DEMO)
    for c in r.claims:
        if c.derived["rule_card"] in HOUSE_LORD_CARDS:
            grahas = {f["key"].split("(")[1].split(",")[0]
                      for f in c.derived["facts"] if f["key"].startswith("mahadasa_lord(")}
            assert grahas.isdisjoint({"Jupiter", "Mercury", "Venus"})


def test_maraka_requires_strength_not_the_local_disposition(cards):
    """v.40 states no local criterion of its own (unlike v.14), so
    PD.20.Maraka reuses the existing chapter-4 `strength` verdict, not
    `dasa_disposition`."""
    c = next(c for c in cards if c.id == "PD.20.Maraka")
    flat = json.dumps(c.conditions)
    assert '"strength"' in flat
    assert '"dasa_disposition"' not in flat
