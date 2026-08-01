"""Regression suite for the Corpus Pipeline v1.0 architectural guarantees.

    python tests/test_pipeline.py            (or: python -m unittest discover tests)

This is not exhaustive coverage. Every test here exists to protect one invariant that
was expensive to establish and would fail *silently* if broken:

  * page identities are globally unique and layout-independent
  * a sidecar can never be applied to the book it was not written for
  * a sidecar can never be applied to OCR it was not verified against
  * the hallucination threshold is derived per book, and refuses to guess
  * the verse audit still detects gaps, duplicates and reordering
  * the assembler is deterministic, and still reproduces the pre-migration corpus

Most tests build synthetic corpora in a temp directory and run in milliseconds. The two
that exercise the real Brihat Jataka data are marked slow and skip cleanly if it is
absent.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from corpuslib import ids, ir, sidecar                      # noqa: E402
from corpuslib.ids import IdError                           # noqa: E402
from corpuslib.sidecar import SidecarError                  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


calibrate_ink = _load("calibrate_ink", "tools/calibrate_ink.py")
verse_audit = _load("verse_audit", "tools/verse_audit.py")
build_book = _load("build_book", "tools/build_book.py")

BOOK = "brihat-jataka"

# Pinned hash of the un-anchored Brihat Jataka corpus. This guards against silent drift:
# any change to the assembler, the normaliser or a sidecar must move this hash
# deliberately, never by accident.
#
# History:
#   ef9b9b7db3bc07c631f9ed08de8fd5acf107fcc82d8eee9310f5612cb61fe8fb
#       the corpus as it stood immediately before the v2 architecture migration. The
#       migration reproduced it byte for byte -- see PHASE1_MIGRATION_REPORT.md 3.1 --
#       which is what proved the restructuring changed no content.
#   1051ba7b8a37a155bce017aa5e0a2ec607afa452d767d84bf6db2460f7df0a13
#       2026-08-01: seven hand-verified figures added (p0016 p0017 p0020 p0022 p0129
#       p0172 p0200), replacing OCR-scrambled tables and charts. An intended change.
#   51f29771fdbee5a1120d6e12d6dc1b07677057f88e0a122ba2dc3433a0c8e99d
#       2026-08-01: two Devanagari glyph corrections from the sample verification pass
#       (p0141 tha->dha, p0102 cha->ya-conjunct), each verified against the page image.
GOLDEN_SHA = "51f29771fdbee5a1120d6e12d6dc1b07677057f88e0a122ba2dc3433a0c8e99d"

LINES = [{"text": "alpha", "bbox": [1, 2, 3, 4]},
         {"text": "beta", "bbox": [5, 6, 7, 8]},
         {"text": "gamma", "bbox": [9, 10, 11, 12]}]


class SyntheticCorpus:
    """A throwaway corpus root with two books, used by most tests."""

    def __enter__(self):
        self.root = tempfile.mkdtemp(prefix="corpus-test-")
        for seq in (1, 2, 3):
            ir.write_page(self.root, "book-a", seq, LINES, {}, {"name": "test"})
        ir.write_page(self.root, "book-b", 1, LINES, {}, {"name": "test"})
        self.fp = ir.fingerprint(LINES)
        self.pages_a = ir.load_book(self.root, "book-a")
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, name, doc, book="book-a"):
        with open(os.path.join(self.root, "books", book, name), "w",
                  encoding="utf-8") as f:
            json.dump(doc, f)

    def ink(self, pages):
        self.write("ink_report.json", {"schema": 2, "book_id": "book-a",
                                       "calibration": {}, "pages": pages})

    def load(self):
        return sidecar.load_all(self.root, "book-a", self.pages_a)


# ---------------------------------------------------------------------------------
# 1. Globally unique, layout-independent page identity
# ---------------------------------------------------------------------------------
class TestPageIdentity(unittest.TestCase):

    def test_page_ids_are_book_qualified(self):
        self.assertEqual(ids.page_id("brihat-jataka", 43), "brihat-jataka/p0043")
        self.assertEqual(ids.parse_page_id("brihat-jataka/p0043"),
                         ("brihat-jataka", 43))

    def test_same_sequence_in_two_books_is_two_identities(self):
        self.assertNotEqual(ids.page_id("book-a", 1), ids.page_id("book-b", 1))

    def test_v1_book_local_ids_are_rejected(self):
        for bad in ("s001a", "s115b", "p0001", "", None):
            with self.assertRaises(IdError):
                ids.parse_page_id(bad)

    def test_page_id_carries_no_scan_layout(self):
        """A two-up book and a single-page book must produce indistinguishable ids."""
        self.assertEqual(ids.page_id("two-up-book", 7), "two-up-book/p0007")
        self.assertEqual(ids.page_id("single-book", 7), "single-book/p0007")

    def test_malformed_book_ids_rejected(self):
        for bad in ("Brihat Jataka", "brihat_jataka", "-x", "UPPER", ""):
            with self.assertRaises(IdError):
                ids.check_book_id(bad)


# ---------------------------------------------------------------------------------
# 2. Cross-book contamination
# ---------------------------------------------------------------------------------
class TestCrossBookIsolation(unittest.TestCase):

    def test_sidecar_naming_another_books_page_is_rejected(self):
        with SyntheticCorpus() as c:
            c.ink({"book-b/p0001": {"ocr_fingerprint": c.fp, "drop": [0], "n": 3}})
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("Refusing to cross books", str(e.exception))

    def test_sidecar_declaring_wrong_book_id_is_rejected(self):
        with SyntheticCorpus() as c:
            c.write("ink_report.json", {"schema": 2, "book_id": "book-b",
                                        "calibration": {}, "pages": {}})
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("Refusing to cross books", str(e.exception))

    def test_verified_figure_from_another_book_is_rejected(self):
        with SyntheticCorpus() as c:
            c.ink({})
            d = os.path.join(c.root, "books", "book-a", "verified")
            os.makedirs(d)
            with open(os.path.join(d, "p0001.json"), "w", encoding="utf-8") as f:
                json.dump({"schema": 2, "page_id": "book-b/p0001",
                           "ocr_fingerprint": c.fp, "exclude_lines": [],
                           "insert_after": 0, "markdown": "x"}, f)
            with self.assertRaises(SidecarError):
                c.load()

    def test_identical_page_content_in_two_books_stays_distinct(self):
        """book-a/p0001 and book-b/p0001 have byte-identical lines and therefore the
        same fingerprint. Identity must still separate them."""
        with SyntheticCorpus() as c:
            a = ir.read_page(c.root, "book-a", 1)
            b = ir.read_page(c.root, "book-b", 1)
            self.assertEqual(a["fingerprint"], b["fingerprint"])
            self.assertNotEqual(a["page_id"], b["page_id"])
            c.ink({"book-b/p0001": {"ocr_fingerprint": c.fp, "drop": [0], "n": 3}})
            with self.assertRaises(SidecarError):
                c.load()          # matching fingerprint must NOT excuse the wrong book


# ---------------------------------------------------------------------------------
# 3. Fingerprint binding
# ---------------------------------------------------------------------------------
class TestFingerprintBinding(unittest.TestCase):

    def test_stale_fingerprint_is_rejected(self):
        with SyntheticCorpus() as c:
            c.ink({"book-a/p0001": {"ocr_fingerprint": "0" * 64, "drop": [0], "n": 3}})
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("no longer meaningful", str(e.exception))

    def test_missing_fingerprint_is_rejected(self):
        with SyntheticCorpus() as c:
            c.ink({"book-a/p0001": {"drop": [0], "n": 3}})
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("cannot be bound", str(e.exception))

    def test_hand_edited_ir_page_is_detected(self):
        with SyntheticCorpus() as c:
            p = os.path.join(c.root, "books", "book-a", "ocr", "p0001.json")
            doc = json.load(open(p, encoding="utf-8"))
            doc["lines"][0]["text"] = "tampered"
            json.dump(doc, open(p, "w", encoding="utf-8"))
            with self.assertRaises(ValueError) as e:
                ir.read_page(c.root, "book-a", 1)
            self.assertIn("edited by hand", str(e.exception))

    def test_fingerprint_is_content_addressed_not_positional(self):
        reordered = list(reversed(LINES))
        self.assertNotEqual(ir.fingerprint(LINES), ir.fingerprint(reordered))
        self.assertEqual(ir.fingerprint(LINES), ir.fingerprint(list(LINES)))

    def test_bbox_change_alone_changes_fingerprint(self):
        moved = [dict(l) for l in LINES]
        moved[0]["bbox"] = [99, 2, 3, 4]
        self.assertNotEqual(ir.fingerprint(LINES), ir.fingerprint(moved))

    def test_missing_ink_report_refuses_to_build(self):
        with SyntheticCorpus() as c:
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("fabricated text", str(e.exception))


# ---------------------------------------------------------------------------------
# 4. Out-of-range line references
# ---------------------------------------------------------------------------------
class TestRangeChecks(unittest.TestCase):

    def test_out_of_range_drop_index_fails(self):
        with SyntheticCorpus() as c:
            c.ink({"book-a/p0001": {"ocr_fingerprint": c.fp, "drop": [99], "n": 3}})
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("out of range", str(e.exception))

    def test_negative_drop_index_fails(self):
        with SyntheticCorpus() as c:
            c.ink({"book-a/p0001": {"ocr_fingerprint": c.fp, "drop": [-1], "n": 3}})
            with self.assertRaises(SidecarError):
                c.load()

    def _figure(self, c, **over):
        c.ink({})
        d = os.path.join(c.root, "books", "book-a", "verified")
        os.makedirs(d, exist_ok=True)
        spec = {"schema": 2, "page_id": "book-a/p0001", "ocr_fingerprint": c.fp,
                "exclude_lines": [0], "insert_after": 0, "markdown": "x"}
        spec.update(over)
        with open(os.path.join(d, "p0001.json"), "w", encoding="utf-8") as f:
            json.dump(spec, f)

    def test_figure_exclude_lines_out_of_range_fails(self):
        with SyntheticCorpus() as c:
            self._figure(c, exclude_lines=[0, 77])
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("out of range", str(e.exception))

    def test_figure_insert_anchor_out_of_range_fails(self):
        with SyntheticCorpus() as c:
            self._figure(c, insert_after=50)
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("insert_after", str(e.exception))

    def test_figure_filed_under_wrong_name_fails(self):
        with SyntheticCorpus() as c:
            c.ink({})
            d = os.path.join(c.root, "books", "book-a", "verified")
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "p0003.json"), "w", encoding="utf-8") as f:
                json.dump({"schema": 2, "page_id": "book-a/p0001",
                           "ocr_fingerprint": c.fp, "exclude_lines": [],
                           "insert_after": 0, "markdown": "x"}, f)
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("filed as", str(e.exception))

    def test_correction_without_evidence_fails(self):
        with SyntheticCorpus() as c:
            c.ink({})
            c.write("corrections.json", {"schema": 2, "book_id": "book-a",
                    "corrections": [{"page_id": "book-a/p0001",
                                     "ocr_fingerprint": c.fp,
                                     "find": "a", "replace": "b", "expect": 1}]})
            with self.assertRaises(SidecarError) as e:
                c.load()
            self.assertIn("evidence", str(e.exception))


# ---------------------------------------------------------------------------------
# 5. Hallucination calibration
# ---------------------------------------------------------------------------------
class TestCalibration(unittest.TestCase):

    def test_bimodal_distribution_cuts_through_the_gap(self):
        spreads = [3, 5, 8, 12, 14] + [71, 90, 120, 150, 188]
        threshold, rec = calibrate_ink.calibrate(spreads)
        self.assertEqual(rec["decision"], "calibrated")
        self.assertTrue(14 < threshold < 71, threshold)
        self.assertEqual(rec["hallucinated_population"]["n"], 5)
        self.assertEqual(rec["real_population"]["n"], 5)

    def test_brihat_jataka_calibration_is_reproducible(self):
        """The real book's populations must keep yielding a threshold that separates
        them; the exact value may move, the classification must not."""
        spreads = [2, 4, 6, 25] * 30 + [62, 80, 140, 235] * 500
        threshold, rec = calibrate_ink.calibrate(spreads)
        self.assertTrue(25 < threshold < 62, threshold)
        self.assertEqual(rec["hallucinated_population"]["max"], 25)
        self.assertEqual(rec["real_population"]["min"], 62)

    def test_book_with_no_hallucination_drops_nothing(self):
        threshold, rec = calibrate_ink.calibrate([80, 95, 120, 160, 200])
        self.assertEqual(rec["decision"], "no-hallucination")
        self.assertEqual(threshold, 0.0)

    def test_overlapping_populations_refuse_to_guess(self):
        """A scan whose faint print overlaps the show-through must stop, not guess."""
        spreads = list(range(5, 100, 2))          # smooth, no gap anywhere
        with self.assertRaises(SystemExit) as e:
            calibrate_ink.calibrate(spreads)
        self.assertIn("CALIBRATION FAILED", str(e.exception))

    def test_margin_just_below_threshold_fails(self):
        spreads = [10] * 20 + [10 + calibrate_ink.MIN_MARGIN - 1] * 20
        with self.assertRaises(SystemExit):
            calibrate_ink.calibrate(spreads)

    def test_margin_just_above_threshold_passes(self):
        spreads = [10] * 20 + [10 + calibrate_ink.MIN_MARGIN + 1] * 20
        threshold, rec = calibrate_ink.calibrate(spreads)
        self.assertEqual(rec["decision"], "calibrated")


# ---------------------------------------------------------------------------------
# 6. Verse audit
# ---------------------------------------------------------------------------------
def _md(chapter, *verse_lines):
    body = "\n\n".join(verse_lines)
    return f"# T\n\n## Chapter {chapter} — क\n\n{body}\n"


class TestVerseAudit(unittest.TestCase):

    def test_clean_sequence_passes(self):
        md = _md(1, "> एक ।। 1 ।।", "> दो ।। 2 ।।", "> तीन ।। 3 ।।")
        self.assertEqual(verse_audit.audit(md), {1: [1, 2, 3]})

    def test_gap_is_detected(self):
        md = _md(1, "> एक ।। 1 ।।", "> तीन ।। 3 ।।")
        nums = verse_audit.audit(md)[1]
        self.assertEqual([n for n in range(1, max(nums) + 1) if n not in nums], [2])

    def test_duplicate_is_detected(self):
        md = _md(1, "> एक ।। 1 ।।", "> दो ।। 2 ।।", "> फिर ।। 2 ।।")
        self.assertEqual(verse_audit.audit(md)[1], [1, 2, 2])

    def test_ordering_error_is_detected(self):
        nums = verse_audit.audit(_md(1, "> a ।। 3 ।।", "> b ।। 1 ।।", "> c ।। 2 ।।"))[1]
        self.assertNotEqual(nums, sorted(nums))

    def test_colophon_chapter_number_is_not_counted_as_a_verse(self):
        """The bug that made 27 of 28 chapters look broken."""
        md = _md(22, "> एक ।। 1 ।।",
                 "*इति श्रीवराहमिहिरकृते बृहज्जातके प्रकीर्णाध्यायो द्वाविंशः ।। 22 ।।*")
        self.assertEqual(verse_audit.audit(md)[22], [1])

    def test_open_terminator_accepted(self):
        """Ch27 v28 is printed with no closing danda in the source itself."""
        self.assertEqual(verse_audit.audit(_md(27, "> क ।। 28"))[27], [28])

    def test_page_anchors_are_ignored(self):
        md = _md(1, "<!-- page x/p0001 -->", "> एक ।। 1 ।।", "> दो ।। 2 ।।")
        self.assertEqual(verse_audit.audit(md)[1], [1, 2])


# ---------------------------------------------------------------------------------
# 7. Page coverage, both scan layouts
# ---------------------------------------------------------------------------------
class TestPageCoverage(unittest.TestCase):

    def _book(self, root, book, n):
        for seq in range(1, n + 1):
            ir.write_page(root, book, seq, LINES, {}, {"name": "t"})

    def test_single_page_book_dense_sequence_loads(self):
        root = tempfile.mkdtemp()
        try:
            self._book(root, "single-book", 5)
            self.assertEqual(len(ir.load_book(root, "single-book")), 5)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_two_up_book_dense_sequence_loads(self):
        """A two-up book yields 2 pages per sheet; coverage must not care."""
        root = tempfile.mkdtemp()
        try:
            self._book(root, "twoup-book", 6)      # 3 sheets x 2 halves
            pages = ir.load_book(root, "twoup-book")
            self.assertEqual(len(pages), 6)
            self.assertEqual(pages[-1]["page_id"], "twoup-book/p0006")
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_gap_in_sequence_is_detected(self):
        root = tempfile.mkdtemp()
        try:
            self._book(root, "gappy", 4)
            os.remove(os.path.join(root, "books", "gappy", "ocr", "p0003.json"))
            with self.assertRaises(ValueError) as e:
                ir.load_book(root, "gappy")
            self.assertIn("gaps at [3]", str(e.exception))
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_missing_final_page_is_invisible_and_is_a_known_limitation(self):
        """A dense sequence cannot detect a truncated tail. Documented in
        Reports/PIPELINE_v1.0.md; page count is checked against the PDF separately."""
        root = tempfile.mkdtemp()
        try:
            self._book(root, "short", 4)
            os.remove(os.path.join(root, "books", "short", "ocr", "p0004.json"))
            self.assertEqual(len(ir.load_book(root, "short")), 3)
        finally:
            shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------------
# 8. Real-corpus regressions (slow; skip if the book is absent)
# ---------------------------------------------------------------------------------
_HAVE_BOOK = os.path.isdir(os.path.join(ROOT, "books", BOOK, "ocr"))


@unittest.skipUnless(_HAVE_BOOK, f"{BOOK} not present")
class TestRealCorpus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="corpus-golden-")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _build(self, name, anchors):
        path = os.path.join(self.tmp, name)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            build_book.build(BOOK, path, anchors=anchors)
        with open(path, "rb") as f:
            return f.read()

    def test_corpus_output_matches_its_pinned_hash(self):
        """The assembled corpus must not change except when someone means it to."""
        data = self._build("plain.md", anchors=False)
        self.assertEqual(hashlib.sha256(data).hexdigest(), GOLDEN_SHA)

    def test_build_is_deterministic(self):
        a = self._build("d1.md", anchors=True)
        b = self._build("d2.md", anchors=True)
        self.assertEqual(hashlib.sha256(a).hexdigest(),
                         hashlib.sha256(b).hexdigest())

    def test_anchors_are_the_only_difference(self):
        """Removing the anchor lines and re-collapsing blank runs must reproduce the
        un-anchored corpus exactly. Line endings are normalised on both sides: the
        corpus is written in text mode and so carries CRLF on Windows (a property of
        the pre-migration baseline too, preserved deliberately for byte-identity)."""
        import re

        def norm(b):
            return b.decode("utf-8").replace("\r\n", "\n")

        anchored = norm(self._build("a.md", anchors=True))
        plain = norm(self._build("p.md", anchors=False))
        stripped = "\n".join(l for l in anchored.split("\n")
                             if not re.fullmatch(r"<!-- page \S+ -->", l))
        self.assertEqual(re.sub(r"\n{3,}", "\n\n", stripped), plain)

    def test_every_content_page_is_anchored_and_none_are_foreign(self):
        import re
        md = self._build("a2.md", anchors=True).decode("utf-8")
        anchors = re.findall(r"^<!-- page (\S+) -->$", md, re.M)
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertTrue(all(a.startswith(BOOK + "/") for a in anchors))

    def test_all_sidecars_validate_against_current_ocr(self):
        pages = ir.load_book(ROOT, BOOK)
        side = sidecar.load_all(ROOT, BOOK, pages)     # raises on any drift
        self.assertEqual(side["calibration"]["decision"], "calibrated")
        self.assertEqual(sum(len(v) for v in side["ink"].values()), 123)


if __name__ == "__main__":
    unittest.main(verbosity=2)
