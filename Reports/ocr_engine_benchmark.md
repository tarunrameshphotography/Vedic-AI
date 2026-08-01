# OCR Engine Benchmark — Phase 1

**Date:** 2026-07-31
**Purpose:** Determine whether an automated OCR engine can reach research-grade fidelity on
both English and Devanagari, before committing to manual page-by-page vision transcription.
**Test corpus:** Brihat Jataka (Varahamihira, tr. P.S. Sastri, Ranjan Publications 2013).

---

## 1. Test Method

Each PDF page in this book is a **two-page scanned spread**. Spreads were split into single
book pages and rendered at **300 DPI** before OCR.

Five representative pages were chosen to cover distinct layout challenges:

| ID | Printed page | Page type | Challenge |
|---|---|---|---|
| `s002b` | title page | Title / display type | Large mixed fonts, centred layout, one Devanagari line |
| `s004a` | iv | Dense English prose | Long justified paragraphs, hyphenation |
| `s010a` | 16 | Devanagari-heavy | Two 4-line shlokas, section headings, **yellow highlighter** |
| `s010b` | 17 | Table | 8-column × 4-row numeric table, shlokas, highlighter |
| `s051b` | 99 | Chapter opening | Chapter number, bilingual title, verses + prose |

**Ground truth** was established by direct visual reading of each rendered page.

**Scoring:** character error rate against ground truth, computed **separately for Latin+digits
and for Devanagari**, since an engine can be strong in one script and useless in the other.

---

## 2. Results

### Character error rate (lower is better)

| Engine | Latin + digits | Devanagari | Verdict |
|---|---|---|---|
| **Surya 0.14.7** | **1.3 %** | **1.5 %** | Research-grade |
| Windows OCR (`winocr`) | 1.5 % | **100 %** | English only; cannot read Devanagari |
| EasyOCR (`hi`+`en`) | 11.2 % | 12.1 % | Not acceptable |
| Existing PDF text layer | 43.4 % | 100 % | Unusable |

> **Caveat on the text-layer row:** the embedded text layer is stored per *spread*, so it was
> scored against a single-page ground truth and its Latin figure is inflated. Its Devanagari
> result is not an artefact — the text layer's Sanskrit is genuine garbage
> (`ftct rnr&(t grr* rffi`), as is its English on many pages (`bec orne a king`).

### Per-page detail (Surya)

| Page | Latin | Devanagari | Note |
|---|---|---|---|
| `s002b` title | 0.0 % | 0.0 % | Exact |
| `s004a` prose | 0.1 % | — | One error: `Varahamihira` → `Warahamihira` |
| `s010a` verses | 0.5 % | 2.2 % | Highlighter caused no degradation |
| `s010b` table | 5.5 % | 0.2 % | **Latin error is table reading order, not characters** |
| `s051b` chapter | 0.4 % | 3.6 % | Rare conjunct `द्व्ये` → `द्वचे` |

---

## 3. Ranking Across All Criteria

| Criterion | Surya | EasyOCR | Windows OCR | Text layer |
|---|---|---|---|---|
| English fidelity | ★★★★★ | ★★ | ★★★★★ | ★ |
| **Devanagari fidelity** | **★★★★★** | ★★ | ✗ none | ✗ none |
| Reading order | ★★★★☆ (tables scrambled) | ★ (badly jumbled) | ★★★ | ★ |
| Formatting preservation | ★★★★☆ (emits `<b>` for bold headings) | ✗ | ✗ | ✗ |
| Speed | ★★★★★ 2.5 s/page (GPU) · 50 s (CPU) | ★★★ ~12 s/page | ★★★★★ 0.15 s/page | ★★★★★ instant |
| Ease of setup | ★★★ (see §4) | ★★★★ | ★★★★★ built-in | ★★★★★ |
| Reproducibility | ★★★★★ pinned, offline, deterministic | ★★★★ | ★★★ OS-dependent | ★★★★★ |

### Engines not successfully benchmarked

