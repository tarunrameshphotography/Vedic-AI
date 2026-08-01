"""Bulk Surya OCR over a directory of page images -> one .txt per page.
Resumable: skips pages already written."""
import os, sys, time, json
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

imgdir, outdir = sys.argv[1], sys.argv[2]
batch = int(sys.argv[3]) if len(sys.argv) > 3 else 4
os.makedirs(outdir, exist_ok=True)

pages = sorted(f for f in os.listdir(imgdir) if f.endswith(".png"))
todo = [p for p in pages if not os.path.exists(os.path.join(outdir, p[:-4] + ".txt"))]
print(f"total={len(pages)} todo={len(todo)}", flush=True)

rec, det = RecognitionPredictor(), DetectionPredictor()
t0 = time.time()
for i in range(0, len(todo), batch):
    chunk = todo[i:i + batch]
    imgs = [Image.open(os.path.join(imgdir, c)).convert("RGB") for c in chunk]
    preds = rec(imgs, ["ocr_with_boxes"] * len(imgs), det, sort_lines=True)
    for c, pr in zip(chunk, preds):
        lines = [{"text": l.text, "bbox": [round(v) for v in l.bbox]} for l in pr.text_lines]
        with open(os.path.join(outdir, c[:-4] + ".txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(l["text"] for l in lines))
        with open(os.path.join(outdir, c[:-4] + ".json"), "w", encoding="utf-8") as f:
            json.dump(lines, f, ensure_ascii=False)
    done = i + len(chunk)
    el = time.time() - t0
    print(f"  {done}/{len(todo)}  {el:.0f}s  ({el/done:.1f}s/page)", flush=True)
print("DONE", flush=True)
