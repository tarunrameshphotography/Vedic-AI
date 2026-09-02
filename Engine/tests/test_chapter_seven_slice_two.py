"""Tests for Milestone 37 -- Phaladeepika chapter 7 slice 2 (vv.13, 18, 20
items (b)-(d), 24, 25; ten firing cards). All ten reuse existing predicates
(vargottama, strength, aspects, nature, in_house, in_house_class,
in_house_from, lord_of_house, dignity, lagna_sign) exactly as-is -- zero new
engine capability.

The chart used throughout is the same real Thanjavur nativity
test_chapter_seven_neechabhanga.py uses (Engine.tests.test_strength.place for
single-body moves). Unlike that file, several cards here need a genuinely
different Lagna, and Milestone 36's own `lagna()` test helper only replaces
`ascendant_sign`/`ascendant_sign_index` -- it leaves every body's own `.house`
field and `chart.houses["signs"]` stale, which `in_house`/`in_house_class`/
`aspects`/`lord_of_house` all read directly. This file's own `lagna()` below
recomputes both consistently instead, and every test that changes the Lagna
uses it. Tests that keep the birth chart's own real Capricorn Lagna use
`base_chart` untouched and only `place()` individual bodies, which is safe
on its own (place() recomputes its one moved body's house against whichever
ascendant is already current).

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import dataclasses
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
    # Real ascendant: Capricorn. Confirmed by direct ephemeris read (no graha
    # is naturally debilitated here), which the "no debilitated graha"/"no
    # malefic in the Lagna" tests below rely on for every body they do not
    # explicitly move.
    return compute_chart(resolve_birth(DEMO, provider), provider)


def lagna(chart, sign: str):
    """A consistent Lagna change: ascendant, `houses["signs"]`, and every
    body's own `.house` are all recomputed together, unlike the shallow
    helper of the same name in test_chapter_seven_neechabhanga.py (safe only
    because every test there re-places every body its conditions reference)."""
    idx = SIGNS.index(sign)
    bodies = {name: dataclasses.replace(b, house=((b.sign_index - idx) % 12) + 1)
              for name, b in chart.bodies.items()}
    return dataclasses.replace(
        chart, ascendant_sign=sign, ascendant_sign_index=idx,
        houses={**chart.houses, "signs": [SIGNS[(idx + i) % 12] for i in range(12)]},
        bodies=bodies,
    )


def sign_mid(sign: str) -> float:
    return SIGNS.index(sign) * 30.0 + 15.0


def deg(sign: str, d: float) -> float:
    return SIGNS.index(sign) * 30.0 + d


def fires(chart, doctrine, cards_, card_id: str) -> bool:
    card = next(c for c in cards_ if c.id == card_id)
    facts = extract_facts(chart, doctrine)
    return evaluate(card.conditions, facts).satisfied


# --- source fidelity --------------------------------------------------------

CARD_IDS = [
    "PD.07.Emperor.VargottamaMoonAspectedNoMalefic",
    "PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation",
    "PD.07.King.JupiterLagnaNotCapricorn",
    "PD.07.King.StrongLagnaLordKendra",
    "PD.07.King.StrongMercuryKendraAspectedJupiter",
    "PD.07.RajaYoga.MaleficsThirdSixthEleventh",
    "PD.07.RajaYoga.MarsMercurySecond",
    "PD.07.RajaYoga.SunVenusFourth",
    "PD.07.RajaYoga.MarsSaturnJupiterTenthEleventhLagna",
    "PD.07.RajaYoga.HouseLordKendraFromMoonJupiterOwnership",
]


def test_all_ten_cards_are_present_and_cite_their_verses(cards):
    by_id = {c.id: c for c in cards if c.id in CARD_IDS}
    assert len(by_id) == 10
    assert by_id["PD.07.Emperor.VargottamaMoonAspectedNoMalefic"].verse == "13"
    assert by_id["PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation"].verse == "18"
    for cid in CARD_IDS[2:5]:
        assert by_id[cid].verse == "20"
    for cid in CARD_IDS[5:9]:
        assert by_id[cid].verse == "24"
    assert by_id["PD.07.RajaYoga.HouseLordKendraFromMoonJupiterOwnership"].verse == "25"


# --- v.13: PD.07.Emperor.VargottamaMoonAspectedNoMalefic -------------------

def test_vargottama_moon_aspected_by_exalted_saturn_no_malefic_in_lagna(base_chart, doctrine, cards):
    """Capricorn Lagna (the real, unmoved ascendant): Moon placed in Aries
    (a movable sign; its own Navamsa-1 starts in Aries, so 1 degree in gives
    Vargottama) in the 4th house; Saturn exalted in Libra, the 10th house --
    strong by exaltation, and its universal 7th-house aspect from the 10th
    reaches the 4th. Venus (benefic) is the only body natally in the Lagna
    (Capricorn), so 'no malefic in the Lagna' already holds without moving
    anything else."""
    c = place(base_chart, "Moon", deg("Aries", 1.0))
    c = place(c, "Saturn", sign_mid("Libra"))
    assert fires(c, doctrine, cards, "PD.07.Emperor.VargottamaMoonAspectedNoMalefic")


def test_malefic_in_the_lagna_blocks_the_yoga(base_chart, doctrine, cards):
    c = place(base_chart, "Moon", deg("Aries", 1.0))
    c = place(c, "Saturn", sign_mid("Libra"))
    c = place(c, "Mars", sign_mid("Capricorn"))  # malefic, now in the Lagna
    assert not fires(c, doctrine, cards, "PD.07.Emperor.VargottamaMoonAspectedNoMalefic")


def test_non_vargottama_moon_does_not_fire(base_chart, doctrine, cards):
    c = place(base_chart, "Moon", deg("Aries", 20.0))  # navamsa 6 -> Libra, not Aries
    c = place(c, "Saturn", sign_mid("Libra"))
    assert not fires(c, doctrine, cards, "PD.07.Emperor.VargottamaMoonAspectedNoMalefic")


# --- v.18: PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation ---------

def test_jupiter_and_moon_kendra_both_aspected_by_venus_no_debilitation(base_chart, doctrine, cards):
    """Jupiter and the Moon both placed in Aries (4th house from the real
    Capricorn Lagna, a kendra); Venus in Libra (10th), whose universal
    7th-house aspect reaches the 4th and so lands on both co-occupants at
    once. Nothing in this chart is debilitated (Jupiter in Aries and Venus in
    its own sign, Libra, are both undebilitated; every other body keeps its
    real, undebilitated natal placement)."""
    c = place(base_chart, "Jupiter", sign_mid("Aries"))
    c = place(c, "Moon", sign_mid("Aries"))
    c = place(c, "Venus", sign_mid("Libra"))
    assert fires(c, doctrine, cards, "PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation")


def test_a_debilitated_graha_anywhere_blocks_the_yoga(base_chart, doctrine, cards):
    c = place(base_chart, "Jupiter", sign_mid("Aries"))
    c = place(c, "Moon", sign_mid("Aries"))
    c = place(c, "Venus", sign_mid("Libra"))
    c = place(c, "Mercury", sign_mid("Pisces"))  # Mercury's own debilitation sign
    assert not fires(c, doctrine, cards, "PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation")


def test_jupiter_out_of_kendra_does_not_fire(base_chart, doctrine, cards):
    c = place(base_chart, "Jupiter", sign_mid("Taurus"))  # 5th -- not kendra
    c = place(c, "Moon", sign_mid("Aries"))
    c = place(c, "Venus", sign_mid("Libra"))
    assert not fires(c, doctrine, cards, "PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation")


# --- v.20(b): PD.07.King.JupiterLagnaNotCapricorn --------------------------

def test_jupiter_in_a_non_capricorn_lagna_fires(base_chart, doctrine, cards):
    c = lagna(base_chart, "Aries")
    c = place(c, "Jupiter", sign_mid("Aries"))
    assert fires(c, doctrine, cards, "PD.07.King.JupiterLagnaNotCapricorn")


def test_jupiter_in_a_capricorn_lagna_does_not_fire(base_chart, doctrine, cards):
    """Capricorn is the chart's own real Lagna -- Jupiter placed there is
    also Jupiter's own sign of debilitation, exactly why v.20 excludes it."""
    c = place(base_chart, "Jupiter", sign_mid("Capricorn"))
    assert not fires(c, doctrine, cards, "PD.07.King.JupiterLagnaNotCapricorn")


