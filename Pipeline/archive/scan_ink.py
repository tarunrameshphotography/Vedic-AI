"""Scan every page for hallucinated OCR lines and write a drop-list.

Surya hallucinates fluent nonsense when it tries to read the faint mirror-image
"show-through" of the reverse of a thin page, and falls into a decoding loop.
See Reports/PROJECT_STATUS.md.

Discriminator is *local contrast* (95th minus 5th percentile grey level) inside the
reported line box. Any real glyph -- dark ink on paper, or the light-on-dark headings
used on the cover blurb pages -- produces a large spread. Blank paper carrying only
show-through produces almost none. Measured on Brihat Jataka: real lines span 71-188,
hallucinated lines 3-14, with no overlap.

Absolute darkness was tried first and rejected: it deletes the genuine light-coloured
"About the Book" / "About the Author" headings, which contain no dark pixels at all.

Emits ink_report.json: {page: {"drop": [line indices], "n": total lines}}
"""
import os, sys, json
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

OCRDIR, IMGDIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
MIN_SPREAD = 30     # p95-p05 grey spread required for a line box to hold real glyphs

pages = sorted(p[:-5] for p in os.listdir(OCRDIR) if p.endswith(".json"))

report, total_lines, total_drop = {}, 0, 0
borderline = []

for page in pages:
    lines = json.load(open(os.path.join(OCRDIR, page + ".json"), encoding="utf-8"))
    total_lines += len(lines)
    if not lines:
        report[page] = dict(drop=[], n=0)
        continue
    a = np.asarray(Image.open(os.path.join(IMGDIR, page + ".png")).convert("L"))
    H, W = a.shape
    drop, stats = [], []
    for i, l in enumerate(lines):
        x0, y0, x1, y1 = [int(v) for v in l["bbox"]]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        if x1 <= x0 or y1 <= y0:
            drop.append(i)
            stats.append((i, -1.0, -1.0))
            continue
        box = a[y0:y1, x0:x1]
        p05, p95 = np.percentile(box, [5, 95])
        spread = float(p95 - p05)
        stats.append((i, spread, float(p05)))
        if spread < MIN_SPREAD:
            drop.append(i)
        elif spread < 60:
            borderline.append((page, i, spread, float(p05), l["text"][:60]))
    report[page] = dict(drop=drop, n=len(lines))
    total_drop += len(drop)

json.dump(report, open(OUT, "w", encoding="utf-8"), indent=1)

affected = {p: r for p, r in report.items() if r["drop"]}
print(f"pages scanned        : {len(pages)}")
print(f"total OCR lines      : {total_lines}")
print(f"hallucinated lines   : {total_drop}  ({total_drop/total_lines:.1%})")
print(f"pages affected       : {len(affected)}")
print()
print("Per-page (dropped / total):")
for p, r in sorted(affected.items(), key=lambda kv: -len(kv[1]["drop"])):
    print(f"  {p}  {len(r['drop']):>3} / {r['n']:<3}")
print()
print(f"BORDERLINE lines (30 <= spread < 60) — need visual check: {len(borderline)}")
for b in borderline[:40]:
    print(f"  {b[0]} #{b[1]}  spread={b[2]:.0f} p05={b[3]:.0f}  | {b[4]}")
