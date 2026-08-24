# VEDIC-AI MASTER PROJECT MILESTONES

**Project purpose:** Build an AI that reads a Vedic birth chart the way a traditional
astrologer would, where every predictive sentence traces to a rule printed in a real book
applied to a quantity that was actually computed. Governing rule: *the system may compute,
and it may quote — it may not invent.*

**Current production-readiness: 59%** (see §A for the weighted breakdown; was 58.80% ≈ 59%
after Milestone 23, and stays 59% here — see Milestone 24's own note on why its real work does
not clear the bar to move a category score under this file's own conservative recomputation
discipline). Card count moved slightly — 501 → 504 — from an encoding pass, not a chapter
completion.

**Current phase:** Phase 4 (Knowledge Integration) is properly under way; Milestone 24 is
ordinary Phase 3 encoding that happened to depend on Phase 4's neighbour, Phase 2's Stage 4.
Stage 7's *representation* half is built; its *weighting* half is deliberately not, and is not
scheduled.

**Current milestone:** Milestone 24 — **the blanket strength condition on chapter 6's Pancha
Mahapurusha Yogas, and the second Duryoga**: `passage:phaladeepika.06.p009` and
`passage:phaladeepika.06.p233`. Ch.4's `dep.strength` (Milestone 22) is used, for the first
time, to gate encoding rather than an engine stage — v.9's "vested with strength ... not
conjunct a malefic" clause is added to `PD.06.Ruchaka/.Bhadra/.Hamsa/.Malavya/.Sasa`, and v.70's
second Duryoga is encoded as two new cards. The milestone's sharpest finding is a real,
evidenced narrowing: the golden/demo chart's Ruchaka claim, firing since Milestone 7, is now
correctly withheld, because Mars there is merely own-sign and ch.4 vv.4-5 do not call own-sign
alone "strong". A second finding, arguably more interesting: one of the two new Duryoga cards
(`PD.06.Duryoga`, the verse's own named configuration) could not be shown firing on *any* chart,
real or constructed, and the reason is now documented rather than left to be rediscovered — see
the card's own note and `Engine/tests/test_chapter_six_strength.py`.

**Exact resume point:** `git fetch --all --prune`, confirm `main` == `origin/main`, then pick up
§D. There is still **no open P0**. §D's recommended next milestone is
`passage:phaladeepika.06.p202` — vv.57-69, the twelve dusthana-lord yogas and the chapter's
richest contradiction (Mantreswara vs. Parashara) — continuing chapter 6 in the natural reading
order and giving Stage 7 adjudication a second genuine claim-to-claim contradiction to read.
**Five decisions are owed by a human**, none blocking that: `concept:moon-nature-criterion`
(Milestone 20), `concept:strength-criterion-scope` (Milestone 21),
`concept:retrograde-combust-collision` (Milestone 22), `concept:parallel-of-overloaded`
(Milestone 23), and `concept:p009-lagna-or-moon-clause` (new — see §D) — the disjunctive
"Lagna or Moon" half of v.9 that this milestone deliberately left unencoded because the Lagna
carries no strength verdict anywhere in this store.

**Current Git SHA:** `a5575d1c232f2db27ea4c4d2395b09a2349d0505` (parent — this milestone's own
commit follows this file's checkpoint)
**Last verified remote SHA (origin/main):** same before this milestone's commit — 0 ahead /
0 behind, working tree clean
**Last update date:** 2026-08-24

**Current test count:** 341 passing (`Engine/tests`) — was 334. Seven new: one renamed/rewritten
and one new sibling in `Engine/tests/test_slice.py` (the golden chart's Ruchaka claim now
withheld, and a constructed positive control showing it returns once Mars is genuinely
exalted); a new `mahapurusha` fixture in `Engine/tests/test_adjudication.py` (the demo chart no
longer exercises the `parallel_of` link to Jataka Parijata's corroboration, since Ruchaka no
longer fires there); and six in the new `Engine/tests/test_chapter_six_strength.py` — scope
(only the five Mahapurusha cards carry the new clauses; an unrelated graha's strength does not
affect Ruchaka), the retrograde-combust collision reproduced for a Mahapurusha card specifically,
`PD.06.Duryoga.Reverse` firing on a constructed chart, and `PD.06.Duryoga`'s structural
unfireability confirmed by comparing its condition tree against its mirror's.
**Current rule-card counts:** **504 total** · 487 executable (firing) · **17 inert** — inert
count unchanged; +3 firing/reference (`PD.06.PanchaMahapurusha.StrengthCondition`, reference;
`PD.06.Duryoga`, `PD.06.Duryoga.Reverse`, both active). Five existing cards
(`PD.06.Ruchaka/.Bhadra/.Hamsa/.Malavya/.Sasa`) had their `conditions` rewritten, not replaced —
the dignity+kendra naming clause is untouched, two clauses were added.
**Current verification:** **501/504 cards signed off (99.4%)** — same three standing holdouts
(`PD.01.Kalapurusha.Strength`, `PD.10.Venus.VargaMarsSaturn`, `PD.04.Lagna.TripedSign`); every
other new or rewritten card this milestone touched was signed by hand
(`tarunrameshphotography + Claude`), including the three new cards and the five rewritten ones,
because rewriting a condition — or authoring a reference card whose note carries a real scope
judgment — is an interpretive act and an inherited or automated sign-off would have been false.

**Backlog (Milestone 24):** 138 entries (was 136). `passage:phaladeepika.06.p009` and
`passage:phaladeepika.06.p233` move to `resolved`. Two new entries: `concept:p009-lagna-or-moon-clause`
(the tracked remainder of v.9) and `passage:phaladeepika.06.colophon` (split out of p233 so its
resolution reflects only the doctrine it actually gained, matching `passage:phaladeepika.04.colophon`'s
own treatment). One new dependency, `dep.lagna-strength` (`implemented: false`) — genuinely new,
not a bookkeeping correction: no encoded chapter states a Lagna-specific strength verdict, and no
extractor derives one, so `strength(Lagna,...)` is both a doctrine gap and an engine gap. It
deliberately carries no `predicate` field in the registry, because `dependency_state()` in
`Rules/tools/backlog.py` marks a dependency implemented the moment ANY extractor emits its named
predicate anywhere — and `strength` already is, for grahas. Giving `dep.lagna-strength` the same
predicate name would have reported it falsely resolved the instant it was declared, which is
exactly the kind of tooling-correct/input-wrong signal Milestone 22 had to catch for `dep.strength`
itself; caught here before it shipped, by reading `backlog.py`'s own logic rather than trusting
its first output.

**Original Milestone 23 note on the backlog:** 136 entries (was 135). One new concept entry,
`concept:parallel-of-overloaded`, and one new dependency, `dep.adjudication-representation`
(`implemented: true`), which is the capability actually built. **`dep.adjudication` itself was
deliberately left outstanding.** Eleven registry entries declare it, this milestone releases
none of them, and marking it implemented would have reported all eleven as newly unblocked —
the same false signal Milestone 22 had to correct after building `dep.strength`. Its `effort`
stays 8, and no `depends_on` edge was drawn to the new entry, because `leverage.py` charges an
entire dependency closure and would have re-billed work already done.

**Original Milestone 22 note on the backlog:** 135 entries (was 137), and the arithmetic is worth stating because it is the
first milestone whose backlog *shrank*: −4 card entries (the four cards that went active stop
being deferred knowledge) and +2 concept entries
(`concept:retrograde-combust-collision`, `concept:strength-is-not-bhava-strength`). The four
cards that stayed inert were already counted and still are. Six new dependencies were
catalogued, five of them
named honestly *because* building Stage 4 revealed that cards were declared against the wrong
blocker: `dep.strength-ranking`, `dep.shadbala-arithmetic`, `dep.compound-friendship`,
`dep.kendra-togetherness`, `dep.body-part-significator`. `dep.strength` itself is now
`implemented: true`, computed from `Engine/facts.py` rather than declared, and has dropped off
`leverage.py` entirely.

**Original Milestone 20 note on the backlog:** 119 entries (was 89). The 30 new entries are the accounting cost of entering a second book honestly: 27 unencoded Brihat Jataka chapters, 1 passage entry claiming the 147 paragraphs of its chapter 2 that these cards do not quote, and the 2 concept questions this milestone's source work produced (`concept:moon-nature-criterion`, `concept:kala-bala-benefic-scope`). Nothing about the second book is silently deferred.

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
| Source verification | 10% | 77% | Corpus pipeline verified byte-exact with hallucination detection, verse reconciliation, figure transcription for the 2 converted books. **The Devanagari glyph-level spot-check owed on Brihat Jataka has now begun** (Milestone 20): ch. 2 v. 5's closing line was compared glyph by glyph against the rendered page and 2 OCR defects found and recorded (`व`→`र`, `सु`→`स`), neither affecting any encoded card. One line is not a spot-check pass, but it is the first evidence about the real error rate rather than an estimate. |
| Rule extraction/encoding | 20% | 42% | Phaladeepika chapters 1, 2, **4**, 8, 9, 10 encoded and 6 partially (through v.9 and v.70 of ~70, Milestone 24); 502 Phaladeepika cards (+2 Brihat Jataka = 504 in the store) from an estimated ~1,535 total across all 28 Phaladeepika chapters at the measured 0.65 cards/paragraph rate — and that is one book of six. Chapter 4 alone contributed 94, and it is the densest chapter encoded so far: 163 paragraphs of computational doctrine, almost all of it `reference` rather than firing. **Milestone 24 added 3 cards (1 reference, 2 firing) and rewrote 5 existing ones' conditions** — held at 42%, not moved: three cards against an estimated ~1,535-card total is below what this table's own rounding can register, and no new chapter was completed (chapter 6 remains partial). |
| Reasoning engine capability | 15% | 65% | Stages 0, 1, 2, **4**, 6, **7 (reading half)**, 9, 10 implemented; Stages 3 and 5 (yogas/houses as first-class computation) not built as dedicated stages; **Stage 7's weighting half deliberately does not exist and is not scheduled**; no varga, dasa, transit or ashtakavarga calculators, and no *numeric* strength calculator — the source withholds the arithmetic one would need (`dep.shadbala-arithmetic`). **Raised 60→65 in Milestone 23: Stage 7's representation half exists** — every relationship the store declares between two cards is read, typed and reported with both sides quoted, and an `unresolved` outcome is a finished answer rather than a placeholder. Not higher, because the half that would let the engine *choose* between two source-backed claims is absent by design: no encoded source supplies a rule for choosing, and the only precedence applied anywhere in the engine is the one verse 4 states in its own sentence. **Previously raised 52→60 in Milestone 22: Stage 4 exists and P0-1 is closed** — every chart now produces graha strength verdicts, read from chapter 4's own cards, and the largest "born inert" tax on every future chapter is paid. Not higher, for three reasons that are the source's and not the schedule's: it is graha strength only (no Bhava Bala — the components are withheld), it is a binary verdict and not an order (no `strongest`), and Stage 3 (yogas) and Stage 5 (houses) are still not dedicated stages. **Previously raised 45→52 in Milestone 20**, the first increase from real capability rather than bookkeeping: P0-2 is closed (all 9 grahas now carry a `nature` fact, so the 22 benefic-conditioned cards can fire), and the first piece of Stage 7 exists — per-graha authority attribution and cross-book corroboration in `_resolve_nature`. Still 52 and not higher because Stage 7's *hard* half — adjudicating authorities that actually disagree — remains unbuilt and deliberately so (§K, P1-3). |
| Contradiction handling | 10% | 82% | Competing authorities are preserved via `contradicts`/`extends` links and dual cards (e.g. PD.01 rising-sign dispute, PD.09 dignity dispute) — the mechanism works and is used repeatedly, but Stage 7 adjudication (weighing contradictions against each other) does not exist yet. **71→82 in Milestone 23**, the largest single move this category has had, and it is a *reading* gain rather than a mechanism gain: the `contradicts`/`extends`/`parallel_of` links were being written faithfully into the store and read by nothing, so no consultation had ever surfaced one. All four relationship types now reach the reader with card id, book, chapter, verse, printed page and both sides' own words. It also repaired a live defect — on 83% of 720 scanned charts Part 3 was printing a verse and its own translator's refutation as *agreeing*, under a heading reading "Terms that recur without contradiction". Not higher for two stated reasons: the engine still cannot choose where the source does not, and `parallel_of` cannot distinguish agreement from a variant reading (`concept:parallel-of-overloaded`), so cross-book *corroboration* of a yoga still cannot be claimed. **68→71 in Milestone 22:** the first *chart-dependent* refusal. A graha that is both retrograde and combust is called strong by ch. 4 v. 5 and weak by v. 4, and the extractor emits no verdict for it, reports the collision by name in the consultation's own "doctrine read, but not complete" section, and lets every rule about its strength correctly not fire. Earlier contradiction handling was static — two cards linked at encoding time; this one only exists on charts that satisfy both. |
| Provenance/auditability | 10% | 98% | Every card is byte-exact hash-verified against the corpus on every run; `verify.py` enforces this as a build gate. `extraction.verified_by` now covers **501/504 cards (99.4%**, was 4/404) via `Rules/tools/review.py`: 271 structural cards signed off automatically (no interpretive layer to review — the byte-exact check already is the complete verification), 230 signed off by an actual human(+Claude) reading pass across chapters 1, 2, 4, 6, 8, 9 and 10 — including 33 of chapter 4's and, as of Milestone 24, the three new and five rewritten chapter 6 cards, re-signed by hand because their encoding involved a real judgement. The interpretive queue is closed; the 3 unsigned cards are deliberate, documented defect holdouts, not unreviewed cards. Not 100% because those three defects are real and still open. **97→98 in Milestone 23:** every adjudication carries the full provenance of both parties and is re-checked by Stage 9 (`verify_adjudications`), so a conclusion *about* sources can be walked back to them the way a claim can; and a relationship link naming a card that does not exist now fails the build, because a link the engine reads is a link whose typo silently costs a reported contradiction. |
| Test coverage | 10% | 76% | 270 tests (was 250), growing with every milestone, covering rule structure, engine extractors, variable binding, overrides, the verification tool itself, and now chapter 4's encoding (`Engine/tests/test_chapter_four_strength.py`, +20 tests: the two authorities never merged, the Mars row's printed defect pinned as printed, the unquantified components pinned as unquantified, and the verses-4-and-5 verdict set pinned as the only source Stage 4 may read); no dedicated end-to-end regression suite across the full corpus of encoded chapters yet. **Milestone 24: 341 tests (was 334)**, +7 in `Engine/tests/test_chapter_six_strength.py` and `test_slice.py`/`test_adjudication.py` fixture updates — held at 76%, not moved: a 2% test-count increase focused on one chapter's encoding is smaller than the swings that have moved this row before, even though the specific finding it pins (a card confirmed structurally unfireable, not merely untested) is a genuine methodological addition. **72→76 in Milestone 23:** 334 tests (was 302), the 32 new ones in `Engine/tests/test_adjudication.py` — and, for the first time in this project, the suite was checked by *mutating the module under test*: four deliberate breakages (directional link reading, treating every `parallel_of` as a second authority, resolving what should stay unresolved, deleting the strength collision's refusal) were each confirmed to fail it, and the second one initially did **not**, which exposed a test that checked the discriminator's input rather than its output. **68→72 in Milestone 22:** 302 tests (was 271), the 30 new ones in `Engine/tests/test_strength.py` covering the extractor's doctrine reading, its calculation on placed edge cases, the retrograde/combust refusal, determinism, and — the ones that matter most — the negatives: no fact carries a number, a component is not a verdict, retrogression does not make the nodes strong, and the doctrine dies with its cards. |
| End-to-end validation | 5% | 36% | CLI produces full 3-part consultations and has been spot-checked against real charts per milestone; no systematic charted validation set (Phase 6 of `Phases.txt`) exists yet. **Milestone 24:** 2,176 real nativities (four cities, 1950-2010) run end to end with **zero pipeline or verification failures** — held at 36%, not moved: the sweep confirms the milestone's own findings (a 29.2% Mahapurusha firing rate, zero natural occurrences of either Duryoga card, an unchanged 13.6% collision rate) without adding a new *kind* of end-to-end evidence beyond what Milestones 22-23 already established this row on. **33→36 in Milestone 23:** 720 nativities across four cities and sixty years were run end to end with **zero pipeline or verification failures**, and the frequency of each relationship type was measured rather than asserted — which is how the 83% figure above is known. Still not Phase 6: nothing here checks whether a prediction is *correct*. **30→33 in Milestone 22:** the first time the project *searched* a chart space rather than spot-checking one nativity — 880 real birth instants were scanned to find a chart for each newly-activated card and to confirm each one actually fires. That is not Phase 6, but it is the first evidence that an activated card is not merely well-formed. |
| Multi-book corroboration | 3% | 30% | **No longer zero (Milestone 20).** Brihat Jataka now has 2 rule cards, and cross-book agreement is not only assessable but implemented and surfaced: 4 grahas' natures are corroborated by both books, and the consultation reports which claims rest on one authority and which on two. Scored 25%, not higher, because corroboration exists for exactly one relation (`graha_nature`) out of the whole store, and the second book has 2 cards against the first book's 499. **25→30 in Milestone 23:** three further books — Jataka Parijata, Saravali and Uttarakalamrita — now reach the reader in their own words, on 92% of charts, wherever the translator reports them on a doctrine the chart activates. Only +5, and deliberately: those statements are reported as *a second authority on the same doctrine* and **not** as corroboration, because one of them states a materially different condition for the same yoga and the store's `parallel_of` link does not record which kind it is. |
| Production safety/reliability | 1% | 50% | Groundedness verification (Stage 9) refuses to emit ungrounded output; no rate limiting, error-recovery, or production deployment hardening attempted (not yet in scope). |
| CLI/API/user-facing readiness | 1% | 40% | Working CLI (`Engine/cli.py`) produces real consultations; no API, no UI, no packaging. |

