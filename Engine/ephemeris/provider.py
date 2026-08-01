"""The astronomical backend boundary.

Everything above this module is backend-agnostic. Nothing outside the
`ephemeris` package may import ctypes, name a DLL, or know that the Swiss
Ephemeris exists. Swapping in pyswisseph means writing one new
:class:`EphemerisProvider` subclass and changing nothing else.

Angles are degrees, times are Julian Day (UT), longitudes are sidereal unless a
name says otherwise. East longitude and north latitude are positive.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# Bodies the MVP knows about. Ketu is always derived, never queried.
BODIES = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")

# Ayanamsa identifiers. The engine passes these strings around; only the
# adapter maps them onto whatever the backend calls them.
AYANAMSAS = ("lahiri", "true_chitra", "raman", "krishnamurti", "yukteshwar", "fagan_bradley")

# House systems. Whole sign is the default: the classical sources currently in
# the rule store count houses as whole signs from the lagna. Which sources
# those are is the rule store's business, not this module's.
HOUSE_SYSTEMS = ("whole_sign", "sripati", "equal", "placidus", "koch", "porphyry")


@dataclass(frozen=True)
class BodyPosition:
    """A body's sidereal position at one instant."""

    body: str
    lon: float           # sidereal longitude, 0-360
    lat: float           # ecliptic latitude
    distance_au: float
    speed_lon: float     # degrees/day; negative means retrograde
    speed_lat: float
    speed_dist: float

    @property
    def retrograde(self) -> bool:
        return self.speed_lon < 0.0


@dataclass(frozen=True)
class HousesResult:
    """House cusps and angles, sidereal."""

    system: str
    cusps: tuple[float, ...]     # 12 entries, cusps[0] is the 1st house
    ascendant: float
    midheaven: float
    armc: float
    vertex: float
    equatorial_ascendant: float


@dataclass(frozen=True)
class BackendInfo:
    """Identifies the backend precisely enough to reproduce a chart.

    Recorded verbatim in the ChartBundle, because a chart computed under a
    different ephemeris is a different chart.
    """

    name: str
    library_version: str
    data_source: str             # e.g. "se1:1800-2399" or "moshier"
    data_files: tuple[str, ...] = field(default_factory=tuple)


class EphemerisError(RuntimeError):
    """The backend refused to answer. Never swallowed, never defaulted around."""


class EphemerisProvider(ABC):
    """Minimal astronomical surface required by the MVP.

    Deliberately small. Every method here is needed by Stage 1; nothing is
    exposed speculatively. Adding a capability is a conscious act.
    """

    @property
    @abstractmethod
    def info(self) -> BackendInfo: ...

    @abstractmethod
    def julian_day_ut(self, year: int, month: int, day: int, hour_ut: float) -> float:
        """Gregorian calendar date + decimal UT hour -> Julian Day (UT)."""

    @abstractmethod
    def delta_t(self, jd_ut: float) -> float:
        """TT - UT in seconds."""

    @abstractmethod
    def ayanamsa(self, jd_ut: float, ayanamsa: str) -> float:
        """The ayanamsa value in degrees at this instant."""

    @abstractmethod
    def body_position(self, jd_ut: float, body: str, ayanamsa: str) -> BodyPosition:
        """Sidereal position of one body."""

    @abstractmethod
    def houses(
        self, jd_ut: float, lat: float, lon: float, system: str, ayanamsa: str
    ) -> HousesResult:
        """Sidereal house cusps and angles."""

    def close(self) -> None:
        """Release backend resources. Safe to call more than once."""
