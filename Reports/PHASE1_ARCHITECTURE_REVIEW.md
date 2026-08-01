# Phase 1 — Architecture Review

**Date:** 2026-08-01
**Reviewer role:** lead architect, reviewing the Phase 1 conversion pipeline before it is
applied to further books.
**Scope:** everything under `Pipeline/`, the corpus layout under `Knowledge/`, and the
verification and audit machinery in `Reports/`.
**Question being answered:** is this architecture robust enough to process 50–100
classical books without a major redesign later?

---

## Verdict

**The methodology is sound. The data model is not.**

The intellectual core of this pipeline — evidence-based hallucination detection from
pixel contrast, sequence-validated verse numbering, corrections that carry their evidence
and refuse to run silently, figures transcribed by eye rather than trusted from OCR — is
genuinely good work and should be preserved as-is. That part scales.

What does not scale is the **plumbing around it**. The pipeline was written against one
book and has quietly absorbed that book's shape in ways that will break on the second
book, not the fiftieth. Most seriously, every file holding expensive human judgement
(`corrections.json`, `verified/*.json`, `ink_report.json`, `page_roles.json`) is keyed by
a page identifier that is only unique *within* a book. Adding a second book does not
degrade these files — it corrupts them, silently, because `s021a` exists in every book.

The good news is that the expensive artefacts are cheap to *rebuild* and hard to
*recreate*. Cached OCR plus sidecar files regenerate the Markdown in seconds, so output
format decisions can be deferred. But the sidecar files themselves encode hours of
human verification per book and must be namespaced and integrity-checked **before** a
second book is processed.

**Recommendation: fix the seven CRITICAL items below — roughly a day of work — before
processing another book. Everything else can wait.**

---

## What is working well

Recorded so it is not lost in a refactor.

- **Hallucination detection by pixel contrast** (`scan_ink.py`). Grounding the decision in
  the image rather than in the text is the single best design decision in the project.
  The rejected alternatives are documented in the code, which is exactly right.
- **Corrections that carry evidence and assert their own application**
  (`build_book.py:66-70`). A correction that silently stops matching is a corpus
  integrity failure; refusing to build is the correct response.
- **Chapter numbers derived from sequence and cross-checked against the printed numeral**
  (`build_book.py:189-198`). Using the unreliable signal as a *check* on the reliable one,
  rather than as the source, is the right inversion.
- **Distinguishing source defects from OCR defects.** The duplicated line on `s016a` and
  the missing closing danda on `s108b` were preserved as printed rather than "fixed". This
  discipline is what makes the corpus research-grade and must survive every refactor.
- **`page_roles.json`** documents exclusions instead of silently dropping pages.

---

## CRITICAL

*Fix before processing another book. Each of these either corrupts data on contact with a
second book, or silently invalidates verification that has already been signed off.*

### C1. Page identifiers are book-local, but every metadata file is global

`corrections.json` entries are keyed `"page": "s096b"`. `verified/` files are named
`s021a.json`. `ink_report.json` and `page_roles.json` are keyed `"s001a"`, `"s115b"`.
None carries a book identifier, and all four live at `Pipeline/` root.

Every book will have an `s001a`. The moment BPHS is processed:

- its `ink_report.json` overwrites Brihat Jataka's, or
- `build_book.py:39` reads the wrong book's drop-list and deletes real content, and
- a `verified/s021a.json` for BPHS collides with Brihat Jataka's friendship table.

This is not degradation, it is data loss of the most expensive artefacts in the project.

**Why before the next book:** the collision is silent. `build_book.py` will happily apply
Brihat Jataka's line-index drop-list to BPHS's OCR and produce a plausible-looking
corpus with real sentences removed. There is no check that would catch it.

**Fix:** namespace everything by book — `Pipeline/books/<book_id>/{ink_report.json,
corrections.json, page_roles.json, verified/}` — and make `<book_id>` a required argument
rather than an implicit global.

### C2. The page-ID scheme assumes two-up spreads

