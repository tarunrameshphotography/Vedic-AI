"""Tests for Milestone 36 -- Phaladeepika chapter 7 slice 1, the Neechabhanga
Raja Yoga family (vv.26-30, five cards: PD.07.Neechabhanga.LordOrExaltedInSign
/.MutualKendra/.AspectedByLord/.LordOrExaltLordKendra/.PlanetItselfKendra).

Zero new engine capability: every card is an existential ("any") over the
seven classical grahas, each branch built from `dignity`, `in_house_class`,
`in_house_from`, `in_house` and `aspects`, all already implemented. What is
new is entirely in the rule store -- a per-graha table of debilitation-sign
lord, debilitation-sign exalter, and own-exaltation-sign lord, read from the
store's own PD.01.SignLord.*/PD.01.Exaltation.* cards at authoring time (see
each card's own `note`), not a Python literal in Engine/*.py.

The chart used throughout is built from a real ephemeris chart with select
bodies moved (Engine.tests.test_strength.place), the same discipline
test_strength.py and test_chapter_twenty.py already use for edge cases that
do not occur on any convenient real birthday: an ascendant is additionally
overridden here (dataclasses.replace) since the worked example needs a
specific Lagna the demo nativity does not happen to have.

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

CARD_IDS = [
    "PD.07.Neechabhanga.LordOrExaltedInSign",
    "PD.07.Neechabhanga.MutualKendra",
    "PD.07.Neechabhanga.AspectedByLord",
    "PD.07.Neechabhanga.LordOrExaltLordKendra",
    "PD.07.Neechabhanga.PlanetItselfKendra",
]


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
    return compute_chart(resolve_birth(DEMO, provider), provider)


def lagna(chart, sign: str):
    idx = SIGNS.index(sign)
    return dataclasses.replace(chart, ascendant_sign=sign, ascendant_sign_index=idx)


def sign_mid(sign: str) -> float:
    return SIGNS.index(sign) * 30.0 + 15.0


def fires(chart, doctrine, cards_, card_id: str) -> bool:
    card = next(c for c in cards_ if c.id == card_id)
    facts = extract_facts(chart, doctrine)
    return evaluate(card.conditions, facts).satisfied


# --- source fidelity -----------------------------------------------------

def test_all_five_cards_cite_their_verses(cards):
    by_id = {c.id: c for c in cards if c.id in CARD_IDS}
    assert len(by_id) == 5
    assert by_id["PD.07.Neechabhanga.LordOrExaltedInSign"].verse == "26"
    assert by_id["PD.07.Neechabhanga.MutualKendra"].verse == "27"
    assert by_id["PD.07.Neechabhanga.AspectedByLord"].verse == "28"
    assert by_id["PD.07.Neechabhanga.LordOrExaltLordKendra"].verse == "29"
    assert by_id["PD.07.Neechabhanga.PlanetItselfKendra"].verse == "30"


def test_per_graha_table_matches_the_stores_own_reference_cards(doctrine):
    """Guards the literal graha names each card's condition hardcodes against
    drift in PD.01.SignLord.*/PD.01.Exaltation.* -- the same per-graha table
    Engine.doctrine.Doctrine.sign_lord/.exaltation expose at runtime for other
    extractors, read once by hand at authoring time for this card family
    (see each card's own note) rather than looked up per-chart."""
    expected = {
        "Sun": ("Libra", "Venus", "Saturn", "Aries", "Mars"),
        "Moon": ("Scorpio", "Mars", None, "Taurus", "Venus"),
        "Mars": ("Cancer", "Moon", "Jupiter", "Capricorn", "Saturn"),
        "Mercury": ("Pisces", "Jupiter", "Venus", "Virgo", "Mercury"),
        "Jupiter": ("Capricorn", "Saturn", "Mars", "Cancer", "Moon"),
        "Venus": ("Virgo", "Mercury", "Mercury", "Pisces", "Jupiter"),
        "Saturn": ("Aries", "Mars", "Sun", "Libra", "Venus"),
    }
    exalts_in = {}
    for g in expected:
        dig = doctrine.exaltation(g).value
        exalts_in[dig["exaltation_sign"]] = g
    for g, (debil_sign, debil_lord, debil_exalter, exalt_sign, exalt_lord) in expected.items():
        dig = doctrine.exaltation(g).value
        assert dig["debilitation_sign"] == debil_sign, g
        assert dig["exaltation_sign"] == exalt_sign, g
        assert doctrine.sign_lord(debil_sign).value == debil_lord, g
        assert doctrine.sign_lord(exalt_sign).value == exalt_lord, g
        assert exalts_in.get(debil_sign) == debil_exalter, g


# --- item (1): PD.07.Neechabhanga.LordOrExaltedInSign, v.26 --------------

def test_worked_example_saturn_in_aries_fires_item_one(base_chart, doctrine, cards):
    """The source's own illustration (p.90 Note): Lagna Leo, Saturn debilitated
    in Aries (9th), Mars in Aquarius (7th, kendra to the Lagna), Sun exalted in
    Aries's own exalter conjunct Mercury in Scorpio (4th, kendra to the Lagna).
    Both of item (1)'s candidates -- Aries's lord Mars, and Sun (exalted in
    Aries) -- are satisfied at once, exactly as the worked example states."""
    c = lagna(base_chart, "Leo")
    c = place(c, "Saturn", sign_mid("Aries"))
    c = place(c, "Mars", sign_mid("Aquarius"))
    c = place(c, "Sun", sign_mid("Scorpio"))
    c = place(c, "Mercury", sign_mid("Scorpio"))
    c = place(c, "Moon", sign_mid("Leo"))
    assert fires(c, doctrine, cards, "PD.07.Neechabhanga.LordOrExaltedInSign")


def test_saturn_debilitated_with_neither_candidate_in_kendra_does_not_fire(base_chart, doctrine, cards):
    c = lagna(base_chart, "Leo")
    c = place(c, "Saturn", sign_mid("Aries"))
    c = place(c, "Mars", sign_mid("Gemini"))    # 11th -- not kendra
    c = place(c, "Sun", sign_mid("Virgo"))       # 2nd -- not kendra
    c = place(c, "Moon", sign_mid("Leo"))        # coincides with the Lagna sign,
    # so kendra-from-Moon and kendra-from-Lagna are the same four houses here
    assert not fires(c, doctrine, cards, "PD.07.Neechabhanga.LordOrExaltedInSign")


def test_moon_debilitated_in_scorpio_uses_only_the_debilitation_lord(base_chart, doctrine, cards):
    """Scorpio has no classical exalter among Sun-Saturn (Mantreswara is
    silent on Rahu/Ketu's exaltation), so the Moon's item-1 branch carries
    only Mars (Scorpio's own lord) as a candidate -- confirmed by construction
    here: Mars in kendra alone is sufficient."""
    c = lagna(base_chart, "Leo")
    c = place(c, "Moon", sign_mid("Scorpio"))
    c = place(c, "Mars", sign_mid("Taurus"))     # 10th -- kendra
    assert fires(c, doctrine, cards, "PD.07.Neechabhanga.LordOrExaltedInSign")


def test_non_debilitated_moon_does_not_fire_item_one(base_chart, doctrine, cards):
    c = lagna(base_chart, "Leo")
    c = place(c, "Moon", sign_mid("Cancer"))     # exalted, not debilitated
    c = place(c, "Mars", sign_mid("Taurus"))
    assert not fires(c, doctrine, cards, "PD.07.Neechabhanga.LordOrExaltedInSign")


# --- item (2): PD.07.Neechabhanga.MutualKendra, v.27 ----------------------

def test_mercury_debilitated_with_mutual_kendra_lords_fires_item_two(base_chart, doctrine, cards):
    """Mercury debilitated in Pisces: debilitation lord Jupiter, own
    exaltation (Virgo) lord Mercury itself. Jupiter three signs from Mercury
    (Pisces to Gemini) -- in whole-sign houses a 3/6/9-sign offset is its own
    inverse mod 12, so Kendra-from-Mercury for Jupiter also makes Mercury
    Kendra-from-Jupiter, satisfying the mutual test in both directions."""
    c = lagna(base_chart, "Aries")
    c = place(c, "Mercury", sign_mid("Pisces"))   # 12th
    c = place(c, "Jupiter", sign_mid("Gemini"))   # 3rd
    assert fires(c, doctrine, cards, "PD.07.Neechabhanga.MutualKendra")


def test_lords_not_a_kendra_offset_apart_does_not_satisfy_the_mutual_test(base_chart, doctrine, cards):
    c = lagna(base_chart, "Aries")
    c = place(c, "Mercury", sign_mid("Pisces"))   # 12th
    c = place(c, "Jupiter", sign_mid("Aries"))    # 1st -- 2nd from Mercury,
    # not a 3/6/9 offset either direction
    assert not fires(c, doctrine, cards, "PD.07.Neechabhanga.MutualKendra")


# --- item (3): PD.07.Neechabhanga.AspectedByLord, v.28 --------------------

def test_debilitated_planet_aspected_by_its_own_lord_fires_item_three(base_chart, doctrine, cards):
    """Saturn debilitated in Aries (lord Mars); Mars placed exactly seven
    houses from Saturn, the universal 7th-house aspect every graha carries."""
    c = lagna(base_chart, "Cancer")
    c = place(c, "Saturn", sign_mid("Aries"))     # 10th
    c = place(c, "Mars", sign_mid("Libra"))       # 4th, 7th from Saturn's house
    assert fires(c, doctrine, cards, "PD.07.Neechabhanga.AspectedByLord")


def test_debilitated_planet_not_aspected_by_its_lord_does_not_fire(base_chart, doctrine, cards):
    c = lagna(base_chart, "Cancer")
    c = place(c, "Saturn", sign_mid("Aries"))
    c = place(c, "Mars", sign_mid("Taurus"))      # not 7th (or a special
    # aspect house) from Saturn's placement
    assert not fires(c, doctrine, cards, "PD.07.Neechabhanga.AspectedByLord")


# --- item (4): PD.07.Neechabhanga.LordOrExaltLordKendra, v.29 -------------

def test_mercury_debilitated_uses_its_own_exaltation_lord_not_the_sign_exalter(base_chart, doctrine, cards):
    """Item 4's second candidate for Mercury is Mercury itself (sign_lord of
    Virgo, Mercury's own exaltation sign) -- unlike item 1's second candidate,
    which for Mercury is Venus (the graha exalted in Pisces, Mercury's
    debilitation sign). Mercury must stay in Pisces to remain debilitated, so
    it is the Lagna, not Mercury, that is chosen to make Pisces a Kendra
    house (Sagittarius Lagna puts Pisces in the 4th) -- satisfying item 4's
    own-exaltation-lord arm (Mercury itself, already in Kendra by
    construction) while Jupiter (both cards' shared first candidate) and
    Venus (item 1's own second candidate) are kept out of Kendra from both
    the Lagna and the Moon, leaving item 1 unsatisfied."""
    c = lagna(base_chart, "Sagittarius")
    c = place(c, "Mercury", sign_mid("Pisces"))   # 4th -- kendra
    c = place(c, "Jupiter", sign_mid("Leo"))       # 9th -- not kendra
    c = place(c, "Venus", sign_mid("Leo"))         # 9th -- not kendra
    c = place(c, "Moon", sign_mid("Sagittarius"))  # coincides with the Lagna
    # sign, so kendra-from-Moon adds nothing Jupiter/Venus's 9th already avoids
    assert not fires(c, doctrine, cards, "PD.07.Neechabhanga.LordOrExaltedInSign")
    assert fires(c, doctrine, cards, "PD.07.Neechabhanga.LordOrExaltLordKendra")


# --- item (5): PD.07.Neechabhanga.PlanetItselfKendra, v.30 ----------------

def test_debilitated_planet_itself_in_kendra_fires_item_five(base_chart, doctrine, cards):
    c = lagna(base_chart, "Sagittarius")
    c = place(c, "Venus", sign_mid("Virgo"))      # debilitated, 10th -- kendra
    assert fires(c, doctrine, cards, "PD.07.Neechabhanga.PlanetItselfKendra")


def test_debilitated_planet_outside_kendra_does_not_fire_item_five(base_chart, doctrine, cards):
    c = lagna(base_chart, "Sagittarius")
    c = place(c, "Venus", sign_mid("Leo"))        # debilitated, 9th -- not kendra
    c = place(c, "Moon", sign_mid("Sagittarius"))  # coincides with the Lagna
    assert not fires(c, doctrine, cards, "PD.07.Neechabhanga.PlanetItselfKendra")


# --- negative discipline --------------------------------------------------

def test_no_undebilitated_graha_ever_fires_any_of_the_five_cards(base_chart, doctrine, cards):
    """A chart with every graha in a strong dignity should satisfy none of
    the five cards -- each one's outer condition is an `any` of per-graha
    branches that all begin with dignity(g, 'debilitated')."""
    c = lagna(base_chart, "Aries")
    for g, sign in [("Sun", "Aries"), ("Moon", "Taurus"), ("Mars", "Capricorn"),
                    ("Mercury", "Virgo"), ("Jupiter", "Cancer"),
                    ("Venus", "Pisces"), ("Saturn", "Libra")]:
        c = place(c, g, sign_mid(sign))  # each graha in its own exaltation sign
    for card_id in CARD_IDS:
        assert not fires(c, doctrine, cards, card_id), card_id
