"""Tests for Milestone 25 -- the twelve dusthana-lord yogas of chapter 6,
vv. 57-69 (passage:phaladeepika.06.p202), and the Mantreswara/Parashara
relationships they open.

v.57 states one template for all twelve house-wise yogas: house N (N=1..12
from the Lagna) forms its own named yoga when any of the lords of the 6th,
8th or 12th houses is posited in house N, or house N is occupied by or
aspected by a malefic. v.63 and v.65 restate this in full for N=6 (Harsha)
and N=8 (Sarala), which is what the general reading rests on rather than
imported convention. The house-10 member is named PD.06.DusthanaLord.Duryoga,
not PD.06.Duryoga, to stay distinguishable from the unrelated v.70 Duryoga
pair (Milestone 24) -- exactly the collision this passage's own deferred.json
entry flagged before either was encoded.

Parashara's own nine-combination breakdown of the same dusthana-lord-in-
dusthana sub-case (paras 220-228, quoted by the translator) is encoded as ten
further cards and linked to PD.06.DusthanaLord.Harsha/.Sarala/.Vimala by
`contradicts` (five pairs, two of them `polarity: qualified`) or `parallel_of`
(two pairs) -- Stage 7's second genuine claim-to-claim contradiction cluster,
after the one PD.09.Dignity.Exalted pair Milestone 23 built the reading layer
for. See Rules/deferred.json's resolution note on passage:phaladeepika.06.p202
for the full relationship-by-relationship reasoning.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.adjudicate import (
    CONTRADICTION,
    PARALLEL_AUTHORITY,
    QUALIFICATION,
    RECORDED,
    UNRESOLVED,
    verify_adjudications,
)
from Engine.chart import BirthRecord
from Engine.pipeline import run
from Engine.rules import load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"


@pytest.fixture(scope="module")
def cards():
    return load_cards(RULES)


def _rec(city, date, time, lat, lon):
    return BirthRecord(
        date=date, time=time, timezone="Asia/Kolkata",
        latitude=lat, longitude=lon, place_name=city,
        time_precision="minute", time_source="memory")


# Real instants found by scanning ~1,700 nativities across four cities
# (Mumbai, Thanjavur, Delhi, Chennai), 1950-2010, for charts where a
# *specific* Parashara sub-case fires alongside its Mantreswara counterpart --
# a genuine chart-dependent relationship, not merely two cards both on record.

# Jupiter, lord of the 6th, sits in the 8th house: Mantreswara's Sarala
# ("excellent results... longlived, resolute, fearless, prosperous...") vs.
# Parashara's item (2), 6th lord in 8th ("sickly, inimical, desire others'
# wealth... impure") -- flatly opposed, no source precedence.
CONTRADICTION_CHART = _rec("Mumbai", "1950-04-05", "14:15", 19.0760, 72.8777)

# Mercury, lord of the 8th, sits in the 8th house, and is independently weak
# (ch.4 strength verdict) on this chart -- both PD.06.Parashara.
# EighthLordInEighth (base: "longlived", agrees with Sarala) and its own
# .Weak sub-card ("medium longevity... a thief, blameworthy", narrows Sarala)
# fire together, so this single real chart exercises both the parallel and
# the qualification relationship at once.
PARALLEL_AND_QUALIFICATION_CHART = _rec(
    "Thanjavur", "1956-10-25", "14:15", 10.7870, 79.1378)

# The project's standing demo nativity: Sarala fires (a malefic aspects the
# 8th) but no Parashara sub-case matches this chart's specific lord
# placements -- the negative control matching test_adjudication.py's own
# demo-chart assertions (all `recorded`, none `unresolved`).
DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate",
)


@pytest.fixture(scope="module")
def contradiction_result():
    return run(CONTRADICTION_CHART)


@pytest.fixture(scope="module")
def parallel_and_qualification_result():
    return run(PARALLEL_AND_QUALIFICATION_CHART)


@pytest.fixture(scope="module")
def demo_result():
    return run(DEMO)


# --- the twelve-card family is a faithful, distinguishable catalogue --------

HOUSE_NAMES = {
    1: "Ava", 2: "Nisswa", 3: "Mriti", 4: "Kuhu", 5: "Pamara", 6: "Harsha",
    7: "Dushkriti", 8: "Sarala", 9: "Nirbhagya", 10: "Duryoga",
    # v.57's own naming list (para. 203) prints "Daridra Yoga"; card id and
    # predicts.yoga follow v.68's own verse spelling, "Daridrya" -- two
    # different printed spellings preserved as printed, same treatment as
    # Subhamala/Asubhamala (Milestone 9). House-number mapping (11th) is
    # unambiguous from the list regardless of which spelling is used.
    11: "Daridrya", 12: "Vimala",
}


def test_twelve_house_cards_match_v57s_own_numbered_list(cards):
    """House-to-name mapping is v.57's own list (para. 203-204), not assumed."""
    by_id = {c.id: c for c in cards}
    for house, name in HOUSE_NAMES.items():
        cid = f"PD.06.DusthanaLord.{name}"
        card = by_id[cid]
        assert card.predicts["house"] == house
        assert card.predicts["yoga"] == name
        assert card.activation == "active"


