"""Run each available OCR engine over the 5 benchmark pages, dump text + timing."""
import os, sys, time, traceback
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent          # Pipeline/archive
ROOT = HERE.parents[1]                          # repository root

# The five benchmark page images (bj/sNNNx.png). They are not in the repository
# -- they are renders of Brihat Jataka spreads, reproducible with
#   python Pipeline/tools/render_pages.py brihat-jataka <pdf>
# Point VEDIC_BENCH_DIR at whatever directory holds bj/.
BENCH = Path(os.environ.get("VEDIC_BENCH_DIR", HERE))
PAGES = ["s002b", "s004a", "s010a", "s010b", "s051b"]
IMGS = {p: str(BENCH / "bj" / (p + ".png")) for p in PAGES}
OUT = HERE / "bench_out"                        # committed: the recorded results
os.makedirs(OUT, exist_ok=True)

engine = sys.argv[1]


def save(name, page, text, secs):
    fn = os.path.join(OUT, f"{name}__{page}.txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(f"### engine={name} page={page} seconds={secs:.1f}\n")
        f.write(text)
    print(f"  {name} {page}: {secs:.1f}s, {len(text)} chars")


if engine == "easyocr":
    import easyocr
    rd = easyocr.Reader(["hi", "en"], gpu=True, verbose=False)
    for p, img in IMGS.items():
        t = time.time()
        res = rd.readtext(img, detail=0, paragraph=True)
        save("easyocr_hi_en", p, "\n".join(res), time.time() - t)

elif engine == "paddle":
    from paddleocr import PaddleOCR
    for lang, tag in (("devanagari", "paddle_deva"), ("en", "paddle_en")):
        try:
            o = PaddleOCR(lang=lang, use_doc_orientation_classify=False,
                          use_doc_unwarping=False, use_textline_orientation=False)
        except Exception as e:
            print(f"  paddle {lang} init failed: {e}")
            continue
        for p, img in IMGS.items():
            t = time.time()
            try:
                r = o.predict(img)
                txt = "\n".join("\n".join(x["rec_texts"]) for x in r)
            except Exception as e:
                txt = f"ERROR {e}"
            save(tag, p, txt, time.time() - t)

elif engine == "surya":
    from PIL import Image
    from surya.recognition import RecognitionPredictor
    from surya.detection import DetectionPredictor
    rec, det = RecognitionPredictor(), DetectionPredictor()
    for p, img in IMGS.items():
        im = Image.open(img).convert("RGB")
        t = time.time()
        preds = rec([im], ["ocr_with_boxes"], det, sort_lines=True)
        txt = "\n".join(l.text for l in preds[0].text_lines)
        save("surya", p, txt, time.time() - t)

elif engine == "winocr":
    import asyncio, winocr
    from PIL import Image
    for p, img in IMGS.items():
        t = time.time()
        r = asyncio.run(winocr.recognize_pil(Image.open(img), "en"))
        save("winocr", p, r.text, time.time() - t)

elif engine == "textlayer":
    import fitz
    d = fitz.open(str(ROOT / "Books" / "Varaha_Mihira_-_Brihat_Jataka.pdf"))
    for p in PAGES:
        spread = int(p[1:4])
        t = time.time()
        save("textlayer_spread", p, d[spread - 1].get_text("text"), time.time() - t)

print("DONE", engine)