**Overall Production Readiness: 0.15×25 + 0.10×77 + 0.20×42 + 0.15×65 + 0.10×82 + 0.10×98 +
0.10×76 + 0.05×36 + 0.03×30 + 0.01×50 + 0.01×40 = 58.80% ≈ 59%**

Recomputed from the table, not incremented — and unchanged from Milestone 23. **No category
score moved in Milestone 24.** This is a deliberate reading of the table's own rows, each
explained where it appears: 3 cards and 5 rewritten conditions is below what "Rule
extraction/encoding" registers against an estimated ~1,535-card total; no new engine mechanism
was built, by design, so "Reasoning engine capability" and "Contradiction handling" could not
move; and while both "Test coverage" (+7 tests) and "End-to-end validation" (a 2,176-chart
sweep) grew, neither cleared the bar the swings that moved those rows in Milestones 22-23 did.
The milestone's real content — a genuine, evidenced narrowing of five long-fired cards, and a
card proven structurally unfireable rather than merely untested — is methodological rigor, not
new capability or new corpus, and this table does not have a row for that. Recording it here
rather than inflating an adjacent row is the same discipline Milestone 23 applied when it
declined to credit "Rule extraction" for links the encoders had already written down.

Movement from 56% (Milestone 22) to 58.80% is +3 points across six categories, unchanged since
Milestone 23: contradiction handling 71→82 (+1.10 pts), reasoning capability 60→65 (+0.75), test
coverage 72→76 (+0.40), end-to-end validation 33→36 (+0.15), multi-book corroboration 25→30
(+0.15), provenance 97→98 (+0.10). Sum of deltas 2.65, and 56.15 + 2.65 = 58.80, which agrees
with the expression above — the two are cross-checked here precisely because §A's own history
contains four milestones of a figure that did not.

**Previous figure (Milestone 23):** identical expression and result to the one above —
58.80% ≈ 59%. Rule extraction did not move there either: not one card was added, removed,
re-quoted or re-conditioned in that milestone — 501 before, 501 after — and it did not so much
as open a chapter file. Corpus completeness and source verification did not move either: no
page was rendered and no book was converted. The temptation there was subtler than Milestone
22's: it would have been to credit the *encoding* score for relationships the encoders had
already written down and that milestone merely learned to read. Those links were encoded in
Milestones 1-14 and were already counted then.

**Previous figure (Milestone 22):** 0.15×25 + 0.10×77 + 0.20×42 + 0.15×60 + 0.10×71 +
0.10×97 + 0.10×72 + 0.05×33 + 0.03×25 + 0.01×50 + 0.01×40 = 56.15% ≈ 56%

**Previous figure (Milestone 21):** 0.15×25 + 0.10×77 + 0.20×42 + 0.15×52 + 0.10×68 +
0.10×97 + 0.10×68 + 0.05×30 + 0.03×25 + 0.01×50 + 0.01×40 = 54.10% ≈ 54%

**Previous figure (Milestone 20):** 0.15×25 + 0.10×75 + 0.20×36 + 0.15×52 + 0.10×62 +
0.10×97 + 0.10×65 + 0.05×30 + 0.03×25 + 0.01×50 + 0.01×40 = 51.80% ≈ 52%

Recomputed from the table above, not incremented — see the correction note below for why that
distinction is now a standing rule. Movement from 49% is +3 points across five categories
(source verification +5, reasoning capability +7, contradiction handling +7, test coverage +2,
multi-book corroboration +25), all of it attributable to Milestone 20's actual work.

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
| Phase 2 | Reasoning engine architecture | Core MVP complete; extensions ongoing | 66% | Stages 0,1,2,6,**7 (reading half)**,9,10 fully implemented (`Engine/chart.py`, `facts.py`, `activate.py`, `render.py`, `pipeline.py`). **14** fact extractors implemented (`Engine/facts.py`): lordship, sign classes, house classes, graha classes, aspects, combustion, dignity, dignity-friendship, occupant count, graha frame, conjunction, nature, nature occupancy, **strength** (Milestone 22). **Stage 4 (graha strength) now exists**, as a verdict extractor rather than a calculator — the source withholds the arithmetic a Shadbala Pinda would need. **Stage 7's reading half now exists** (`Engine/adjudicate.py`, Milestone 23), so Stages 3 and 5 (yoga/house computation as dedicated stages) are the largest remaining items — see `dep.varga`, `dep.dasa`, `dep.ashtakavarga`, `dep.transit`, `dep.vargottama`, `dep.upagraha` in `Rules/deferred.json`, all currently `implemented: false`; `dep.strength` and `dep.adjudication-representation` are `implemented: true`, and `dep.adjudication` (weighting) is outstanding by design. | ~~Build `dep.strength`~~ **done, Milestone 22**. ~~Build the adjudication representation~~ **done, Milestone 23**. Build `dep.varga`, `dep.dasa`, `dep.ashtakavarga`, `dep.transit`. |
| Phase 3 | Classical Knowledge Extraction | In progress | 33% | 502 cards from Phaladeepika chapters 1, 2, **4**, 6 (partial, through v.9 and v.70 of ~70 as of Milestone 24), 8, 9, 10 of 28 total chapters, plus 2 from Brihat Jataka ch. 2. Estimated ~1,535 total cards across all 28 Phaladeepika chapters at the measured 0.65 cards/paragraph rate (`Reports/PHASE3_PLAN.md`), so 502/1535 ≈ 33% of just this one book, before the rest of Brihat Jataka or the 4 unconverted books are touched at all. | Continue chapter-by-chapter encoding (ch. 3, 5, 6 remainder — vv.39-43, 57-69 next, ch. 7, 11-28); extend Brihat Jataka extraction; human sign-off is no longer the bottleneck (501/504, see §K P1-1). |
| Phase 4 | Knowledge Integration | **Under way (Milestones 20, 23)** | 40% | `Phases.txt` names six things for this phase — rule conflicts, priority, weighting, cancellation, reinforcement, cross-book agreement. **Milestone 23 settled four of them, two by building and two by finding they needed nothing built.** *Conflicts* are now read, typed and reported with full provenance (`Engine/adjudicate.py`). *Priority* exists only where a source states it — the combustion override, applied on 11% of charts — and nowhere else. *Cancellation* turned out to need no mechanism at all: the one real cancellation doctrine in the store (Sakata Yoga, ch. 6 v. 17) is printed in the same sentence as the yoga it cancels, so it is a negated conjunct inside the card's own condition and has been working since Milestone 9; the same is true of every "unless" in the store. *Cross-book agreement* is reported for `graha_nature` and three further books' statements now reach the reader, though deliberately not as corroboration. **Weighting is the one item deliberately not built and not scheduled**, and *reinforcement* is untouched. Earlier: the corroboration half of Stage 7 was built and exercised (Milestone 20): two books now classify grahas by nature, agreement between them is recorded per graha (`authorities`, `books`, `corroborated`) rather than the second authority overwriting the first, and the consultation reports it. `dep.rule-transfer` and `dep.dignity-override` remain as narrow primitives. | Rule *reinforcement*, and resolving `concept:parallel-of-overloaded` so a yoga stated by two books can be reported as corroborated the way a graha's nature already is. **Not** weighting: it stays unbuilt until a source supplies a rule for choosing, and none does (§K, P1-3). |
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

### Milestone 20 — Brihat Jataka's natural benefic/malefic classification: P0-2 closed, first cross-book corroboration

**Phase:** 3 (knowledge) + 4 (integration) — Phase 4 begins here
**Status:** COMPLETE
**Completion:** 100%

**The blocker:** P0-2, found in Milestone 19. Jupiter and Venus — the two principal natural
benefics — received no `nature` fact on any chart, because the only encoded classification
(Phaladeepika ch. 2 v. 27 and its Notes) names the malefics exhaustively and names only the
waxing Moon and unassociated Mercury as benefic. 22 active cards conditioning on `benefic`
under-fired on every consultation. `PD.10.Benefics.In7` could not fire for Jupiter in the 7th.

**Source work first, encoding second.** Three candidate sources were identified in Milestone
19. Brihat Jataka ch. 2 v. 5 was chosen, and then actually checked rather than assumed:

1. **The quote was verified against the rendered source page, not just the corpus.** Image
   `p0033` (printed p.30) confirms the OCR character for character. It also settled a
   provenance question that mattered: the classification sits in the **main translation body**,
   in a paragraph that ends before the italicised `Commentary:` marker — so it is translation,
   not the translator's commentary, and does not fall under the apparatus rule that would have
   disqualified the ch. 8 candidate.
2. **The verse behind it was read.** The Devanagari of v. 5 (image `p0034`, printed p.31)
   reads `क्षीणेन्द्वर्कमहीसुतार्कतनयाः पापा बुधस्तैर्युतः` — "the **क्षीण** (diminished/waned) Moon, Sun,
   Mars, Saturn are malefics; Mercury when joined with them." **It contains no numeral.**
3. **Which resolved the Moon question that had been the whole reason this needed adjudication.**
   The printed English reads "the Moon (within less than 72 degrees distance from Sun)". That
   figure is the **translator's editorial gloss**, printed in parentheses, with no warrant in
   the verse. Milestone 19 had recorded this as a genuine cross-book contradiction — Brihat
   Jataka by elongation vs. Phaladeepika by waxing/waning — and concluded that Stage 7
   adjudication had to be built before the fix could be taken. **That conclusion was wrong, and
   reading the Sanskrit is what showed it.** Both books condition the Moon on the same
   underlying term; only their translators' renderings of it differ.
4. **Two Devanagari OCR defects were found** in that line (`व` misread as `र`, `सु` as `स`) —
   the first concrete evidence about this book's Devanagari error rate, which had been an
   estimate since conversion. Neither touches any encoded card. Recorded in the new manifest's
   `known_defects`.

**What was encoded:** `BJ.02.Nature.Malefics` (Sun, Mars, Saturn outright; Mercury conditional
on malefic company) and `BJ.02.Nature.Benefics` (**Jupiter and Venus outright**; Mercury
conditional). Both are `reference` cards, both byte-exact at multi-span quotes, both carrying a
real human(+Claude) sign-off rather than the automated structural one, because deciding what to
assert here was a judgement and not a transcription.

**The Moon clause is quoted in full and asserted by neither card.** This is the milestone's
central editorial decision and it was made deliberately rather than by default. Encoding the
72-degree gloss as doctrine would manufacture a cross-book contradiction out of two renderings
of one Sanskrit word; encoding it as "waning" would silently substitute Phaladeepika's wording
for what this page actually prints. Both are choices a verification-and-encoding pass has no
standing to make. So the Moon is left to Phaladeepika, which classifies it unopposed and is
**not overwritten**, and the question is registered as `concept:moon-nature-criterion` for a
human to decide. Pinned by three tests so a later session cannot resolve it quietly.

**The smallest Phase 4 mechanism the real relationship required — corroboration, not
resolution.** Once the Moon was correctly classified as a translation difference rather than a
doctrinal conflict, the two books turned out to **agree everywhere they both speak**. So what
Stage 7 needed here was not a way to choose between authorities but a way to record that two of
them concur:

- `settle()` in `Engine/facts.py` now accumulates authorities instead of overwriting, and each
  nature fact carries `authorities`, `books` and `corroborated`.
- Attribution became **per graha rather than per extractor run**. Previously every nature fact
  cited every `graha_nature` card in the store. With one book that was harmless; with two it is
  a false citation — Phaladeepika's cards say nothing whatever about Jupiter. This was a real
  provenance defect created by the second book's arrival and fixed in the same milestone.
