import sys, os
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

# Benchmark page image. Pass a path as argv[1], or set VEDIC_BENCH_DIR to a
# directory containing bj/. See run_engines.py for how these were produced.
BENCH = Path(os.environ.get("VEDIC_BENCH_DIR", Path(__file__).resolve().parent))
IMG = sys.argv[1] if len(sys.argv) > 1 else str(BENCH / "bj" / "s051b.png")
img = Image.open(IMG).convert("RGB")

from surya.recognition import RecognitionPredictor
rec = RecognitionPredictor()
preds = rec([img], full_page=True)

for p in preds:
    for line in p.text_lines:
        print(line.text)
