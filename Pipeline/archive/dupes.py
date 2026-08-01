import fitz, os, hashlib, re
from collections import Counter, defaultdict
from pathlib import Path

# Resolved from this file's location, so the script runs from any working
# directory and on any machine. Pipeline/archive/ -> repository root.
BOOKS = Path(__file__).resolve().parents[2] / "Books"
for fn in sorted(os.listdir(BOOKS)):
    if not fn.lower().endswith(".pdf") or fn.startswith("ae_"):
        continue
    d = fitz.open(os.path.join(BOOKS, fn))
    sigs = defaultdict(list)
    for i in range(d.page_count):
        t = re.sub(r"\s+", " ", d[i].get_text("text")).strip()
        if len(t) < 40:
            continue
        sigs[hashlib.md5(t.encode()).hexdigest()].append(i + 1)
    dups = {k: v for k, v in sigs.items() if len(v) > 1}
    # xref identity of page objects (detects page-tree cycles reusing objects)
    xrefs = [d[i].xref for i in range(d.page_count)]
    xdup = {x: [i+1 for i, y in enumerate(xrefs) if y == x] for x in set(xrefs) if xrefs.count(x) > 1}
    print(f"\n=== {fn}  pages={d.page_count}")
    print(f"  duplicate TEXT pages: {len(dups)} groups -> {list(dups.values())[:10]}")
    print(f"  duplicate PAGE OBJECTS (xref): {len(xdup)} -> {list(xdup.values())[:10]}")
    d.close()
