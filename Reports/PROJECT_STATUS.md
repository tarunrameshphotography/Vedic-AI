# Phase 1 — Status & Resume Notes

**Last updated:** 2026-08-01 (post architecture migration)
**Next action:** transcribe the 17 remaining figures (see §"Figure transcription queue"),
then get format approval and convert the remaining five books.

---

## Done

- **Folder structure created.** `Books/`, `Knowledge/`, `Ephemeris/`, `Reports/`, plus a
  `Pipeline/` folder holding the conversion tooling and cached OCR.
- **Ephemeris relocated and inventoried.** 40 years 1996–2035, complete, no gaps.
  See `Ephemeris/README.md`.
- **All six books audited.** See §"Book audit" below.
- **OCR engine benchmark completed.** Surya 0.14.7 selected at ~1.3 % Latin / ~1.5 %
  Devanagari character error. See `Reports/ocr_engine_benchmark.md`.
- **Brihat Jataka fully OCR'd** — all 230 book pages cached in
  `Pipeline/books/brihat-jataka/ocr/` as fingerprinted IR pages.
- **Draft Markdown assembled** at `Pipeline/books/brihat-jataka/draft.md`.

### Fixed on 2026-08-01

**1. Hallucinated text removed — 123 lines across 14 pages.**
The cover-page hallucination noted in the previous checkpoint was a symptom of a much
broader problem, and the diagnosis in that checkpoint was wrong. The cause is **not**
low-contrast covers, it is **show-through**: faint mirror-image ghosting from the printed
reverse of thin paper bleeding into blank page regions. Surya attempts to read the ghost
and falls into a decoding loop producing *fluent invented* English plus runs of Arabic,
CJK, Korean and Cyrillic. Worst on pages where a chapter ends partway down.

Detection is by **local contrast** (p95−p05 grey level) inside each OCR line box,
measured against the page image: real lines scored 71–188, hallucinated lines 3–14, no
overlap. `tools/calibrate_ink.py` writes `books/<book-id>/ink_report.json`, which `tools/build_book.py` consumes and validates against the OCR fingerprints.
All 123 dropped lines were reviewed by hand — none contained real content.

> Absolute darkness was tried first and rejected: hallucinated boxes contain literally
> zero dark pixels, but so do the genuine light-on-dark "About the Book" / "About the
> Author" headings, which it deleted. Text-only heuristics were also rejected — low
> lexical diversity flagged 172 of 230 pages, because the prose is genuinely repetitive.

**2. Verse count reconciled — 389 → 408, every chapter now sequential.**
All 28 chapters now run 1..N with no gaps, duplicates or out-of-order numbers. Causes:

- The audit had been counting **colophon chapter numbers as verse numbers**.
- `corpuslib/normalize.py` missed terminator variants: single danda `।`, true double danda `॥`
  (U+0965), mixed `1।` / `।1`, and a hyphen before the closing danda (`।। 3-11`).
- Two verses where Surya misread the printed Latin **8** as Devanagari **४**
  (`brihat-jataka/p0192`, `brihat-jataka/p0204`). Both confirmed against the page
  images; recorded in `corrections.json` with the evidence, and asserted to fire
  exactly once each.
- Chapter 27 verse 28 is printed **with no closing danda in the source itself**
  (verified on `brihat-jataka/p0216`). Preserved as printed; the audit accepts the open form.

**3. Chapter numbering fixed.** Seven chapters rendered as `## Chapter -1` because the
printed numeral above the title was absent or unread. Openers are strictly sequential, so
they are now numbered by position, with the 21 numerals that *were* read asserted against
that sequence. All 21 agree.

**4. Duplicate-line flags resolved.** Both checked against the page images.
`brihat-jataka/p0031` — the **source book itself prints a duplicated line** (a typesetting defect);
preserved as printed. `brihat-jataka/p0150` — false positive; "(v) Aspected by Sun: A king." and
"(vi) Aspected by Mars: A king." are distinct entries sharing a result.

