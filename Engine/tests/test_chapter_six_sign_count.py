"""Tests for Milestone 27 -- chapter 6's seven-planets-in-N-signs family
(vv. 39-41, passage:phaladeepika.06.p168): Vallaki/Veena, Dharma, Hasha,
Kendra, Shula, Yuga and Gola.

Each of the seven items states one exact count of how many distinct signs
the seven classical grahas (Sun through Saturn; Rahu and Ketu excluded, as
the verse never names them) occupy between them -- 7 down to 1 -- and no
other condition. This needed one new engine fact, `seven_graha_sign_count`
(Engine/facts.py::_seven_graha_sign_count), because nothing in the prior
vocabulary counted distinct signs occupied by a fixed set of bodies:
`occupant_count` counts occupants of one house, not signs occupied overall.
The fact is chart-wide (no graha argument, the same shape as `lagna_sign`),
and each card matches a literal `n` against its exact key -- the same
mechanism `occupant_count` already uses for a literal count, so no new
combinator was needed.

Which nine grahas count as "the seven" is doctrine, not an engine choice, so
it is read from a reference card (PD.06.SevenGrahas, `Doctrine.seven_grahas`)
rather than written as a Python literal in `Engine/facts.py` -- the same
discipline `combustion_source` already follows for naming the Sun, and the
one `test_no_doctrinal_constant_is_written_in_python[facts.py]` exists to
enforce.

Unlike every other family in this store, these seven cards partition every
possible chart: the count is always some value from 1 to 7, so exactly one
of the seven fires on *any* chart, real or constructed -- never zero, never
more than one. That property, not rarity, is what most of the tests below
are actually checking.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from Engine.chart import SIGNS, BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine, DoctrineError
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import (
    DoctrineReport,
    _seven_graha_sign_count,
    chart_frame,
    extract_facts,
)
from Engine.activate import activate
from Engine.pipeline import run
from Engine.rules import load_cards
from Engine.tests.test_strength import place

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

SEVEN_CARDS = ("PD.06.Vallaki", "PD.06.Dharma", "PD.06.Hasha", "PD.06.Kendra",
               "PD.06.Shula", "PD.06.Yuga", "PD.06.Gola")
N_FOR = {"PD.06.Vallaki": 7, "PD.06.Dharma": 6, "PD.06.Hasha": 5,
         "PD.06.Kendra": 4, "PD.06.Shula": 3, "PD.06.Yuga": 2, "PD.06.Gola": 1}


@pytest.fixture(scope="module")
def cards():
    return load_cards(RULES)


@pytest.fixture(scope="module")
def doctrine(cards):
    return Doctrine.from_cards(cards)


@pytest.fixture(scope="module")
def provider():
    p = SwissEphemerisDLL()
    yield p
    p.close()


# --- the card store itself ----------------------------------------------------

def test_seven_cards_exist_active_with_the_right_exact_counts(cards):
    by_id = {c.id: c for c in cards if c.id in SEVEN_CARDS}
    assert set(by_id) == set(SEVEN_CARDS)
    for cid, n in N_FOR.items():
        c = by_id[cid]
        assert c.activation == "active"
        assert c.conditions == {"all": [{"seven_graha_sign_count": {"n": n}}]}
        assert c.predicts["domain"] == "yoga"
        assert c.predicts["yoga"] == cid.split(".")[-1]


def test_seven_cards_are_all_mutually_linked_parallel_of(cards):
    by_id = {c.id: c for c in cards if c.id in SEVEN_CARDS}
    for cid, c in by_id.items():
        others = set(SEVEN_CARDS) - {cid}
        assert set(c.raw.get("parallel_of", [])) == others
        assert not c.raw.get("contradicts")
        assert not c.raw.get("extends")


def test_no_two_of_the_seven_share_a_quote(cards):
    """Each item is its own self-contained paragraph -- no shared template
    span the way vv.44-56's house-wise family has (Milestone 8)."""
    by_id = {c.id: c for c in cards if c.id in SEVEN_CARDS}
    hashes = {c.quote_sha256 for c in by_id.values()}
    assert len(hashes) == 7