# --- v.20(c): PD.07.King.StrongLagnaLordKendra -----------------------------

def test_strong_lagna_lord_in_kendra_fires(base_chart, doctrine, cards):
    """Capricorn's own lord is Saturn; placed in Libra it is both exalted
    (strong) and in the 10th house from the real Capricorn Lagna (a kendra)
    -- one placement satisfies all three clauses at once."""
    c = place(base_chart, "Saturn", sign_mid("Libra"))
    assert fires(c, doctrine, cards, "PD.07.King.StrongLagnaLordKendra")


def test_lagna_lord_neither_strong_nor_in_kendra_does_not_fire(base_chart, doctrine, cards):
    c = place(base_chart, "Saturn", sign_mid("Gemini"))  # 6th -- not kendra, not exalted
    assert not fires(c, doctrine, cards, "PD.07.King.StrongLagnaLordKendra")


# --- v.20(d): PD.07.King.StrongMercuryKendraAspectedJupiter ----------------

def test_strong_mercury_in_kendra_aspected_by_jupiter_fires(base_chart, doctrine, cards):
    """Sagittarius Lagna puts Virgo (Mercury's own exaltation sign) in the
    10th house; Jupiter in Pisces (its own sign, the 4th) reaches the 10th
    with its universal 7th-house aspect."""
    c = lagna(base_chart, "Sagittarius")
    c = place(c, "Mercury", sign_mid("Virgo"))
    c = place(c, "Jupiter", sign_mid("Pisces"))
    assert fires(c, doctrine, cards, "PD.07.King.StrongMercuryKendraAspectedJupiter")


