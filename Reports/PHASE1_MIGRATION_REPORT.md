# Phase 1 — Migration Report

**Date:** 2026-08-01
**Scope:** every CRITICAL item from `Reports/PHASE1_ARCHITECTURE_REVIEW.md` (C1–C7).
**Outcome:** the single-book pipeline is now a multi-book corpus system. Brihat Jataka was
migrated and rebuilt, and its Markdown is **byte-identical** to the pre-migration draft.

No new features were added. No OCR was run on any other book.

---

## 1. What changed, and why

### C1 — Globally unique identities

**Was:** page ids were `s021a`, unique only *within* a book, and every sidecar
(`corrections.json`, `page_roles.json`, `ink_report.json`, `verified/*.json`) sat at
`Pipeline/` root keyed on them. Every book has an `s001a`; processing a second book would
have applied one book's line-index drop-list to another's OCR and silently deleted real
text.

**Now:** identity is `<book_id>/pNNNN` — e.g. `brihat-jataka/p0043` — constructed and
parsed only through `corpuslib/ids.py`. Bare v1 ids are rejected wherever they appear.
All per-book state lives under `Pipeline/books/<book_id>/`. A sidecar that names a page
belonging to another book, or that declares a different `book_id` than the one being
built, raises rather than loading.

### C2 — Page ids no longer encode scan layout

**Was:** `sNNN[ab]` meant "sheet N, half a/b". Only Brihat Jataka is scanned two-up.
`verify.py` parsed `p[1:4]` as a sheet number and checked that both halves of every sheet
existed — meaningless for the five single-page books, where it would have reported a clean
bill of health while checking nothing.

**Now:** page ids are opaque and densely numbered. Scan layout moved to the book profile
(`"scan_layout": "two-up"`), and the sheet/half survives in `source_ref` as *provenance,
not identity*. Coverage is a dense sequence check enforced in `corpuslib/ir.load_book`,
which is layout-independent and fails on any gap.

### C3 — Integrity binding

**Was:** drop-lists and figure specs address OCR lines *by list position*, with nothing
tying them to the OCR run that produced those positions. Corrections had an expected-hit
count and figures a bounds check, but the hallucination drop-list — the mechanism guarding
the project's worst failure mode — had **no guard at all**.

**Now:** every IR page carries a `fingerprint` (sha256 over its canonical line payload),
and every sidecar entry carries the `ocr_fingerprint` it was written against. Any mismatch
stops the build with an explanation. IR files also self-verify, so a hand-edited page is
detected. A missing `ink_report.json` is now a hard error rather than a warning — the build
refuses to produce a corpus that may contain fabricated text.

### C4 — Per-book hallucination calibration

**Was:** `MIN_SPREAD = 30`, a literal justified by one book's measured separation. That
margin is a property of that scan's paper, ink density and scanner gamma. Too high deletes
real text; too low admits invented text; neither is visible in the output.

**Now:** `tools/calibrate_ink.py` derives the threshold from the book's own contrast
distribution — it finds the widest gap between the two populations and cuts through the
middle — and **records the calibration in the report**. If the populations are not cleanly
separated (gap narrower than 15 grey levels) the run *fails and asks for a human* instead
of guessing.

On Brihat Jataka it independently chose **43.5**, from a gap running 25 → 62 (width 37),
and selected **exactly the same 123 lines across the same 14 pages** as the hardcoded 30.

### C5 — Book layout moved into profiles

**Was:** `build_book.py` hardcoded one book's page anatomy, including the rule that *any*
line containing Devanagari is a verse line. That holds in Brihat Jataka, where Sanskrit
appears only as set-off verses. In BPHS and Jataka Parijata, Devanagari terms appear inline
in English prose, where the rule would promote ordinary paragraph lines to blockquoted
verse and shred the surrounding text — while the verse audit, which only checks numbering,
still passed.

**Now:** `profiles/<book_id>.json` carries the chapter/colophon patterns, heading policy,
indent band, gutter margin and verse strategy. `corpuslib/profile.py` defaults
`verse_requires_danda` to **true** — a verse line must look like verse, not merely contain
the script. Brihat Jataka's profile explicitly sets it **false**, with a note recording
that this is what the corpus was verified against and why it is safe *for this book only*.

### C6 — One intermediate representation, two producers

**Was:** Phaladeepika and Saravali were slated for "direct extraction" with no extraction
path, no normaliser and no verification — a second pipeline waiting to diverge.

**Now:** `corpuslib/ir.py` defines the contract. `producers/surya_ocr.py` (scanned) and
`producers/pdf_text.py` (clean digital text) both emit it, so normalisation, assembly and
verification are shared. `pdf_text.py` refuses to run on a book whose profile declares a
two-up layout, and warns loudly about pages with no text layer rather than emitting them
silently empty.