`sNNN[ab]` encodes "spread N, half a/b". Brihat Jataka is the *only* book with two-up
spreads; the other five are single-page. `verify.py:14-20` parses `p[1:4]` as a spread
number and reports "missing halves" over `"ab"`. Run against a single-page book, its
coverage check is meaningless — it will report a clean bill of health on page identifiers
it does not understand.

**Why before the next book:** the very first book processed after this one is
single-page, and the primary coverage check silently stops checking anything.

**Fix:** adopt an opaque, book-scoped page id (e.g. `p0007`) plus a separate
`source_ref` field recording provenance (`{"pdf_page": 7, "half": "a"}` where relevant).
Coverage checks then validate a dense integer sequence regardless of scan layout.

### C3. Sidecar files are bound to OCR output by positional line index, with no integrity check

`ink_report.json` and `verified/*.json` both address OCR lines by **list position**.
Nothing binds them to the OCR run that produced those positions. If OCR is ever re-run —
a Surya upgrade, a different DPI, a re-render — every index silently shifts.

`corrections.json` is partly protected (the `expect` count, `build_book.py:66`) and
`verified/` has a bounds check (`build_book.py:95`), but **`ink_report.json` has no guard
at all** (`build_book.py:43-47`). A stale drop-list deletes arbitrary real lines and
reports a confident `hallucinated lines removed: 123`.

**Why before the next book:** this is the mechanism protecting against the project's worst
failure mode, and it is the one with no safety check. It will be re-run per book, so the
chance of staleness rises with every book added.

