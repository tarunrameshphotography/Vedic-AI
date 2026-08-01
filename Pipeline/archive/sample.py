import fitz, os, sys
from pathlib import Path

# Resolved from this file's location, so the script runs from any working
# directory and on any machine. Pipeline/archive/ -> repository root.
BOOKS = Path(__file__).resolve().parents[2] / "Books"
fn = sys.argv[1]
pages = [int(x) for x in sys.argv[2].split(",")]
d = fitz.open(os.path.join(BOOKS, fn))
for i in pages:
    print(f"\n{'='*70}\n### PAGE {i} (0-idx) of {d.page_count}\n{'='*70}")
    print(d[i].get_text("text"))
