"""The intermediate representation every producer must emit, and its fingerprint.

One IR file per page. Surya OCR and direct PDF text extraction are both *producers* of
this shape, so everything downstream -- normalisation, assembly, verification -- is
shared and cannot diverge between scanned and digital books.

    {
      "schema": 2,
      "page_id": "brihat-jataka/p0007",
      "book_id": "brihat-jataka",
      "seq": 7,
      "source_ref": {"pdf_page": 4, "half": "a"},   # provenance, never identity
      "producer": {"name": "surya", "version": "0.14.7", ...},
      "lines": [{"text": "...", "bbox": [x0, y0, x1, y1]}, ...]
    }

`fingerprint()` hashes only the `lines` payload -- the thing sidecar files address by
position. Re-running a producer at a different DPI, or with a different model, changes
the fingerprint and every sidecar bound to it fails loudly instead of silently applying
stale line indices to different text.
"""
import hashlib
import json
import os

from .ids import check_book_id, local_name, page_id, parse_page_id

SCHEMA = 2


def fingerprint(lines):
    """Stable sha256 over the line payload. Canonical, key-sorted, no whitespace."""
    canon = json.dumps(
        [{"text": l["text"], "bbox": [int(v) for v in l["bbox"]]} for l in lines],
        ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def ocr_dir(root, book_id):
    return os.path.join(root, "books", check_book_id(book_id), "ocr")


def write_page(root, book_id, seq, lines, source_ref, producer):
    pid = page_id(book_id, seq)
    d = ocr_dir(root, book_id)
    os.makedirs(d, exist_ok=True)
    doc = {
        "schema": SCHEMA,
        "page_id": pid,
        "book_id": book_id,
        "seq": seq,
        "source_ref": source_ref,
        "producer": producer,
        "fingerprint": fingerprint(lines),
        "lines": [{"text": l["text"], "bbox": [int(v) for v in l["bbox"]]}
                  for l in lines],
    }
    with open(os.path.join(d, local_name(pid) + ".json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    return pid


def read_page(root, book_id, seq):
    pid = page_id(book_id, seq)
    path = os.path.join(ocr_dir(root, book_id), local_name(pid) + ".json")
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("schema") != SCHEMA:
        raise ValueError(f"{path}: schema {doc.get('schema')!r}, expected {SCHEMA}")
    if doc.get("page_id") != pid:
        raise ValueError(f"{path}: declares page_id {doc.get('page_id')!r} but is "
                         f"filed as {pid!r}")
    actual = fingerprint(doc["lines"])
    if doc.get("fingerprint") != actual:
        raise ValueError(f"{path}: stored fingerprint {doc.get('fingerprint')!r} does "
                         f"not match its own lines ({actual!r}). The file has been "
                         f"edited by hand or is corrupt.")
    return doc


def load_book(root, book_id):
    """Every page of a book, in sequence. Fails on gaps -- a dense sequence is the
    coverage guarantee that replaces the old spread/half arithmetic."""
    d = ocr_dir(root, book_id)
    seqs = sorted(int(f[1:-5]) for f in os.listdir(d)
                  if f.startswith("p") and f.endswith(".json"))
    if not seqs:
        raise ValueError(f"{d}: no pages")
    missing = [s for s in range(1, seqs[-1] + 1) if s not in set(seqs)]
    if missing:
        raise ValueError(f"{book_id}: page sequence has gaps at {missing}")
    return [read_page(root, book_id, s) for s in seqs]


def book_dir(root, book_id):
    return os.path.join(root, "books", check_book_id(book_id))


def parse(pid):
    return parse_page_id(pid)
