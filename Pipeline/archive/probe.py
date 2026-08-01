import fitz, os, sys, json
from pathlib import Path

# Resolved from this file's location, so the script runs from any working
# directory and on any machine. Pipeline/archive/ -> repository root.
BOOKS = Path(__file__).resolve().parents[2] / "Books"
rows = []
for fn in sorted(os.listdir(BOOKS)):
    if not fn.lower().endswith(".pdf"):
        continue
    p = os.path.join(BOOKS, fn)
    d = fitz.open(p)
    n = d.page_count
    # sample up to 25 pages spread through the doc
    idxs = sorted(set(int(i * (n - 1) / 24) for i in range(25))) if n > 1 else [0]
    chars = 0
    imgpages = 0
    for i in idxs:
        pg = d[i]
        t = pg.get_text("text").strip()
        chars += len(t)
        if pg.get_images(full=True):
            imgpages += 1
    avg = chars / len(idxs)
    # total text across whole doc (cheap enough)
    total = sum(len(d[i].get_text("text")) for i in range(n))
    meta = d.metadata or {}
    rows.append(dict(file=fn, pages=n, avg_chars_sampled=round(avg),
                     total_chars=total, chars_per_page=round(total / n),
                     img_pages_sampled=f"{imgpages}/{len(idxs)}",
                     producer=meta.get("producer"), title=meta.get("title"),
                     type="TEXT" if avg > 200 else ("SCANNED" if avg < 50 else "MIXED")))
    d.close()

print(json.dumps(rows, indent=2, ensure_ascii=False))
