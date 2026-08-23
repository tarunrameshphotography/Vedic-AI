# VEDIC-AI MASTER PROJECT MILESTONES

**Project purpose:** Build an AI that reads a Vedic birth chart the way a traditional
astrologer would, where every predictive sentence traces to a rule printed in a real book
applied to a quantity that was actually computed. Governing rule: *the system may compute,
and it may quote — it may not invent.*

**Current production-readiness: 49%** (see §A for the weighted breakdown). **This is not a
9-point jump in capability.** §A's published category scores and weights have always summed
to 48.30%, not the 39.55% the file stated; the per-milestone *increments* were computed
correctly but the base was wrong and carried forward unchanged for four milestones. Milestone
19 recomputed it from the same categories and weights (§A) and corrected the arithmetic. Real
movement this session is +2 provenance and +1 test coverage, i.e. about +0.3 points.

**Current phase:** Production Blocker Clearance Program (interrupts ordinary Phase 3
rule extraction — see §J and §K). Phase 3 itself remains at the state described in §B.

**Current milestone:** Milestone 19 — verification queue, chapter 10 batch (36 cards; 1
defect corrected, 1 documented and held unsigned, 2 prior claims corrected), which **closes
the interpretive verification queue** and clears blocker P1-1. The same session found a new
production blocker, **P0-2, the benefic classification gap** — see §K.

**Exact resume point:** `git fetch --all --prune`, confirm `main` == `origin/main`, then
read §K, **P0-2**. Do not resume ordinary chapter encoding first: 22 active cards across
chapters 6 and 10 systematically under-fire today because Jupiter and Venus receive no
`nature` fact at all, and P0-2 needs a human decision between three real sources before any
of it can be encoded. The verification queue (P1-1) is finished apart from two deliberate,
documented holdouts and needs no further work.

**Current Git SHA:** `86047e98db2775de11c58d5924fb5d3c1d66c42b` (parent — this milestone's
own commit follows this file's checkpoint)
**Last verified remote SHA (origin/main):** same before this milestone's commit — 0 ahead /
0 behind, working tree clean
**Last update date:** 2026-08-23

**Current test count:** 241 passing (`Engine/tests`) — was 233
**Current rule-card counts:** 405 total · 385 executable (firing) · 20 inert (recorded, blocked)
— unchanged this session; Milestone 19 corrected a condition in place and split no cards.
**Current verification:** **403/405 cards signed off (99.5%)** — was 368/405 (91%), and 4/404
(1%) before Milestone 15. 175 structural (reference/table) cards signed off by automated
structural check; 228 interpretive cards signed off by human(+Claude) reading pass (3
pre-existing + 20 chapter 9 + 8 of chapters 1-2 + 53 of chapter 6 + 109 of chapter 8 + 35 of
chapter 10). **The interpretive queue is closed.** Exactly two cards remain deliberately
**unsigned**, both for real, documented condition defects blocked on capabilities that do not
exist:
  - `PD.01.Kalapurusha.Strength` — found in Milestone 16; needs `dep.strength` +
    `dep.condition-variables`. Its Milestone 16 note was **corrected** in Milestone 19: it
    claimed the stub leaf was "vacuously true"; it is vacuously *false* (see §I, "any" is a
    literal, not a wildcard), which points the eventual repair the other way.
  - `PD.10.Venus.VargaMarsSaturn` — found in Milestone 19; its varga branch does not encode
    "the Varga of Mars or Saturn" and repairing it requires deciding what "Varga" denotes,
    which belongs to whoever encodes chapters 3/21, not to a review pass.

**Backlog:** 89 entries (20 card, 44 passage, 22 chapter, 3 concept), 0 resolved

---

## A. PRODUCTION READINESS

Weighted categories. Weights reflect how much of the project's stated vision (README:
*"the system may compute, and it may quote — it may not invent"*, end-to-end cited
consultations) each category gates. Card count is deliberately **not** a category on its
own — it feeds "Rule extraction" but does not define readiness by itself, per the vision's
own warning that a system can have many cards while lacking reasoning capability.

| Category | Weight | Score | Rationale |
|---|---:|---:|---|
| Corpus completeness | 15% | 25% | 2 of 6 planned books converted and frozen (Brihat Jataka, Phaladeepika); 4 pending (BPHS, Jataka Parijata, Uttara Kalamrita, Saravali) behind a deliberate freeze. |
| Source verification | 10% | 70% | Corpus pipeline verified byte-exact with hallucination detection, verse reconciliation, figure transcription for the 2 converted books; Devanagari glyph-level spot-check still owed on Brihat Jataka. |
| Rule extraction/encoding | 20% | 36% | Phaladeepika chapters 1, 2, 8, 9, 10 encoded and 6 partially (through v.38 of ~70); 405 cards (one card split into two during verification, not new corpus material) from an estimated ~1,535 total across all 28 Phaladeepika chapters at the measured 0.65 cards/paragraph rate — and that is one book of six. |
| Reasoning engine capability | 15% | 45% | Stages 0, 1, 2, 6, 9, 10 implemented; Stage 3-5 (yogas/strength/houses as first-class computation) not built as dedicated stages; Stage 7 (adjudication) only partial (synthesis exists, weighting/cancellation does not); no varga, dasa, transit, ashtakavarga, or strength calculators yet. **This score is now known to overstate effective capability** and is held only because Milestone 19's discovery is a doctrine-coverage gap rather than an engine one: Jupiter and Venus receive no `nature` fact on any chart, so all 22 active cards conditioning on `benefic` systematically under-fire (§K, P0-2). Revise this score when P0-2 is decided. |
| Contradiction handling | 10% | 55% | Competing authorities are preserved via `contradicts`/`extends` links and dual cards (e.g. PD.01 rising-sign dispute, PD.09 dignity dispute) — the mechanism works and is used repeatedly, but Stage 7 adjudication (weighing contradictions against each other) does not exist yet. |
| Provenance/auditability | 10% | 97% | Every card is byte-exact hash-verified against the corpus on every run; `verify.py` enforces this as a build gate. `extraction.verified_by` now covers **403/405 cards (99.5%**, was 4/404) via `Rules/tools/review.py`: 175 structural cards signed off automatically (no interpretive layer to review — the byte-exact check already is the complete verification), 228 interpretive cards signed off by an actual human(+Claude) reading pass across chapters 1, 2, 6, 8, 9 and 10. The interpretive queue is closed; the 2 unsigned cards are deliberate, documented defect holdouts, not unreviewed cards. Not 100% because those two defects are real and still open. |
| Test coverage | 10% | 63% | 241 tests (was 233), growing with every milestone, covering rule structure, engine extractors, variable binding, overrides, the verification tool itself, and now the chapter 10 verification batch's findings (the missing inimical-sign disjunct, and a test pinning that `"any"` is a literal so every inert stub condition is fail-safe); no dedicated end-to-end regression suite across the full corpus of encoded chapters yet. |
| End-to-end validation | 5% | 30% | CLI produces full 3-part consultations and has been spot-checked against real charts per milestone; no systematic charted validation set (Phase 6 of `Phases.txt`) exists yet. |
| Multi-book corroboration | 3% | 0% | Only one book (Phaladeepika) has cards in the store; Brihat Jataka is corpus-converted but has zero rule cards. Cross-book agreement (a Phase 4 goal) cannot be assessed with one book. |
| Production safety/reliability | 1% | 50% | Groundedness verification (Stage 9) refuses to emit ungrounded output; no rate limiting, error-recovery, or production deployment hardening attempted (not yet in scope). |
| CLI/API/user-facing readiness | 1% | 40% | Working CLI (`Engine/cli.py`) produces real consultations; no API, no UI, no packaging. |

**Overall Production Readiness: 0.15×25 + 0.10×70 + 0.20×36 + 0.15×45 + 0.10×55 + 0.10×97 +
0.10×63 + 0.05×30 + 0.03×0 + 0.01×50 + 0.01×40 = 48.60% ≈ 49%**

**Arithmetic correction (Milestone 19).** The previous line claimed this expression equalled
39.55%. It does not, and never did: with the same eleven categories, the same weights (which
sum to exactly 100) and the same scores, it comes to 48.30%. The error was in the *base*, not
in the updates — each milestone's increment (e.g. provenance 90→95 adding 0.10×5 = 0.5 points,
39.05→39.55) was applied correctly on top of a wrong starting figure and carried forward
unchanged through Milestones 15-18. Milestone 15's §J.1 audit checked whether the *categories
and weights* were sound (they are) but did not re-evaluate the sum itself, which is how the
error survived an audit explicitly aimed at this number.

So the headline figure moves 40% → 49%, of which **about 8.7 points are the correction and
about 0.3 points are this session's actual progress** (+2 provenance, +1 test coverage). Do
not report this as capability gained. It also means the project has been *under*-reporting
itself for several milestones — the opposite of the inflation §J.1 was looking for — while
simultaneously, per P0-2, overstating what its reasoning actually delivers on a real chart.
Both are corrected here rather than one being used to offset the other.

This number should be recomputed (not incremented by feel) whenever a category's score
changes materially — see §16.

---

## B. PHASE STATUS

| Phase | Purpose | Status | Completion | Evidence | Remaining |
|---|---|---|---:|---|---|
| Phase 1 | Corpus & OCR | **Not complete — documentation overstates it** | 33% | 2 of 6 books converted, verified, frozen (`Knowledge/brihat-jataka.md`, `Knowledge/phaladeepika.md`). `Phases.txt` marks "Phase 1 — Corpus & OCR" with a ✅, which is **inaccurate**: 4 books (BPHS Vol.1, Jataka Parijata Vol.1, Uttara Kalamrita, Saravali) are audited but not yet OCR'd/converted (`Reports/PROJECT_STATUS.md`). The pipeline architecture itself is frozen and proven across two structurally different books, which is what "frozen" refers to — not full corpus completeness. | Convert and verify the remaining 4 books; get Devanagari glyph-level spot-check on Brihat Jataka; write `Reports/conversion_report.md`. |
| Phase 2 | Reasoning engine architecture | Core MVP complete; extensions ongoing | 55% | Stages 0,1,2,6,9,10 fully implemented (`Engine/chart.py`, `facts.py`, `activate.py`, `render.py`, `pipeline.py`). 13 fact extractors implemented (`Engine/facts.py`): lordship, sign classes, house classes, graha classes, aspects, combustion, dignity, dignity-friendship, occupant count, graha frame, conjunction, nature, nature occupancy. Stages 3-5 (yoga/strength/house computation as dedicated stages) and Stage 7 (adjudication) are the largest open items — see `dep.strength`, `dep.varga`, `dep.dasa`, `dep.adjudication`, `dep.ashtakavarga`, `dep.transit`, `dep.vargottama`, `dep.upagraha` in `Rules/deferred.json`, all currently `implemented: false`. | Build `dep.strength` (Stage 4, highest closure-unlock return), `dep.varga`, `dep.dasa`, `dep.adjudication`, `dep.ashtakavarga`, `dep.transit`. |
| Phase 3 | Classical Knowledge Extraction | In progress | 26% | 404 cards from Phaladeepika chapters 1, 2, 6 (partial), 8, 9, 10 of 28 total chapters; 0 cards yet from Brihat Jataka despite it being corpus-converted. Estimated ~1,535 total cards across all 28 Phaladeepika chapters at the measured 0.65 cards/paragraph rate (`Reports/PHASE3_PLAN.md`), so 404/1535 ≈ 26% of just this one book, before Brihat Jataka or the 4 unconverted books are touched at all. | Continue chapter-by-chapter encoding (ch. 3, 4, 5, 6 remainder, 7, 11-28); start Brihat Jataka extraction; resolve `concept:manual-verification` (human sign-off, currently 368/405 cards, see §K P1-1). |
| Phase 4 | Knowledge Integration | Not started | 5% | `dep.adjudication`, `dep.rule-transfer` (implemented), `dep.dignity-override` (implemented) exist as primitives but no rule-priority/weighting/cancellation system exists. Contradictory cards are recorded and linked but never adjudicated against each other at query time. | Design and build Stage 7 adjudication: conflict detection, priority, weighting, cancellation, cross-book agreement scoring. |
| Phase 5 | Consultation Intelligence | Not started | 10% | Stage 8 (compose prose) and part of Stage 7 (synthesis, grouping/recurrence) exist (`Engine/synthesis.py`, `render.py`) and produce a real 3-part consultation today, but there is no contradiction-explaining or cross-book-convergence narrative yet — that needs Phase 4 first. | Build after Phase 4 adjudication exists. |
| Phase 6 | Validation | Not started | 0% | No charted validation set, no celebrity/historical chart corpus, no accuracy measurement exists yet. Individual milestones are spot-checked against 1-2 real charts each (ad hoc), which is not the same as this phase. | Build hundreds of known charts and measure prediction accuracy, per `Phases.txt`. |
| Phase 7 | Research Platform | Not started | 0% | Depends on Phase 4 (cross-book comparison) and Phase 6 (validated data) neither of which exist yet. | Not actionable yet. |
| Phase 8 | Expert System | Not started | 0% | Depends on Phases 4-7. | Not actionable yet. |
| Production | Ship-readiness | Not started | 15% | CLI works end-to-end for one book; no API, UI, packaging, or deployment hardening. | See §8 "Production blockers". |