def test_general_condition_card_is_reference_only(cards):
    general = next(c for c in cards if c.id == "PD.06.DusthanaLord.General")
    assert general.activation == "reference"
    assert general.conditions == {"all": []}


def test_house_ten_duryoga_stays_distinct_from_verse_70s_duryoga(cards):
    """The exact collision Rules/deferred.json flagged before either was
    encoded: two unrelated yogas share the printed name "Duryoga"."""
    by_id = {c.id: c for c in cards}
    v57_duryoga = by_id["PD.06.DusthanaLord.Duryoga"]
    v70_duryoga = by_id["PD.06.Duryoga"]
    v70_reverse = by_id["PD.06.Duryoga.Reverse"]
    assert v57_duryoga.id != v70_duryoga.id != v70_reverse.id
    assert v57_duryoga.quote_sha256 not in (
        v70_duryoga.quote_sha256, v70_reverse.quote_sha256)
    assert v57_duryoga.predicts["house"] == 10
    # v.70's pair test strength/combustion of a different set of house-lords
    # entirely and carry no "house" key at all.
    assert "house" not in v70_duryoga.predicts
    assert "house" not in v70_reverse.predicts


def test_astra_h06_notes_forward_reference_is_now_resolved(cards):
    """PD.06.Astra.H06.Notes (slice 2) already quoted a translator aside
    naming "Verse 57 of this very chapter" before v.57 was encoded; it must
    now corroborate the card that resolves it."""
    notes = next(c for c in cards if c.id == "PD.06.Astra.H06.Notes")
    assert "PD.06.DusthanaLord.General" in notes.raw["parallel_of"]
    assert "not yet encoded" not in notes.raw["note"]


# --- the Parashara breakdown: relationship classification -------------------

def test_parashara_cards_are_active_not_reference(cards):
    """Unlike PD.06.Vesi.AuthoritativeWorks (an undifferentiated collective
    doctrine with no per-graha testable condition), every Parashara
    combination here names one specific lord and one specific house and is
    directly testable -- so, unlike that precedent, these are firing cards."""
    by_id = {c.id: c for c in cards}
    parashara_ids = [c.id for c in cards if c.id.startswith("PD.06.Parashara.")]
    assert len(parashara_ids) == 10
    for cid in parashara_ids:
        assert by_id[cid].activation == "active"


def test_parashara_relationship_types_match_the_sources_own_valence(cards):
    """Not forced uniformly to `contradicts`: the classification follows a
    plain reading of each combination's own stated effect against the
    Mantreswara card's blanket claim (see Rules/deferred.json's resolution
    note for the reasoning behind each one)."""
    by_id = {c.id: c for c in cards}

    contradicts_plain = {
        "PD.06.Parashara.SixthLordInEighth": "PD.06.DusthanaLord.Sarala",
        "PD.06.Parashara.SixthLordInTwelfth": "PD.06.DusthanaLord.Vimala",
        "PD.06.Parashara.EighthLordInTwelfth": "PD.06.DusthanaLord.Vimala",
        "PD.06.Parashara.TwelfthLordInSixth": "PD.06.DusthanaLord.Harsha",
        "PD.06.Parashara.TwelfthLordInTwelfth": "PD.06.DusthanaLord.Vimala",
    }
    for cid, target in contradicts_plain.items():
        card = by_id[cid]
        assert card.raw.get("contradicts") == [target]
        assert card.predicts.get("polarity") != "qualified"

    contradicts_qualified = {
        "PD.06.Parashara.SixthLordInSixth": "PD.06.DusthanaLord.Harsha",
        "PD.06.Parashara.EighthLordInSixth": "PD.06.DusthanaLord.Harsha",
        "PD.06.Parashara.EighthLordInEighth.Weak": "PD.06.DusthanaLord.Sarala",
    }
    for cid, target in contradicts_qualified.items():
        card = by_id[cid]
        assert card.raw.get("contradicts") == [target]
        assert card.predicts.get("polarity") == "qualified"

    parallel = {
        "PD.06.Parashara.EighthLordInEighth": "PD.06.DusthanaLord.Sarala",
        "PD.06.Parashara.TwelfthLordInEighth": "PD.06.DusthanaLord.Sarala",
    }
    for cid, target in parallel.items():
        card = by_id[cid]
        assert card.raw.get("parallel_of") == [target]
        assert card.predicts.get("authority") == "Parashara"


