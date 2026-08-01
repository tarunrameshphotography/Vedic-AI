import fitz, os
from pathlib import Path

# Resolved from this file's location, so the script runs from any working
# directory and on any machine. Pipeline/archive/ -> repository root.
BOOKS = Path(__file__).resolve().parents[2] / "Books"
for fn in sorted(os.listdir(BOOKS)):
    if not fn.lower().endswith(".pdf") or fn.startswith("ae_"):
        continue
    d = fitz.open(os.path.join(BOOKS, fn))
    empty, thin = [], []
    for i in range(d.page_count):
        t = d[i].get_text("text").strip()
        if len(t) == 0:
            empty.append(i + 1)
        elif len(t) < 100:
            thin.append(i + 1)
    print(f"\n{fn}  pages={d.page_count}")
    print(f"   EMPTY ({len(empty)}): {empty}")
    print(f"   THIN<100ch ({len(thin)}): {thin[:60]}")
    d.close()
