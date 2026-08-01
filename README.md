# AI Vedic Astrologer

Building an AI that interprets Vedic birth charts the way an experienced traditional
astrologer would — and that can prove where every word of its reading came from.

**Current release: `v0.1.0` — the first complete consultation works end to end.**

---

## The vision

Most astrology software either computes a chart and stops, or generates fluent
interpretation with no accountability for where it came from. This project refuses both.

The goal is a system that reads a birth chart in the manner of the classical tradition,
in which **every predictive statement is the application of a rule printed in a real book
to a quantity that was actually calculated.**

One rule governs the whole design:

> **The system may compute, and it may quote. It may not invent.**

That is enforced by machinery, not by good intentions. A language model already knows
Vedic astrology from pretraining and will leak that knowledge into any output it is
allowed to author freely. The architecture is arranged so it never gets the chance:
ten of eleven pipeline stages are deterministic code, and the one stage that produces
prose is handed a closed set of pre-verified, chart-matched, cited claims and permitted
only to compose them.

---

## What works today

```
python -m Engine.cli --date 1987-03-14 --time 04:22 --tz Asia/Kolkata \
    --lat 10.7870 --lon 79.1378 --place "Thanjavur, India" \
    --precision minute --source certificate
```

Produces a consultation in three parts that are never allowed to blur:

| Part | Contents | Voice |
|---|---|---|
| **1 — Objective chart facts** | Sidereal positions, signs, houses, nakshatras, derived fact keys, invariants checked | Computed. No doctrine, no citation. |
| **2 — Activated classical rules** | Every passage in the corpus that applies to this chart, with source, rule card, trigger fact, page anchor and character span | The book's words, verbatim. |
| **3 — Synthesised interpretation** | Where the applicable passages concentrate, and which of their terms recur or contradict | The system's own voice — the only such section. |

Every claim carries four provenance links: the **astronomical quantity** that produced it,
the **derived fact** that matched, the **source book and verse**, and the **exact passage**
with its page anchor. A reader can walk from any sentence back to the scan of the printed
page it came from.

---

## Architecture

Two layers, built in that order.

### Layer 1 — the corpus pipeline (Phase 1, frozen)

Converts scanned Sanskrit/English astrology books into research-grade Markdown. It does
not summarise, modernise or guess; where text is genuinely unreadable it says so.

### Layer 2 — the reasoning engine (Phase 2)

```
birth details
  → Stage 0   resolve time zone, place, uncertainty          (code)
  → Stage 1   compute chart via EphemerisProvider            (code)  → ChartBundle
  → Stage 2   derive typed facts                             (code)  → FactSet
  → Stage 3-5 yogas, strengths, houses                       (code)  [not yet built]
  → Stage 6   activate rule cards by exact predicate lookup   (code)  → Claims
  → Stage 7   adjudicate, weight, measure convergence        (code)  [partial]
  → Stage 8   compose prose                                  (the only authoring stage)
  → Stage 9   verify groundedness from scratch               (code)  ← refuses to emit on failure
  → Stage 10  render                                         (code)
```

### The idea that makes it work: the rule store

Prose cannot be executed, and a model reading prose cannot be trusted to extract the rule
correctly. So between the corpus and the engine sits a layer neither of them contains: a
store of **machine-readable rule cards**, each bound to a byte-exact quote from the corpus
with its character span and SHA-256.

Without it there are only two options, both unacceptable — let a model decide what the
books say (unverifiable), or hardcode astrology into Python (makes the engine the
authority instead of the books, and every new book becomes an engine change).

Rule cards are what make explainability and extensibility real rather than aspirational.
**The engine contains no book names at all**; a test fails the build if one appears.

Two further deliberate choices:

- **Retrieval happens *before* synthesis.** Synthesising first and citing afterwards builds
  a citation-laundering machine whose output is *undetectably* unsourced, because every
  sentence has a footnote.