def test_vallaki_records_its_own_dual_naming_in_the_note(cards):
    vallaki = next(c for c in cards if c.id == "PD.06.Vallaki")
    assert "Veena" in vallaki.quote
    assert "also called Veena Yoga" in vallaki.raw["note"]


def test_seven_grahas_reference_card(cards):
    ref = next(c for c in cards if c.id == "PD.06.SevenGrahas")
    assert ref.activation == "reference"
    assert ref.conditions == {"all": []}
    assert ref.predicts["relation"] == "seven_grahas"
    assert ref.predicts["grahas"] == [
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    assert "Rahu" not in ref.predicts["grahas"]
    assert "Ketu" not in ref.predicts["grahas"]
    # The quote is a strict substring of PD.06.Vallaki's own span, not an
    # invented restatement.
    vallaki = next(c for c in cards if c.id == "PD.06.Vallaki")
    assert ref.quote in vallaki.quote
    assert ref.quote_sha256 != vallaki.quote_sha256


def test_deferred_json_resolves_p168_and_opens_the_new_dependency():
    import json
    registry = json.loads((RULES / "deferred.json").read_text(encoding="utf-8"))
    p168 = next(e for e in registry["entries"]
                if e["id"] == "passage:phaladeepika.06.p168")
    assert p168["status"] == "resolved"

    dep = registry["dependencies"]["dep.seven-graha-sign-count"]
    assert dep["predicate"] == "seven_graha_sign_count"


# --- the doctrine accessor -----------------------------------------------------

def test_doctrine_seven_grahas_reads_from_the_reference_card(cards, doctrine):
    grahas, used = doctrine.seven_grahas()
    assert grahas == ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
    assert used == ("PD.06.SevenGrahas",)


def test_doctrine_seven_grahas_raises_without_the_reference_card():
    """No hardcoded fallback: remove the one card that carries the doctrine
    and the accessor must refuse rather than silently assume Sun-through-
    Saturn from nowhere."""
    empty = Doctrine.from_cards([])
    with pytest.raises(DoctrineError):
        empty.seven_grahas()


# --- the new primitive, in isolation -------------------------------------------

def _count(chart, doctrine) -> tuple[int, dict]:
    rep = DoctrineReport()
    out = _seven_graha_sign_count(chart, doctrine, rep, chart_frame(chart))
    assert len(out) == 1
    f = out[0]
    assert f.predicate == "seven_graha_sign_count"
    return f.args["n"], f.evidence


DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate",
)


@pytest.fixture(scope="module")
def demo_chart(provider):
    return compute_chart(resolve_birth(DEMO, provider), provider)


def _seven_signs(chart, sign_indices: dict[str, int]):
    """The base chart with the seven classical grahas moved to given signs
    (by sign index), everything else -- including Rahu/Ketu -- untouched."""
    for g, idx in sign_indices.items():
        chart = place(chart, g, idx * 30.0 + 15.0)
    return chart


def test_all_seven_in_distinct_signs_counts_seven(demo_chart, doctrine):
    chart = _seven_signs(demo_chart, {
        "Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3,
        "Jupiter": 4, "Venus": 5, "Saturn": 6})
    n, ev = _count(chart, doctrine)
    assert n == 7
    assert sorted(ev["signs"]) == sorted(SIGNS[i] for i in range(7))
    assert ev["doctrine"] == ["PD.06.SevenGrahas"]


def test_all_seven_in_one_sign_counts_one(demo_chart, doctrine):
    chart = _seven_signs(demo_chart, {
        "Sun": 3, "Moon": 3, "Mars": 3, "Mercury": 3,
        "Jupiter": 3, "Venus": 3, "Saturn": 3})
    n, ev = _count(chart, doctrine)
    assert n == 1
    assert ev["signs"] == ["Cancer"]


