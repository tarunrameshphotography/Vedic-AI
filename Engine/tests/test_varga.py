"""Tests for dep.varga / dep.vargottama / dep.dignity-in-varga (Milestone 29).

Chapter 3 v.1 defines the Navamsa (9 equal parts of 3 deg 20' each) and
Vargottama (same sign in Rasi and Navamsa); v.4's closing sentence gives four
worked examples of which sign a Navamsa begins from, by mobility. Both the
unit arithmetic (against a synthetic chart, so exact boundaries can be
probed) and one real chart (through the whole pipeline) are exercised here,
per the same two-layer discipline test_overrides.py uses.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import types
from pathlib import Path

import pytest

from Engine.chart import BirthRecord
from Engine.doctrine import Doctrine
from Engine.facts import DoctrineReport, _varga, chart_frame
from Engine.pipeline import run
from Engine.rules import load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

# The real store's own ch. 1 (sign_attributes, exaltation) and ch. 3
# (dasavarga, vargottama_definition, navamsa_start) doctrine -- these tests
# exercise the production reference cards, not a synthetic stand-in.
CARDS = load_cards(RULES)
DOCTRINE = Doctrine.from_cards(CARDS)
FRAME = {"reference": "lagna", "varga": "D1", "house_system": "whole_sign"}

# Hand-verified against the classical triplicity mnemonic (Fire signs ->
# Aries, Earth -> Capricorn, Air -> Libra, Water -> Cancer), independently of
# the mobility-offset arithmetic _varga actually runs, so this table is a
# genuine cross-check and not a restatement of the implementation.
EXPECTED_NAVAMSA_START = {
    "Aries": "Aries", "Taurus": "Capricorn", "Gemini": "Libra",
    "Cancer": "Cancer", "Leo": "Aries", "Virgo": "Capricorn",
    "Libra": "Libra", "Scorpio": "Cancer", "Sagittarius": "Aries",
    "Capricorn": "Capricorn", "Aquarius": "Libra", "Pisces": "Cancer",
}

SIGN_ORDER = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)


def _body(name, sign, deg_in_sign, lon=None):
    idx = SIGN_ORDER.index(sign)
    return types.SimpleNamespace(
        body=name, sign=sign, sign_index=idx, deg_in_sign=deg_in_sign,
        lon=(idx * 30.0 + deg_in_sign) if lon is None else lon,
    )


def _chart(bodies: dict):
    return types.SimpleNamespace(bodies=bodies)


def _facts_for(bodies: dict) -> dict:
    chart = _chart(bodies)
    rep = DoctrineReport()
    facts = _varga(chart, DOCTRINE, rep, FRAME)
    return {f.key: f for f in facts}


# --- Navamsa-start rule, all twelve signs, at the first degree ---------------

@pytest.mark.parametrize("sign", SIGN_ORDER)
def test_navamsa_start_matches_the_classical_table(sign):
    """deg_in_sign=0 is the first Navamsa; its sign must match the mobility
    rule for every sign, not just the four the verse gives directly."""
    facts = _facts_for({"Sun": _body("Sun", sign, 0.0)})
    got = facts[f"in_varga_sign(Sun,D9,{EXPECTED_NAVAMSA_START[sign]})"]
    assert got.args["sign"] == EXPECTED_NAVAMSA_START[sign]


# --- exact boundary arithmetic within one sign -------------------------------

def test_navamsa_index_boundaries_within_aries():
    """Aries is Moveable (offset 0), so its nine Navamsas step directly
    through the zodiac in order: Aries, Taurus, ..., Sagittarius."""
    arc = 30.0 / 9.0  # 3 deg 20'
    expected = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius"]
    for i, want in enumerate(expected):
        # Just inside the segment, and (for i>0) just past its start.
        deg = i * arc + 1e-6
        facts = _facts_for({"Sun": _body("Sun", "Aries", deg)})
        assert facts[f"in_varga_sign(Sun,D9,{want})"].args["sign"] == want


def test_navamsa_index_just_before_a_boundary_is_the_prior_segment():
    arc = 30.0 / 9.0
    just_before = arc - 1e-6           # inside segment 0, not segment 1
    facts = _facts_for({"Sun": _body("Sun", "Aries", just_before)})
    assert facts["in_varga_sign(Sun,D9,Aries)"].args["sign"] == "Aries"


def test_navamsa_index_at_the_last_degree_of_the_sign():
    facts = _facts_for({"Sun": _body("Sun", "Aries", 29.999999)})
    # ninth segment (index 8): Aries + 8 = Sagittarius
    assert facts["in_varga_sign(Sun,D9,Sagittarius)"].args["sign"] == "Sagittarius"


# --- Vargottama: positive, negative, boundary --------------------------------

def test_vargottama_positive_when_navamsa_sign_equals_rasi_sign():
    facts = _facts_for({"Sun": _body("Sun", "Aries", 1.0)})  # navamsa 0 -> Aries
    assert "vargottama(Sun)" in facts


def test_vargottama_negative_when_navamsa_sign_differs():
    facts = _facts_for({"Sun": _body("Sun", "Aries", 5.0)})  # navamsa 1 -> Taurus
    assert "vargottama(Sun)" not in facts


def test_vargottama_boundary_just_either_side_of_a_navamsa_edge():
    arc = 30.0 / 9.0
    just_inside = _facts_for({"Sun": _body("Sun", "Aries", arc - 1e-9)})
    just_outside = _facts_for({"Sun": _body("Sun", "Aries", arc + 1e-9)})
    assert "vargottama(Sun)" in just_inside
    assert "vargottama(Sun)" not in just_outside


def test_vargottama_is_per_graha_with_no_cross_contamination():
    """One graha's Vargottama status must not leak onto another's."""
    facts = _facts_for({
        "Sun": _body("Sun", "Aries", 1.0),      # vargottama
        "Moon": _body("Moon", "Aries", 5.0),    # not (navamsa 1 -> Taurus)
    })
    assert "vargottama(Sun)" in facts
    assert "vargottama(Moon)" not in facts


def test_vargottama_across_all_twelve_rasi_signs():
    """Placing a graha at 1 degree (navamsa 0, offset applies) of every sign
    and checking against the same classical table used above -- Vargottama
    holds exactly when the sign is its own Navamsa-1 start."""
    for sign in SIGN_ORDER:
        facts = _facts_for({"Sun": _body("Sun", sign, 1.0)})
        is_vargottama = "vargottama(Sun)" in facts
        assert is_vargottama == (EXPECTED_NAVAMSA_START[sign] == sign), sign


def test_varga_facts_are_deterministic():
    body = _body("Mars", "Scorpio", 17.234)
    a = _facts_for({"Mars": body})
    b = _facts_for({"Mars": body})
    assert {k: v.args for k, v in a.items()} == {k: v.args for k, v in b.items()}


# --- dep.dignity-in-varga: debilitated in Navamsa ----------------------------

def test_dignity_in_varga_debilitated_when_navamsa_sign_is_the_debilitation_sign():
    # Sun debilitates in Libra (PD.01.Exaltation.Sun). Aries is Moveable
    # (offset 0), so its Navamsa segments run Aries, Taurus, ..., Sagittarius
    # in order; segment 6 (21-23.33 degrees) lands on Libra. Aries is Sun's
    # own *exaltation* sign in Rasi, isolating the Navamsa alternative: this
    # placement is debilitated in Navamsa while dignified, not debilitated,
    # in Rasi -- the two alternatives the verse states are independent.
    facts = _facts_for({"Sun": _body("Sun", "Aries", 21.0)})
    assert facts["in_varga_sign(Sun,D9,Libra)"].args["sign"] == "Libra"
    assert "dignity_in_varga(Sun,D9,debilitated)" in facts


def test_dignity_in_varga_absent_when_navamsa_sign_is_not_the_debilitation_sign():
    # Sun at 1 degree of Aries: Navamsa 0 -> Aries (Sun's own exaltation
    # sign, not Libra), so no debilitated-in-Navamsa fact should appear.
    facts = _facts_for({"Sun": _body("Sun", "Aries", 1.0)})
    assert not any(k.startswith("dignity_in_varga(Sun") for k in facts)


# --- golden: the real card, through the whole pipeline -----------------------

NAVAMSA_DEBILITATION_DEMO = BirthRecord(
    date="1990-06-15", time="06:00", timezone="Asia/Kolkata",
    latitude=13.0827, longitude=80.2707, place_name="Chennai",
    time_precision="minute", time_source="certificate",
)


@pytest.fixture(scope="module")
def golden():
    return run(NAVAMSA_DEBILITATION_DEMO)


def test_golden_in_varga_sign_is_present_for_every_graha(golden):
    for name in golden.chart.bodies:
        assert any(
            f.predicate == "in_varga_sign" and f.args["graha"] == name
            for f in golden.facts
        ), name


def test_golden_still_verifies(golden):
    assert golden.verification.ok


# A real instant, found by an ephemeris sweep (below), where Saturn is
# debilitated in Navamsa specifically and not in Rasi, in a house that is not
# 6th/8th/12th, uncombust and in a friendly sign -- so PD.02.AdverseDisposition
# fires for Saturn on this chart *solely* via the leaf this milestone added,
# not incidentally alongside one of the other six.
SOLO_NAVAMSA_DEBILITATION_DEMO = BirthRecord(
    date="1975-01-01", time="12:00", timezone="Asia/Kolkata",
    latitude=13.0827, longitude=80.2707, place_name="Chennai",
    time_precision="minute", time_source="certificate",
)


def test_golden_new_leaf_fires_a_real_claim_on_its_own():
    r = run(SOLO_NAVAMSA_DEBILITATION_DEMO)
    assert "dignity_in_varga(Saturn,D9,debilitated)" in r.facts
    adv = [c for c in r.claims if c.derived["rule_card"] == "PD.02.AdverseDisposition"
           and c.derived["variables"]["?g"] == "Saturn"]
    assert len(adv) == 1
    assert adv[0].derived["conditions_satisfied"] == ["dignity_in_varga(Saturn,D9,debilitated)"]
    assert r.verification.ok


# --- real-chart sweep, per master-prompt step 17 -----------------------------

def test_sweep_finds_both_polarities_of_both_new_facts():
    """A direct ephemeris sweep (sign occupancy depends only on longitude, the
    same reasoning Milestone 27's sweep used) over 2,609 weekly instants,
    1975-2025 -- not birth records, so no timezone/DST cost -- confirms both
    dep.vargottama and dep.dignity-in-varga occur naturally, in both
    directions, rather than only in hand-built fixtures."""
    import datetime as dt

    from Engine.ephemeris import SwissEphemerisDLL
    from Engine.chart import SIGNS as _SIGNS

    provider = SwissEphemerisDLL()
    try:
        n = vargottama_hits = debil_hits = 0
        no_vargottama = no_debil = False
        start = dt.date(1975, 1, 1)
        for i in range(0, 18262, 7):
            d = start + dt.timedelta(days=i)
            jd = provider.julian_day_ut(d.year, d.month, d.day, 12.0)
            bodies = {}
            for name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                         "Saturn", "Rahu", "Ketu"):
                bp = provider.body_position(jd, name, "lahiri")
                idx = int(bp.lon // 30.0) % 12
                bodies[name] = _body(name, _SIGNS[idx], bp.lon - idx * 30.0, bp.lon)
            rep = DoctrineReport()
            facts = _varga(types.SimpleNamespace(bodies=bodies), DOCTRINE, rep, FRAME)
            n += 1
            if any(f.predicate == "vargottama" for f in facts):
                vargottama_hits += 1
            else:
                no_vargottama = True
            if any(f.predicate == "dignity_in_varga" for f in facts):
                debil_hits += 1
            else:
                no_debil = True
    finally:
        provider.close()

    assert n == 2609
    assert 0 < vargottama_hits < n and no_vargottama          # both polarities
    assert 0 < debil_hits < n and no_debil                     # both polarities