- The consultation now reports cross-book agreement in its "Scope and silence" section, as
  counts of books and never as a score.
- **The refusal to adjudicate genuine conflict is untouched**, and now names both offending
  cards in its error instead of just declining. A test asserts it still raises.

**Result:** all 9 grahas carry a `nature` fact. Sun, Mars, Saturn and Mercury are corroborated
by both books; Jupiter and Venus rest on Brihat Jataka; Moon, Rahu and Ketu on Phaladeepika.
On the demo chart the claim count moves **35 → 41**, with five further cards reaching their
conditions (`PD.06.Parijata`, `PD.06.Subhavesi`, `PD.06.Subhavasi`, `PD.06.Subhobhayachari`,
`PD.10.Couple.BeneficAspect`) and **nothing that previously fired ceasing to fire** — purely
additive, which is what adding a classification rather than altering one should do.

**Accounting cost, paid rather than deferred:** entering one chapter of a 28-chapter book means
the rest must be explicitly claimed. 30 backlog entries were added (27 chapters, 1 passage entry
covering the 147 unquoted paragraphs of ch. 2, 2 concept questions), taking the backlog 89 → 119.

**Tests:** +9 (241 → 250). Two tests that asserted the *old* behaviour — that Jupiter and Venus
were unclassified — were **inverted rather than deleted**, and now assert that the
classification exists and is attributed to the book that makes it, with a note that the fix for
a future failure is a card and never a Python constant. New tests cover: Jupiter and Venus
benefic from an encoded source; corroboration recorded for grahas both books classify; *not*
recorded for grahas only one classifies; a benefic clause now satisfiable by Jupiter; the Moon
asserted by neither Brihat Jataka card while still quoted; the Moon question registered in the
backlog; the Moon still resolving from Phaladeepika; **the Kala Bala statement not encoded as
general nature doctrine**; that scope decision registered; genuine contradiction still raising
with both cards named; and the consultation reporting agreement without scoring it. The two
golden claim-count assertions were updated 35 → 41 with the five newly-firing cards named — the
test's own comment already required that this number move only when doctrine is added.

**Why this milestone matters:** It closes the most consequential defect the project has found,
and it does so by the project's own rules — no graha was ever hardcoded as benefic; a book was
encoded and the same extractor read it. More importantly it shows what the source discipline is
actually *for*: Milestone 19 had correctly identified a blocker and correctly identified that
adjudication gated it, and reading the Sanskrit behind one parenthetical dissolved the gate
entirely. A session that had trusted the English would have built a contradiction-adjudication
engine to resolve a contradiction that does not exist.

### Milestone 21 — Phaladeepika chapter 4 encoded in full: the source half of P0-1

**Phase:** 3 (knowledge)
**Status:** COMPLETE
**Completion:** 100% of the encoding half of P0-1. The engine half (Stage 4) is not started
and deliberately so.

**What this milestone is:** the chapter that `dep.strength` must be built from is now in the
store - 94 cards, 163 paragraphs, byte-exact. **No strength engine was built.** A chart still
produces no strength fact today, and the reasoning-capability score was left untouched to say
so.

**The chapter turned out to print two strength doctrines by two different authorities, and
separating them is the milestone's substance.** This was not visible from the chapter title:

- **Paragraphs 1-83 (printed pp.35-42)** are the *translator's survey of "the views of other
  ancients"* - the familiar Shadbala apparatus, Shastyamsa arithmetic at 60 to the Rupa, the
  tables everyone expects. **55 cards.** Framed by `PD.04.Frame.OtherAncients`, which names
  the works the chapter itself credits (Sripati Padhati, Keshavi Jataka, Brihat Parasara Hora
  Shastra, Jataka Padhati by Bhu Deva).
- **Verses 1-24 (printed pp.42-50)** are **Mantreswara's own doctrine**, and he names a
  **different six balas** (`PD.04.SixBalas.Order`: Kala, Chesta, Uchcha, Dik, Ayana, Sthana)
  and leaves them almost entirely unquantified. **34 cards.** Framed by
  `PD.04.Frame.Mantreswara`.
- A further **5 cards** carry the translator, Dr. G. S. Kapoor, as their authority where the
  text is his and not either scheme's.

The two are separated by `predicts.authority` and by tier and are **never merged**, including
where they cover the same bala under the same name. They disagree substantively and the store
records that rather than smoothing it: Jupiter's Bala Pinda is 6-32 in the survey's table
against 8.5 Rupas in Mantreswara's verse 22, which the translator's own framing explains only
partly.

**The strength criterion the engine will implement is not the chapter's formal one, and this
is the milestone's most consequential decision.** Verses 22-23 give Mantreswara's real
definition - a graha is strong when its Shadbala Pinda reaches a per-graha threshold in Rupas
(`PD.04.BalaPinda.Thresholds`). **That is not computable and will not become computable from
this chapter**, because the six components that would sum to a Pinda are quantified only in
the *other* authorities' scheme, and even there the source **explicitly withholds the
arithmetic for three of them** (Yudha, Chesta, Drig - each recorded as withheld rather than
guessed at). So the `strong`/`weak` verdicts Stage 4 will emit come instead from **verses 4
and 5**, which state "strong" and "weak" outright about conditions the engine can already
evaluate: exalted, retrograde, retrograde-in-debilitation, combust (weak, overriding
dignity), and Rahu/Ketu by sign. Registered as `concept:strength-criterion-scope` so this is
never quietly forgotten. **A graha the engine calls strong is one Phaladeepika calls strong
for a stated reason - not one whose Shadbala Pinda has been measured**, and a consultation
must never imply otherwise.

**Three printed defects were found, confirmed against the rendered pages, and preserved as
printed rather than corrected:**

1. **Mars's Bala Pinda row does not add up** (`PD.04.BalaPinda.OtherAuthorities`). Six of the
   seven rows sum exactly; Mars's does not. 1-16 + 0-30 + 0-40 + 1-7 + 0-20 = 233 Shastyamsa
   = **3-53**, against a **printed total of 4-13**. Saturn's row, whose other four cells are
   identical, carries 1-36 for Sthan and does total 4-13 - so the discrepancy is one digit in
   one cell, and the obvious "fix" is obvious enough to be dangerous. **The page was rendered
   and inspected** (image `p0050`, printed p.50): the table is cleanly laid out, every column
   aligns, and `1-16` is what the book prints. It is therefore a defect of the book and not of
   the extraction, and the store's rule is to preserve those. **Not corrected.** Registered as
   `concept:mars-bala-pinda-row`.
2. **The Chandravela prose figure contradicts its own table** (`PD.04.Chandravela.Table`). The
   text says one part comes to 13-13-20; 13 degrees 20 minutes divided by 36 is 22 minutes
   13.33 seconds, and the table's own first row (0-22-13-20) gives exactly that. The prose is
   wrong, the table is right, both recorded as printed. Rows (15) and (19) also break the
   series and are preserved as printed.
3. **"Triped"** (`PD.04.Lagna.TripedSign`, v. 6). The verse partitions the signs three ways and
   names the first class *triped* - a category appearing **nowhere else in this book**. Ch. 1
   v. 7's body-form table classifies signs biped, quadruped, keeta and watery, and this
   chapter's own Bhava Dik Bala uses the same four. Confirmed as the printed word against the
   rendered page (image `p0044`, printed p.44). Whether it is a misprint for "biped" is
   **exactly the substitution a card must not make on its own**, so the card is the milestone's
   **single inert card** and is queued for human sign-off. `dep.triped-sign-class` exists
   because the book never gives the class.

**A digression that is not strength at all was encoded rather than dropped.** Between verses 11
and 21 the chapter carries a self-contained Chandra Kriya / Chandravela / Chandra Avastha
divination on the elapsed fraction of the birth nakshatra, yielding 108 numbered effects with
no connection to the balas on either side. Its printed divisors do not agree with its printed
part-counts (`concept:chandra-divisor-mismatch`), so it is not computable as printed; the three
effect lists are recorded as `reference` so nothing is lost, behind `dep.chandra-kriya`.

**The Kala Bala benefic/malefic lists were encoded without being promoted to nature doctrine.**
Milestone 20 had deliberately declined to encode the chapter's "for determining Kala Bala
Mercury should be treated as a benefic" as a `graha_nature` card. That sentence is now encoded
- as `PD.04.Ancients.KalaBala.BeneficList` / `.MaleficList`, with relation `kala_bala_benefic`
and an **explicit scope field** - which records the definition where it belongs without letting
it collide with ch. 2 v. 27's conditional Mercury or overwrite the Moon. The backlog entry stays
open because what is deferred is its *use*: the Kala Bala computation that would consume it
cannot be built, since the source withholds the arithmetic for three of the six components.

**Verification:** 33 of the 94 cards were **re-signed by hand** after the automated structural
pass, because their encoding involved a real judgement - an arithmetic check, a rendered page,
a scoping decision - and the automated "the quote is the fact itself" stamp would have been
false for them. Store-wide: 498/501 signed (99.4%), with three deliberate holdouts.

**Accounting cost, paid in the same milestone:** backlog 119 -> 137. 15 concept questions, 2
passage claims covering the chapter's apparatus, and 1 card entry (the inert `TripedSign`).
Seven new dependencies catalogued: `dep.day-night`, `dep.paksha`, `dep.declination`,
`dep.degree-range`, `dep.chandra-kriya`, `dep.weekday-hora-lords`, `dep.triped-sign-class`.
`chapter:phaladeepika.04` moved to **resolved**.

**Tests:** +20 (250 -> 270), in `Engine/tests/test_chapter_four_strength.py`. They pin the
things a later session could most easily undo: that the two authorities are never merged, that
the Mars row stays as printed, that the three withheld components stay unquantified, and that
the verses-4-and-5 verdict set is the only source Stage 4 may read for `strong`/`weak`.

**Why this milestone matters:** it is the first time the project encoded a chapter whose whole
subject is *computation*, and the finding is that the book does not actually supply the
computation it is famous for. The honest result was to encode what is there, record what is
withheld, and build the engine against the verdicts the text states outright rather than
against a Shadbala number no one in this chapter can produce. A session that had skimmed the
chapter for its tables would have built a Shadbala calculator on three components the source
refuses to define.

---

### Milestone 22 — Stage 4 built: `dep.strength` as a verdict extractor, closing P0-1

**Phase:** 2 (engine completion)
**Scope:** the engine half of P0-1 — one extractor, one doctrine accessor, one vocabulary
entry, four card conditions rewritten, four card dependencies corrected
**Status:** COMPLETE
**Completion:** 100% of what the source supports; see "What was deliberately not built"
**Commit:** this milestone's own commit (see `git log`)
**Remote:** VERIFIED

**What was built.** `Engine/facts.py::_strength`, the fourteenth fact extractor, and
`Engine/doctrine.py::graha_strength_verdicts`, the accessor that feeds it. The extractor
emits one new predicate, `strength(graha, strength)`, whose only values are the two words the
source itself uses — `strong` and `weak`. It carries no doctrine: every verdict it emits
names the card it read, and deleting those cards deletes the capability (a test asserts
exactly that).

**Exact source passages used.** Five reference cards, all from Phaladeepika chapter 4 verses
4 and 5, printed page 43-44:

| Card | Verse | What it states | Verdict |
|---|---|---|---|
| `PD.04.Strength.Exalted` | 5 | "All planets are strong when they are posited in their sign of exaltation." | strong |
| `PD.04.Strength.RetrogradeFive` | 5 | "The other five non-luminous planets are strong when they are retrograde." | strong |
| `PD.04.Strength.RetrogradeInDebilitation` | 4 | debilitated + retrograde + rays unaffected | strong |
| `PD.04.Weakness.Combust` | 4 | rays eclipsed → weak, **overriding** exaltation, own and friend's sign | weak |
| `PD.04.RahuKetu.StrongSigns` | 5 | Rahu in Cancer/Taurus/Aries/Aquarius/Scorpio; Ketu in Pisces/Virgo/Taurus | strong |

A sixth card carries the same `graha_strength` relation and is deliberately **not** read:
`PD.04.DikBala.Houses` quantifies one *component* of strength without reaching a verdict, and
a graha with full Dik Bala may be weak on every other count.

**What "strong" means here, and what it does not.** The chapter prints two criteria and they
are not equivalent. Verses 22-23 give Mantreswara's formal definition — Shadbala Pinda at or
above a per-graha threshold in Rupas — and that is **not computable from this book**: three of
the six components (Yudha, Chesta, Drig) have their arithmetic explicitly withheld by the
source. Verses 4-5 say "strong" and "weak" outright about conditions a chart settles, and
those are what the engine emits. **A graha this engine calls strong is one Phaladeepika calls
strong for a stated reason, not one whose Shadbala has been measured**, and every strength
fact carries that sentence in its own evidence block so a consultation cannot quietly imply
otherwise. Registered at `concept:strength-criterion-scope`, which stays open: what is owed is
a human's ratification, not a decision (§D).

**The one piece of ordering logic is the source's.** Verse 4 prints the combustion override in
the same sentence as the weakness — weak "even though he may be posited in his sign of
exaltation, in his own or a friend's sign" — so the card carries the override list and the
extractor applies what the card names. It applies nothing further, which is the whole of the
next finding.

**What building it found that reading it could not.** Chapter 4 was read card by card and
signed off in Milestone 21. This conflict is between two of those cards and appears only on a
chart that satisfies both: a graha that is **retrograde and combust** is called strong by
verse 5 (which conditions on retrogression alone) and weak by verse 4 (whose override list
names dignities, not retrogression). Verse 4's own retrograde clause points the other way,
requiring the rays to be unaffected, but reading that condition into verse 5 would be the
engine narrowing a verse the book states flatly. **So the extractor emits no verdict at all
for such a graha**, reports the collision by name, and lets every rule about its strength
correctly not fire. This is not a corner case — retrograde Mercury and Venus are often
combust, and it was observed on real charts during validation. Registered as
`concept:retrograde-combust-collision`, requiring `dep.adjudication`.

**Cards unblocked — four, all firing on real nativities:**

| Card | What now makes it expressible |
|---|---|
| `PD.02.Form.Mars.Youthful` | strength test added to *both* leaves, which the previous verification pass explicitly said whoever built `dep.strength` must do rather than merely dropping the dependency |
| `PD.10.WeakMoon5.Malefics` | all five clauses now conjoined — Moon in the 5th, Moon weak, malefics in the 1st, 7th and 12th. The weak Moon here is a combust Moon, which is the source's own worked example in v. 4 |
| `PD.10.Lord7.BeneficStrong` | the lord of the 7th bound by a variable and tested for *both* stated properties, benefic and strong |
| `PD.10.WifeChildren.EvenSigns` | all five clauses — 7th an even sign, its lord and Venus in even signs, lords of the 5th and 7th strong and not eclipsed |