---

## C. COMPLETED MILESTONES

Reconstructed from `git log` (25 commits total as of `978998a`) and `Rules/deferred.json`
provenance notes. Chronological.

### Milestone 1 — Initial commit: verified classical corpus and Phase 2 reasoning engine MVP

**Phase:** 1 (frozen scope) + 2
**Scope:** Repository bootstrap
**Status:** COMPLETE
**Completion:** 100%
**Commit:** `06f6082`
**Remote:** VERIFIED

**What was built:** Corpus pipeline (Phase 1, frozen) converting scanned Sanskrit/English
astrology books to research-grade Markdown without summarizing or guessing, including a
show-through hallucination detector (found 123 invented lines across 14 pages of Brihat
Jataka via local-contrast measurement). Reasoning engine MVP (Phase 2): birth details →
`EphemerisProvider` → `ChartBundle` → `FactSet` → rule activation → verification → cited
consultation.

**What was encoded:** 108 rule cards from Phaladeepika chapter 8, each bound to a
byte-exact quote with a SHA verified on every run.

**Engine changes:** Full pipeline skeleton (Stages 0,1,2,6,9,10). `EphemerisProvider` ABC
+ Swiss Ephemeris ctypes adapter (chosen because `pyswisseph` publishes no Windows wheels).

**Tests:** 47.

**Important architectural decisions:** Rule store as an intermediate layer between corpus
and engine (neither hardcodes doctrine); retrieval-before-synthesis; exact predicate
lookup instead of embedding similarity; the engine contains no book names at all (enforced
by a failing test).

**Source ambiguities/defects preserved:** N/A at this granularity — bootstrap commit.

**Dependencies unlocked:** N/A — this is the baseline.

**Why this milestone matters:** Establishes the entire architectural contract everything
after it depends on.

---

### Milestone 2 — Phaladeepika chapters 9 and 10 encoded

**Phase:** 3
**Scope:** 23 + 38 = 61 cards
**Status:** COMPLETE
**Commit:** `155e42a` (ch.9, 23 cards), `1df0fe0` (ch.10, 38 cards)
**Remote:** VERIFIED

**What was encoded:** Chapter 9 and chapter 10 doctrine, including the first
sex-scoped-rule and second-nativity deferrals that later shaped `dep.native-sex` and
`dep.second-nativity`.

**Why this milestone matters:** First proof the toolchain and card schema generalize past
chapter 8.

---

### Milestone 3 — Deferred-knowledge registry and Phase 3 ranking tools

**Phase:** 3 (process)
**Status:** COMPLETE
**Commit:** `1094020` (deferred-knowledge registry), `5124171` (rank Phase 3 by executable
knowledge unlocked per unit of work), `37bc308` (encoding toolchain: `build_chapter.py`,
`verify.py`, `dupes.py`)

**What was built:** `Rules/deferred.json` as the permanent record of everything
deliberately not encoded, with dependency tracking so no knowledge silently disappears.
`Rules/tools/leverage.py`-style ranking of what capability to build next by cards
unlocked ÷ effort — this is the same method `Reports/PHASE3_PLAN.md` still uses today.

**Why this milestone matters:** Without this, deferred work would be invisible to future
sessions — this is the direct ancestor of this very `MILESTONES.md` file's discipline.

---

### Milestone 4 — Two highest-return engine capabilities

**Phase:** 2
**Status:** COMPLETE
**Commit:** `bbd9597`

**What was built:** The two capabilities the ranking tool identified as highest-return at
that point (lordship and a related extractor — see `Engine/facts.py` `_lordship`).

---

### Milestone 5 — Phaladeepika chapters 1 and 2 encoded

**Phase:** 3
**Scope:** 94 + 82 = 176 cards
**Status:** COMPLETE
**Commit:** `3608ab6` (ch.1, 94 cards), `a993107` (ch.2, 82 cards)
**Remote:** VERIFIED

**Source ambiguities/defects preserved:** Rising-sign verse-8 self-contradiction (5 vs. 6
Prishtodaya signs), Rasi-Sandhi definition dispute, nodal exaltation 3-way dispute, natural
friendship table column-interleaving (OCR/pdf_text defect), Sun-as-father-significator
dispute (v.1 vs. v.25), substances table "Cold" for Jupiter defect — all documented in
`Rules/phaladeepika/manifest.json` `known_defects`.

---

### Milestone 6 — Six doctrine-backed extractors, quantified conditions, dignity-override, counting/reference-frames, rule-transfer, natural-friendship table

**Phase:** 2 + 3
**Status:** COMPLETE
**Commits:** `c0f3b92` (six extractors reading only from reference cards), `e6d7df9`
(`dep.condition-variables`), `30f1bc1` (counting, reference frames, benefic/malefic
nature), `14125a4` (`dep.dignity-override`), `e66632d` (natural-friendship table from
verified source page 22), `e17e524` (`dep.dignity-friendship` extractor), `04dfba7`
(`dep.rule-transfer`)

**Engine changes:** Aspects, combustion, dignity, dignity-friendship, occupant-count,
graha-frame, conjunction, nature, nature-occupancy extractors — the bulk of
`Engine/facts.py`'s current capability. Condition-variable schema (multi-variable
conditions). Dignity-override mechanism. Rule-transfer mechanism (a card can state its
effect "shares with" another card's already-encoded effect instead of restating it).

**Important architectural decisions:** Doctrine-backed extractors read *only* from
reference cards already in the store — the engine never hardcodes a classification the
corpus itself states (e.g. which signs are benefic/malefic).

**Why this milestone matters:** This is the single largest capability jump in the
project's history — it is what made chapter 6 (yoga-dense, lordship/dignity/aspect-heavy)
encodable at all.

---

### Milestone 7 — Phaladeepika chapter 6, slice 1: Pancha Mahapurusha Yogas

**Phase:** 3
**Scope:** vv. 1-4 (p.55-57)
**Status:** COMPLETE
**Commit:** `c3b62dc`
**Remote:** VERIFIED

**What was encoded:** `PD.06.Ruchaka/.Bhadra/.Hamsa/.Malavya/.Sasa` — the five Pancha
Mahapurusha Yogas, two-span cards (naming clause + effect verse).

**Source ambiguities/defects preserved:** Verse 9's blanket strength caveat recorded once
rather than duplicated per card (`passage:phaladeepika.06.p009`, blocked on
`dep.strength`). The closing sentence (also true from the Moon; compounds when multiple
fire) deferred as `passage:phaladeepika.06.p022` rather than widened or invented — needs
`dep.yoga-combination-count`. Four illustrative horoscope clusters (Stalin, Dr.
Radhakrishnan, Moti Lal Nehru) excluded as tier-3 apparatus.

---

### Milestone 8 — Chapter 6, slice 2: the twelve house-wise yogas

**Phase:** 3
**Scope:** vv. 44-56 (p.55-57 region continues elsewhere in ch.6)
**Status:** COMPLETE
**Commit:** `e13ab32`

**What was encoded:** Chamara, Dhenu, Shaurya, Jaladhi, Chhattra, Astra (6th and 8th house
variants, kept distinguished), Kama, Bhagya, Khyati, Parijata, Musala — one repeating
template carried forward from item 1's full statement into items 2-12's "similarly
disposed" shorthand, exactly as the source instructs.

**Source ambiguities/defects preserved:** Sunapha/Anapha/Durudhara cluster investigated
and explicitly set aside — the text states the collective condition but never names which
sub-condition maps to which yoga name; deferred as `passage:phaladeepika.06.p031` rather
than importing the convention from outside the passage.

---

### Milestone 9 — Chapter 6, slice 3: vv. 14-27

**Phase:** 3
**Status:** COMPLETE
**Commit:** `edddad5`

**What was encoded:** Mahabhagya (sex-scoped; day/night birth read as Sun above/below
horizon, an engine choice recorded as such rather than asserted by the verse), Kesari,
Sakata (with cancellation clause), Adhama/Sama/Varishtha (from the Sun), Amala,
Subhamala/Asubhamala (two different printed spellings preserved), Lakshmi, Gouri,
Saraswati Yogas.

**Source ambiguities/defects preserved:** Vasumati Yoga (`PD.06.Vasumati`) recorded
inert — universally quantified over the variable-membership set of benefic grahas,
needing a new `dep.universal-quantification` combinator, not an extension of an existing
one. Pushkala Yoga (`PD.06.Pushkala`) inert on three independent grounds (`dep.strength`,
an unresolved "together in a Kendra" reading, an undefined "Adhimitra" friendship tier).

---

### Milestone 10 — Chapter 6, slice 4: vv. 5-7, Kemadruma

**Phase:** 3
**Status:** COMPLETE
**Commit:** `393875f`

**What was encoded:** Mantreswara's own Kemadruma Yoga definition (absence of the three
Moon-adjacency yogas).

**Source ambiguities/defects preserved:** Two competing Kemadruma definitions (Saravali's,
Hora Sara's) deferred pending `dep.manual-verification`, not merged or resolved.

---

### Milestone 11 — Chapter 6, slice 5: vv. 8-13, Vesi/Vasi/Ubhayachari/Kartari/Susubha

**Phase:** 3
**Status:** COMPLETE
**Commit:** `3cbaa7e`

**Source ambiguities/defects preserved:** Translator's editorial preference for
Mantreswara's benefic/malefic reading over "authoritative works" recorded as tier-3
apparatus, not doctrine. Susubha/Subhakartari/Subhavesi's rule-transfer to
Sunapha/Anapha/Durudhara deferred (`dep.manual-verification`) because the source of that
transfer doesn't exist as a card yet (that cluster is itself still deferred).

---

### Milestone 12 — Chapter 6, slice 6: vv. 28-34, Srikantha/Srinatha/Virinchi and Maha/Dainya/Kahala

**Phase:** 3
**Status:** COMPLETE
**Commit:** `3a6346c`

**Source ambiguities/defects preserved:** Verse 32's itemized Notes lists (Maha/Dainya/
Kahala Parivartana pairs by name) recorded as redundant tier-2 apparatus — verse 32 itself
already states the complete classification rule in intact prose.

---

### Milestone 13 — Chapter 6, slice 7: vv. 35-36, Parvata and the dispositor-chain Kahala Yoga

**Phase:** 3
**Status:** COMPLETE
**Commit:** `e9741e2`

**Important architectural decisions:** Confirmed the dispositor-chain doctrine (a planet's
lord's lord's...) could be represented using existing predicates without introducing a new
`dispositor_chain()` predicate — a "don't build speculative architecture" precedent this
file's §12 now records permanently.

---

### Milestone 14 — Chapter 6, slice 8: vv. 37-38, Raja Yoga and Shankha Yoga

**Phase:** 3
**Status:** COMPLETE
**Completion:** 100%
**Commit:** `978998a`
**Remote:** VERIFIED

**What was built/encoded:** `PD.06.RajaYoga`, `PD.06.Shankha` — 9th/10th lord
conjunction/kendra-trikona doctrine, using only existing predicates (`lord_of_house`,
`in_house`, `house_class`). No engine changes required.

**Tests:** +9 (222 → 224), covering positive/negative firing, the same-graha edge case,
the Raja⊂Shankha overlap, provenance, exact transcription.

**Important architectural decisions:** Raja Yoga is structurally a specific case of the
general Shankha Yoga (9th=trikona, 10th=kendra) — both legitimately fire together on the
same chart; documented as not-a-duplicate rather than merged.

**Source ambiguities/defects preserved:** "Auspicious house" has two different corpus
definitions (ch.1 v.17 general definition vs. a narrower kendra-or-trikona gloss found
once elsewhere) — the general definition was used since it's the term this verse invokes,
and the narrower alternate reading documented in the card's `note`, not silently chosen.

**Dependencies unlocked:** none.

**Why this milestone matters:** Most recent Phase-3 checkpoint before this session's
production-blocker audit interrupted ordinary extraction (see §J).

---

### Milestone 15 — Production blocker audit, and the human(+Claude) verification workflow

**Phase:** Production Blocker Clearance Program (not ordinary Phase 3)
**Status:** COMPLETE
**Completion:** 100%

