"""Locate tabular pages from the Surya OCR geometry.

Surya scrambles table cell reading order, so tables can never be trusted from OCR and
must be transcribed by vision. This finds the pages that need that treatment.

A tabular page shows many short line boxes (cells) sharing y-bands across distinct
x-columns, rather than the single wide body column normal prose produces.
"""
import os, sys, json, collections

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import strip_tags

OCRDIR = sys.argv[1]
INK = sys.argv[2] if len(sys.argv) > 2 else None

pages = sorted(p[:-5] for p in os.listdir(OCRDIR) if p.endswith(".json"))
drop = json.load(open(INK, encoding="utf-8")) if INK and os.path.exists(INK) else {}

rows = []
for p in pages:
    lines = json.load(open(os.path.join(OCRDIR, p + ".json"), encoding="utf-8"))
    skip = set(drop.get(p, {}).get("drop", []))
    lines = [l for i, l in enumerate(lines) if i not in skip]
    if len(lines) < 4:
        continue
    short = [l for l in lines if len(strip_tags(l["text"]).strip()) <= 14]
    # group line boxes into y-bands; a band holding >=2 boxes is a table row
    bands = collections.defaultdict(list)
    for l in lines:
        bands[round((l["bbox"][1] + l["bbox"][3]) / 2 / 40)].append(l)
    multi = [b for b in bands.values() if len(b) >= 2]
    widths = [l["bbox"][2] - l["bbox"][0] for l in lines]
    narrow = sum(1 for w in widths if w < 420)
    rows.append(dict(page=p, n=len(lines), short=len(short),
                     short_r=len(short) / len(lines),
                     multi=len(multi), narrow_r=narrow / len(lines)))

cand = [r for r in rows
        if (r["short_r"] >= 0.30 and r["narrow_r"] >= 0.35) or r["multi"] >= 3]
cand.sort(key=lambda r: -(r["short_r"] + r["narrow_r"] + r["multi"] / 10))

print(f"{'page':<8}{'lines':>6}{'short':>7}{'short%':>8}{'narrow%':>9}{'multirow':>10}")
print("-" * 48)
for r in cand:
    print(f"{r['page']:<8}{r['n']:>6}{r['short']:>7}{r['short_r']:>8.0%}"
          f"{r['narrow_r']:>9.0%}{r['multi']:>10}")
print("-" * 48)
print(f"{len(cand)} candidate tabular page(s) of {len(rows)} scanned")
