"""EphemerisProvider backed by Astrodienst's official swedll64.dll via ctypes.

Only the handful of Swiss Ephemeris entry points the MVP needs are bound. This
is a deliberate floor, not an unfinished wrapper: an unbound function is one
that cannot be called by mistake, and the surface stays small enough to audit.

Replacing this with pyswisseph (once a wheel or a compiler exists) means
implementing EphemerisProvider against the same six methods. No caller changes.
"""

from __future__ import annotations

import ctypes
import os
from ctypes import POINTER, c_char_p, c_double, c_int, c_int32
from pathlib import Path

from .provider import (
    AYANAMSAS,
    HOUSE_SYSTEMS,
    BackendInfo,
    BodyPosition,
    EphemerisError,
    EphemerisProvider,
    HousesResult,
)

_VENDOR = Path(__file__).resolve().parent.parent / "vendor" / "swisseph"

# --- Swiss Ephemeris constants (swephexp.h) ---------------------------------

_SE_GREG_CAL = 1

_PLANET_ID = {
    "Sun": 0, "Moon": 1, "Mercury": 2, "Venus": 3, "Mars": 4,
    "Jupiter": 5, "Saturn": 6, "Rahu": 11,  # 11 = SE_TRUE_NODE
}
_MEAN_NODE = 10

_SEFLG_SWIEPH = 2
_SEFLG_MOSEPH = 4
_SEFLG_SPEED = 256
_SEFLG_SIDEREAL = 64 * 1024

_SIDM = {
    "fagan_bradley": 0,
    "lahiri": 1,
    "raman": 3,
    "krishnamurti": 5,
    "yukteshwar": 7,
    "true_chitra": 27,
}

_HSYS = {
    "whole_sign": b"W", "sripati": b"S", "equal": b"E",
    "placidus": b"P", "koch": b"K", "porphyry": b"O",
}