Two of those four had conditions that could never have fired even once activated:
`lord_of_house(any, 7)` matches no fact, because `any` is a literal to the evaluator and not a
wildcard. Making a card active is not the same as making it fire, which is why each of the
four was confirmed against a real chart rather than against the schema.

**Cards still blocked — four, each with its declared dependency corrected.** This is the
milestone's least glamorous and most load-bearing work: every one of these named
`dep.strength` and would have been reported as *released* by the backlog the moment the
capability existed.

| Card | Why `dep.strength` does not release it | Now declares |
|---|---|---|
| `PD.10.WifeDirection.Strongest` | asks which of three is **strongest**; the doctrine gives a verdict, not an order | `dep.strength-ranking` |
| `PD.10.Marriage.StrongerDasha` | same superlative, plus varga/dasa/transit independently | `dep.strength-ranking` (+ the three) |
| `PD.06.Pushkala` | the strength clause is now expressible; "the house of an **Adhimitra**" and "**together** in a Kendra" are not | `dep.compound-friendship`, `dep.kendra-togetherness` |
| `PD.01.Kalapurusha.Strength` | condition still defective, and nothing in the store maps a house to a body part | `dep.body-part-significator`, `dep.manual-verification` |

**Engine changes.** `Engine/facts.py`: `VOCABULARY` gains `strength`; `_strength_condition_met`
reads a card's `when` block and **raises** on a key it does not recognise rather than skipping
it, because a silently-dropped clause would let a card fire on a weaker condition than it
states; `_strength` resolves per graha and registers in `EXTRACTORS`. Its inputs are the
existing `_dignity` and `_combustion` extractors' own output, recomputed rather than
re-derived, so no second copy of the dignity or combustion rules can drift into this function.
`Engine/doctrine.py`: `graha_strength_verdicts()`, which filters to cards that state a verdict
and returns each card's structure unflattened — three shapes are in the store (`when`, `when`
restricted by `grahas`, and a per-graha sign `table` for the nodes) and all three are the
source's.

**Source defects and restraint preserved.**
- **The Mars Bala Pinda row that does not sum** (1-16 + 0-30 + 0-40 + 1-7 + 0-20 = 3-53 against
  a printed 4-13) is untouched, and the protection is structural rather than arithmetic: the
  thresholds cards assert no verdict, so nothing in that table is reachable by the extractor
  at all. A test pins it.
- **No number ever reaches a fact.** Rupas, Shastyamsas and Pindas are all in the chapter and
  none of them may enter the engine; a test walks every strength fact's evidence and fails on
  a numeric value.
- **Retrogression does not make the nodes strong**, though they are retrograde on every chart
  ever cast, because verse 5 names five grahas and the nodes are not among them.
- **Ketu's unreachable clauses stay unasserted** — "the latter half of Sagittarius" and the
  Parivesha/Indrachapa condition (`concept:ketu-strength-clauses`).
- **No Bhava Bala.** House strength is stated in the chapter only as a formula over the same
  withheld components, and its Dik Bala half further needs a Bhava madhya that whole-sign
  houses do not have. Recorded as `concept:strength-is-not-bhava-strength` rather than left to
  be inferred from an absence.
- **The Kala Bala benefic list still does not leak into `dep.nature`**, as Milestones 20 and 21
  both took care to ensure.

**A bookkeeping correction the milestone forced.** Four chapter 4 questions
(`concept:yudha-bala-method-not-given`, `concept:chesta-bala-manda-definitions`,
`concept:bhava-bala-subtraction-scope`, `concept:mars-bala-pinda-row`) were declared against
`dep.strength` as a proxy for "matters once the strength engine exists". With the engine built
and deliberately not computing those components, that declaration made the backlog report all
four as newly unblocked — a false signal generated by the tooling working correctly on a wrong
input. They now declare `dep.shadbala-arithmetic`, a new catalogue entry naming what they are
really waiting for: a book that prints the three withheld methods. BPHS is the obvious
candidate and is not yet converted.

**Tests:** 302 (was 271). `Engine/tests/test_strength.py` is 30 of them, grouped as doctrine /
calculation / rule activation / source integrity. Edge cases the calendar does not supply — a
combust exalted Saturn, a retrograde debilitated Saturn — are tested by moving one body on a
real chart, so every other quantity stays what the ephemeris produced. Two existing tests were
rewritten in place: the chapter 4 suite's assertion that `dep.strength` was still outstanding
(it asserted the half-built state deliberately, so it could not be mistaken for a finished
one) became two assertions about the finished one, and `test_slice.py`'s Pushkala assertion
moved to the card's corrected dependencies.

**Real-chart validation.** 880 real birth instants were scanned to find a nativity exercising
each newly-activated card, and all four were found and confirmed firing — the first time this
project searched a chart space rather than spot-checking a single nativity. Two charts were
then compared before and after in full:
- **1986-06-10 21:15 Mumbai** (Mars retrograde in the lagna): 42 claims → 43. The gained claim
  is `PD.02.Form.Mars.Youthful`, triggered by `in_house(Mars,1)` and `strength(Mars,strong)`,
  whose fact cites `PD.04.Strength.RetrogradeFive`. **Nothing was lost.**
- **The demo nativity, 1987-03-14 Thanjavur** (the negative control): 41 claims → 41. It
  produces strength facts — Jupiter weak (combust), Ketu strong (Virgo) — and **no**
  strength-conditioned rule fires on it, because Mars is neither in the lagna nor its lord,
  the Moon is not in the 5th, and the lord of the 7th is not a strong benefic. Facts existing
  is not the same as rules firing, and this chart is the standing test of that distinction.
- **1985-03-29 02:15 Mumbai** (retrograde combust Mercury): the collision surfaces in the
  consultation's own "Doctrine read, but not complete" section, naming both cards.

**Production blockers cleared:** **P0-1**. There is now **no open P0**.

**What was deliberately not built**, each because the source forbids it: a Shadbala Pinda, a
Bhava Bala, any numeric strength score, any ordinal comparison of one graha against another,
and any strength verdict from a verse that does not say "strong" or "weak" outright.

**Why this milestone matters.** It is the first time the project built an engine capability
whose *scope was set by what the source withholds* rather than by what the capability
conventionally means. Every general-purpose Vedic engine has a Shadbala calculator; this one
does not, because the book it reads does not supply one, and pretending otherwise would have
produced authoritative-looking numbers that no quote supports. The milestone also demonstrates
something the verification workflow could not: that a chapter can be read card by card,
signed off, and still contain a conflict that only a chart reveals.

---

### Milestone 23 — Stage 7's reading half: the store's own relationships, finally read

**Phase:** 4 (knowledge integration)
**Scope:** one new module, one structured channel on the doctrine report, one build gate, one
consultation section, and a correction to Part 3 — no rule card touched
**Status:** COMPLETE
**Completion:** 100% of what the corpus supports; see "What was deliberately not built"
**Commit:** this milestone's own commit (see `git log`)
**Remote:** VERIFIED

**The finding that set the scope.** Before writing any code, the store was inventoried for
real conflicts. `contradicts` appears on 12 cards, `extends` on 2, `parallel_of` on 27 — and
`grep` over `Engine/` found **no code anywhere that reads any of them**. They had been written
faithfully by every encoding pass since chapter 1 and were inert. So the smallest useful
adjudicator was not a weighting scheme; it was a reader.

**The live defect that proves it.** On a chart with an exalted graha, two cards fire on the
same fact: `PD.09.Dignity.Exalted` (ch. 9 v. 14 — the native "will shine like king
Vikramaditya") and `PD.09.Dignity.Exalted.Notes` (the translator's own dissent on the same
page — the native "cannot shine like king Vikramaditya"). The store links them with
`contradicts`. Part 2 printed them as two unrelated paragraphs. Worse, Part 3's lexical pass
saw "ruler", "shine" and "vikramaditya" un-negated in both — *"cannot"* is not one of its
negation cues — and printed:

> **“vikramaditya”** — asserted in 2 passages: `clm-0023`, `clm-0024`

under a heading reading **“Terms that recur without contradiction.”** The system was reporting
a verse and its own printed refutation as agreeing. Measured over 720 nativities, this
happened on **598 of them — 83%**. The cue list was never the real problem, and lengthening it
would not have been the real fix: the contradiction was declared in the store all along and
nothing read it.

**Conflicts inventoried, and what each turned out to be.** Every linked pair was classified
against the source, and the classification decided the build:

| Conflict | Source(s) | Represented as | Does the source resolve it? | What Stage 7 does |
|---|---|---|---|---|
| `PD.09.Dignity.Exalted` vs `.Notes` | PD ch. 9 v. 14 and its own Notes | `contradicts`, and the Notes card carries `polarity: qualified` | **No.** The Notes narrows rather than denies — the effect holds if the graha is in an auspicious house, free of malefic influence and "supported by other helpful planetary combinations" | **qualification / unresolved.** Both stand, and the reason states that the qualifying condition is not encoded, so the engine cannot test it |
| `concept:retrograde-combust-collision` | PD ch. 4 v. 5 against v. 4 | not a card link at all — only a chart produces it | **No.** v. 4's own override list names dignities, not retrogression | **contradiction / unresolved**, promoted from a prose aside into a relationship with both verses quoted; still no verdict emitted |
| Combustion override | PD ch. 4 v. 4 | `predicts.overrides` on the weak card | **Yes** — in the same sentence as the weakness | **override / applied**, naming the sentence that authorises it. Fires on 11% of charts |
| `PD.06.Dainya` vs `PD.06.VipareetaRajaYoga.Uttarakalamrita` | PD ch. 6 vv. 32-33 vs Uttarakalamrita khand 4 sloka 22, via the translator | `contradicts`; the Uttarakalamrita side is a reference card | **No**, and it cannot be evaluated either: its clauses 4 and 5 are not resolvable into the condition language, which the card's note already said | **contradiction / recorded.** Fires on 18% of charts, and is the first time a reader learns another authority calls this configuration a *Raja* yoga |
| Pancha Mahapurusha, Vesi/Vasi families | Jataka Parijata, Saravali, unnamed "authoritative works", via the translator | `parallel_of` to cards naming an authority | n/a — they are not in conflict | **parallel_authority / recorded**, on 92% of charts |
| Rising-sign, Rasi Sandhi, nodal exaltation (3-way), Sun's karaka, kendra positional strength | PD ch. 1, 2, 4 | `contradicts` between **reference** cards | Not applicable to a nativity | **Nothing.** No side is ever a claim, so reporting them on every chart would pad the report with doctrine the reading never touched |

**Two findings that removed work rather than adding it.**
- **Cancellation needs no mechanism.** The obvious case, Sakata Yoga (ch. 6 v. 17), prints the
  yoga and its cancellation in one sentence — "cancelled if the Moon be in a Kendra position
  from the Ascendant" — so the encoder made the cancelling clause a negated conjunct *inside
  the card's own condition*, and the card has simply not fired for a kendra Moon since
  Milestone 9. There is no second claim to cancel. Every "unless" in the store
  (`PD.10.Benefics.In7`) is the same shape. A cross-card cancellation framework built for this
  would have been architecture for a problem the encoding had already solved — so none was
  built.
- **Exactly one claim-to-claim contradiction exists in the whole corpus.** Every other
  `contradicts` link has at least one side that never becomes a claim. Verified across 720
  charts and pinned by a test. This is the concrete reason no machinery for *weighing rival
  predictions* was built: there is one pair that could ever need it, and the source does not
  settle that pair either.

**The one judgement the data would not settle, registered rather than decided.**
`parallel_of` is overloaded. It links a card to another named authority's statement of the
same doctrine, **and** it links sibling cards cut from a single sentence
(`PD.06.Varishtha`/`.Sama`/`.Adhama` are three mutually exclusive readings of one verse; so are
Lakshmi/Gouri, Subhamala/Asubhamala, Mahabhagya.Male/.Female, Amala/Amala.V12). Reporting the
second kind as a second authority would manufacture corroboration out of the project's own
filing. `predicts.authority` separates the two groups cleanly and is what the engine keys on.
But even in the first group the link does not record *agreement*:
`PD.06.Vesi.AuthoritativeWorks` reports that most authoritative works define the yoga
**without** the benefic/malefic split this book uses — a different condition for the same yoga
— while `PD.06.PanchaMahapurusha.JatakaParijata` restates the same one. So Stage 7 reports
"a second authority on the same doctrine" and **deliberately does not report corroboration**.
Registered as `concept:parallel-of-overloaded`; resolving it is an encoding decision, not an
engine one.

**What was built.**
- `Engine/adjudicate.py` — `Adjudication` (subject, relationship, resolution, reason, parties,
  basis, declared_as) and `Party` (card, book, chapter, verse, page anchor, authority,
  statement, activation, claim ids). **There is deliberately no field in which a number could
  be recorded.** Four relationships (`contradiction`, `qualification`, `parallel_authority`,
  `override`) and three resolutions (`applied`, `unresolved`, `recorded`), both closed
  vocabularies enforced by Stage 9.
- Links are read **undirected**. Six links in the store are declared from one end only —
  including this milestone's flagship, which only the Notes card declares — and which end
  carries the declaration is an accident of encoding order.
- `DoctrineReport.conflict()`, a structured channel beside `incomplete()`, so the strength
  extractor's chart-dependent collision reaches Stage 7 as data rather than as a sentence to
  be parsed. The two coexist because they say different things: `incomplete` is a coverage
  statement ("this graha got no fact"), the conflict is a relationship ("these two verses
  disagree here"), and only the second can carry the verses.
- A consultation section, **“How the applicable passages stand to one another,”** opening
  Part 3.
- `verify_cards` now fails the build on a relationship link naming a card that does not exist.
  These fields were inert clutter until this milestone; a typo in one now silently costs a
  reported contradiction.
- `synthesise()` takes the claim pairs Stage 7 found in a source-stated disagreement, so a
  theme spanning such a pair is contested **by doctrine** and says so. Synthesis still measures
  no astrology of its own: what enters is a citation the encoder wrote off the printed page.

**`unresolved` is a finished answer.** Where the corpus states no precedence, both statements
stand, the reason says why no choice was made, and that is the output — not a placeholder for
a decision the engine is waiting on.

**Tests:** 334 (was 302). `Engine/tests/test_adjudication.py` is 32 of them. **Four deliberate
mutations of the module were run against the suite** to confirm the tests can fail: reading
links directionally (caught), resolving an unresolved dispute (caught, 5 tests), deleting the
strength collision's refusal (caught, 6 tests), and treating every `parallel_of` as a second
authority — which was **not** caught on the first attempt, because the test checked the
discriminator's *input* (do sibling cards name an authority?) rather than its *output* (does
the adjudicator ever emit one without a named authority?). Two behavioural tests replaced it
and the mutation is now caught.

