"""Tests for Milestone 39 -- Phaladeepika chapter 7 v.23
(PD.07.King.MoonAdhimitraNavamsaVenusAspected /
.MoonAdhimitraNavamsaVenusJupiterAspected), the passage
dep.compound-friendship was built to release.

"The Navamsa of an Adhimitra" is read the same idiom dep.dignity-friendship
already established for natural friendship -- the sign's *lord* classifies
the graha occupying it -- extended from the Rasi to the Navamsa (D9) and from
natural friendship to the compound (Panchadha Maitri) tier. Both cards are a
six-way existential over the D9 sign(s) each of the six other classical
grahas rules (this store's own PD.01.SignLord.* table, embedded at authoring
time, the same discipline PD.05.Livelihood.* and PD.07.Neechabhanga.* already
used) AND that lord's own compound_relationship to the Moon being Adhimitra.
No new predicate beyond compound_relationship itself; in_varga_sign and
aspects are both reused exactly as declared.

The chart used throughout is the project's own real Thanjavur nativity
(Capricorn Lagna). Moon and, where needed, Venus/Jupiter are moved with
Engine.tests.test_strength.place -- a real chart with one body relocated,
not a hand-built world -- following test_chapter_five_livelihood.py's own
lon_for/place idiom for landing a body's D9 sign on a chosen target.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.chart import BirthRecord, SIGNS, compute_chart, resolve_birth
from Engine.doctrine import Doctrine
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import extract_facts
from Engine.rules import evaluate, load_cards, _predicates_used
from Engine.tests.test_chapter_five_livelihood import lon_for, d9_of
from Engine.tests.test_strength import place

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)

CARD_IDS = [
    "PD.07.King.MoonAdhimitraNavamsaVenusAspected",
    "PD.07.King.MoonAdhimitraNavamsaVenusJupiterAspected",
]

LORD_FOR_SIGN = {"Aries": "Mars", "Scorpio": "Mars", "Gemini": "Mercury",
                  "Virgo": "Mercury", "Sagittarius": "Jupiter", "Pisces": "Jupiter",
                  "Taurus": "Venus", "Libra": "Venus", "Capricorn": "Saturn",
                  "Aquarius": "Saturn", "Leo": "Sun"}


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


def fires(chart, doctrine, cards_, card_id: str) -> bool:
    card = next(c for c in cards_ if c.id == card_id)
    facts = extract_facts(chart, doctrine)
    return evaluate(card.conditions, facts).satisfied


# --- source fidelity ---------------------------------------------------------

def test_both_cards_are_present_and_cite_v23(cards):
    by_id = {c.id: c for c in cards if c.id in CARD_IDS}
    assert set(by_id) == set(CARD_IDS)
    for c in by_id.values():
        assert c.verse == "23"
        assert c.chapter == 7
        assert c.activation != "inert"


def test_second_card_extends_the_first(cards):
    c2 = next(c for c in cards if c.id == "PD.07.King.MoonAdhimitraNavamsaVenusJupiterAspected")
    assert c2.raw.get("extends") == ["PD.07.King.MoonAdhimitraNavamsaVenusAspected"]


def test_cards_use_no_predicate_beyond_what_the_milestone_claims(cards):
    by_id = {c.id: c for c in cards if c.id in CARD_IDS}
    used = set()
    for c in by_id.values():
        used |= _predicates_used(c.conditions)
    assert used == {"in_varga_sign", "compound_relationship", "aspects"}


# --- drift guard: the per-graha D9 sign-lord table both cards embed --------

def _signs_by_other_graha(node, out=None):
    """{other_graha: {D9 signs the card's own branch requires for it}},
    read directly out of the authored condition tree rather than trusted."""
    if out is None:
        out = {}
    if isinstance(node, dict):
        if "compound_relationship" in node:
            pass  # matched at the sibling level below
        for k in ("all", "any"):
            for child in node.get(k, ()):
                _signs_by_other_graha(child, out)
        if "all" in node:
            branch = node["all"]
            other = next((c["compound_relationship"]["other"] for c in branch
                          if "compound_relationship" in c), None)
            if other:
                signs = set()
                for c in branch:
                    if "in_varga_sign" in c:
                        signs.add(c["in_varga_sign"]["sign"])
                    for grand in c.get("any", ()):
                        if "in_varga_sign" in grand:
                            signs.add(grand["in_varga_sign"]["sign"])
                out.setdefault(other, set()).update(signs)
    return out


@pytest.mark.parametrize("card_id", CARD_IDS)
def test_embedded_navamsa_lord_table_matches_pd01_signlord(card_id, cards, doctrine):
    """The D9 sign(s) each branch requires for a given lord must be exactly
    the signs PD.01.SignLord.* (ch.1 v.6) gives that graha as lord of, and the
    Moon itself must carry no branch (Cancer is missing on purpose --
    compound_relationship(Moon,Moon,*) is never emitted)."""
    card = next(c for c in cards if c.id == card_id)
    embedded = _signs_by_other_graha(card.conditions)
    assert set(embedded) == {"Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    for graha, signs in embedded.items():
        assert signs == set(doctrine.signs_ruled_by(graha).value), graha
    assert "Moon" not in embedded


@pytest.mark.parametrize("card_id", CARD_IDS)
def test_every_adhimitra_branch_names_the_moon(card_id, cards):
    """Every compound_relationship leaf is anchored to the Moon specifically
    (v.23's own subject) and asks for the Adhimitra tier, never a weaker one."""
    card = next(c for c in cards if c.id == card_id)

    def leaves(node):
        if isinstance(node, dict):
            if "compound_relationship" in node:
                yield node["compound_relationship"]
            for k in ("all", "any"):
                for child in node.get(k, ()):
                    yield from leaves(child)

    found = list(leaves(card.conditions))
    assert len(found) == 6
    for leaf in found:
        assert leaf["graha"] == "Moon"
        assert leaf["category"] == "Adhimitra"


# --- pipeline: the real chart, one body relocated, not a hand-built world -

def test_fires_when_moon_sits_in_its_adhimitra_navamsa_aspected_by_venus(
        base_chart, doctrine, cards):
    """Moon placed in Aries (carrier) with its own D9 landing on Leo -- the
    Sun's own sign -- makes the Sun the Navamsa-owner. The Sun classifies the
    Moon a natural friend (PD.02.Friendship.NaturalTable, unambiguously: Sun's
    own row lists the Moon once, under Friend only) and, from Aries, the Sun
    (real chart position: Aquarius) falls in the 3rd house from the Moon -- a
    temporary friend by v.23's own house partition -- so the pair is
    Adhimitra. Venus is placed in Libra, the 7th house from the Moon's new
    house (4th), the only offset an ordinary graha casts a full aspect at."""
    c = place(base_chart, "Moon", lon_for("Aries", 4))
    assert d9_of(c, doctrine, "Moon") == "Leo"
    assert c.bodies["Sun"].sign == "Aquarius"          # real, unmoved
    c = place(c, "Venus", SIGNS.index("Libra") * 30.0 + 10.0)
    assert c.bodies["Moon"].house == 4
    assert c.bodies["Venus"].house == 10
    facts = extract_facts(c, doctrine)
    assert "compound_relationship(Moon,Sun,Adhimitra)" in facts
    assert "aspects(Venus,Moon)" in facts
    assert fires(c, doctrine, cards, "PD.07.King.MoonAdhimitraNavamsaVenusAspected")
    assert not fires(c, doctrine, cards,
                     "PD.07.King.MoonAdhimitraNavamsaVenusJupiterAspected")


def test_the_jupiter_variant_also_needs_jupiters_own_aspect(base_chart, doctrine, cards):
    """The same configuration as above, with Jupiter additionally placed to
    cast a full aspect on the Moon too -- only then does the second sentence's
    own card fire, on top of (not instead of) the first."""
    c = place(base_chart, "Moon", lon_for("Aries", 4))
    c = place(c, "Venus", SIGNS.index("Libra") * 30.0 + 10.0)
    c = place(c, "Jupiter", SIGNS.index("Libra") * 30.0 + 20.0)
    assert c.bodies["Jupiter"].house == 10
    facts = extract_facts(c, doctrine)
    assert "aspects(Jupiter,Moon)" in facts
    assert fires(c, doctrine, cards, "PD.07.King.MoonAdhimitraNavamsaVenusAspected")
    assert fires(c, doctrine, cards,
                "PD.07.King.MoonAdhimitraNavamsaVenusJupiterAspected")


def test_does_not_fire_on_the_real_unmodified_chart(base_chart, doctrine, cards):
    """Negative control: the real nativity's own Moon (Leo, D9 Leo, its own
    Navamsa -- not any other graha's) does not qualify, and neither card
    over-fires on a chart that was never built to satisfy it."""
    assert not fires(base_chart, doctrine, cards,
                     "PD.07.King.MoonAdhimitraNavamsaVenusAspected")
    assert not fires(base_chart, doctrine, cards,
                     "PD.07.King.MoonAdhimitraNavamsaVenusJupiterAspected")


def test_does_not_fire_when_the_navamsa_lord_is_only_a_plain_friend(base_chart, doctrine, cards):
    """Same D9/aspect setup, but the temporary relationship flipped to
    inimical (Moon moved to a sign 6 signs from the Sun rather than 2) drops
    the pair to Sama, not Adhimitra -- the card must not accept a lesser
    compound tier as though the verse had said "a friend" rather than "an
    Adhimitra"."""
    c = place(base_chart, "Moon", lon_for("Leo", 4))     # D9 still Leo (Fixed, +4)
    assert d9_of(c, doctrine, "Moon") == "Leo"
    facts = extract_facts(c, doctrine)
    rel = next(f for f in facts.by_predicate("compound_relationship")
              if f.args["graha"] == "Moon" and f.args["other"] == "Sun")
    assert rel.args["category"] != "Adhimitra"
    assert not fires(c, doctrine, cards, "PD.07.King.MoonAdhimitraNavamsaVenusAspected")


# --- golden: the real chart, whole pipeline, verified end to end ----------

def test_golden_pipeline_verifies_on_the_real_chart(provider):
    from Engine.pipeline import run
    r = run(DEMO)
    assert r.verification.ok