### C7 — Page provenance

**Was:** the Markdown recorded no page numbers. A reviewer who spotted a suspect line had
no way back to the page image, and Phase 3 could not cite a source location.

**Now:** every page emits `<!-- page brihat-jataka/p0043 -->` before its content —
invisible to readers, exact for tooling. 219 anchors for 219 content pages, none foreign,
none missing. `--no-anchors` reproduces the pre-anchor output exactly, which is what the
byte-identity proof below uses.

### Additional correction made during migration

The new assembler defaulted its output to `Knowledge/<book_id>.md`. That contradicts the
project's own rule that `Knowledge/` holds only the approved corpus while unverified work
stays in `Pipeline/`. The default is now `books/<book_id>/draft.md`; promotion to
`Knowledge/` remains a deliberate, separate act. The prematurely written
`Knowledge/brihat-jataka.md` was removed.

---

## 2. Migration performed

`tools/migrate_v1_to_v2.py` — one shot, idempotent, non-destructive to its inputs.

| Step | Result |
|---|---|
| OCR cache → IR | 230 pages, `s001a → brihat-jataka/p0001` … `s115b → brihat-jataka/p0230` |
| Corrections | 2 migrated, fingerprint-bound |
| Page roles | 11 exclusions migrated, fingerprint-bound |
| Verified figures | 2 migrated, renamed `s021a → p0041.json`, `s031a → p0061.json`, fingerprint-bound |
| Migration map | `books/brihat-jataka/migration_map.json` (full v1 → v2 mapping) |

Sequence mapping: `seq = (sheet − 1) × 2 + (1 if half a else 2)`. The old name is retained
in `source_ref.v1_page` and in each migrated sidecar entry as `v1_page`, so any v1
reference in the existing reports can still be resolved.

`ink_report.json` was deliberately **not** migrated. It derives from the page images, so it
was regenerated by `calibrate_ink.py` — which also gave it the calibration record the v1
file could not have carried.

### Files removed (rejected or superseded code paths)

`halluc.py` (the text-based heuristic explicitly rejected in the review — it flagged 172 of
230 pages and was still runnable next to the accepted approach), `inkcheck.py`,
`find_tables.py`, `verse_gaps.py` and `gap_lines.py` (both carrying a now-stale hardcoded
gap list), `assemble.py`, plus the root-level `ink_report.json`, `corrections.json`,
`page_roles.json`, `halluc_report.json`, `verified/`, `ocr_cache/` and `img/`.

### Files archived (retained, off the active path)

`Pipeline/archive/` holds the v1 tools and the benchmark/audit one-offs that document how
the engine was chosen (`run_engines.py`, `score.py`, `bench_*.py`, the `gt_*.txt` ground
truths, `bench_out/`) and the one-off book-audit scripts. These are evidence for
`Reports/ocr_engine_benchmark.md` and are kept, but nothing on the build path references
them.

---

## 3. Validation results

### 3.1 Byte-identical output

```
pre-migration  Brihat-Jataka.draft.md   ef9b9b7db3bc07c631f9ed08de8fd5acf107fcc82d8eee9310f5612cb61fe8fb
post-migration build --no-anchors        ef9b9b7db3bc07c631f9ed08de8fd5acf107fcc82d8eee9310f5612cb61fe8fb
```

**Identical.** Re-confirmed after all script removals and directory restructuring.

The anchored corpus differs from this only by the anchor lines: stripping
`^<!-- page \S+ -->$` and collapsing blank runs reproduces the plain output exactly
(verified programmatically).

### 3.2 Content invariants unchanged

| Check | Pre-migration | Post-migration |
|---|---|---|
| Content pages | 219 | 219 |
| Chapters | 28, numbered 1–28 | 28, numbered 1–28 |
| Colophons | 32 | 32 |
| Verse terminators | 408, all chapters sequential | 408, all chapters sequential |
| Chapters with anomalies | none | none |
| Hallucinated lines removed | 123 (threshold 30, hardcoded) | 123 (threshold 43.5, calibrated) |
| Corrections applied | 2 | 2 |
| Figures spliced | 2 | 2 |
| Gutter bleed removed | 18 | 18 |
| `[UNCLEAR]` | 0 | 0 |
| Duplicate page groups | 0 | 0 |

### 3.3 Integrity guarantees — 9/9 verified

Each failure mode was exercised against synthetic corpora and confirmed to raise:

