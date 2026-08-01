"""Sidecar files: hallucination drop-lists, corrections, page roles, verified figures.

These four files hold the expensive part of the project -- human judgement about a
specific page. Two invariants are enforced here and nowhere else:

  1. Every entry is keyed by a globally unique `page_id`, so a sidecar can never be
     applied to a different book than the one it was written for.
  2. Every entry carries the `ocr_fingerprint` of the page it was written against.
     The drop-lists and figure specs address OCR lines *by position*; if the producer
     is re-run and the line list changes, those positions mean something different.
     Rather than silently deleting or replacing the wrong text, the build stops.

The original pipeline guarded corrections by an expected-hit count and figure specs by a
bounds check, but the hallucination drop-list -- the mechanism protecting against the
worst failure mode in the project -- had no guard at all.
"""
import json
import os

from .ids import check_book_id, local_name, parse_page_id

SCHEMA = 2


class SidecarError(Exception):
    pass


def _check_book(path, doc, book_id):
    if doc.get("schema") != SCHEMA:
        raise SidecarError(f"{path}: schema {doc.get('schema')!r}, expected {SCHEMA}")
    if doc.get("book_id") != book_id:
        raise SidecarError(f"{path}: declares book_id {doc.get('book_id')!r} but was "
                           f"loaded for {book_id!r}. Refusing to cross books.")


def _check_page(path, pid, book_id, fp, pages):
    got_book, _ = parse_page_id(pid)
    if got_book != book_id:
        raise SidecarError(f"{path}: entry {pid!r} belongs to book {got_book!r}, not "
                           f"{book_id!r}. Refusing to cross books.")
    page = pages.get(pid)
    if page is None:
        raise SidecarError(f"{path}: entry for unknown page {pid!r}")
    if not fp:
        raise SidecarError(f"{path}: entry {pid!r} has no ocr_fingerprint; it cannot be "
                           f"bound to the OCR it was written against")
    if fp != page["fingerprint"]:
        raise SidecarError(
            f"{path}: entry {pid!r} was written against OCR fingerprint {fp[:12]}... "
            f"but the current OCR is {page['fingerprint'][:12]}.... The page has been "
            f"re-produced since this entry was verified, so its line positions are no "
            f"longer meaningful. Re-verify the page and update the entry.")


def load_ink(book_dir, book_id, pages):
    """{page_id: [line indices to drop]} plus the calibration record."""
    path = os.path.join(book_dir, "ink_report.json")
    if not os.path.exists(path):
        raise SidecarError(
            f"{path} missing. The hallucination scan has not been run for this book; "
            f"refusing to build a corpus that may contain fabricated text. "
            f"Run tools/calibrate_ink.py first.")
    doc = json.load(open(path, encoding="utf-8"))
    _check_book(path, doc, book_id)
    out = {}
    for pid, ent in doc.get("pages", {}).items():
        _check_page(path, pid, book_id, ent.get("ocr_fingerprint"), pages)
        drop = ent.get("drop", [])
        n = len(pages[pid]["lines"])
        bad = [i for i in drop if not 0 <= i < n]
        if bad:
            raise SidecarError(f"{path}: {pid} drop indices {bad} out of range (page "
                               f"has {n} lines)")
        out[pid] = drop
    return out, doc.get("calibration", {})


def load_corrections(book_dir, book_id, pages):
    path = os.path.join(book_dir, "corrections.json")
    if not os.path.exists(path):
        return []
    doc = json.load(open(path, encoding="utf-8"))
    _check_book(path, doc, book_id)
    for c in doc.get("corrections", []):
        _check_page(path, c["page_id"], book_id, c.get("ocr_fingerprint"), pages)
        for field in ("find", "replace", "expect", "reason"):
            if field not in c:
                raise SidecarError(f"{path}: correction for {c['page_id']} is missing "
                                   f"{field!r}; every correction must carry its evidence")
    return doc.get("corrections", [])


def load_roles(book_dir, book_id, pages):
    """{page_id: reason} for pages excluded from the corpus."""
    path = os.path.join(book_dir, "page_roles.json")
    if not os.path.exists(path):
        return {}
    doc = json.load(open(path, encoding="utf-8"))
    _check_book(path, doc, book_id)
    out = {}
    for pid, ent in doc.get("exclude", {}).items():
        _check_page(path, pid, book_id, ent.get("ocr_fingerprint"), pages)
        if not ent.get("reason"):
            raise SidecarError(f"{path}: {pid} excluded without a reason")
        out[pid] = ent["reason"]
    return out


def load_verified(book_dir, book_id, pages):
    """{page_id: figure spec} for hand-transcribed tables and charts."""
    d = os.path.join(book_dir, "verified")
    out = {}
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(d, fn)
        spec = json.load(open(path, encoding="utf-8"))
        if spec.get("schema") != SCHEMA:
            raise SidecarError(f"{path}: schema {spec.get('schema')!r}, expected {SCHEMA}")
        pid = spec.get("page_id")
        _check_page(path, pid, book_id, spec.get("ocr_fingerprint"), pages)
        if local_name(pid) + ".json" != fn:
            raise SidecarError(f"{path}: filed as {fn} but declares {pid!r}")
        n = len(pages[pid]["lines"])
        bad = [i for i in spec.get("exclude_lines", []) if not 0 <= i < n]
        if bad:
            raise SidecarError(f"{path}: exclude_lines {bad} out of range (page has "
                               f"{n} lines)")
        anchor = spec.get("insert_after", -1)
        if not -1 <= anchor < n:
            raise SidecarError(f"{path}: insert_after {anchor} out of range")
        if pid in out:
            raise SidecarError(f"{path}: duplicate figure for {pid}")
        out[pid] = spec
    return out


def load_all(root, book_id, pages_list):
    """Load and validate every sidecar for a book. Raises on any inconsistency."""
    check_book_id(book_id)
    book_dir = os.path.join(root, "books", book_id)
    pages = {p["page_id"]: p for p in pages_list}
    ink, calib = load_ink(book_dir, book_id, pages)
    return {
        "ink": ink,
        "calibration": calib,
        "corrections": load_corrections(book_dir, book_id, pages),
        "roles": load_roles(book_dir, book_id, pages),
        "verified": load_verified(book_dir, book_id, pages),
    }