- **Retrieval is by exact predicate lookup, not embedding similarity.** "Mars in the 7th"
  and "Mars in the 8th" embed almost identically and mean entirely different things. Exact
  lookup also means there is no top-k and no recall cliff: the system knows precisely what
  its books say about a chart.

Full design: [`Reports/PHASE2_SYSTEM_ARCHITECTURE.md`](Reports/PHASE2_SYSTEM_ARCHITECTURE.md).

---

## Repository structure

```
Vedic-AI/
├── Books/            Source PDFs — not tracked (see Books/README.md)
├── Knowledge/        The verified corpus, one Markdown file per book
├── Rules/            Rule cards, per book, each citing the corpus byte-exactly
│   ├── phaladeepika/ 108 cards from chapter 8, plus the book manifest
│   └── tools/        Rule-card proposers (machine proposes, human verifies)
├── Engine/           The Phase 2 reasoning engine
│   ├── ephemeris/    EphemerisProvider ABC + Swiss Ephemeris ctypes adapter
│   ├── chart.py      Stage 0-1  birth details → ChartBundle
│   ├── facts.py      Stage 2    ChartBundle → FactSet
│   ├── rules.py      Rule loading, quote verification, condition evaluation
│   ├── activate.py   Stage 6 + Stage 9
│   ├── synthesis.py  Stage 7c
│   ├── render.py     Stage 8 + Stage 10
│   ├── pipeline.py   Stage orchestration
│   └── tests/        47 tests
├── Pipeline/         The Phase 1 corpus pipeline (frozen)
│   ├── tools/        render, OCR, calibrate, build, verify, audit
│   ├── corpuslib/    Shared conversion library
│   ├── profiles/     Per-book page anatomy — the assembler carries no defaults
│   └── books/        Per-book OCR cache and hand-verified figure transcriptions
├── Ephemeris/        Printed ephemeris tables — not tracked (see its README)
├── Cases/            Generated consultations — not tracked (personal data)
└── Reports/          Architecture, status and benchmark documents
```

---

## Running it

**Prerequisite: Python 3.12.** `pyswisseph` publishes no Windows wheels for any version,
and building from source needs a C toolchain. This project therefore drives Astrodienst's
official Swiss Ephemeris DLL through a small `ctypes` adapter instead, behind an
`EphemerisProvider` interface so `pyswisseph` can replace it later without touching a
single caller.

```bash
# 1. environment
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe tzdata pytest

# 2. fetch the Swiss Ephemeris binaries (not committed — see "Licensing" below)
python Engine/vendor/fetch_swisseph.py

# 3. verify
python -m pytest Engine/tests -q          # expect 47 passed

# 4. your first consultation — prints to stdout
python -m Engine.cli --date 1987-03-14 --time 04:22 --tz Asia/Kolkata \
    --lat 10.7870 --lon 79.1378 --place "Thanjavur, India" \
    --precision minute --source certificate

# 5. or save it, with the full provenance trace
mkdir -p Cases/demo
python -m Engine.cli --date 1987-03-14 --time 04:22 --tz Asia/Kolkata \
    --lat 10.7870 --lon 79.1378 --place "Thanjavur, India" \
    --precision minute --source certificate \
    --out Cases/demo/consultation.md --json Cases/demo/trace.json --audit
```

Useful flags: `--audit` prints the full provenance trace for every claim, `--json <path>`
writes the complete machine-readable case file, `--ayanamsa` and `--houses` override the
defaults.

> `--out` and `--json` do not create directories, and `Cases/` is not in the repository
> (it holds personal data), so `mkdir` it first on a fresh clone.

Time zones are given as **IANA identifiers**, never as a raw UTC offset — the offset is
derived for that instant, so historical rule changes are honoured. Ambiguous and
non-existent local times (daylight-saving transitions) are hard errors that you must
resolve; the engine will not pick one for you.

---

## Completed milestones

