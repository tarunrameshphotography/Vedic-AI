# Corpus Pipeline v1.0

**Frozen:** 2026-08-01
**Status:** stable. Do not redesign unless a book exposes a genuinely new class of problem.
**Regression suite:** `Pipeline/tests/test_pipeline.py` — 43 tests, ~2.5 s, must stay green.
**Validated on:** Brihat Jataka (Surya OCR, two-up, Devanagari) and Phaladeepika
(`pdf_text`, single-page, Latin-only). See `PROJECT_STATUS.md` for the four gaps
Phaladeepika exposed; all were filled inside the profile system without redesign.

This document is the specification. `PHASE1_ARCHITECTURE_REVIEW.md` records why the design
changed; `PHASE1_MIGRATION_REPORT.md` records how it was migrated and validated.

---

## 1. Architecture

A book moves through five stages. Each writes a durable artefact, so any stage can be
re-run without repeating the ones before it.

```
  PDF
   │  tools/render_pages.py          layout from the book profile
   ▼
  page images            books/<book>/img/pNNNN.png
   │  producers/surya_ocr.py   OR   producers/pdf_text.py
   ▼
  IR  (intermediate representation)  books/<book>/ocr/pNNNN.json   ← fingerprinted
   │  tools/calibrate_ink.py         per-book hallucination threshold
   │  + human judgement              corrections / page roles / verified figures
   ▼
  sidecars               books/<book>/*.json, verified/   ← bound to IR fingerprints
   │  tools/build_book.py            generic engine + profiles/<book>.json
   ▼
  Markdown               books/<book>/draft.md  →  Knowledge/<book>.md when approved
```

The controlling idea: **machine output and human judgement are stored separately and
bound by content hash.** OCR is cheap and reproducible; the human verification of a page
is expensive and irreplaceable. Keeping them apart means OCR can be re-run freely, and any
drift between the two is detected rather than silently absorbed.

---

## 2. Directory structure

```
Pipeline/
  corpuslib/            shared library — the only place invariants are enforced
    ids.py              book_id / page_id construction and parsing
    ir.py               IR read/write, fingerprinting, dense-sequence loading
    sidecar.py          sidecar loading + all integrity checks
    profile.py          per-book layout profile, with safe defaults
    normalize.py        Surya error-class normalisation (danda, visarga, tags)
  producers/            anything that can emit IR
    surya_ocr.py        scanned books
    pdf_text.py         books with a clean digital text layer
  tools/                one job each, all take <book_id> as first argument
    render_pages.py  calibrate_ink.py  build_book.py
    verify.py  verse_audit.py  find_figures.py  migrate_v1_to_v2.py
  profiles/<book_id>.json
  books/<book_id>/
    ocr/pNNNN.json      IR, one per page
    img/pNNNN.png       rendered page images
    ink_report.json     hallucination drop-list + calibration record
    corrections.json    evidence-bearing OCR corrections
    page_roles.json     pages excluded from the corpus, with reasons
    verified/pNNNN.json hand-transcribed tables and charts
    draft.md            assembled output, pre-approval
    build_stats.json    chapters, verses, colophons, flags
    migration_map.json  (Brihat Jataka only) v1 → v2 page id mapping
  tests/test_pipeline.py
  archive/              v1 tools and benchmark evidence; nothing references these
Knowledge/<book_id>.md  approved corpus only
```

---

## 3. Data model

| Entity | Identity | Notes |
|---|---|---|
| Book | `book_id` — lowercase slug, e.g. `brihat-jataka` | unique across the corpus |
| Page | `page_id` — `<book_id>/pNNNN`, e.g. `brihat-jataka/p0043` | globally unique, opaque, dense from 1 |
| Line | position within a page's `lines` array | **not** an identity; only valid against a fingerprint |
| Figure | one `verified/pNNNN.json` per page | at most one per page |

**Page ids carry no information about scan layout.** Brihat Jataka is scanned two pages to
a sheet; nothing downstream knows or cares. Where the page came from lives in `source_ref`
as provenance. This is the distinction v1 got wrong, and it is the reason `verify.py`
silently stopped checking anything on single-page books.

Page numbering is the *book page* sequence, not the PDF page sequence. For a two-up scan
`seq = (sheet − 1) × 2 + (1 if left half else 2)`.

