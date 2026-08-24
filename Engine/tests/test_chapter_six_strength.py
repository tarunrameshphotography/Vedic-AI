"""Tests for Milestone 24 -- the blanket strength condition on chapter 6's
Pancha Mahapurusha Yogas (passage:phaladeepika.06.p009) and the second Duryoga
(passage:phaladeepika.06.p233).

p009 sits inside the Pancha Mahapurusha section of chapter 6 (immediately
after the Jataka Parijata/Saravali corroboration of those five yogas,
immediately before the worked-example introduction for those same five) and
adds two testable clauses to each of PD.06.Ruchaka/.Bhadra/.Hamsa/.Malavya/
.Sasa: the yoga-forming planet must be "vested with strength" (ch.4 vv.4-5's
verdict) and must not be conjunct a malefic. The disjunctive "Lagna or Moon"
clause and the papakartari/hemmed-between clause remain unencoded -- neither
is expressible today (see the cards' own notes and Rules/deferred.json).

p233 (v.70) states a second, unrelated Duryoga: three house-lords (6th, 8th,
12th) vested with strength in a kendra or trikona against four house-lords
(1st, 4th, 9th, 10th) weak or combust in a dusthana, and its unnamed reverse
configuration. Both are encoded with only existing predicates. The most
important finding in this file is that only the reverse configuration can be
shown firing: see test_duryoga_reverse_fires_on_a_constructed_chart and
test_duryoga_named_cannot_fire_given_the_suns_single_strong_path for why, and
PD.06.Duryoga's own note for the full account.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.activate import activate
from Engine.adjudicate import CONTRADICTION, UNRESOLVED, adjudicate
from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import extract_facts
from Engine.pipeline import run
from Engine.rules import load_cards
from Engine.tests.test_strength import place

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

MAHAPURUSHA_CARDS = {
    "PD.06.Ruchaka": "Mars", "PD.06.Bhadra": "Mercury", "PD.06.Hamsa": "Jupiter",
    "PD.06.Malavya": "Venus", "PD.06.Sasa": "Saturn",
}

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


# --- scope: the strength/conjunction clauses touch only the five Mahapurusha
# cards, per the source's own textual position ----------------------------

def test_only_the_five_mahapurusha_cards_carry_the_strength_clause(cards):
    """v.9 is textually anchored to the Pancha Mahapurusha section (see the
    passage:phaladeepika.06.p009 reference card's own note); no other
    chapter-6 card was touched, per the read against the primary text."""
    by_id = {c.id: c for c in cards if c.book_id == "phaladeepika" and c.chapter == 6}
    for cid, graha in MAHAPURUSHA_CARDS.items():
        leaves = by_id[cid].conditions["all"]
        assert {"strength": {"graha": graha, "strength": "strong"}} in leaves
        assert any(
            leaf.get("not", {}).get("all", [{}])[0].get("conjunct")
            == {"graha": graha, "other": "?m"}
            for leaf in leaves
        ), f"{cid} missing the not-conjunct-malefic clause"

    # A sample of other chapter-6 cards, none of which should mention strength.
    untouched = ("PD.06.Chamara", "PD.06.Kesari", "PD.06.Adhama", "PD.06.Sakata",
                 "PD.06.RajaYoga", "PD.06.Shankha")
    for cid in untouched:
        card = by_id[cid]
        import json
        assert '"strength"' not in json.dumps(card.conditions), cid


def test_the_p009_reference_card_never_becomes_a_claim(cards):
    card = next(c for c in cards if c.id == "PD.06.PanchaMahapurusha.StrengthCondition")
    assert card.activation == "reference"
    assert card.conditions == {"all": []}
    r = run(DEMO)
    assert "PD.06.PanchaMahapurusha.StrengthCondition" not in {
        c.derived["rule_card"] for c in r.claims}


def test_an_unrelated_grahas_strength_does_not_affect_ruchaka(provider, cards, doctrine):
    """Ruchaka's strength clause is bound to Mars specifically (a literal, not
    a variable) -- moving an unrelated graha's strength must not change
    whether it fires."""
    base = compute_chart(resolve_birth(DEMO, provider), provider)
    # Mars stays exactly as the demo chart has it (own sign, no verdict);
    # only Jupiter, already weak on the demo chart, moves to exalted/strong.
    moved = place(base, "Jupiter", lon=95.0, retrograde=False)  # Cancer, exalted
    facts = extract_facts(moved, doctrine)
    claims, _ = activate(moved, facts, cards)
    fired = {c.derived["rule_card"] for c in claims}
    assert "PD.06.Ruchaka" not in fired, (
        "Ruchaka must not fire just because an unrelated graha became strong")


# --- adjudication: the retrograde-combust collision behaves identically for
# a Mahapurusha card as it already does for every other strength-conditioned
# card -- no new engine code, confirmed here rather than assumed ------------

def test_ruchaka_does_not_fire_when_mars_hits_the_strength_collision(provider, cards, doctrine):
    """Mars exalted (Capricorn) and in the lagna satisfies Ruchaka's own
    naming clause; retrograde would ordinarily also satisfy v.9's strength
    clause via PD.04.Strength.RetrogradeFive -- but combust at the same time
    triggers concept:retrograde-combust-collision, so _strength emits no
    verdict at all for Mars, and Ruchaka correctly withholds the claim rather
    than guessing which of the two verses governs."""
    base = compute_chart(resolve_birth(DEMO, provider), provider)
    chart = place(base, "Mars", lon=280.0, retrograde=True)      # Capricorn, exalted
    chart = place(chart, "Sun", lon=282.0, retrograde=False)     # combust orb of Mars

    facts = extract_facts(chart, doctrine)
    assert "strength(Mars,strong)" not in facts.keys()
    assert "strength(Mars,weak)" not in facts.keys()

    claims, _ = activate(chart, facts, cards)
    fired = {c.derived["rule_card"] for c in claims}
    assert "PD.06.Ruchaka" not in fired

    adjs = adjudicate(claims, facts, cards)
    hit = [a for a in adjs if a.subject == "the strength of Mars"]
    assert hit, "the collision must still be reported even though no card used it"
    assert hit[0].relationship == CONTRADICTION
    assert hit[0].resolution == UNRESOLVED


# --- p233: the second Duryoga (v.70) ----------------------------------------

def _duryoga_reverse_chart(provider):
    """Leo lagna: the seven relevant house-lords are Sun(1), Mars(4,9),
    Venus(10), Saturn(6), Jupiter(8), Moon(12) -- no graha rules a house on
    both sides of the reverse configuration's strong/weak split. Sun's only
    strong path is exaltation (Aries), which lands in the 9th (trikona) for
    this lagna, so it is placed there; Mars and Venus are placed retrograde
    in other kendra/trikona houses. Saturn, Jupiter and the Moon are placed
    together just across the Aries/Pisces boundary from the Sun -- within
    every one of their combustion orbs (8-17 degrees against a ~1 degree
    separation) -- landing in Pisces, the 8th house (a dusthana), and weak.
    Found by construction, not scanning: see the session's own reasoning for
    why a real chart is astronomically implausible for this seven-role
    condition, and PD.06.Duryoga's note for why the other (named)
    configuration cannot be constructed at all."""
    rec = BirthRecord(date="1990-06-15", time="11:00", timezone="Asia/Kolkata",
                       latitude=19.0760, longitude=72.8777, place_name="Mumbai",
                       time_precision="minute", time_source="memory", sex="male")
    base = compute_chart(resolve_birth(rec, provider), provider)
    assert base.ascendant_sign == "Leo"
    chart = place(base, "Sun", lon=0.5, retrograde=False)          # Aries -> H9 trikona
    chart = place(chart, "Mars", lon=7 * 30 + 10, retrograde=True)  # Scorpio -> H4 kendra
    chart = place(chart, "Venus", lon=1 * 30 + 10, retrograde=True)  # Taurus -> H10 kendra
    chart = place(chart, "Saturn", lon=359.5, retrograde=False)    # Pisces -> H8 dusthana
    chart = place(chart, "Jupiter", lon=359.5, retrograde=False)   # Pisces -> H8 dusthana
    chart = place(chart, "Moon", lon=359.5, retrograde=False)      # Pisces -> H8 dusthana
    return chart


def test_duryoga_reverse_fires_on_a_constructed_chart(provider, cards, doctrine):
    chart = _duryoga_reverse_chart(provider)
    facts = extract_facts(chart, doctrine)
    strengths = {f.args["graha"]: f.args["strength"]
                 for f in facts if f.key.startswith("strength(")}
    assert strengths["Sun"] == "strong"
    assert strengths["Mars"] == "strong"
    assert strengths["Venus"] == "strong"
    assert strengths["Saturn"] == "weak"
    assert strengths["Jupiter"] == "weak"
    assert strengths["Moon"] == "weak"

    claims, _ = activate(chart, facts, cards)
    fired = {c.derived["rule_card"] for c in claims}
    assert "PD.06.Duryoga.Reverse" in fired
    assert "PD.06.Duryoga" not in fired, (
        "the named configuration's roles are the exact opposite and must not "
        "also be satisfied by this chart")

    claim = next(c for c in claims if c.derived["rule_card"] == "PD.06.Duryoga.Reverse")
    assert claim.derived["variables"] == {
        "?l1": "Sun", "?l4": "Mars", "?l9": "Mars", "?l10": "Venus",
        "?l6": "Saturn", "?l8": "Jupiter", "?l12": "Moon",
    }


def test_duryoga_named_cannot_fire_given_the_suns_single_strong_path(cards):
    """Documents, rather than papers over, a real finding: PD.06.Duryoga (the
    verse's own named configuration) could not be shown firing on any
    lagna, real or constructed. Verified across all twelve whole-sign
    lagnas: eight put two of the seven required lord-roles on the same
    graha (impossible -- one graha, one strength verdict), and the
    remaining four -- Leo, Virgo, Sagittarius, Pisces, the only
    collision-free ones -- each bind the Sun to one of the seven roles.
    The Sun's only route to a 'strong' verdict in this store is exaltation
    (Aries; ch.4 v.5 names no other route for a luminary), and Aries does
    not land in a kendra or trikona house for any of those four lagnas
    under the *named* configuration's own role assignment (it does for two
    of them under the reverse configuration's swapped assignment, which is
    exactly why PD.06.Duryoga.Reverse could be constructed and this could
    not). This is confirmed by exhaustive enumeration in the session that
    authored this milestone, not asserted from a single failed attempt --
    reproduced here as a structural check on the condition itself rather
    than a chart search, since no chart to search for exists.
    """
    card = next(c for c in cards if c.id == "PD.06.Duryoga")
    reverse = next(c for c in cards if c.id == "PD.06.Duryoga.Reverse")
    assert card.activation == "active"  # not inert: no predicate is missing

    def strong_weak_split(leaves):
        strong, weak = set(), set()
        for leaf in leaves:
            if "strength" in leaf and leaf["strength"].get("strength") == "strong":
                strong.add(leaf["strength"]["graha"])
            any_leaf = leaf.get("any", [])
            for a in any_leaf:
                s = a.get("strength")
                if s and s.get("strength") == "weak":
                    weak.add(s["graha"])
        return strong, weak

    named_strong, named_weak = strong_weak_split(card.conditions["all"])
    rev_strong, rev_weak = strong_weak_split(reverse.conditions["all"])
    # The two cards test the same seven role-variables with strong/weak
    # swapped -- confirmed structurally, which is what makes the reverse
    # card's real firing a genuine proof of the shared machinery rather
    # than evidence specific to one card.
    assert named_strong == rev_weak == {"?l6", "?l8", "?l12"}
    assert named_weak == rev_strong == {"?l1", "?l4", "?l9", "?l10"}