**Phase 1 — corpus pipeline** *(frozen)*

- OCR engine benchmarked and selected: Surya 0.14.7, ~1.3% Latin / ~1.5% Devanagari
  character error. See [`Reports/ocr_engine_benchmark.md`](Reports/ocr_engine_benchmark.md).
- **Brihat Jataka** converted and verified — 28 chapters, 408 verses, every chapter
  sequential with no gaps, 219 page anchors.
- **Phaladeepika** converted and verified — 28 chapters, 265 page anchors. First book
  through the frozen pipeline architecture; no redesign was needed.
- **Hallucination detector built.** Surya is a vision model, and on blank page regions
  backed by print on thin paper it invents *fluent* text. 123 invented lines across 14
  pages of Brihat Jataka were found by measuring local contrast in the page image —
  they were undetectable from the text alone.

**Phase 2 — reasoning engine**

- Architecture designed and frozen: [`Reports/PHASE2_SYSTEM_ARCHITECTURE.md`](Reports/PHASE2_SYSTEM_ARCHITECTURE.md).
- `EphemerisProvider` interface with a Swiss Ephemeris 2.10.03 backend.
- 108 rule cards extracted from Phaladeepika chapter 8, every quote verified byte-exact.
- **The first complete consultation runs end to end**, with 47 tests green.

---

## Current capabilities

- Birth-data resolution with IANA time zones, historical offsets, and DST-transition
  detection that refuses to guess.
- Sidereal chart computation — 9 bodies, whole-sign houses, nakshatras and padas,
  retrogradation. Six ayanamsas and six house systems available; Lahiri and whole sign
  are the defaults.
- Positions agree with the printed Astrodienst tables to **under half an arcminute**.
- Rule activation over **planets in the twelve houses** (Phaladeepika ch. 8), for all
  nine bodies including Rahu and Ketu.
- Cited three-part consultation with reader and audit views, plus a JSON trace.
- Groundedness verification that re-derives everything from scratch and **refuses to emit
  a report it cannot verify**.

---

## Current limitations

Stated plainly, because a system like this is only as good as its honesty about its edges.

**Doctrine**

- **One chapter of one book.** Only planet-in-house placements. Nothing on planetary
  strength, house lords, yogas, dashas, transits, or divisional charts — not because
  those texts are silent, but because no rule card addresses them yet.
- Four of the six source books are not yet converted. The corpus pipeline is deliberately
  frozen until measured coverage gaps justify unfreezing it.

**Reasoning**

- **Synthesis matches lexical recurrence only.** In the demo chart `longlived` is asserted
  twice and `shortlived` once, and the system does not connect them — a human astrologer
  would call that the chart's central tension and lead with it.
- Negation is detected by cue words within a fixed window. It is a reading aid, not a
  truth function; the quoted passage is always authoritative.
- "Asserted" means a word stands un-negated in its passage, **not** that the passage is
  favourable. *"Troubled by the enemies"* asserts *enemies*.
- Stage 7 adjudication is unexercised: with one chapter there is nothing to adjudicate.
- Stage 8 uses **no language model**. It composes by quotation, which is the honest floor
  rather than a placeholder; the `Synthesizer` protocol is the seam where a model-backed
  one drops in under the same Stage 9 gate.

**Calculation**

- No interval-mode birth-time stability analysis. The engine warns on *declared*
  precision but does not yet report *actual* sensitivity — a chart with the ascendant at
  29.89° of a sign flips every house placement on half a minute of error.
- The ayanamsa and node type are engine choices, not doctrine; the classical texts specify
  neither. They are recorded as unsourced in every chart bundle.
- Chart validation is against Astrodienst's printed tables, which are themselves generated
  by the Swiss Ephemeris. That checks our code path, not the library. A genuinely
  independent oracle is still owed.

---

## Roadmap

Ordered by what unblocks the most, not by what is most visible.