**5. Publisher front/back matter excluded** — 11 pages (covers, advertisements for other
titles, "About the Book", "About the Author", one blank). Each page and its reason are
recorded in `Pipeline/books/brihat-jataka/page_roles.json`. Title page, imprint, the translator's
Introduction and the Contents are **retained** as part of the work.

**6. Paragraph-shattering fixed.** Text that wraps beside a figure starts far right of the
margin and was being read as a new indented paragraph *per line*, shattering the
commentary on every page carrying a chart. The indent test is now a bounded band.

**7. Vision-verified figure mechanism built.** `Pipeline/books/<book-id>/verified/pNNNN.json` records, per figure,, the OCR lines it occupies and the hand-transcribed Markdown to put in their
place; `build_book.py` splices it in and fails loudly if the line indices are stale.

### Verification currently passing on Brihat Jataka

| Check | Result |
|---|---|
| Content pages | 219 (230 scanned − 11 excluded as publisher matter) |
| Chapter openers | **28 / 28, numbered 1–28 in order** |
| Chapter colophons | 28 chapter colophons, 1–28 sequential (+4 verse-initial `इति` lines) |
| Verse numbering | **408 verses, every chapter sequential 1..N, zero gaps** |
| Hallucinated lines | 0 remaining (123 removed) |
| `[UNCLEAR]` sections | 0 |
| Duplicate pages | 0 |

---

## Not yet done

### Figure transcription queue — 17 of 19 remaining

Surya scrambles table cell reading order and reads chart cells as loose words that it
interleaves with the surrounding commentary. Neither is recoverable from OCR, so each
figure is transcribed by eye into `Pipeline/books/<book-id>/verified/pNNNN.json`.

**Done:** `brihat-jataka/p0041` (Mutual Friendship table), `brihat-jataka/p0061` (horoscope chart).

**Tables remaining (7):** `brihat-jataka/p0016`, `brihat-jataka/p0017`, `brihat-jataka/p0020`, `brihat-jataka/p0022`, `brihat-jataka/p0029`, `brihat-jataka/p0071`, `brihat-jataka/p0200`

**Horoscope charts remaining (10):** `brihat-jataka/p0034`, `brihat-jataka/p0035`, `brihat-jataka/p0055`, `brihat-jataka/p0128`, `brihat-jataka/p0129`,
`brihat-jataka/p0171`, `brihat-jataka/p0172`, `brihat-jataka/p0184`, `brihat-jataka/p0185`, `brihat-jataka/p0188`

`brihat-jataka/p0064` and `brihat-jataka/p0066` were flagged by the detector but contain no figure — no action.

**Agreed format** (project owner, 2026-08-01): charts get a structured planet-placement
list **plus** a fenced ASCII diagram preserving the printed layout. Where a chart carries
no lagna marker and no sign labels — as on `brihat-jataka/p0061` — house numbers are **not** guessed; the
sign reading is derived from the fixed South Indian cell positions and labelled as such.

### Other

1. **Sample Devanagari shloka verification.** The benchmark measured ~1.5 % Devanagari
   character error and individual characters may still be wrong at that rate. The verse
   *structure* is now fully verified; the *glyphs* are not.
2. **Promote the approved draft to `Knowledge/brihat-jataka.md`.** It stays at
   `Pipeline/books/brihat-jataka/draft.md` until the figure queue is finished;
   `Knowledge/` holds only approved corpus.
3. **Format approval from the project owner**, then convert the remaining five books.
4. **`Reports/conversion_report.md`** — written once books are converted. Must list the
   11 excluded publisher pages from `page_roles.json`.

---

## Phaladeepika — first book through Corpus Pipeline v1.0

Converted 2026-08-01 as a validation of the frozen architecture. The pipeline handled a
structurally very different book; **no redesign was needed**, and Brihat Jataka's output
stayed byte-identical throughout (43/43 regression tests green after every change).

| Check | Result |
|---|---|
| Producer | `pdf_text` (first real use) — 265 pages, every page has a text layer |
| Page coverage | dense 1..265, no gaps; 265 anchors, none foreign, none missing |
| Chapters | **28 / 28, numbered 1–28 in order**, titles captured |
| Hallucination scan | `not-applicable` — no model reads pixels, so fabrication is impossible |
| `[UNCLEAR]` | 0 |
| Duplicate page text | 0 |