@pytest.mark.parametrize("n_wanted,placement", [
    (2, {"Sun": 0, "Moon": 0, "Mars": 0, "Mercury": 0, "Jupiter": 0,
         "Venus": 0, "Saturn": 6}),
    (3, {"Sun": 0, "Moon": 0, "Mars": 0, "Mercury": 4, "Jupiter": 4,
         "Venus": 4, "Saturn": 8}),
    (4, {"Sun": 0, "Moon": 0, "Mars": 1, "Mercury": 1, "Jupiter": 2,
         "Venus": 2, "Saturn": 3}),
    (5, {"Sun": 0, "Moon": 0, "Mars": 0, "Mercury": 1, "Jupiter": 2,
         "Venus": 3, "Saturn": 4}),
    (6, {"Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3, "Jupiter": 4,
         "Venus": 5, "Saturn": 5}),
])
def test_every_boundary_count_two_through_six(demo_chart, doctrine, n_wanted, placement):
    chart = _seven_signs(demo_chart, placement)
    n, _ = _count(chart, doctrine)
    assert n == n_wanted


def test_rahu_and_ketu_do_not_affect_the_count(demo_chart, doctrine):
    """The reference card names only the seven; moving the nodes into signs
    none of the seven occupy must not change n."""
    base = _seven_signs(demo_chart, {
        "Sun": 0, "Moon": 0, "Mars": 0, "Mercury": 0, "Jupiter": 0,
        "Venus": 0, "Saturn": 0})
    n_before, _ = _count(base, doctrine)
    moved = place(base, "Rahu", 7 * 30.0 + 15.0)
    moved = place(moved, "Ketu", 8 * 30.0 + 15.0)
    n_after, ev = _count(moved, doctrine)
    assert n_before == n_after == 1
    assert "Rahu" not in ev["grahas"]
    assert "Ketu" not in ev["grahas"]


def test_deterministic(demo_chart, doctrine):
    a, _ = _count(demo_chart, doctrine)
    b, _ = _count(demo_chart, doctrine)
    assert a == b


def test_no_arithmetic_in_the_condition_language(cards):
    """Every one of the seven cards matches a literal n against the fact's
    exact key -- no comparison, threshold or variable arithmetic."""
    for cid in SEVEN_CARDS:
        c = next(x for x in cards if x.id == cid)
        leaf = c.conditions["all"][0]["seven_graha_sign_count"]
        assert isinstance(leaf["n"], int)
        assert not str(leaf["n"]).startswith("?")


# --- rule-card firing: positive, negative, boundary ----------------------------

