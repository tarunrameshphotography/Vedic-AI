"""Vimshottari mahadasa arithmetic (dep.dasa).

Mahadasa only. No antardasa formula is printed anywhere in ch. 19 or ch. 20 --
both chapters state antardasa *effects*, never the sub-division arithmetic --
so building one here would be the engine inventing doctrine the corpus does
not carry. `dep.dasa`'s own effort_basis is "vimshottari balance at birth plus
a timeline, and claims that carry a window"; this module is exactly that and
nothing more.

Two numbers this module uses are not read from a reference card, and are
recorded here rather than smuggled in as literals:

  * Krittika's position in the 27-nakshatra cycle (index 2 of
    `Engine.chart.NAKSHATRAS`) is coordinate bookkeeping -- the same kind of
    fact `SIGNS.index(...)` already supplies elsewhere -- not a claim this
    book makes. Which nakshatra the cycle *starts* from, and which nine
    grahas preside over it in which order, are read from `PD.19.
    VimshottariPeriods` via `Doctrine.vimshottari_periods()`, never
    hardcoded.
  * A dasa-year's length in days. Ch. 19 v. 4 defines it as a solar year (the
    Sun's return to the same position) without printing a day-count, so this
    is calendar arithmetic filling a gap the source leaves numeric, not a
    doctrinal choice -- the same category ch. 1 v. 3's note already assigns
    to "the engine already does what it asks, by a different instrument".
    365.25 days (the Julian year) is used, and is recorded here rather than
    silently assumed.
"""

from __future__ import annotations

from dataclasses import dataclass

from .chart import NAKSHATRAS

DASA_YEAR_DAYS = 365.25

# Matches Engine.chart._NAK_ARC exactly (360/27, one nakshatra's arc) --
# defined here rather than imported across the module boundary because that
# name is private to chart.py. Not re-derived, restated: both are the same
# fixed astronomical constant and cannot drift apart.
_NAK_ARC = 360.0 / 27.0


@dataclass(frozen=True)
class MahadasaPeriod:
    graha: str
    ordinal: int          # 1..9, order the periods run in from birth
    years: float           # this graha's full Vimshottari period length
    start_jd: float
    end_jd: float
    balance_at_birth: bool  # True for the first (birth-nakshatra) period only


def nakshatra_lord(
    nakshatra_index: int, order: tuple[str, ...], starting_nakshatra: str,
) -> str:
    """Which of the nine grahas presides over one nakshatra's dasa.

    Ch. 19 v. 2: "Count the stars from Krittika in groups of nine" -- the
    27 nakshatras cycle through `order` three times, starting the count at
    `starting_nakshatra`. Both `order` and `starting_nakshatra` are the
    card's own words; only the arithmetic connecting them to a 0-26 index is
    the engine's.
    """
    start_idx = NAKSHATRAS.index(starting_nakshatra)
    offset = (nakshatra_index - start_idx) % len(order)
    return order[offset]


def balance_at_birth_years(moon_lon: float, dasa_years: float) -> float:
    """The birth graha's own dasa-years still to run at the moment of birth.

    Ch. 19 v. 3, the degree/longitude method -- "now-a-days the easiest
    method... based on the longitude of the Moon" -- which the translator's
    Notes endorse over the root verse's own division-by-60 shortcut ("this in
    our view is not correct as the total number of ghatikas are not always
    60"). Both are on record in the rule store, two reference cards linked by
    `contradicts`; this is the one the engine computes with.

    The fraction of the birth nakshatra still to elapse, times the ruling
    graha's full period, is the whole of the arithmetic -- verified in
    `Engine/tests/test_dasa.py` against the chapter's own worked example
    (Moon at Cancer 13°20'..., 9°52' elapsed in Pushyami, balance of Saturn's
    dasa = 4y 11m 8d) rather than a synthetic case.
    """
    elapsed = moon_lon % _NAK_ARC
    remaining_fraction = (_NAK_ARC - elapsed) / _NAK_ARC
    return remaining_fraction * dasa_years


def mahadasa_sequence(
    birth_jd: float,
    moon_lon: float,
    moon_nakshatra_index: int,
    order: tuple[str, ...],
    years: dict[str, float],
    starting_nakshatra: str,
) -> list[MahadasaPeriod]:
    """The full nine-period Vimshottari sequence for one birth.

    Every graha gets exactly one period (the 120-year cycle contains each
    graha's period once), starting with the birth nakshatra's lord at its
    balance-at-birth length and continuing through `order`, cycled from
    there. This is a property of the birth moment alone -- not of "now" --
    which is why no query date enters anywhere in this pipeline: a chart's
    mahadasa timeline is as fixed as its planetary placements.
    """
    lord = nakshatra_lord(moon_nakshatra_index, order, starting_nakshatra)
    start_pos = order.index(lord)

    periods: list[MahadasaPeriod] = []
    jd = birth_jd
    for i in range(len(order)):
        graha = order[(start_pos + i) % len(order)]
        full_years = years[graha]
        if i == 0:
            span_years = balance_at_birth_years(moon_lon, full_years)
        else:
            span_years = full_years
        end_jd = jd + span_years * DASA_YEAR_DAYS
        periods.append(MahadasaPeriod(
            graha=graha, ordinal=i + 1, years=full_years,
            start_jd=jd, end_jd=end_jd, balance_at_birth=(i == 0),
        ))
        jd = end_jd
    return periods


def jd_to_iso(jd: float) -> str:
    """Julian Day (UT) -> an ISO-8601 UTC instant string.

    Standard Gregorian-calendar conversion (Fliegel & Van Flandern / Meeus),
    doctrine-free astronomical calendar arithmetic -- the forward direction
    of the same kind of computation `Engine/chart.py::resolve_birth` already
    does backward (calendar -> JD) via the ephemeris provider.
    """
    jd_plus = jd + 0.5
    z = int(jd_plus)
    f = jd_plus - z
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day_frac = b - d - int(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    day = int(day_frac)
    hour_frac = (day_frac - day) * 24.0
    hh = int(hour_frac)
    mm_frac = (hour_frac - hh) * 60.0
    mm = int(mm_frac)
    ss = int(round((mm_frac - mm) * 60.0))
    if ss == 60:
        ss = 0
        mm += 1
    if mm == 60:
        mm = 0
        hh += 1
    return f"{year:04d}-{month:02d}-{day:02d}T{hh:02d}:{mm:02d}:{ss:02d}Z"