### What this book differs in, and how the profile absorbed it

- **No Devanagari at all.** It is an English translation; source shlokas appear only as
  numbered English paragraphs and there is not one danda in the book. The verse-block
  machinery correctly never fires, and verse numbering is preserved inline as printed.
- **Latin chapter openers.** A bare bold `Chapter N` with the title on the following
  line(s). The `Chapter N: Title` form appears *only* in the contents on p0004–p0009;
  matching it there would have invented six spurious chapters.
- **Page numbers at the foot**, not the head — 264 of 265 pages.
- **Bounding boxes in PDF points**, not image pixels, so every geometry offset in the
  profile is about a quarter of the Brihat Jataka value.

### Four gaps the book exposed in v1.0 (all filled without redesign)

1. `calibrate_ink.py` demanded a contrast scan for a producer that cannot hallucinate.
   Now records `decision: not-applicable` for non-model producers.
2. `build_book.py` hardcoded `has_deva()` in the chapter-opener test, so chapter
   detection could never fire on a Latin-script book. Now driven by `profile.script`.
3. Page-number stripping only looked at the head of the page, leaving bare numerals
   embedded in prose (`"Second house — the face 10"`). Now `page_number_position`.
4. `find_figures.py` used pixel-scale constants, flagging 262 of 265 pages. Band height
   and narrow-width are now profile units; 53 candidates remain.

### Figures — 24 charts done, tables outstanding

**All 24 horoscope/Ashtakavarga charts are transcribed** into
`books/phaladeepika/verified/`. These were machine-proposed by
`tools/propose_charts.py` and checked against the rendered pages.

That aid is sound *only* for `pdf_text` books, where two things are exact rather than
inferred: cell labels come from the embedded text layer (no OCR error), and the chart
grid is vector graphics, so cell boundaries are known precisely. **Neither holds for a
scanned book** — Brihat Jataka's charts remain a manual, by-eye job.

Two things it caught that hand-transcription would likely have missed:

- **Merged cells.** PyMuPDF returns one line per baseline, so two adjacent cells on the
  same baseline arrive as one string (`"00000 0000"`). Assigning that by its midpoint
  silently moved four bindus from Libra into Scorpio on printed page 227. Tokens are now
  placed individually by interpolated position.
- **A source defect.** Ashtakavarga totals are self-checking: one planet's chart must
  total 48 bindus, the sarvashtakavarga 337. Page 227 totals 48; **page 221 totals 44**.
  Verified by eye — the transcription matches the page exactly and the error is in the
  book. Preserved as printed and flagged in `verified/p0221.json`, never corrected.

### Not yet done

1. **Tables: ~10 genuinely tabular pages still flattened into prose** — `p0230` (100 %
   short/narrow), `p0254`, `p0023`, `p0012`, `p0013`, `p0025` and similar. `find_figures`
   reports "53 candidates, 18 transcribed, 35 pending", but that count is misleading in
   both directions: 6 of the 24 charts were on pages it never flagged, and many of the
   35 "pending" (e.g. `p0189`, `p0129`, `p0016`) are pure prose — false positives from
   the multi-row band heuristic. The real remaining work is the tabular pages listed
   above, not 35 pages.
2. **Front matter roles not yet assigned.** p0001–p0009 (title page, preface, contents)
   are currently all included; no covers or advertisements were detected, but this has
   not been audited page by page.
3. **No spot-check against the printed page.** Direct text extraction cannot hallucinate,
   but it can drop or reorder; a sample comparison against the PDF rendering is still
   owed.

---

## Book audit

| Book | PDF pages | Text layer | Method | Notes |
|---|---|---|---|---|
| Brihat Jataka | 115 spreads = **230 book pages** | Corrupt OCR | Surya | **Two-up spreads — must be split** |
| BPHS Vol. 1 | 482 | Corrupt OCR | Surya | Pending |
| Jataka Parijata Vol. 1 | 324 | Severely corrupt | Surya | Pending |
| Uttara Kalamrita | 256 | Corrupt + **75 pages with no text at all** | Surya | Pending |
| Phaladeepika | 265 | Clean digital | `pdf_text` producer | **Converted 2026-08-01**, 28 chapters, figure queue open |
| Saravali | 203 | Clean but **diacritics lost in the source PDF itself** | Direct extraction | See below |