| Engine | Outcome | Operational cost |
|---|---|---|
| **Tesseract** (`san`/`hin`) | **Not tested.** Official Windows build host returns HTTP 403 to scripted download; `winget` offers no user-scope installer. | Would need a manual, interactive install. |
| **OCRmyPDF** | Not tested — depends on a working Tesseract binary. | Blocked by the same issue. |
| **PaddleOCR 3.7.0** | **Failed.** No Devanagari model available for this release; the English pipeline crashed with a oneDNN error (`ConvertPirAttribute2RuntimeAttribute not support`). | High — would need a version downgrade hunt. |
| **Surya ≥ 0.15** | Rejected. Newer releases run the model as a served VLM requiring **Docker/vLLM** or a llama.cpp server. | High. Version **0.14.7** runs directly in PyTorch and was used instead. |
| **Google Vision / Azure Document Intelligence** | **Not attempted.** Requires API credentials, and would mean uploading the full text of copyrighted books to a third-party service. | Deferred — this is the project owner's decision to make, not an automatic one. |

---

## 4. Environment (reproducible)

The main interpreter is Python 3.14, but most OCR stacks have no 3.14 wheels yet. OCR
therefore runs in a dedicated Python 3.12 environment:

```
python 3.12.13            (provisioned via uv)
surya-ocr   == 0.14.7     (torch backend; NOT >=0.15, which requires Docker)
torch       == 2.9.0+cu128
torchvision == 0.24.0+cu128
```

`torchvision` **must** be pinned to `0.24.0+cu128`: resolving it without an explicit local
version tag silently installs the ancient pure-Python `0.2.0` and breaks `torchvision::nms`.
The `cu129` index has no Windows wheel for torchvision, so `cu128` is required.

Hardware used: NVIDIA GeForce RTX 5060 (8 GB), 16 logical cores, 15 GB RAM.
GPU gives a **20× speedup** (2.5 s/page vs 50 s/page) with byte-identical output.

---

## 5. Known Surya Error Classes

These are systematic and mostly correctable deterministically:

| # | Error | Example | Handling |
|---|---|---|---|
| 1 | Visarga `ः` emitted as ASCII colon `:` | `शर्मण:` → `शर्मणः` | Deterministic normalisation |
| 2 | Double danda `।।` emitted as `11` | `11 2 11` → `।। 2 ।।` | Deterministic normalisation |
| 3 | `<math>…</math>` wrappers around digit runs | `<math>(1, 3, 5)</math>` | Strip tags, keep content |
| 4 | `<b>…</b>` on bold headings | `<b>Rajayogas</b>` | Convert to Markdown heading/bold |
| 5 | **Table cell reading order scrambled** | Exaltation table on p. 17 | **Vision pass required** |
| 6 | Rare conjunct misreads | `द्व्ये` → `द्वचे` | Vision verification of verses |

---

## 6. Recommendation

**Adopt a hybrid pipeline: Surya OCR (GPU) → deterministic normalisation → targeted vision
verification.** Do *not* hand-transcribe all 1,177 pages.

1. **Bulk OCR** every page with Surya 0.14.7 on the GPU.
2. **Normalise** deterministically: fix visarga and danda, strip `<math>`, convert `<b>` to
   Markdown, rejoin hyphenated line breaks, drop running headers and page numbers.
3. **Vision-verify the high-value, low-volume content** — every Devanagari shloka and every
   table. These are where Surya's residual ~1.5 % error concentrates, and they are exactly
   the content that must be perfect for a classical-text corpus.
4. **Spot-check English prose** rather than reading every page, since it measures at 0.1–0.5 %.

### Why this over pure manual vision transcription

Manual transcription is not automatically more accurate. During this benchmark **Surya
corrected an error in my own vision reading**: on page 99 I transcribed `पोडश`, where the
printed word is `षोडश` ("sixteen") — Surya read it correctly, and the surrounding English
("making the total sixteen") confirms it. A machine pass plus focused human-grade
verification is more reliable than unaided transcription of 1,177 pages, and roughly
**50× faster** — about one hour of OCR versus an estimated 40+ hours.

### Residual risk, stated plainly

Surya is ~98.5 % accurate on Devanagari, not 100 %. The verification pass in step 3 is what
makes this research-grade; without it, roughly 1–2 characters per shloka would be wrong.
Tables must not be trusted from OCR alone.
