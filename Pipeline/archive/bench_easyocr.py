import easyocr, sys, io, os
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

# Benchmark page image. Pass a path as argv[1], or set VEDIC_BENCH_DIR to a
# directory containing bj/. See run_engines.py for how these were produced.
BENCH = Path(os.environ.get("VEDIC_BENCH_DIR", Path(__file__).resolve().parent))
IMG = sys.argv[1] if len(sys.argv) > 1 else str(BENCH / "bj" / "s051b.png")

for langs in (["en"], ["hi", "en"]):
    print(f"\n{'='*70}\nEasyOCR langs={langs}\n{'='*70}")
    try:
        rd = easyocr.Reader(langs, gpu=False, verbose=False)
        res = rd.readtext(IMG, detail=0, paragraph=True)
        print("\n".join(res))
    except Exception as e:
        print("ERROR:", type(e).__name__, e)
