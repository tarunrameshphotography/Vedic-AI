"""Render a book's PDF to one image per *book page*, named by sequence.

    python tools/render_pages.py <book_id> <pdf> [--dpi 300]

Scan layout comes from the book's profile. Brihat Jataka is scanned two pages to a sheet
("two-up") and must be split; every other book so far is one page per sheet ("single").
Output is books/<book_id>/img/pNNNN.png, matching the IR page sequence exactly, so no
downstream tool has to know how the book was scanned.
"""
import argparse
import os
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir, profile
from corpuslib.ids import local_name, page_id

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def page_rects(doc, layout, overlap):
    """Yield (seq, pdf_page_index, half, clip_rect) in book-page order."""
    seq = 0
    for i in range(doc.page_count):
        r = doc[i].rect
        if layout == "two-up":
            mid = r.x0 + r.width / 2
            for half, clip in (("a", fitz.Rect(r.x0, r.y0, mid + r.width * overlap, r.y1)),
                               ("b", fitz.Rect(mid - r.width * overlap, r.y0, r.x1, r.y1))):
                seq += 1
                yield seq, i, half, clip
        else:
            seq += 1
            yield seq, i, None, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("pdf")
    ap.add_argument("--dpi", type=int, default=300)
    a = ap.parse_args()

    prof = profile.load(ROOT, a.book_id)
    layout = prof.data.get("scan_layout", "single")
    overlap = prof.data.get("scan_overlap", 0.02)

    outdir = os.path.join(ir.book_dir(ROOT, a.book_id), "img")
    os.makedirs(outdir, exist_ok=True)
    doc = fitz.open(a.pdf)
    n = 0
    for seq, i, half, clip in page_rects(doc, layout, overlap):
        pid = page_id(a.book_id, seq)
        path = os.path.join(outdir, local_name(pid) + ".png")
        n += 1
        if os.path.exists(path):
            continue
        doc[i].get_pixmap(dpi=a.dpi, clip=clip).save(path)
    print(f"{a.book_id}: layout={layout} sheets={doc.page_count} pages={n} -> {outdir}")


if __name__ == "__main__":
    main()
