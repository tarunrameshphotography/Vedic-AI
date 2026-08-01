"""Producer: direct PDF text extraction -> IR.

    python producers/pdf_text.py <book_id> <pdf>

For books whose PDF carries a clean digital text layer (Phaladeepika, Saravali), OCR is
both unnecessary and lossy. This emits the *same* intermediate representation as
producers/surya_ocr.py, so normalisation, assembly and verification are shared and cannot
drift into two pipelines with two verification stories.

It deliberately does not "improve" the extracted text. Saravali's PDF has lost the
diacritics on transliterated Sanskrit in its own rendering ("Horā Śāstra" prints as
"Hora Sstr"); per the project rules those are preserved as printed and flagged, never
guessed at.
"""
import argparse
import datetime
import os
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir, profile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def page_lines(page):
    """One IR line per rendered text line, with its bbox, in reading order."""
    out = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            text = "".join(span["text"] for span in line["spans"])
            if not text.strip():
                continue
            bold = any("bold" in span["font"].lower() for span in line["spans"])
            x0, y0, x1, y1 = line["bbox"]
            out.append({"text": f"<b>{text}</b>" if bold else text,
                        "bbox": [round(x0), round(y0), round(x1), round(y1)]})
    out.sort(key=lambda l: (l["bbox"][1], l["bbox"][0]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("pdf")
    a = ap.parse_args()

    prof = profile.load(ROOT, a.book_id)
    if prof.data.get("scan_layout", "single") != "single":
        raise SystemExit(
            f"{a.book_id}: profile declares scan_layout="
            f"{prof.data.get('scan_layout')!r}. Direct text extraction assumes one book "
            f"page per PDF page; a two-up book must go through the OCR producer.")

    doc = fitz.open(a.pdf)
    producer = {"name": "pdf_text", "engine": "pymupdf", "version": fitz.__doc__.strip(),
                "run_date": datetime.date.today().isoformat()}
    empty = []
    for i in range(doc.page_count):
        lines = page_lines(doc[i])
        if not lines:
            empty.append(i + 1)
        ir.write_page(ROOT, a.book_id, i + 1, lines,
                      {"pdf_page": i + 1}, producer)
    print(f"{a.book_id}: {doc.page_count} pages -> {ir.ocr_dir(ROOT, a.book_id)}")
    if empty:
        print(f"WARNING: {len(empty)} page(s) have no text layer and will be empty in "
              f"the corpus: {empty[:20]}{' ...' if len(empty) > 20 else ''}")
        print("         These pages need the OCR producer instead.")


if __name__ == "__main__":
    main()
