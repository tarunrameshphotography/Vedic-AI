"""Tests for Milestone 26 -- chapter 6's Adhiyoga (vv. 42-43,
passage:phaladeepika.06.p175).

V.42 states one disjunctive condition in one sentence: Mercury, Jupiter and
Venus each individually within houses 6, 7 or 8, counted from the Lagna OR
from the Moon. This is encoded as a single card, PD.06.Adhiyoga, not two --
a two-card split (one per reference frame) would have quoted the identical
naming-plus-effect text on both cards, which Rules/tools/dupes.py correctly
flags as a same-book encoding defect (no other pair in the store shares a
full quote_sha256; this was checked directly during encoding). The worked
example's own "Lagnadhiyoga"/"Chandradhiyoga" labels (tier-3 apparatus) are
not imported into predicts; Engine/rules.py::evaluate's own solution
bindings already distinguish which frame(s) actually satisfied the
condition, so which reference frame fired is still visible in a claim's
own `conditions_satisfied` without a second card.

The Notes (para 183) report an unnamed "some authors" reading requiring all
three houses non-vacant, which the translator explicitly rejects in the
same sentence in favour of Shruti Kirti's (per Vyas) confirmation of the
looser reading PD.06.Adhiyoga already tests. PD.06.Adhiyoga.ShrutiKirti
(reference) preserves that dispute in the source's own words. The rejected
reading is NOT encoded as a competing active `contradicts` card -- see
concept:adhiyoga-distribution-strictness in Rules/deferred.json for why:
its actual claim is a denial that the yoga forms, which the schema has no
way to assert as a firing rule.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.activate import activate
from Engine.adjudicate import PARALLEL_AUTHORITY, RECORDED, verify_adjudications
from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import extract_facts
from Engine.pipeline import run
from Engine.rules import load_cards
from Engine.tests.test_strength import place

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"


@pytest.fixture(scope="module")
def cards():
    return load_cards(RULES)


@pytest.fixture(scope="module")
def provider():
    p = SwissEphemerisDLL()
    yield p
    p.close()


@pytest.fixture(scope="module")
def doctrine(cards):
    return Doctrine.from_cards(cards)


# --- the card store itself ---------------------------------------------------

def test_adhiyoga_is_one_active_card_not_two(cards):
    """The Lagna-or-Moon disjunction is one condition on one card; there is
    no PD.06.Adhiyoga.Lagna / .Moon pair."""
    ids = {c.id for c in cards if c.id.startswith("PD.06.Adhiyoga")}
    assert ids == {"PD.06.Adhiyoga", "PD.06.Adhiyoga.ShrutiKirti"}
    adhiyoga = next(c for c in cards if c.id == "PD.06.Adhiyoga")
    assert adhiyoga.activation == "active"
    assert adhiyoga.predicts == {"domain": "yoga", "yoga": "Adhiyoga"}


def test_adhiyoga_condition_is_the_lagna_or_moon_disjunction(cards):
    """One top-level `any` of two frame blocks, each requiring Mercury,
    Jupiter and Venus individually within houses 6/7/8 -- no requirement
    that all three houses be occupied (the reading the Notes reject)."""
    adhiyoga = next(c for c in cards if c.id == "PD.06.Adhiyoga")
    outer = adhiyoga.conditions["all"]
    assert len(outer) == 1
    frames = outer[0]["any"]
    assert len(frames) == 2

    def grahas_tested(frame_block, key):
        leaves = frame_block["all"]
        assert len(leaves) == 3
        grahas = set()
        for leaf in leaves:
            options = leaf["any"]
            assert len(options) == 3
            houses = {opt[key]["house"] for opt in options}
            assert houses == {6, 7, 8}
            grahas.add(options[0][key]["graha"])
        return grahas

    lagna_block = next(f for f in frames if "in_house" in f["all"][0]["any"][0])
    moon_block = next(f for f in frames if "in_house_from" in f["all"][0]["any"][0])
    assert grahas_tested(lagna_block, "in_house") == {"Mercury", "Jupiter", "Venus"}
    assert grahas_tested(moon_block, "in_house_from") == {"Mercury", "Jupiter", "Venus"}
    for opt in moon_block["all"][0]["any"]:
        assert opt["in_house_from"]["reference"] == "Moon"


def test_shruti_kirti_card_is_reference_only(cards):
    """Tests nothing beyond PD.06.Adhiyoga's own loose reading; exists so
    the rejected "some authors" reading is preserved in the source's own
    words rather than silently dropped."""
    notes = next(c for c in cards if c.id == "PD.06.Adhiyoga.ShrutiKirti")
    assert notes.activation == "reference"
    assert notes.conditions == {"all": []}
    assert notes.predicts["authority"] == "Shruti Kirti (per Vyas)"
    assert notes.raw["parallel_of"] == ["PD.06.Adhiyoga"]
    # Both readings the Notes paragraph reports are visible in one quote --
    # the rejected one and the endorsed one -- not just the winning side.
    assert "some authors" in notes.quote.lower()
    assert "shruti kirti" in notes.quote.lower()
    assert "not correct" in notes.quote.lower()


def test_notes_quote_uses_an_em_dash_not_a_defect(cards):
    """The byte between "Notes" and "Some authors" is a genuine em dash
    (U+2014) in Knowledge/phaladeepika.md -- it renders as a replacement
    glyph in some fonts/terminals, which is why it looked like a defect
    during encoding, but it is a valid character, matching the "Notes - "
    separator used elsewhere in this chapter."""
    notes = next(c for c in cards if c.id == "PD.06.Adhiyoga.ShrutiKirti")
    assert notes.quote.startswith("Notes— Some authors")


def test_adhiyoga_names_exactly_mercury_jupiter_venus(cards):
    """V.42 itself says only "the benefic planets"; the Notes and the
    worked example both fix the acting set to these three specifically, not
    "any benefic" including a variable-nature Moon."""
    adhiyoga = next(c for c in cards if c.id == "PD.06.Adhiyoga")
    grahas = set()
    for frame in adhiyoga.conditions["all"][0]["any"]:
        for leaf in frame["all"]:
            key = "in_house" if "in_house" in leaf["any"][0] else "in_house_from"
            grahas.add(leaf["any"][0][key]["graha"])
    assert grahas == {"Mercury", "Jupiter", "Venus"}


# --- adjudication: parallel authority, never a fabricated contradiction -----

def test_shruti_kirti_relationship_is_parallel_not_contradicts(cards):
    """The store draws no `contradicts` link for the rejected reading --
    see concept:adhiyoga-distribution-strictness for why one would
    misrepresent the actual disagreement (a denial of formation the schema
    cannot assert as a firing claim)."""
    adhiyoga = next(c for c in cards if c.id == "PD.06.Adhiyoga")
    notes = next(c for c in cards if c.id == "PD.06.Adhiyoga.ShrutiKirti")
    assert not notes.raw.get("contradicts")
    assert not adhiyoga.raw.get("contradicts")
    assert not adhiyoga.raw.get("parallel_of")


def test_deferred_json_resolves_p175_and_opens_the_strictness_concept():
    import json
    registry = json.loads((RULES / "deferred.json").read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in registry["entries"]}

    p175 = by_id["passage:phaladeepika.06.p175"]
    assert p175["status"] == "resolved"

    concept = by_id["concept:adhiyoga-distribution-strictness"]
    assert concept["status"] == "deferred"
    assert concept["kind"] == "concept"


# --- real charts --------------------------------------------------------------

# The project's standing demo nativity already exercises Adhiyoga via its
# Moon-frame arm alone: Mercury in the 7th, Jupiter in the 8th and Venus in
# the 6th, all counted from the Moon -- confirmed by inspecting the fired
# claim's own conditions_satisfied, not assumed.
DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate",
)


@pytest.fixture(scope="module")
def demo_result():
    return run(DEMO)


def test_demo_chart_fires_adhiyoga_via_the_moon_frame_only(demo_result):
    fired = [c for c in demo_result.claims
             if c.derived["rule_card"] == "PD.06.Adhiyoga"]
    assert len(fired) == 1
    sats = set(fired[0].derived["conditions_satisfied"])
    assert sats == {
        "in_house_from(Mercury,Moon,7)",
        "in_house_from(Jupiter,Moon,8)",
        "in_house_from(Venus,Moon,6)",
    }
    assert not any(s.startswith("in_house(") for s in sats)


def test_demo_chart_shruti_kirti_relationship_is_recorded_not_unresolved(
    demo_result, cards
):
    """PD.06.Adhiyoga.ShrutiKirti never fires (reference-only), so the
    relationship the store declares is on file but not a chart finding."""
    hits = [a for a in demo_result.adjudications
            if {p.card for p in a.parties} == {
                "PD.06.Adhiyoga", "PD.06.Adhiyoga.ShrutiKirti"}]
    assert len(hits) == 1
    adj = hits[0]
    assert adj.relationship == PARALLEL_AUTHORITY
    assert adj.resolution == RECORDED
    assert verify_adjudications(
        demo_result.adjudications, demo_result.claims, cards
    ) == []


# --- constructed charts: the Lagna-only and both-frames-at-once cases -------
#
# The demo chart's own Lagna (Capricorn, sign_index 9) and Moon (Leo, sign_index
# 4) sit five signs apart. Because each frame's window is exactly the three
# signs {6th,7th,8th} = a 90-degree arc, the two windows overlap only when the
# frames are within about two signs of each other -- five signs apart, as here,
# never overlaps for any placement, which is why the demo chart's own claim
# fires via the Moon frame alone and can never also satisfy the Lagna frame.
# A "both frames" chart therefore needs a genuinely different Lagna/Moon
# separation, and a blind search across thousands of real nativities (four
# cities, 1950-2010, by date and time of day) found none within the sweep's
# own time budget -- not surprising once the five-sign-separation arithmetic
# above is worked out; a same-day, all-hours scan at the demo's own
# coordinates independently confirmed no Lagna in that specific day's rotation
# ever lands within two signs of that day's Moon. So these two cases are
# constructed, the same precedent test_chapter_six_strength.py itself uses
# for placements "that simply do not occur on any convenient birthday" (see
# its own docstring on test_duryoga_reverse_fires_on_a_constructed_chart):
# `place()` moves one body on a real, ephemeris-computed chart to an exact
# sidereal longitude, keeping every other quantity -- the Lagna, the other
# bodies, the whole house frame -- exactly what the ephemeris produced.

DEMO_BASE = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate",
)


def _sign_lon(sign_index: int) -> float:
    return sign_index * 30.0 + 15.0  # middle of the sign, well clear of a cusp


def _base_chart(provider):
    return compute_chart(resolve_birth(DEMO_BASE, provider), provider)


def _with_mercury_jupiter_venus_at(chart, m_idx, j_idx, v_idx):
    chart = place(chart, "Mercury", _sign_lon(m_idx))
    chart = place(chart, "Jupiter", _sign_lon(j_idx))
    chart = place(chart, "Venus", _sign_lon(v_idx))
    return chart


def test_lagna_only_fires_on_a_constructed_chart(provider, cards, doctrine):
    """Mercury, Jupiter and Venus moved to the 6th, 7th and 8th signs from
    the (unmoved, real) Lagna; the Moon is left at its own real placement
    (Leo, five signs from the Lagna), so the Moon-frame window ({9,10,11}
    by the same arithmetic) cannot also be satisfied."""
    chart = _base_chart(provider)
    # Ascendant is sign_index 9 (Capricorn) on this chart; 6th/7th/8th signs
    # from it are indices 2, 3, 4 (Gemini, Cancer, Leo).
    assert chart.ascendant_sign_index == 9
    chart = _with_mercury_jupiter_venus_at(chart, 2, 3, 4)
    facts = extract_facts(chart, doctrine)
    claims, _ = activate(chart, facts, cards)
    fired = [c for c in claims if c.derived["rule_card"] == "PD.06.Adhiyoga"]
    assert len(fired) == 1
    sats = set(fired[0].derived["conditions_satisfied"])
    assert sats == {
        "in_house(Mercury,6)", "in_house(Jupiter,7)", "in_house(Venus,8)",
    }
    assert not any(s.startswith("in_house_from(") for s in sats)


def test_both_frames_fire_together_on_a_constructed_chart(provider, cards, doctrine):
    """The Moon moved into the same sign as the Lagna makes the two frames
    coincide exactly, so Mercury/Jupiter/Venus in the 6th/7th/8th signs from
    the Lagna satisfy the Moon frame identically -- the same "there is both
    Lagnadhiyoga and Chandradhiyoga" situation the Sardar Patel worked
    example (tier-3 apparatus, para 178) reports for its own real chart,
    reproduced here as the specific geometry that makes it possible.

    Two claims, not one: the outer `any` has two independently-satisfying
    branches on this chart, and the engine records one claim per distinct
    satisfying solution -- the same multi-claims-per-card behaviour the
    twelve PD.06.DusthanaLord.* cards already exercise on real charts
    (Milestone 25), not a special case for this card."""
    chart = _base_chart(provider)
    assert chart.ascendant_sign_index == 9
    chart = place(chart, "Moon", _sign_lon(9))  # same sign as the Lagna
    chart = _with_mercury_jupiter_venus_at(chart, 2, 3, 4)
    facts = extract_facts(chart, doctrine)
    claims, _ = activate(chart, facts, cards)
    fired = [c for c in claims if c.derived["rule_card"] == "PD.06.Adhiyoga"]
    assert len(fired) == 2
    solutions = {frozenset(c.derived["conditions_satisfied"]) for c in fired}
    assert solutions == {
        frozenset({"in_house(Mercury,6)", "in_house(Jupiter,7)", "in_house(Venus,8)"}),
        frozenset({"in_house_from(Mercury,Moon,6)", "in_house_from(Jupiter,Moon,7)",
                   "in_house_from(Venus,Moon,8)"}),
    }


def test_neither_frame_fires_on_a_constructed_negative_control(
    provider, cards, doctrine
):
    """Mercury, Jupiter and Venus all moved to Aries -- outside both the
    Lagna window ({4th sign} on this chart) and the Moon window ({9th
    sign}) -- so PD.06.Adhiyoga does not fire at all."""
    chart = _base_chart(provider)
    chart = _with_mercury_jupiter_venus_at(chart, 0, 0, 0)
    facts = extract_facts(chart, doctrine)
    claims, _ = activate(chart, facts, cards)
    fired = [c for c in claims if c.derived["rule_card"] == "PD.06.Adhiyoga"]
    assert fired == []