**Fix:** write a fingerprint (sha256 of the page's OCR JSON) into every sidecar entry and
verify it at build time; refuse to build on mismatch. Additionally, prefer *content*
anchors over indices where practical — `verified/`'s `insert_after` in particular should
anchor to a text snippet, not line 17.

### C4. The hallucination threshold is calibrated on one book's scan quality

`scan_ink.py` uses `MIN_SPREAD = 30`, justified by a measured separation on Brihat Jataka
(real 71–188, hallucinated 3–14). That margin is a property of *this scan*: its paper,
ink density, scanner gamma and JPEG quality. A darker scan, a greyer paper, or a book
with genuinely faint print will narrow or invert that gap.

**Why before the next book:** the failure is asymmetric and silent in both directions —
too high a threshold deletes real text, too low admits fabricated text. Neither is visible
in the output. Uttara Kalamrita, with 75 pages of unreadable scan quality, is exactly the
book likely to break this constant.

**Fix:** compute the separation per book and **report the margin**, failing loudly if the
two populations are not cleanly separated (e.g. if the gap between the real-line 5th
percentile and the hallucinated-line 95th percentile falls below a set width). The
constant should become a calibrated, per-book, recorded value — not a literal.

### C5. `build_book.py` hardcodes one book's page anatomy

The script is explicitly documented as "Brihat Jataka layout" (`build_book.py:1`) and bakes
in:

- chapter opener = a line matching `...ध्यायः` (`:130`)
- colophon = a line starting `इति` (`:131`)
- **any Devanagari line = a verse line** (`:261-268`)
- running headers = Latin-only text appearing on ≥4 pages (`:133-140`)
- section heading = any bold line under 70 characters (`:271`)

The Devanagari-implies-verse rule is the most dangerous. It holds in Brihat Jataka because
Sanskrit appears only as set-off verses. In BPHS and Jataka Parijata, Devanagari terms
appear *inline within English prose*; every such line would be silently promoted to a
blockquoted verse, shredding the paragraph around it — the same class of bug already seen
with chart cells, but far more widespread.

**Why before the next book:** the output will look structurally plausible while being
wrong throughout, and the verse audit — which only checks numbering — would still pass.

**Fix:** extract the book-specific rules into a per-book profile (regexes, heading policy,
verse-detection strategy) and keep `build_book.py` as a generic engine. Add a verse
heuristic stronger than "contains Devanagari" — e.g. requires a danda, or line geometry
consistent with a set-off block.

### C6. Two of the six books do not go through this pipeline at all

Phaladeepika and Saravali are clean digital text and are slated for direct extraction.
There is currently **no extraction path, no normaliser, and no verification** for them —
yet they must land in the same corpus, with the same structure, and satisfy the same
audits.

**Why before the next book:** if the text-extraction path is built later and independently,
it will produce a differently-shaped Markdown and a second, divergent verification story.
Deciding the shared intermediate representation *now* is what prevents two pipelines.

**Fix:** define the intermediate form — a per-page list of `{text, bbox, source}` — as the
pipeline's contract. PDF text extraction and Surya OCR both become *producers* of it;
everything downstream (`normalize`, `build_book`, `verify`) is shared.

### C7. No provenance from a corpus line back to its printed page

The Markdown records no page numbers. Once built, there is no way to trace a verse or a
sentence back to the page it came from, which means:

- a reviewer who spots a suspect line cannot find the page image to check it,
- Phase 3 retrieval cannot cite a source location,
- the corpus cannot be re-verified against the scans without redoing the mapping.

Provenance *is* currently recoverable by rebuilding, since `stats.json` retains some page
associations — which is why this is a data-model bug and not an unrecoverable loss.

**Why before the next book:** it costs almost nothing to emit now, and the whole point of
Phase 1 is a *research-grade* corpus. A research corpus that cannot cite its own source
pages is not research-grade. Retrofitting after 50 books means 50 rebuilds and 50
re-verifications.

**Fix:** emit page anchors into the Markdown (an HTML comment per page boundary is
sufficient and invisible to readers), and carry them into the structured sidecar.

---

## IMPORTANT

*Real debt, but it can wait until Phase 1's six books are done. None of these corrupts
data or invalidates verification; they cost time and rework rather than correctness.*

### I1. Markdown is the only output; there is no structured corpus artefact

`build_book.py` computes exactly what Phase 3 will need — chapter number, verse number,
colophon boundaries, page association — and then discards it, emitting flat Markdown plus
a loosely-shaped `stats.json` written to `OUTFILE + ".stats.json"` (`:290`).

Phase 3 retrieval will need addressable units (`brihat-jataka/ch17/v13`) with metadata.
Re-deriving those by re-parsing Markdown with regexes is a strictly worse version of the
information already in hand.

**Why it can wait:** rebuilds are cheap and fully deterministic from cached OCR plus
sidecars. Emitting a structured JSON corpus alongside the Markdown is a additive change
that can be applied to all books at once, at any point, in a single batch rebuild. It does
not require redoing any human verification.

### I2. Global geometry constants are computed across the whole book

`BODY_L`/`BODY_R` (`:110-113`) and `MARGIN` (`:146`) are single values derived from every
line in the book. They work here because Brihat Jataka has a uniform single-column body.
A book mixing single- and double-column pages, or with many full-page tables, will pull
these constants toward a value correct for no page.

The `INDENT_MAX` band (`:150`) is a good local fix but inherits the same global `MARGIN`.

**Why it can wait:** the failure is visible in the output as mangled paragraphs, not
silent, and it can be corrected per-book by making the constants per-page or per-section
without touching any stored human judgement.

### I3. `verified/` insert positioning is fragile and manual

`insert_after` is an integer line index, and the index arithmetic (`:101`) mixes original
and post-exclusion index spaces — correct as written, but subtle enough to be a latent
bug. Building ~19 of these per book by hand across 50 books is also a lot of hand-authored
line indices.

**Why it can wait:** it is guarded (`:95-97`), the failure mode is a loud `SystemExit`, and
the volume for the remaining five books is manageable. Worth revisiting before book ~10.

### I4. No test suite

`normalize.py` now contains genuinely subtle regex work — the `_DANDA` alternation ordering
exists specifically so that a verse numbered 11 is not mistaken for a danda substitute.
That logic was validated interactively and the test cases were not kept. Any future edit
risks silently regressing verse numbering across every book.

**Why it can wait:** the verse audit acts as a strong integration-level backstop and would
catch a numbering regression on rebuild. But the unit-level cases should be captured
before `normalize.py` is edited again.

### I5. Corrections are literal string find/replace, book-wide per page

`corrections.json` applies `find`→`replace` to every line on a page (`:62-65`). It happens
to be safe here because the strings are distinctive, but the model cannot express "the
third occurrence" or "this specific line", and `expect` is the only guard.

**Why it can wait:** the `expect` assertion makes over-application loud rather than silent,
which is the property that matters.

### I6. Dead and superseded scripts are accumulating

`Pipeline/` holds 25 scripts, several superseded or stale:

- `halluc.py` — superseded by `scan_ink.py`; its text-based heuristic was explicitly
  rejected, but it remains runnable and would produce misleading output.
- `find_tables.py` — superseded by `find_tables_ocr.py`; reads the corrupt PDF text layer
  and hardcodes the Brihat Jataka path.
- `verse_gaps.py`, `gap_lines.py` — one-off debugging tools carrying a hardcoded `GAPS`
  dict (`verse_gaps.py:28`) that is now **stale**: every gap listed there has been fixed.
- `inkcheck.py` — a debug precursor to `scan_ink.py`.

**Why it can wait:** clutter, not corruption. But a rejected approach left executable next
to the accepted one is a genuine trap for a future maintainer, so `halluc.py` in particular
should be removed or clearly marked.

### I7. OCR runs record no provenance

`bulk_ocr.py` writes `.txt` and `.json` per page with no record of Surya version, model
weights, device, DPI, or date. For a corpus whose central claim is fidelity, the
provenance of the machine-read layer should be part of the artefact.

**Why it can wait:** the pins are documented in `Reports/ocr_engine_benchmark.md` and the
environment is reproducible today. It becomes urgent only when a second OCR version enters
the picture.

---

## OPTIONAL

*Future benefit; no current cost.*

### O1. Capture per-line OCR confidence
The cached JSON stores only `text` and `bbox`. If the Surya API exposes confidence, storing
it would give the verification layer a third independent signal alongside contrast and
sequence, and would help target the sampling for glyph-level checks.

### O2. Corpus manifest and build reproducibility
A top-level manifest recording, per book, the source PDF hash, OCR run id, sidecar hashes
and output hash would make the whole corpus reproducible and diffable — valuable when 50
books are in flight and someone asks what changed.

### O3. Incremental and parallel builds
Currently every build reprocesses every page. Irrelevant at 230 pages; noticeable at
50 books × ~300 pages.

### O4. Automated figure-region detection
`find_tables_ocr.py` finds candidate pages; a human then crops and transcribes. Detecting
the figure's bounding region automatically would cut the manual step and make
`exclude_lines` derivable rather than hand-authored.

### O5. IAST transliteration layer
Already deferred by project rules. When it arrives it should be an additive layer keyed to
the structured corpus (I1), never a mutation of the preserved Devanagari.

### O6. Glyph-level Devanagari sampling harness
The ~1.5 % character error rate is currently unmeasured in the output. A harness that
samples N verses per book and diffs a re-read against the corpus would turn that from an
assumption into a reported number.

---

## Suggested target shape

```
Pipeline/
  profiles/<book_id>.json        # per-book: page anatomy, regexes, thresholds
  books/<book_id>/
    ocr/                         # per-page {text,bbox} + run provenance
    ink_report.json              # fingerprinted to the ocr run
    corrections.json             # fingerprinted, evidence-bearing
    page_roles.json
    verified/                    # figures, content-anchored
  lib/                           # normalize, geometry, audits (shared, tested)
  producers/                     # surya_ocr.py | pdf_text.py -> common IR
Knowledge/
  <book_id>.md                   # human-readable, with page anchors
  <book_id>.json                 # structured, addressable, cited
```

**Migration order:** C1 and C2 together (they are one change to page identity), then C3
(fingerprints), then C6 (the shared intermediate representation), then C5 (profiles), then
C4 and C7. C4 and C7 are small and independent.

---

## Answer to the review question

**Not yet — but it is close, and the gap is plumbing rather than method.**

The verification methodology is strong enough for 100 books today. The data model will not
survive the second book, and three of the seven CRITICAL items (C1, C3, C4) fail *silently*
— producing a confident, plausible, wrong corpus rather than an error. For a project whose
entire value proposition is fidelity to the source, silent failure modes are the ones worth
spending a day to eliminate now.

None of the CRITICAL items requires redesigning the parts that are good. They are
namespacing, fingerprinting, calibration and configuration extraction — mechanical changes
around an intellectual core that should be left intact.