| Guarantee | Result |
|---|---|
| Bare v1 page id `s001a` rejected | PASS |
| Missing `ink_report.json` refuses the build | PASS |
| Sidecar naming another book's page refused | PASS |
| Sidecar declaring the wrong `book_id` refused | PASS |
| Stale `ocr_fingerprint` refused | PASS |
| Missing `ocr_fingerprint` refused | PASS |
| Out-of-range drop index refused | PASS |
| Hand-edited IR page detected | PASS |
| Gap in the page sequence detected | PASS |

### 3.4 Provenance

219 page anchors for 219 content pages; zero foreign anchors; zero unanchored pages.

---

## 4. New layout

```
Pipeline/
  corpuslib/      ids.py  ir.py  sidecar.py  profile.py  normalize.py
  producers/      surya_ocr.py  pdf_text.py          -> both emit the same IR
  tools/          render_pages.py  calibrate_ink.py  build_book.py
                  verify.py  verse_audit.py  find_figures.py  migrate_v1_to_v2.py
  profiles/       brihat-jataka.json
  books/brihat-jataka/
                  ocr/p0001.json … p0230.json        (IR, each fingerprinted)
                  img/p0001.png  … p0230.png
                  ink_report.json  corrections.json  page_roles.json
                  verified/p0043.json  verified/p0061.json
                  draft.md  build_stats.json  migration_map.json
  archive/        v1 tools, benchmark and audit one-offs
Knowledge/        (empty — holds only the approved corpus)
```

### Processing a new book

```powershell
$P = "$PWD\Pipeline"    # run from the repository root
# 1. write profiles/<book-id>.json   (layout, chapter/colophon patterns, verse strategy)
python "$P\tools\render_pages.py"   <book-id> <pdf>
python "$P\producers\surya_ocr.py"  <book-id>          # or producers\pdf_text.py
python "$P\tools\calibrate_ink.py"  <book-id>          # fails if not cleanly separated
python "$P\tools\find_figures.py"   <book-id>          # -> transcribe into verified/
python "$P\tools\build_book.py"     <book-id>
python "$P\tools\verify.py"         <book-id>
python "$P\tools\verse_audit.py"    <book-id>
```

---

## 5. Remaining technical debt

None of the CRITICAL items remain. Carried forward from the review, unchanged in priority:

**IMPORTANT**

- **I1 — no structured corpus artefact.** The assembler still computes chapter, verse and
  page associations and then emits only Markdown plus `build_stats.json`. Phase 3 needs
  addressable units (`brihat-jataka/ch17/v13`). Deferred deliberately: rebuilds are cheap
  and deterministic, so this can be applied to every book in one batch without redoing any
  human verification. C7's anchors are the prerequisite and are now in place.
- **I2 — global geometry constants.** `body_l`/`body_r`/`margin` are still single values
  per book. Fine for a uniform single-column body; a book mixing column counts will pull
  them toward a value correct for no page. Now at least per-book *configurable* via the
  profile offsets.
- **I3 — figure `insert_after` is still a line index.** Guarded by fingerprint and bounds
  checks, so failure is loud, but content anchors would be sturdier. Worth revisiting
  around book ~10.
- **I4 — no test suite.** The integrity checks above were run as a one-off script, not
  committed as a permanent suite. `corpuslib/normalize.py` still contains the subtle
  `_DANDA` alternation ordering whose test cases were never captured. **This is the most
  valuable remaining item**: it now guards shared code used by every book, not one.
- **I5 — corrections are page-wide literal find/replace.** Cannot express "the third
  occurrence"; `expect` remains the only guard.
- **I7 — OCR provenance.** Fixed going forward (`surya_ocr.py` records engine version,
  device and date), but the 230 migrated Brihat Jataka pages carry
  `"note": "migrated from the v1 cache; device/date/dpi unknown"`, because v1 never
  recorded it. Recoverable only by re-running OCR; not worth it.

**OPTIONAL** — O1–O6 unchanged (line confidence capture, corpus manifest, incremental
builds, automated figure-region detection, IAST layer, glyph sampling harness).

**Unchanged from before this work:** 17 of 19 Brihat Jataka figures are still to be
transcribed, and the Devanagari glyphs have had no sample-level check. `find_figures.py`
now reports 24 candidates, 2 transcribed, 22 pending — that count includes contents pages
and two known detector false positives; the curated list is in `PROJECT_STATUS.md`.

---

## 6. Answer to the original question

The review asked whether the architecture could carry 50–100 books without a major
redesign. It now can. The three silent failure modes are gone — cross-book contamination,
stale line indices, and a hallucination threshold calibrated on one scan — and each is
replaced by something that fails loudly and explains itself. The remaining debt is
additive: a structured output layer and a test suite, both of which can be applied across
the whole corpus in a single batch because every book rebuilds deterministically from its
fingerprinted IR and sidecars.