def test_weak_split_is_conditional_not_a_restatement(cards):
    """Item (5)'s two sentences -- an unconditional 'longlived' and a
    conditional 'if weak... medium longevity, a thief' -- are two different
    cards, not one card with an unused clause."""
    by_id = {c.id: c for c in cards}
    base = by_id["PD.06.Parashara.EighthLordInEighth"]
    weak = by_id["PD.06.Parashara.EighthLordInEighth.Weak"]
    assert {"strength"} <= {list(leaf)[0] for leaf in weak.conditions["all"]}
    assert not any("strength" in leaf for leaf in base.conditions["all"])
    assert base.quote_sha256 != weak.quote_sha256


# --- real charts: the relationships as chart-dependent findings -------------

def test_contradiction_fires_on_a_real_chart(contradiction_result, cards):
    fired = {c.derived["rule_card"] for c in contradiction_result.claims}
    assert "PD.06.DusthanaLord.Sarala" in fired
    assert "PD.06.Parashara.SixthLordInEighth" in fired

    hits = [a for a in contradiction_result.adjudications
            if {p.card for p in a.parties} == {
                "PD.06.DusthanaLord.Sarala", "PD.06.Parashara.SixthLordInEighth"}]
    assert len(hits) == 1
    adj = hits[0]
    assert adj.relationship == CONTRADICTION
    assert adj.resolution == UNRESOLVED
    assert all(p.activated for p in adj.parties)
    assert verify_adjudications(
        contradiction_result.adjudications, contradiction_result.claims, cards
    ) == []


def test_parallel_and_qualification_both_fire_on_one_real_chart(
    parallel_and_qualification_result, cards
):
    """Mercury as the 8th lord in the 8th, and independently weak, exercises
    the base card (parallel with Sarala) and its own .Weak qualification of
    Sarala in the same reading -- the source's own two-sentence structure,
    not two unrelated findings stitched together."""
    r = parallel_and_qualification_result
    fired = {c.derived["rule_card"] for c in r.claims}
    assert {
        "PD.06.DusthanaLord.Sarala",
        "PD.06.Parashara.EighthLordInEighth",
        "PD.06.Parashara.EighthLordInEighth.Weak",
    } <= fired

    by_pair = {frozenset(p.card for p in a.parties): a for a in r.adjudications}

    parallel = by_pair[frozenset({
        "PD.06.DusthanaLord.Sarala", "PD.06.Parashara.EighthLordInEighth"})]
    assert parallel.relationship == PARALLEL_AUTHORITY
    assert parallel.resolution == UNRESOLVED

    qualification = by_pair[frozenset({
        "PD.06.DusthanaLord.Sarala", "PD.06.Parashara.EighthLordInEighth.Weak"})]
    assert qualification.relationship == QUALIFICATION
    assert qualification.resolution == UNRESOLVED

    assert verify_adjudications(r.adjudications, r.claims, cards) == []


def test_demo_chart_is_the_negative_control(demo_result):
    """Sarala fires (a malefic aspects the 8th) but this chart's dusthana
    lords do not land in a dusthana, so no Parashara sub-case matches: every
    relationship involving the new cards is `recorded`, not `unresolved` --
    a second authority on file, not a finding about this nativity. See
    test_slice.py's own accounting of exactly which grahas fire and why."""
    fired = {c.derived["rule_card"] for c in demo_result.claims}
    assert "PD.06.DusthanaLord.Sarala" in fired
    assert not any(cid.startswith("PD.06.Parashara.") for cid in fired)
    hits = [a for a in demo_result.adjudications
            if any(p.card.startswith("PD.06.Parashara.") for p in a.parties)]
    assert hits
    assert all(a.resolution == RECORDED for a in hits)