class SwissEphemerisDLL(EphemerisProvider):
    """Adapter over swedll64.dll.

    Parameters
    ----------
    dll_path:
        Defaults to the vendored DLL.
    ephe_path:
        Directory of .se1 data files. If none are present the backend falls
        back to Moshier, which needs no data and stays within ~0.1 arcsec of
        JPL -- far below the resolution any classical rule operates at. The
        choice is recorded in :attr:`info` either way, never hidden.
    """

    def __init__(self, dll_path: str | os.PathLike | None = None,
                 ephe_path: str | os.PathLike | None = None) -> None:
        dll_path = Path(dll_path) if dll_path else _VENDOR / "swedll64.dll"
        if not dll_path.exists():
            raise EphemerisError(f"Swiss Ephemeris DLL not found at {dll_path}")

        self._lib = ctypes.CDLL(str(dll_path))
        self._bind()

        ephe_path = Path(ephe_path) if ephe_path else _VENDOR
        se1 = sorted(p.name for p in Path(ephe_path).glob("*.se1"))
        if se1:
            self._lib.swe_set_ephe_path(str(ephe_path).encode("utf-8"))
            data_source, data_files = "se1", tuple(se1)
            self._base_flag = _SEFLG_SWIEPH
        else:
            data_source, data_files = "moshier", ()
            self._base_flag = _SEFLG_MOSEPH

        buf = ctypes.create_string_buffer(256)
        self._lib.swe_version(buf)
        self._info = BackendInfo(
            name="swisseph-dll",
            library_version=buf.value.decode("ascii", "replace"),
            data_source=data_source,
            data_files=data_files,
        )
        self._sid_mode: int | None = None
        self._closed = False

    # --- ctypes signatures --------------------------------------------------

    def _bind(self) -> None:
        L = self._lib
        L.swe_version.argtypes = [c_char_p]
        L.swe_version.restype = c_char_p

        L.swe_set_ephe_path.argtypes = [c_char_p]
        L.swe_set_ephe_path.restype = None

        L.swe_julday.argtypes = [c_int, c_int, c_int, c_double, c_int]
        L.swe_julday.restype = c_double

        L.swe_deltat_ex.argtypes = [c_double, c_int32, c_char_p]
        L.swe_deltat_ex.restype = c_double

        L.swe_set_sid_mode.argtypes = [c_int32, c_double, c_double]
        L.swe_set_sid_mode.restype = None

        L.swe_get_ayanamsa_ex_ut.argtypes = [c_double, c_int32, POINTER(c_double), c_char_p]
        L.swe_get_ayanamsa_ex_ut.restype = c_int32

        L.swe_calc_ut.argtypes = [c_double, c_int32, c_int32, POINTER(c_double), c_char_p]
        L.swe_calc_ut.restype = c_int32

        L.swe_houses_ex.argtypes = [
            c_double, c_int32, c_double, c_double, c_int,
            POINTER(c_double), POINTER(c_double),
        ]
        L.swe_houses_ex.restype = c_int

        L.swe_close.argtypes = []
        L.swe_close.restype = None

    # --- helpers ------------------------------------------------------------

    def _apply_sid_mode(self, ayanamsa: str) -> None:
        if ayanamsa not in AYANAMSAS:
            raise EphemerisError(f"unknown ayanamsa {ayanamsa!r}; known: {AYANAMSAS}")
        mode = _SIDM[ayanamsa]
        if mode != self._sid_mode:
            self._lib.swe_set_sid_mode(mode, 0.0, 0.0)
            self._sid_mode = mode

    @staticmethod
    def _err(buf: ctypes.Array) -> str:
        return buf.value.decode("utf-8", "replace").strip()

    # --- EphemerisProvider --------------------------------------------------

    @property
    def info(self) -> BackendInfo:
        return self._info

    def julian_day_ut(self, year: int, month: int, day: int, hour_ut: float) -> float:
        return float(self._lib.swe_julday(year, month, day, hour_ut, _SE_GREG_CAL))

    def delta_t(self, jd_ut: float) -> float:
        err = ctypes.create_string_buffer(256)
        days = float(self._lib.swe_deltat_ex(jd_ut, self._base_flag, err))
        msg = self._err(err)
        if msg:
            raise EphemerisError(f"swe_deltat_ex: {msg}")
        return days * 86400.0

    def ayanamsa(self, jd_ut: float, ayanamsa: str) -> float:
        self._apply_sid_mode(ayanamsa)
        out, err = c_double(), ctypes.create_string_buffer(256)
        rc = self._lib.swe_get_ayanamsa_ex_ut(
            jd_ut, self._base_flag | _SEFLG_SIDEREAL, ctypes.byref(out), err
        )
        if rc < 0:
            raise EphemerisError(f"swe_get_ayanamsa_ex_ut: {self._err(err)}")
        return out.value

    def body_position(self, jd_ut: float, body: str, ayanamsa: str) -> BodyPosition:
        # Ketu is exactly opposite Rahu by definition. Asking the ephemeris for
        # it would be meaningless, so it is derived and labelled as derived.
        if body == "Ketu":
            rahu = self.body_position(jd_ut, "Rahu", ayanamsa)
            return BodyPosition(
                body="Ketu",
                lon=(rahu.lon + 180.0) % 360.0,
                lat=-rahu.lat,
                distance_au=rahu.distance_au,
                speed_lon=rahu.speed_lon,
                speed_lat=-rahu.speed_lat,
                speed_dist=rahu.speed_dist,
            )

        if body not in _PLANET_ID:
            raise EphemerisError(f"unknown body {body!r}")
        self._apply_sid_mode(ayanamsa)

        xx = (c_double * 6)()
        err = ctypes.create_string_buffer(256)
        flags = self._base_flag | _SEFLG_SPEED | _SEFLG_SIDEREAL
        rc = self._lib.swe_calc_ut(jd_ut, _PLANET_ID[body], flags, xx, err)
        if rc < 0:
            raise EphemerisError(f"swe_calc_ut({body}): {self._err(err)}")

        return BodyPosition(
            body=body,
            lon=xx[0] % 360.0,
            lat=xx[1],
            distance_au=xx[2],
            speed_lon=xx[3],
            speed_lat=xx[4],
            speed_dist=xx[5],
        )

    def houses(self, jd_ut: float, lat: float, lon: float,
               system: str, ayanamsa: str) -> HousesResult:
        if system not in HOUSE_SYSTEMS:
            raise EphemerisError(f"unknown house system {system!r}")
        # Cusp-based systems degenerate above the polar circles. Refuse rather
        # than return nonsense; whole sign is always well defined.
        if system in ("placidus", "koch") and abs(lat) > 66.0:
            raise EphemerisError(
                f"{system} is undefined at latitude {lat}; use whole_sign"
            )
        self._apply_sid_mode(ayanamsa)

        cusps = (c_double * 13)()
        ascmc = (c_double * 10)()
        rc = self._lib.swe_houses_ex(
            jd_ut, self._base_flag | _SEFLG_SIDEREAL, lat, lon,
            ord(_HSYS[system]), cusps, ascmc,
        )
        if rc < 0:
            raise EphemerisError(f"swe_houses_ex({system}) failed")

        return HousesResult(
            system=system,
            cusps=tuple(cusps[i] % 360.0 for i in range(1, 13)),
            ascendant=ascmc[0] % 360.0,
            midheaven=ascmc[1] % 360.0,
            armc=ascmc[2] % 360.0,
            vertex=ascmc[3] % 360.0,
            equatorial_ascendant=ascmc[4] % 360.0,
        )

    def close(self) -> None:
        if not self._closed:
            self._lib.swe_close()
            self._closed = True