**What was audited:** A full read-only pass over `MILESTONES.md`, `Phases.txt`,
`Reports/PHASE3_PLAN.md`, `Reports/PHASE3_BACKLOG.md`, `Rules/deferred.json`, the engine
capability matrix, and the corpus/dependency catalogue, followed by running
`verify.py`/`dupes.py`/`pytest` for objective evidence. Conclusion: the existing 39%
figure and its weighting are not inflated and did not need methodology correction (see
§J.1) — this audit's only material finding was a genuinely new blocker not previously
named in this file: **there was no systematic workflow for human verification at all**,
only 4 cards signed off ad hoc when a dispute forced the question.

**What was built:** `Rules/tools/review.py` — draws the one distinction that actually
determines whether a card needs a human: **structural** cards (`activation: "reference"`,
i.e. tables/classifications quoted directly, no interpretation between quote and card) are
signed off automatically, because `verify.py`'s byte-exact check already is the complete
verification such a card can receive; **interpretive** cards (the condition/effect binding
is a judgment call) are queued into `Reports/VERIFICATION_QUEUE.md` for an actual reading
pass. This directly answers the audit brief's question of "whether automated source
verification is sufficient for some classes" — yes, for structural cards, and the tool now
enacts that rather than leaving it a discussion.

**What was verified:** 175 structural cards signed off automatically (`--sign-structural`).
Then, as a bounded proof that the interpretive queue is actually workable, all 20 queued
interpretive cards of chapter 9 (Phaladeepika) were read against their quoted verses one by
one and signed off in the same `"tarunrameshphotography + Claude (...)"` style already
established by the 4 pre-existing sign-offs — no defects found; every condition and
`predicts` block was confirmed to faithfully represent its quote, including the dasa-vs-
natal timing distinctions and the two cards correctly marked inert for undeliverable
predicates. Verification moved from 4/404 (1%) to 198/404 (49%). 206 interpretive cards
(chapters 1, 2, 6, 8, 10 in full) remain queued — this is not claimed as cleared, it is
explicitly the next resume point (§K, blocker P1-1).

**Tests:** +6 (224 → 230): `Engine/tests/test_review.py` covers the structural/interpretive
classification, that a dry run never writes, that applying is idempotent, that
`manifest.json` is never touched, that the real store's queue excludes every already-signed
card, and that the rendered report is stable markdown.

**Important architectural decisions:** Verification sign-off does not require a literal
human alone; the project's own precedent (`PD.02.Friendship.NaturalTable`, `PD.09.*`
dignity-friendship cards) already records `"tarunrameshphotography + Claude"` jointly, and
this milestone formalizes that as the standing pattern rather than inventing a new one —
see §I.

**Why this milestone matters:** Establishes the mechanism the project's own §H/§I already
called for ("design a realistic verification workflow... whether verification can be done
systematically rather than manually card-by-card") without fabricating sign-off it hadn't
actually earned, and without building the far larger, doctrine-heavy `dep.strength` chain
that was the more obvious "highest-leverage" pick but not completable end-to-end in one
session (see §J.4 for why it was not chosen first).

---

### Milestone 16 — Verification queue, chapters 1-2 batch

**Phase:** Production Blocker Clearance Program (P1-1)
**Status:** COMPLETE
**Completion:** 100%

**What was verified:** All 9 interpretive cards queued from chapters 1-2 (2 in ch. 1, 7 in
ch. 2), read one by one against their quoted verses (`Knowledge/phaladeepika.md`) and,
for the two the note flagged as extraction-ambiguous, against the rendered source PDF page.
8 of 9 were confirmed faithful and signed off; 1 (`PD.01.Kalapurusha.Strength`) was found to
have a genuine condition defect and was deliberately **not** signed off — see below.
Verification moved from 198/404 (49%) to 206/404 (51%).

**Defects found (per the audit brief's instruction not to silently fix or hide these):**

1. **`PD.01.Kalapurusha.Strength` (left unsigned, queued).** The quote states three
   alternative causes of a strong house (occupied by a benefic, aspected by a benefic, or
   its lord bestowed with strength); the encoded condition carries only two leaves, omits
   the "occupied" (`in_house`) case entirely, and its `lord_of_house(any,any)` leaf doesn't
   test strength at all — every house always has a lord, so that leaf is vacuously true as
   written. Currently harmless (the card is `inert` and never evaluated), but the condition
   would need real correction, not just a dependency removal, whenever `dep.strength` +
   `dep.condition-variables` land. Documented in the card's own `note`, not fixed — fixing it
   now would be choosing the correction during a verification pass rather than deferring the
   choice to whoever actually builds those capabilities, per the instruction to preserve
   rather than silently resolve.
2. **`PD.01.SignBodyForm.Table` (signed off, note corrected).** The prior session's claim
   that this sign-classification table is irreducibly ambiguous — based on the flattened
   `pdf_text` extraction reading as jumbled columns — was checked against the rendered PDF
   page (printed p.13, 300 dpi) and found **incorrect**: the printed table is a clean,
   standard four-column layout matching the classical Dwipada/Chatushpada/Keeta/Jalachara
   classification. The card's actual quote and `predicts` don't overclaim anything (they only
   name the four classes, assert no mapping), so nothing currently encoded was wrong — signed
   off — but the note is corrected, and a future Phase 3 session should properly encode the
   full table as a reference card now that the ambiguity is resolved. Not done in this
   verification pass, which does not extract new doctrine.
3. **`PD.02.Form.Mars.Youthful` (signed off, metadata corrected).** `requires` listed
   `dep.lord-of-house` as a blocker; that capability has been implemented since Milestone 4
   and is used throughout the store, so it was stale bookkeeping, not a real blocker —
   corrected to `dep.strength` alone (the doctrine — conditions/predicts — was untouched).
   `Reports/PHASE3_BACKLOG.md` and `Reports/PHASE3_PLAN.md` regenerated to match.
4. **`PD.02.Prashna.ReservoirWater` (signed off, metadata corrected).** `timing` said
   `"natal"` though the card's own note says this is a horary (query-moment) rule. Confirmed
   this was harmless today — `timing` is not read anywhere in `Engine/` yet (grepped) — but
   corrected to `"query"`. Separately confirmed, by reading `Engine/activate.py`, that this
   card's condition (six houses for the Moon, exactly expressible on a natal chart) *cannot*
   fire on a natal chart regardless: `activate()` skips any `activation == "inert"` card
   before its condition is ever evaluated. The domain-crossing risk this card represents is
   real in principle but structurally closed, not just closed by convention.

**Tests:** unchanged at 230 (this batch corrected data and documentation, not engine code);
`Reports/PHASE3_BACKLOG.md` and `Reports/PHASE3_PLAN.md` regenerated after the
`dep.lord-of-house` correction so `test_backlog_report_is_current` stays green.

**Why this milestone matters:** First proof that the verification pass finds real things —
not just a rubber stamp. One genuine, still-open condition defect was found and preserved
rather than hidden or silently patched; two stale metadata claims were corrected without
touching doctrine; one prior claim of irreducible ambiguity was checked against the primary
source (the rendered PDF) and shown to be wrong.

---

### Milestone 17 — Verification queue, chapter 6 batch (53 cards)

**Phase:** Production Blocker Clearance Program (P1-1)
**Status:** COMPLETE
**Completion:** 100%

**What was verified:** All 53 interpretive cards queued from chapter 6 — the Pancha
Mahapurusha family (5), the twelve house-wise yogas (12), Mahabhagya male/female (2),
Kesari/Sakata/Varishtha/Sama/Adhama (5), Amala/Vasumati/Pushkala (3), Subhamala/Asubhamala
(2), Lakshmi/Gouri/Saraswati (3), Kemadruma + its Jataka-Parijata alternative (2), the
Vesi/Vasi/Ubhayachari/Kartari/Susubha cluster (9), Srikantha/Srinatha/Virinchi (3),
Maha/Dainya/Kahala Parivartana (3), the dispositor-chain Kahala/Parvata pair (2), and
RajaYoga/Shankha (2). All 53 checked out and were signed off — chapter 6 already carried
unusually rigorous notes from its original encoding sessions, including several specific,
checkable claims of having independently rendered PDF pages to resolve arithmetic and
worked-example ambiguities.

**Independent re-verification, not just trust:** two of chapter 6's highest-stakes prior
claims were re-checked against the primary source this session rather than accepted on
faith, per the audit brief's instruction to use the PDF for difficult passages:
1. `PD.06.Dainya`/`PD.06.Kahala` claimed the itemized Parivartana lists on printed p.69 were
   independently rendered and found respectively defective (items 13, 28 truncated) and
   intact (all 8 items present). Re-rendered p.69 (PDF page index 68) this session at 300dpi
   and confirmed both claims exactly: item (13) reads "the lord of the 8th" with no pair
   partner, item (28) reads "the lord of 12th," equally truncated; all 8 Kahala items are
   present and match the card's derivation one-for-one.
2. `PD.06.Kahala.Dispositor`/`PD.06.Parvata` claimed a three-hop vs. two-hop distinction
   settled by Mantreswara's own worked examples on printed pp.71-72. Re-rendered both pages
   this session and confirmed: the Kahala-Dispositor example reads Mars → Sun → Saturn
   (three hops, Saturn tested, including the example's own uncorrected "own sign of
   exaltation" inconsistency for Saturn); the Parvata example reads Mars → Jupiter (two
   hops, Jupiter tested directly).

Both re-checks corroborated the prior session's claims exactly, with no discrepancy found —
strong evidence that chapter 6's unusually detailed notes reflect real verification work,
not confident-sounding narration.

**Defects found:** none. Verification moved from 206/404 (51%) to 259/404 (64%).

**Tests:** unchanged at 230 (no engine or metadata changes this batch — every card's
`requires`/`timing` fields were already accurate).

**Why this milestone matters:** Establishes that spot-checking a prior session's specific,
falsifiable claims (not just its conclusions) is part of what this verification pass means
by "verify" — and that doing so here increased confidence in the existing encoding rather
than finding more defects, which is itself useful evidence about the store's reliability.

---

### Milestone 18 — Verification queue, chapter 8 batch (108 cards, 1 defect corrected)

**Phase:** Production Blocker Clearance Program (P1-1)
**Status:** COMPLETE
**Completion:** 100%

**What was verified:** All 108 interpretive cards queued from chapter 8 — the graha-in-house
effects chapter, 9 grahas (Sun through Ketu) × 12 houses, the first chapter ever encoded in
this project (Milestone 1). Every card was read individually against its quoted verse, and
the (graha, house) pair in each card's `conditions`/`predicts` was additionally cross-checked
programmatically against the graha name and house ordinal actually printed in its own quote
— a legitimate rigor-appropriate check for this specific template, where the whole condition
is a single `in_house(graha, house)` leaf with no variables, dignity, or combinators, so
"does the condition match the quote" reduces almost entirely to "does this (graha, house)
pair appear in this quote."

**Defect found and corrected:** `PD.08.Saturn.01` was the one card in the entire 108-card
template that did not fit it. Its quote states two mutually exclusive outcomes for Saturn in
the Lagna, conditioned on dignity: "equal to the king" if Saturn is in its own or exaltation
sign there, "sorrow and misery" if any other sign — but the encoded condition was only
`in_house(Saturn, 1)`, with no dignity test, so a real consultation would have quoted *both*
contradictory outcomes for the same simple placement, regardless of which sign Saturn
actually occupied. Unlike the `PD.01.Kalapurusha.Strength` holdout (Milestone 16), this
needed no missing engine capability — `dignity` is already implemented and used throughout
the store — so per the defect-handling framework's category B ("clear representation error;
correct it when the source establishes the correction"), it was corrected rather than
deferred: split into `PD.08.Saturn.01.OwnOrExalted` (dignity own/exalted → the favourable
outcome) and `PD.08.Saturn.01.OtherSign` (negated dignity, grounded with no variables → the
unfavourable outcome), each with its own byte-exact sub-span and hash recomputed from
`Knowledge/phaladeepika.md`, not hand-typed. All other 107 cards in the template were
checked and confirmed to carry no comparable internal branch.

**Corrections made:** 1 (the Saturn split above). Card count rose from 404 to 405 as a
direct consequence — one card became two — not from new corpus material.

**Tests:** +3 (230 → 233): `test_saturn_in_lagna_own_or_exalted_fires_only_the_favourable_card`,
`test_saturn_in_lagna_other_sign_fires_only_the_unfavourable_card`, and
`test_saturn_in_lagna_own_sign_also_fires_the_favourable_card` in
`Engine/tests/test_counting_and_nature.py`. `test_chapter_eight_is_complete` (previously
asserting exactly 108 cards over 108 distinct (subject, house) pairs) was updated — not
weakened — to assert 109 cards over the same 108 distinct pairs, with an added check that
the one repeated pair (Saturn, house 1) is covered by exactly the two dignity-discriminated
cards expected. `Reports/PHASE3_BACKLOG.md` and `Reports/PHASE3_PLAN.md` regenerated for the
new card count.

**Verification moved from 259/404 (64%) to 368/405 (91%).**

**Why this milestone matters:** The largest single verification batch so far, and the first
to require an actual code-level correction rather than a documentation fix or a "leave
queued" deferral — proving the defect-handling framework's category distinctions (missing
capability vs. clear source-established error) work in practice, not just on paper.

---

### Milestone 19 — Verification queue, chapter 10 batch (36 cards) — queue closed

**Phase:** Production Blocker Clearance Program (P1-1 — **cleared**)
**Status:** COMPLETE
**Completion:** 100%

**What was verified:** All 36 queued interpretive cards of chapter 10 (Kalatra Bhava, the
7th house), read one by one against their quoted verses in `Knowledge/phaladeepika.md`. 35
were signed off; 1 was found defective and is deliberately held unsigned (below). This
**closes the interpretive verification queue**: 403/405 cards are now signed, and the only
two unsigned cards are documented defects, not unread cards.

**Checks run beyond reading, since chapter 10 is not a uniform template:**
- Every literal graha, sign and house number in every condition was cross-checked
  programmatically against that card's *own* quote. This surfaced exactly two cards whose
  condition mentions something its quote does not — both anaphoric sentences — and both were
  then resolved against the surrounding corpus text rather than assumed.
- The reference cards that chapter 10 conditions depend on were checked to actually exist and
  say what the cards assume: `PD.02.GrahaSex` really does print "Mercury, Ketu and Saturn are
  eunuchs" (backing the "hermaphrodite planet" reading), and `Dual` really is a source-printed
  sign attribute (`PD.01.SignAttributes.{Gemini,Virgo,Sagittarius,Pisces}`), not an engine
  coinage.
- `scope.sex` was verified to be genuinely enforced (`Engine/activate.py` 93-97) rather than
  decorative, and `BirthRecord` was confirmed to carry `sex` (`Engine/chart.py:58`).

**Defect found and corrected — `PD.10.WifeLoss.Lord7Afflicted` (v. 15).** The verse gives
four ways the 7th lord may be afflicted — "posited in his sign of debilitation, **be in an
inimical sign**, be combust or be aspected by a malefic" — and the encoded condition carried
only three, silently dropping the inimical-sign alternative; the card's own note then
mis-enumerated the list as three. This was demonstrated, not merely read: on a constructed
fact set (7th lord in an inimical sign, malefic occupying the 7th) the card did not fire,
while `PD.10.WifeDeprived.Lord7Afflicted` — the *same doctrine, stated twice by the book* —
did fire on identical facts, because that card carries the branch this one lacked. Since
`dignity(?g,"inimical")` is already derivable (`dep.dignity-friendship`, implemented since
Milestone 6), this was Milestone 18's category B (a clear representation error the source
itself corrects), so it was fixed in place rather than deferred: the branch was inserted in
the verse's own order. The quote, span and hash were untouched — only `conditions` and `note`
changed — so no re-hashing was required.