def test_mercury_strong_and_kendra_but_not_aspected_does_not_fire(base_chart, doctrine, cards):
    c = lagna(base_chart, "Sagittarius")
    c = place(c, "Mercury", sign_mid("Virgo"))
    c = place(c, "Jupiter", sign_mid("Aries"))  # 5th -- does not reach the 10th
    assert not fires(c, doctrine, cards, "PD.07.King.StrongMercuryKendraAspectedJupiter")


# --- v.24 item (1): PD.07.RajaYoga.MaleficsThirdSixthEleventh --------------

def test_malefics_in_third_sixth_eleventh_from_the_lagna_fires(base_chart, doctrine, cards):
    """Branch (c) of the card's own `any` -- counted from the Lagna itself
    (Capricorn): Sun in Pisces (3rd), Mars in Gemini (6th), Saturn in
    Scorpio (11th)."""
    c = place(base_chart, "Sun", sign_mid("Pisces"))
    c = place(c, "Mars", sign_mid("Gemini"))
    c = place(c, "Saturn", sign_mid("Scorpio"))
    assert fires(c, doctrine, cards, "PD.07.RajaYoga.MaleficsThirdSixthEleventh")


def test_only_two_of_the_three_houses_occupied_does_not_fire(base_chart, doctrine, cards):
    """Sun alone in the 3rd (Pisces); Mars and Saturn moved well away from
    every reference point's 3rd/6th/11th (Lagna, Moon, or the Lagna-lord
    Saturn's own -- now relocated -- house), so no branch of the `any`
    completes its three-house requirement."""
    c = place(base_chart, "Sun", sign_mid("Pisces"))     # 3rd from the Lagna
    c = place(c, "Mars", sign_mid("Aquarius"))           # 2nd -- no branch wants this
    c = place(c, "Saturn", sign_mid("Taurus"))           # 5th -- no branch wants this
    assert not fires(c, doctrine, cards, "PD.07.RajaYoga.MaleficsThirdSixthEleventh")


# --- v.24 item (2): PD.07.RajaYoga.MarsMercurySecond -----------------------

