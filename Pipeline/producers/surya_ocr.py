"""Producer: Surya OCR over a book's rendered page images -> IR.

    python producers/surya_ocr.py <book_id> [--batch 4]

Reads books/<book_id>/img/pNNNN.png and writes books/<book_id>/ocr/pNNNN.json in the
shared intermediate representation. Resumable: pages already written are skipped.

Unlike v1's bulk_ocr.py this records run provenance (engine version, device, date) in
every page, so a corpus can always answer which machine-read layer produced a given line.
"""
import argparse
import datetime
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir
from corpuslib.ids import local_name, page_id

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("--batch", type=int, default=4)
    a = ap.parse_args()

    from surya.detection import DetectionPredictor
    from surya.recognition import RecognitionPredictor
    try:
        from surya import __version__ as surya_version
    except Exception:
        surya_version = "unknown"

    imgdir = os.path.join(ir.book_dir(ROOT, a.book_id), "img")
    ocrdir = ir.ocr_dir(ROOT, a.book_id)
    os.makedirs(ocrdir, exist_ok=True)

    seqs = sorted(int(f[1:-4]) for f in os.listdir(imgdir)
                  if f.startswith("p") and f.endswith(".png"))
    todo = [s for s in seqs
            if not os.path.exists(os.path.join(
                ocrdir, local_name(page_id(a.book_id, s)) + ".json"))]
    print(f"pages={len(seqs)} todo={len(todo)}", flush=True)
    if not todo:
        return

    producer = {
        "name": "surya", "version": surya_version, "task": "ocr_with_boxes",
        "device": os.environ.get("TORCH_DEVICE", "default"),
        "run_date": datetime.date.today().isoformat(),
    }
    rec, det = RecognitionPredictor(), DetectionPredictor()
    for i in range(0, len(todo), a.batch):
        chunk = todo[i:i + a.batch]
        imgs = [Image.open(os.path.join(imgdir, f"p{s:04d}.png")).convert("RGB")
                for s in chunk]
        preds = rec(imgs, ["ocr_with_boxes"] * len(imgs), det, sort_lines=True)
        for s, pr in zip(chunk, preds):
            lines = [{"text": l.text, "bbox": [round(v) for v in l.bbox]}
                     for l in pr.text_lines]
            ir.write_page(ROOT, a.book_id, s, lines,
                          {"image": f"img/p{s:04d}.png"}, producer)
        print(f"  {i + len(chunk)}/{len(todo)}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
