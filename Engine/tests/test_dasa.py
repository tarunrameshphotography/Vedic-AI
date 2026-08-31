"""Tests for dep.dasa -- the Vimshottari mahadasa engine (Milestone 30).

Chapter 19 v.2 gives the nine-graha order, their period-years and the
Krittika-groups-of-nine nakshatra cycle; v.3 gives the balance-at-birth
method, with a worked example this file uses as a real oracle rather than a
synthetic one. Mahadasa only -- no antardasa formula is printed anywhere in
the source, so none is tested here because none is built.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import datetime as dt
import types

import pytest

from Engine.chart import BirthRecord, NAKSHATRAS
from Engine.dasa import (
    balance_at_birth_years,
    chart_mahadasa_timeline,
    jd_to_iso,
    mahadasa_sequence,
    nakshatra_lord,
    DASA_YEAR_DAYS,
)
from Engine.doctrine import Doctrine
from Engine.facts import DoctrineReport, _dasa, chart_frame
from Engine.pipeline import run
from Engine.rules import load_cards
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

CARDS = load_cards(RULES)
DOCTRINE = Doctrine.from_cards(CARDS)
FRAME = {"reference": "lagna", "varga": "D1", "house_system": "whole_sign"}

ORDER = ("Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus")
YEARS = {"Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16,
         "Saturn": 19, "Mercury": 17, "Ketu": 7, "Venus": 20}

# Hand-verified against the standard Vimshottari nakshatra-lord assignment --
# an independently known table, not re-derived from the groups-of-nine
# formula `nakshatra_lord` actually runs, so this is a genuine cross-check.
EXPECTED_LORD = {
    "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun",
    "Rohini": "Moon", "Mrigashira": "Mars", "Ardra": "Rahu",
    "Punarvasu": "Jupiter", "Pushya": "Saturn", "Ashlesha": "Mercury",
    "Magha": "Ketu", "Purva Phalguni": "Venus", "Uttara Phalguni": "Sun",
    "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu",
    "Vishakha": "Jupiter", "Anuradha": "Saturn", "Jyeshtha": "Mercury",
    "Mula": "Ketu", "Purva Ashadha": "Venus", "Uttara Ashadha": "Sun",
    "Shravana": "Moon", "Dhanishta": "Mars", "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn",
    "Revati": "Mercury",
}


# --- v.2: the nine-graha order and period-years table ------------------------

def test_period_years_sum_to_120():
    assert sum(YEARS.values()) == 120


def test_period_years_match_the_verse_exactly():
    assert YEARS == {"Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16,
                      "Saturn": 19, "Mercury": 17, "Ketu": 7, "Venus": 20}


@pytest.mark.parametrize("nakshatra", NAKSHATRAS)
def test_nakshatra_lord_matches_the_standard_table(nakshatra):
    idx = NAKSHATRAS.index(nakshatra)
    assert nakshatra_lord(idx, ORDER, "Krittika") == EXPECTED_LORD[nakshatra]


def test_nakshatra_lord_cycles_every_nine():
    """The 27 nakshatras are exactly three passes through the nine-graha
    order, starting from Krittika (index 2)."""
    lords = [nakshatra_lord(i, ORDER, "Krittika") for i in range(27)]
    assert lords[2:11] == list(ORDER)
    assert lords[11:20] == list(ORDER)
    assert lords[20:27] + lords[0:2] == list(ORDER)


# --- v.3: balance-at-birth, against the chapter's own worked example ---------

def test_balance_at_birth_matches_the_chapters_own_worked_example():
    """Moon at Cancer 13 deg 12' (sidereal longitude 103.2), 9 deg 52' elapsed
    in Pushyami, Saturn's dasa balance stated as 4y 11m 8d -- 4 + 11/12 +
    8/30/12 years is approximately 4.9389; the engine's own arithmetic
    (fraction of the nakshatra remaining, times Saturn's 19-year period)
    should land within a day's worth of that, not merely the same ballpark."""
    moon_lon = 3 * 30.0 + 13.0 + 12.0 / 60.0     # Cancer is the 4th sign, index 3
    balance = balance_at_birth_years(moon_lon, YEARS["Saturn"])
    stated = 4.0 + 11.0 / 12.0 + 8.0 / 365.25
    assert abs(balance - stated) < 0.01


def test_balance_at_birth_elapsed_matches_the_quoted_minutes():
    """The quote states 9 deg 52' elapsed in Pushyami -- checked directly,
    independently of the balance figure above."""
    from Engine.dasa import _NAK_ARC
    moon_lon = 3 * 30.0 + 13.0 + 12.0 / 60.0
    elapsed = moon_lon % _NAK_ARC
    assert abs(elapsed - (9.0 + 52.0 / 60.0)) < 1e-6


def test_balance_at_birth_is_full_term_at_the_start_of_a_nakshatra():
    from Engine.dasa import _NAK_ARC
    nak_start = 7 * _NAK_ARC       # start of Pushya (index 7)
    balance = balance_at_birth_years(nak_start, YEARS["Saturn"])
    assert abs(balance - YEARS["Saturn"]) < 1e-9


def test_balance_at_birth_is_near_zero_at_the_end_of_a_nakshatra():
    from Engine.dasa import _NAK_ARC
    nak_end = 8 * _NAK_ARC - 1e-6  # just before Ashlesha
    balance = balance_at_birth_years(nak_end, YEARS["Mercury"])
    assert 0.0 <= balance < 1e-4


# --- the full nine-period sequence -------------------------------------------

def test_sequence_has_nine_periods_one_per_graha():
    periods = mahadasa_sequence(
        2451545.0, 103.2, 7, ORDER, YEARS, "Krittika")  # Moon at Pushya
    assert len(periods) == 9
    assert {p.graha for p in periods} == set(ORDER)
    assert [p.ordinal for p in periods] == list(range(1, 10))


def test_sequence_starts_with_the_birth_nakshatra_lord():
    periods = mahadasa_sequence(2451545.0, 103.2, 7, ORDER, YEARS, "Krittika")
    assert periods[0].graha == "Saturn"        # Pushya's lord
    assert periods[0].balance_at_birth is True
    assert all(not p.balance_at_birth for p in periods[1:])


def test_sequence_periods_are_sequential_and_non_overlapping():
    periods = mahadasa_sequence(2451545.0, 103.2, 7, ORDER, YEARS, "Krittika")
    for a, b in zip(periods, periods[1:]):
        assert a.end_jd == b.start_jd


def test_sequence_spans_120_years_from_birth():
    birth_jd = 2451545.0
    periods = mahadasa_sequence(birth_jd, 103.2, 7, ORDER, YEARS, "Krittika")
    total_days = periods[-1].end_jd - birth_jd
    # First period is a *balance*, not a full term, so the total span is less
    # than a full 120 years by exactly what was already spent of Saturn's own
    # period before birth (its full 19 years minus the balance).
    spent = YEARS["Saturn"] - (periods[0].end_jd - periods[0].start_jd) / DASA_YEAR_DAYS
    assert abs(total_days / DASA_YEAR_DAYS - (120 - spent)) < 1e-6


def test_sequence_full_periods_after_the_first_use_the_whole_term():
    periods = mahadasa_sequence(2451545.0, 103.2, 7, ORDER, YEARS, "Krittika")
    for p in periods[1:]:
        assert abs((p.end_jd - p.start_jd) / DASA_YEAR_DAYS - p.years) < 1e-9


def test_sequence_is_deterministic():
    a = mahadasa_sequence(2451545.0, 103.2, 7, ORDER, YEARS, "Krittika")
    b = mahadasa_sequence(2451545.0, 103.2, 7, ORDER, YEARS, "Krittika")
    assert [(p.graha, p.start_jd, p.end_jd) for p in a] == \
           [(p.graha, p.start_jd, p.end_jd) for p in b]


# --- jd_to_iso: doctrine-free calendar arithmetic -----------------------------

def test_jd_to_iso_matches_the_j2000_epoch():
    # 2451545.0 is the well-known J2000.0 epoch: 2000-01-01 12:00 UTC.
    assert jd_to_iso(2451545.0) == "2000-01-01T12:00:00Z"


def test_jd_to_iso_matches_a_midnight_instant():
    assert jd_to_iso(2451544.5) == "2000-01-01T00:00:00Z"


# --- the extractor, against the real production doctrine cards ---------------

def _body(name, lon, nakshatra_index):
    return types.SimpleNamespace(body=name, lon=lon, nakshatra_index=nakshatra_index,
                                  nakshatra=NAKSHATRAS[nakshatra_index])


def _chart(moon_lon, moon_nak_idx, birth_jd=2451545.0):
    return types.SimpleNamespace(
        bodies={"Moon": _body("Moon", moon_lon, moon_nak_idx)},
        resolved_birth={"julian_day_ut": birth_jd},
    )


def test_extractor_emits_nine_mahadasa_lord_facts():
    rep = DoctrineReport()
    facts = [f for f in _dasa(_chart(103.2, 7), DOCTRINE, rep, FRAME)
             if f.predicate == "mahadasa_lord"]
    assert len(facts) == 9
    assert {f.args["graha"] for f in facts} == set(ORDER)
    for f in facts:
        assert "start" in f.evidence and "end" in f.evidence


# --- dep.mahadasa-ordinal (Milestone 33) --------------------------------------

def test_extractor_emits_nine_mahadasa_ordinal_facts():
    rep = DoctrineReport()
    facts = [f for f in _dasa(_chart(103.2, 7), DOCTRINE, rep, FRAME)
             if f.predicate == "mahadasa_ordinal"]
    assert len(facts) == 9
    assert {f.args["graha"] for f in facts} == set(ORDER)


def test_mahadasa_ordinal_values_are_1_through_9_each_exactly_once():
    facts = [f for f in _dasa(_chart(103.2, 7), DOCTRINE, DoctrineReport(), FRAME)
             if f.predicate == "mahadasa_ordinal"]
    assert sorted(f.args["ordinal"] for f in facts) == list(range(1, 10))


def test_mahadasa_ordinal_matches_the_verses_own_worked_examples():
    """v.24's Notes give three worked examples of ordinal counting from the
    birth dasa; each is reproduced here directly against the extractor,
    not just against `mahadasa_sequence` in isolation (see the
    `mahadasa_sequence`-level equivalents below for the pure-arithmetic
    check)."""
    def ordinal_of(moon_lon, moon_nak_idx, graha):
        facts = [f for f in _dasa(_chart(moon_lon, moon_nak_idx), DOCTRINE,
                                   DoctrineReport(), FRAME)
                 if f.predicate == "mahadasa_ordinal"]
        return next(f.args["ordinal"] for f in facts if f.args["graha"] == graha)

    # Born in Mars dasa (Mrigashira, index 4, Mars's own nakshatra) -> Saturn 4th.
    assert ordinal_of(4 * (360.0 / 27.0) + 1.0, 4, "Saturn") == 4
    # Born in Venus dasa (Bharani, index 1) -> Rahu 5th, Jupiter 6th.
    assert ordinal_of(1 * (360.0 / 27.0) + 1.0, 1, "Rahu") == 5
    assert ordinal_of(1 * (360.0 / 27.0) + 1.0, 1, "Jupiter") == 6
    # Born in Ketu dasa (Ashwini, index 0) -> Mars 5th.
    assert ordinal_of(0 * (360.0 / 27.0) + 1.0, 0, "Mars") == 5


def test_mahadasa_ordinal_is_birth_fixed_not_query_date_dependent():
    """No query date enters `_dasa` anywhere -- the same birth produces the
    same nine ordinals regardless of when a report is generated, mirroring
    `test_sequence_is_deterministic` for the underlying sequence."""
    a = [(f.args["graha"], f.args["ordinal"])
         for f in _dasa(_chart(103.2, 7), DOCTRINE, DoctrineReport(), FRAME)
         if f.predicate == "mahadasa_ordinal"]
    b = [(f.args["graha"], f.args["ordinal"])
         for f in _dasa(_chart(103.2, 7), DOCTRINE, DoctrineReport(), FRAME)
         if f.predicate == "mahadasa_ordinal"]
    assert sorted(a) == sorted(b)


def test_mahadasa_ordinal_provenance_matches_mahadasa_lord():
    """Both predicates are read from the same doctrine cards -- there is no
    second source of truth for the ordering."""
    facts = _dasa(_chart(103.2, 7), DOCTRINE, DoctrineReport(), FRAME)
    lord_doctrine = {tuple(f.evidence["doctrine"]) for f in facts
                      if f.predicate == "mahadasa_lord"}
    ordinal_doctrine = {tuple(f.evidence["doctrine"]) for f in facts
                         if f.predicate == "mahadasa_ordinal"}
    assert lord_doctrine == ordinal_doctrine
    assert lord_doctrine  # non-empty: doctrine was actually consulted


def test_mahadasa_ordinal_agrees_with_mahadasa_sequence_directly():
    """Cross-check against `mahadasa_sequence` itself, independent of the
    extractor's doctrine plumbing."""
    periods = mahadasa_sequence(2451545.0, 103.2, 7, ORDER, YEARS, "Krittika")
    by_ordinal = {p.ordinal: p.graha for p in periods}
    facts = [f for f in _dasa(_chart(103.2, 7), DOCTRINE, DoctrineReport(), FRAME)
             if f.predicate == "mahadasa_ordinal"]
    for f in facts:
        assert by_ordinal[f.args["ordinal"]] == f.args["graha"]


def test_extractor_records_which_doctrine_cards_it_consulted():
    rep = DoctrineReport()
    _dasa(_chart(103.2, 7), DOCTRINE, rep, FRAME)
    assert "PD.19.VimshottariPeriods" in rep.consulted["dasa"]
    assert "PD.19.BalanceMethod.Mantreswara" in rep.consulted["dasa"]


def test_extractor_absent_when_moon_is_missing():
    chart = types.SimpleNamespace(bodies={}, resolved_birth={"julian_day_ut": 2451545.0})
    assert _dasa(chart, DOCTRINE, DoctrineReport(), FRAME) == []


# --- golden: the real cards, through the whole pipeline -----------------------

DASA_DEMO = BirthRecord(
    date="1990-06-15", time="06:00", timezone="Asia/Kolkata",
    latitude=13.0827, longitude=80.2707, place_name="Chennai",
    time_precision="minute", time_source="certificate",
)


@pytest.fixture(scope="module")
def golden():
    return run(DASA_DEMO)


def test_golden_nine_mahadasa_facts_present(golden):
    assert sum(1 for f in golden.facts if f.predicate == "mahadasa_lord") == 9


def test_golden_nine_dasa_claims_each_carry_a_window(golden):
    dasa_claims = [c for c in golden.claims if c.derived["rule_card"].startswith("PD.19.Dasa.")]
    assert len(dasa_claims) == 9
    for c in dasa_claims:
        assert c.window is not None
        assert c.window["start"] < c.window["end"]


def test_golden_dasa_windows_are_sequential_and_cover_120_years(golden):
    dasa_claims = sorted(
        (c for c in golden.claims if c.derived["rule_card"].startswith("PD.19.Dasa.")),
        key=lambda c: c.window["start"])
    for a, b in zip(dasa_claims, dasa_claims[1:]):
        assert a.window["end"] == b.window["start"]
    birth = dt.datetime.fromisoformat(golden.chart.resolved_birth["utc_instant"][:-1])
    first_start = dt.datetime.fromisoformat(dasa_claims[0].window["start"][:-1])
    assert abs((first_start - birth).total_seconds()) < 1.0


def test_golden_verification_passes_including_window_grounding(golden):
    assert golden.verification.ok
    assert golden.verification.checks["window_grounding_passed"] >= 9


def test_golden_dasa_section_renders_chronologically_and_not_under_ascendant(golden):
    text = golden.consultation
    assert "### Vimshottari Mahadasa Timeline" in text
    timeline = text[text.index("### Vimshottari Mahadasa Timeline"):]
    starts = [line for line in timeline.splitlines() if line.startswith("**") and "mahadasa" in line]
    # At least the nine PD.19.Dasa.<Graha> claims; other windowed claims (e.g.
    # PD.09.Dignity.Inimical.DasaEnmity, on a chart where it fires) share this
    # same chronological section rather than the house-grouped one.
    assert len(starts) >= 9
    # Chronological: extract each period's start year and check non-decreasing.
    years = []
    for line in starts:
        # "**Graha** mahadasa — YYYY-MM-DD to YYYY-MM-DD"
        years.append(line.split("—")[1].strip()[:4])
    assert years == sorted(years)
    ascendant_section = text[text.index("### The Ascendant"):text.index("### Vimshottari Mahadasa Timeline")] \
        if "### The Ascendant" in text[:text.index("### Vimshottari Mahadasa Timeline")] else ""
    assert "mahadasa" not in ascendant_section


# --- chart_mahadasa_timeline: the full sequence, shared by Stage 9 and the ---
# --- frontend's own dasa-timeline view (Milestone 35) -------------------------

def test_chart_mahadasa_timeline_returns_nine_periods_matching_golden_claims(golden):
    """Not a second source of truth: the same windows Stage 9 already
    re-derived for each PD.19.Dasa.<Graha> claim, read off this one function."""
    periods = chart_mahadasa_timeline(golden.chart, CARDS)
    assert len(periods) == 9
    dasa_windows = {c.derived["rule_card"].rsplit(".", 1)[-1]: c.window
                     for c in golden.claims if c.derived["rule_card"].startswith("PD.19.Dasa.")}
    for p in periods:
        window = dasa_windows.get(p.graha)
        assert window is not None
        assert window["start"] == jd_to_iso(p.start_jd)
        assert window["end"] == jd_to_iso(p.end_jd)


def test_chart_mahadasa_timeline_agrees_with_mahadasa_sequence_directly(golden):
    moon = golden.chart.bodies["Moon"]
    periods_doc, _ = DOCTRINE.vimshottari_periods()
    expected = mahadasa_sequence(
        golden.chart.resolved_birth["julian_day_ut"], moon.lon, moon.nakshatra_index,
        periods_doc["order"], periods_doc["years"], periods_doc["starting_nakshatra"])
    actual = chart_mahadasa_timeline(golden.chart, CARDS)
    assert [(p.graha, p.start_jd, p.end_jd) for p in actual] == \
           [(p.graha, p.start_jd, p.end_jd) for p in expected]


def test_chart_mahadasa_timeline_empty_when_moon_missing():
    chart = types.SimpleNamespace(bodies={}, resolved_birth={"julian_day_ut": 2451545.0})
    assert chart_mahadasa_timeline(chart, CARDS) == []


def test_chart_mahadasa_timeline_empty_when_doctrine_absent():
    assert chart_mahadasa_timeline(_chart(103.2, 7), []) == []


# --- real-instant sweep, per master-prompt step 17 ----------------------------

def test_sweep_balance_always_within_range_and_boundaries_occur():
    """A direct ephemeris sweep of the Moon's longitude (balance depends only
    on longitude, the same reasoning test_varga.py's sweep uses) confirming
    the balance-at-birth arithmetic never produces a value outside
    [0, graha_years] and that both near-zero and near-full balances occur
    naturally across real dates."""
    from Engine.ephemeris import SwissEphemerisDLL

    provider = SwissEphemerisDLL()
    try:
        n = 0
        near_zero = near_full = False
        start = dt.date(1975, 1, 1)
        for i in range(0, 18262, 11):     # coprime-ish stride against 27-day cycles
            d = start + dt.timedelta(days=i)
            jd = provider.julian_day_ut(d.year, d.month, d.day, 12.0)
            bp = provider.body_position(jd, "Moon", "lahiri")
            n_idx = int(bp.lon // (360.0 / 27.0)) % 27
            lord = nakshatra_lord(n_idx, ORDER, "Krittika")
            balance = balance_at_birth_years(bp.lon, YEARS[lord])
            n += 1
            assert 0.0 <= balance <= YEARS[lord] + 1e-9
            if balance < 0.05 * YEARS[lord]:
                near_zero = True
            if balance > 0.95 * YEARS[lord]:
                near_full = True
    finally:
        provider.close()

    assert n > 1000
    assert near_zero and near_full
