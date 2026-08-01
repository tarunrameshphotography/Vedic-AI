"""Command line entry point for the vertical slice.

    python -m Engine.cli --date 1987-03-14 --time 04:22 --tz Asia/Kolkata \
        --lat 10.7870 --lon 79.1378 --place "Thanjavur, India"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .chart import BirthDataError, BirthRecord
from .pipeline import PipelineError, run


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Vedic chart reading, cited to source.")
    ap.add_argument("--date", required=True, help="YYYY-MM-DD (Gregorian)")
    ap.add_argument("--time", required=True, help="HH:MM[:SS] local clock time")
    ap.add_argument("--tz", required=True, help="IANA zone, e.g. Asia/Kolkata")
    ap.add_argument("--lat", type=float, required=True, help="north positive")
    ap.add_argument("--lon", type=float, required=True, help="east positive")
    ap.add_argument("--place", default="", help="display label only")
    ap.add_argument("--name", default="")
    ap.add_argument("--precision", default="minute",
                    choices=["second", "minute", "fiveminute", "quarterhour",
                             "hour", "unknown"])
    ap.add_argument("--source", default="unknown",
                    choices=["certificate", "hospital", "family", "memory",
                             "rectified", "unknown"])
    ap.add_argument("--ayanamsa", default="lahiri")
    ap.add_argument("--houses", default="whole_sign")
    ap.add_argument("--audit", action="store_true", help="print the audit view too")
    ap.add_argument("--json", type=Path, help="write the full trace here")
    ap.add_argument("--out", type=Path, help="write the consultation here")
    args = ap.parse_args(argv)

    # The report contains degree signs, em-dashes and Devanagari. A console
    # that cannot encode them must not be able to kill the run.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass

    record = BirthRecord(
        date=args.date, time=args.time, timezone=args.tz,
        latitude=args.lat, longitude=args.lon,
        place_name=args.place, name=args.name,
        time_precision=args.precision, time_source=args.source,
    )

    try:
        result = run(record, ayanamsa=args.ayanamsa, house_system=args.houses)
    except (BirthDataError, PipelineError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(result.consultation)
    if args.audit:
        print("\n\n" + result.audit)
    if args.out:
        args.out.write_text(result.consultation, encoding="utf-8")
        print(f"\n[consultation written to {args.out}]", file=sys.stderr)
    if args.json:
        trace = {
            "chart": result.chart.to_dict(),
            "facts": [
                {"key": f.key, "frame": f.frame, "evidence": f.evidence,
                 "stability": f.stability}
                for f in result.facts
            ],
            "claims": [
                {"claim_id": c.claim_id, "astronomical": c.astronomical,
                 "derived": c.derived, "source": c.source, "passage": c.passage,
                 "weight": c.weight, "tier": c.tier}
                for c in result.claims
            ],
            "coverage": result.coverage,
            "verification": {
                "ok": result.verification.ok,
                "checks": result.verification.checks,
                "failures": result.verification.failures,
            },
        }
        args.json.write_text(json.dumps(trace, indent=2, ensure_ascii=False, default=str),
                             encoding="utf-8")
        print(f"[trace written to {args.json}]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
