"""Fetch the Swiss Ephemeris binaries the engine needs.

They are not committed. Two reasons: the Swiss Ephemeris is dual-licensed
(AGPL or commercial), so redistributing the compiled library carries
obligations this repository should not silently take on; and the ~3 MB of
binary would be re-downloaded on every clone for no benefit.

Everything fetched here comes from the official upstream repository,
github.com/aloistr/swisseph, and the DLL is checked against the size and
CRC-32 published in that repository's own manifest (windows/swephzip.txt)
before it is written to disk.

    python Engine/vendor/fetch_swisseph.py

Without these files the adapter still runs: it falls back to the built-in
Moshier ephemeris, which needs no data and stays within ~0.1 arcsec of JPL --
far finer than any classical rule resolves. The .se1 files simply make the
default path the real Swiss Ephemeris.
"""

from __future__ import annotations

import io
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent / "swisseph"
RAW = "https://raw.githubusercontent.com/aloistr/swisseph/master/"

# name -> (expected size, expected CRC-32) from windows/swephzip.txt
DLL_MEMBER = "sweph/bin/swedll64.dll"
DLL_SIZE = 999936
DLL_CRC = "5bf1f794"

# 1800-2399: planets, moon, main asteroids. Enough for any human birth chart.
SE1_FILES = ("sepl_18.se1", "semo_18.se1", "seas_18.se1")


def _get(url: str) -> bytes:
    print(f"  fetching {url}")
    with urllib.request.urlopen(url, timeout=300) as r:
        return r.read()


def main() -> int:
    HERE.mkdir(parents=True, exist_ok=True)

    dll = HERE / "swedll64.dll"
    if dll.exists():
        print(f"  {dll.name} already present, skipping")
    else:
        data = _get(RAW + "windows/sweph.zip")
        z = zipfile.ZipFile(io.BytesIO(data))
        info = z.getinfo(DLL_MEMBER)
        crc = format(info.CRC, "08x")
        if info.file_size != DLL_SIZE or crc != DLL_CRC:
            print(
                f"REFUSING TO WRITE: {DLL_MEMBER} is {info.file_size} bytes / CRC {crc}, "
                f"expected {DLL_SIZE} / {DLL_CRC}. Upstream has changed; verify before "
                f"updating the constants in this script.",
                file=sys.stderr,
            )
            return 1
        dll.write_bytes(z.read(DLL_MEMBER))
        print(f"  wrote {dll.name} ({DLL_SIZE} bytes, CRC {crc} verified)")

        try:
            (HERE / "LICENSE").write_bytes(z.read("sweph/src/LICENSE"))
            print("  wrote LICENSE")
        except KeyError:
            print("  warning: LICENSE not found in archive", file=sys.stderr)

    for name in SE1_FILES:
        target = HERE / name
        if target.exists():
            print(f"  {name} already present, skipping")
            continue
        target.write_bytes(_get(RAW + "ephe/" + name))
        print(f"  wrote {name} ({target.stat().st_size} bytes)")

    print("\nDone. Verify with:  python -m pytest Engine/tests -q")
    return 0


if __name__ == "__main__":
    sys.exit(main())