| Next | Why it comes first |
|---|---|
| **Interval-mode stability analysis** | A correctness gap, not a feature. Every conclusion in an ascendant-sensitive chart is currently reported with more confidence than the birth time supports. |
| **Phaladeepika ch. 9 — ascendants** | Needs only the `lagna_sign` predicate, which already exists. Cheapest possible proof that adding doctrine requires no engine change. |
| **Phaladeepika ch. 19–20 — dashas** | The first genuinely new calculator, and the step from a static reading to a timed one. Vimshottari is fully sourceable from ch. 19. |
| **Strength (ch. 4) and house assessment (ch. 15–16)** | Turns a flat list of activated rules into a weighted one, which is what Stage 7 needs to do real work. |
| **A second book** | Only once the gap log shows a specific recurring need. Adding a book must change no engine code — that is the test. |

Longer term: model-backed synthesis behind the existing verification gate, and the
remaining four source books as coverage demands them.

---

## Corpus principles

The corpus is a faithful reproduction of the source texts, not a summary or a
modernisation. These rules are not negotiable and carry forward into Phase 2.

- Preserve the original wording exactly. No summarising, rewriting or modernising.
- Omit nothing — chapter and section titles, verse numbers, Devanagari, transliterations,
  tables, lists, footnotes and appendices are all retained.
- Remove only page numbers, repeated running headers/footers and scanning artefacts.
- Correct an OCR error only where the surrounding context makes the correction certain.
- Where text is genuinely unreadable, mark it `[UNCLEAR]` rather than guessing.
- **Defects in the source are preserved as printed and flagged, never silently fixed.**
  One Ashtakavarga chart in Phaladeepika totals 44 bindus where it must total 48; it is
  transcribed exactly as printed, with the discrepancy recorded.

---

## Source books

| Book | Author | Pages (PDF) | Text layer | Status |
|---|---|---|---|---|
| Brihat Jataka | Varahamihira, tr. P. S. Sastri | 115 spreads / 230 pages | OCR, corrupt | **Converted & verified** |
| Phaladeepika | Mantreswara, tr. G. S. Kapoor | 265 | Clean digital | **Converted & verified** |
| Brihat Parasara Hora Sastra, Vol. 1 | Maharishi Parashara | 482 | OCR, corrupt | Pending |
| Jataka Parijata, Vol. 1 | Vaidyanatha Dikshita | 324 | OCR, severely corrupt | Pending |
| Uttara Kalamrita | Kalidasa, tr. P. S. Sastri | 256 | OCR, corrupt + 75 blank pages | Pending |
| Saravali | Kalyana Varma | 203 | Clean, but diacritics lost in the source PDF | Pending |

Per-book defects and conversion notes: [`Reports/PROJECT_STATUS.md`](Reports/PROJECT_STATUS.md).

---

## Notes on data and licensing

**Source PDFs are not tracked.** They are scans of published, in-copyright works — inputs
to the pipeline, not products of it, and not ours to redistribute. Everything *derived*
from them is committed. See [`Books/README.md`](Books/README.md).

**`Ephemeris/` holds printed tables, not ephemeris data.** The 41 PDFs there are
Astrodienst's published yearly tables, not Swiss Ephemeris `.se1` files. They are useful
as a validation oracle; they do **not** bound the engine's date range, which is
effectively unbounded for human births.

**The Swiss Ephemeris is dual-licensed (AGPL or commercial)** and its binaries are not
committed. `Engine/vendor/fetch_swisseph.py` retrieves them from the official upstream
repository and verifies the DLL against the size and CRC-32 published in upstream's own
manifest before writing it.

**Line endings are load-bearing here.** Rule cards cite the corpus by character offset, so
`.gitattributes` marks `Knowledge/` and `Rules/` as `-text`. Without that, an LF checkout
would shift every offset in `phaladeepika.md` by up to 5,969 characters and break
verification on every card outside Windows.
