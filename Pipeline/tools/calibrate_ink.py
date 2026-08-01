"""Detect hallucinated OCR lines, with the threshold calibrated per book.

    python tools/calibrate_ink.py <book_id>

Surya is a vision-language model. Where a scanned page has a blank region backed by
printing on the reverse of thin paper, the faint mirror-image show-through is enough to
make it attempt a read, and it emits fluent invented text. This is the project's worst
failure mode: it reads as real content.

The discriminator is local contrast -- 95th minus 5th percentile grey level -- inside each
reported line box. Real glyphs produce a large spread whichever way round the polarity is;
blank paper carrying only show-through produces almost none.

WHY THE THRESHOLD IS NOT A CONSTANT
-----------------------------------
v1 hardcoded MIN_SPREAD = 30, justified by the separation measured on Brihat Jataka
(real 71-188, hallucinated 3-14). That margin is a property of *that scan* -- its paper,
ink density, scanner gamma and JPEG quality. A darker scan, greyer paper or genuinely
faint print narrows or inverts it, and the failure is invisible in both directions: too
high deletes real text, too low admits fabricated text.

So the threshold is derived from the book's own measurements: find the widest gap in the
observed spread distribution and cut through the middle of it. If the two populations are
not cleanly separated, the run FAILS and asks for a human, rather than guessing.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir
from corpuslib.ids import local_name

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEARCH_LO, SEARCH_HI = 2, 120   # a cut is only plausible inside this band
MIN_MARGIN = 15                 # required width of the empty gap between populations
NO_HALLUC_FLOOR = 45            # if every line is above this, nothing was hallucinated

# Producers that read an image with a model, and can therefore fabricate text. Only
# these need a contrast scan: a producer that extracts an embedded PDF text layer has
# no model in the loop and cannot invent a sentence. Its line boxes are also in PDF
# points rather than image pixels, so measuring them against a rendered page would be
# meaningless even if images existed.
IMAGE_PRODUCERS = {"surya"}


def measure(book_id, pages):
    imgdir = os.path.join(ir.book_dir(ROOT, book_id), "img")
    per_page, spreads = {}, []
    for p in pages:
        path = os.path.join(imgdir, local_name(p["page_id"]) + ".png")
        if not os.path.exists(path):
            raise SystemExit(f"missing page image {path}. Run tools/render_pages.py.")
        a = np.asarray(Image.open(path).convert("L"))
        H, W = a.shape
        rows = []
        for i, l in enumerate(p["lines"]):
            x0, y0, x1, y1 = [int(v) for v in l["bbox"]]
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
            if x1 <= x0 or y1 <= y0:
                rows.append((i, None))          # degenerate box: never real text
                continue
            box = a[y0:y1, x0:x1]
            lo, hi = np.percentile(box, [5, 95])
            s = float(hi - lo)
            rows.append((i, s))
            spreads.append(s)
        per_page[p["page_id"]] = rows
    return per_page, spreads


def calibrate(spreads):
    """Return (threshold, record). Fails loudly if the populations are not separated."""
    vals = sorted(spreads)
    if not vals:
        raise SystemExit("no measurable lines")
    if vals[0] >= NO_HALLUC_FLOOR:
        return 0.0, {"decision": "no-hallucination",
                     "reason": f"lowest observed contrast {vals[0]:.0f} is above the "
                               f"floor {NO_HALLUC_FLOOR}; no blank-region reads present",
                     "min_spread": vals[0], "max_spread": vals[-1]}
    band = [v for v in vals if SEARCH_LO <= v <= SEARCH_HI]
    best = (0.0, None, None)
    for a, b in zip(band, band[1:]):
        if b - a > best[0]:
            best = (b - a, a, b)
    gap, lo, hi = best
    below = [v for v in vals if v <= (lo if lo is not None else -1)]
    if gap < MIN_MARGIN or lo is None:
        raise SystemExit(
            "CALIBRATION FAILED: the contrast distribution is not cleanly bimodal.\n"
            f"  widest gap inside [{SEARCH_LO},{SEARCH_HI}] is {gap:.1f}, "
            f"below the required margin of {MIN_MARGIN}.\n"
            f"  observed range {vals[0]:.0f}..{vals[-1]:.0f}; "
            f"deciles {[round(float(v)) for v in np.percentile(vals, range(0, 101, 10))]}\n"
            "  Refusing to guess a threshold. Inspect the page images: either this book\n"
            "  has no hallucinated lines (raise NO_HALLUC_FLOOR) or its scan contrast\n"
            "  differs enough that the populations overlap and need a human decision.")
    return (lo + hi) / 2.0, {
        "decision": "calibrated",
        "threshold": (lo + hi) / 2.0,
        "gap_lower": lo, "gap_upper": hi, "gap_width": gap,
        "required_margin": MIN_MARGIN,
        "hallucinated_population": {"n": len(below),
                                    "max": max(below) if below else None},
        "real_population": {"n": len(vals) - len(below), "min": hi},
        "min_spread": vals[0], "max_spread": vals[-1],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    a = ap.parse_args()
    pages = ir.load_book(ROOT, a.book_id)

    producers = sorted({p.get("producer", {}).get("name", "?") for p in pages})
    if not (set(producers) & IMAGE_PRODUCERS):
        record = {"decision": "not-applicable",
                  "reason": f"producer(s) {producers} do not read pixels with a model, "
                            f"so blank-region fabrication is impossible; no contrast "
                            f"scan is meaningful",
                  "producers": producers}
        doc = {"schema": 2, "book_id": a.book_id, "calibration": record, "pages": {}}
        path = os.path.join(ir.book_dir(ROOT, a.book_id), "ink_report.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        print(f"producers          : {producers}")
        print(f"decision           : not-applicable ({record['reason']})")
        print(f"-> {path}")
        return

    per_page, spreads = measure(a.book_id, pages)
    threshold, record = calibrate(spreads)

    print(f"lines measured     : {len(spreads)}")
    for k, v in record.items():
        print(f"  {k:<26}: {v}")

    out, total = {}, 0
    fps = {p["page_id"]: p["fingerprint"] for p in pages}
    for pid, rows in per_page.items():
        drop = [i for i, s in rows if s is None or s < threshold]
        if drop:
            out[pid] = {"ocr_fingerprint": fps[pid], "drop": drop, "n": len(rows)}
            total += len(drop)
    doc = {"schema": 2, "book_id": a.book_id, "calibration": record, "pages": out}
    path = os.path.join(ir.book_dir(ROOT, a.book_id), "ink_report.json")
    json.dump(doc, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"\nhallucinated lines : {total} ({total/len(spreads):.1%}) "
          f"across {len(out)} page(s)")
    for pid, e in sorted(out.items(), key=lambda kv: -len(kv[1]["drop"]))[:20]:
        print(f"  {pid}  {len(e['drop']):>3} / {e['n']:<3}")
    print(f"-> {path}")


if __name__ == "__main__":
    main()