**Real-chart validation.** 720 nativities, four cities, 1950-2010, **zero pipeline or
verification failures**. Every relationship type and every resolution occurred. Frequencies
were measured, not asserted: `parallel_authority`/`recorded` on 92.2% of charts,
`qualification`/`unresolved` on 83.1%, `contradiction`/`recorded` on 18.1%,
`contradiction`/`unresolved` on 12.4%, `override`/`applied` on 11.1%.

**Nothing was gained or lost in Part 2.** On both the demo nativity (41 claims) and the
exaltation chart (46 claims), Part 2 is **byte-identical** before and after. A test asserts
that running the adjudicator leaves the claim list unchanged, because raw source claims stay
authoritative and adjudication is a layer above them.

**What was deliberately not built**, each because the corpus does not support it: any
weighting, confidence, source-prestige or ranking of one authority against another; any
precedence not stated by a source in its own sentence; a cross-card cancellation mechanism (no
case needs one); corroboration of yogas (the link cannot distinguish agreement from a variant
reading); and any relationship type outside the four the store actually exhibits.

**Production blockers cleared:** none, and **`dep.adjudication` was deliberately left
outstanding**. Eleven registry entries declare it and this milestone releases none of them.

**Why this milestone matters.** Milestone 22's lesson was that a chapter can be read card by
card, signed off, and still hide a conflict only a chart reveals. This one is the mirror
image: a relationship can be read correctly, recorded correctly, and carried in the store for
twenty-two milestones while the system's own output contradicts it. Card-level verification
could not have caught it and neither could running a consultation and reading Part 2 — the
error was in Part 3, in a heading that said "without contradiction" over a contradiction the
project itself had documented.

---

### Milestone 24 — Chapter 6's blanket strength condition, and the second Duryoga

**Phase:** 3 (knowledge), using capability built in Phase 2 (Milestone 22)
**Scope:** one new reference card, two new predictive cards, five existing cards' conditions
extended, one deferred.json entry resolved and split, one new dependency registered
**Status:** COMPLETE
**Completion:** 100% of what the source's testable clauses support; see "What was deliberately
not built"
**Commit:** this milestone's own commit (see `git log`)
**Remote:** VERIFIED

**Source-first reconnaissance, not the backlog's paraphrase.** `Rules/deferred.json`'s existing
entry for `passage:phaladeepika.06.p009` read "the blanket condition that every yoga in the
chapter needs strength in the Lagna/Moon and the yoga-forming planets" — read against
`Knowledge/phaladeepika.md` directly (paragraph 9, printed p.55) rather than trusted, two things
in that paraphrase turned out to be imprecise:

1. **"Lagna/Moon" is a disjunction, not a conjunction.** The verse's own words: *"...only when
   the Lagna **or** the Moon and the Yoga forming planets are without blemish."* The true parse
   is `(Lagna-strong OR Moon-strong) AND (yoga-forming-planets without blemish)`.
2. **The scope is textually anchored to the five Pancha Mahapurusha Yogas, not the whole
   chapter.** The sentence sits inside that section — immediately after the Jataka Parijata and
   Saravali corroboration quotes for those five yogas, and immediately before "As the names of
   Yogas denote the persons with such Yogas at birth become Mahapurushas..." and the translator's
   introduction to worked examples of those same five yogas. "Every yoga in the chapter" was the
   original encoder's own generalisation from Milestone 7, not something this sentence states.
   Consistent with that: of chapter 6's 60 cards (before this milestone), only the five
   Mahapurusha cards ever cross-referenced `passage:phaladeepika.06.p009` in their own notes; no
   other card did. The engine did not touch any other chapter-6 card.

The verse's own "without blemish" gloss bundles four sub-conditions: *"vested with strength and
are not associated with or in conjunction with malefics, are not combust and not placed between
malefics."* Only two of the four are encodable today:

- **Vested with strength** → the existing `strength(graha,"strong")` predicate (`dep.strength`,
  Milestone 22), reused exactly as built, with no new engine code.
- **Not conjunct a malefic** → a correlated negation over the existing `conjunct`/`nature`
  predicates (`{"not": {"all": [{"conjunct":...},{"nature":...,"malefic"}]}}`), a shape the
  engine's `_solve` already supports generically (`Engine/rules.py`'s own docstring names exactly
  this pattern) but which no card in the store had previously exercised. Verified with a
  dedicated construction before use in a production card, not assumed from the docstring.
- **Not combust** is already subsumed: `PD.04.Weakness.Combust` forces a `weak` verdict on any
  combust graha, so a card testing `strength(g,"strong")` already excludes combustion.
- **Not hemmed between malefics (papakartari)** and **the Lagna-or-Moon disjunction** remain
  unencoded — the first needs `dep.hemmed-between` (already registered, still unimplemented, and
  blocked on the rest of chapter 6 per its own entry); the second needs a Lagna-specific strength
  verdict that exists nowhere in this engine or this store's doctrine (see below).

**Inspecting `dep.strength` before extending it, per the resume brief's own instruction.**
`Engine/facts.py::_strength` iterates only `chart.bodies.values()` — the nine grahas
(`Engine/ephemeris/provider.py::BODIES`). The Lagna is a scalar (`ChartBundle.ascendant_sign`),
never a member of that set, exposed only through the sign-only `lagna_sign(sign)` predicate. A
card literal `strength(Lagna,"strong")` would load and pass `verify.py` (which never validates
that a `graha` argument names a real body) but would **permanently and silently never match any
fact** — indistinguishable from an ordinary unmet condition, the exact failure mode the resume
brief's §4 asked to be checked for before extending the mechanism. This is not solely an engine
gap: ch.4 vv.4-5, the only source `dep.strength` reads, state strong/weak verdicts about grahas
only; no encoded passage states a Lagna-specific verdict even if the plumbing existed. Building
it would be new engine code on top of doctrine that does not exist — exactly the "do not build
speculative architecture" case §I already forbids. So the Lagna-or-Moon clause was left off every
card's conditions rather than encoded as a disjunction with one arm permanently, silently dead;
registered instead as `dep.lagna-strength` (new, `implemented: false`) and
`concept:p009-lagna-or-moon-clause` (new, deferred).

**A real, evidenced consequence — not silently smoothed over.** The five Mahapurusha cards are
encoded as *own-sign-or-exaltation dignity* + *kendra placement*, Mantreswara's own naming
condition (v.1). Ch.4 vv.4-5's five verdict cards do **not** independently state "own sign ⇒
strong" — only exaltation, retrogression (of the five non-luminous grahas), retrograde-in-
debilitation, and the nodes' own signs produce a `strong` verdict. So adding
`strength(graha,"strong")` as an *additional* required clause narrows these cards: a graha in its
own sign, not exalted, not retrograde, now carries no strength verdict at all and the card
correctly withholds the claim. This is not hypothetical — it is the project's own golden/demo
chart (1987-03-14, Thanjavur): Mars sits in Aries, its own sign, in the 4th (a kendra), and
`PD.06.Ruchaka` has fired on this exact chart since Milestone 7. It no longer does. Confirmed as
the source's own additional requirement, not an artefact of the encoding: the five cards' own
notes, written in Milestone 7 before `dep.strength` existed, already anticipated this — *"this
card fires on placement alone, which is not the whole of what the chapter says."* The dignity and
kendra clauses were **added to, never removed**; the yoga's own naming condition is untouched.
Measured across 2,176 real nativities (four cities, 1950–2010): the Mahapurusha family now fires
on 29.2% of charts, still a substantial fraction — this is a narrowing, not a near-elimination.

**`passage:phaladeepika.06.p233` — the second Duryoga (v.70, printed p.82).** *"If the lords of
the 6th, 8th and 12th houses vested with strength are posited in Kendra or Trikona and the lords
of 1st, 10th, 4th and 9th houses be weak or combust, and occupy the 6th, 8th and 12th houses, the
yoga so arising is named Duryoga. If, however, the above dispositions are in the reverse order...
the native will become a king, fortunate, wealthy, happy and virtuous."* Distinct from the
10th-house "Duryoga" inside the still-unencoded vv.57-69 dusthana-lord cluster
(`passage:phaladeepika.06.p202`) — the source names both "Duryoga" and they are unrelated
conditions. Encoded as two new cards, `PD.06.Duryoga` (the named configuration) and
`PD.06.Duryoga.Reverse` (the verse's own unnamed reverse configuration, which the card id and
`predicts.yoga` record honestly rather than inventing a Sanskrit name the source does not give).
"Weak or combust" is tested as `strength(g,"weak") OR combust(g)` directly — not routed through
the strength verdict alone — because the verse names combustion as an independent alternative;
this also means the ch.4 retrograde-combust collision cannot silently block this test the way it
blocks a bare `strength(g,"weak")` leaf. The chapter's closing colophon (paragraph 234, on the
same printed page) is narrative, not doctrine, and was split into its own entry,
`passage:phaladeepika.06.colophon`, matching `passage:phaladeepika.04.colophon`'s treatment,
rather than left bundled with v.70 under `dep.strength`.

**The finding that took the most work to confirm: `PD.06.Duryoga` cannot be shown firing on any
chart.** Both cards use the identical seven-role machinery (three house-lords needing
strong+kendra/trikona, four needing weak-or-combust+dusthana) with the two roles swapped. Only
`PD.06.Duryoga.Reverse` could be constructed firing — deliberately constructed, not scanned,
because the joint probability of seven independent strength/house-class facts is far below what
even a several-thousand-chart scan would find (confirmed: zero natural occurrences of either card
across the 2,176-chart validation sweep). Working out why `PD.06.Duryoga` specifically resisted
construction, by exhaustively checking all twelve whole-sign lagnas, is itself a finding: eight of
the twelve force two of the seven lord-roles onto the same graha (impossible — one graha carries
one strength verdict at a time), and the remaining four collision-free lagnas each bind the Sun
to one of the seven roles. The Sun's only route to a `strong` verdict in this store is exaltation
(Aries; ch.4 v.5 names no other route for a luminary, and the Sun can never be `weak` either —
`Engine/facts.py::_combustion` excludes it by construction, "the doctrine is stated as distance
*from* the Sun"), and Aries does not land in a kendra or trikona house for any of those four
lagnas under the *named* configuration's own role assignment. It does for two of them (Leo,
Sagittarius) under the *reverse* configuration's swapped assignment — which is exactly why the
reverse card, and only the reverse card, could be built. `PD.06.Duryoga` is left **active**, not
marked `inert`: no predicate is missing and no capability is absent — every clause is exactly as
expressible as its mirror's — so this is not the "card ahead of the engine" category `inert`
exists for. It is the other category Milestone 22 named directly: *"a card can be made active,
pass every structural check, and still never fire on any chart because its condition is
unsatisfiable."* Recorded in the card's own `note` and pinned by
`test_duryoga_named_cannot_fire_given_the_suns_single_strong_path`.

**Adjudication interaction, checked per the resume brief's §7, not assumed.** A Mahapurusha
graha that is both retrograde and combust hits `concept:retrograde-combust-collision` exactly as
any other strength-conditioned card does: `_strength` emits no verdict, the card silently does
not fire, and `Engine/adjudicate.py` — untouched this milestone — still and separately reports
the collision as an unresolved `contradiction`. Confirmed by construction (Mars exalted and in
the lagna, then made retrograde and combust): `PD.06.Ruchaka` does not fire, and the adjudication
`contradiction`/`unresolved` for "the strength of Mars" still appears, unaffected by whether any
downstream card tried to use the fact. No new engine code was needed or written for this.

**Engine changes:** none. Every clause uses predicates that already existed
(`strength`, `conjunct`, `nature`, `combust`, `lord_of_house`, `in_house_class`) in combinators
the engine already generically supports. This was verified, not assumed, for the one genuinely
novel combination (`{"not": {"all": [...]}}` with a fresh existential variable inside the
negation) before it was used in a production card.

