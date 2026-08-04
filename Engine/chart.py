"""Stages 0 and 1: birth details -> ResolvedBirth -> ChartBundle.

Nothing here interprets anything. It computes, and it refuses to guess: an
ambiguous local time or an unknown zone is an error the caller must resolve,
not something to be silently defaulted.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .ephemeris import BODIES, EphemerisProvider, HousesResult

ENGINE_VERSION = "0.1.0"

SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)

NAKSHATRAS = (
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
)

_NAK_ARC = 360.0 / 27.0          # 13 deg 20'
_PADA_ARC = _NAK_ARC / 4.0       # 3 deg 20'


class BirthDataError(ValueError):
    """The birth details cannot be resolved without a human decision."""


@dataclass(frozen=True)
class BirthRecord:
    """Raw input, as given."""

    date: str                    # "YYYY-MM-DD", proleptic Gregorian
    time: str                    # "HH:MM" or "HH:MM:SS", local clock time
    timezone: str                # IANA id, e.g. "Asia/Kolkata"
    latitude: float              # north positive
    longitude: float             # east positive
    place_name: str = ""
    name: str = ""
    time_precision: str = "minute"   # second|minute|fiveminute|quarterhour|hour|unknown
    time_source: str = "unknown"     # certificate|hospital|family|memory|rectified|unknown
    # Some classical rules are stated for a male nativity and others for a
    # female one, and a few pairs differ in nothing else. Left unknown, such a
    # rule cannot be applied at all -- which is the correct outcome, not a
    # reason to guess.
    sex: str = "unknown"             # male|female|unknown


@dataclass(frozen=True)
class ResolvedBirth:
    """Stage 0 output. Enough to reproduce the chart exactly."""

    record: BirthRecord
    utc_instant: str
    julian_day_ut: float
    utc_offset: str
    offset_source: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class BodyState:
    """One body's placement, with the evidence behind every derived label."""

    body: str
    lon: float
    lat: float
    speed_lon: float
    retrograde: bool
    sign: str
    sign_index: int              # 0-11
    deg_in_sign: float
    nakshatra: str
    nakshatra_index: int         # 0-26
    pada: int                    # 1-4
    house: int                   # whole sign, counted from the lagna


@dataclass(frozen=True)
class ChartBundle:
    """Stage 1 output. Immutable and content-addressed."""

    bundle_id: str
    engine_version: str
    backend: dict
    settings: dict
    resolved_birth: dict
    ascendant: float
    ascendant_sign: str
    ascendant_sign_index: int
    midheaven: float
    houses: dict
    bodies: dict[str, BodyState]
    invariants_checked: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        d = asdict(self)
        d["bodies"] = {k: asdict(v) if not isinstance(v, dict) else v
                       for k, v in self.bodies.items()}
        return d


# --- Stage 0 ----------------------------------------------------------------

def resolve_birth(record: BirthRecord, provider: EphemerisProvider) -> ResolvedBirth:
    """Local clock time -> UTC instant and Julian Day.

    A bare UTC offset is never accepted as input. The offset is derived from the
    IANA zone *for that instant*, so historical rule changes are honoured rather
    than assumed away.
    """
    try:
        tz = ZoneInfo(record.timezone)
    except ZoneInfoNotFoundError as exc:
        raise BirthDataError(f"unknown IANA time zone {record.timezone!r}") from exc

    parts = [int(p) for p in record.time.split(":")]
    while len(parts) < 3:
        parts.append(0)
    hh, mm, ss = parts
    y, mo, d = (int(p) for p in record.date.split("-"))

    naive = datetime(y, mo, d, hh, mm, ss)
    local = naive.replace(tzinfo=tz)

    warnings: list[str] = []

    # Order matters. In a spring-forward gap the two `fold` values *also*
    # disagree about the offset, so testing ambiguity first would report every
    # non-existent time as an ambiguous one. Only the round trip distinguishes
    # them: a time that never occurred cannot survive it.
    utc = local.astimezone(timezone.utc)
    if utc.astimezone(tz).replace(tzinfo=None) != naive:
        raise BirthDataError(
            f"local time {record.date} {record.time} does not exist in "
            f"{record.timezone} (daylight-saving spring-forward gap)."
        )

    # A local time that occurs twice (DST fall-back) round-trips, but carries
    # two different offsets depending on `fold`. We will not pick one.
    if local.utcoffset() != naive.replace(tzinfo=tz, fold=1).utcoffset():
        raise BirthDataError(
            f"local time {record.date} {record.time} occurs twice in "
            f"{record.timezone} (daylight-saving fall-back). Supply the UTC "
            f"offset that applied at birth."
        )

    if record.time_precision in ("hour", "unknown") or record.time_source == "unknown":
        warnings.append(
            f"birth time precision '{record.time_precision}' from source "
            f"'{record.time_source}': ascendant-sensitive conclusions are not reliable"
        )

    off = local.utcoffset() or timedelta(0)
    total = int(off.total_seconds())
    sign = "+" if total >= 0 else "-"
    offset = f"{sign}{abs(total)//3600:02d}:{(abs(total)%3600)//60:02d}"

    hour_ut = utc.hour + utc.minute / 60.0 + utc.second / 3600.0
    jd = provider.julian_day_ut(utc.year, utc.month, utc.day, hour_ut)

    return ResolvedBirth(
        record=record,
        utc_instant=utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        julian_day_ut=jd,
        utc_offset=offset,
        offset_source=f"zoneinfo/{record.timezone}",
        warnings=tuple(warnings),
    )


