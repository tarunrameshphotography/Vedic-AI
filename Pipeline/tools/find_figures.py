"""Locate candidate figure pages (tables and horoscope charts) from the IR geometry.

    python tools/find_figures.py <book_id>

Surya scrambles table cell reading order and reads chart cells as loose words which it
interleaves with the surrounding commentary. Neither is recoverable from OCR, so this
finds the pages that need transcribing by eye into books/<book_id>/verified/.
"""
import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir, profile, sidecar
from corpuslib.normalize import strip_tags

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    a = ap.parse_args()
    prof = profile.load(ROOT, a.book_id)
    band = prof["figure_band_height"]
    narrow_w = prof["figure_narrow_width"]
    pages = ir.load_book(ROOT, a.book_id)
    side = sidecar.load_all(ROOT, a.book_id, pages)
    done = set(side["verified"])
    roles = side["roles"]

    rows = []
    for p in pages:
        pid = p["page_id"]
        if pid in roles:
            continue
        skip = set(side["ink"].get(pid, []))
        lines = [l for i, l in enumerate(p["lines"]) if i not in skip]
        if len(lines) < 4:
            continue
        short = [l for l in lines if len(strip_tags(l["text"]).strip()) <= 14]
        bands = collections.defaultdict(list)
        for l in lines:
            bands[round((l["bbox"][1] + l["bbox"][3]) / 2 / band)].append(l)
        multi = [b for b in bands.values() if len(b) >= 2]
        narrow = sum(1 for l in lines if l["bbox"][2] - l["bbox"][0] < narrow_w)
        rows.append(dict(pid=pid, n=len(lines), short_r=len(short) / len(lines),
                         multi=len(multi), narrow_r=narrow / len(lines)))

    cand = [r for r in rows
            if (r["short_r"] >= 0.30 and r["narrow_r"] >= 0.35) or r["multi"] >= 3]
    cand.sort(key=lambda r: -(r["short_r"] + r["narrow_r"] + r["multi"] / 10))

    print(f"{'page':<24}{'lines':>6}{'short%':>8}{'narrow%':>9}{'multirow':>10}  status")
    print("-" * 68)
    for r in cand:
        print(f"{r['pid']:<24}{r['n']:>6}{r['short_r']:>8.0%}{r['narrow_r']:>9.0%}"
              f"{r['multi']:>10}  {'transcribed' if r['pid'] in done else 'PENDING'}")
    print("-" * 68)
    pending = [r["pid"] for r in cand if r["pid"] not in done]
    print(f"{len(cand)} candidate(s), {len(cand) - len(pending)} transcribed, "
          f"{len(pending)} pending")


if __name__ == "__main__":
    main()