**Defect found and deliberately NOT corrected — `PD.10.Venus.VargaMarsSaturn` (v. 4).** Its
first branch, `in_varga_sign(Venus,"D9","any")`, does not encode what the verse says. The
verse conditions on Venus being in "the Varga of Mars or Saturn" — a varga *owned by* one of
those grahas — and the leaf tests neither ownership nor any particular sign, while narrowing
"Varga" to D9, a reading the verse never states. The prior note disclosed only that the quote
crosses a page break, so the gap was undisclosed. Left unsigned and documented in full,
following the `PD.01.Kalapurusha.Strength` precedent: choosing what "Varga" denotes here is an
interpretive decision belonging to whoever encodes the varga doctrine with chapters 3 and 21
in hand, not to a verification pass. Its two aspect branches were confirmed faithful.

**Prior claim corrected — `"any"` is a literal, not a wildcard.** Milestone 16's note on
`PD.01.Kalapurusha.Strength` justified its defect finding by saying the card's
`lord_of_house(any,any)` leaf is "vacuously true — every house always has a lord". That is
**wrong about the engine**, and the direction of the error matters. `VARIABLE_RE` is
`^\?[a-z][a-z0-9_]*$`, so only `?`-prefixed arguments quantify; a literal is matched by exact
string equality against the fact set, and `"any"` matches no fact at all. Verified empirically:
against a fact set containing `lord_of_house(Jupiter,7)`, the condition `lord_of_house(?g,7)`
is satisfied and `lord_of_house(any,7)` is not. The leaf is therefore vacuously **false**. The
defect finding itself stands (the condition still does not represent its quote), but the
consequence reverses: chapter 10's seven inert placeholder cards are **fail-safe by
construction**, not latent over-fires — and, more usefully, each must have its condition
*rewritten* when its dependency lands, never merely have `activation` flipped. Recorded in
the affected cards' sign-offs and pinned by a test.