---

## 4. IR schema

One JSON file per page. This is the contract every producer must satisfy.

```jsonc
{
  "schema": 2,
  "page_id": "brihat-jataka/p0043",
  "book_id": "brihat-jataka",
  "seq": 43,
  "source_ref": { "pdf_page": 22, "half": "a" },   // provenance, never identity
  "producer": { "name": "surya", "version": "0.14.7",
                "task": "ocr_with_boxes", "device": "cuda",
                "run_date": "2026-07-31" },
  "fingerprint": "sha256 of the lines payload",
  "lines": [ { "text": "…", "bbox": [x0, y0, x1, y1] } ]
}
```

`fingerprint` is sha256 over the canonical, key-sorted, whitespace-free serialisation of
`lines` only — text and integer bboxes. Producer metadata is deliberately excluded so that
re-recording provenance does not invalidate verified human work, while any change to the
text or its geometry does.

Reading a page verifies its own fingerprint, so a hand-edited IR file is rejected.
Loading a book requires a dense sequence and fails on any interior gap.

`text` may carry inline `<b>`, `<i>`, `<math>` markers as emitted by the producer;
`corpuslib.normalize.strip_tags` removes them at assembly time.

---

## 5. Sidecar system

Four files per book hold everything a human decided about a page. All are keyed by
`page_id` and all carry the `ocr_fingerprint` they were written against.

| File | Holds | Guard |
|---|---|---|
| `ink_report.json` | line indices to drop as hallucinated, plus the calibration record | fingerprint, index range; **missing file is a hard error** |
| `corrections.json` | `find`/`replace` with `reason`, `verified`, and an `expect` count | fingerprint, required evidence fields, exact hit count |
| `page_roles.json` | pages excluded from the corpus, each with a reason | fingerprint, reason required |
| `verified/pNNNN.json` | hand-transcribed figure Markdown, `exclude_lines`, `insert_after` | fingerprint, index range, filename must match `page_id` |

Every load path raises `SidecarError` rather than degrading. The specific failures that
are tested: an entry naming another book's page; a file declaring a different `book_id`;
a stale fingerprint; a missing fingerprint; an out-of-range index; a figure filed under
the wrong name; a correction without evidence.

A missing `ink_report.json` refuses the build outright. The reasoning is asymmetric: a
corpus with no corrections is merely unpolished, but a corpus that never had its
hallucination scan may contain invented sentences that read as real content.

---

## 6. Producer interface

A producer turns a source into IR and nothing more. It must:

1. take `book_id` as its first argument and read the book's profile,
2. emit exactly one IR page per **book page**, densely numbered from 1,
3. record its own identity and version in `producer`,
4. call `corpuslib.ir.write_page`, which computes the fingerprint,
5. never normalise, correct or interpret — that is the assembler's job.

Two producers exist. `surya_ocr.py` reads rendered images and is resumable. `pdf_text.py`
extracts an existing text layer, refuses to run on a book whose profile declares a two-up
layout, and warns loudly about pages with no text rather than emitting them silently
empty.

Adding a third producer requires no changes anywhere else.

---

## 7. Verification pipeline

| Tool | Checks |
|---|---|
| `ir.load_book` | dense page sequence, per-page fingerprint self-consistency |
| `sidecar.load_all` | every guard in §5 |
| `calibrate_ink.py` | contrast populations are cleanly bimodal, else refuses |
| `build_book.py` | correction hit counts, figure index ranges, chapter numeral vs sequence |
| `verify.py` | page coverage, duplicate page text, anchor completeness, no foreign anchors |
| `verse_audit.py` | verse numbers run 1..N per chapter: no gaps, duplicates or reordering |
| `find_figures.py` | candidate table/chart pages, and which are still untranscribed |
| `tests/test_pipeline.py` | the architectural guarantees themselves |

**Hallucination calibration.** Contrast (`p95 − p05` grey level) is measured inside every
line box. The threshold is the midpoint of the widest gap in the observed distribution
within `[2, 120]`, and the gap must be at least `MIN_MARGIN = 15` wide. If every line is
above `NO_HALLUC_FLOOR = 45`, the book has no blank-region reads and nothing is dropped.
If the populations overlap, the run fails and asks for a human. On Brihat Jataka this
independently produced 43.5 — from a gap of 25→62 — and selected exactly the same 123
lines as the hand-tuned constant it replaced.