def test_mars_and_mercury_in_the_second_fires(base_chart, doctrine, cards):
    c = place(base_chart, "Mars", sign_mid("Aquarius"))
    c = place(c, "Mercury", sign_mid("Aquarius"))
    assert fires(c, doctrine, cards, "PD.07.RajaYoga.MarsMercurySecond")


def test_only_mars_in_the_second_does_not_fire(base_chart, doctrine, cards):
    c = place(base_chart, "Mars", sign_mid("Aquarius"))
    c = place(c, "Mercury", sign_mid("Pisces"))
    assert not fires(c, doctrine, cards, "PD.07.RajaYoga.MarsMercurySecond")


# --- v.24 item (3): PD.07.RajaYoga.SunVenusFourth --------------------------

def test_sun_and_venus_in_the_fourth_fires(base_chart, doctrine, cards):
    c = place(base_chart, "Sun", sign_mid("Aries"))
    c = place(c, "Venus", sign_mid("Aries"))
    assert fires(c, doctrine, cards, "PD.07.RajaYoga.SunVenusFourth")


def test_only_sun_in_the_fourth_does_not_fire(base_chart, doctrine, cards):
    c = place(base_chart, "Sun", sign_mid("Aries"))
    c = place(c, "Venus", sign_mid("Taurus"))
    assert not fires(c, doctrine, cards, "PD.07.RajaYoga.SunVenusFourth")


# --- v.24 item (4): PD.07.RajaYoga.MarsSaturnJupiterTenthEleventhLagna -----

def test_mars_saturn_jupiter_respectively_in_tenth_eleventh_lagna_fires(base_chart, doctrine, cards):
    c = place(base_chart, "Mars", sign_mid("Libra"))       # 10th
    c = place(c, "Saturn", sign_mid("Scorpio"))            # 11th
    c = place(c, "Jupiter", sign_mid("Capricorn"))         # Lagna
    assert fires(c, doctrine, cards, "PD.07.RajaYoga.MarsSaturnJupiterTenthEleventhLagna")


def test_the_three_grahas_in_the_wrong_houses_does_not_fire(base_chart, doctrine, cards):
    """'Respectively' fixes the pairing -- the same three grahas in the same
    three houses but permuted must not satisfy the card."""
    c = place(base_chart, "Mars", sign_mid("Scorpio"))     # swapped with Saturn
    c = place(c, "Saturn", sign_mid("Libra"))
    c = place(c, "Jupiter", sign_mid("Capricorn"))
    assert not fires(c, doctrine, cards, "PD.07.RajaYoga.MarsSaturnJupiterTenthEleventhLagna")


# --- v.25: PD.07.RajaYoga.HouseLordKendraFromMoonJupiterOwnership ----------

def test_second_lord_jupiter_in_kendra_from_moon_with_jupiter_owning_second_fires(base_chart, doctrine, cards):
    """Scorpio Lagna: Jupiter rules both the 2nd (Sagittarius) and the 5th
    (Pisces), so 'Jupiter owns the 2nd, 5th or 11th' holds regardless of
    where Jupiter sits. The Moon is left at its own real natal sign (Leo);
    Jupiter placed in Scorpio -- the 4th sign from Leo, a kendra-from-Moon --
    is simultaneously the 2nd house's own lord in kendra from the Moon."""
    c = lagna(base_chart, "Scorpio")
    c = place(c, "Jupiter", sign_mid("Scorpio"))
    assert fires(c, doctrine, cards, "PD.07.RajaYoga.HouseLordKendraFromMoonJupiterOwnership")


def test_jupiter_owning_neither_second_fifth_nor_eleventh_does_not_fire(base_chart, doctrine, cards):
    """The chart's own real Capricorn Lagna: Jupiter rules neither the 2nd
    (Aquarius, Saturn's), the 5th (Taurus, Venus's) nor the 11th (Scorpio,
    Mars's), so the card's second clause fails outright regardless of which
    lord sits in kendra from the Moon."""
    assert not fires(base_chart, doctrine, cards, "PD.07.RajaYoga.HouseLordKendraFromMoonJupiterOwnership")