**Tests:** 341 (was 334). Two in `Engine/tests/test_slice.py` (the golden chart's Ruchaka claim
now withheld; a constructed positive control — Mars moved to its exaltation sign — showing it
returns), a new fixture in `Engine/tests/test_adjudication.py` (a real chart, found by scanning,
where `PD.06.Sasa` still exercises the `parallel_of` corroboration link the demo chart no longer
does), and six in the new `Engine/tests/test_chapter_six_strength.py`: scope (only the five
Mahapurusha cards carry the new clauses, confirmed against a sample of untouched chapter-6 cards;
an unrelated graha's strength cannot affect Ruchaka), the reference card never becomes a claim,
the retrograde-combust collision reproduced for a Mahapurusha card specifically, `PD.06.Duryoga.
Reverse` firing on the constructed chart with its full seven-variable binding checked, and
`PD.06.Duryoga`'s structural unfireability confirmed by comparing its condition tree's
strong/weak role assignment against its mirror's.

**Real-chart validation.** 2,176 real nativities (four cities, 1950–2010, sparse stride), **zero
pipeline or verification failures**. The Mahapurusha family fires on 29.2% of charts (was higher
before this milestone on an unrestricted-by-strength basis, though that count was never itself
pinned by a test to compare against directly — the golden chart's own concrete before/after,
41 claims → 40, is the pinned comparison). `PD.06.Duryoga` and `PD.06.Duryoga.Reverse` each fired
on **zero** of the 2,176 charts, consistent with the construction finding above. The
retrograde-combust collision was reported on 13.6% of charts, continuing to behave exactly as
Milestone 22/23 left it.

**Production blockers cleared:** none. This was ordinary Phase 3 encoding using an
already-cleared P0's capability; no blocker was open going in.

**What was deliberately not built**, each because the source or the engine's own honest limits
forbid it: a Lagna-specific strength verdict (no source states one; registered as
`dep.lagna-strength` rather than guessed at); the papakartari/hemmed-between clause (needs
`dep.hemmed-between`, already registered, blocked on the rest of chapter 6); any attempt to force
`PD.06.Duryoga` to fire by loosening its condition beyond what the verse states (its
unfireability is the source's own doctrine meeting this engine's own honest strength model, not
an encoding defect to paper over); and any extension of the strength/malefic-conjunction clauses
to chapter-6 cards the verse's own text does not reach.

**Why this milestone matters.** It is the first time `dep.strength` (Milestone 22) was used to
*gate encoding* rather than to complete an engine stage, and the first time this project's own
"is this card active or does it actually fire" discipline (Milestone 22's own words) produced a
documented, permanent answer — "it structurally cannot" — for a card that is neither buggy nor
missing a capability. Both findings (the golden chart's narrowed Ruchaka, `PD.06.Duryoga`'s
unfireability) came from the same discipline: read the source exactly, extend an existing
mechanism instead of inventing one, and then actually run a chart rather than trust that a
well-formed condition is a firing one.

---

---

## D. CURRENT MILESTONE

**Nothing is currently in progress.** Milestone 24 above is fully committed, tested, verified,
and pushed.

**Five decisions are owed by a human.** None blocks the next milestone; each should be
settled before the work it touches is extended.

### Decision 0b (new, Milestone 24) — `concept:p009-lagna-or-moon-clause`

**What v.9's disjunctive clause requires, and why only half of it is encoded.** The verse:
*"...only when the Lagna **or** the Moon and the Yoga forming planets are without blemish."*
Milestone 24 encoded the yoga-forming-planets half onto the five Mahapurusha cards. The
Lagna-or-Moon half is not encoded at all — not narrowed, not approximated, simply absent from
every card's conditions.

**Why it was left off rather than partially encoded.** The Moon side is trivially testable (the
Moon is one of the nine grahas `dep.strength` already covers). The Lagna side needs two things
this engine and this store's doctrine do not have: `ChartBundle` never treats the Lagna as a
strength-bearing subject (it is a scalar, `ascendant_sign`, never a member of `chart.bodies`), and
no encoded passage states a Lagna-specific strong/weak verdict even if the plumbing existed.
Writing `strength(Moon,"strong") OR strength(Lagna,"strong")` into a card today would be honest
but permanently half-dead — the Lagna arm could never match a fact, forever, until both gaps
close — so it was left off entirely rather than encoded as a disjunction whose second arm silently
does nothing.

**What closing it would take, if a human decides it should be closed:**
1. **New doctrine.** No encoded chapter states a Lagna strong/weak verdict. The nearest classical
   candidate is Bhava Bala (house strength), which chapter 4 states only as a formula over
   components this book withholds the arithmetic for (`concept:strength-is-not-bhava-strength`) —
   so even converting a new book would need one that states a Lagna verdict *outright*, the way
   ch.4 vv.4-5 state graha verdicts outright, not one that only supplies more withheld arithmetic.
2. **New engine plumbing.** A Lagna-shaped strength extractor, whatever doctrine it reads.
   Registered as `dep.lagna-strength` (`implemented: false`, effort costed as a guess until the
   source is identified).

**Recommendation: leave it closed for now.** Nothing is wrong in any consultation the five cards
produce today — they assert exactly what their conditions test, no more. This is not a
precedent-setting editorial call the way Decisions 1-2 below are; it is a straightforward
"no source, no capability" gap. It is listed as a decision anyway because a future session should
not silently start encoding a Lagna-strength guess without first finding the source that would
justify it.

### Decision 0a (Milestone 23) — `concept:parallel-of-overloaded`

**What a `parallel_of` link means.** It is currently used for two different things, and the
engine can tell them apart only by whether the linked card names an authority:

1. **Another authority's statement of the same doctrine** — `PD.06.PanchaMahapurusha.JatakaParijata`,
   `.Saravali`, `PD.06.Vesi.AuthoritativeWorks`, `PD.06.VesiVasi.Saravali`. These carry
   `predicts.authority`.
2. **Sibling cards cut from one sentence** — `PD.06.Varishtha`/`.Sama`/`.Adhama` (three
   mutually exclusive readings of one verse), Lakshmi/Gouri, Subhamala/Asubhamala,
   Mahabhagya.Male/.Female, Amala/Amala.V12. These carry no authority, and
   `PD.06.Amala.V12`'s own note already states the principle: a restatement by the same author
   must not be counted as a second corroborating card.

**Why it matters.** Even within group 1 the link does not say whether the other authority
*agrees*. `PD.06.PanchaMahapurusha.JatakaParijata` restates the same condition;
`PD.06.Vesi.AuthoritativeWorks` states a **different** one — the yoga without the
benefic/malefic split. Stage 7 therefore reports "a second authority on the same doctrine" for
both and claims corroboration for neither, which is honest but weaker than what the corpus
could support.

**Three defensible positions:**
1. **Split the link at encoding time** into an agreement link and a variant-reading link, and
   backfill the 27 existing cards. Lets cross-book corroboration be reported for yogas the way
   it already is for `graha_nature`, and would move the multi-book score materially. Costs a
   re-reading pass over chapter 6's notes.
2. **Add a field rather than a link type** — e.g. `predicts.agrees: true|false|unstated` on the
   authority-naming card. Cheaper, and `unstated` is an honest third value where the translator
   reports another book without comparing it.
3. **Leave it** — what Stage 7 does today. Nothing is wrong in any consultation; the reader
   sees both statements and compares them. Sustainable indefinitely, but it means the project
   never reports yoga corroboration.

**Recommendation: (2).** It matches how the store already records nuance (`polarity`,
`overrides`, `conditional`) and its `unstated` value is the one the corpus most often warrants.
But it decides what this project will treat as cross-book agreement, which is a
precedent-setting call and explicitly a human's.

### Decision 0 (Milestone 22, now surfaced) — `concept:retrograde-combust-collision`

**What a graha that is both retrograde and combust is.** Verse 5 calls it strong (the five
non-luminous planets are strong when retrograde, no further condition); verse 4 calls it weak
(rays eclipsed), and verse 4's override list names dignities — exaltation, own sign, friend's
sign — not retrogression, so the source does not settle it. The engine currently **emits no
verdict** for such a graha and reports the collision, which is the correct behaviour in the
absence of Stage 7 adjudication and is not a placeholder for a decision it is waiting on.

Two readings are defensible and both are the human's to pick, not the engine's:
1. **Verse 4 governs.** Its own retrograde clause conditions the rescue on the rays being
   unaffected, which suggests Mantreswara means combustion to defeat retrogression throughout.
   Reads the chapter as internally consistent — but narrows a verse the book states flatly.
2. **Hold it unasserted** — what the engine does today. Nothing is wrong in any consultation,
   the question stays visible, and retrograde-combust grahas simply get no strength claim.

**Recommendation: (2), unchanged.** **MILESTONE 23 UPDATE.** Stage 7 now exists and does not
change this answer — it changes only how visible the question is. The collision used to appear
as one sentence in the consultation's coverage list; it is now reported as a contradiction with
both verses quoted, both pages cited, and an explicit statement that the source does not settle
it, on the 12% of charts that produce one. **Stage 7 will never resolve this**: the engine can
only apply a precedence a source states, and neither verse states one. What is owed is a
human's ruling, not a capability, and the entry's `requires: dep.adjudication` is retained
because a *general* precedence rule — should it ever be supplied by a source — is where the
answer would come from.

### Decision 1 (Milestone 21, now live) — `concept:strength-criterion-scope`

Chapter 4 states two different criteria for "strong" and the engine can only implement one of
them. **The choice has already been made and encoded** — what is owed is a human's ratification
of it, because it determines what the word "strong" means in every consultation the project
will ever emit.

- **Verses 22-23** give Mantreswara's formal definition: strong = Shadbala Pinda at or above a
  per-graha threshold in Rupas (Sun 6.5, Moon 6, Mars 5, Mercury 7, Jupiter 8.5, Venus 5.5,
  Saturn 5). **Not computable**, and not made computable by anything in this chapter: the
  components are quantified only in the other authorities' scheme, and three of those (Yudha,
  Chesta, Drig) have their arithmetic **explicitly withheld by the source**.
- **Verses 4 and 5** state "strong" and "weak" outright about conditions the engine already
  evaluates. **Computable today.**

**What was encoded:** the verdicts, from vv. 4-5. **What a consultation must therefore never
say:** that a graha's Shadbala has been measured. The gap between the two criteria is real and
they are not equivalent — a graha this engine calls strong is one Phaladeepika calls strong for
a stated reason. If a human decides that is too weak a sense of the word, the alternative is
not a better calculator; it is emitting no strength verdicts at all until a source that
supplies the missing arithmetic is encoded.

**MILESTONE 22 UPDATE — this decision is now live, not latent.** When it was written, no chart
produced a strength fact and the question was about what a future engine would mean. That
engine exists, is emitting verdicts, and four rule cards are firing on them. The wording it
governs is now in real consultations. Two things were done to keep it honest in the meantime:
every strength fact carries the criterion in its own evidence block (*"the verdict verses 4-5
state outright, not a Shadbala Pinda; the chapter withholds the arithmetic for three of the
six components"*), and a test walks every strength fact and fails if any numeric value ever
reaches one. The missing arithmetic now has a dependency of its own,
`dep.shadbala-arithmetic`, so "encode a source that supplies it" is a tracked item rather than
a sentence in this file.

### Decision 2 (carried from Milestone 20, unchanged) — `concept:moon-nature-criterion`

Milestone 20 deliberately left one question open rather than answering it, and it should be
settled before any further `graha_nature` doctrine is encoded, because the answer sets the
precedent for every translator's gloss in the corpus.

**The question:** what makes the Moon malefic, and do the two books actually disagree?
- Brihat Jataka's English prints "the Moon (within less than 72 degrees distance from Sun)".
- The Devanagari it translates (ch. 2 v. 5, checked against the printed page) says only
  **क्षीण** — diminished/waned — and carries **no numeral**.
- Phaladeepika's translator renders the same underlying criterion as "the waning Moon".
- Operationally the two English renderings disagree on many charts: a Moon 60° from the Sun is
  waxing (benefic to Phaladeepika) but within 72° (malefic to Brihat Jataka's gloss).

**Three defensible positions:**
1. **Gloss is doctrine.** Encode the 72° figure as Brihat Jataka's criterion. Honest to what
   this edition prints, but it manufactures a cross-book contradiction from two renderings of
   one word, and it would require Stage 7 conflict adjudication (P1-3) to be built before the
   Moon can be classified at all.
2. **Gloss is apparatus; read the Sanskrit.** Treat क्षीण as the criterion both books state, as
   Phaladeepika's translator does. Doctrinally the most defensible, and it makes the books
   agree completely — but it substitutes one book's wording for what this page prints, and it
   commits the project to reading Sanskrit behind English wherever the two diverge.
3. **Hold it unasserted** — what Milestone 20 did. Phaladeepika governs the Moon unopposed,
   nothing is overwritten, no consultation is wrong today, and the question stays visible.
   Sustainable indefinitely, but it is a deferral, not an answer.

**Recommendation: (2), with the gloss preserved in the card's note as apparatus.** It matches
the project's existing treatment of translator's material (Milestone 11), and Milestone 20's
source work already established the factual basis for it. But it is a precedent-setting
editorial call about how this project reads its translations, and it is explicitly a human's to
make — which is why it was not taken unilaterally.

### Next milestone — a choice, not a critical path

**With P0-1 closed there is no open P0.** Nothing is gating production that a single capability
would clear, and the next milestone is therefore a judgement about return rather than an
obligation. `leverage.py` now ranks `dep.triped-sign-class` first (cost 1, +1 card) and that is
a human's reading (whether "Triped" is a misprint for "biped") rather than an implementation, so
the ranked list does not settle it either.

**Recommended: `passage:phaladeepika.06.p202` — vv.57-69, the twelve dusthana-lord yogas.**
Continues chapter 6 in its natural reading order (v.9 and v.70 are now both consumed; the
chapter's remaining unencoded material is vv.39-41, vv.42-43 and this passage). Explicitly
flagged since Milestone 8 as "the richest single contradiction in the chapter" — Mantreswara
calls Harsha/Sarala/Vimala auspicious, Parashara's own nivritti verse calls them the opposite —
which makes it the natural next exercise for Stage 7 adjudication's reading half (Milestone 23):
it would give the store a **second** genuine claim-to-claim contradiction, where today there is
exactly one (`PD.09.Dignity.Exalted` vs. its own Notes). Ready now — `dep.none` — no capability
is missing.

**Three alternatives, each defensible:**

1. **`passage:phaladeepika.06.p175`** (vv.42-43, Adhiyoga) or **`passage:phaladeepika.06.p168`**
   (vv.39-41, the seven-planets-in-N-signs family — needs one small new engine fact, a
   distinct-sign-count over the seven classical grahas). Either continues chapter 6 without
   p202's adjudication angle.
2. **`dep.compound-friendship`** (cost 3). The Adhimitra/Adhishatru tiers, which the book
   defines in ch. 2 and then uses without definition in ch. 6 v. 19, ch. 10 v. 23 and six
   rows of the ch. 4 survey. Cheap, well-sourced, and releases `PD.06.Pushkala`'s first
   remaining obstacle.
3. **`concept:parallel-of-overloaded`** (Decision 0a) — an encoding pass over chapter 6's notes
   that would let cross-book corroboration be reported for yogas the way it already is for
   `graha_nature`. Precedent-setting (see Decision 0a's own text), so best taken only after a
   human has read that decision.

**Four things the next milestone must NOT do**, each of which the source still forbids:

- **Do not compute a Shadbala Pinda.** Three of six components have no printed arithmetic.
  This did not change by building Stage 4; it is why Stage 4 is shaped the way it is. See
  `dep.shadbala-arithmetic`.
- **Do not implement Bhava Bala numerically**, and do not add a `bhava_strength` predicate.
  Same withheld components, plus a Bhava madhya whole-sign houses do not have.
  (`concept:strength-is-not-bhava-strength`.)
- **Do not rank grahas by strength.** `dep.strength-ranking` is registered, is priced at 13,
  and is blocked on source material rather than on code. Two cards are waiting on it and must
  keep waiting.
- **Do not add weighting to Stage 7.** The adjudicator has four relationships and three
  resolutions and no field a number could live in; a test asserts that, and another asserts no
  percentage reaches a `reason` string. The way to resolve more conflicts is to encode a source
  that states a precedence, never to invent one. See `dep.adjudication`, still outstanding on
  purpose. (New, Milestone 24: nor should a future session build `dep.lagna-strength` from a
  *guess* at what "Lagna strength" would mean — Decision 0b is explicit that this waits on a
  source stating a verdict outright, not on engine work.)

**Blockers:** none blocking encoding, and no open P0.
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
| Ch.4 — Shadbala/Bhavabala strengths | ~~`dep.strength`~~ **built, Milestone 22**; the *numeric* half is blocked on `dep.shadbala-arithmetic` | a source that prints the Yudha, Chesta and Drig methods Phaladeepika withholds — BPHS is the candidate, and is not converted | chapter fully encoded; its verdict doctrine is live and its arithmetic is permanently blocked on this book |
| Ch.13 — Longevity (ayurdaya) | `dep.adjudication` | competing longevity methods disagree by construction and need adjudication before weighing | blocked |
| Ch.19 — Dasas | none to encode the chapter itself, but it is the source of `dep.dasa` | building the dasa engine after encoding | partially ready — the chapter carries an internal balance dispute to preserve as disagreement |
| Ch.20 — Dasa/antardasa effects by house lord | `dep.dasa`, `dep.lord-of-house` (lord-of-house is implemented) | dasa engine | blocked |
| Ch.22 — Kalachakra dasa | `dep.dasa` (its own calculator, distinct from vimshottari) | out of MVP scope | blocked, beyond MVP |
| Ch.23 — Ashtakavarga | none to encode, source of `dep.ashtakavarga` | building the ashtakavarga engine; chapter itself preserves a 44-vs-48-bindu source defect | partially ready |
| Ch.24 — Ashtakavarga per Horasara | `dep.ashtakavarga` | ashtakavarga engine | blocked |
| Ch.25 — Upagraha computation | `dep.upagraha` | upagraha calculator | blocked |
| Ch.26 — Transit (gochara) | `dep.transit` | transit engine, beyond MVP | blocked |
| `card:PD.09.Vargottama` | `dep.vargottama` | vargottama extractor (needs `dep.varga` first) | blocked |
| `card:PD.06.Pushkala`, `card:PD.06.Vasumati` | `dep.compound-friendship` + `dep.kendra-togetherness`, `dep.universal-quantification` respectively | new engine capabilities. **Pushkala's dependency was corrected in Milestone 22**: it named `dep.strength`, which is now built and does not release it | blocked |
| 16 cards with no unlock path yet | various combinations, see `Reports/PHASE3_PLAN.md` "Cards that no sequence here releases" | multiple simultaneous capabilities | blocked |

### Planned later

| Description | Notes |
|---|---|
| Brihat Jataka rule extraction | Book is corpus-converted (`Knowledge/brihat-jataka.md`, 6282 lines) but has **zero** rule cards. First cross-book corroboration cannot happen until this starts. |
| Convert remaining 4 books (BPHS Vol.1, Jataka Parijata Vol.1, Uttara Kalamrita, Saravali) | Behind the deliberate Phase 1 freeze; each has known OCR/text-layer problems documented in `Reports/PROJECT_STATUS.md` "Book audit". |
| `concept:manual-verification` — human sign-off on all cards | Only 4 of 404 cards have `extraction.verified_by` set. |
| ~~Stage 7 adjudication design~~ | **Done, Milestone 23** — the reading half is `Engine/adjudicate.py`. What is left here is `concept:parallel-of-overloaded` (§D Decision 0a), an *encoding* pass, not an engine one. Weighting is refused, not pending. |
| Phase 6 validation corpus | Hundreds of known/celebrity/historical charts — not started. |

### Production blockers

Must be solved before the system can be called production-ready, independent of card
count:

1. ~~**Stage 7 adjudication does not exist.**~~ **Reading half CLEARED in Milestone 23** —
   contradictory doctrine is now read, typed and reported with both sides quoted. It is still
   never *weighed*, and that is deliberate and permanent absent a source that states a
   precedence. See §K, P1-3.
2. **Only one book has rule cards.** Multi-book corroboration (a stated goal) cannot be
   assessed or delivered with a single-book store.
3. **No validation corpus.** No measurement exists of whether the system's predictions are
   any good (`Phases.txt` Phase 6).
4. **Human verification was essentially absent** (4/404 cards) as of Milestone 14; a
   systematic workflow now exists and 368/405 cards (91%) are signed off — see §K P1-1 for
   the current, authoritative count. This list (§E) predates that work and is kept for
   history; §K is the live register.
5. **No API/UI/packaging.** CLI-only today.
6. ~~**Stage 4 (strength) does not exist**~~ — **CLEARED in Milestone 22.** Graha
   strength exists and is read from the source's own verdicts. What remains is not a
   missing stage but a missing *source*: no encoded book supplies the arithmetic for a
   Shadbala Pinda, a Bhava Bala, or any ranking of one graha against another
   (`dep.shadbala-arithmetic`, `dep.strength-ranking`).

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
| **Graha strength verdicts (Stage 4)** | **Implemented (Milestone 22)** | `Engine/facts.py::_strength`, `Engine/doctrine.py::graha_strength_verdicts` — reads the five Phaladeepika ch. 4 vv. 4-5 verdict cards and emits `strong`/`weak`; **not** a Shadbala calculator | `PD.02.Form.Mars.Youthful`, `PD.10.WeakMoon5.Malefics`, `PD.10.Lord7.BeneficStrong`, `PD.10.WifeChildren.EvenSigns` |
| **Adjudication: reading the store's own relationships (Stage 7, reading half)** | **Implemented (Milestone 23)** | `Engine/adjudicate.py` — reads `contradicts`/`extends`/`parallel_of` undirected plus the strength extractor's chart-dependent collisions, and emits typed relationships (`contradiction`, `qualification`, `parallel_authority`, `override`) with resolutions (`applied`, `unresolved`, `recorded`). **No weighting, no score, no ranking, and no field one could live in** | the consultation's "How the applicable passages stand to one another"; `synthesise()`, which uses the contested pairs so a verse and its own refutation are no longer reported as agreeing |
| Relationship-link integrity as a build gate | Implemented (Milestone 23) | `Engine/rules.py::verify_cards` — a `contradicts`/`extends`/`parallel_of` target that is not a card in the store fails the run, as a stale quote does | every card carrying a link |
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
| Numeric Shadbala / Bhava Bala | Not implemented, and **not implementable from the encoded corpus** | `dep.shadbala-arithmetic`. Phaladeepika ch. 4 states the six components and explicitly withholds the arithmetic for three of them (Yudha, Chesta, Drig), so no Pinda can be computed from this book at all; Bhava Bala additionally needs a Bhava madhya whole-sign houses do not have. This is a *source* gap. Superseded the previous "Stage 4 not built" row when Milestone 22 built the verdict half. |
| Ordinal strength (which graha is *strongest*) | Not implemented | `dep.strength-ranking`. The encoded doctrine states a verdict, not an order, and ranking two grahas that are both merely "strong" would be the engine inventing an order the source never supplies. Blocks `PD.10.WifeDirection.Strongest` and `PD.10.Marriage.StrongerDasha`. |
| Compound (Panchadha maitri) friendship | Not implemented | `dep.compound-friendship`. The Adhimitra/Adhishatru tiers, which the book defines in ch. 2 and then uses without definition in ch. 6 v. 19, ch. 10 v. 23 and six rows of the ch. 4 survey. Cheap (cost 3) and well-sourced; identified in Milestone 22 as `PD.06.Pushkala`'s real blocker. |
| House-to-body-part correspondence | Not implemented | `dep.body-part-significator`. Nothing in the store maps a house to a limb, so `PD.01.Kalapurusha.Strength` would emit a claim naming no body part. |
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
| Stage 7 **weighting/precedence** (deciding which of two claims wins) | Not implemented, and **not scheduled** | `dep.adjudication`. The *reading* half was split off as `dep.adjudication-representation` and built in Milestone 23; what remains would require the engine to choose where the corpus does not, which the standing prohibition on invented confidence and source prestige forbids. Eleven registry entries declare this dependency and each needs either a rule from a source or a human's ruling. |
| Cross-card cancellation mechanism | Not implemented, **and no case needs one** | Investigated in Milestone 23. The store's one real cancellation doctrine (Sakata Yoga, ch. 6 v. 17) prints the yoga and its cancellation in a single sentence, so the cancelling clause is a negated conjunct inside the card's own condition and the card has simply not fired for a kendra Moon since Milestone 9. Every "unless" in the store is the same shape. Building a framework for this would have been architecture for a solved problem. |
| Corroboration between books on a **yoga** | Not implemented | `concept:parallel-of-overloaded`. `parallel_of` does not distinguish "this authority agrees" from "this authority states it differently" — and one linked card does state it differently — so Stage 7 reports a second authority's words without asserting agreement. An encoding decision, not an engine one; see §D Decision 0a. |
| Distinct-sign-count fact (how many signs the 7 classical grahas occupy) | Not implemented | Newly identified this session, blocks ch.6 vv.39-41 specifically; small and well-scoped, not yet built. |
| Native-sex-scoped rule handling | **Implemented (row corrected in Milestone 19).** The previous text here claimed "the birth record does not carry sex, so all sex-scoped cards stay inert regardless" — that is stale and was wrong at the time of writing. `BirthRecord` carries `sex` (`Engine/chart.py:58`), `Engine/cli.py` exposes `--sex`, and `Engine/activate.py` 93-97 enforces `scope.sex`, refusing a card whose stated sex does not match the record (including when the record says `unknown`, which is the correct outcome rather than a guess). | Sex-scoped cards such as `PD.10.Female.MoonSaturn7Remarriage` / `PD.10.Male.MoonSaturn7` are `active` and fire correctly when `--sex` is supplied. ch.11 (Female Horoscopy) is **not** blocked on this and is listed as newly unblocked by `backlog.py`. |

---

## G. SOURCE / CORPUS STATUS

| Book | PDF pages | Text layer | Method | Converted? | In `Knowledge/`? | Rule cards? | Known defects |
|---|---|---|---|---|---|---|---|
| Brihat Jataka | 230 book pages (115 scanned spreads) | Corrupt OCR | Surya OCR | Yes — 28/28 chapters, 408 verses sequential, 0 hallucinated lines, 0 `[UNCLEAR]` | Yes (`Knowledge/brihat-jataka.md`, 6282 lines) | **2** (ch. 2 v. 5's natural benefic/malefic classification, Milestone 20) | Devanagari glyph-level spot-check still owed (~1.5% char-error rate measured, not yet spot-checked); 2 misread verse numbers (8 vs. ४) corrected with evidence; 1 printed duplicate line preserved as printed; 7 tables + 10 charts of figure-transcription queue status unverified this session |
| Phaladeepika | 265 pages | Clean digital | `pdf_text` direct extraction | Yes — 28/28 chapters | Yes (`Knowledge/phaladeepika.md`, 5969 lines) | **499**, from chapters 1, 2, 4, 6 (partial), 8, 9, 10 | Numerous — see `Rules/phaladeepika/manifest.json` `known_defects` (24 entries); most severe is the ch.23 Ashtakavarga chart totaling 44 instead of 48 bindus, preserved as printed |
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
**Passages requiring human verification:** `concept:manual-verification` — the interpretive
queue is closed (498/501 signed). 3 cards are deliberately held unsigned for real defects, not
for want of review: `PD.01.Kalapurusha.Strength` and `PD.10.Venus.VargaMarsSaturn` (blocked on
missing capabilities) and `PD.04.Lagna.TripedSign` (blocked on a human's reading of a printed
word). See §K P1-1 and `Reports/VERIFICATION_QUEUE.md`.

---

## H. KNOWN DEFERMENTS

The full machine-readable list lives in `Rules/deferred.json` and is rendered by
`Rules/tools/backlog.py` into `Reports/PHASE3_BACKLOG.md` (136 entries as of Milestone 23) on every run — that
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
| `concept:manual-verification` | Human sign-off on all cards | 498/501 verified (99.4%) as of Milestone 21; see §K P1-1 for the live count | Queue closed; 3 deliberate defect holdouts remain | **Arguably yes for true production** | Cleared as a blocker (P1-1, Milestone 19); the 3 holdouts are tracked individually |
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
still pending in ch.19). **As of Milestone 23 they are also read**: Stage 7 reports each
relationship with both sides quoted and an explicit `unresolved` outcome. They are still never
weighed against each other.

**Decision (Milestone 23):** Adjudication is a layer *above* the claims and may not edit them.
**Reason:** The system must be able to answer "what did the source say?" and "how did the
reasoning layer reconcile those statements?" separately. Collapsing the two produces output in
which a reader cannot tell a quotation from an inference — the failure this whole architecture
is arranged against.
**Consequence:** `adjudicate()` is pure with respect to `claims` and `facts`; Part 2 is
byte-identical with the module present and absent, and a test asserts it. Adjudications are a
separate list on `Result` with their own Stage 9 verification (`verify_adjudications`).

**Decision (Milestone 23):** The engine may apply a precedence only where a source states one
in its own sentence; otherwise the relationship is `unresolved` and both statements stand.
**Reason:** Any general precedence rule the engine supplied would be doctrine the engine
invented — "book A is more correct than book B" — which the corpus does not authorise and no
citation could support.
**Consequence:** Exactly one precedence is applied anywhere in the engine: chapter 4 verse 4's
combustion override, which the verse prints in the same sentence as the weakness. There is no
field on an `Adjudication` in which a number could be recorded, the relationship and resolution
vocabularies are closed and enforced by Stage 9, and `unresolved` is a finished answer rather
than a placeholder.

**Decision (Milestone 23):** A relationship link is classified from fields the encoder wrote,
never from prose in a `note`.
**Reason:** Parsing an encoder's prose to decide what a link means would put the engine's
reading of English where a recorded judgement belongs, and would silently change meaning
whenever a note was reworded.
**Consequence:** `contradicts` + `polarity: "qualified"` → qualification; `extends` →
qualification; `parallel_of` + `predicts.authority` on the other card → parallel authority;
`parallel_of` without one → **no relationship at all**, because that shape is a sibling card
from the same sentence. Where the fields cannot settle a question the answer is a registry
entry, not a guess — `concept:parallel-of-overloaded` exists because the link cannot express
whether the second authority agrees.

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

> **Read §K, not this section, for the live state.** This audit is kept verbatim as the record
> of how the blockers were ranked, and two of its conclusions have since been overtaken by
> events: it ranks `dep.strength` as the highest-leverage missing capability (it was built in
> Milestone 22) and it describes `PD.06.Pushkala` and `PD.01.Kalapurusha.Strength` as blocked
> on `dep.strength` (both were re-diagnosed in Milestone 22 and neither is). Its *method* —
> ranking by what a capability releases rather than by how interesting it is — is what has
> lasting value here.

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

***There is no open P0.*** P0-2 was cleared in Milestone 20 and **P0-1 in Milestone 22**. This is the first time the register has been empty at this level, and it means the next milestone is chosen for return rather than forced by a blocker — see §D.

**P0-1 — `dep.strength` (Stage 4) did not exist. CLEARED (Milestone 22).**
- **Why it matters:** Classical doctrine conditions on planetary/house strength throughout
  the corpus; without it, ch. 4 itself and large fractions of many other chapters (ch.19 at
  70% inert-on-arrival, ch.20 at 67%, ch.21 at 89%, per `Reports/PHASE3_PLAN.md`) are born
  inert regardless of how much more is encoded.
- **Current state:** **Half done (Milestone 21).** The source half is complete — ch. 4 is
  encoded in full, 94 cards, and `chapter:phaladeepika.04` is resolved. The engine half is
  not started: no chart produces a strength fact today. Blocks 8 cards directly
  (`PD.02.Form.Mars.Youthful`, `PD.06.Pushkala`, `PD.01.Kalapurusha.Strength` and 5 in ch. 10),
  7 in closure per `leverage.py`.
- **Dependency:** **satisfied.** Ch. 4 had to be encoded first — the engine may not hardcode
  strength rules the book itself states — and it now is. `leverage.py` no longer lists a
  blocking chapter and ranks `dep.strength` second overall (cost 8).
- **Exact work required:** ~~(1) encode ch. 4 fully as ordinary Phase 3 work~~ **done,
  Milestone 21**; (2) build Stage 4 as a `_strength` extractor reading only ch. 4's reference
  cards — the five verdict cards from vv. 4-5 listed in §D, **not** a numeric Shadbala
  calculator; (3) re-run `backlog.py`/`leverage.py` to confirm the unlock.
- **What it unlocks:** 2 cards go active immediately (`PD.02.Form.Mars.Youthful`,
  `PD.06.Pushkala`); 6 more move one dependency closer; and it removes the single largest
  "born inert" tax on every future chapter per §J.5.
- **Scope correction from the source (Milestone 21):** this blocker was written expecting
  Shadbala/Bhavabala arithmetic. **The chapter does not supply it** — three of the six
  components have their arithmetic explicitly withheld, so a Pinda cannot be computed from
  this book at all. Stage 4 will therefore emit the `strong`/`weak` verdicts vv. 4-5 state
  outright and nothing numeric. Registered as `concept:strength-criterion-scope`; ratifying
  that is one of the two decisions owed in §D.
- **How it was closed (Milestone 22):** `Engine/facts.py::_strength`, a verdict extractor
  reading the five vv. 4-5 cards and nothing numeric, plus
  `Engine/doctrine.py::graha_strength_verdicts`. **No graha and no rule is hardcoded**; delete
  the cards and the capability goes with them, and a test asserts that.
- **What it actually delivered:** 4 cards active (`PD.02.Form.Mars.Youthful`,
  `PD.10.WeakMoon5.Malefics`, `PD.10.Lord7.BeneficStrong`, `PD.10.WifeChildren.EvenSigns`),
  each confirmed firing on a real nativity; 2 chapter 6 passages released for encoding; the
  "born inert" tax on future chapters paid; and a conflict found that the encoding pass could
  not see (`concept:retrograde-combust-collision`).
- **What it did NOT deliver, by the source's choice and not the schedule's:** no Shadbala
  Pinda, no Bhava Bala, no ranking. Four cards named `dep.strength` and are *not* released by
  it; each had its declared dependency corrected rather than being forced active, because a
  card left declaring a satisfied dependency is reported by the backlog as released.
- **Scope correction, restated because it is permanent:** this blocker was written expecting
  Shadbala arithmetic. The chapter does not supply it and no encoded book does. That gap is
  now its own catalogue entry, `dep.shadbala-arithmetic`, rather than an unmet expectation
  attached to a cleared blocker.
- **Status:** **CLEARED.** Do not re-open it to add a calculator. If a future session wants
  numeric strength, the work is *converting a source that prints the three withheld methods*,
  not writing arithmetic against this one.

**P0-2 — The benefic classification gap. CLEARED (Milestone 20).**
- **What it was:** Jupiter and Venus received no `nature` fact on any chart, so all 22 active
  cards conditioning on `benefic` under-fired on every consultation. `PD.10.Benefics.In7`
  could not fire for Jupiter in the 7th.
- **How it was closed:** by encoding Brihat Jataka ch. 2 v. 5 — *"Moon other than of the nature
  referred to above, Mercury, Jupiter and Venus are natural benefics."* — as
  `BJ.02.Nature.Benefics` / `BJ.02.Nature.Malefics`, and letting the existing extractor read
  them. **No graha was hardcoded**; the fix is a card, and if the classification ever goes
  missing again the fix is another card, never a Python constant. A test says so.
- **Verified at the source, not just the corpus:** the quote was confirmed against the rendered
  page (image `p0033`, printed p.30), which also established that it sits in the translation
  body rather than the `Commentary:` block. The verse behind it was read on image `p0034`.
- **Result:** all 9 grahas classified. 4 corroborated by both books. Demo-chart claims 35 → 41,
  five further cards firing, none lost.
- **Status:** **CLEARED.** The Moon half of the passage was deliberately not asserted; that is
  `concept:moon-nature-criterion`, an open question for a human (§D), not a residual blocker —
  Phaladeepika classifies the Moon unopposed today.

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
  `PD.01.Kalapurusha.Strength` (**re-diagnosed in Milestone 22**: it was recorded as needing
  `dep.strength` + `dep.condition-variables`, both of which now exist and neither of which
  releases it — what it actually needs is `dep.body-part-significator`, because nothing in the
  store maps a house to a limb, plus a condition repair that means splitting one quote stating
  two opposite verdicts into the two cards it contains) and
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

**P1-2 — Only one book had rule cards. CLEARED (Milestone 20).**
- **What it was:** Brihat Jataka was fully corpus-converted and frozen but had **zero** rule
  cards, so multi-book corroboration — a stated Phase 4 goal — could not be assessed at all.
- **How it was closed:** `BJ.02.Nature.Malefics` and `BJ.02.Nature.Benefics`, the first cards
  ever encoded from a second book, together with `Rules/brihat-jataka/manifest.json`. The
  existing toolchain (`verify.py`, `dupes.py`, `backlog.py`, `review.py`) accepted the second
  book without modification, which is the real proof that the store's design generalises.
- **What it delivered immediately:** genuine cross-book corroboration on 4 grahas, surfaced in
  the consultation, plus the discovery and repair of a provenance defect the second book's
  arrival created (nature facts had been citing every `graha_nature` card in the store rather
  than the ones that classify that particular graha).
- **Status:** **CLEARED** in the sense that mattered — the single-book condition is broken and
  corroboration is real and exercised. Breadth is now ordinary Phase 3 work: the book has 2
  cards against Phaladeepika's 499, and its remaining 27 chapters plus the rest of ch. 2 are
  registered in the backlog (`chapter:brihat-jataka.*`, `passage:brihat-jataka.02.remainder`).

**P1-3 — Stage 7 adjudication. The reading half is BUILT (Milestone 23); the weighting half is
deliberately not, and is no longer scheduled.**

- **What Milestone 23 delivered.** `Engine/adjudicate.py`. The `contradicts`, `extends` and
  `parallel_of` links had been carried in the store since chapter 1 and **no code read any of
  them** — so no consultation had ever surfaced a single declared contradiction, and Part 3
  actively reported one as agreement on 83% of charts. All four relationship types now reach
  the reader with full provenance and an explicit `unresolved` state. Claims are untouched:
  Part 2 is byte-identical before and after.
- **What it deliberately did not deliver, and why the blocker text below still stands.** No
  weighting, no confidence, no precedence beyond the one the source states in its own sentence.
  Not for want of material — because the material argues the other way. **Exactly one
  claim-to-claim contradiction exists in the whole corpus** (`PD.09.Dignity.Exalted` against
  its own translator's note), verified across 720 charts and pinned by a test; every other
  `contradicts` link has a side that never becomes a claim. A weighting scheme designed for a
  sample of one is how a project invents doctrine, which is the same reasoning that kept this
  blocker closed before — it just now rests on a measurement rather than an estimate.
- **The bookkeeping.** `dep.adjudication-representation` is registered `implemented: true`;
  `dep.adjudication` stays outstanding because eleven entries declare it and this releases
  none of them.
- **Status: half CLEARED, half correctly refused.** Do not open the second half to add a
  weighting scheme. If a future session wants the engine to choose between two claims, the work
  is *encoding a source that states the precedence*, not writing arithmetic against ones that
  do not.

**Original P1-3 text (Milestone 20-22), kept for the record:**
- **Why it matters:** Contradictory doctrine is preserved (`contradicts`/`extends`) but never
  weighed against itself. `Phases.txt` Phase 4 was otherwise entirely unbuilt.
- **What changed in Milestone 20 — a partial build, and a correction to this entry's own
  premise.** Milestone 19 re-scoped this blocker on the grounds that P0-2's fix could not be
  taken without conflict adjudication, because the two books appeared to define the Moon's
  nature by incompatible criteria. **That premise was wrong.** Reading the Devanagari behind
  Brihat Jataka's English showed the 72-degree figure to be the translator's parenthetical
  gloss on क्षीण, not a competing doctrine — so the two books agree everywhere they both speak,
  and what the relationship actually required was a way to *record agreement*, not to resolve
  disagreement. That half was built:
  - `settle()` accumulates authorities instead of overwriting; nature facts carry
    `authorities`, `books`, `corroborated`.
  - Attribution is per graha, not per extractor run.
  - The consultation reports cross-book agreement as counts of books, never as a score.
- **What is still missing:** everything to do with authorities that genuinely *disagree*.
  `_resolve_nature` still raises `DoctrineError` rather than choosing — deliberately, and now
  naming both offending cards so an encoder can find the pair. There is still no priority rule,
  no weighting, no cancellation, and no cross-book disagreement narrative.
- **Dependency: SATISFIED as of Milestone 22.** What was missing was a **real conflict to
  design against**; Milestone 20 removed the one candidate this project had, and there are now
  three, all preserved and none resolved:
  1. `concept:kendra-positional-strength-conflict` — ch. 4 v. 3 against v. 8, on how much
     positional strength a kendra is worth. Both encoded, linked with `contradicts`.
  2. `concept:retrograde-rescue-scope` — ch. 4 v. 4 against ch. 9 v. 20, on whether
     retrogression rescues unconditionally. Linked with `extends`.
  3. `concept:retrograde-combust-collision` — ch. 4 v. 5 against v. 4, and **the first that is
     not visible in the cards at all**: it exists only on a chart where a graha is both
     retrograde and combust, and `_strength` refuses a verdict there rather than choosing.
  Three is enough material to design against without inventing a scheme for a sample of one,
  which was the whole reason for the wait. Chapter 6's Mantreswara-vs-Parashara dusthana-lord
  dispute (`passage:phaladeepika.06.p202`) would be a fourth and is still unencoded.
- **Note on what the third one teaches:** the two existing refusal sites now differ in kind.
  `_resolve_nature` raises and aborts, because a graha classified two ways is an encoding fault
  affecting every chart. `_strength` declines *per graha* and continues, because a
  chart-dependent collision is not a fault and aborting the extractor would lose eight sound
  verdicts to save one. Any adjudication design has to accommodate both shapes.
- **Exact work required:** do **not** build a general weighting or confidence system. When two
  or more genuine conflicts exist, build only what represents them: which authorities claim
  what, on what basis, and an explicit "unresolved" state where no documented priority rule
  applies. The standing prohibition on invented numeric confidence stands.
- **Status:** **Half built, and correctly stalled on the other half.** It is no longer gating
  anything: P0-2 is closed without it. Note the standing lesson — before building adjudication
  for an apparent contradiction, read the source behind both sides; one of them may be a gloss.

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

- **A relationship the store records is worth nothing until code reads it.** For twenty-two
  milestones every encoding pass faithfully wrote `contradicts`, `extends` and `parallel_of`
  links, and no line of engine code ever read one — so no consultation surfaced a single
  declared contradiction, and Part 3 reported a verse and its own printed refutation as
  *agreeing* on 83% of charts, under a heading that said "without contradiction". Card-level
  verification could not catch it; neither could reading Part 2. **When adding a field to a
  card, check that something consumes it, and add the build gate that fails when it dangles.**
  (Milestone 23.)
- **`unresolved` is a finished answer, not a placeholder.** Where the corpus states no
  precedence the engine says so, quotes both sides, and stops. Do not add weighting to Stage 7
  to "finish" it — `dep.adjudication` is outstanding on purpose, and the way to resolve more
  conflicts is to encode a source that states one.
- **The obvious cancellation case needs no cancellation mechanism.** Sakata Yoga's cancellation
  is printed in the same sentence as the yoga, so it is a negated conjunct inside the card's
  own condition and has worked since Milestone 9. Check whether the encoding already handles a
  case before building architecture for it. (Milestone 23; the same lesson as §I's standing
  rule, arrived at from the other direction.)
- **Test the output of a discriminator, not its input.** Milestone 23's suite passed a mutation
  that would have manufactured corroboration out of sibling cards, because the test asked "do
  these cards name an authority?" instead of "does the adjudicator ever emit one without a
  named authority?". Mutating the module under test is what found it, and is worth doing again.
- **Before building adjudication for an apparent contradiction, read the source behind both
  sides — one of them may be a translator's gloss.** Milestone 19 identified a hard cross-book
  conflict on the Moon's nature and concluded Stage 7 had to be built before P0-2 could be
  fixed. Milestone 20 read the Devanagari and found the conflicting criterion was a
  parenthetical gloss with no warrant in the verse. Building the adjudication engine first
  would have been architecture for a contradiction that does not exist. This is the single most
  transferable lesson in this file.
- **P0-2 is CLEARED (Milestone 20)** — Jupiter and Venus are classified, from Brihat Jataka
  ch. 2 v. 5. **Never fix a classification gap by telling the engine the answer**; encode the
  book that says it. A test asserts the citation for Jupiter and Venus comes from a card.
- **One human decision is owed: `concept:moon-nature-criterion`** — settle it before encoding
  further `graha_nature` doctrine, because it sets the precedent for every translator's gloss
  in the corpus. §D states the three positions and the recommendation.
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
- **Brihat Jataka has 2 rule cards** (was zero) and a manifest, as of Milestone 20. The
  toolchain accepted a second book with no changes. Extracting more of it is now ordinary
  Phase 3 work with no setup cost, and its ch. 2 remainder restates doctrine Phaladeepika
  already carries — the cheapest place to test whether corroboration holds on a second
  relation.
- **vv.39-41 needs a small new engine capability** (distinct-sign-count of the 7 classical
  grahas) — well-scoped, not yet built, `passage:phaladeepika.06.p168`.
- **`dep.strength` (Stage 4) is the single highest-leverage missing capability** — it
  unlocks 8 cards directly and gates entire future chapters (ch.4 itself, and large
  fractions of many others per `Reports/PHASE3_PLAN.md`'s inert-on-arrival table, e.g.
  ch.19 at 70%, ch.20 at 67%, ch.21 at 89%).
- **Second-nativity architecture is deliberately unbuilt** — do not approximate a spouse's
  chart from the native's own chart as a shortcut; it was explicitly deferred as a schema
  decision requiring real design (`dep.second-nativity`).
- **Cross-book corroboration exists and is exercised** — 4 grahas' natures are stated
  independently by both books, and the consultation reports which claims rest on one authority
  and which on two. It is reported as counts of books and **never as a score**; the engine has
  no mechanism for preferring one authority to another and the output must not imply one.
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