**Chapter numbering.** Openers are numbered by their position in the book; a numeral read
off the page is used only as a cross-check and warns on disagreement. The unreliable
signal never becomes the source of truth.

---

## 8. Design principles

1. **Fidelity over tidiness.** A defect in the printed source is preserved and flagged, not
   repaired. Brihat Jataka prints a duplicated line on p0031 and omits a closing danda on
   p0216; both are in the corpus as printed.
2. **Correct only where certain.** An OCR correction must carry its evidence and is
   asserted to fire an exact number of times. A correction that stops matching fails the
   build rather than passing unnoticed.
3. **Never guess; flag instead.** Unreadable text is `[UNCLEAR]`. A chart with no lagna
   marker gets no house numbers.
4. **Ground decisions in the artefact, not the text.** Hallucination detection reads
   pixels, because the fabricated text is fluent and no lexical heuristic separates it —
   one such heuristic flagged 172 of 230 pages.
5. **Fail loudly, never silently.** Every guard raises with an explanation of what drifted
   and what to do. Silent failure is the only kind that corrupts a corpus.
6. **Human judgement is the expensive artefact.** Machine output is disposable and
   reproducible; the sidecars are not. They are stored separately and integrity-bound.
7. **Book-specific knowledge lives in profiles, never in code.**
8. **Deterministic and reproducible.** Same inputs, same bytes out — enforced by test.

---

## 9. Known limitations

**Accepted, with reasons.**

- **A truncated tail is undetectable.** A dense sequence catches interior gaps but not a
  book missing its final pages. Page count is checked against the PDF at render time
  instead. Covered by an explicit test that documents the behaviour.
- **Line indices remain positional.** Fingerprints make staleness loud, but a figure's
  `insert_after` is still a line number. Content anchors would be sturdier; deferred.
- **Geometry constants are per book, not per page.** `body_l`/`body_r`/`margin` are single
  values. A book mixing column counts will pull them toward a value correct for no page.
  Offsets are at least configurable per book via the profile.
- **Corrections are page-wide literal find/replace.** No way to express "the third
  occurrence"; the `expect` count is the only guard.
- **No structured corpus artefact yet.** Chapter/verse/page associations are computed and
  then emitted only as Markdown plus `build_stats.json`. Phase 3 will want addressable
  units (`brihat-jataka/ch17/v13`). Deferrable because rebuilds are deterministic and
  cheap — the page anchors are the prerequisite and are in place.
- **Migrated Brihat Jataka OCR has no run provenance.** v1 never recorded it; those pages
  carry an explicit note saying so. Fixed for all future books.
- **Output is written in text mode**, so the corpus carries CRLF on Windows. Preserved
  deliberately: changing it would break byte-identity with the pre-migration baseline.
- **Glyph-level accuracy is unverified.** All structural checks pass, but the ~1.5 %
  Devanagari character error measured in the engine benchmark has not been sampled in the
  output. Structure is verified; glyphs are not.

**Not limitations of the design, but standing hazards of the material:** Surya fabricates
text on blank regions backed by print; it scrambles table cell order; it reads chart cells
as loose words. All three are handled, and all three must be assumed present in every new
book until checked.

---

## 10. Adding a book

```powershell
$P = "$PWD\Pipeline"    # run from the repository root
# 1. write profiles/<book-id>.json  — layout, chapter/colophon patterns, verse strategy
python "$P\tools\render_pages.py"   <book-id> <pdf>
python "$P\producers\surya_ocr.py"  <book-id>      # or producers\pdf_text.py <book-id> <pdf>
python "$P\tools\calibrate_ink.py"  <book-id>
python "$P\tools\find_figures.py"   <book-id>      # then transcribe into verified/
python "$P\tools\build_book.py"     <book-id>
python "$P\tools\verify.py"         <book-id>
python "$P\tools\verse_audit.py"    <book-id>
python "$P\tests\test_pipeline.py"                 # must stay green
```

`verse_requires_danda` defaults to **true**. Brihat Jataka sets it false because its
Sanskrit appears only as set-off verses; do not copy that to a book where Devanagari terms
appear inline in English prose.