def test_each_card_fires_only_at_its_own_exact_count(demo_chart, cards, doctrine):
    """Constructing all seven counts on one family of charts and checking
    that only the matching card fires -- the negative case for the other six
    is exercised on every one of these, not just asserted once."""
    placements = {
        1: {"Sun": 2, "Moon": 2, "Mars": 2, "Mercury": 2, "Jupiter": 2, "Venus": 2, "Saturn": 2},
        2: {"Sun": 0, "Moon": 0, "Mars": 0, "Mercury": 0, "Jupiter": 0, "Venus": 0, "Saturn": 6},
        3: {"Sun": 0, "Moon": 0, "Mars": 0, "Mercury": 4, "Jupiter": 4, "Venus": 4, "Saturn": 8},
        4: {"Sun": 0, "Moon": 0, "Mars": 1, "Mercury": 1, "Jupiter": 2, "Venus": 2, "Saturn": 3},
        5: {"Sun": 0, "Moon": 0, "Mars": 0, "Mercury": 1, "Jupiter": 2, "Venus": 3, "Saturn": 4},
        6: {"Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3, "Jupiter": 4, "Venus": 5, "Saturn": 5},
        7: {"Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3, "Jupiter": 4, "Venus": 5, "Saturn": 6},
    }
    name_for = {7: "PD.06.Vallaki", 6: "PD.06.Dharma", 5: "PD.06.Hasha",
                4: "PD.06.Kendra", 3: "PD.06.Shula", 2: "PD.06.Yuga", 1: "PD.06.Gola"}
    for n, placement in placements.items():
        chart = _seven_signs(demo_chart, placement)
        facts = extract_facts(chart, doctrine)
        claims, _ = activate(chart, facts, cards)
        fired = [c for c in claims if c.derived["rule_card"] in SEVEN_CARDS]
        assert len(fired) == 1, (n, [c.derived["rule_card"] for c in fired])
        assert fired[0].derived["rule_card"] == name_for[n]
        assert fired[0].derived["conditions_satisfied"] == [
            f"seven_graha_sign_count({n})"]


def test_exactly_one_of_the_seven_fires_never_zero_never_two(demo_chart, cards, doctrine):
    """The partition property itself, checked directly rather than assumed:
    on an unmodified real chart (no constructed placement at all), exactly
    one of the seven cards fires."""
    facts = extract_facts(demo_chart, doctrine)
    claims, _ = activate(demo_chart, facts, cards)
    fired = [c for c in claims if c.derived["rule_card"] in SEVEN_CARDS]
    assert len(fired) == 1


# --- real charts ----------------------------------------------------------------
#
# Sign occupancy depends only on each body's ecliptic longitude, not on the
# observer's location or the ascendant, so a direct ephemeris sweep (not a
# birth-record sweep) was used first to find the true natural frequency of
# each count before picking real instants: 219,132 daily instants scanned
# across 1800-01-02 to 2399-12-20 (the full range the vendored Swiss
# Ephemeris data file covers) found n=5 most common (43.3%), n=1 rarest
# (4 days in 600 years, 0.0018%) -- and confirmed every one of the seven
# values actually occurs in that range, so none of the seven cards is
# structurally impossible; none needed to be. The four n=1 days found were
# 1821-04-02/03 (Pisces) and 1962-02-04/05 (Capricorn) -- the second is the
# widely reported "Great Conjunction" of February 1962, an independently
# documented historical event, not a coincidence manufactured for this test.
# One real instant per count was then picked from the 1950-2035 window (a
# stable, unambiguous Asia/Kolkata UTC+5:30 era) and confirmed through the
# full birth-record pipeline below, not just the direct ephemeris check.

REAL_CHARTS = {
    "PD.06.Gola":    ("1962-02-04", 1),   # the Feb 1962 Great Conjunction
    "PD.06.Yuga":    ("1955-07-28", 2),
    "PD.06.Shula":   ("1950-01-19", 3),
    "PD.06.Kendra":  ("1950-01-08", 4),
    "PD.06.Hasha":   ("1950-01-01", 5),
    "PD.06.Dharma":  ("1950-03-21", 6),
    "PD.06.Vallaki": ("1950-05-20", 7),
}


@pytest.mark.parametrize("card_id,date_n", REAL_CHARTS.items(),
                          ids=list(REAL_CHARTS))
def test_real_chart_fires_the_matching_card_and_no_other(card_id, date_n):
    date, n = date_n
    rec = BirthRecord(
        date=date, time="12:00", timezone="Asia/Kolkata",
        latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
        time_precision="minute", time_source="memory",
    )
    r = run(rec)
    fired = [c for c in r.claims if c.derived["rule_card"] in SEVEN_CARDS]
    assert len(fired) == 1
    assert fired[0].derived["rule_card"] == card_id
    assert fired[0].derived["conditions_satisfied"] == [
        f"seven_graha_sign_count({n})"]


def test_demo_chart_fires_dharma_via_six_distinct_signs():
    """The project's standing demo nativity (1987-03-14, Thanjavur) happens
    to land on n=6, Dharma -- confirmed from the claim's own
    conditions_satisfied, not assumed. See the 60 -> 61 note in
    test_slice.py::test_slice_runs_and_verifies."""
    r = run(DEMO)
    fired = [c for c in r.claims if c.derived["rule_card"] in SEVEN_CARDS]
    assert len(fired) == 1
    assert fired[0].derived["rule_card"] == "PD.06.Dharma"
    assert fired[0].derived["conditions_satisfied"] == ["seven_graha_sign_count(6)"]
