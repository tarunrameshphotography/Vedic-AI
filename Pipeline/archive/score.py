"""Score engine outputs against vision ground truth, split by script."""
import os, re, sys, difflib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

# Both inputs live beside this script and are committed: the gt_*.txt vision
# ground truths, and bench_out/ holding each engine's recorded output. This
# reproduces the scoring behind Reports/ocr_engine_benchmark.md with no
# external state.
SP = Path(__file__).resolve().parent
OUT = SP / "bench_out"
PAGES = ["s002b", "s004a", "s010a", "s010b", "s051b"]
ENGINES = ["surya", "easyocr_hi_en", "winocr", "textlayer_spread"]

DEVA = re.compile(r"[\u0900-\u097F]")
LATIN = re.compile(r"[A-Za-z]")


def norm(s, script):
    s = s.replace("<b>", "").replace("</b>", "")
    s = re.sub(r"</?math>", "", s)
    if script == "deva":
        keep = lambda c: DEVA.match(c)
    else:
        keep = lambda c: LATIN.match(c) or c.isdigit()
    return "".join(c for c in s if keep(c)).lower()


def cer(ref, hyp):
    if not ref:
        return None
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    return round(100 * (1 - sm.ratio()), 1)


print(f"{'engine':<18}{'page':<8}{'Latin+digit err%':>18}{'Devanagari err%':>18}")
print("-" * 62)
totals = {}
for e in ENGINES:
    agg = {"lat": [], "dev": []}
    for p in PAGES:
        gt_f = os.path.join(SP, f"gt_{p}.txt")
        out_f = os.path.join(OUT, f"{e}__{p}.txt")
        if not (os.path.exists(gt_f) and os.path.exists(out_f)):
            continue
        gt = open(gt_f, encoding="utf-8").read()
        hy = "\n".join(open(out_f, encoding="utf-8").read().splitlines()[1:])
        cl = cer(norm(gt, "lat"), norm(hy, "lat"))
        cd = cer(norm(gt, "deva"), norm(hy, "deva"))
        if cl is not None:
            agg["lat"].append(cl)
        if cd is not None:
            agg["dev"].append(cd)
        print(f"{e:<18}{p:<8}{cl if cl is not None else '-':>18}{cd if cd is not None else '-':>18}")
    if agg["lat"]:
        totals[e] = (round(sum(agg['lat']) / len(agg['lat']), 1),
                     round(sum(agg['dev']) / len(agg['dev']), 1) if agg["dev"] else None)
    print()

print("=" * 62)
print(f"{'ENGINE MEAN':<18}{'':<8}{'Latin+digit err%':>18}{'Devanagari err%':>18}")
for e, (l, d) in sorted(totals.items(), key=lambda x: x[1][0]):
    print(f"{e:<18}{'':<8}{l:>18}{d if d is not None else '-':>18}")