# --- Stage 1 ----------------------------------------------------------------

def _sign_of(lon: float) -> tuple[int, float]:
    idx = int(lon // 30.0) % 12
    return idx, lon - idx * 30.0


def _nakshatra_of(lon: float) -> tuple[int, int]:
    idx = int(lon // _NAK_ARC) % 27
    pada = int((lon - idx * _NAK_ARC) // _PADA_ARC) + 1
    return idx, min(pada, 4)


def compute_chart(
    resolved: ResolvedBirth,
    provider: EphemerisProvider,
    ayanamsa: str = "lahiri",
    house_system: str = "whole_sign",
) -> ChartBundle:
    """Compute every quantity Stage 2 will turn into facts."""
    jd = resolved.julian_day_ut
    rec = resolved.record

    houses: HousesResult = provider.houses(
        jd, rec.latitude, rec.longitude, house_system, ayanamsa
    )
    asc_sign_index, _ = _sign_of(houses.ascendant)

    bodies: dict[str, BodyState] = {}
    for name in BODIES:
        p = provider.body_position(jd, name, ayanamsa)
        s_idx, deg = _sign_of(p.lon)
        n_idx, pada = _nakshatra_of(p.lon)
        # Whole sign: the lagna's whole sign is the 1st house, so a body's
        # house is simply how many signs it sits from the lagna's sign.
        house = ((s_idx - asc_sign_index) % 12) + 1
        bodies[name] = BodyState(
            body=name,
            lon=p.lon,
            lat=p.lat,
            speed_lon=p.speed_lon,
            retrograde=p.retrograde,
            sign=SIGNS[s_idx],
            sign_index=s_idx,
            deg_in_sign=deg,
            nakshatra=NAKSHATRAS[n_idx],
            nakshatra_index=n_idx,
            pada=pada,
            house=house,
        )

    settings = {
        "ayanamsa": ayanamsa,
        "ayanamsa_value": provider.ayanamsa(jd, ayanamsa),
        "house_system": house_system,
        "node_type": "true",
        # Recorded because the classics do not choose an ayanamsa; we do.
        "unsourced_engine_choices": ["ayanamsa", "node_type"],
    }

    backend = {
        "name": provider.info.name,
        "library_version": provider.info.library_version,
        "data_source": provider.info.data_source,
        "data_files": list(provider.info.data_files),
        "delta_t_seconds": provider.delta_t(jd),
    }

    checks = _check_invariants(bodies, houses, asc_sign_index)

    payload = {
        "engine_version": ENGINE_VERSION,
        "backend": {k: backend[k] for k in ("name", "library_version", "data_source")},
        "settings": settings,
        "jd": jd,
        "lat": rec.latitude,
        "lon": rec.longitude,
    }
    bundle_id = "sha256:" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()

    return ChartBundle(
        bundle_id=bundle_id,
        engine_version=ENGINE_VERSION,
        backend=backend,
        settings=settings,
        resolved_birth={
            "date": rec.date, "time": rec.time, "timezone": rec.timezone,
            "latitude": rec.latitude, "longitude": rec.longitude,
            "place_name": rec.place_name,
            "utc_instant": resolved.utc_instant,
            "julian_day_ut": jd,
            "utc_offset": resolved.utc_offset,
            "offset_source": resolved.offset_source,
            "time_precision": rec.time_precision,
            "time_source": rec.time_source,
            "sex": rec.sex,
            "warnings": list(resolved.warnings),
        },
        ascendant=houses.ascendant,
        ascendant_sign=SIGNS[asc_sign_index],
        ascendant_sign_index=asc_sign_index,
        midheaven=houses.midheaven,
        houses={
            "system": houses.system,
            "cusps": list(houses.cusps),
            "signs": [SIGNS[(asc_sign_index + i) % 12] for i in range(12)],
        },
        bodies=bodies,
        invariants_checked=checks,
    )


def _check_invariants(bodies, houses, asc_sign_index) -> tuple[str, ...]:
    """Fail loudly rather than emit a bundle we could not verify."""
    checked = []

    rahu, ketu = bodies["Rahu"], bodies["Ketu"]
    sep = (ketu.lon - rahu.lon) % 360.0
    assert abs(sep - 180.0) < 1e-6, f"Rahu/Ketu separation is {sep}, expected 180"
    checked.append("nodes_opposed_180")

    for b in bodies.values():
        assert 0.0 <= b.lon < 360.0, f"{b.body} longitude {b.lon} out of range"
        assert 1 <= b.house <= 12, f"{b.body} house {b.house} out of range"
        assert 1 <= b.pada <= 4, f"{b.body} pada {b.pada} out of range"
    checked.append("longitudes_and_houses_in_range")

    assert bodies["Sun"].retrograde is False, "the Sun is never retrograde"
    assert bodies["Moon"].retrograde is False, "the Moon is never retrograde"
    checked.append("sun_moon_never_retrograde")

    # Under whole sign the 1st house must be the ascendant's own sign.
    assert houses.system != "whole_sign" or (
        int(houses.cusps[0] // 30.0) % 12 == asc_sign_index
    ), "whole-sign 1st cusp is not the ascendant's sign"
    checked.append("whole_sign_first_house_is_lagna_sign")

    return tuple(checked)