### Saravali caveat

The Saravali PDF *renders* "Horā Śāstra" as `Hora Sstr`, "Rāśi" as `Rsi`/`Ri`. A defect
baked into the source PDF, not an extraction fault. Preserved as printed and flagged,
never guessed at. A transliteration normalisation map is deferred to a later phase.

### Applies to every remaining book

- **Run `tools/calibrate_ink.py` before trusting any output.** The show-through hallucination is a
  property of Surya plus thin paper, not of this one book.
- **Find the figures first.** `find_tables_ocr.py` locates candidate table/chart pages
  from the OCR geometry.

---

## How to resume

The pipeline was restructured on 2026-08-01 into a multi-book corpus system; see
`Reports/PHASE1_MIGRATION_REPORT.md`. All per-book state now lives under
`Pipeline/books/<book-id>/` and page ids are globally unique (`brihat-jataka/p0043`).
Page images and OCR are already present, so nothing needs re-running to continue.

```powershell
$P = "$PWD\Pipeline"    # run from the repository root

python "$P\tools\build_book.py"  brihat-jataka     # -> books/brihat-jataka/draft.md
python "$P\tools\verify.py"      brihat-jataka
python "$P\tools\verse_audit.py" brihat-jataka
python "$P\tools\find_figures.py" brihat-jataka    # figure queue, transcribed vs pending
```

To regenerate page images if they are ever cleared (~1 minute):

```powershell
python "$P\tools\render_pages.py" brihat-jataka "Books\Varaha_Mihira_-_Brihat_Jataka.pdf"
python "$P\tools\calibrate_ink.py" brihat-jataka
```

### Transcribing a figure

Write `Pipeline/books/brihat-jataka/verified/pNNNN.json` with `schema: 2`, the `page_id`,
the page's current `ocr_fingerprint` (from `books/<id>/ocr/pNNNN.json`), the
`exclude_lines` the figure occupies, an `insert_after` anchor, and the `markdown`. The
build refuses to run if the fingerprint is stale or the indices are out of range.

### Adding a new book

Write `Pipeline/profiles/<book-id>.json` first — the assembler carries no book's page
anatomy as a default. Then render, produce, calibrate, find figures, build, verify. Full
sequence in `Reports/PHASE1_MIGRATION_REPORT.md` §4.

**`verse_requires_danda` defaults to true.** Brihat Jataka sets it false because its
Sanskrit appears only as set-off verses. Do not copy that setting to BPHS or Jataka
Parijata, where Devanagari appears inline in English prose.

### OCR environment

Only needed to OCR a *new* book. See `Reports/ocr_engine_benchmark.md` §4 for exact pins.

```powershell
uv venv --python 3.12 <path>\ocrenv
uv pip install --python <path>\ocrenv\Scripts\python.exe surya-ocr==0.14.7
uv pip install --python <path>\ocrenv\Scripts\python.exe `
   --reinstall-package torchvision "torch==2.9.0+cu128" "torchvision==0.24.0+cu128" `
   --index-url https://download.pytorch.org/whl/cu128
```

`torchvision` **must** carry the explicit `+cu128` tag or pip silently installs the
ancient 0.2.0 and breaks `torchvision::nms`.

---

## Open decision for the project owner

Review `Pipeline/books/brihat-jataka/draft.md` for **structure and formatting** — heading
hierarchy, how shlokas are presented (blockquote, one line per verse line), chapter
headings as `## Chapter N — <Devanagari> · <English>`, colophons in italics, and the new
figure format (see `brihat-jataka/p0041` and `brihat-jataka/p0061` in the draft, printed
pages 38 and 58). Once approved, the same pipeline
runs unchanged across the remaining books.

The draft has **not** yet had a Devanagari glyph-level check, so individual characters may
still be wrong at roughly the 1.5 % rate measured in the benchmark. Verse *structure* is
fully verified.
