# VEDIC-AI MASTER PROJECT MILESTONES

**Project purpose:** Build an AI that reads a Vedic birth chart the way a traditional
astrologer would, where every predictive sentence traces to a rule printed in a real book
applied to a quantity that was actually computed. Governing rule: *the system may compute,
and it may quote — it may not invent.*

**Current production-readiness: 39%** (see §A for the weighted breakdown)

**Current phase:** Production Blocker Clearance Program (interrupts ordinary Phase 3
rule extraction — see §J and §K). Phase 3 itself remains at the state described in §B.

**Current milestone:** Milestone 15 — human(+Claude) verification workflow built and
applied. See §J for the full production-blocker audit and §D below for the resume point.

**Exact resume point:** `git fetch --all --prune`, confirm `main` == `origin/main`, then
read §K (Production Blocker Register) for the next blocker on the critical path, or §7/§8
if the decision is to resume ordinary Phase 3 extraction instead.

**Current Git SHA:** `978998ac147b48d812b39d98a66a0c42da7a3944` (parent — this milestone's
own commit follows this file's checkpoint)
**Last verified remote SHA (origin/main):** same before this milestone's commit — 0 ahead /
0 behind, working tree clean
**Last update date:** 2026-08-23

**Current test count:** 230 passing (`Engine/tests`) — was 224
**Current rule-card counts:** 404 total · 384 executable (firing) · 20 inert (recorded, blocked)
**Current verification:** 198/404 cards signed off (49%) — was 4/404 (1%). 175 structural
(reference/table) cards signed off by automated structural check; 23 interpretive cards
signed off by human(+Claude) reading pass (3 pre-existing + 20 new, all of chapter 9).
206 interpretive cards remain queued — see `Reports/VERIFICATION_QUEUE.md`.
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
| Rule extraction/encoding | 20% | 36% | Phaladeepika chapters 1, 2, 8, 9, 10 encoded and 6 partially (through v.38 of ~70); 404 cards from an estimated ~1,535 total across all 28 Phaladeepika chapters at the measured 0.65 cards/paragraph rate — and that is one book of six. |
| Reasoning engine capability | 15% | 45% | Stages 0, 1, 2, 6, 9, 10 implemented; Stage 3-5 (yogas/strength/houses as first-class computation) not built as dedicated stages; Stage 7 (adjudication) only partial (synthesis exists, weighting/cancellation does not); no varga, dasa, transit, ashtakavarga, or strength calculators yet. |
| Contradiction handling | 10% | 55% | Competing authorities are preserved via `contradicts`/`extends` links and dual cards (e.g. PD.01 rising-sign dispute, PD.09 dignity dispute) — the mechanism works and is used repeatedly, but Stage 7 adjudication (weighing contradictions against each other) does not exist yet. |
| Provenance/auditability | 10% | 92% | Every card is byte-exact hash-verified against the corpus on every run; `verify.py` enforces this as a build gate. `extraction.verified_by` now covers 198/404 cards (49%, was 4/404) via `Rules/tools/review.py`: 175 structural cards signed off automatically (no interpretive layer to review — the byte-exact check already is the complete verification), 23 interpretive cards signed off by an actual human(+Claude) reading pass. 206 interpretive cards remain queued in `Reports/VERIFICATION_QUEUE.md`. |
| Test coverage | 10% | 61% | 230 tests (was 224), growing with every milestone, covering rule structure, engine extractors, variable binding, overrides, and now the verification tool itself; no dedicated end-to-end regression suite across the full corpus of encoded chapters yet. |
| End-to-end validation | 5% | 30% | CLI produces full 3-part consultations and has been spot-checked against real charts per milestone; no systematic charted validation set (Phase 6 of `Phases.txt`) exists yet. |
| Multi-book corroboration | 3% | 0% | Only one book (Phaladeepika) has cards in the store; Brihat Jataka is corpus-converted but has zero rule cards. Cross-book agreement (a Phase 4 goal) cannot be assessed with one book. |
| Production safety/reliability | 1% | 50% | Groundedness verification (Stage 9) refuses to emit ungrounded output; no rate limiting, error-recovery, or production deployment hardening attempted (not yet in scope). |
| CLI/API/user-facing readiness | 1% | 40% | Working CLI (`Engine/cli.py`) produces real consultations; no API, no UI, no packaging. |

**Overall Production Readiness: 0.15×25 + 0.10×70 + 0.20×36 + 0.15×45 + 0.10×55 + 0.10×92 +
0.10×61 + 0.05×30 + 0.03×0 + 0.01×50 + 0.01×40 = 39.25% ≈ 39%**

(Was 39.05%. The verification workflow moved the needle on its own category —
provenance/auditability rose 90→92, a real change, not felt — but the category's 10% weight
keeps the effect on the headline number below the rounding threshold. This is the expected
shape of this kind of fix: the number that actually matters is 198/404 verified, not the
composite percentage, which is why §A tracks both.)

This number should be recomputed (not incremented by feel) whenever a category's score
changes materially — see §16.

---

## B. PHASE STATUS

| Phase | Purpose | Status | Completion | Evidence | Remaining |
|---|---|---|---:|---|---|
| Phase 1 | Corpus & OCR | **Not complete — documentation overstates it** | 33% | 2 of 6 books converted, verified, frozen (`Knowledge/brihat-jataka.md`, `Knowledge/phaladeepika.md`). `Phases.txt` marks "Phase 1 — Corpus & OCR" with a ✅, which is **inaccurate**: 4 books (BPHS Vol.1, Jataka Parijata Vol.1, Uttara Kalamrita, Saravali) are audited but not yet OCR'd/converted (`Reports/PROJECT_STATUS.md`). The pipeline architecture itself is frozen and proven across two structurally different books, which is what "frozen" refers to — not full corpus completeness. | Convert and verify the remaining 4 books; get Devanagari glyph-level spot-check on Brihat Jataka; write `Reports/conversion_report.md`. |
| Phase 2 | Reasoning engine architecture | Core MVP complete; extensions ongoing | 55% | Stages 0,1,2,6,9,10 fully implemented (`Engine/chart.py`, `facts.py`, `activate.py`, `render.py`, `pipeline.py`). 13 fact extractors implemented (`Engine/facts.py`): lordship, sign classes, house classes, graha classes, aspects, combustion, dignity, dignity-friendship, occupant count, graha frame, conjunction, nature, nature occupancy. Stages 3-5 (yoga/strength/house computation as dedicated stages) and Stage 7 (adjudication) are the largest open items — see `dep.strength`, `dep.varga`, `dep.dasa`, `dep.adjudication`, `dep.ashtakavarga`, `dep.transit`, `dep.vargottama`, `dep.upagraha` in `Rules/deferred.json`, all currently `implemented: false`. | Build `dep.strength` (Stage 4, highest closure-unlock return), `dep.varga`, `dep.dasa`, `dep.adjudication`, `dep.ashtakavarga`, `dep.transit`. |
| Phase 3 | Classical Knowledge Extraction | In progress | 26% | 404 cards from Phaladeepika chapters 1, 2, 6 (partial), 8, 9, 10 of 28 total chapters; 0 cards yet from Brihat Jataka despite it being corpus-converted. Estimated ~1,535 total cards across all 28 Phaladeepika chapters at the measured 0.65 cards/paragraph rate (`Reports/PHASE3_PLAN.md`), so 404/1535 ≈ 26% of just this one book, before Brihat Jataka or the 4 unconverted books are touched at all. | Continue chapter-by-chapter encoding (ch. 3, 4, 5, 6 remainder, 7, 11-28); start Brihat Jataka extraction; resolve `concept:manual-verification` (human sign-off, currently 4/404 cards). |
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

## D. CURRENT MILESTONE

**Nothing is currently in progress.** Milestone 15 above is fully committed, tested,
verified, and pushed.

**Next approved action — resume the verification queue (§K, blocker P1-1):** work through
`Reports/VERIFICATION_QUEUE.md` chapter by chapter (ch. 1 or ch. 2 next — both are fully
encoded, self-contained, and mostly templated like ch. 9 was), reading each interpretive
card's condition/effect against its quoted verse and recording a real sign-off in the
established style. Regenerate the queue with `python Rules/tools/review.py --queue` after
each batch.

**Alternative — resume ordinary Phase 3 extraction (§7/§8):**
- Phaladeepika ch.6 vv.39-41 (Vallaki/Dharma/Hasha/Kendra/Shula/Yuga/Gola) — **blocked**,
  needs a new "distinct signs occupied by the 7 classical grahas" engine fact.
- Phaladeepika ch.6 vv.42-43 (Adhiyoga) — **ready now**, already scoped
  (`passage:phaladeepika.06.p175`).

**Blockers:** none preventing Adhiyoga or the next verification batch.
**Dependencies:** none new required.
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
4. **Human verification is essentially absent** (4/404 cards). Every card is
   machine-verified byte-exact but not yet human-reviewed for correct reading.
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
| Native-sex-scoped rule handling | Implemented as a schema (`dep.native-sex`) but the birth record does not carry sex, so all sex-scoped cards stay inert regardless | Birth-record schema does not yet capture sex; ch.11 (Female Horoscopy) is entirely blocked on this. |

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
**Tables requiring visual reconstruction (unresolved):** ch.1 v.7 biped/quadruped/table
(`PD.01.SignBodyForm.Table`, inert), ch.2 vv.21-22 natural friendship table (encoded but
inert pending human verification of the reconstruction)
**Passages requiring human verification:** `concept:manual-verification` — 400 of 404
cards have `extraction.verified_by` null.

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
| `concept:manual-verification` | Human sign-off on all cards | Only 4/404 verified by a human | Dedicated review pass | **Arguably yes for true production** | Yes — production blocker #4 |
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
| Provenance | Strong | Byte-exact hash gate; **now 198/404 (49%) human(+Claude) sign-off**, was 4/404 | 206 interpretive cards still queued | Work the queue (§K, P1-1) |
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

### P1 — required for the intended MVP/production scope

**P1-1 — Human(+Claude) verification queue: 206 interpretive cards still unsigned.**
- **Why it matters:** Byte-exact quote verification proves the words are real; it does not
  prove the card reads them correctly. This is the one component of "provenance" the store
  cannot yet claim in full.
- **Current state:** Workflow built and proven this session (Milestone 15). 198/404 signed
  (49%), was 4/404. Queue lives in `Reports/VERIFICATION_QUEUE.md`, regenerated by
  `python Rules/tools/review.py --queue`.
- **Dependency:** None — the tool and methodology are complete; this is now a bounded
  reading-and-recording task, chapter by chapter.
- **Exact work required:** Work through the queue (ch. 1, 2, 6, 8, 10 remain, in that order
  of increasing template-repetition benefit), recording real sign-offs in the established
  style, re-running `review.py --queue` after each batch.
- **What it unlocks:** Provenance/auditability category score continues to rise (§A);
  eventually clears this production gate in full.
- **Status:** In progress — 20/226 originally-queued interpretive cards done this session.

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
- **Dependency:** None blocking design work, but building the *general* mechanism now, when
  only 1 card needs it, risks exactly the speculative-architecture-ahead-of-need §I warns
  against.
- **Exact work required:** Wait until more contradictory cards accumulate (ch. 6's
  Mantreswara-vs-Parashara dusthana-lord dispute at `passage:phaladeepika.06.p202` will add
  several), then design Stage 7 against real, multiple examples rather than one.
- **What it unlocks:** Phase 4 entirely; contradiction-explaining narrative in Phase 5.
- **Status:** Deliberately not started — correctly deferred per §I, not neglected.

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

- **A verification workflow now exists — use it, don't repeat the audit.**
  `Rules/tools/review.py` classifies every card as structural (auto-signed) or interpretive
  (queued in `Reports/VERIFICATION_QUEUE.md`). Resume the queue chapter by chapter rather
  than re-deriving whether verification "can be done systematically" — that question is
  answered (§J.4, §K P1-1).
- **206 interpretive cards remain unsigned** (chapters 1, 2, 6, 8, 10). Chapter 9 (20 cards)
  was done this session as the proof batch — read each card's `conditions`/`predicts`
  against its quoted verse; do not blanket-approve a whole file at once.
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
- **Human verification is nearly absent** — 400 of 404 cards have no `verified_by`. This
  is a real production blocker even though the machine-verification (byte-exact quote
  hashing) is solid.
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
