"""Tests for Milestone 38 -- Phaladeepika chapter 5, vv.2-9 (ten firing cards).

Verses 2-8 are one repeating family: whichever classical graha the 10th
house's lord (`?g`) occupies the Navamsa (D9) of names the source of
livelihood. Verse 9's first two sentences gate the amount of wealth on that
same Navamsa-lord's own strength; its fourth and fifth sentences (one card,
two branches) give two independent ways the 10th house indicates the
native's own country. All ten reuse existing predicates exactly as declared
-- lord_of_house, in_varga_sign (dep.varga, D9 only), strength, in_house and
aspects -- zero new engine capability.

The per-graha Navamsa sign-lord table (vv.2-8's own condition) and the
Fixed-sign subset PD.05.Livelihood.Country.OwnLand's second branch needs are
both embedded at authoring time from this store's own PD.01.SignLord.*/
PD.01.SignAttributes.* reference cards (ch.1 vv.6-7) -- the drift-guard tests
below cross-check both tables against those cards directly, the same
discipline Milestone 36 established for PD.07.Neechabhanga.*'s own per-graha
table, so a future change to chapter 1's own cards cannot silently strand
this chapter's hardcoded conditions.

The chart used throughout is the project's own real Thanjavur nativity
(Capricorn Lagna -- test_chapter_seven_slice_two.py's own `base_chart`),
where the 10th house is Libra and its lord is Venus. Every test moves Venus
(and, for the strength cards, Mars) to a specific D9/D1 placement with
`Engine.tests.test_strength.place`, which recomputes the moved body's own
`.house` field against the chart's real, unmoved ascendant -- safe here
since no test changes the Lagna itself.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.chart import BirthRecord, SIGNS, compute_chart, resolve_birth
from Engine.doctrine import Doctrine
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import extract_facts
from Engine.rules import evaluate, load_cards
from Engine.tests.test_strength import place

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)

ARC = 30.0 / 9.0  # one Navamsa segment, 3 deg 20'


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
def base_chart(provider):
    # Real ascendant: Capricorn (the same chart test_chapter_seven_slice_two.py
    # uses). The 10th house from Capricorn is Libra, so Venus is the 10th
    # lord on every test below that does not itself move Venus off Libra.
    return compute_chart(resolve_birth(DEMO, provider), provider)


def lon_for(carrier: str, k: int) -> float:
    """Absolute sidereal longitude landing a body's D9 sign on a chosen
    target, via a chosen carrier D1 sign and Navamsa segment `k` (0-8).

    Cross-checked against Engine/tests/test_varga.py's own
    EXPECTED_NAVAMSA_START table: `carrier="Aries"` (Moveable, offset 0)
    gives D9 index == k directly for k in 0..8 (Aries..Sagittarius);
    `carrier="Taurus"` (Fixed, offset 8) gives D9 index == (9+k) % 12,
    reaching the three signs Aries's own family cannot (Capricorn,
    Aquarius, Pisces) plus, at k=4, Taurus itself.
    """
    return SIGNS.index(carrier) * 30.0 + k * ARC + 1.0


def d9_of(chart, doctrine, graha: str) -> str:
    facts = extract_facts(chart, doctrine)
    (f,) = [f for f in facts if f.predicate == "in_varga_sign" and f.args["graha"] == graha]
    return f.args["sign"]


def fires(chart, doctrine, cards_, card_id: str) -> bool:
    card = next(c for c in cards_ if c.id == card_id)
    facts = extract_facts(chart, doctrine)
    return evaluate(card.conditions, facts).satisfied


# --- source fidelity ----------------------------------------------------

CARD_IDS = [
    "PD.05.Livelihood.SunNavamsa",
    "PD.05.Livelihood.MoonNavamsa",
    "PD.05.Livelihood.MarsNavamsa",
    "PD.05.Livelihood.MercuryNavamsa",
    "PD.05.Livelihood.JupiterNavamsa",
    "PD.05.Livelihood.VenusNavamsa",
    "PD.05.Livelihood.SaturnNavamsa",
    "PD.05.Livelihood.NavamsaLordStrong",
    "PD.05.Livelihood.NavamsaLordWeak",
    "PD.05.Livelihood.Country.OwnLand",
]


def test_all_ten_cards_are_present_and_cite_their_verses(cards):
    by_id = {c.id: c for c in cards if c.id in CARD_IDS}
    assert len(by_id) == 10
    expected_verse = {
        "PD.05.Livelihood.SunNavamsa": "2", "PD.05.Livelihood.MoonNavamsa": "3",
        "PD.05.Livelihood.MarsNavamsa": "4", "PD.05.Livelihood.MercuryNavamsa": "5",
        "PD.05.Livelihood.JupiterNavamsa": "6", "PD.05.Livelihood.VenusNavamsa": "7",
        "PD.05.Livelihood.SaturnNavamsa": "8", "PD.05.Livelihood.NavamsaLordStrong": "9",
        "PD.05.Livelihood.NavamsaLordWeak": "9", "PD.05.Livelihood.Country.OwnLand": "9",
    }
    for cid, verse in expected_verse.items():
        assert by_id[cid].verse == verse, cid


def test_ten_cards_carry_zero_new_predicates(cards):
    """Every leaf predicate across all ten cards must already be one this
    store used before chapter 5 -- the milestone's own zero-new-capability
    claim, checked mechanically rather than only asserted in prose."""
    from Engine.rules import _predicates_used
    by_id = {c.id: c for c in cards if c.id in CARD_IDS}
    used = set()
    for c in by_id.values():
        used |= _predicates_used(c.conditions)
    assert used == {"lord_of_house", "in_varga_sign", "strength", "in_house", "aspects"}


# --- drift guard: the per-graha Navamsa sign-lord table vv.2-8 embed -------

NAVAMSA_CARD_BY_GRAHA = {
    "Sun": "PD.05.Livelihood.SunNavamsa", "Moon": "PD.05.Livelihood.MoonNavamsa",
    "Mars": "PD.05.Livelihood.MarsNavamsa", "Mercury": "PD.05.Livelihood.MercuryNavamsa",
    "Jupiter": "PD.05.Livelihood.JupiterNavamsa", "Venus": "PD.05.Livelihood.VenusNavamsa",
    "Saturn": "PD.05.Livelihood.SaturnNavamsa",
}


def _signs_in_condition(node) -> set[str]:
    found = set()
    if isinstance(node, dict):
        if "in_varga_sign" in node:
            found.add(node["in_varga_sign"]["sign"])
        for k in ("all", "any"):
            for child in node.get(k, ()):
                found |= _signs_in_condition(child)
    return found


@pytest.mark.parametrize("graha", sorted(NAVAMSA_CARD_BY_GRAHA))
def test_navamsa_sign_table_matches_pd01_signlord(graha, cards, doctrine):
    """The signs each PD.05.Livelihood.*Navamsa card's condition hardcodes
    must be exactly the signs PD.01.SignLord.* (ch.1 v.6) gives `graha` as
    lord of -- guards against the two tables silently drifting apart."""
    card = next(c for c in cards if c.id == NAVAMSA_CARD_BY_GRAHA[graha])
    embedded = _signs_in_condition(card.conditions)
    assert embedded == set(doctrine.signs_ruled_by(graha).value)


def test_fixed_navamsa_signs_in_country_ownland_match_pd01_signattributes(cards, doctrine):
    """PD.05.Livelihood.Country.OwnLand's own second branch hardcodes the
    Fixed-mobility subset of the seven Navamsa-owner sign pairs. Recomputed
    here from PD.01.SignAttributes.* directly (ch.1 v.7) rather than trusted,
    the same drift guard as the sign-lord table above."""
    card = next(c for c in cards if c.id == "PD.05.Livelihood.Country.OwnLand")
    embedded = _signs_in_condition(card.conditions)
    all_navamsa_signs = {s for g in NAVAMSA_CARD_BY_GRAHA
                          for s in doctrine.signs_ruled_by(g).value}
    expected_fixed = {s for s in all_navamsa_signs
                       if doctrine.sign_attributes(s).value["mobility"] == "Fixed"}
    # embedded also carries no `in_varga_sign` sign outside that Fixed subset
    assert embedded == expected_fixed


# --- vv.2-8: the seven-way Navamsa-lord family, mutually exclusive --------

# (graha, target D9 sign, (carrier, k) for that sign)
NAV_PLACEMENT = {
    "Sun": ("Leo", "Aries", 4),
    "Moon": ("Cancer", "Aries", 3),
    "Mars": ("Aries", "Aries", 0),
    "Mercury": ("Gemini", "Aries", 2),
    "Jupiter": ("Sagittarius", "Aries", 8),
    "Venus": ("Taurus", "Aries", 1),
    "Saturn": ("Capricorn", "Taurus", 0),
}

# The second sign each two-sign-owning graha also rules.
NAV_SECOND_PLACEMENT = {
    "Mars": ("Scorpio", "Aries", 7),
    "Mercury": ("Virgo", "Aries", 5),
    "Jupiter": ("Pisces", "Taurus", 2),
    "Venus": ("Libra", "Aries", 6),
    "Saturn": ("Aquarius", "Taurus", 1),
}


@pytest.mark.parametrize("graha", sorted(NAV_PLACEMENT))
def test_navamsa_lord_card_fires_only_for_its_own_graha(graha, base_chart, doctrine, cards):
    target_sign, carrier, k = NAV_PLACEMENT[graha]
    c = place(base_chart, "Venus", lon_for(carrier, k))
    assert d9_of(c, doctrine, "Venus") == target_sign
    own_card = NAVAMSA_CARD_BY_GRAHA[graha]
    assert fires(c, doctrine, cards, own_card)
    for other_graha, other_card in NAVAMSA_CARD_BY_GRAHA.items():
        if other_graha == graha:
            continue
        assert not fires(c, doctrine, cards, other_card), (
            f"{other_card} fired alongside {own_card} on the same chart")


@pytest.mark.parametrize("graha", sorted(NAV_SECOND_PLACEMENT))
def test_navamsa_lord_card_also_fires_on_the_graha_s_second_ruled_sign(
        graha, base_chart, doctrine, cards):
    target_sign, carrier, k = NAV_SECOND_PLACEMENT[graha]
    c = place(base_chart, "Venus", lon_for(carrier, k))
    assert d9_of(c, doctrine, "Venus") == target_sign
    assert fires(c, doctrine, cards, NAVAMSA_CARD_BY_GRAHA[graha])


# --- v.9 sentences 1-2: PD.05.Livelihood.NavamsaLordStrong/.NavamsaLordWeak

def test_navamsa_lord_strong_fires_when_the_navamsa_owner_is_exalted(base_chart, doctrine, cards):
    # Venus's D9 in Aries (Mars's own sign) makes Mars the Navamsa-lord;
    # Mars exalts in Capricorn (PD.01.Exaltation.Mars).
    c = place(base_chart, "Venus", lon_for("Aries", 0))
    c = place(c, "Mars", lon_for("Capricorn", 0) - 0.5, retrograde=False)
    assert fires(c, doctrine, cards, "PD.05.Livelihood.NavamsaLordStrong")
    assert not fires(c, doctrine, cards, "PD.05.Livelihood.NavamsaLordWeak")


def test_navamsa_lord_weak_fires_when_the_navamsa_owner_is_combust(base_chart, doctrine, cards):
    c = place(base_chart, "Venus", lon_for("Aries", 0))
    sun_lon = SIGNS.index("Gemini") * 30.0 + 10.0
    c = place(c, "Sun", sun_lon)
    c = place(c, "Mars", sun_lon + 0.3, retrograde=False)  # well within any combustion orb
    assert fires(c, doctrine, cards, "PD.05.Livelihood.NavamsaLordWeak")
    assert not fires(c, doctrine, cards, "PD.05.Livelihood.NavamsaLordStrong")


def test_navamsa_lord_strength_cards_do_not_fire_when_the_owner_has_no_verdict(
        base_chart, doctrine, cards):
    """Mars neither exalted, retrograde, nor combust -- `strength` (Milestone
    22's own documented behaviour) emits no fact at all, so neither card
    should fire, mirroring dep.strength's own no-forced-choice discipline."""
    c = place(base_chart, "Venus", lon_for("Aries", 0))
    c = place(c, "Mars", SIGNS.index("Gemini") * 30.0 + 10.0, retrograde=False)
    assert not fires(c, doctrine, cards, "PD.05.Livelihood.NavamsaLordStrong")
    assert not fires(c, doctrine, cards, "PD.05.Livelihood.NavamsaLordWeak")


# --- v.9 sentences 4-5: PD.05.Livelihood.Country.OwnLand -------------------

def test_country_ownland_fires_when_tenth_lord_occupies_the_tenth(base_chart, doctrine, cards):
    c = place(base_chart, "Venus", SIGNS.index("Libra") * 30.0 + 15.0)
    assert c.bodies["Venus"].house == 10
    assert fires(c, doctrine, cards, "PD.05.Livelihood.Country.OwnLand")


def test_country_ownland_fires_when_tenth_lord_aspects_the_tenth_from_the_fourth(
        base_chart, doctrine, cards):
    # House 4's own universal 7th-house aspect reaches house 10; D9 (Cancer)
    # is deliberately not one of the Fixed signs, isolating this branch.
    c = place(base_chart, "Venus", lon_for("Aries", 3))
    assert c.bodies["Venus"].house == 4
    assert d9_of(c, doctrine, "Venus") == "Cancer"
    assert fires(c, doctrine, cards, "PD.05.Livelihood.Country.OwnLand")


def test_country_ownland_fires_when_the_navamsa_is_a_fixed_sign(base_chart, doctrine, cards):
    # Carrier Taurus, k=4 lands D9 back on Taurus itself (Fixed); D1 house 5
    # neither occupies house 10 nor aspects it (house 5 aspects house 11).
    c = place(base_chart, "Venus", lon_for("Taurus", 4))
    assert c.bodies["Venus"].house == 5
    assert d9_of(c, doctrine, "Venus") == "Taurus"
    assert fires(c, doctrine, cards, "PD.05.Livelihood.Country.OwnLand")


def test_country_ownland_does_not_fire_otherwise(base_chart, doctrine, cards):
    # Venus in Cancer (D1 house 7, aspects house 1, not house 10) with its
    # own D9 also Cancer -- neither occupied/aspected-tenth nor Fixed-Navamsa.
    c = place(base_chart, "Venus", lon_for("Cancer", 0))
    assert c.bodies["Venus"].house == 7
    assert d9_of(c, doctrine, "Venus") == "Cancer"
    assert not fires(c, doctrine, cards, "PD.05.Livelihood.Country.OwnLand")


# --- golden: the real chart, whole pipeline, verified end to end ----------

def test_golden_pipeline_verifies_on_the_real_chart(provider):
    from Engine.pipeline import run
    r = run(DEMO)
    assert r.verification.ok