**Prior claim corrected — `PD.10.Couple.BeneficAspect`'s anaphora.** "But should the above two
houses be associated with or aspected by benefics..." names no houses; the card encodes the
2nd and 7th and its note asserted that reading flatly. Reading the whole of v. 7 in the corpus
shows the *nearest* preceding sentence names the 7th and 8th houses of the **wife's** nativity.
The encoded reading is still the better one (the "But" contrasts with v. 7's opening 2nd-and-7th
rule, and the effect is stated of "the couple", i.e. the native's own chart) and is unchanged,
but the competing antecedent is now recorded in the note instead of being asserted away — per
the standing rule never to resolve a source ambiguity silently. The alternative would place the
card in a second nativity (`dep.second-nativity`), which is exactly why it matters.

**New production blocker discovered — P0-2, the benefic classification gap.** Running an
actual end-to-end consultation (per §13 of the session brief, "inspect the actual output")
surfaced the engine's own honesty report saying: *"the encoded doctrine does not classify
Jupiter, Venus; no nature fact is emitted for them and rules about benefics under-fire
accordingly."* Investigated and confirmed as a genuine, severe, previously unrecorded blocker.
See §K, P0-2 for the full analysis and the three candidate sources. Quantified: **22 active
cards** (all executable, none inert) across chapters 6 and 10 condition on `benefic` and
therefore under-fire on every chart. Demonstrated concretely: `PD.10.Benefics.In7` ("Benefics
in the 7th house will produce good effects") **cannot fire for Jupiter in the 7th**, the most
textbook instance of the rule it encodes.

**Arithmetic defect found in this file — see §A.** The published production-readiness figure
did not equal its own published inputs (claimed 39.55%, actually 48.30% from the same
categories, weights and scores). Corrected, with an explicit warning that the resulting 40% →
49% move is almost entirely the correction and not progress.

**Tests:** +8 (233 → 241), all in `Engine/tests/test_counting_and_nature.py`: the missing
inimical branch firing; each of the three other afflictions firing independently
(parametrised); both halves of the verse's conjunction refusing to fire alone (two tests);
the `"any"`-is-a-literal semantics; and a guard asserting that chapter 10's only unsigned card
is the one documented holdout, so a future session cannot quietly leave a card unreviewed.
`Reports/PHASE3_BACKLOG.md` and `Reports/PHASE3_PLAN.md` regenerated (card notes changed), and
`Reports/VERIFICATION_QUEUE.md` regenerated — it now lists only the 2 holdouts.

**Verification moved from 368/405 (91%) to 403/405 (99.5%). Blocker P1-1 is cleared.**

**Why this milestone matters:** Closes the production blocker that has driven the last five
milestones, and does it without rubber-stamping the last chapter — the batch found one real
under-firing bug, one undisclosed condition gap, and two incorrect claims made by previous
verification passes, including one about the engine's own semantics that had been reasoning in
the wrong direction. It also demonstrates the limit of the verification queue as a quality
instrument: every one of chapter 10's cards can be individually faithful to its verse while the
consultation they collectively produce is still substantially wrong, because the *doctrine they
depend on* is missing (P0-2). Card-level verification was necessary and is now finished; it was
never sufficient.

---

## D. CURRENT MILESTONE

**Nothing is currently in progress.** Milestone 19 above is fully committed, tested,
verified, and pushed.

**Next approved action — decide P0-2 (§K), the benefic classification gap.** This is a
**human judgement call and is why this session stopped here**, per the session brief's own
instruction to stop rather than invent an answer to a source ambiguity. Jupiter and Venus
receive no `nature` fact on any chart, and 22 active cards under-fire as a result. The engine
may not simply be told they are benefic — §I forbids hardcoding a classification the corpus
itself states, and the corpus states it three different ways, each with a real cost:

1. **Phaladeepika ch. 4 (Kala Bala), char ~64650:** *"The Moon, Mercury, Jupiter and Venus are
   benefics."* Names both missing grahas outright, in the same book already encoded. But it is
   scoped to a strength computation, and the sentences immediately after it explicitly scope
   Mercury's treatment to that computation (*"for determining kala Bala Mercury should be
   treated as a benefic. We support this view"*), in open disagreement with ch. 2 v. 27.
   Encoded unscoped it would also make the Moon unconditionally benefic, colliding with ch. 2's
   waxing/waning rule and raising `DoctrineError` on real charts.
2. **Phaladeepika ch. 8 Notes:** *"Jupiter is the greatest natural benefic amongst all the
   planets"* and *"Venus is the benefic No. 2."* General and unscoped, and they name exactly
   the two grahas that are missing — but both are the translator's commentary, and this project
   has consistently recorded such Notes as tier-2/3 apparatus rather than doctrine (Milestone
   11 did precisely this with the translator's benefic/malefic preference). Promoting apparatus
   to doctrine is a precedent change that should be made deliberately, not incidentally.
3. **Brihat Jataka, char ~50134:** *"Sun, Mars, Saturn and the Moon (within less than 72
   degrees distance from Sun) are treated as natural malefics. Moon other than of the nature
   referred to above, Mercury, Jupiter and Venus are natural benefics."* The cleanest statement
   of the three — verse-level, general, unscoped, and directly parallel to Phaladeepika ch. 2
   v. 27. It would also clear blocker **P1-2** (Brihat Jataka has zero cards) and produce the
   project's **first real cross-book corroboration** (both books make Sun/Mars/Saturn malefic
   and both make Mercury conditional on its company). But it introduces the project's first
   genuine cross-book *contradiction*: the two books define the Moon's nature by different
   criteria — Phaladeepika by waxing/waning, Brihat Jataka by distance from the Sun — which
   disagree on real charts (a Moon 60° from the Sun is waxing, so benefic to Phaladeepika, and
   within 72°, so malefic to Brihat Jataka). `_resolve_nature`'s `settle()` refuses such a
   conflict by design, raising `DoctrineError` rather than picking an authority. So option 3
   depends on **P1-3 (Stage 7 adjudication)** existing first.

**This is the moment P1-3 stops being speculative.** §K P1-3 has been deferred on the grounds
that only one card needed adjudication, so building a general mechanism would be architecture
ahead of need. That reasoning no longer holds: adjudication is now the gate on a P0 blocker
affecting 22 active cards, with a specific, reproducible, two-book contradiction to design
against instead of a hypothetical one. Recommended sequence once the decision is made: option 3
→ Stage 7 adjudication scoped to exactly this conflict → then reassess.

**Do not** resume ordinary chapter encoding before P0-2 is decided. Every new chapter encoded
against `benefic` conditions inherits the same silent under-firing.

**Alternative (unblocked, if P0-2 is deliberately deferred):**
- Phaladeepika ch. 6 vv. 42-43 (Adhiyoga) — ready now, scoped
  (`passage:phaladeepika.06.p175`). Note it is a benefic-conditioned yoga, so it would be
  born into P0-2's under-firing.
- Phaladeepika ch. 6 vv. 39-41 — still blocked, needs a distinct-sign-count fact.

**Blockers:** P0-2 blocks meaningful consultation quality; it does not block encoding.
**Dependencies:** none new required to *decide* P0-2; option 3 requires P1-3.
**Last commit:** this milestone's own commit (see git log for the SHA).
**Working tree:** clean, in sync with `origin/main`.

---

## E. UPCOMING MILESTONES

### Ready now (existing capabilities suffice)

| Description | Dependencies | Unlocks | Status |
|---|---|---|---|
| Ch.6 vv.42-43, Adhiyoga | none | continues ch.6 | ready, scoped in `passage:phaladeepika.06.p175` |
| Ch.6 vv.57-69, twelve dusthana-lord yogas (Ava, Nisswa, Mriti, Kuhu, Pamara, Harsha, Dushkriti, Sarala, Nirbhagya, Duryoga, Daridrya, Vimala) | none | continues ch.6; contains the richest contradiction in the chapter (Mantreswara vs. Parashara on which of these are auspicious) | ready, `passage:phaladeepika.06.p202` |
| Ch.5 — Source of livelihood | none | new chapter, rule-dense | ready |
| Ch.7 — RAJA YOGAS | none | new chapter, rule-dense; shares lordship dependency with ch.6 | ready |
| Ch.12 — Progeny (5th house) | none | new chapter, rule-dense | ready |
| Ch.14 — Diseases, Death, Past/Future births | none, but sensitive-content policy applies | new chapter | ready |
| Ch.15 — Assessment of houses | none | feeds future Stage 7 weighting | ready |
| Ch.16 — General effects of the twelve houses | none | would replace `HOUSE_LABEL_UNSOURCED` in the renderer | ready |
| Ch.17 — Exit from the world | none, sensitive-content gate | new chapter | ready |
| Ch.27 — Sanyasa yogas | none | new chapter | ready |
| `chapter:phaladeepika.11` (Female Horoscopy), `chapter:phaladeepika.18` (graha-pair conjunction effects), `passage:phaladeepika.08.p057` | now unblocked (`dep.lord-of-house`, `dep.aspects`, `dep.dignity` etc. are implemented) | see `Reports/PHASE3_BACKLOG.md` "Newly unblocked" | ready — flagged by `backlog.py` as newly unblocked, not yet acted on |

### Blocked

| Description | Blocked on | What would unblock it | Status |
|---|---|---|---|
| Ch.6 vv.39-41, seven-planets-in-N-signs family | new fact: distinct-sign-count of the 7 classical grahas | small, well-scoped engine addition | blocked, `passage:phaladeepika.06.p168` |
| Ch.3, Ch.21 — vargas (divisional charts) | `dep.varga` calculator | building the varga engine | blocked, source chapters for `dep.varga` |
| Ch.4 — Shadbala/Bhavabala strengths | `dep.strength` calculator | building Stage 4 | blocked, source chapter for `dep.strength`; highest-return single capability (unlocks 7 solo, 7 in closure) |
| Ch.13 — Longevity (ayurdaya) | `dep.adjudication` | competing longevity methods disagree by construction and need adjudication before weighing | blocked |
| Ch.19 — Dasas | none to encode the chapter itself, but it is the source of `dep.dasa` | building the dasa engine after encoding | partially ready — the chapter carries an internal balance dispute to preserve as disagreement |
| Ch.20 — Dasa/antardasa effects by house lord | `dep.dasa`, `dep.lord-of-house` (lord-of-house is implemented) | dasa engine | blocked |
| Ch.22 — Kalachakra dasa | `dep.dasa` (its own calculator, distinct from vimshottari) | out of MVP scope | blocked, beyond MVP |
| Ch.23 — Ashtakavarga | none to encode, source of `dep.ashtakavarga` | building the ashtakavarga engine; chapter itself preserves a 44-vs-48-bindu source defect | partially ready |
| Ch.24 — Ashtakavarga per Horasara | `dep.ashtakavarga` | ashtakavarga engine | blocked |
| Ch.25 — Upagraha computation | `dep.upagraha` | upagraha calculator | blocked |
| Ch.26 — Transit (gochara) | `dep.transit` | transit engine, beyond MVP | blocked |
| `card:PD.09.Vargottama` | `dep.vargottama` | vargottama extractor (needs `dep.varga` first) | blocked |
| `card:PD.06.Pushkala`, `card:PD.06.Vasumati` | `dep.strength`, `dep.universal-quantification` respectively | new engine capabilities | blocked |
| 16 cards with no unlock path yet | various combinations, see `Reports/PHASE3_PLAN.md` "Cards that no sequence here releases" | multiple simultaneous capabilities | blocked |

### Planned later

| Description | Notes |
|---|---|
| Brihat Jataka rule extraction | Book is corpus-converted (`Knowledge/brihat-jataka.md`, 6282 lines) but has **zero** rule cards. First cross-book corroboration cannot happen until this starts. |
| Convert remaining 4 books (BPHS Vol.1, Jataka Parijata Vol.1, Uttara Kalamrita, Saravali) | Behind the deliberate Phase 1 freeze; each has known OCR/text-layer problems documented in `Reports/PROJECT_STATUS.md` "Book audit". |
| `concept:manual-verification` — human sign-off on all cards | Only 4 of 404 cards have `extraction.verified_by` set. |
| Stage 7 adjudication design | Needed before Phase 4 can start; currently only `dep.rule-transfer` and `dep.dignity-override` exist as narrow primitives. |
| Phase 6 validation corpus | Hundreds of known/celebrity/historical charts — not started. |

### Production blockers

Must be solved before the system can be called production-ready, independent of card
count:

1. **Stage 7 adjudication does not exist.** Contradictory doctrine is preserved but never
   weighed — `Phases.txt` Phase 4 is entirely unbuilt.
2. **Only one book has rule cards.** Multi-book corroboration (a stated goal) cannot be
   assessed or delivered with a single-book store.
3. **No validation corpus.** No measurement exists of whether the system's predictions are
   any good (`Phases.txt` Phase 6).
4. **Human verification was essentially absent** (4/404 cards) as of Milestone 14; a
   systematic workflow now exists and 368/405 cards (91%) are signed off — see §K P1-1 for
   the current, authoritative count. This list (§E) predates that work and is kept for
   history; §K is the live register.
5. **No API/UI/packaging.** CLI-only today.
6. **Stage 4 (strength) does not exist**, and a large share of classical doctrine
   conditions on planetary/house strength — without it, entire chapters (4, and large
   parts of others) stay inert on arrival.

---

## F. ENGINE CAPABILITY MATRIX

### Implemented

| Capability | Status | Evidence | Used By |
|---|---|---|---|
| Lordship (`lord_of_house`) | Implemented | `Engine/facts.py::_lordship` | most ch.6 yoga cards, ch.1/2/8/9/10 |
| Sign classification | Implemented | `Engine/facts.py::_sign_classes` | dignity, house-class-dependent cards |
| House classification (kendra/trikona/dusthana/upachaya) | Implemented | `Engine/facts.py::_house_classes` | Shankha/Raja Yoga, twelve house-wise yogas |
| Graha classification (benefic/malefic reference) | Implemented | `Engine/facts.py::_graha_classes` | nature-dependent cards |
| Aspects | Implemented | `Engine/facts.py::_aspects` | Pushkala (partially blocked elsewhere), ch.8 translator-argument cards |
| Combustion | Implemented | `Engine/facts.py::_combustion` | ch.2 adverse-disposition (partially blocked elsewhere) |
| Dignity (exaltation/debilitation/own-sign) | Implemented | `Engine/facts.py::_dignity` | Pancha Mahapurusha Yogas, dignity dispute cards |
| Dignity-friendship (natural friendship) | Implemented | `Engine/facts.py::_dignity_friendship`, commit `e17e524`/`e66632d` | friendship-conditioned cards |
| Occupant counting | Implemented | `Engine/facts.py::_occupant_count` | multi-occupant conditions |
| Graha reference frame (houses counted from a graha, not just lagna) | Implemented | `Engine/facts.py::_graha_frame` | dispositor-chain Kahala Yoga |
| Conjunction | Implemented | `Engine/facts.py::_conjunction` | Raja Yoga, conjunction-conditioned cards |
| Benefic/malefic nature resolution | Implemented | `Engine/facts.py::_nature`, `_resolve_nature` | nature-conditioned cards |
| Nature occupancy (house occupied by grahas of a given nature) | Implemented | `Engine/facts.py::_nature_occupancy` | occupancy-by-nature cards |
| Condition-variable schema (multi-variable conditions) | Implemented | commit `e6d7df9` | most cards from ch.6 onward |
| Dignity-override mechanism | Implemented | commit `14125a4` | retrograde-as-exalted override cards |
| Rule-transfer mechanism | Implemented | commit `04dfba7` | "shares effect with" cards |
| Correlated negation | Implemented | `Rules/deferred.json` `dep.correlated-negation` | negation-in-binding cards |
| Multi-span quotation | Implemented | `dep.multi-span-quote` | two-span cards e.g. Pancha Mahapurusha naming+effect |
| Sign-class / house-class / graha-class reference tables | Implemented | `dep.sign-class`, `dep.house-class`, `dep.graha-class` | reference-card-backed extractors |
| Moon as alternative reference frame | Implemented | `dep.moon-frame` | Moon-counted yogas |

### Deliberately not implemented (deferred, with reason)

| Capability | Status | Why |
|---|---|---|
| Planetary/house strength (Shadbala/Bhavabala, Stage 4) | Not implemented | Highest-return single capability not yet built (`dep.strength`); source chapter (ch.4) not yet encoded. Blocks 8 cards directly, 7 in closure. |
| Varga (divisional chart) engine | Not implemented | `dep.varga`; source chapters 3/21 not yet encoded. |
| Vargottama extractor | Not implemented | `dep.vargottama`; depends on `dep.varga` first. |
| Vimshottari dasa engine | Not implemented | `dep.dasa`; source ch.19 carries an internal dasa-balance dispute that must be encoded as disagreement, not resolved, before the engine reads it. |
| Kalachakra dasa | Not implemented | Named explicitly out of MVP scope; needs its own calculator distinct from vimshottari. |
| Ashtakavarga | Not implemented | `dep.ashtakavarga`; source ch.23 preserves a 44-vs-48-bindu printed defect that must survive encoding as-is. |
| Upagraha computation | Not implemented | `dep.upagraha`; source ch.25 not yet encoded. |
| Transit (gochara) | Not implemented | `dep.transit`; explicitly "beyond the MVP". |
| Prashna (horary) branch | Not implemented | `dep.prashna`; explicitly "beyond the MVP" — at least one horary rule (`PD.02.Prashna.ReservoirWater`) sits inert among natal material pending a branch distinction. |
| Second nativity (spouse's chart etc.) | Not implemented | `dep.second-nativity`; explicitly "beyond the MVP". |
| Universal quantification over a variable-membership set | Not implemented | `dep.universal-quantification`; needs a new combinator, not an extension of existing condition language — e.g. Vasumati Yoga ("ALL benefic planets"). |
| Yoga-combination counting (N sibling yoga-conditions true simultaneously) | Not implemented | `dep.yoga-combination-count`; beyond the MVP; blocks the Pancha Mahapurusha compounding-effects closing sentence. |
| Hemmed-between (papakartari/subhakartari) extractor | Not implemented | `dep.hemmed-between`; no chapter dependency yet identified, low priority. |
| Stage 7 adjudication (weighting, priority, cancellation) | Not implemented | `dep.adjudication`; the largest single open architectural item — Phase 4 in `Phases.txt` has not started. |
| Distinct-sign-count fact (how many signs the 7 classical grahas occupy) | Not implemented | Newly identified this session, blocks ch.6 vv.39-41 specifically; small and well-scoped, not yet built. |
| Native-sex-scoped rule handling | **Implemented (row corrected in Milestone 19).** The previous text here claimed "the birth record does not carry sex, so all sex-scoped cards stay inert regardless" — that is stale and was wrong at the time of writing. `BirthRecord` carries `sex` (`Engine/chart.py:58`), `Engine/cli.py` exposes `--sex`, and `Engine/activate.py` 93-97 enforces `scope.sex`, refusing a card whose stated sex does not match the record (including when the record says `unknown`, which is the correct outcome rather than a guess). | Sex-scoped cards such as `PD.10.Female.MoonSaturn7Remarriage` / `PD.10.Male.MoonSaturn7` are `active` and fire correctly when `--sex` is supplied. ch.11 (Female Horoscopy) is **not** blocked on this and is listed as newly unblocked by `backlog.py`. |

---

## G. SOURCE / CORPUS STATUS

| Book | PDF pages | Text layer | Method | Converted? | In `Knowledge/`? | Rule cards? | Known defects |
|---|---|---|---|---|---|---|---|
| Brihat Jataka | 230 book pages (115 scanned spreads) | Corrupt OCR | Surya OCR | Yes — 28/28 chapters, 408 verses sequential, 0 hallucinated lines, 0 `[UNCLEAR]` | Yes (`Knowledge/brihat-jataka.md`, 6282 lines) | **0** | Devanagari glyph-level spot-check still owed (~1.5% char-error rate measured, not yet spot-checked); 2 misread verse numbers (8 vs. ४) corrected with evidence; 1 printed duplicate line preserved as printed; 7 tables + 10 charts of figure-transcription queue status unverified this session |
| Phaladeepika | 265 pages | Clean digital | `pdf_text` direct extraction | Yes — 28/28 chapters | Yes (`Knowledge/phaladeepika.md`, 5969 lines) | **404**, from chapters 1, 2, 6 (partial), 8, 9, 10 | Numerous — see `Rules/phaladeepika/manifest.json` `known_defects` (24 entries); most severe is the ch.23 Ashtakavarga chart totaling 44 instead of 48 bindus, preserved as printed |
| BPHS Vol. 1 | 482 | Corrupt OCR | Surya (pending) | No | No | 0 | Pending, behind Phase 1 freeze |
| Jataka Parijata Vol. 1 | 324 | Severely corrupt | Surya (pending) | No | No | 0 | Pending, behind Phase 1 freeze |
| Uttara Kalamrita | 256 | Corrupt + 75 pages with no text at all | Surya (pending) | No | No | 0 | Pending, behind Phase 1 freeze |
| Saravali | 203 | Clean but diacritics lost in the source PDF itself | Direct extraction (pending) | No | No | 0 | Source-baked diacritic loss ("Horā Śāstra" → "Hora Sstr"); transliteration normalization deferred to a later phase |

**Chapters completed (Phaladeepika):** 1, 2, 8, 9, 10 (fully encoded)
**Chapters partially encoded:** 6 (through v.38 of ~70 verses)
**Chapters deferred (not yet started):** 3, 4, 5, 7, 11-28 (22 chapters)
**Tables requiring visual reconstruction:** ch.1 v.7 biped/quadruped/table
(`PD.01.SignBodyForm.Table`) — **resolved** as of Milestone 16: rendered against printed
p.13, the table is a clean standard layout, not ambiguous; the card itself was already
accurate and is signed off, but the sign-to-class mapping itself is not yet encoded as
queryable reference data (a Phase 3 opportunity, not a verification blocker). ch.2 vv.21-22
natural friendship table remains encoded but inert pending human verification of the
reconstruction.
**Passages requiring human verification:** `concept:manual-verification` — 37 of 405
cards remain queued (all of chapter 10), plus 1 (`PD.01.Kalapurusha.Strength`) deliberately
held unsigned for a real defect blocked on missing capabilities. See §K P1-1.

---

## H. KNOWN DEFERMENTS

The full machine-readable list lives in `Rules/deferred.json` and is rendered by
`Rules/tools/backlog.py` into `Reports/PHASE3_BACKLOG.md` (89 entries) on every run — that
report is the authoritative live listing. This section is the *permanent, curated*
subset most likely to be forgotten. See §I "DO NOT FORGET" for the most critical items.

| Identifier | Description | Why deferred | Unblocks with | MVP blocker? | Revisit? |
|---|---|---|---|---|---|
| `passage:phaladeepika.06.p168` | vv.39-41 seven-planets-in-N-signs family | Needs new distinct-sign-count fact | Small engine addition | No | Yes — next candidate milestone |
| `passage:phaladeepika.06.p175` | vv.42-43 Adhiyoga | Ordering only, plus an attribution dispute to preserve | Nothing — ready now | No | Yes — likely next milestone |
| `passage:phaladeepika.06.p202` | vv.57-69, twelve dusthana-lord yogas | Ordering only | Nothing — ready now | No | Yes — richest contradiction in the chapter |
| `card:PD.06.Vasumati` | Universally-quantified benefic-set condition | `dep.universal-quantification` doesn't exist | New combinator | No | Yes, low priority |
| `card:PD.06.Pushkala` | Strength + Kendra-togetherness + undefined friendship tier | Triple-blocked | `dep.strength` + 2 unresolved readings | No | Yes |
| `concept:sunapha-anapha-durudhara-naming` | Which yoga name maps to which Moon-adjacency condition | Source states the collective condition, never names which sub-case is which | Human verification against another authority, or leave unnamed permanently | No | Yes — flagged twice already (slices 2 and 5) |
| `concept:nodal-retrograde-dignity` | Whether the retrograde-as-exalted override applies to Rahu/Ketu | Source says "a planet" without exclusion; engine already marks nodes retrograde on every chart | Human verification | No | Yes |
| `concept:manual-verification` | Human sign-off on all cards | 368/405 verified (91%) as of Milestone 18; see §K P1-1 for the live count | Continue the queue (ch. 10, 37 cards) | **Arguably yes for true production** | Yes — production blocker #4, nearly cleared |
| Brihat Jataka rule extraction | Entire book has 0 cards despite being converted | Ordering — Phaladeepika prioritized first | Just start | **Yes — for multi-book corroboration** | Yes — production blocker #2 |
| 4 unconverted books | BPHS, Jataka Parijata, Uttara Kalamrita, Saravali | Deliberate Phase 1 freeze after proving the pipeline on 2 structurally different books | Format approval + conversion run | No, not for MVP | Yes, eventually |
| `dep.second-nativity` | Spouse's chart / second nativity | Explicitly "beyond the MVP" | Schema design decision | No | Yes, post-MVP |
| `dep.prashna` | Horary branch | Explicitly "beyond the MVP" | Engine branch design | No | Yes, post-MVP; at least one card is stuck inside natal material because of this |
| `dep.transit` | Gochara | Explicitly "beyond the MVP" | Transit calculator | No | Yes, post-MVP |

---

## I. ARCHITECTURAL DECISIONS

**Decision:** Rule store as an intermediate machine-readable layer, not hardcoded doctrine
in Python, and not left as unstructured prose.
**Reason:** Prose cannot be executed and a model reading prose cannot be trusted to
extract the rule correctly; hardcoding in Python makes the engine the authority instead
of the books, and every new book becomes an engine change.
**Consequence:** Every rule card cites the corpus by byte-exact span + SHA-256, verified
on every run (`Rules/tools/verify.py`). The engine contains no book names — a test fails
the build if one appears.

**Decision:** Retrieval happens before synthesis, not after.
**Reason:** Synthesizing first and citing afterward builds a citation-laundering machine
whose output is undetectably unsourced, since every sentence gets a footnote regardless.
**Consequence:** Stage 6 (activation) runs before Stage 8 (composition); the composing
stage is handed a closed set of pre-verified claims and may only arrange them.

**Decision:** Retrieval by exact predicate lookup, not embedding similarity.
**Reason:** "Mars in the 7th" and "Mars in the 8th" embed almost identically and mean
entirely different things; exact lookup has no top-k and no recall cliff.
**Consequence:** The system knows precisely what its books say about a chart — no
approximate matching anywhere in the activation path.

**Decision:** Preserve contradictory authorities rather than resolving them.
**Reason:** Classical astrology genuinely disagrees between books and even within one
translator's notes; silently picking a winner would misrepresent the tradition.
**Consequence:** `contradicts`/`extends` links and dual cards recur throughout (rising-sign
verse-8 dispute, nodal exaltation 3-way dispute, dignity dispute, dasa-balance dispute
still pending in ch.19). Stage 7 adjudication (weighing them) does not exist yet — they
are preserved, not yet reasoned about.

**Decision:** Reference cards (tables, classifications) are distinct from predictive
cards, and doctrine-backed extractors read only from reference cards already in the
store.
**Reason:** The engine must never hardcode a classification (e.g. which signs are
benefic) that the corpus itself states — otherwise the corpus stops being the sole
authority.
**Consequence:** Extractors like `_nature`, `_dignity`, `_house_classes` derive their
tables from previously-encoded reference cards, not from Python constants.

**Decision:** Do not build speculative engine architecture ahead of source need.
**Reason:** Established explicitly in milestone 13 (dispositor-chain Kahala Yoga): the
multi-hop "lord of lord of..." doctrine was representable with existing predicates, so no
`dispositor_chain()` predicate was added.
**Consequence:** New engine capabilities are only built when (1) an actual source passage
requires it, (2) existing predicates genuinely cannot express it, (3) it's small and
reusable, (4) its semantics come from the source, not a guess. This is now the standing
rule for every future milestone (see the resume prompt's §6, echoed here permanently).

**Decision:** Retrograde-as-exalted dignity override is encoded as a general mechanism
(`dep.dignity-override`), and its applicability to the lunar nodes is left an open,
recorded question (`concept:nodal-retrograde-dignity`) rather than silently assumed.
**Reason:** The source verse says "a planet" without exclusion, but nodes have no physical
retrograde motion in the same sense — extending the override to them would be an
interpretive leap the text doesn't make explicit.
**Consequence:** The engine's retrograde predicate already marks nodes retrograde on every
chart (since their apparent motion is always retrograde), but the override's applicability
to them is deferred to human judgment rather than assumed either way.

**Decision:** Natural friendship ambiguity (ch.2 vv.21-22 table) resolved by direct
high-zoom visual inspection of the source PDF page, not by trusting the OCR/`pdf_text`
line dump.
**Reason:** The flattened line dump made the table look damaged (columns interleaved)
when direct inspection showed it is printed correctly, including two genuine anomalies
(Mercury under both Friend and Neutral for the Moon row; "-----" for the Moon's Enemy
column) that are source-real, not extraction artifacts.
**Consequence:** Established the standing practice (used again in ch.6 slice 2 for the
Sunapha/Anapha/Durudhara cluster) of never trusting extracted text alone when a table or
figure is ambiguous — always render and inspect the actual page.

**Decision:** Second nativity (e.g., deriving a "wife's chart" from the birth chart) is
deferred as a schema (`dep.second-nativity`), not attempted with an approximation.
**Reason:** Explicitly named "beyond the MVP" — the birth-record and chart schema would
need real redesign to represent more than one nativity per consultation.
**Consequence:** Cards like `PD.10.WifeChart.Houses7And8` stay inert rather than being
approximated (e.g., by reusing the native's own chart).

**Decision:** Multi-hop lordship/dispositor logic represented via repeated application of
the existing `lord_of_house` predicate rather than a dedicated chain predicate.
**Reason:** See "Do not build speculative engine architecture" above — this is the
concrete instance that established the rule.
**Consequence:** `PD.06.Kahala.Dispositor` (milestone 13) proves the pattern generalizes;
future dispositor-chain doctrine should follow the same approach unless a genuine
counter-example appears.

---

## J. PRODUCTION BLOCKER AUDIT (2026-08-23)

### J.1 — Is the 39% weighting itself sound?

Audited against the instruction to not trust it blindly. Conclusion: **the categories and
weights in §A are appropriate and were not adjusted**, for these reasons:

- **Categories are not missing anything material.** The ten categories already cover every
  item the audit brief asked to check for (corpus, verification, extraction, reasoning,
  contradiction handling, provenance, testing, end-to-end validation, cross-book
  corroboration, safety, interface) — nothing on that list lacks a category.
- **No category is overweighted.** Rule extraction (20%) and reasoning capability (15%) are
  the two largest, which matches the project's own stated vision (cited quotes applied to
  computed quantities) — a system cannot be "production ready" with either weak, however
  many cards exist.
- **No category is counted complete despite an unresolved dependency.** Provenance was 90%
  (now 92%) specifically *because* it named its own gap ("verified_by null on all but 4") in
  the same breath as the score — it was never silently rounded up.
- **Card count is deliberately not its own category**, which the file already states
  explicitly and which this audit confirms is correct — a store can have many cards and
  still lack reasoning capability (Stage 4 strength, Stage 7 adjudication).

**Verdict: methodology sound, not corrected. Only the underlying category scores for
provenance/auditability and test coverage were recomputed this session, per §A's own rule
that this happens "whenever a category's score changes materially," which it did (verified
cards, not the composite %, is the metric that moved materially — see §A's note).**

### J.2 — Production gate checklist

The gates below are what "production ready" concretely means for *this* project, derived
from the README's own governing rule ("the system may compute, and it may quote — it may
not invent") and the phase roadmap in `Phases.txt`/§B — not invented requirements.

| Gate | Status | Evidence | Blocker | What clears it |
|---|---|---|---|---|
| Required source corpus | Partial | 2/6 books converted (§G) | Phase 1 freeze (deliberate) | Convert BPHS, Jataka Parijata, Uttara Kalamrita, Saravali — not required for MVP scope (see K, P2) |
| Source conversion | Done for converted books | `verify.py`/Pipeline byte-exact + hallucination-detected | none for the 2 done books | N/A until more books are converted |
| Source verification | Mostly done | Byte-exact hash-verified every run; Devanagari glyph spot-check owed on Brihat Jataka | Minor, not blocking | Spot-check pass |
| Rule extraction | Partial | 404/~1535 cards, one book | Ordering, not a capability gap | Continue Phase 3 chapter-by-chapter |
| Rule-store integrity | Done | `verify.py`/`dupes.py` clean, 404 cards, 0 duplicates | none | N/A |
| Reasoning capability | Partial | Stages 0,1,2,6,9,10 done; 3-5,7 not dedicated stages | `dep.strength` (highest leverage), `dep.adjudication` | Build Stage 4, then Stage 7 |
| Contradiction handling | Mechanism exists, weighing doesn't | `contradicts`/`extends` links used repeatedly | `dep.adjudication` | Stage 7 |
| Provenance | Strong | Byte-exact hash gate; **now 368/405 (91%) human(+Claude) sign-off**, was 4/404 | 37 interpretive cards still queued (ch. 10) | Work the queue (§K, P1-1) |
| Human verification | **This milestone's subject** | Workflow now exists and is proven on ch. 9 | Remaining 206 cards | Continue the queue |
| Cross-book corroboration | Not possible yet | Only 1 book has cards | Brihat Jataka has 0 cards | Start Brihat Jataka extraction (§K, P1-2) |
| Regression testing | Partial | 230 tests, no full-corpus e2e suite | Not yet built | Build after more chapters land |
| Real-chart validation | Ad hoc only | Spot-checked per milestone, no charted set | Phase 6 not started | Out of MVP critical path per `Phases.txt` |
| Reproducibility | **Sound** | README documents the exact `uv venv`/`pip install`/`fetch_swisseph.py` sequence; verified this session by running the full suite from a clean invocation | none found | N/A |
| Privacy/security | Sound for current scope | `Cases/` (real birth data) gitignored by design; no PII stored elsewhere | none found | N/A |
| Production interface | CLI only | `Engine/cli.py` produces full consultations | No API/UI | Not required — see §K, P3-1 |
| Deployment/installability | Documented, not packaged | README setup sequence works; no PyPI package, no container | Low priority | Not required for current scope |
| Critical dependency resolution | See §K | — | — | — |

### J.3 — Corpus incompleteness (item A)

6 books planned; 2 converted (Brihat Jataka, Phaladeepika), 4 pending behind a **deliberate**
Phase 1 freeze after the pipeline was proven on two structurally different books (clean
digital text vs. corrupt OCR). Rule cards exist only for Phaladeepika (404) — Brihat Jataka
has 0 despite being fully converted. **The minimum defensible production corpus is not "all
6 books"**: the project's own vision (cited, computed answers) is satisfiable by one
well-verified book with correct reasoning; a second book (Brihat Jataka, already converted)
is what's needed specifically for *cross-book corroboration*, which is its own gate, not a
corpus-completeness one. Converting the 4 frozen books is P2 — valuable, not MVP-blocking.

### J.4 — Human verification (item B) — this milestone's subject

Answered in full by this milestone: "human verification" in this project already meant, by
its own 4-card precedent, a joint human(+Claude) reading pass recorded with a specific
description of what was checked — not solitary human labor. Reference/table cards do not
need it (automated structural check is provably sufficient — J.2). Interpretive cards do,
systematically, via the new queue. See Milestone 15 above and §K, P1-1 for the resume point.

### J.5 — `dep.strength` (item C)

Confirmed as the single highest-leverage missing engine capability (unlocks 7 cards solo, 7
in closure; blocks ch. 4 entirely and large fractions of ch. 19/20/21 per
`Reports/PHASE3_PLAN.md`). **Not implemented this session, and not chosen as the first
blocker**, for a concrete reason distinct from "it's a lot of work": building Stage 4
(Shadbala/Bhavabala) legitimately requires *encoding ch. 4 first* (163 paragraphs, ~106
cards) — the engine may not hardcode strength doctrine the book itself states, per §I's own
rule. That is a multi-session Phase-3 encoding effort chained to an engine-architecture
effort, not a single completable blocker; picking it first would have produced exactly the
half-finished state item 8/13 of the audit brief forbids. It remains the top item on the
critical path (§K, P0-1) for the *next* session once ordinary Phase 3 work resumes.

### J.6 — Cross-book corroboration (item D)

Phase 4's cross-book goal cannot be evaluated with one book holding cards. Corroboration
technically means: the same predicted effect (e.g. a specific yoga's claim) is independently
stated in two or more books' cards, checkable once both exist — no new engine mechanism is
required beyond querying the store by predicted effect across `book_id`s, which the current
schema already supports (`card.book_id` is a field). **This is a production gate** (README's
own vision implies converging authorities, and `Phases.txt` Phase 4 depends on it) but not
one clearable by architecture — it needs actual Brihat Jataka cards to exist first (§K, P1-2).
No speculative cross-book architecture was built, per §I.

### J.7 — Deferred reasoning capabilities (item E)

Audited against §F "Deliberately not implemented." None reclassified: vargas, dasas,
ashtakavarga, transits, second nativity, and universal quantification each still lack both
an MVP requirement and (except dasa/varga) the source chapter that would justify building
them. `dep.strength` is the only one of this group promoted to "P0, first on the critical
path once corpus work resumes" (§K) — all others stay correctly deferred, not because they
are uninteresting but because no source passage yet forces them (§I's standing rule).

### J.8 — Production interface / deployment (item F)

The intended production artifact, per the repository's own plans, is the CLI
(`Engine/cli.py`) — nothing in `Phases.txt`, `README.md`, or this file's history establishes
that an API or UI is required scope; §K, P3-1 keeps that explicitly out of the MVP per §13's
own instruction not to over-build. Installation is already documented and was verified this
session to work as written (README's `uv venv`/`pip install tzdata pytest`/
`fetch_swisseph.py` sequence, checked against the actual `.venv` in this repository).
Privacy is sound for current scope: `Cases/` (the only place real birth data would land) is
gitignored by design, and nothing else in the pipeline retains personal data. No packaging
(PyPI, container) exists, which is fine — nothing in the project's plans calls for
distributing this to third parties yet.

---

## K. PRODUCTION BLOCKER REGISTER

Permanent section, per the continuity rule in §12/§M below. Update on every blocker
cleared, newly identified, or re-scoped.

### P0 — must be solved before production

*Ordered by position on the critical path: **P0-2 is the top item**, discovered in Milestone 19 and degrading every consultation today, while P0-1 gates whole future chapters. P0-1 is listed first only because it is the older entry.*

**P0-1 — `dep.strength` (Stage 4: Shadbala/Bhavabala) does not exist.**
- **Why it matters:** Classical doctrine conditions on planetary/house strength throughout
  the corpus; without it, ch. 4 itself and large fractions of many other chapters (ch.19 at
  70% inert-on-arrival, ch.20 at 67%, ch.21 at 89%, per `Reports/PHASE3_PLAN.md`) are born
  inert regardless of how much more is encoded.
- **Current state:** Not implemented. Blocks 8 cards directly (`PD.06.Ruchaka` family's
  strength caveat, `PD.06.Pushkala`, others), 7 in closure.
- **Dependency:** Ch. 4 (Shadbala/Bhavabala doctrine, 163 paragraphs, ~106 est. cards) must
  be encoded first — the engine may not hardcode strength rules the book itself states.
- **Exact work required:** (1) encode ch. 4 fully as ordinary Phase 3 work, (2) design and
  build Stage 4 as a dedicated engine stage reading only from ch. 4's now-encoded reference
  cards, (3) re-run `backlog.py`/`leverage.py` to confirm the 7-8 card unlock.
- **What it unlocks:** ch. 4 chapter itself, 7-8 currently-inert cards, and removes the
  single largest "born inert" tax on every future chapter per §J.5.
- **Status:** Deferred to next Phase-3-resuming session; not started this session (§J.5).

**P0-2 — The benefic classification gap: Jupiter and Venus have no `nature` fact at all.**
- **Why it matters:** This is the most consequential defect found in the project so far,
  because it degrades *every* consultation silently rather than failing loudly. The two
  principal natural benefics of the entire tradition are unclassified by the encoded doctrine,
  so `nature(Jupiter,benefic)` and `nature(Venus,benefic)` are never emitted, and every rule
  conditioning on a benefic under-fires. It is not an engine bug — `Engine/facts.py`
  `_resolve_nature` is correct and even reports the gap honestly in the consultation's own
  "Doctrine read, but not complete" section — it is a doctrine-coverage gap.
- **Quantified:** **22 active cards** (all executable, none inert) condition on `benefic`:
  the twelve house-wise yogas of ch. 6 (`Chamara`, `Dhenu`, `Shaurya`, `Jaladhi`, `Chhattra`,
  `Astra.H06`, `Astra.H08`, `Kama`, `Bhagya`, `Khyati`, `Parijata`, `Musala`), `PD.06.Amala`,
  the Subha- cluster (`Subhavesi`, `Subhavasi`, `Subhobhayachari`, `Subhakartari`, `Susubha`),
  and 4 of chapter 10 (`Houses5And7.Flourish`, `Benefics.In7`, `Couple.BeneficAspect`,
  `WifeChildren.Lords2712`). Anything conditioning on `nature_occupancy(house, "benefic")` is
  affected the same way.
- **Demonstrated, not inferred:** `PD.10.Benefics.In7` encodes "Benefics in the 7th house will
  produce good effects unless they happen to be lords of the 6th, 8th or 12th house". Given a
  chart with Jupiter in the 7th — the most textbook instance of that rule — the card does not
  fire. Supplying the single missing fact `nature(Jupiter,benefic)` makes it fire immediately.
- **Root cause:** The only two `graha_nature` reference cards are `PD.02.Nature.Malefics`
  (ch. 2 v. 27) and `PD.02.Nature.Benefics` (that verse's Notes). Read together they name the
  malefics exhaustively (Sun, Mars, Saturn, Rahu, Ketu, plus the waning Moon and Mercury when
  associated with them) but name only the waxing Moon and unassociated Mercury as benefic.
  Jupiter and Venus are simply never mentioned in that passage — the book treats them as
  benefic by default, and "not on the malefic list, therefore benefic" is an inference the
  engine is forbidden to make on its own (§I: the corpus is the sole authority for a
  classification the corpus states).
- **Dependency:** A human decision between three real sources, each with a real cost — see §D
  for the full statement of all three with corpus offsets. Briefly: Phaladeepika ch. 4's
  benefic list is scoped to Kala Bala and collides with ch. 2 on both Mercury and the Moon;
  Phaladeepika ch. 8's two statements are general but are translator's apparatus, not verse;
  Brihat Jataka's is the cleanest and most general but starts a second book and introduces the
  project's first genuine cross-book contradiction (the two books define the Moon's nature by
  incompatible criteria), which `settle()` refuses to adjudicate by design.
- **Exact work required:** (1) decide which source governs; (2) if Brihat Jataka, build Stage 7
  adjudication (P1-3) first, because the Moon conflict raises `DoctrineError` on real charts;
  (3) encode the chosen passage as a `graha_nature` reference card with the existing toolchain;
  (4) re-run a consultation and confirm the 22 cards now fire where they should.
- **What it unlocks:** correct firing of 22 active cards today and every benefic-conditioned
  card encoded hereafter; materially better consultations; and, via option 3, blockers P1-2 and
  the first cross-book corroboration the project has ever been able to attempt.
- **Status:** **OPEN, and it is the top of the critical path.** Discovered in Milestone 19; not
  actioned, deliberately, because choosing among the three sources is a judgement call with
  lasting consequences and the session brief's §14/§18 forbid inventing an answer to exactly
  this kind of ambiguity. Do not resolve it by hardcoding the conventional classification.

### P1 — required for the intended MVP/production scope

**P1-1 — Human(+Claude) verification queue. CLEARED (Milestone 19).**
- **Why it mattered:** Byte-exact quote verification proves the words are real; it does not
  prove the card reads them correctly. This was the one component of "provenance" the store
  could not claim in full.
- **Final state:** **403/405 cards signed (99.5%)**, from 4/404 (1%) when the workflow was
  built. 175 structural cards signed automatically; 228 interpretive cards signed by an actual
  human(+Claude) reading pass across chapters 1, 2, 6, 8, 9 and 10, over five batches
  (Milestones 15-19). The interpretive queue is empty apart from two deliberate holdouts, both
  real documented condition defects blocked on capabilities that do not exist:
  `PD.01.Kalapurusha.Strength` (needs `dep.strength` + `dep.condition-variables`) and
  `PD.10.Venus.VargaMarsSaturn` (needs the varga doctrine decided). A test
  (`test_chapter_ten_interpretive_cards_are_signed_off_except_the_one_holdout`) pins the second
  so a future session cannot quietly leave a card unreviewed.
- **What the pass actually found**, across the five batches: 3 genuine condition defects (1
  corrected in ch. 8, 1 corrected in ch. 10, 2 held open with documentation), 4 stale or wrong
  metadata claims corrected, 3 prior sessions' claims re-checked against the primary source (1
  found false, 2 confirmed exact), and 1 incorrect claim about the engine's own semantics
  corrected. It was not a rubber stamp.
- **Standing lesson — card-level verification is necessary but not sufficient.** Every chapter
  10 card can be individually faithful to its verse while the consultation they collectively
  produce is still substantially wrong, because the doctrine they *depend on* is missing. That
  is exactly what P0-2 below turned out to be, and it was invisible to 5 milestones of
  card-by-card review; it took running an actual consultation and reading the output to see it.
- **Status:** **CLEARED.** Do not re-open. Re-run `python Rules/tools/review.py --queue` after
  encoding any new chapter — new interpretive cards will queue themselves.

**P1-2 — Only one book (Phaladeepika) has rule cards; Brihat Jataka has zero.**
- **Why it matters:** Multi-book corroboration is a stated project goal (`Phases.txt` Phase
  4) and cannot be assessed or delivered from a single-book store.
- **Current state:** Brihat Jataka is fully corpus-converted (`Knowledge/brihat-jataka.md`,
  6282 lines) and frozen, but has 0 cards.
- **Dependency:** None technical — purely an ordering choice (Phaladeepika was prioritized
  first as the cleaner-text book).
- **Exact work required:** Begin Brihat Jataka rule extraction using the existing toolchain
  (`build_chapter.py`), same discipline as Phaladeepika ch. 1-10.
- **What it unlocks:** First possible cross-book corroboration check (§J.6); second book
  toward the eventual 6-book corpus.
- **Status:** Not started; queued behind current Phaladeepika ch. 6 continuation in the
  ordinary Phase 3 backlog (§E).

**P1-3 — Stage 7 adjudication does not exist.**
- **Why it matters:** Contradictory doctrine is preserved (`contradicts`/`extends`) but
  never weighed against itself — `Phases.txt` Phase 4 is otherwise entirely unbuilt.
- **Current state:** Only `dep.rule-transfer` and `dep.dignity-override` exist as narrow
  primitives; `dep.adjudication` unlocks only 1 card solo today.
- **Dependency (re-scoped in Milestone 19):** the previous entry here deferred this on the
  grounds that "only 1 card needs it, [so building it] risks exactly the
  speculative-architecture-ahead-of-need §I warns against." **That reasoning no longer holds.**
  P0-2 — a P0 blocker degrading 22 active cards on every chart — has a candidate fix (adopting
  Brihat Jataka's natural-benefic classification, which is the cleanest of the three available
  sources and would also clear P1-2) that **cannot be taken without adjudication**, because the
  two books define the Moon's nature by incompatible criteria (Phaladeepika: waxing/waning;
  Brihat Jataka: within/beyond 72° of the Sun) and `_resolve_nature`'s `settle()` raises
  `DoctrineError` rather than choosing an authority. Adjudication is now a gate on production
  quality, not a speculative nicety.
- **Exact work required:** design Stage 7 against the concrete, reproducible conflict P0-2
  supplies — one graha, two books, two stated criteria that genuinely disagree on real charts —
  rather than against a hypothetical. The smallest defensible version does not need weighting or
  numeric confidence: it needs to represent that two authorities classify the same graha
  differently, surface both with their sources, and mark the conflict unresolved where no
  documented priority rule exists. Additional real examples will arrive with ch. 6's
  Mantreswara-vs-Parashara dusthana-lord dispute (`passage:phaladeepika.06.p202`), which should
  be encoded alongside if possible so the design is tested against two independent conflicts.
- **What it unlocks:** P0-2's best fix; P1-2 (Brihat Jataka's first cards); Phase 4 entirely;
  contradiction-explaining narrative in Phase 5.
- **Status:** Not started, but **no longer correctly deferred** — it is now on the critical path
  behind P0-2's decision. Do not build a general weighting/confidence system; build exactly the
  mechanism the Moon conflict requires and no more (§I).

### P2 — important, can follow initial production release

**P2-1 — 4 books remain unconverted (BPHS Vol.1, Jataka Parijata Vol.1, Uttara Kalamrita,
Saravali).**
- **Why it matters:** Broader corpus is valuable but not MVP-required (§J.3) — one
  well-verified, well-reasoned book satisfies the project's core vision.
- **Current state:** Behind a deliberate Phase 1 freeze; each has documented OCR/text-layer
  problems (`Reports/PROJECT_STATUS.md`).
- **Dependency:** Format approval + a conversion run per book.
- **Exact work required:** Lift the freeze deliberately when corroboration/breadth is
  actually needed, not on a schedule.
- **What it unlocks:** Broader corpus, more corroboration candidates.
- **Status:** Deferred, not urgent.

**P2-2 — No dedicated end-to-end regression suite across the full corpus of encoded
chapters.**
- **Why it matters:** 230 unit/integration tests exist; nothing runs the full pipeline over
  every encoded chapter and diffs the consultation output.
- **Current state:** Spot-checked per milestone against 1-2 real charts (ad hoc).
- **Dependency:** None.
- **Exact work required:** Build a golden-output regression test once enough chapters exist
  that drift would be worth catching automatically.
- **What it unlocks:** Confidence that new chapters/engine changes don't silently break old
  consultations.
- **Status:** Deferred — not yet worth the fixture-maintenance cost at 6 chapters.

### P3 — future enhancement

**P3-1 — No API/UI/packaging.**
- **Why it matters:** Nothing in the project's own plans establishes this is required scope
  (§J.8); building one now would be exactly the over-building §13 forbids.
- **Current state:** CLI-only, works end-to-end.
- **Status:** Correctly out of scope until the project's plans say otherwise.

**P3-2 — Phase 6 validation corpus (hundreds of known/celebrity/historical charts).**
- **Why it matters:** Needed eventually to measure whether predictions are any good, but
  requires a much larger encoded corpus and reasoning-capability set first.
- **Status:** Correctly not started — no reasoning depth yet to validate against.

---

## DO NOT FORGET

- **P0-2 IS THE TOP OF THE CRITICAL PATH: Jupiter and Venus have no `nature` fact.** 22
  active cards under-fire on every chart because of it. Do **not** fix this by telling the
  engine they are benefic — that is precisely the hardcoding §I forbids. Three real corpus
  sources exist and choosing between them is a human decision; §D lays out all three with
  offsets. Read §K P0-2 before doing anything else.
- **Card-level verification is necessary but not sufficient.** Five milestones of card-by-card
  review (368 → 403 cards signed) never once surfaced P0-2, because every individual card was
  faithful to its own verse; the gap was in the doctrine they all depend on. It took running
  an actual consultation and reading the engine's own "Doctrine read, but not complete"
  report. **Run a real consultation and read the output as part of every milestone**, not just
  the test suite.
- **`"any"` in a condition is a LITERAL, not a wildcard.** `VARIABLE_RE` is
  `^\?[a-z][a-z0-9_]*$`, so only `?`-prefixed arguments quantify. `lord_of_house(any,7)`
  matches no fact and is vacuously **false**. This means every inert placeholder card is
  fail-safe, and — importantly — that such a card must have its condition **rewritten** when
  its dependency lands, never merely have `activation` flipped to active. Milestone 16's note
  claimed the opposite ("vacuously true"); it was corrected in Milestone 19 and is pinned by a
  test.
- **The verification queue is CLOSED (Milestone 19)** — 403/405, with exactly two deliberate,
  documented holdouts (`PD.01.Kalapurusha.Strength`, `PD.10.Venus.VargaMarsSaturn`). Do not
  re-open it or re-derive whether verification can be systematic; that is settled. Just re-run
  `python Rules/tools/review.py --queue` after encoding a new chapter.
- **§A's headline percentage was miscomputed for four milestones** (claimed 39.55%, its own
  inputs give 48.30%). Corrected in Milestone 19. **Recompute the sum from the table, never
  by adding a delta to the previous headline** — that is exactly how the error propagated.
- **A verification workflow now exists — use it, don't repeat the audit.**
  `Rules/tools/review.py` classifies every card as structural (auto-signed) or interpretive
  (queued in `Reports/VERIFICATION_QUEUE.md`). Resume the queue chapter by chapter rather
  than re-deriving whether verification "can be done systematically" — that question is
  answered (§J.4, §K P1-1).
- **Never blanket-approve a file of cards, even a uniform-looking one.** `PD.08.Saturn.01`
  broke chapter 8's uniform template and was caught only by reading every card individually
  (Milestone 18); `PD.10.WifeLoss.Lord7Afflicted` was missing a disjunct its own sibling card
  carried, and was caught only by comparing the two against the same doctrine (Milestone 19).
- **`Phases.txt` marks Phase 1 complete with a ✅ — this is wrong.** Only 2 of 6 planned
  books are converted (Brihat Jataka, Phaladeepika); 4 are pending behind a deliberate
  freeze. Do not treat Phase 1 as finished when reasoning about project state.
- **`Reports/PROJECT_STATUS.md` is stale** — it has never been updated since the initial
  commit and describes an in-progress checkpoint (Brihat Jataka draft not yet promoted)
  that the same commit's message already superseded. Treat it as historical color, not
  current state; rely on live tool output (`verify.py`, `dupes.py`, `backlog.py`,
  `leverage.py`) instead.
- **Brihat Jataka has zero rule cards** despite being fully corpus-converted and frozen.
  No cross-book corroboration is possible until this starts — this is a named production
  blocker.
- **vv.39-41 needs a small new engine capability** (distinct-sign-count of the 7 classical
  grahas) — well-scoped, not yet built, `passage:phaladeepika.06.p168`.
- **`dep.strength` (Stage 4) is the single highest-leverage missing capability** — it
  unlocks 8 cards directly and gates entire future chapters (ch.4 itself, and large
  fractions of many others per `Reports/PHASE3_PLAN.md`'s inert-on-arrival table, e.g.
  ch.19 at 70%, ch.20 at 67%, ch.21 at 89%).
- **Second-nativity architecture is deliberately unbuilt** — do not approximate a spouse's
  chart from the native's own chart as a shortcut; it was explicitly deferred as a schema
  decision requiring real design (`dep.second-nativity`).
- **Cross-book corroboration (Phase 4 goal) cannot be evaluated yet** — only one book has
  cards in the store.
- **Human verification is complete** — 403/405 cards (99.5%) have `verified_by` set; the 2
  that do not are documented defect holdouts, not unreviewed cards. This was a real production
  blocker as recently as Milestone 14 (4/404). See §K P1-1, now marked CLEARED.
- **Never merge contradictory authorities into one card** — this project's core value is
  preserving disagreement (rising-sign dispute, nodal-exaltation 3-way dispute, dignity
  dispute, natural-friendship table anomalies, ch.19's dasa-balance dispute still
  pending). This is not optional cleanup work; resolving these away would break the
  project's stated purpose.
- **Do not build speculative engine capabilities** ahead of an actual source passage
  requiring them — see §I's standing architectural rule, established concretely at
  milestone 13.

---

## HOW TO RESUME

A fresh Claude Code session (with no memory of any previous conversation) should:

1. Read this file (`MILESTONES.md`) in full before doing anything else.
2. Run `git fetch --all --prune`.
3. Verify local `HEAD` matches `origin/main` and check ahead/behind counts
   (`git rev-list --left-right --count main...origin/main`). If they diverge, stop and
   investigate — do not reset, rebase, or force-push.
4. Verify the working tree is clean (`git status`).
5. Re-read §D "Current Milestone" and §E "Upcoming Milestones" — do not trust a stale
   memory of what's next; the repository (via `Rules/tools/backlog.py` and
   `Rules/tools/leverage.py`) is the live source of truth, and this file is a curated
   snapshot that can itself go stale between updates.
6. Inspect the relevant source passage(s) and any related `Rules/deferred.json` entries
   before writing a single card.
7. Run the project's integrity checks before starting work, to confirm this file's
   snapshot still matches reality:
   ```powershell
   python Rules/tools/verify.py
   python Rules/tools/dupes.py
   python Rules/tools/backlog.py
   python Rules/tools/leverage.py
   python -m pytest Engine/tests -q
   ```
8. Continue only from the stated resume point — do not restart already-completed
   milestones, and do not skip ahead of a milestone marked blocked without first
   resolving its blocker.
9. When a milestone is completed (implementation + tests + verification passing +
   diff reviewed), update this file — §D (current → move to §C completed, pick new
   current), §B/§A percentages if materially changed, §E if a blocker was resolved,
   §H/§I/DO-NOT-FORGET if new deferrals or decisions were made.
10. Commit the updated `MILESTONES.md` **together with** the milestone's own changes (not
    as a separate follow-up commit), push to `origin/main`, fetch again, and verify
    local `HEAD == origin/main`, ahead/behind `0/0`, working tree clean.

---

## MILESTONE UPDATE RULE (permanent)

**`MILESTONES.md` must be updated after every completed milestone**, as part of the same
git checkpoint as the milestone's own commit. A milestone is complete only when:

1. implementation is complete
2. tests pass
3. verification passes (`verify.py`, `dupes.py`, `backlog.py`, `leverage.py`, pytest)
4. the diff has been reviewed
5. a git commit exists
6. the commit is pushed
7. local `HEAD == origin/main`
8. the working tree is clean
9. **this file has been updated** with the completed milestone
10. the next resume point is recorded here

If a milestone is committed without the corresponding update to this file, that is an
**incomplete checkpoint** and must be corrected before moving on. Percentages must be
recomputed from the category weights in §A — never incremented because time was spent.
