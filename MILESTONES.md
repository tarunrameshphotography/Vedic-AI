# VEDIC-AI MASTER PROJECT MILESTONES

**Project purpose:** Build an AI that reads a Vedic birth chart the way a traditional
astrologer would, where every predictive sentence traces to a rule printed in a real book
applied to a quantity that was actually computed. Governing rule: *the system may compute,
and it may quote — it may not invent.*

**Current production-readiness: 60%** (see §A; recomputed, not incremented — Milestone 37 holds
60.00% exactly: every row's own delta this milestone (10 new firing cards against a ~1,535-card
estimate; 0 new predicates/stages; 0 new relationship links; a raw-fraction provenance move; +23
tests) falls below every row's own established rounding threshold, the same posture
Milestones 26/32/34/36 already took for their own small, correct, fully-verified additions. Card
count moves 601 → 611 (+10 firing, +0 reference)).

**Current phase:** knowledge (Phase 3). Milestone 37 closes Phaladeepika chapter 7's own slice 2
(vv.13, 18, 20 items (b)-(d), 24, 25) — ten firing cards, closing zero new engine capability, plus one
new dependency registered (`dep.own-or-benefic-dignity-in-varga`) for a gap discovered while reading
v.19. Phase 2 (engine completion) and Phase 4 (integration) are both untouched. Stage 7's
*representation* half is built; its *weighting* half is deliberately not, and is not scheduled.

**Current milestone:** Milestone 37 — **Phaladeepika chapter 7 slice 2 encoded
(`PD.07.Emperor.VargottamaMoonAspectedNoMalefic` v.13, `PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation`
v.18, `PD.07.King.JupiterLagnaNotCapricorn`/`.StrongLagnaLordKendra`/`.StrongMercuryKendraAspectedJupiter`
v.20 items (b)-(d), `PD.07.RajaYoga.MaleficsThirdSixthEleventh`/`.MarsMercurySecond`/`.SunVenusFourth`/
`.MarsSaturnJupiterTenthEleventhLagna` v.24 items (1)-(4), `PD.07.RajaYoga.HouseLordKendraFromMoonJupiterOwnership`
v.25): ten further Raja Yoga configurations from the chapter's own general (unnamed) material, selected
from the eight `dep.none`-tagged verse clusters Milestone 36 flagged as "chapter 7 slice 2" candidates
(vv.10,13,14,18,19,20,24-25). Zero new engine capability — `vargottama`, `strength`, `aspects`,
`nature`, `in_house`, `in_house_class`, `in_house_from`, `lord_of_house`, `dignity` and `lagna_sign`
all reused exactly as-is; `in_house_from`'s reference argument is bound to a variable (the Lagna-lord)
rather than only the literal `"Moon"` for the first time, exercising `dep.graha-frame`'s already-general
shape rather than extending it. Three of the eight candidate clusters were found, on closer reading, NOT
actually ready and were deliberately left out with corrected bookkeeping rather than forced through: v.10
(a fully specified configuration whose "middle of Sagittarius"/"very powerful Mars" phrasing needs its
own descriptive-vs-testable judgement call, not bundled into a five-verse slice); v.14 and v.21 (both
need "aspected by or associated with a friendly planet", and natural friendship — though the doctrine
exists, `dep.dignity-friendship` — is not exposed as a directly queryable condition-language predicate);
and v.19, whose Milestone 36 note ("reuses dignity/dignity_in_varga") was found on inspection to be
wrong — `dignity_in_varga` was built Milestone 29 deliberately scoped to emit only `"debilitated"`, so
it cannot test "own... Varga", and "benefic Varga" is itself an undefined term in this corpus; corrected
under a newly registered dependency, `dep.own-or-benefic-dignity-in-varga` (not implemented), rather
than left mis-filed under `dep.none`, which would have reported it falsely available. `passage:phaladeepika.07.p020`,
`.p038` and `.p055` move to `resolved`; `passage:phaladeepika.07.p040` is split into a `resolved` remainder
(items (b)-(d)) and a newly-deferred `passage:phaladeepika.07.p040-royalfamily` (item (a), gated on the
native being "born in a royal family" — a birth-record field `BirthRecord` does not carry, the same gap
`passage:phaladeepika.07.p001` already named for vv.1-2, not a temporal-ordering deferral).** See
Milestone 37 in §C for the full write-up.

**Previous milestone:** Milestone 36 — **Phaladeepika chapter 7 slice 1 encoded
(`PD.07.Neechabhanga.LordOrExaltedInSign`/`.MutualKendra`/`.AspectedByLord`/`.LordOrExaltLordKendra`
/`.PlanetItselfKendra`, vv.26-30): the Neechabhanga Raja Yoga family — the five ways a debilitated
graha's debilitation is classically said to be cancelled (its debilitation-sign lord or the graha
exalted in that sign, in Kendra from the Lagna or the Moon; that lord and the graha's own
exaltation-sign lord mutually in Kendra; the debilitated graha aspected by its own sign's lord; the
debilitation-sign lord or the graha's own exaltation-sign lord in Kendra; the debilitated graha
itself in Kendra). Zero new engine capability — `dignity`, `in_house_class`, `in_house_from`,
`in_house` and `aspects` all reused exactly as-is; each card is an existential ("any") over the seven
classical grahas rather than five per-graha named cards, matching `PD.20.MiseryDasa.DusthanaLords`'s
own existential-over-a-fixed-set precedent rather than Pancha Mahapurusha's per-graha-named one,
since Neechabhanga carries one name for a general condition on "a planet," not five separately named
yogas. The per-graha debilitation/exaltation-sign-lord table is read from the store's own
`PD.01.SignLord.*`/`PD.01.Exaltation.*` reference cards at authoring time, not a Python literal, and
cross-checked by a dedicated regression test against drift. A sixth, non-firing reference card
(`PD.07.Neechabhanga.UchchanathaNote`) preserves the translator's own Note resolving two interpretive
questions v.26's prose leaves open (which of two commentators' readings of "the planet exalted in
the sign" is correct, and whether the verse's "or" is disjunctive or conjunctive) — both resolved
within the source itself, using its own worked example (Saturn debilitated in Aries; Mars, Aries's
lord, and Sun, exalted in Aries, both in Kendra to the Lagna), which is also this milestone's primary
real-chart validation case, reconstructed as a synthetic chart from a real ephemeris nativity with
select bodies and the Lagna overridden. Verses 1-25 are individually deferred in `Rules/deferred.json`
(23 new passage entries, none silently dropped), three genuinely new dependencies registered
(`dep.graha-condition-count`, `dep.digbala`, `dep.parivartana`) and several existing ones reused
(`dep.paksha`, `dep.day-night`, `dep.compound-friendship`, `dep.lagna-strength`) — roughly a third of
those 25 verses (vv.10,13,14,18,19,20,24,25) were found, on a full verse-by-verse reading, to be
independently close to encodable with zero new capability and are flagged as a strong "chapter 7
slice 2" candidate for the next Phase 3 session.** See Milestone 36 in §C for the full write-up.

**Milestone before that:** Milestone 35 — **Developer frontend + local API adapter (`Api/`, `Frontend/`):
a local FastAPI adapter over the unchanged `Engine.pipeline.run()`, and a React/TypeScript inspection
UI covering all 13 views the master prompt specifies — birth input, chart summary, claims explorer
with full source/provenance, Vimshottari dasa timeline, adjudication view, a deferred/unsupported
view that keeps "not triggered"/"not computable"/"reference only"/"source unresolved" visibly
separate, fact inspector, rule inspector, verification view, comparison mode, chart view, and local
test-chart save/load. Zero doctrine change, zero new predicate, zero new rule card; one additive
`Engine.dasa.chart_mahadasa_timeline` helper, extracted (not duplicated) from logic
`activate.py`'s Stage-9 window re-derivation already had. Verified end-to-end in a real headless
browser against the project's own Thanjavur demo chart, and by an automated live CLI-vs-API
regression test — not merely built.** See Milestone 35 in §C for the full write-up.

**Milestone before that:** Milestone 34 — **Phaladeepika chapter 20 v.26 encoded
(`PD.20.WealthDasa.Venus`): Venus in its own sign or exaltation sign, in the 10th, 11th or 12th
house, uneclipsed (not combust) and free from the influence of a malefic (not conjunct or aspected
by one), producing wealth, glory, splendour and comfort during Venus's own mahadasa. Zero new
engine capability — `dignity`, `in_house`, `combust`, `conjunct`, `aspects`, `nature` and
`mahadasa_lord` all reused exactly as-is. "Uneclipsed" confirmed as this book's own synonym for
`combust`, twice inside chapter 20 itself (vv.19, 22); "influence of a malefic" read as
`conjunct`/`aspects`, corroborated at ch.9's own "associated with or aspected by malefics." The
original three-verse combined deferral (`passage:phaladeepika.20.p025-026-033`) is split into
three entries — v.26 resolved, v.25 and v.33 each carrying forward their own distinct,
still-unbuilt sign-class dependency.** See Milestone 34 in §C for the full write-up.

**Milestone before that:** Milestone 33 — **Phaladeepika chapter 20 v.24 items (1)-(3) and (5) encoded
(`PD.20.MiseryDasa.SaturnFourth`/`.JupiterSixth`/`.MarsRahuFifth`/`.DusthanaLords`): Saturn's/
Jupiter's/Mars-or-Rahu's mahadasa bringing misery when it occupies a specific ordinal position
(4th/6th/5th respectively) in the birth-fixed mahadasa sequence counted from the dasa the native
was born in, plus the unconditional dasas of the lords of the 6th, 8th and 12th houses.
`dep.mahadasa-ordinal` built — one predicate, `mahadasa_ordinal(graha,ordinal)`, exposing
`MahadasaPeriod.ordinal` (already computed for `dep.dasa`) as its own fact. Item (4) (last-degree
placement) stays deferred under a new `dep.dasa-last-degree`, split out from the same passage
entry rather than left inside a now-resolved catch-all — the verse gives no numeral and no Notes
for it, unlike items (1)-(3)'s three worked examples. `PD.20.MiseryDasa.DusthanaLords`'s own
unconditional claim was found, at authoring time, to collide with vv.7/9/13's strength-gated
`PD.20.Strong.House6`/`.House8`/`.House12` for a chart where a dusthana lord is both strong and
its own mahadasa lord; recorded as three `contradicts` pairs (Stage 7's existing reading
mechanism, not a new one) rather than left for a lexical pass to silently miss.** See Milestone 33
in §C for the full write-up.

**Milestone before that:** Milestone 32 — **Phaladeepika chapter 20 v.27 encoded
(`PD.20.Placement.BeneficAdverse` / `.MaleficMiseries`): benefics/malefics in debilitation, an
inimical sign, or literally the 6th or 12th house (not the full 6th/8th/12th dusthana class)
producing adverse/miserable dasa effects, for any graha rather than specifically a house lord. Zero
new engine capability — `nature`, `dignity`, `in_house` and `mahadasa_lord` reused exactly as-is.**
See Milestone 32 in §C for the full write-up.

**Previous milestone:** Milestone 31 — **Chapter 20's Mahadasa-scoped house-lord dasa doctrine
encoded (vv.2-21, v.22's first two sentences, v.40's first sentence, v.41); no Antardasa mechanism
built — confirmed, by reading all 63 verses directly, that no order or duration arithmetic for the
nine antardasa sub-periods is printed anywhere in chapters 19 or 20.** See Milestone 31 in §C for
the full write-up.

**Milestone before that:** Milestone 30 — **`dep.dasa` built (Vimshottari mahadasa only); chapter 19
encoded; `PD.09.Dignity.Inimical` released and split.** See Milestone 30 in §C for the full
write-up.

**Two milestones before that:** Milestone 29 — **`dep.varga`/`dep.vargottama` built (Navamsa/D9 only);
chapter 3 slice 1; two cards released, one re-diagnosed.** See Milestone 29 in §C for the full
write-up.

**Exact resume point:** Milestone 37 closed chapter 7's own slice 2 (vv.13, 18, 20(b)-(d), 24, 25) in
full; chapter 20's own state is exactly where Milestone 34 left it (Milestones 35-37 all touched
chapter 7 or infrastructure only). `git fetch --all --prune`, confirm `main` == `origin/main`, then
pick up §D. There is still **no open P0**. Of the eight verse clusters Milestone 36 flagged as "chapter
7 slice 2" candidates, five are now resolved (this milestone) and three remain genuinely blocked, each
corrected below rather than left mis-tagged `dep.none`: **v.10** (a fully specified configuration whose
"middle of Sagittarius"/"very powerful Mars" phrasing needs its own descriptive-vs-testable reading,
deliberately not bundled into this slice — `passage:phaladeepika.07.p015`, still `dep.none`, genuinely
available whenever a session wants to make that reading call); **v.14 and v.21** (both need "aspected
by or associated with a friendly planet" — `dep.dignity-friendship` computes natural friendship
internally but does not expose it as a directly queryable condition-language predicate; still
`dep.none`, since the gap is architectural exposure, not missing doctrine, and a future session should
check whether widening `_dignity`'s own friendship half into its own fact is the right fix before
building anything); and **v.19** (`passage:phaladeepika.07.p039`, "own or benefic Varga" — re-tagged
this milestone from `dep.none` to the newly registered `dep.own-or-benefic-dignity-in-varga`,
unimplemented; `dignity_in_varga` was built Milestone 29 deliberately scoped to only "debilitated", and
"benefic Varga" itself still needs a human reading before any arithmetic is well-posed). The rest of
chapter 7 is unchanged from Milestone 36's own accounting: blocked on `dep.graha-condition-count`
(vv.1-4,8,12), `dep.digbala` (v.4), `dep.parivartana` (v.9's second yoga), `dep.paksha` (vv.7,11,12,17,22),
`dep.day-night` (v.16), `dep.compound-friendship` (v.23), `dep.lagna-strength`'s own architecture gap
(v.5), and two passages needing a careful human re-reading (v.6's unclear second "the lord" referent;
v.15's own two-commentator dispute). `passage:phaladeepika.20.p026` is `resolved`; v.25 and v.33 each
still need their own unencoded sign classification (`dep.urdhvamukha-sign-class`,
`dep.rising-order-sign-class` respectively). Everything else in chapter 20 stays correctly blocked
(`dep.antardasa`, `dep.dasa-last-degree`, `dep.weakest-of-comparator`, `dep.degree-position-quality`,
or `dep.adjudication` for v.30's own invented-weighting refusal). Chapter 3 remains open with 8 of 9
doctrine clusters remaining (`passage:phaladeepika.03.p003` through `.p054`). **Do not re-open
`dep.triped-sign-class`** — a human's reading of a printed word, not an implementation; three
independent sessions (21, 28, and in passing, 30) have confirmed the source does not settle it.
Separately, `Rules/tools/backlog.py` still flags **4 concept entries as newly resolvable** and stale
since `dep.strength` landed in Milestone 22 — `concept:kala-bala-benefic-scope`,
`concept:oja-yugma-fifth-graha`, `concept:strength-criterion-scope`,
`concept:strength-is-not-bhava-strength` — untouched by twelve consecutive milestones now; a future
session should read them before picking a next chapter. `backlog.py` also flags
`passage:phaladeepika.20.p021` (the ch.20 rule-transfer meta-rule) as newly resolvable via
`dep.rule-transfer` — Milestone 31 already noted this requires systematically re-conditioning cards
across six other chapters, out of any single slice's scope; still untouched. **Eight decisions are
still owed by a human**, none blocking any of the above: `concept:moon-nature-criterion` (Milestone
20), `concept:strength-criterion-scope` (Milestone 21), `concept:retrograde-combust-collision`
(Milestone 22), `concept:parallel-of-overloaded` (Milestone 23), `concept:p009-lagna-or-moon-clause`
(Milestone 24), `concept:adhiyoga-distribution-strictness` (Milestone 26), `dep.triped-sign-class`
(Decision 0d, Milestone 28), `Decision 0e` (Milestone 29, which division "the Varga of Mars or Saturn"
means) — none touched by Milestones 34-37.

**Current Git SHA:** `92963d48944b75e09a210245f3ee5af202ffa9be` (parent — Milestone 36's own commit;
this milestone's own commit follows this file's checkpoint)
**Last verified remote SHA (origin/main):** same before this milestone's commit — 0 ahead /
0 behind, working tree clean before this commit
**Last update date:** 2026-09-02

**Current test count (`Engine/tests`):** 596 passing — was 573. The 23 new tests (Milestone 37, in
`Engine/tests/test_chapter_seven_slice_two.py`) cover all ten new cards, at least one positive and one
negative case each, against the project's own real Thanjavur nativity with individual bodies moved
(`Engine.tests.test_strength.place`, the same discipline Milestone 36 established) plus a corrected,
self-contained `lagna()` helper for the cards that need a genuinely different Lagna (unlike the
shallow one in `test_chapter_seven_neechabhanga.py`, this one also recomputes `chart.houses["signs"]`
and every body's own `.house` field, since `in_house`/`in_house_class`/`aspects`/`lord_of_house` all
read those directly rather than deriving them from `ascendant_sign_index` on demand — a latent
staleness risk in the Milestone 36 helper that happened not to matter there because every test using
it re-placed every body its own conditions referenced). Three authoring bugs were caught by failing
assertions during authoring, not shipped: two house-arithmetic errors (Sagittarius, not Scorpio, sits
opposite the point I intended for a malefic-in-the-11th test — corrected after recomputing the
whole-sign house table by hand rather than trusting an earlier miscomputed one) and one test whose
intended "negative" case was not actually negative (a 2nd-house lord placed outside kendra-from-the-Moon
was still correctly satisfying the card's own `any`-of-three-lords first clause via the unmoved,
already-well-placed 11th lord — the card's own logic was right; the test's premise was wrong, and was
replaced with a construction that fails the card's second clause outright, independent of any lord's
placement). **Previous count (Milestone 36):** 573 passing — was 559. The 14 new tests (Milestone 36, in
`Engine/tests/test_chapter_seven_neechabhanga.py`) cover all five Neechabhanga cards: the source's
own worked example reconstructed as a synthetic chart (a real ephemeris nativity with the Lagna and
select bodies overridden, the same discipline `test_strength.py`'s own `place()` helper already
established for edge cases no convenient real birthday produces); a positive and negative case per
card; the Moon's item-1 single-candidate collapse (Scorpio has no classical exalter, confirmed by
construction rather than asserted); item 1 vs. item 4 kept distinguishable on Mercury, where the two
cards' own second candidates differ (Venus vs. Mercury itself); a doctrine-drift guard cross-checking
the cards' own hardcoded per-graha table against live `Doctrine.sign_lord`/`.exaltation` reads; and a
seven-graha "seven exalted grahas fire nothing" negative-discipline sweep. One test file authoring
bug was caught and fixed before commit, not shipped: the condition language's variable-name regex is
lowercase-only (`^\?[a-z][a-z0-9_]*$`), so `?hSaturn` silently matched as a literal rather than a
variable — found by a failing assertion, not by inspection, and fixed by lowercasing every per-graha
variable name across the whole card family. `Engine/tests/test_slice.py`'s own
"chapters already encoded" negative-control assertion, which had named chapter 7 as its example of an
*unencoded* chapter, was updated to name chapter 5 instead — the only pre-existing test this milestone
touched, and only because it is a chapter-agnostic tooling test whose own example became stale by
construction, not evidence of anything wrong in the tooling itself. **Previous count (Milestone 35):**
559 passing — was 555. The 4 new tests (Milestone 35, in
`Engine/tests/test_dasa.py`) are for `chart_mahadasa_timeline`, the one additive plumbing function
this milestone built: agreement with the golden chart's own `PD.19.Dasa.*` claim windows, direct
cross-check against `mahadasa_sequence`, and `[]` on a missing Moon or absent doctrine. Milestone
34's own 19 tests (chapter-20 `PD.20.WealthDasa.Venus`) are unchanged and described in full under
Milestone 34 above. **New this milestone, outside `Engine/tests`:** `Api/tests/` — 24 passing (5
files: health, `/consult` response shape, the live CLI-vs-API regression comparison, `/cases`
against an isolated `tmp_path` root, the full error taxonomy). `Frontend/` (Vitest) — 21 passing
(5 files: birth form, loading/error states, claims explorer, dasa timeline, `ComparisonMode`'s diff
logic as a pure function). Neither suite is counted in this row's own historical figure, which this
table's convention has always scoped to `Engine/tests` — see Milestone 35's own §A accounting.
**Current rule-card counts:** **611 total** · 597 executable (firing) · **14 inert** — Milestone 37
added 10 chapter-7 cards (0 reference, 10 firing); no card was removed, and none of the 14 existing
inert cards changed status (all ten reuse existing predicates on their own literal/existential shapes;
none releases anything that was previously blocked). **Previous count (Milestone 36):** 601 total ·
587 executable · 14 inert — 6 chapter-7 cards added (1 reference, 5 firing).
**Current verification:** **609/611 cards signed off (99.67%, was 599/601 ≈ 99.67%)** — all 10 new
cards signed at authoring time; the same two standing holdouts unchanged (`PD.01.Kalapurusha.Strength`,
`PD.04.Lagna.TripedSign` — untouched, genuine source-level defects, not oversights). A raw-fraction
move within existing rounding, held at 98% in §A.

**Backlog (Milestone 37):** 199 entries (+1 net — `passage:phaladeepika.07.p040` split into a
`resolved` remainder and a newly-deferred `passage:phaladeepika.07.p040-royalfamily`, +1 over the one
entry it replaces; `p020`/`p038`/`p055` each flip in place from `deferred` to `resolved`, no count
change). "Available now" moves 108 → 104 (−4: −3 for the three passages that resolved outright,
`p020`/`p038`/`p055`; −1 for `p039`, re-tagged from `dep.none` to the newly registered
`dep.own-or-benefic-dignity-in-varga`, which is not implemented, so it is no longer counted as
available by ordering alone — `p040-royalfamily`'s own `dep.none` tag keeps the split-off remainder
counted exactly where the original entry already was, a wash). One new dependency registered
(`dep.own-or-benefic-dignity-in-varga`), not implemented, not yet releasing a card.

**Backlog (Milestone 36):** 198 entries (+22 net — +23 new chapter-7 passage entries, −1 the old
blanket `chapter:phaladeepika.07` entry they replace). "Available now" moves 97 → 108 (+11: 12 of the
23 new entries are tagged `dep.none` — vv.6,10,13,14,15,18,19,20,21,24-25, the Neechabhanga
illustration, and the colophon — deferred by ordering/human-reading rather than by any missing
capability, minus the −1 blanket-entry disappearance the split replaced). Three new dependencies
registered (`dep.graha-condition-count`, `dep.digbala`, `dep.parivartana`), none yet implemented, none
yet releasing a card.

**Backlog (Milestone 34, unchanged by Milestone 35 — confirmed by re-running `backlog.py`, identical
output):** 176 entries (+2 — the combined `passage:phaladeepika.20.p025-026-033`
entry split into three: `p025` (deferred), `p026` (resolved), `p033` (deferred), a net +2 over the
one entry it replaced). "Available now" holds at 97 (the split entry was never counted there —
each half still names an unimplemented dependency — so nothing about availability changed).

**Original Milestone 30 note on the backlog:** 159 entries (was 151: +9 chapter-19 passage entries
net of the one chapter entry resolved, +1 dependency implemented in place). "Available now" moves
86 → 92.

**Original Milestone 27 note on the backlog:** 139 entries (was 139 — unchanged in count, one status flip and one
new dependency). `passage:phaladeepika.06.p168` moves to `resolved`. One new dependency,
`dep.seven-graha-sign-count` (`predicate: "seven_graha_sign_count"`, `implemented: true` the
moment `Engine/facts.py` emits it, effort 2 — the smallest predicate dependency in the registry).
No entry in the *backlog* names this dependency as a blocker (it did not exist until this
milestone built it alongside the passage it was built for). "Available now" drops 73 → 72 for the
same accounting reason Milestone 25 and Milestone 26 each gave for their own resolved passage:
p168 stops being counted there once resolved, and nothing else was released by the new
dependency.

**Original Milestone 26 note on the backlog:** 139 entries (was 138). `passage:phaladeepika.06.p175`
moves to `resolved`. One new entry: `concept:adhiyoga-distribution-strictness`, the tracked
judgement call above. No new dependencies: the condition uses predicates (`in_house`,
`in_house_from`) already in the vocabulary. "Available now" drops 74 → 73 for the same reason —
p175 stops being counted there once resolved.

**Original Milestone 25 note on the backlog:** 138 entries (was 138 — unchanged in count, one
status flip). `passage:phaladeepika.06.p202` moves to `resolved`. No new entries and no new
dependencies: every condition uses predicates (`lord_of_house`, `in_house`, `aspects`, `nature`,
`strength`) already in the vocabulary, so nothing was catalogued as newly blocked or newly
released beyond the one resolution itself. "Available now" drops 75 → 74 for the same reason —
p202 stops being counted there once resolved.

**Original Milestone 24 note on the backlog:** 138 entries (was 136). `passage:phaladeepika.06.p009` and
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
| Rule extraction/encoding | 20% | 44% | Phaladeepika chapters 1, 2, **4**, **6 (complete)**, 7 **(slices 1-2)**, 8, 9, 10, **19**, **20 (Mahadasa-scoped slice)** encoded; 609 Phaladeepika cards (+2 Brihat Jataka = 611 in the store) from an estimated ~1,535 total across all 28 Phaladeepika chapters at the measured 0.58 cards/paragraph rate — and that is one book of six. Chapter 4 alone contributed 94, still the densest chapter encoded so far. **Milestone 37 added 10 cards** (0 reference, 10 firing), ten further Raja Yoga configurations from chapter 7's own general material (vv.13, 18, 20(b)-(d), 24, 25) — **held at 44%**: 10 cards against the ~1,535-card estimate is below this table's own rounding, comparable to Milestone 31's own 34-card move only in kind, not in size; chapter 7 remains open (three of its own eight "slice 2" candidates were found not actually ready and correctly left deferred rather than forced through — see this milestone's own §C write-up), so no "chapter now complete" credit applies. **Milestone 36 added 6 cards** (1 reference, 5 firing), the five `PD.07.Neechabhanga.*` cards (vv.26-30) plus one documentary Note card — **held at 44%**: 6 cards against the ~1,535-card estimate is below this table's own rounding, comparable to Milestone 33's own 4-card addition, which also held; chapter 7 itself opens with this milestone rather than closes, so no "chapter now complete" credit applies the way it did for chapter 6 in Milestone 27. **Milestone 34 added 1 card** (0 reference, 1 firing), `PD.20.WealthDasa.Venus` (v.26) — **held at 44%**: 1 card against the ~1,535-card estimate is smaller than every prior addition this row has ever credited, well below this table's own rounding. **Milestone 33 added 4 cards** (0 reference, 4 firing), `PD.20.MiseryDasa.SaturnFourth`/`.JupiterSixth`/`.MarsRahuFifth`/`.DusthanaLords` (v.24 items (1)-(3),(5)) — **held at 44%**: 4 cards against the ~1,535-card estimate is below this table's own rounding, smaller than Milestone 31's own 34-card move and comparable to Milestone 32's own 2-card addition, which also held. **Milestone 32 added 2 cards** (0 reference, 2 firing), `PD.20.Placement.BeneficAdverse`/`.MaleficMiseries` (v.27) — **held at 44%**: 2 cards against the ~1,535-card estimate is below this table's own rounding, the same size as Milestone 26's own 2-card addition, which also held. **Milestone 31 added 34 cards** (1 reference, 33 firing) closing chapter 20's clean Mahadasa-scoped block — **43%→44%**: 34 cards is roughly 2.2% of the ~1,535-card estimate, comparable to Milestone 25's own 23-card (1.5%) move that last moved this row, and larger than every card-count addition since. The chapter's Antardasa-relational, transit, weakest-of-comparator, degree-position and sign-class-gated remainders stay unencoded by design (no printed arithmetic for the first, no `dep.transit`/comparator/degree-predicate for the rest) and are not counted as progress here. **Milestone 27 added 8 cards** (one reference, seven firing) closing the chapter's last passage, the seven-planets-in-N-signs family — **held at 43%**: 8 cards against the ~1,535-card estimate is smaller than Milestone 25's 23-card move and closer to Milestone 24's 3 and Milestone 26's 2, both of which fell below this table's rounding. **Chapter 6 is now fully encoded on its testable doctrine** — every remaining deferred passage in it is tier-3 apparatus or a standing human-decision concept, not unencoded doctrine — a qualitative completion this row's own text records even though the percentage does not move, the same posture Milestone 26 took for its own two-card addition. **Milestone 26 added 2 cards** (one reference, one firing) closing the chapter's Adhiyoga passage — held at 43% for the same reason. **Milestone 25 added 23 cards** (one reference, twenty-two firing) closing the chapter's twelve-yoga dusthana-lord cluster and its Parashara counter-doctrine — **42%→43%**: 23 cards is roughly 1.5% of the ~1,535-card estimate, small but not below this table's own rounding the way Milestone 24's 3 cards were, and it is the first time in several milestones a chapter has moved from "partial" to "essentially complete." **Milestone 24 added 3 cards (1 reference, 2 firing) and rewrote 5 existing ones' conditions** — held at 42% then: three cards against the same estimate is below what rounding can register. |
| Reasoning engine capability | 15% | 67% | Stages 0, 1, 2, **4**, 6, **7 (reading half)**, 9, 10 implemented; Stages 3 and 5 (yogas/houses as first-class computation) not built as dedicated stages; **Stage 7's weighting half deliberately does not exist and is not scheduled**; transit and ashtakavarga calculators still absent, and no *numeric* strength calculator — the source withholds the arithmetic one would need (`dep.shadbala-arithmetic`). **Milestone 37 built zero new engine capability**, by design: all ten new cards reuse `vargottama`, `strength`, `aspects`, `nature`, `in_house`, `in_house_class`, `in_house_from`, `lord_of_house`, `dignity` and `lagna_sign` exactly as declared — held at 67%, not raised, the same "same mechanism, more instances" posture this row has held since Milestone 24. One new dependency was registered (`dep.own-or-benefic-dignity-in-varga`, for v.19's own "own or benefic Varga" gap), not built. **Milestone 36 built zero new engine capability**, by design: every Neechabhanga card reuses `dignity`, `in_house_class`, `in_house_from`, `in_house` and `aspects` exactly as-is, existentially quantified over a fixed graha set the same way `PD.20.MiseryDasa.DusthanaLords` already existentially quantifies over a fixed house set — held at 67%, not raised, the same "same mechanism, more instances" posture this row has held since Milestone 24. Three genuinely new dependencies were registered (`dep.graha-condition-count`, `dep.digbala`, `dep.parivartana`) for chapter 7's own remaining verses, none built. **Milestone 33 built one small new predicate, `mahadasa_ordinal`** (ch. 20 v.24: a graha's
1-based position in the birth-fixed mahadasa sequence, counted from the dasa the native was born
in) — held at 67%, not raised: `MahadasaPeriod.ordinal` was already computed by `dep.dasa`
(Milestone 30) for the window every dasa card already carries, and this milestone's own extractor
change is one extra `make_fact` call exposing that pre-existing field as its own queryable fact,
smaller in kind than `dasa_disposition`'s own new verdict-derivation logic and just as clearly the
same "same mechanism, more instances" case this row has held on since Milestone 24. **Milestone 31
built one small new predicate/extractor, `dasa_disposition`** (ch. 20 v.14's own local strong/weak-like criterion, kept deliberately distinct from `strength`) — held at 67%, not raised: it is architecturally the same *kind* of capability `strength` already is (a doctrine-read verdict extractor, the identical shape, not a new stage or combinator), the same "same mechanism, more instances" case Milestone 24 first declined to credit and every milestone since has held this row on consistently. No Antardasa mechanism was built — confirmed by reading all 63 verses of ch. 20 directly that no order or duration formula for the nine sub-periods is printed anywhere in ch. 19 or ch. 20, so `dep.antardasa` stays unimplemented by design, not by oversight. **65→67 in Milestone 30: `dep.dasa` built** — a genuine new calculator (one of the four this row used to name by name as missing; varga was narrowly built in Milestone 29, dasa narrowly here — mahadasa only, no antardasa, since no antardasa formula is printed anywhere in the source), and the first time any claim in this store carries a date window rather than being timelessly true or false of a static placement (`Claim.window`, additive). Not higher: mahadasa only, not the general capability; transit and ashtakavarga are still unbuilt; Stages 3/5 are still not dedicated stages. **Raised 60→65 in Milestone 23: Stage 7's representation half exists** — every relationship the store declares between two cards is read, typed and reported with both sides quoted, and an `unresolved` outcome is a finished answer rather than a placeholder. Not higher, because the half that would let the engine *choose* between two source-backed claims is absent by design: no encoded source supplies a rule for choosing, and the only precedence applied anywhere in the engine is the one verse 4 states in its own sentence. **Previously raised 52→60 in Milestone 22: Stage 4 exists and P0-1 is closed** — every chart now produces graha strength verdicts, read from chapter 4's own cards, and the largest "born inert" tax on every future chapter is paid. Not higher, for three reasons that are the source's and not the schedule's: it is graha strength only (no Bhava Bala — the components are withheld), it is a binary verdict and not an order (no `strongest`), and Stage 3 (yogas) and Stage 5 (houses) are still not dedicated stages. **Previously raised 45→52 in Milestone 20**, the first increase from real capability rather than bookkeeping: P0-2 is closed (all 9 grahas now carry a `nature` fact, so the 22 benefic-conditioned cards can fire), and the first piece of Stage 7 exists — per-graha authority attribution and cross-book corroboration in `_resolve_nature`. Still 52 and not higher because Stage 7's *hard* half — adjudicating authorities that actually disagree — remains unbuilt and deliberately so (§K, P1-3). |
| Contradiction handling | 10% | 82% | Competing authorities are preserved via `contradicts`/`extends` links and dual cards (e.g. PD.01 rising-sign dispute, PD.09 dignity dispute) — the mechanism works and is used repeatedly, but Stage 7 adjudication (weighing contradictions against each other) does not exist yet. **Milestone 33 adds a third real `contradicts` cluster** — `PD.20.MiseryDasa.DusthanaLords` (v.24's unconditional 6th/8th/12th-lord misery dasa) against `PD.20.Strong.House6`/`.House8`/`.House12` (vv.7/9/13's own strength-gated good-dasa cards for the same three house lords) — held at 82%, not moved, for the identical reason Milestone 25's own second cluster (ch. 6's Harsha/Sarala/Vimala vs. Parashara) held this row: the milestone reused Stage 7's existing reading mechanism on a new pair of cards, it did not build a new relationship type or a weighting mechanism. **71→82 in Milestone 23**, the largest single move this category has had, and it is a *reading* gain rather than a mechanism gain: the `contradicts`/`extends`/`parallel_of` links were being written faithfully into the store and read by nothing, so no consultation had ever surfaced one. All four relationship types now reach the reader with card id, book, chapter, verse, printed page and both sides' own words. It also repaired a live defect — on 83% of 720 scanned charts Part 3 was printing a verse and its own translator's refutation as *agreeing*, under a heading reading "Terms that recur without contradiction". Not higher for two stated reasons: the engine still cannot choose where the source does not, and `parallel_of` cannot distinguish agreement from a variant reading (`concept:parallel-of-overloaded`), so cross-book *corroboration* of a yoga still cannot be claimed. **68→71 in Milestone 22:** the first *chart-dependent* refusal. A graha that is both retrograde and combust is called strong by ch. 4 v. 5 and weak by v. 4, and the extractor emits no verdict for it, reports the collision by name in the consultation's own "doctrine read, but not complete" section, and lets every rule about its strength correctly not fire. Earlier contradiction handling was static — two cards linked at encoding time; this one only exists on charts that satisfy both. |
| Provenance/auditability | 10% | 98% | Every card is byte-exact hash-verified against the corpus on every run; `verify.py` enforces this as a build gate. **609/611 cards signed off (99.67%, was 599/601 ≈ 99.67%) after Milestone 37** — all ten new cards signed at authoring time, the same two holdouts unchanged; a raw-fraction move within existing rounding, held at 98%. **599/601 cards signed off (99.67%, was 593/595 ≈ 99.66%) after Milestone 36** — all six new cards signed at authoring time, the same two holdouts unchanged; a raw-fraction move within existing rounding, held at 98%. **593/595 cards signed off (99.66%, was 592/594 ≈ 99.66%) after Milestone 34** — the one new card signed at authoring time, the same two holdouts unchanged; a raw-fraction move within existing rounding, held at 98%. **592/594 cards signed off (99.66%, was 588/590 ≈ 99.66%) after Milestone 33** — all four new cards signed at authoring time, the same two holdouts unchanged; a raw-fraction move within existing rounding, held at 98%. **588/590 cards signed off (99.66%, was 586/588 ≈ 99.7%) after Milestone 32** — both new cards signed at authoring time, the same two holdouts unchanged; a raw-fraction move within existing rounding, held at 98%. **586/588 cards signed off (99.7%, was 552/554 ≈ 99.6%) after Milestone 31** — all 34 new chapter-20 cards signed at authoring time, the same two holdouts unchanged; a raw-fraction move within existing rounding, held at 98%. `extraction.verified_by` previously covered **501/504 cards (99.4%**, was 4/404) via `Rules/tools/review.py`: 271 structural cards signed off automatically (no interpretive layer to review — the byte-exact check already is the complete verification), 230 signed off by an actual human(+Claude) reading pass across chapters 1, 2, 4, 6, 8, 9 and 10 — including 33 of chapter 4's and, as of Milestone 24, the three new and five rewritten chapter 6 cards, re-signed by hand because their encoding involved a real judgement. The interpretive queue is closed; the 3 unsigned cards are deliberate, documented defect holdouts, not unreviewed cards. Not 100% because those three defects are real and still open. **97→98 in Milestone 23:** every adjudication carries the full provenance of both parties and is re-checked by Stage 9 (`verify_adjudications`), so a conclusion *about* sources can be walked back to them the way a claim can; and a relationship link naming a card that does not exist now fails the build, because a link the engine reads is a link whose typo silently costs a reported contradiction. |
| Test coverage | 10% | 79% | **Milestone 37: 596 tests (was 573), +23 (~4%)** — held at 79%, not moved: comparable to Milestone 32's own +19 and Milestone 33's own +27, both of which held, smaller than the deltas that have moved this row (Milestones 22-23, 30); every one of the ten new cards gets its own positive and negative case, against the same real Thanjavur nativity Milestone 36 established, extended with a corrected `lagna()` helper that also recomputes `chart.houses["signs"]` and every body's own `.house` field (a latent staleness gap in Milestone 36's own shallow helper, caught here rather than shipped again). **Milestone 36: 573 tests (was 559), +14 (~2.5%)** — held at 79%, not moved: comparable to Milestone 24's own +7 (~2%) and Milestone 26's own +12, both of which held, smaller than the deltas that have moved this row (Milestones 22-23, 30); the source's own worked example (v.26's Note, Saturn debilitated in Aries) reconstructed as a synthetic chart is the same *kind* of evidence Milestone 30's ch.19 v.3 worked-example oracle already established this row on, not a new technique. **Milestone 34: 555 tests (was 536), +19 (~3.5%)** — held at 79%, not moved: all 19 in `test_chapter_twenty.py` for one card's five-conjunct condition, comparable to Milestone 32's own +19, smaller than the deltas that have moved this row (Milestones 22-23, 30); the genuine ephemeris search (a real positive instant per named house, plus a real negative control) is the same *kind* of evidence Milestone 22's own chart-space search already established this row on, not a new technique. **Milestone 33: 536 tests (was 509), +27 (~5.3%)** — held at 79%, not moved: comparable to Milestone 31's own +21 (~4.5%) and Milestone 27's own +28 (~7.7%, itself held), smaller than the deltas that have moved this row (Milestones 22-23, 30); the real-instant search for the two ordinal cases the DEMO chart does not exercise is the same *kind* of evidence Milestone 22's own chart-space search already established this row on, not a new technique. **Milestone 32: 509 tests (was 490), +19 (~3.9%)** — held at 79%, not moved: comparable to Milestone 24's own +7 (~2%) and Milestone 26's own +12, smaller than the deltas that have moved this row (Milestones 22-23, 30). **Milestone 31: 490 tests (was 469), +21 (~4.5%)** — held at 79%, not moved: smaller proportionally than the deltas that have moved this row (Milestones 22-23, 30), comparable to Milestone 24's own +7 (~2%) and Milestone 27's +28 (~7.7%, itself held), even though the new file pins a genuine negative-discipline set (the collision case reported not dropped, no numeric verdict ever, the trikona/upachaya house-list regressions) matching `test_strength.py`'s own established pattern rather than a new technique. **76→79 in Milestone 30:** 469 tests (was 418), +51 (~12.2%) — comparable to or larger than the deltas that moved this row 68→72→76 in Milestones 22-23 — including a genuine new technique for this store: a real classical worked example (ch. 19 v.3's Notes) used as a numeric oracle to sub-day precision, not a hand-built or independently-derived synthetic table. 270 tests (was 250), growing with every milestone, covering rule structure, engine extractors, variable binding, overrides, the verification tool itself, and now chapter 4's encoding (`Engine/tests/test_chapter_four_strength.py`, +20 tests: the two authorities never merged, the Mars row's printed defect pinned as printed, the unquantified components pinned as unquantified, and the verses-4-and-5 verdict set pinned as the only source Stage 4 may read); no dedicated end-to-end regression suite across the full corpus of encoded chapters yet. **Milestone 24: 341 tests (was 334)**, +7 in `Engine/tests/test_chapter_six_strength.py` and `test_slice.py`/`test_adjudication.py` fixture updates — held at 76%, not moved: a 2% test-count increase focused on one chapter's encoding is smaller than the swings that have moved this row before, even though the specific finding it pins (a card confirmed structurally unfireable, not merely untested) is a genuine methodological addition. **72→76 in Milestone 23:** 334 tests (was 302), the 32 new ones in `Engine/tests/test_adjudication.py` — and, for the first time in this project, the suite was checked by *mutating the module under test*: four deliberate breakages (directional link reading, treating every `parallel_of` as a second authority, resolving what should stay unresolved, deleting the strength collision's refusal) were each confirmed to fail it, and the second one initially did **not**, which exposed a test that checked the discriminator's input rather than its output. **68→72 in Milestone 22:** 302 tests (was 271), the 30 new ones in `Engine/tests/test_strength.py` covering the extractor's doctrine reading, its calculation on placed edge cases, the retrograde/combust refusal, determinism, and — the ones that matter most — the negatives: no fact carries a number, a component is not a verdict, retrogression does not make the nodes strong, and the doctrine dies with its cards. |
| End-to-end validation | 5% | 36% | CLI produces full 3-part consultations and has been spot-checked against real charts per milestone; no systematic charted validation set (Phase 6 of `Phases.txt`) exists yet. **Milestone 24:** 2,176 real nativities (four cities, 1950-2010) run end to end with **zero pipeline or verification failures** — held at 36%, not moved: the sweep confirms the milestone's own findings (a 29.2% Mahapurusha firing rate, zero natural occurrences of either Duryoga card, an unchanged 13.6% collision rate) without adding a new *kind* of end-to-end evidence beyond what Milestones 22-23 already established this row on. **33→36 in Milestone 23:** 720 nativities across four cities and sixty years were run end to end with **zero pipeline or verification failures**, and the frequency of each relationship type was measured rather than asserted — which is how the 83% figure above is known. Still not Phase 6: nothing here checks whether a prediction is *correct*. **30→33 in Milestone 22:** the first time the project *searched* a chart space rather than spot-checking one nativity — 880 real birth instants were scanned to find a chart for each newly-activated card and to confirm each one actually fires. That is not Phase 6, but it is the first evidence that an activated card is not merely well-formed. |
| Multi-book corroboration | 3% | 30% | **No longer zero (Milestone 20).** Brihat Jataka now has 2 rule cards, and cross-book agreement is not only assessable but implemented and surfaced: 4 grahas' natures are corroborated by both books, and the consultation reports which claims rest on one authority and which on two. Scored 25%, not higher, because corroboration exists for exactly one relation (`graha_nature`) out of the whole store, and the second book has 2 cards against the first book's 499. **25→30 in Milestone 23:** three further books — Jataka Parijata, Saravali and Uttarakalamrita — now reach the reader in their own words, on 92% of charts, wherever the translator reports them on a doctrine the chart activates. Only +5, and deliberately: those statements are reported as *a second authority on the same doctrine* and **not** as corroboration, because one of them states a materially different condition for the same yoga and the store's `parallel_of` link does not record which kind it is. |
| Production safety/reliability | 1% | 50% | Groundedness verification (Stage 9) refuses to emit ungrounded output; no rate limiting, error-recovery, or production deployment hardening attempted (not yet in scope). |
| CLI/API/user-facing readiness | 1% | 60% | Working CLI (`Engine/cli.py`) produces real consultations. **Milestone 35 adds a working local API (`Api/`, FastAPI) and a working local developer UI (`Frontend/`, React) covering all 13 required inspection views, verified end-to-end in a real browser** — the row's own stated gap ("no API, no UI") is half-closed. Not higher: no packaging/installer, no authentication or multi-user surface, no production deployment, no external/systematic user testing. |

**Overall Production Readiness: 0.15×25 + 0.10×77 + 0.20×44 + 0.15×67 + 0.10×82 + 0.10×98 +
0.10×79 + 0.05×36 + 0.03×30 + 0.01×50 + 0.01×60 = 60.00% ≈ 60%**

**Milestone 37: 60.00% → 60.00%, held.** No row moved. Every row's own delta this milestone (10 new
firing cards against the ~1,535-card estimate; zero new predicates/stages (one new dependency
registered, none built); zero new relationship links; a raw-fraction provenance move,
599/601→609/611; +23 tests, ~4%) falls below that row's own established rounding threshold — the
same posture Milestones 26, 32, 34 and 36 each took for their own small, correct, fully-verified
additions. Corpus completeness, Source verification, Contradiction handling, End-to-end validation,
Multi-book corroboration, Production safety/reliability and CLI/API/user-facing readiness are
untouched outright (no book, corpus-verification pass, relationship link, chart-space sweep, second
book, safety mechanism, or API/UI work this milestone).

**Milestone 36: 60.00% → 60.00%, held.** No row moved. Every row's own delta this milestone (6 new
cards against the ~1,535-card estimate; zero new predicates/stages; zero new relationship links; a
raw-fraction provenance move, 593/595→599/601; +14 tests, ~2.5%) falls below that row's own
established rounding threshold — the same posture Milestones 26, 32 and 34 each took for their own
small, correct, fully-verified additions. Corpus completeness, Source verification, Contradiction
handling, End-to-end validation, Multi-book corroboration, Production safety/reliability and
CLI/API/user-facing readiness are untouched outright (no book, corpus-verification pass, relationship
link, chart-space sweep, second book, safety mechanism, or API/UI work this milestone).

**Milestone 35: 59.80% → 60.00% ≈ 60%.** Exactly one row moved: "CLI/API/user-facing readiness"
40→60 (+0.20 pts on the 1%-weighted row), and 59.80 + 0.20 = 60.00 agrees with the recomputed
expression above — the headline rounded figure does not visibly move, because this row's weight is
the smallest in the table. Every other row held for a stated reason, all given in full in Milestone
35's own write-up (§C): no card was added, removed, or reworded (Corpus completeness, Rule
extraction, Multi-book corroboration, Provenance/auditability all untouched); the one engine change
(`Engine.dasa.chart_mahadasa_timeline`) is a pure refactor of arithmetic `activate.py` already ran,
not new reasoning capability (Reasoning engine capability untouched); no relationship type or card
changed (Contradiction handling untouched); "Test coverage" is scoped to `Engine/tests` by this
table's own established convention, and that suite's own +4 tests (all *for* the one refactored
helper) is smaller than every delta that has moved this row before; "End-to-end validation" is
scoped to chart-space evidence about the doctrine, not the presence of a UI — the new `Api`/
`Frontend` test suites (24 + 21 passing) and the real-browser verification are credited above under
"CLI/API/user-facing readiness" instead, not double-counted here.

**Milestone 33: identical expression and result to Milestone 32's — 59.80% ≈ 60%.** No category
score moved. "Rule extraction/encoding" — 4 cards (v.24 items (1)-(3)/(5)) against the ~1,535-card
estimate is below this table's own rounding, comparable to Milestone 32's own 2-card move, which
also held; "Reasoning engine capability" — the one new predicate, `mahadasa_ordinal`, is a pure
lookup into a value `dep.dasa` already computed (`MahadasaPeriod.ordinal`), architecturally smaller
than `dasa_disposition`'s own new verdict logic and just as clearly the "same mechanism, more
instances" case this row has held since Milestone 24; "Contradiction handling" — three new
`contradicts` links, but the existing reading mechanism applied to a new pair, not a new
relationship type or a weighting mechanism, the same reasoning Milestone 25's own second cluster
held this row on; "Provenance/auditability" — 592/594 signed (99.66%, was 588/590 ≈ 99.66%) with
the same two holdouts, a raw-fraction move within existing rounding; "Test coverage" — +27 tests
(~5.3%) is smaller than the deltas that have moved this row (Milestones 22-23, 30); "End-to-end
validation" — a direct ephemeris search for two ordinal cases the standing DEMO chart does not
exercise, each run through the full pipeline with `verification.ok` confirmed, is the same *kind*
of evidence this row already credits (a real chart producing the claim the doctrine predicts), not
Phase 6 correctness validation; "Multi-book corroboration" — unaffected, v.24 is Phaladeepika-only.
Corpus completeness, source verification, production safety and CLI/API readiness are all
untouched by this milestone.

**Milestone 34: identical expression and result to Milestone 33's — 59.80% ≈ 60%.** No category
score moved. "Rule extraction/encoding" — 1 card (v.26) against the ~1,535-card estimate is smaller
than every prior addition this row has credited; "Reasoning engine capability" — untouched, zero
new predicates or engine code; "Contradiction handling" — untouched, v.26 records no relationship;
"Provenance/auditability" — 593/595 signed (99.66%, was 592/594 ≈ 99.66%) with the same two
holdouts, a raw-fraction move within existing rounding; "Test coverage" — +19 tests (~3.5%) is
smaller than the deltas that have moved this row (Milestones 22-23, 30); "End-to-end validation" —
a direct ephemeris search finding three real positive instants and one real negative control for
v.26's own condition, each run through the full pipeline with `verification.ok` confirmed, is the
same *kind* of evidence this row already credits, not Phase 6 correctness validation;
"Multi-book corroboration" — unaffected, v.26 is Phaladeepika-only. Corpus completeness, source
verification, production safety and CLI/API readiness are all untouched by this milestone.

**Milestone 32: identical expression and result to Milestone 31's — 59.80% ≈ 60%.** No category
score moved. "Rule extraction/encoding" — 2 cards (v.27's two placement cards) against the
~1,535-card estimate is below this table's own rounding, the same size as Milestone 26's own
2-card move, which also held; "Reasoning engine capability" — no new predicate or extractor was
built, by design: v.27 states no local disposition criterion of its own the way v.14 does, so it
was encoded directly with the existing `nature`, `dignity`, `in_house` and `mahadasa_lord`
predicates, zero new mechanism; "Contradiction handling" — v.27 carries no Notes and names no
competing authority, so no new `contradicts`/`parallel_of` link was drawn; "Provenance/
auditability" — 588/590 signed (99.66%, was 586/588 ≈ 99.7%) with the same two holdouts, a
raw-fraction move within existing rounding; "Test coverage" — +19 tests (~3.9%) is smaller than
the deltas that have moved this row; "End-to-end validation" — one more real-chart CLI inspection
(the three inimically-placed malefics on the standing Thanjavur demo chart, each firing
`PD.20.Placement.MaleficMiseries` under the correct mahadasa window) is the same *kind* of evidence
this row already credits, not Phase 6 correctness validation; "Multi-book corroboration" —
unaffected, v.27 is Phaladeepika-only. Corpus completeness, source verification, production safety
and CLI/API readiness are all untouched by this milestone.

**Milestone 31: 59.60% → 59.80% ≈ 60%.** Exactly one row moved: "Rule extraction/encoding" 43→44
(+0.20 pts), and 59.60 + 0.20 = 59.80 agrees with the recomputed expression above. Every other row
held for a stated reason: "Reasoning engine capability" — `dasa_disposition` is architecturally
the same *kind* of capability `strength` already is (a doctrine-read verdict extractor), not a new
stage, the "same mechanism, more instances" case this row has declined to credit since Milestone
24; "Contradiction handling" — the two genuine source tensions this milestone investigated (the
ch.1/ch.20 "trikona" discrepancy, v.43-44's apparent conflict with vv.2-21) were both resolved by
reading, not left as unresolved `contradicts` links, so no new relationship was added to the store;
"Provenance/auditability" — 586/588 signed (99.7%, was 552/554 ≈ 99.6%) with the same two holdouts,
a raw-fraction move within existing rounding; "Test coverage" — +21 tests (~4.5%) is smaller than
the deltas that have moved this row; "End-to-end validation" — one real named-chart CLI inspection
is the same *kind* of evidence this row already credits, not Phase 6 correctness validation;
"Multi-book corroboration" — unaffected, chapter 20's doctrine is Phaladeepika-only. Corpus
completeness, source verification, production safety and CLI/API readiness are all untouched by
this milestone.

**Previous figure (Milestone 30): 0.15×25 + 0.10×77 + 0.20×43 + 0.15×67 + 0.10×82 + 0.10×98 +
0.10×79 + 0.05×36 + 0.03×30 + 0.01×50 + 0.01×40 = 59.60% ≈ 60%**

**Milestone 30: 59.00% → 59.60% ≈ 60%.** Two rows moved, cross-checked by delta: reasoning
capability 65→67 (+0.30 pts) and test coverage 76→79 (+0.30 pts), sum 0.60, and 59.00 + 0.60 =
59.60 agrees with the recomputed expression above. Every other row held for a stated reason: "Rule
extraction/encoding" — 14 net new cards (13 chapter-19, +1 from the `PD.09.Dignity.Inimical`
split) against the ~1,535-card estimate is comparable to Milestone 27's own 8-card move, which
held; "Contradiction handling" — one new `contradicts` pair, but documentary only (neither side
ever fires as a claim, so it never reaches `Engine.adjudicate`'s output), not a new relationship
type or mechanism, the same "reused, not new" reasoning that has held this row since Milestone 25;
"Provenance/auditability" — 552/554 signed (99.6%, was 536/540 ≈ 99.3%) with the same two
holdouts, a raw-fraction move within existing rounding; "End-to-end validation" — a boundary-value
ephemeris sweep and one real named-chart CLI inspection is the same *kind* of evidence this row
already credits, not Phase 6 correctness validation; "Multi-book corroboration" — unaffected, dasa
doctrine is Phaladeepika-only in the current corpus. Corpus completeness, source verification,
production safety and CLI/API readiness are all untouched by this milestone.

**Previous figure (before Milestone 30): 0.15×25 + 0.10×77 + 0.20×43 + 0.15×65 + 0.10×82 + 0.10×98 +
0.10×76 + 0.05×36 + 0.03×30 + 0.01×50 + 0.01×40 = 59.00% ≈ 59%**

**Milestone 27: identical expression and result to Milestone 26's — 59.00% ≈ 59%.** No category
score moved, each checked and held for a stated reason. "Rule extraction/encoding": 8 cards is
smaller than Milestone 25's 23-card move (see that row's own text); chapter 6's completion is
real and stated in the row's own text, but a qualitative fact is not itself a score input.
"Reasoning engine capability": one new predicate (`seven_graha_sign_count`, `dep.seven-graha-
sign-count`, effort 2) reusing an existing literal-match mechanism (`occupant_count`'s own) is not
a new stage or combinator, the same "same mechanism, more instances" case Milestone 24 declined
to credit and Milestone 26 held for the same reason. "Contradiction handling": `parallel_of` was
used again for a sibling family, not a new relationship type or a new `contradicts` pair, so this
holds exactly as every milestone since 23 that reused the existing relationship types has held it.
"Test coverage": 391 tests (was 363), +28 (~7.7%) — larger than Milestone 26's own +12 but the
same *kind* of test this suite already runs throughout (structure, isolated-primitive, boundary,
real-chart), not a new verification technique the way Milestone 23's mutation testing was, so it
does not clear the bar that moved this row 68→72→76. "End-to-end validation": a 219,132-instant
direct ephemeris sweep is methodologically new (centuries rather than decades, no birth record
built at all) but is still the same *kind* of finding — a real chart producing the claim the
doctrine predicts — Milestones 22-24 already established this row on, so it holds per the
discipline Milestone 24 itself applied to its own larger, but not newly-kinded, 2,176-chart sweep.
"Provenance" holds at the same 99.4% raw fraction (534/537, was 526/529) with the same three
holdouts; the new reference card was auto-signed structural and all seven firing cards were
signed by hand at authoring time, exactly as Milestone 26's two cards were.

**Milestone 28: identical expression and result — 59.00% ≈ 59%, held for the simplest reason yet:
nothing was built, encoded, or changed.** This was a read-only investigation of one dependency
(`dep.triped-sign-class`) that concluded, with new corroborating source evidence, the same thing
Milestone 21 already concluded: the source does not resolve the term, so the card stays inert and
no capability was implemented. No row in this table moves on an investigation whose outcome is
"confirmed still unresolved" — not "Rule extraction/encoding" (0 cards), not "Reasoning engine
capability" (0 predicates), not "Test coverage" (0 tests), not "Provenance" (534/537, unchanged). A dependency being
*investigated* is not the same as it being *cleared*, and the score must not move to reward the
investigation itself.

**Milestone 26: identical expression and result to Milestone 25's — 59.00% ≈ 59%.** No category
score moved. Two cards closing one small passage is smaller than Milestone 24's own 3-card
addition, which itself fell below "Rule extraction/encoding"'s rounding — see that row's own
text. No new engine mechanism was built (both predicates already existed) and no new
`contradicts` pair was drawn, so "Reasoning engine capability" and "Contradiction handling" hold
exactly as Milestone 24 held them for the same reason. Twelve new tests (~3%) is the same order
of magnitude as Milestone 25's own ten (which did not move "Test coverage") and Milestone 24's
seven. The real-chart sweep (~4,500 nativities) is the same *kind* of evidence Milestones 23-25
already established "End-to-end validation" on, not a new kind — and, notably, it found *nothing*
this time (no naturally-occurring "both frames" instance), which is itself informative but is not
a new kind of finding this row has not already credited. Provenance holds at the same 99.4% raw
fraction with the same three holdouts, both new cards signed by hand.

Recomputed from the table, not incremented. **Exactly one category score moved in Milestone 25:
"Rule extraction/encoding" 42→43** (+0.20 pts), for the reasons given in that row itself — 23
cards is small against the ~1,535-card estimate but not below this table's own rounding, and
chapter 6 moved from partial to essentially complete. Every other row was checked and held for a
stated reason: "Reasoning engine capability" and "Contradiction handling" did not move because no
new engine mechanism was built — the milestone reused Stage 7's existing reading layer
(Milestone 23) on a second doctrine cluster, exactly the "same mechanism, more instances" case
Milestone 24 itself declined to credit; "Test coverage" (+10 tests, ~3%) did not clear the bar
the swings that moved that row in Milestones 22-23 did, matching Milestone 24's own +7-test
precedent; "End-to-end validation" grew (a ~4,500-chart sweep measuring the new family's firing
rates and the new relationship-type frequencies) but is the same *kind* of evidence Milestone 23
already established this row on, not a new kind, so it holds exactly as Milestone 24's own
2,176-chart sweep did; "Provenance" holds at the same 99.4% raw fraction with the same three
holdouts, all 23 new cards signed by hand. This is the same discipline Milestone 23 applied when
it declined to credit "Rule extraction" for links the encoders had already written down, and
Milestone 24 applied when it recorded real methodological work without inflating an adjacent row.

Movement from 56% (Milestone 22) to 59.00% is +3 points across seven categories: contradiction
handling 71→82 (+1.10 pts), reasoning capability 60→65 (+0.75), test coverage 72→76 (+0.40), end-
to-end validation 33→36 (+0.15), multi-book corroboration 25→30 (+0.15), provenance 97→98
(+0.10), rule extraction 42→43 (+0.20, Milestone 25 only). Sum of deltas 2.85, and 56.15 + 2.85 =
59.00, which agrees with the expression above — the two are cross-checked here precisely because
§A's own history contains four milestones of a figure that did not.

**Previous figure (Milestone 24):** identical expression and result to Milestone 23's —
58.80% ≈ 59%. No category score moved: three cards and five rewritten conditions were below
what "Rule extraction/encoding" registers, and no new engine mechanism was built, by design, so
"Reasoning engine capability" and "Contradiction handling" could not move either.

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
| Phase 2 | Reasoning engine architecture | Core MVP complete; extensions ongoing | 66% | Stages 0,1,2,6,**7 (reading half)**,9,10 fully implemented (`Engine/chart.py`, `facts.py`, `activate.py`, `render.py`, `pipeline.py`). **14** fact extractors implemented (`Engine/facts.py`): lordship, sign classes, house classes, graha classes, aspects, combustion, dignity, dignity-friendship, occupant count, graha frame, conjunction, nature, nature occupancy, **strength** (Milestone 22). **Stage 4 (graha strength) now exists**, as a verdict extractor rather than a calculator — the source withholds the arithmetic a Shadbala Pinda would need. **Stage 7's reading half now exists** (`Engine/adjudicate.py`, Milestone 23), so Stages 3 and 5 (yoga/house computation as dedicated stages) are the largest remaining items — see `dep.varga`, `dep.dasa`, `dep.ashtakavarga`, `dep.transit`, `dep.vargottama`, `dep.upagraha` in `Rules/deferred.json`, all currently `implemented: false`; `dep.strength` and `dep.adjudication-representation` are `implemented: true`, and `dep.adjudication` (weighting) is outstanding by design. `dep.dasa` (Milestone 30) and `dep.dasa`'s own small sibling `dasa_disposition` (Milestone 31, ch. 20 v.14's local criterion, not a new stage) are also now implemented; `dep.antardasa` was formally registered (Milestone 31) as `implemented: false` -- no order/duration arithmetic for the nine sub-periods is printed anywhere in ch. 19 or ch. 20, confirmed by two independent full readings. | ~~Build `dep.strength`~~ **done, Milestone 22**. ~~Build the adjudication representation~~ **done, Milestone 23**. ~~Build `dep.varga`, `dep.dasa`~~ **done, Milestones 29-30**. Build `dep.ashtakavarga`, `dep.transit`. |
| Phase 3 | Classical Knowledge Extraction | In progress | 36% | 586 cards from Phaladeepika chapters 1, 2, **4**, **6 (complete on testable doctrine, Milestone 27)**, 8, 9, 10, **19**, **20 (Mahadasa-scoped slice, Milestone 31)** of 28 total chapters, plus 2 from Brihat Jataka ch. 2. Estimated ~1,535 total cards across all 28 Phaladeepika chapters at the measured 0.67 cards/paragraph rate (`Reports/PHASE3_PLAN.md`), so 586/1535 ≈ 38% of just this one book, before the rest of Brihat Jataka or the 4 unconverted books are touched at all. | Continue chapter-by-chapter encoding (ch. 3, 5, 7, 11-18, 21-28 — chapter 6 needs no further Phase 3 work); chapter 20's own remainder (Antardasa-relational, transit, weakest-of, degree-position and sign-class clusters) is individually tracked in `Rules/deferred.json`, not further Phase 3 work until the blocking capabilities exist; extend Brihat Jataka extraction; human sign-off is no longer the bottleneck (586/588, see §K P1-1). |
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

### Milestone 25 — Chapter 6's twelve dusthana-lord yogas, and Stage 7's second contradiction cluster

**Phase:** 3 (knowledge), exercising Phase 4's existing adjudication mechanism (Milestone 23)
**Scope:** one new reference card, twenty-two new firing cards, one existing card's note/link
updated, one `Rules/deferred.json` entry resolved
**Status:** COMPLETE
**Completion:** 100% of the passage's testable clauses; see "What was deliberately not built"
**Commit:** this milestone's own commit (see `git log`)
**Remote:** VERIFIED

**Source-first reconnaissance.** `passage:phaladeepika.06.p202` (vv.57-69, printed pp.78-82) was
read directly from `Knowledge/phaladeepika.md` (paragraphs 202-232 of chapter 6, located the same
way `Rules/tools/backlog.py::paragraphs()` does, not by trusting the deferred.json paraphrase),
not from the backlog's summary alone. Verse 57 states one template, ambiguously worded in
translation: *"If the lords of the houses from the Lagna onwards are in the 6th, 8th or the 12th.
or If the houses are occupied or aspected by malefics, 12 kinds of yogas are formed from the
houses commencing from the Lagna."* Read literally this could mean either "house N's own lord
goes to a dusthana" or "a dusthana lord lands in house N" — a real interpretive fork, not
resolved by guessing. It was settled by the passage's own later verses rather than imported
convention: v.63 (*"if the lords of the 6th, 8th and 12th occupy the 6th house..."*) and v.65
(*"the lords of the 6th, 8th or 12th are posited in the 8th house"*) both restate the template in
full, unambiguous subject-verb-object prose, for N=6 and N=8 — three lords (plural subject)
occupying one named house. That is "a dusthana lord lands in house N," confirmed twice by the
source itself, and the translator's own note at p.231 (*"it is also stated in verse 57... that
Harsha, Sarala and Vimala Yogas will also be formed if the 6th, 8th or 12th houses be associated
with or aspected by malefics"*) independently cross-checks the same reading from a different
angle. One further, unplanned piece of corroboration: `PD.06.Astra.H06.Notes`, encoded in slice 2
(Milestone 8-era) before this passage was ever read, already quoted a translator aside stating
*"he has also expressed the opinion that if lord of a Dusthana is posited in another dusthana he
does good. This has been described in Verse 57 of this very chapter"* — a forward reference this
milestone resolves rather than one it discovers.

**One template, twelve cards — the same idiom as slice 2, a different trigger.** The twelve
house-wise yogas (vv.58-69: Ava, Nisswa, Mriti, Kuhu, Pamara, Harsha, Dushkriti, Sarala,
Nirbhagya, Duryoga [house 10], Daridrya, Vimala) are encoded as one reference card,
`PD.06.DusthanaLord.General` (v.57's full condition, quoted in full: paras 202-204), plus twelve
firing cards, `PD.06.DusthanaLord.<Name>`, each testing: any of the 6th/8th/12th lords posited in
house N, OR house N occupied by a malefic, OR house N aspected by a malefic. This is `PD.06.
Chamara`/`.Dhenu`/... (vv.44-56, Milestone 8)'s own precedent — item 1 states the template in
full, items 2-12 say only "similarly disposed" — carried to a second family with a dusthana-lord-
or-malefic trigger instead of a benefic one. Two of the twelve (Harsha, Sarala) restate the
condition in their own verse and so confirm it directly; the other ten rely on it exactly as
Chamara's siblings rely on item 1. Two printed-spelling defects preserved, not corrected:
"Daridra Yoga" (v.57's naming list) vs. "Daridrya Yoga" (v.68's own naming sentence — the id and
`predicts.yoga` follow the card's own quoted verse); "VimalaYoga" (v.57's list, no space) vs.
"Vlmla Yoga" (v.69, an evident scan defect), both transcribed as printed.

**The house-10 naming collision, flagged before it could happen.** `passage:phaladeepika.06.p202`'s
own deferred.json entry warned, before either card existed, that this passage's 10th-house yoga
shares the printed name "Duryoga" with the unrelated weak/strong-lord Duryoga of v.70
(`PD.06.Duryoga`/`.Reverse`, Milestone 24) — a different condition entirely (strength/combustion
of the 1st/4th/9th/10th lords, not house-10 occupation by a dusthana lord). Named
`PD.06.DusthanaLord.Duryoga`, not `PD.06.Duryoga`, precisely to keep the two apart; a dedicated
test (`test_house_ten_duryoga_stays_distinct_from_verse_70s_duryoga`) pins the distinction rather
than trusting the naming convention alone.

**Parashara's nine-combination breakdown — the chapter's richest contradiction, read carefully
rather than forced.** The Notes at pp.80-81 quote Parashara's own effects for each of the nine
combinations of {6th, 8th, 12th}-lord × {6th, 8th, 12th}-house — exactly the sub-case Harsha,
Sarala and Vimala make a blanket auspicious claim about. Rather than linking all nine to their
Mantreswara counterpart as flat contradictions, each was read on its own words and classified by
its actual valence against the blanket claim (§7 of the resume brief: *"the objective is NOT
'make the two books agree'... it is to determine exactly what each authority says and represent
the relationship faithfully"*):

- **Five flat contradictions** (`contradicts`, no `polarity`): 6th-in-8th and 8th-in-12th and
  12th-in-6th and 12th-in-12th and 6th-in-12th — each entirely negative against a Mantreswara
  card that is entirely positive. (6th-in-12th vs. Vimala's "frugal in expenses" is the cleanest:
  Parashara's own words are "spend on vices.")
- **Three qualifications** (`contradicts` + `predicts.polarity: "qualified"`): 6th-in-6th and
  8th-in-6th, each mixed-valence (Parashara: "enmity with kinsmen BUT friendly to others" /
  "win over enemies BUT afflicted by disease") rather than flatly opposed, and the weak-graha
  half of 8th-in-8th (below).
- **Two parallel-authority agreements** (`parallel_of` + `predicts.authority: "Parashara"`):
  12th-in-8th — the one combination Parashara's own text calls good (*"According to him only the
  12th lord in the 8th produces some good effects"*, para. 228's own summary) — and the
  unconditional half of 8th-in-8th ("the native will be longlived," matching Sarala's own
  "longlived" claim before any further qualification).

**Item (5), 8th lord in 8th, is genuinely two claims, not one card with an unused clause.** Its
paragraph reads: *"The native will be longlived. If the said planet be weak being in the 8th the
native's longevity will be medium, he will be a thief, be blameworthy..."* — an unconditional
sentence and a conditional one. Split into `PD.06.Parashara.EighthLordInEighth` (base, no
strength clause, `parallel_of` Sarala) and `.EighthLordInEighth.Weak` (adds `strength(?g,"weak")`
on the same shared lord variable — ch.4's `dep.strength`, Milestone 22, reused with no new engine
code — `contradicts` Sarala with `polarity: "qualified"`, since it narrows rather than denies).
A real chart (Thanjavur, 1956-10-25, 14:15) has Mercury as the 8th lord in the 8th and
independently weak, firing both cards together — the source's own two-sentence structure showing
up as two adjudications on one nativity, not two unrelated findings stitched together.

**What was read and deliberately left uncoded, not silently dropped.** Item (6)'s trailing clause
— *"More so, if there be additionally a malefic in the said house"* — states a further
intensification when a *second, distinct* graha also occupies house 12. The condition language
has no distinct-from-the-already-bound-variable quantifier (`?m != ?g`); a naive `in_house(?m,12)`
test could bind `?m` to the very lord the sentence says is already there, asserting the
intensifier on a chart the sentence does not describe. Not encoded, and no new dependency was
registered for it — a single clause across the whole store does not justify inventing a
quantifier nothing else has ever needed (§13 of the resume brief: *"if the capability would be
speculative or architecturally consequential, stop and report it"*). Dr. B.V. Raman's commentary
(paras 229-230, disputing the "sting disappears entirely" reading — *"the intensity will be
somewhat modified"*) and the translator's closing remarks (paras 231-232: verse 57's malefic
clause also produces Harsha/Sarala/Vimala; the three yogas appear in none of Brihat Jataka,
Saravali or Jataka Parijata) remain tier-3 discursive apparatus, restating Parashara's own side
without adding independently testable doctrine — quoted by no card, claimed by
`passage:phaladeepika.06.p202`'s own paragraph list.

**Engine changes:** none. Every condition uses predicates that already existed
(`lord_of_house`, `in_house`, `aspects`, `nature`, `strength`) in combinators the engine already
generically supports (nested `any`-of-`all`, already exercised by `PD.06.RajaYoga`'s shared-
variable pattern). No new dependency was registered.

**Tests:** 351 (was 341). Ten new in `Engine/tests/test_chapter_six_dusthana_lord.py`: the
twelve-card catalogue checked against v.57's own numbered naming list rather than assumed; the
house-10 naming-collision distinctness check; that `PD.06.DusthanaLord.General` is
`reference`-only; that `PD.06.Astra.H06.Notes`'s forward reference is resolved; that all ten
Parashara cards are `active`, not `reference` (unlike `PD.06.Vesi.AuthoritativeWorks`'s collective
doctrine, each of these names one specific lord and one specific house and is directly testable);
the full relationship-type catalogue (five plain contradictions, three qualifications, two
parallels) checked against the store rather than spot-checked; that the weak-graha split is
genuinely conditional, not a restatement; and three real-chart tests (below). Four existing tests
updated: the demo chart's claim count (40 → 59, with the exact graha-by-graha accounting for
every new claim recorded in `test_slice.py`'s own comment, matching the project's standing
practice) and quoted-sentence count; the "only one claim-to-claim contradiction" test, renamed
and extended to catalogue all nine new active-active `contradicts` pairs alongside the original
`PD.09.Dignity.Exalted` one; the demo chart's adjudication-relationship-set assertion (now
`{parallel_authority, contradiction, qualification}`, all `recorded`); and `PD.06.Astra.H06.Notes`'s
own `parallel_of` list.

**Real-chart validation.** Two sweeps, ~4,500 real nativities total (four cities — Mumbai,
Thanjavur, Delhi, Chennai — 1950-2010), **zero pipeline or verification failures** across both.
A 3,968-chart sweep measured per-card fire counts (each of the twelve `PD.06.DusthanaLord.*`
cards fires on well over half of all charts, several past once per chart on average via multiple
independently-satisfying grahas — expected, given the disjunction includes "any malefic aspects
this house" and nine grahas commonly aspect twelve houses; each Parashara card, needing one
*specific* lord in one *specific* house, fires at 7-11% except the weak-graha sub-case at 1.4%)
and adjudication-type frequencies (1,697 chart-instances of an unresolved contradiction, 828 of
an unresolved qualification, 709 of an unresolved parallel authority, among the new cards alone).
A second, 504-chart sweep measured the per-chart (not per-instance) rate directly: **63.7% of
real charts produce at least one genuine, chart-dependent, both-sides-activated Mantreswara/
Parashara relationship** — not merely two authorities on file, an actual finding about that
nativity, exactly the demonstration Milestone 23's reading layer was built to make possible on a
second real contradiction cluster. `verify_adjudications` (Stage 9's adjudication-integrity check)
raised no problems on any scanned chart that exercised the new relationships.

**Production blockers cleared:** none. Ordinary Phase 3 encoding, using an already-built Phase 4
mechanism; no blocker was open going in.

**What was deliberately not built:** the distinct-graha quantifier item (6)'s intensifier would
need (a single clause does not justify it — see above); any weighting between Mantreswara and
Parashara (§7 of the resume brief is explicit that an unresolved contradiction is a valid,
final result, not a placeholder waiting on a ranking mechanism); a card for Dr. B.V. Raman's
commentary or the translator's closing remarks (discursive restatement, not independently
testable doctrine); and any change to the "Contradiction handling" or "Reasoning engine
capability" production-readiness rows, since no new engine mechanism was built — see §A's own
note on why only "Rule extraction/encoding" moved.

**Why this milestone matters.** It is the first time Stage 7's reading layer (Milestone 23) has
been exercised on a *cluster* of real, chart-dependent, claim-to-claim relationships rather than
the single pair (`PD.09.Dignity.Exalted`) it was built to read — proof that the mechanism
generalises to a second, larger, more textured case (five contradictions, three qualifications,
two parallels, one genuinely conditional split) without any new code, and that "the corpus does
not settle this" can be demonstrated as a real, evidenced, majority-of-charts finding rather than
a single hand-picked example.

---

### Milestone 26 — Chapter 6's Adhiyoga (vv.42-43)

**Phase:** 3 (knowledge), reusing Phase 4's existing adjudication representation (Milestone 23)
**Scope:** one new active card, one new reference card, one `Rules/deferred.json` passage entry
resolved, one new concept entry opened
**Status:** COMPLETE
**Completion:** 100% of the passage's testable clauses; see "What was deliberately not built"
**Commit:** this milestone's own commit (see `git log`)
**Remote:** VERIFIED

**Source-first reconnaissance.** `passage:phaladeepika.06.p175` (vv.42-43, printed pp.74-75) was
read directly from `Knowledge/phaladeepika.md` via the same paragraph-index method
`Rules/tools/backlog.py::paragraphs()` uses, not from the deferred entry's own paraphrase, which
turned out to describe the passage's dispute in slightly looser terms than the primary text
actually supports. V.42's full sentence: *"When the benefic planets occupy the 6th, 7th and 8th
places from the Lagna or the Moon, the Yoga so formed is called Adhiyoga."* The Notes (para 183,
printed p.75) immediately dispute how strictly this must be read: *"Some authors are of the view
that... all the three houses viz., the 6th, 7th and 8th should be occupied by Mercury, Jupiter or
Venus. None of them should be vacant but this is not correct. Shruti Kirti has pronounced that
according to Vyas and other ancient sages Mercury, Jupiter and Venus may be separately in the
three houses or two may be in one house and the third may be in any other house... and all the
three may be together in any of these three houses to meet the requirements..."* — the translator
explicitly names one reading incorrect and endorses the other, inside the same sentence. This
differs in an important way from the resume brief's own description of a "contradicts pair": it
is not two standing authorities left unreconciled (the shape `PD.09.Dignity.Exalted` vs. its own
Notes has, and the shape Stage 7 was built to read), it is the translator settling a dispute
between an unnamed position and a named one, the same posture `passage:phaladeepika.06.p060`
already established this project treats as apparatus around doctrine, not as doctrine itself.

**One card, not two — a design correction made mid-session, not guessed right the first time.**
The first draft encoded two cards, `PD.06.Adhiyoga.Lagna` and `PD.06.Adhiyoga.Moon`, one per
reference frame, on the reasoning that the Sardar Patel worked example (tier-3 apparatus, para
177-178: *"Mercury, Jupiter and Venus are in the 7th from the Lagna and in the 6th from the
exalted Moon... There is both Lagnadhiyoga and Chandradhiyoga"*) names two distinct yogas.
`Rules/tools/dupes.py` caught the problem immediately: both cards necessarily quoted the
identical naming-and-effect text (v.42's naming sentence carries both reference frames in one
clause, and neither v.42's own effect nor v.43's further effects differ by frame), producing the
first same-book, full-`quote_sha256` duplicate this project has ever recorded — a real defect by
the tool's own stated philosophy (*"only the same book saying the same thing twice from the same
words is a genuine encoding error"*). Checked against precedent (`PD.06.Varishtha`/`.Sama`/
`.Adhama`, three cards cut from one verse, but each with its *own* distinct effect sentence),
nothing here supplies that distinguishing text. The correction: **one card**, `PD.06.Adhiyoga`,
whose condition is v.42's own disjunction — `any` of a Lagna-frame block and a Moon-frame block,
each an `all` of three grahas' own `any` of houses 6/7/8 — reusing the nested `any`-of-`all`
combinator `PD.06.RajaYoga` already exercises, no new engine code. `Engine/rules.py::evaluate`'s
own solution-per-satisfying-binding design means which frame(s) actually fired is still visible
in a claim's `conditions_satisfied` without a second card, and — discovered while testing, not
predicted in advance — a chart satisfying *both* frames produces *two* claims for this one card,
one per independently-satisfying solution, exactly mirroring the twelve `PD.06.DusthanaLord.*`
cards' own already-documented multi-claim behaviour (Milestone 25) and reproducing the source's
own "there is both Lagnadhiyoga and Chandradhiyoga" observation without inventing a second card
to hold it.

**The rejected reading, preserved but not made an active contradiction.** `PD.06.Adhiyoga.
ShrutiKirti` (reference, tier 2) quotes the Notes paragraph in full — both the unnamed "some
authors" position and the translator's rejection of it in favour of Shruti Kirti's (per Vyas)
confirmation — and is linked `parallel_of` `PD.06.Adhiyoga`, since Shruti Kirti's own reading is
the same loose condition already encoded. The rejected reading is independently *expressible*
with predicates already in the vocabulary (an `all`, over houses 6/7/8, of an `any` over the
three grahas being posited there — "no house among the three left vacant") but was deliberately
**not** encoded as a competing active `contradicts` card. The reason is structural, not
editorial: that reading's actual claim is that Adhiyoga does *not* form when a house is left
vacant, and the card schema has no way to assert the *absence* of another card's yoga as a firing
rule — every narrower-condition sibling already in the store (e.g. `PD.06.Parashara.
EighthLordInEighth.Weak`, Milestone 25) predicts something for a chart satisfying its *own*
condition, never a negation of a different card's formation. Building that would need a new
negation-of-another-card's-formation predicate nothing else in the store has ever required —
exactly the kind of speculative architecture this project declines to build for one clause (the
same call Milestone 25 made for `PD.06.Parashara.EighthLordInTwelfth`'s own distinct-graha
quantifier). Opened as `concept:adhiyoga-distribution-strictness` in `Rules/deferred.json` for a
human to review, since it is a judgement call, not an engine gap.

**Engine changes:** none. Both `in_house` and `in_house_from` (`dep.graha-frame`) already existed
and are already exercised by `PD.06.Kesari`, `.Sakata` and the Adhama/Sama/Varishtha trio.

**A correction found and fixed within this same milestone, not carried forward.** The Notes
quote's first extraction pass described the character between "Notes" and "Some authors" as a
corpus OCR defect (a U+FFFD replacement character) — a plausible-sounding claim that turned out
to be wrong on direct inspection: the byte is a valid em dash (U+2014), matching the "Notes - "
separator this chapter uses elsewhere, and it only *renders* as a replacement glyph in some
terminals and fonts. Caught by a test asserting the exact codepoint before that test was ever
committed, not left standing. Both the card's `note`, its `extraction.verified_by`, and the test
itself were corrected in place; nothing false about the corpus was written into the permanent
record.

**Tests:** 363 (was 351). Twelve new in `Engine/tests/test_chapter_six_adhiyoga.py`: the
card-store shape (exactly one active Adhiyoga card plus the reference card, not a Lagna/Moon
pair); the condition's exact nested structure (one `any` of two three-graha `all` blocks, each
graha's own `any` over houses 6/7/8, houses always `{6,7,8}` for every leaf); that the acting set
is fixed to Mercury/Jupiter/Venus, not "any benefic"; the reference card's `conditions == {"all":
[]}`, its `parallel_of` link, and both readings' text present in its quote; the corrected em-dash
finding; that no `contradicts` link exists anywhere on either card; the `deferred.json` resolution
and new concept entry; a real-chart test on the standing demo nativity (fires once, via the
Moon-frame arm only, confirmed from `conditions_satisfied` rather than assumed) plus its
`parallel_authority`/`recorded` adjudication; and three constructed-chart tests (Lagna-only, both
frames together — two claims — and a negative control) built with `Engine.tests.test_strength.
place`, after a ~4,500-nativity blind sweep (four cities, 1950-2010, by date and time of day)
failed to find a "both frames" chart within its own time budget — worked out afterward rather
than guessed: the demo chart's Lagna (Capricorn) and Moon (Leo) sit five zodiac signs apart, and
the two frames' three-sign-wide windows only overlap when the two are within about two signs of
each other, so no birth instant at the demo's own coordinates on its own date could ever produce
one regardless of time of birth. One existing test updated: `test_slice.py`'s demo-chart claim
count (59 → 60, with the exact new claim's derivation recorded in the same comment style the
prior four milestones established).

**Real-chart validation.** The standing demo nativity (Thanjavur, 1987-03-14, 04:22) fires
`PD.06.Adhiyoga` once, via Mercury in the 7th, Jupiter in the 8th and Venus in the 6th, all
counted from the Moon — a genuine, previously-latent claim this milestone's own encoding
surfaced on a chart already used throughout the test suite, not a hand-picked new one. The
~4,500-chart blind sweep (Mumbai, Thanjavur, Delhi, Chennai, 1950-2010) found no pipeline or
verification failures and no naturally-occurring "both frames" instance within its budget; the
Lagna-only, both-frames and negative-control configurations are demonstrated instead on charts
built by moving one or two bodies on a real, ephemeris-computed chart to an exact sidereal
longitude (`Engine.tests.test_strength.place`), the same technique `test_chapter_six_strength.py`
already uses for placements "that simply do not occur on any convenient birthday."

**Production blockers cleared:** none. Ordinary Phase 3 encoding; no blocker was open going in.

**What was deliberately not built:** `passage:phaladeepika.06.p168` (vv.39-41, the seven-planets-
in-N-signs family) — needs a genuinely new engine fact (a distinct-sign-count over the seven
classical grahas) that this milestone was scoped not to add without a specific reason to; a
`contradicts` card for the rejected "some authors" reading (see above — structurally
unrepresentable, not merely deferred); and any weighting between Shruti Kirti's reading and the
rejected one (there is nothing to weigh: the store encodes exactly one reading, the one the
translator endorses, and documents the other as apparatus). No change to "Reasoning engine
capability" or "Contradiction handling," since no new engine mechanism was built and no new
`contradicts` pair was drawn.

**Why this milestone matters.** It is a small, single-passage encoding session, and it is
reported as one: two cards, no chapter closed outright (`passage:phaladeepika.06.p168` remains).
Its actual interest is procedural — a real example of the project's own tooling (`dupes.py`)
catching a genuine design mistake mid-session and the correction being cheaper and more honest
than the original two-card plan, and a second real example (the em-dash) of a claim about the
corpus being checked and corrected before it became permanent, rather than after.

---

### Milestone 27 — Chapter 6's seven-planets-in-N-signs family (vv.39-41), closing chapter 6's testable doctrine

**Phase:** 3 (knowledge), with one small Phase 2 addition (a new fact/predicate)
**Scope:** seven new active cards, one new reference card, one new engine predicate, one new
dependency-registry entry, one `Rules/deferred.json` passage entry resolved
**Status:** COMPLETE
**Completion:** 100% of the passage's testable clauses; chapter 6's testable doctrine is now
fully encoded (see "Chapter 6 accounting" below)
**Commit:** this milestone's own commit (see `git log`)
**Remote:** VERIFIED

**Source-first reconnaissance.** `passage:phaladeepika.06.p168` (vv.39-41, printed pp.73-74) was
read from `Knowledge/phaladeepika.md` (paragraph indices 168-174, confirmed against
`Rules/tools/backlog.py::paragraphs()`), then independently checked against a direct 300dpi
render of the source PDF pages (`Books/Mantreswara_s__Phaladeeplka_.pdf`, 0-indexed pages 72-73)
rather than trusted from the OCR/markdown extraction alone. The render matches the extraction
exactly: no printing defect, no OCR artifact, no Notes section, no translator commentary on this
passage at all — unlike almost every other chapter 6 slice, this one closes with nothing to
preserve as a defect. The text is seven fully self-contained items, each stating its own naming
clause, exact condition and effect in one paragraph (unlike the vv.44-56 and vv.57-69 house-wise
families, which share one governing template across items): *"(1) When the seven planets from
Sun to Saturn occupy seven separate signs the Yoga so arising is known as Vallaki. This is also
called Veena Yoga... (2) When all the seven planets are in six signs, they form Dharma Yoga...
(3) ...five signs only... Hasha Yoga... (4) ...four signs only... Kendra Yoga... (5) ...three
signs only... Shula Yoga... (6) ...two signs only... Yuga Yoga... (7) ...one sign... Gola
Yoga."* The seven counts (7 down to 1) exhaust every value the count of distinct signs occupied
by seven bodies can take, so the family is a genuine partition of every possible chart, not seven
independent conditions that might overlap or leave a gap — confirmed empirically below, not
merely asserted from the arithmetic. "The seven planets from Sun to Saturn" is the verse's own
words for its own set: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, naming the nodes not at
all. No day/night distinction, no Lagna, no dignity or strength condition, no distinction between
occupation and lordship — the doctrine is exactly what it appears to be, existential over none of
its variables (there are none) and categorical: a chart's own count of distinct signs determines
which one of the seven names applies to it, and exactly one always does.

**One new engine fact, kept as narrow as the doctrine that needs it.** Nothing in the prior
vocabulary counts distinct signs occupied by a set of bodies: `occupant_count` counts occupants of
one house, not signs occupied overall, and no combinator in `Engine/rules.py` can express "how
many distinct values does this variable take." Built `seven_graha_sign_count(n)`
(`Engine/facts.py::_seven_graha_sign_count`), one chart-wide fact with no graha argument — the
same shape as `lagna_sign`, because the doctrine asks about the seven bodies collectively, not
about any one of them. Each of the seven cards matches a literal `n` against this fact's exact
key, the identical mechanism `occupant_count` already uses for a literal count (`Milestone 6`'s
counting work), so **no new condition-language combinator was built** — the resume brief's own
"do not build arbitrary counting infrastructure ahead of doctrine" is honoured by construction,
not by restraint alone: there was nothing more general to build than what seven cards asking "is
the count exactly N?" actually need.

**Which nine grahas count as "the seven" is doctrine, not an engine choice — caught by the
project's own architecture test, not anticipated in the design.** The first implementation wrote
`SEVEN_CLASSICAL_GRAHAS = ("Sun", "Moon", ...)` directly into `Engine/facts.py`, on the reasoning
that "the seven classical planets" is a fixed astronomical convention rather than book-specific
doctrine. `Engine/tests/test_doctrine.py::test_no_doctrinal_constant_is_written_in_python[facts.py]`
disagreed, correctly: any graha name written as a Python literal in `facts.py` or `doctrine.py` is
exactly the "table smuggled past the store" the whole architecture exists to prevent, regardless
of how conventional the table feels, because a second book that named a different seven (or
included the nodes) would then require a code change instead of an encoding one. Corrected before
this milestone's first commit: a new reference card, `PD.06.SevenGrahas`, quotes "the seven
planets from Sun to Saturn" — a strict substring of `PD.06.Vallaki`'s own span, not an invented
restatement, so it carries a different `quote_sha256` and trips no `dupes.py` SAME-QUOTE finding
— under `predicts.relation: "seven_grahas"`, and a new `Doctrine.seven_grahas()` accessor
(`Engine/doctrine.py`) reads it the same way `combustion_source()` already reads which body
combustion is measured from. `_seven_graha_sign_count` now names no graha at all; it reads the
set from the store, the way every other doctrine-backed extractor in this module does.

**Seven cards, no governing/reference card for the condition.** `PD.06.Vallaki` (n=7),
`.Dharma` (n=6), `.Hasha` (n=5), `.Kendra` (n=4), `.Shula` (n=3), `.Yuga` (n=2), `.Gola` (n=1) —
each a single-span active card quoting its own item's full paragraph, `activation: "active"`. No
governing card was needed (unlike `PD.06.DusthanaLord.General` for vv.57-69): every item already
states its own complete condition, name and effect, so there is no shared template to factor out.
All seven are linked to each other by `parallel_of` (21 links total, 6 per card) — mutually
exclusive readings of one family from one book, no `authority` field, the same relationship
`PD.06.Varishtha`/`.Sama`/`.Adhama` and `PD.06.Lakshmi`/`.Gouri` already carry, extended here to a
family of seven rather than three. `PD.06.Vallaki`'s own naming clause gives the yoga two names
in the same sentence — *"known as Vallaki. This is also called Veena Yoga."* — recorded as the
source's own deliberate dual naming, not a printed-spelling defect the way Subhamala/Asubhamala's
two spellings are; the card id and `predicts.yoga` use the first-given name, the note records the
second.

**Chapter 6 accounting.** With `passage:phaladeepika.06.p168` resolved, every remaining
`passage:phaladeepika.06.*` entry in `Rules/deferred.json` (26 of them) is tier-3 apparatus —
worked-example horoscope illustrations (Stalin, Radhakrishnan, the Nehrus, Indira Gandhi, Sardar
Patel, Morarji Desai — the same category chapters 8-9 already excluded), the chapter's closing
colophon, itemized Notes lists that restate a rule already stated in intact prose, or translator
asides — or a standing, already-tracked concept (the Sunapha/Anapha/Durudhara naming convention,
alternate Kemadruma definitions pending manual verification, and the three human-decision items
in §D below). None represents unencoded *testable* doctrine. **Chapter 6's testable doctrine is
therefore complete** — every verse that states a condition and a predictable effect now has an
active or reference card, and every verse that does not (an example, an aside, a closing formula)
is recorded as deliberately excluded rather than silently absent. This is a qualitative
completion the raw card count under-states, exactly as Milestone 25's own text observed when
chapter 6 first moved from "partial" to "essentially complete" — see "Production impact" below
for why the score itself does not move on it.

**Tests:** 391 (was 363). Twenty-eight new in `Engine/tests/test_chapter_six_sign_count.py`: the
card-store shape (seven active cards with the right exact conditions and `predicts.yoga` names,
all mutually `parallel_of`-linked, no two sharing a quote, the dual-naming note, the reference
card's `relation`/`grahas`/quote-is-a-substring-of-Vallaki's-own-span shape); the
`deferred.json`/dependency-registry resolution; the new `Doctrine.seven_grahas()` accessor read
directly (including that it raises `DoctrineError` — not a silent Sun-through-Saturn default —
when handed a store with no reference card at all); the new fact tested in isolation via
`Engine.tests.test_strength.place`-constructed charts across every count 1 through 7, including
that Rahu/Ketu placed into signs none of the seven occupy leaves the count unchanged, and
determinism; a positive/negative sweep across all seven cards on one family of constructed charts
confirming each fires only at its own exact count; a direct property test that exactly one of the
seven fires on an unmodified real chart, never zero and never two; and seven parametrized
real-chart tests, one per count (below). One existing test file, `test_slice.py`, updated for the
demo chart's new claim (60 → 61; `PD.06.Dharma` fires via `seven_graha_sign_count(6)` on the
standing demo nativity).

**Real-chart search.** Sign occupancy depends only on each body's ecliptic longitude, not on the
observer's location or the ascendant, so the search used a direct ephemeris sweep rather than a
birth-record sweep — much faster, and able to span centuries rather than decades. **219,132 daily
instants** were scanned from 1800-01-02 to 2399-12-20 (the full range the vendored Swiss
Ephemeris data file, `Engine/vendor/swisseph/*_18.se1`, covers), tallying the distinct-sign count
directly from `body_position` calls with no chart or birth record built at all. Every one of the
seven values occurs naturally in that range — none is structurally impossible, and none needed to
be, established empirically rather than assumed from the arithmetic. Distribution: n=5 most
common (43.3%), n=6 (22.4%), n=4 (26.4%), n=7 (2.6%), n=3 (5.1%), n=2 (0.24%), and **n=1 rarest by
far — 4 days across the entire 600-year range (0.0018%)**: 1821-04-02/03 (Pisces) and
1962-02-04/05 (Capricorn). The second is the widely reported "Great Conjunction" of February
1962, an independently documented historical event, not a coincidence manufactured for this
milestone. One real instant per count was then picked from the 1950-2035 window (a stable,
unambiguous Asia/Kolkata UTC+5:30 era) and run through the full birth-record pipeline —
`Engine.chart.resolve_birth` → `compute_chart` → `Engine.pipeline.run` — confirming each fires
exactly its matching card and no other: 1950-05-20 (Vallaki, n=7), 1950-03-21 (Dharma, n=6),
1950-01-01 (Hasha, n=5), 1950-01-08 (Kendra, n=4), 1950-01-19 (Shula, n=3), 1955-07-28 (Yuga,
n=2), and **1962-02-04, the Great Conjunction itself (Gola, n=1)**. All seven are pinned in
`Engine/tests/test_chapter_six_sign_count.py`, not left as one-off scratch output.

**Verification results.** `Rules/tools/verify.py`: clean (537 cards, every quote byte-exact, every
deferred item recorded). `Rules/tools/dupes.py`: no duplicate candidates, cross-book or
within-book — the seven cards' quotes, though structurally similar prose, differ enough in words
that not even the `NEAR-TEXT` reviewer flagged them. `Rules/tools/backlog.py --write` and
`Rules/tools/leverage.py --write`: both regenerated clean; `Rules/tools/review.py --queue`: 0 new
structural cards to sign (`PD.06.SevenGrahas` auto-signed as structural, 273 → 274), 0 new
interpretive cards queued (all seven firing cards hand-signed at authoring time — the same
`"tarunrameshphotography + Claude (...)"` discipline established since Milestone 15 — so the
standing three holdouts are still the only queued cards). Full suite: 391/391 passing.

**Production blockers cleared:** none. Ordinary Phase 3 encoding; no blocker was open going in.

**What was deliberately not built.** A generic "distinct-value-count over any variable" combinator
— the resume brief's own warning against speculative counting infrastructure, honoured because
seven cards each asking "is n exactly K?" never needed one. A generic "fixed member-set" doctrine
accessor beyond `seven_grahas()` itself — the next passage that needs one gets its own narrowly
named accessor the way `graha_classes()`, `combustion_source()` and this one each are, not a
general "named set" facility built ahead of a second user. Any weighting or precedence among the
seven cards — there is nothing to weigh: they are a partition, and the store's own real-chart
tests confirm exactly one is ever satisfied at once, which is a property of the doctrine, not an
engine guarantee that needed building.

**Production impact.** No production-readiness category score moved — see §A's own entry for the
row-by-row reasoning. In short: 8 cards (7 firing, 1 reference) is smaller than Milestone 25's
23-card move and closer to Milestone 24's 3-card and Milestone 26's 2-card additions that held;
the new engine fact is a single small predicate (`dep.seven-graha-sign-count`, effort 2, the
smallest predicate dependency in the registry) reusing an existing matching mechanism, not a new
combinator or stage, so "Reasoning engine capability" holds exactly as Milestone 26 held it for
Adhiyoga; the real-chart evidence is methodologically distinct (a direct multi-century ephemeris
sweep rather than a birth-record sweep) but is still the same *kind* of evidence — "does a real
chart produce the claim the doctrine predicts" — that "End-to-end validation" is already credited
for, so it holds per the same discipline Milestone 24 applied to its own 2,176-chart sweep; +28
tests (~7.7%) is proportionally larger than Milestone 26's +12 but the same *kind* of test
(structure, isolated-primitive, positive/negative/boundary, real-chart) already exercised
elsewhere in the suite, not a new verification technique the way Milestone 23's mutation testing
was, so "Test coverage" holds too. Provenance holds at the same ~99.4% raw fraction (534/537),
all new cards hand-signed. **Chapter 6's completion is real and stated plainly above, and is
exactly the kind of qualitative fact this table's own text records even when the percentage does
not move** — the same posture Milestone 26 took for its own two-card addition.

**Why this milestone matters.** It closes chapter 6's testable doctrine outright — the last
unencoded passage identified since Milestone 8 first opened this chapter — with a new capability
kept exactly as narrow as the one family that needed it, and with the project's own two guard
rails (`dupes.py` for encoding defects, `test_no_doctrinal_constant_is_written_in_python` for
smuggled tables) each catching a real design mistake before it shipped, not after: the first
draft's hardcoded graha tuple would have been the second time in two consecutive milestones a
design correction was caught mid-session by the store's own tooling rather than assumed right the
first time (the first being Milestone 26's `dupes.py` catch on the Adhiyoga card split).

---

### Milestone 28 — `dep.triped-sign-class` re-investigated; confirmed unresolved, left inert

**Phase:** none (read-only investigation; no Phase 2 or 3 deliverable was produced)
**Scope:** zero cards, zero engine changes, zero dependency-registry edits — one deepened,
re-confirmed finding, recorded as `MILESTONES.md` §D Decision 0d
**Status:** COMPLETE (as an investigation; this is not an implementation milestone)
**Commit:** this milestone's own commit (see `git log`)
**Remote:** VERIFIED

**Why this dependency was investigated rather than implemented.** `Rules/tools/leverage.py`
ranks `dep.triped-sign-class` first by ROI (cost 1, unlocks 1 card,
`PD.04.Lagna.TripedSign`) — the same ranking Milestone 27's own header noted and explicitly
declined to act on, because the ranking measures cost and cards-unlocked, not whether the
question is actually an engineering question. It is not: `Rules/deferred.json`'s own entry
already stated *"nothing to build until the term is resolved,"* and the entry was written by
Milestone 21 after a source check, not asserted without one. This session's brief was to verify
that diagnosis against the live repository and the primary source directly, rather than either
trust it uncritically or discard it in favor of implementing a guess to clear the backlog.

**Source-first reconnaissance.** Read `Knowledge/phaladeepika.md`'s chapter 4 (Kalapurusha
strength material, pp.35-50) end to end, not just the one verse: verse 6 (line ~865) is
Mantreswara's own doctrine (the numbered-paragraph strength commentary), immediately preceded
by a structurally different, translator-authored rule with the same shape — "Bhava Dik Bala,"
pp.40-41 — which classifies signs biped/quadruped/keeta/watery and gives each a Lagna-or-house
strength rule. Grepped the full corpus (`Knowledge/phaladeepika.md`, `Knowledge/brihat-jataka.md`)
for every spelling near "triped," "biped," "quadruped," "centiped"/"keeta," and "watery" to
locate every passage that could corroborate or define the term; found the chapter 1 v.7 body-form
table (`PD.01.SignBodyForm.Table`) and the chapter 4 Bhava Dik Bala rule, both already known to
the store, and confirmed no third passage anywhere names "triped."

**Independent primary-source verification, not reuse of the prior session's claim.** Opened
`Books/Mantreswara_s__Phaladeeplka_.pdf` directly with PyMuPDF this session (0-indexed page 43,
printed p.44 — located by searching the PDF's own text layer for the sentence, not by trusting
the stored `page_anchor`). Three independent checks, not one: (1) the raw extracted text layer
reads "...if it is a triped sign..." exactly as the card quotes it; (2) `page.get_text("dict")`
span data shows this entire sentence as a single unbroken `TimesNewRomanPSMT` run, ruling out a
font-substitution or ligature artifact at the specific letter; (3) a 600dpi crop of just this
line was rendered to an image and read directly — plain, legible, unambiguous "triped." Cross-
checked against `Pipeline/profiles/phaladeepika.json`, which records this book's extraction
method as `pdf_text` direct extraction from a clean digital layer, not OCR over a scan — the
class of extraction defect that would most plausibly explain a single-letter substitution
(scanned-image OCR misreading a glyph) does not apply to this book's pipeline at all.

**Conclusion: Decision 0d (see §D) — genuinely unresolved, not a capability gap.** "Biped" is
the most textually plausible reading (the Bhava Dik Bala rule states the identical Lagna-biped-
one-Rupa clause), but it is a different authority's table, and it does not explain the verse's
own "Vrischika gets 1/4 Rupa" clause, which nothing in either converted book corroborates. Per
this project's own standing rule that a card must never make a substitution the source itself
does not make, `dep.triped-sign-class` was left exactly as `Rules/deferred.json` already had it
(`effort: 1`, `implemented: false`) and `PD.04.Lagna.TripedSign` was left exactly as encoded
(`activation: "inert"`). **No file in `Rules/` was edited.**

**What would still be needed even if "biped" were later ratified by a human.** Discovered as a
side finding, not chased further: `PD.01.SignBodyForm.Table` records only the four class names
(`classes: ["human", "quadruped", "centiped", "watery"]`), not a sign→class mapping — the
Milestone 16 verification pass confirmed the printed table's *layout* is unambiguous but
deliberately left encoding its *contents* to a future Phase 3 session. So resolving the "triped"/
"biped" question would not, by itself, make `PD.04.Lagna.TripedSign` executable; the per-sign
table would still need to be encoded as `predicts` data first. Recorded in Decision 0d; no
`dep.*` entry was added for it, because `dep.triped-sign-class` already exists to cover the gap
and a second dependency for the same missing table would double-count it in `leverage.py`.

**Verification results.** `Rules/tools/verify.py`: clean, unchanged (537 cards, every quote
byte-exact, every deferred item recorded — no output differs from before this session).
`Rules/tools/dupes.py`: no duplicate candidates, unchanged. `Rules/tools/backlog.py`: 139
entries, unchanged, same 72 available-now, same 7 newly-unblocked-but-stale entries already
flagged by Milestone 27's own header. `Rules/tools/leverage.py`: unchanged — `dep.triped-sign-
class` still ranks first by the tool's own ROI metric, exactly as it did before this session,
because the tool has no way to represent "this is a human question, not an engineering one";
that gap is now recorded in prose (§D, Decision 0d, and the header's resume point) rather than
left implicit. Full suite: 391/391 passing, unchanged.

**Production blockers cleared:** none. **Production-readiness impact:** none — see §A's own
Milestone 28 paragraph for the row-by-row reasoning; a confirmed-unresolved investigation is not
a cleared capability and must not move any category.

**Why this milestone matters.** It is the difference between a stale note that might be wrong by
now and a note two independent sessions, seven milestones apart, have each derived from the
primary source by different methods. A future session reading `leverage.py`'s output cold would
otherwise see `dep.triped-sign-class` sitting at the top of the ROI table and reasonably wonder
whether it was overlooked; it was not, twice over, and that is now on the record in a form a
future session can check rather than merely trust.

---

### Milestone 29 — Chapter 3 slice 1, `dep.varga`/`dep.vargottama` built, and a re-diagnosis both directions found

**Phase:** 2 (engine completion) + 3 (knowledge)
**Scope:** 1 new chapter file (`Rules/phaladeepika/ch03.json`, 3 reference cards), 2 cards edited
(`PD.09.Vargottama` released; `PD.10.Venus.VargaMarsSaturn` re-diagnosed, still inert), 1 card
released as a side effect of dependency reconciliation (`PD.02.AdverseDisposition`), 3 new engine
predicates (`in_varga_sign`, `vargottama`, `dignity_in_varga`; a fourth, `varga_owned_by`, declared
but deliberately not implemented), 3 new `Doctrine` accessors, 4 `Rules/deferred.json` dependency
entries (`dep.varga`, `dep.vargottama` resolved; `dep.dignity-in-varga` resolved; `dep.varga-
ownership` newly registered, unresolved), 14 new chapter-3 passage backlog entries, 27 new tests
(`Engine/tests/test_varga.py`), 2 existing tests corrected for stale assumptions.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**Why Chapter 3, not the whole thing.** The chapter is not rule-dense the way ch. 6 or ch. 9 are:
v.1-v.20 cover roughly nine independent doctrine clusters (varga definitions; an effect-fraction
table and five Avastha age-states; Hora/Drekkana/Dwadasamsa/Trimsamsa ownership; a Krura Shastyamsa
list; Saptamsa/Dasamsa/Shodasamsa counting plus a three-way strength-method dispute; a 13-varga
Vaiseshikamsa dignity-tier system; a 10-varga strength ladder; several Shadvarga/Hora/Drekkana
yogas; a Mandi/Gulika alternate-lagna method; and an 11-state Avastha-naming system with percentage
effects). Per the master prompt's own instruction ("use the smallest real test case first," "do
not try to encode all of Chapter 3 in one giant commit"), this milestone extracted exactly the one
cluster `dep.varga`/`dep.vargottama` needed -- v.1's Dasavarga list and Vargottama definition, and
v.4's Navamsa-start sentence -- and left the other eight as individually reasoned, paragraph-level
`Rules/deferred.json` entries (`passage:phaladeepika.03.p003` through `.p054`) rather than one
whole-chapter placeholder, now that any card exists for the chapter at all.

**Source read in full before writing anything.** `Knowledge/phaladeepika.md` ch. 3 (all 20 verses,
lines 501-627) was read completely, not just the backlog summary, per the master prompt's §4. Two
findings corrected the master prompt's own working assumptions before implementation began:

1. **`dep.varga`'s prior note ("MVP scope names D-1, D-3 and D-9") was re-checked against the live
   store, not trusted.** Nothing currently in the corpus consumes a D-3 (Drekkana) fact:
   `PD.10.Venus.VargaMarsSaturn`'s "Varga of Mars or Saturn" turned out to be an *ownership*
   question (see below), not a sign-occupancy one, and stays blocked regardless of which division
   it means. So only D9 (Navamsa) was built -- the one division ch. 3 v.1's own Vargottama
   definition actually requires -- matching the same one-capability-at-a-time discipline
   `dep.seven-graha-sign-count` and `dep.strength` already followed. D3/D2/D12/Trimsamsa were not
   built speculatively.
2. **Ch. 21, named alongside ch. 3 as a varga source in the prior standing note, is Brihat Jataka's
   chapter, not a second Phaladeepika chapter** (Phaladeepika's own ch. 21 is "Nature of Antar
   Dasas and Pratyantar Dasas" -- unrelated). Brihat Jataka ch. 21, "आश्रययोगाध्यायः · Planets in
   Vargas," was read in full this milestone. It independently corroborates the Vargottama concept
   (v.7: Navamsa-in-lagna character effects "for ascendants other than Vargottam," with a
   named-leader effect when the lagna's own Navamsa is Vargottam) -- consistent with, not a second
   definition of, Phaladeepika's own ch.3 v.1 definition -- but states no ownership doctrine at
   all, so it does not resolve `PD.10.Venus.VargaMarsSaturn`'s ambiguity either. Brihat Jataka
   carries zero rule cards (no extraction has started on it), so nothing from ch. 21 was encoded as
   a card this milestone; the corroboration is recorded in prose
   (`passage:phaladeepika.03.p052`'s deferred entry and `dep.varga-ownership`'s own note) for
   whoever starts that book's extraction.

**Exact doctrine encoded (`Rules/phaladeepika/ch03.json`, all `activation: "reference"`).**
- `PD.03.Dasavarga` (v.1): the full ten-fold Dasavarga list, quoted whole. `predicts.table` carries
  only `{"D1": 1, "D9": 9}` -- the two codes the store's varga vocabulary uses -- with the other
  eight divisions preserved uncoded in `predicts.printed_list` rather than assigned a modern
  `D`-number the verse itself never uses. Two source observations recorded rather than corrected:
  Trimsamsa's "5 parts" counts five planetary allotments, not five equal arcs (the verse's own
  parenthetical, "All parts are not equal," says so); Shodasamsa's printed arc (1°16'52") does not
  equal 30°/16 (1°52'30"), read as a probable OCR digit transposition and left as printed.
- `PD.03.Vargottama.Definition` (v.1): "Vargottama is the name given to that particular Navamsa in
  a Rasi which bears the same sign as that of Rasi itself" -- `predicts.varga_a`/`varga_b` =
  "D1"/"D9", read by `Doctrine.vargottama_definition()` so the comparison is doctrine the engine
  reads, not two literals in `_varga`.
- `PD.03.Navamsa.Start` (v.4): "The first Navamsa in the signs from Aries onwards begins
  respectively with Aries, Capricorn, Libra and Cancer" -- four worked examples, not a general rule
  stated in words. `predicts.table` (`{"Moveable": 0, "Fixed": 8, "Dual": 4}`) is the engine's
  arithmetic restatement of those four examples by mobility class (ch. 1's own `sign_attributes`,
  not re-derived): the two Moveable examples (Aries, Cancer), three signs apart, independently
  agree with each other and with this reading, which is the cross-check that justifies generalising
  by mobility rather than treating the four as four unrelated positional facts. Independently
  re-verified in this milestone against the classical triplicity mnemonic (Fire→Aries,
  Earth→Capricorn, Air→Libra, Water→Cancer) for all twelve signs, not just the four the verse
  gives -- see `Engine/tests/test_varga.py::test_navamsa_start_matches_the_classical_table`.

**Engine architecture chosen, and why it is the minimum justified one (§9).** Raw arithmetic
(dividing 30° into 9 equal parts, a division index) stays source-independent, the way `_sign_of`
already is. Everything that varies by book -- the division count, and which sign a Navamsa begins
from -- is read from the two reference cards above via two new `Doctrine` accessors
(`varga_division_count`, `navamsa_start_offset`), never a Python literal; a defensive check
(`{definition["varga_a"], definition["varga_b"]} != {"D1", "D9"}` raises `DoctrineError`) stops the
extractor from silently comparing the wrong two vargas if the reference card ever changed. No
generalized `VargaChart` abstraction, no per-division plugin system, and no D2/D3/D7/D10/D12/D16/D60
calculator were built -- nothing in the current corpus justifies them, per the master prompt's own
"do not build D10/D12/D16/D20 etc. merely because commonly used." One function,
`Engine/facts.py::_varga`, computes the D9 sign of every graha in one pass and, from the same
already-computed D9 sign, emits `in_varga_sign`, `vargottama` (same sign in D1 and D9) and
`dignity_in_varga` (see below) together -- no duplicated arithmetic across three extractors.

**A second card released by the same reconciliation, not by design.** Investigating "every card
that can become executable after the minimum Varga capability exists" (master prompt §13) surfaced
`PD.02.AdverseDisposition` (ch. 2 v.36) as newly unblocked by dependency bookkeeping alone --
`Engine/tests/test_counting_and_nature.py::test_every_card_whose_dependencies_are_met_is_no_longer_inert`
caught it. The verse: "adversely disposed, if... debilitated (be in a sign of debilitation **or
Navamsa**)..." -- six alternatives, quantified over the grahas, one of which needs debilitation
tested against the D9 placement as well as the D1 one. `dep.varga` alone does not supply that (it
gives D9 *occupancy*, not *dignity against* a D9 placement), so a new predicate,
`dignity_in_varga(graha, varga, dignity)`, was built -- narrowly: only the "debilitated" value is
emitted, since that is the only dignity this verse names for a divisional placement, and
exalted/own/Moolatrikona-in-Navamsa facts would be speculative vocabulary no card asks for (the
same restraint `_dignity` itself already exercises by leaving friend/neutral/enemy to a separate
extractor). The card's six "any"-sentinel leaves were rewritten to `?g` (the Milestone 16/18
finding: "any" is a literal that matches no fact, so a released card must have its condition
rewritten, not merely its activation flipped) and a seventh leaf,
`dignity_in_varga(?g,"D9","debilitated")`, was added alongside the existing D1 `dignity(?g,
"debilitated")` leaf as an independent alternative, not a replacement. Released:
`activation: "active"`, `requires` removed.

**A second card re-diagnosed, deliberately not resolved.** `PD.10.Venus.VargaMarsSaturn` (ch. 10
v.4) was the card the standing note on `dep.varga` explicitly named as "belonging to whoever
encodes the varga doctrine with chapters 3 and 21 in hand" -- this milestone. Its first branch
used to read `in_varga_sign(Venus,"D9","any")`: occupancy of a literal D9 sign, narrowing "Varga"
to Navamsa on no textual basis, and further broken by "any" matching no fact at all. Having now
read both candidate source chapters with this verse specifically in mind, neither Phaladeepika
ch. 3 nor Brihat Jataka ch. 21 states an ownership doctrine that names which division "the Varga of
Mars or Saturn" means -- this is a genuine source ambiguity (master prompt §15, category D), not a
missing calculation, and it was not resolved by inventing a reading. The condition was rewritten to
test ownership rather than occupancy -- `varga_owned_by(Venus,?v,Mars)` /
`varga_owned_by(Venus,?v,Saturn)`, existentially quantified over *which* division, matching the
verse's own silence on that point -- and `varga_owned_by` was declared in `Engine/facts.py`'s
`VOCABULARY` without an extractor, so the branches stay correctly unfireable rather than
coincidentally satisfied by `dep.varga`'s D9-occupancy machinery. A new dependency,
`dep.varga-ownership`, was registered in `Rules/deferred.json` (`depends_on`: both chapter's own
ids) and the card's `requires` corrected to it, so `backlog.py`/`leverage.py` do not misreport this
card as released by `dep.varga` -- the same re-diagnosis shape Milestone 22 gave `PD.06.Pushkala`
when `dep.strength` landed and did not release it either. The two aspect branches (Mars/Saturn
aspecting Venus) remain faithful, confirmed in Milestone 19 and unchanged here. A genuine sign-off
was recorded (`extraction.verified_by`), not left unsigned this time, because what was verified
this session is the *new* condition's honesty about the ambiguity, not a rubber stamp of the old,
already-known-wrong one -- `test_chapter_ten_interpretive_cards_are_signed_off` (renamed from
`..._except_the_one_holdout`) now expects zero unsigned cards in the chapter.

**See Decision 0e below** for the standing human question this leaves open (which division "the
Varga" means, if the source is ever otherwise clarified).

**Cross-book check (master prompt §14).** Brihat Jataka ch. 21 read in full (see above). No other
chapter of either converted book was searched beyond what the existing dependency registry already
pointed at. Brihat Jataka has no rule cards yet, so no `contradicts`/`parallel_of`/corroboration
link was created; the corroboration finding is prose only, in
`passage:phaladeepika.03.p052`'s deferred entry and `dep.varga-ownership`'s note, for whoever starts
that book's extraction.

**Testing.** `Engine/tests/test_varga.py`, 27 new tests: Navamsa-start for all twelve signs against
an independently-derived classical table (not the implementation's own formula); exact boundary
arithmetic within one sign (just-inside, just-outside, the last representable degree); Vargottama
positive/negative/boundary/no-cross-graha-contamination/all-twelve-signs; determinism (same input
twice); `dignity_in_varga` positive/negative, isolating the Navamsa alternative from the Rasi one
(Sun at 21° of Aries -- its own exaltation sign in Rasi -- lands on Navamsa 6, Libra, its
debilitation sign); one golden chart through the full pipeline where the new leaf fires a real
`PD.02.AdverseDisposition` claim *solely* via `dignity_in_varga`, not incidentally alongside one of
the card's six other leaves; and a direct ephemeris sweep (master prompt §17) of 2,609 weekly
instants, 1975-2025, confirming both `vargottama` and `dignity_in_varga` occur naturally in both
directions (neither always true nor always false) rather than only in hand-built fixtures. Existing
tests updated for the two newly-released cards' effect on the demo chart: `test_slice.py`'s claim
count (61 → 66: `PD.02.AdverseDisposition` fires for Jupiter/combust, Sun/Saturn/Rahu/inimical-sign
and Moon/8th-house -- no graha on that particular chart is debilitated in Rasi or Navamsa, so the
two new leaves this milestone added are not what fires there) and
`test_counting_and_nature.py`'s chapter-10 sign-off expectation (see above).

**Verification results.** `Rules/tools/verify.py`: clean -- 540 cards (was 537; +3 reference), 278
reference (was 274), 15 inert (was 17: `PD.09.Vargottama` released, `PD.02.AdverseDisposition`
released), `vargottama`/`in_varga_sign`/`dignity_in_varga` no longer listed as undeliverable,
`varga_owned_by` newly listed (1 card, as designed). `Rules/tools/dupes.py`: no duplicate
candidates. `Rules/tools/backlog.py`: 151 entries (was 139; +14 chapter-3 passages, +1 net
dependency-registry bookkeeping), 86 available now (was 72), every deferred item accounted for.
`Rules/tools/leverage.py`: `dep.varga` and `dep.vargottama` no longer appear in the blocked-
dependency table at all (resolved); `dep.varga-ownership` and `dep.dignity-in-varga` (immediately
resolved) appear as new entries. Full suite: 418/418 passing (was 391; +27 new).

**Production blockers cleared:** none of §A's named blockers. **Production-readiness impact:**
held, not moved -- three cards released (`PD.09.Vargottama`, `PD.02.AdverseDisposition`) and one
partial chapter slice (3 of 20 verses' worth of doctrine) is a small delta against the ~1,535-card
Phase-3 estimate, the same rounding-floor reasoning Milestones 24 and 26 gave for their own
few-card additions. Chapter 3 is **not** marked complete -- 8 of its 9 doctrine clusters remain,
tracked individually in `Rules/deferred.json`, not as one whole-chapter placeholder.

**Why this milestone matters.** It closes the two dependencies the master prompt named
(`dep.varga`, `dep.vargottama`) with the smallest capability the corpus actually justifies, and in
doing so it found -- rather than assumed -- that the capability's completion does not automatically
resolve every card that names it: one card it *does* release turned out to need a second, narrower
predicate first (`dep.dignity-in-varga`), and one card it does *not* release needed its stated
blocker corrected so the registry keeps telling the truth (`dep.varga-ownership`). Both are exactly
the reconciliation the master prompt asked for in §13, not a side effect it overlooked.

### Milestone 30 — `dep.dasa` built (Vimshottari mahadasa only); chapter 19 encoded; `PD.09.Dignity.Inimical` released and split

**Phase:** 2 (engine completion) + 3 (knowledge)
**Scope:** 1 new chapter file (`Rules/phaladeepika/ch19.json`, 4 reference cards, 9 firing cards),
1 chapter-9 card split into two (`PD.09.Dignity.Inimical` released, `.DasaEnmity` new), 5 new
`Engine` modules/mechanisms (`Engine/dasa.py`; `mahadasa_lord` predicate; `Claim.window`;
dasa-aware sort/render; a new Stage 9 window-grounding check), 2 new `Doctrine` accessors, 9
`Rules/deferred.json` entries added/resolved, 51 new tests (`Engine/tests/test_dasa.py`).
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**Candidate selection (master-prompt-style investigation, this session's actual brief).** Asked to
pick the next milestone from the live dependency graph, not `leverage.py`'s ranking, and to
specifically re-examine `dep.compound-friendship`, `dep.second-nativity`, `dep.transit` and
`dep.prashna`. Findings, each checked against the actual corpus and code rather than assumed:

- `dep.compound-friendship` — ch. 2 v.23 gives the full 6-row combination table explicitly, clean
  and deterministic. But its only registered payoff, `PD.06.Pushkala`, is *also* gated by the
  unresolved `dep.kendra-togetherness` reading question, so building it alone releases zero cards.
  A live, uncounted use was found at ch. 7 v.23 (a Raja Yoga via "Navamsa of an Adhimitra") — real,
  but ch. 7 isn't encoded yet, so the registry doesn't see it.
- `dep.second-nativity` / `dep.prashna` — each is justified by exactly one sentence in the whole
  corpus (ch. 10 v.7's "similar results may be declared from the wife's nativity"; ch. 2 v.36's
  reservoir-water horary rule). Building "a second chart through the whole pipeline" or a whole
  horary-branch mechanism for one verse each is the premature generalization a prior milestone's
  own standing guidance already warns against.
- `dep.transit` — real doctrine exists (ch. 16 vv.31-35, already encoded, uses transit language the
  `leverage.py` heuristic doesn't recognize; ch. 26 is the dedicated gochara chapter) but ch. 26
  itself is not yet encoded. Building the calculator now would be architecture speculating ahead of
  an as-yet-unread source chapter.
- Remaining chapter 3 — real doctrine, but most of what's left needs several new varga divisions
  (D3/D7/D10/D12/D16/D60), a 13-tier Vaiseshikamsa system, and an 11-state *percentage-weighted*
  Avastha system that runs straight into `dep.adjudication`, explicitly not scheduled (no invented
  numeric weighting, by design).
- `dep.dasa` — not named in the brief, surfaced by reading `Rules/deferred.json` directly. Ch. 19
  v.2 is a clean, fully deterministic classical table (nine grahas, years summing exactly to 120).
  v.3's balance dispute is narrow, not open (see below). It is Phase 2, not "beyond the MVP," and
  the largest real payoff of any candidate: it opens ch. 19 outright and unblocks ch. 20
  (`dep.lord-of-house` is already implemented) next, versus one card for every other candidate.
  Verified against `Engine/activate.py`/`rules.py`/`pipeline.py`/`render.py` line by line before
  committing to it, not assumed additive.

**Source read in full before writing anything.** `Knowledge/phaladeepika.md` ch. 19 (all 26
verses) and ch. 20 (skimmed for antardasa-formula sourcing — none found). Two encoding decisions
this forced:

1. **Verses 5-17 are NOT firing cards, on the source's own instruction.** V.17's own Notes say
   outright: *"the effects given in verses 5-17 are such as could be ascribed to the other dasa
   systems also... Therefore the effects given in verses 5-17 should not apply to Vimsottari dasa
   system."* Since `dep.dasa` builds specifically the Vimshottari engine, encoding vv.5-17 against
   `mahadasa_lord` would attach doctrine the source itself disclaims to a Vimshottari-computed
   window. vv.18-26 (the block the same Notes identify as Vimshottari-specific) became the nine
   firing cards instead; vv.5-17 are recorded as a deferred passage quoting the disclaimer verbatim.
2. **The balance-at-birth dispute (v.3) is narrow, not open.** The printed root verse states
   Mantreswara's own shortcut (divide by 60 always) — `PD.19.BalanceMethod.Mantreswara`, its
   `relation` deliberately spelled `dasa_balance_method_disputed` in code so the engine's own source
   file never names it directly (see `Engine/tests/test_slice.py::test_engine_names_no_book`, which
   this caught on the first pass). The same verse's own Notes reject it — *"not correct as the
   total number of ghatikas are not always 60"* — and give a degree/longitude restatement
   (`PD.19.BalanceMethod`, quoted in two spans across the p.175/176 page break) worked with a full
   numeric example the engine's own test suite reproduces to sub-day precision (Moon at Cancer
   13°12', 9°52' elapsed in Pushyami, Saturn's balance stated as 4y11m8d). The two are linked by
   `contradicts` — documentary only: neither ever fires as a claim (both justify a *computation*
   rather than assert something about a nativity), so `Engine.adjudicate`'s own rule (report a
   declared link only once at least one side has an activated claim) means it is on record in the
   store but never rendered in a per-chart consultation. A third, smaller gap — v.4 names a
   dasa-year as "a solar year" with no printed day-count — is filled with 365.25 days, recorded as
   engine arithmetic (`Engine/dasa.py::DASA_YEAR_DAYS`) rather than doctrine, the same category a
   prior milestone's ch. 1 v.3 note already assigned to method vs. doctrine.

**Architecture, verified rather than assumed additive.** `Claim` gained one new optional field,
`window`, confirmed safe because `Claim(...)` is constructed only once, by keyword, in
`activate.py::_claim`. The new predicate `mahadasa_lord(graha)` goes through the *ordinary*
condition/predicate machinery — zero changes to `rules.py::evaluate`/`build_predicate_index` — the
same shape `dignity`'s literal per-graha cards already use. All nine grahas' facts fire on every
chart unconditionally (the birth moment fixes the whole 120-year sequence, not "now"), which is why
no query-date input was added anywhere in the pipeline: a chart's dasa timeline is as fixed as its
planetary placements. `Engine/dasa.py` (new module) holds the pure arithmetic — nakshatra-lord
cycling, balance-at-birth, the nine-period sequence, and a JD→ISO calendar formatter (the forward
direction of the calendar math `Engine/chart.py` already does backward) — kept separate from the
thin `Engine/facts.py::_dasa` extractor, mirroring `_varga`'s own separation of "what a card states"
from "what the extractor computes." Which body's nakshatra the balance measures from (the Moon,
per v.3) is itself read from doctrine (`Doctrine.dasa_measured_from`, a new accessor), not written
as a Python literal — `test_no_doctrinal_constant_is_written_in_python[facts.py]` caught the first
draft's `chart.bodies.get("Moon")` before the first commit, the same discipline
`combustion_source` already applies to the Sun. `Engine/pipeline.py`'s claim sort and
`Engine/render.py`'s Part-2 house-grouping loop both assumed every claim was house-shaped; both
gained a small, additive branch routing window-bearing claims to their own chronologically-sorted
"Vimshottari Mahadasa Timeline" section instead of the "no house of its own" bucket the Ascendant
otherwise uses. `Engine/activate.py::verify_claims` (Stage 9) gained a sixth, additive check:
every window claim's dates are independently re-derived from the chart's own birth JD and Moon
position — not read back off the same `FactSet` Stage 6 already trusted — so a bug shared between
the extractor and the check would still be caught.

**A card released and split, not blindly released.** `PD.09.Dignity.Inimical` (ch. 9 v.17) had
been inert since encoding on a `graha: "any"` sentinel bug (matches no fact key, distinct from a
real `?`-prefixed variable) with `dep.dasa` among its declared blockers. With `dep.dasa` now
built, `Engine/tests/test_counting_and_nature.py::test_every_card_whose_dependencies_are_met_is_
no_longer_inert` correctly flagged it. Fixing the sentinel to `?g` (the same pattern its siblings
`PD.09.Dignity.Exalted`/`.OwnSign` already use) was mechanical, but the verse itself states two
distinct claims under one paragraph — general lifelong effects, and a further, dasa-scoped
sentence ("Even his friends will become his enemies in the dasa of such a planet.") — so the
mechanical fix alone would have either dropped the dasa-scoping or asserted it as an unconditional
effect the verse doesn't claim. Split at the sentence boundary into `PD.09.Dignity.Inimical`
(general, released) and a new `PD.09.Dignity.Inimical.DasaEnmity` (correlated via a shared `?g`
across `dignity(?g,inimical)` and `mahadasa_lord(?g)` — the first correlated dep.dasa condition in
the store, joined the same way `lord_of_house`/`in_house` already are elsewhere). Because
`mahadasa_lord(?g)` holds for every graha unconditionally, the join doesn't narrow which grahas
fire (both cards fire on the same set) — its distinctive content is that it attaches each firing
graha's own mahadasa window to the claim, which the general card does not carry.

**Testing (`Engine/tests/test_dasa.py`, 51 new).** Nakshatra→lord table against an independently-
known standard assignment (not re-derived from the groups-of-nine formula the extractor actually
runs); period-years table; balance-at-birth reproduced against the chapter's own worked example to
sub-day precision (the real oracle, not a synthetic one); full nine-period sequence boundary/
determinism/120-year-coverage checks; `jd_to_iso` round-tripped against the J2000.0 epoch; the
extractor exercised against the real production doctrine cards (`Doctrine.from_cards(load_cards
(RULES))`, the same production-store discipline `test_varga.py` established); a golden real chart
through the whole pipeline (nine windowed claims, chronologically sorted, correctly excluded from
the house-grouped/Ascendant sections, `verification.ok`); and a real-instant ephemeris sweep
(>1,600 dates, 1975-2025) confirming both near-zero and near-full balances occur naturally. Existing
tests updated: `test_slice.py`'s demo-chart claim count (66 → 81: +9 unconditional `PD.19.Dasa.*`,
+3 `PD.09.Dignity.Inimical` on the chart's known 3 inimical grahas, +3 its new sibling on the same
three) and a new `window_grounding_passed` check.

**Verification results.** `Rules/tools/verify.py`: clean — 554 cards (was 540; +13 ch.19, +1 net
from the PD.09 split), 282 reference (was 282; the ch.19 reference cards offset by none removed),
14 inert (was 15: `PD.09.Dignity.Inimical` released). `Rules/tools/dupes.py`: no duplicate
candidates. `Rules/tools/backlog.py`: 159 entries (was 151; +9 chapter-19 passages net of the
chapter entry resolved), 92 available now (was 86), every deferred item accounted for.
`Rules/tools/leverage.py`: `dep.dasa` no longer appears in the blocked-dependency table. One real
named chart (1987-03-14, Thanjavur) run end-to-end through the CLI and inspected by eye: the
rendered timeline is sequential and correctly dated from birth (a 1.5-year Ketu balance, a full
20-year Venus mahadasa, a 6-year Sun mahadasa with both `PD.19.Dasa.Sun` and `PD.09.Dignity.
Inimical.DasaEnmity` firing on it, since the Sun is inimically placed on this chart). Full suite:
469/469 passing (was 418; +51 new).

**Production blockers cleared:** none of §A's named blockers (there is no open P0). **Production-
readiness impact:** 59.00% → 59.60% ≈ 60% — see §A for the full row-by-row accounting. This is a
larger move than most recent milestones because `dep.dasa` is a genuine new calculator (one of the
four the "Reasoning engine capability" row names by name as missing) rather than a narrow reference
lookup, and because the new test file is materially larger (+51, ~12.2%) than the increments that
have held that row steady since Milestone 25.

**Why this milestone matters.** It is the first capability in this store that gives the engine a
temporal dimension — a claim that is true over a date range a chart's own birth fixes, not merely
true or false of a static placement — which is the piece every later dated-prediction-style
consultation ("career is strong during Jupiter's mahadasa...") needs before it can exist. Chapter
20 (dasa effects by house lord) is now genuinely ready, both of its dependencies implemented, and
is the explicit next-milestone pointer left in §D/the resume point above.

---

### Milestone 31 — Chapter 20's Mahadasa-scoped house-lord dasa doctrine encoded; no Antardasa mechanism built

**Phase:** 2 (engine completion, one small verdict extractor) + 3 (knowledge)
**Scope:** 1 new chapter file (`Rules/phaladeepika/ch20.json`, 34 cards: 1 reference, 33 firing),
1 new `Engine/facts.py` extractor (`_dasa_disposition`) and predicate (`dasa_disposition`), 1 new
`Doctrine` accessor (`dasa_effect_disposition_criteria`), 15 new `Rules/deferred.json` passage
entries plus 6 new dependency registrations, 1 new test file (`Engine/tests/test_chapter_twenty.py`,
21 tests), `test_slice.py`'s demo-chart accounting updated.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**The central question, settled before writing a single card.** The master prompt's own brief was
explicit: chapter 20 must be read directly, and an Antardasa engine must not be assumed necessary
just because the chapter's title says "and their Antar Dasas." All 63 verses were read in full
(`Knowledge/phaladeepika.md:4081-4345`), not the deferred-summary. Finding: **no Antardasa order or
duration arithmetic is printed anywhere in this chapter either**, confirming and extending Milestone
30's own note on `dep.dasa`. Verses invoking antardasa (vv.22c, 23, 28-29, 34-39, 42, 43-54, 59-62)
name *which* related planet's antardasa matters and *what effect* it carries — kendra/trikona
relationships, yogakaraka status, which nakshatra the antardasa lord rules — but never *how long* a
sub-period lasts or *in what order* the nine sub-lords run within a mahadasa. That is assumed
background knowledge the classical reader already has, not doctrine this corpus states. Per the
project's standing rule against filling a source gap from outside tradition, **no antardasa
mechanism — not even an order-only one — is built this milestone.** `dep.antardasa` is now formally
registered in `Rules/deferred.json` (`implemented: false`) rather than left as a note on `dep.dasa`,
so the gap is a tracked, named blocker rather than prose.

**Source matrix and scope decision.** The chapter splits into several genuinely distinct doctrine
clusters, not one uniform block — see the full verse-by-verse table this milestone produced (kept
in this session's working notes; the per-cluster reasoning is preserved instead in each
`passage:phaladeepika.20.*` deferred entry's own `reason` field, which is the durable record).
Confirmed with the user before encoding: the milestone's scope is the clean, purely Mahadasa-scoped
core — vv.2-13 (strong house-lord effects, houses 1-12), v.14 (the shared disposition clause gating
both directions), vv.15-20 (weak house-lord effects, split at the paragraph boundary into 12
house-specific cards since these verses print two houses per verse, unlike vv.2-13's one-per-verse
pattern), v.22's first two sentences (Vargottama effects in dasa), v.40's first sentence (maraka
houses), and v.41 (Parasara's kendra/trikona/upachaya/8th-lord dasa doctrine). Everything else —
the Antardasa-relational cluster, transit-during-dasa (needs `dep.transit`, ch. 26 itself still
unencoded), a "weakest of N candidates" death-timing cluster (no ranking/comparison mechanism exists
anywhere in this engine), v.30's explicit percentage-weighted dignity effects (hits the project's
standing no-invented-numeric-weighting refusal directly), vv.56-57's degree-position dasa-quality
doctrine (real, but needs a new predicate), vv.25-26/33 (need sign classifications this store has
not encoded), v.21's cross-chapter attribution meta-rule, and v.24's ordinal-dasa-position clauses
(small and genuinely buildable later from the already-computed `mahadasa_sequence()` with zero
antardasa, but explicitly excluded from this milestone by the user's own instruction) — is deferred
and individually tracked, not bundled into one vague line. 15 new `passage:phaladeepika.20.*`
entries were added to `Rules/deferred.json`, each naming the exact verses, the exact blocking
capability, and (where real) a newly registered dependency: `dep.antardasa`, `dep.mahadasa-ordinal`,
`dep.weakest-of-comparator`, `dep.degree-position-quality`, `dep.urdhvamukha-sign-class`,
`dep.rising-order-sign-class`.

**Two genuine source tensions, investigated and resolved by reading rather than assumed.**

1. **v.41 states "trikonas (1,5,9)"; the existing `PD.01.HouseClass.Trikona` reference card (ch.1
   v.18) defines Trikona as houses 5,9 only in this same book** — the Ascendant is classified
   `kendra`, not `trikona`, elsewhere in this book (ch.1 v.17). This is a genuine intra-book
   terminology inconsistency between two Phaladeepika passages, not an extraction error (both are
   byte-exact quotes). `PD.20.Parasara.TrikonaLord`'s condition uses v.41's own explicit house
   numbers (1, 5, 9) directly rather than a `house_class` lookup — the most literal reading of what
   this specific verse states, without silently picking a side on which definition of "trikona"
   governs generally elsewhere in the book. `PD.20.Parasara.UpachayaLordEvil` has the same shape in
   the other direction: v.41 names only houses 3, 6, 11, narrower than the store's own `upachaya`
   class (3, 6, 10, 11) — house 10 is deliberately excluded, matching the verse's own list.
   `Engine/tests/test_chapter_twenty.py::test_trikona_lord_conditions_on_the_verses_own_houses_
   not_house_class` and `::test_upachaya_lord_evil_excludes_house_ten` regression-pin both choices
   against a future "simplification" that would silently reintroduce the discrepancy.
2. **v.43 ("No planet produces good or bad effects to the native in accordance with the house he
   owns during his dasa and his own antar dasa") appears, on first reading, to flatly contradict
   vv.2-21's entire premise** — restated two verses earlier at v.41 as "Parasara's opinion." Read
   together with v.44, which immediately follows it ("Find out what all planets are related to the
   particular planet whose dasa is under consideration... It is only in the antar dasas of these
   planets that the original planet will in his main dasa manifest his effect"), this resolves: v.43
   specifically negates the dasa lord's *own* antardasa as the trigger, and v.44 states the real
   trigger is the antardasa of a *related* planet. This is an Antardasa-scoped refinement of *when
   within* a mahadasa the vv.2-21 effects manifest, not a denial that they exist. No `contradicts`
   link was drawn against vv.2-21/v.41 — that would overstate a tension the source's own adjacent
   sentence resolves — and vv.43-44 are recorded together in the antardasa-relational deferred
   entry with this reading documented, per the user's explicit instruction to investigate before
   deciding rather than assume the apparent contradiction was genuine.

**Architecture: one small, narrow verdict extractor, not a new stage.** v.14 states its own local
"auspiciously/inauspiciously disposed" criterion for whether a house lord's dasa effects actually
fire: auspicious = not placed in a dusthana AND (own sign, exaltation, or retrograde); adverse =
placed in a dusthana, OR (inimical sign, debilitation, or combust). This is **not** the same
criterion chapter 4's `strength` verdict already computes — confirmed by reading all three
`PD.04.Strength.*` / `PD.04.Weakness.Combust` cards in full before deciding: chapter 4's verdict has
no own-sign clause, no inimical-sign clause and no dusthana-placement clause, so it is verifiably
narrower than what v.14 states. Per Decision 1's own precedent (a chapter's own restated criterion
is encoded on its own terms, not folded into an existing verdict whenever the wording differs — the
user confirmed this explicitly before any card was written), a new predicate, `dasa_disposition`,
was built: `Engine/facts.py::_dasa_disposition`, mirroring `_strength`'s exact shape (reuses
`_dignity` and `_combustion`'s already-computed facts rather than recomputing dignity/combustion
logic locally; a graha satisfying both of v.14's clauses at once gets no verdict, the same collision
discipline `_strength` already applies for retrograde+combust, reported via `rep.conflict`/
`rep.incomplete` rather than silently dropped). One bug caught mid-session by cross-checking the
real DEMO chart's own output against the doctrine's own wording: the first draft only consulted
`_dignity`, which never emits "inimical" (that value is minted by the separate `_dignity_friendship`
extractor) — v.14's adverse clause explicitly names the inimical sign, so `_dasa_disposition` was
fixed to consult both, the same way `PD.02.AdverseDisposition`'s own condition already reads
whichever extractor produced a `dignity` fact from the assembled `FactSet`. New reference card
`PD.20.Disposition` (v.14, byte-verified) backs the new `Doctrine.dasa_effect_disposition_criteria`
accessor. This is the only new engine mechanism this milestone builds; `mahadasa_lord`,
`lord_of_house`, `dignity`, `combust`, `retrograde`, `house_class`, `nature`, `vargottama` and
`strength` are all reused exactly as-is. `v.40`'s maraka-house card (`PD.20.Maraka`) deliberately
reuses `strength(?g,strong)` rather than `dasa_disposition` — that verse states no local criterion
of its own ("powerful"), unlike v.14, so there is nothing to keep separate.

**A within-book duplicate-quote defect caught by `dupes.py`, fixed by design, not suppression.**
The first draft of `PD.20.Parasara.KendraLordBenefic`/`.KendraLordMalefic` quoted the identical full
sentence for both cards (the sentence states both the benefic and malefic clauses together), and
`PD.20.Parasara.EighthLordSun`/`.EighthLordMoon` did the same for the Sun/Moon sentence.
`Rules/tools/dupes.py`'s own SAME-QUOTE detector correctly flagged both pairs as within-book
encoding defects (its own documented policy: two cards from the same book sharing byte-identical
text is a defect, not corroboration, unlike a cross-book pair). Fixed two different ways, matching
what each sentence's own grammar supports: the kendra-lord sentence has a natural clause boundary
("...benefic natural benefic **and** auspicious or favourable if..."), so it was split into two
non-overlapping sub-quotes, each card citing only the clause it asserts. The Sun/Moon sentence names
both grahas together with no such boundary, so the two cards were merged into one,
`PD.20.Parasara.EighthLordSunMoon`, whose condition is `any` of two fully self-contained `all`
blocks (`{lord_of_house:Sun,8} + {mahadasa_lord:Sun}` OR the Moon equivalent) — the identical
top-level `any`-of-`all` shape `PD.02.Form.Mars.Youthful` already uses in this store, chosen
specifically because it cannot let Sun-owns-the-8th pair with a Moon mahadasa or vice versa
(confirmed by `test_eighth_lord_sun_moon_binds_each_graha_independently`). `dupes.py` is clean
after the fix; the final card count is 34, not the originally-planned 35.

**Testing.** `Engine/tests/test_chapter_twenty.py` (21 new): the doctrine accessor's exact
criteria, and that it vanishes without `PD.20.Disposition` (mirroring `test_strength.py`'s own
discipline); the extractor's auspicious path (own sign, exaltation, retrograde, each confirmed
not-a-dusthana), adverse path (debilitation; own sign *in* a dusthana confirmed NOT auspicious,
using Mercury in its own Gemini falling in this chart's 6th house), the retrograde+combust collision
(no verdict, and reported via `rep.conflict` rather than dropped); no disposition fact ever carries
a number; all 12 Strong/12 Weak cards bind the right house number and polarity; the trikona/upachaya
house-list regressions above; the `EighthLordSunMoon` binding-independence check; the real DEMO
chart's exact 17 `PD.20.*` claims (cross-checked against the chart's own `lord_of_house` facts, not
merely asserted), Rahu's real-chart collision (retrograde and inimical at once on this actual
nativity) confirmed to fire no card, all 17 claims carrying a window, and `PD.20.Maraka` confirmed
to condition on `strength` rather than `dasa_disposition`. `test_slice.py`'s demo-chart accounting
updated: claims 81 → 98 (+17, full breakdown in that file's own comment), `window_grounding_passed`
12 → 29 (every `PD.20.*` claim conditions on `mahadasa_lord(?g)`, so `activate.py`'s existing
generic window-carrying-fact scan populates `Claim.window` for all of them automatically — no
`render.py` change was needed; they render under the existing "Vimshottari Mahadasa Timeline"
section alongside ch. 19's own claims).

**Verification results.** `Rules/tools/verify.py`: clean — 588 cards (was 554; +34), 283 reference
(was 282; +1), 14 inert (unchanged), every paragraph of chapter 20 either quoted by a card or
claimed by a deferred-passage entry. `Rules/tools/dupes.py`: no duplicate candidates (after the
fix above). `Rules/tools/backlog.py`: 173 entries (was 159; +14 net of the one chapter entry
resolved), 98 available now (was 92). `Rules/tools/leverage.py`: regenerated. One real named chart
(1987-03-14, Thanjavur — the same chart Milestone 30 spot-checked) run end-to-end through the CLI
and inspected by eye: all 17 `PD.20.*` claims render correctly under the existing Vimshottari
Mahadasa Timeline section, each attached to the correct house lord's own window (e.g. Moon's
2014-2024 mahadasa carries both `PD.20.Weak.House7`, Moon owning the 7th with an adverse
disposition, and `PD.20.Parasara.KendraLordBenefic`, Moon being a benefic kendra lord). This one
chart happened to exercise both polarities and the collision case naturally (Mars/Ketu auspicious,
Moon/Saturn/Sun adverse, Rahu and Jupiter each colliding), so no additional ephemeris sweep was
needed to find a second chart. Full suite: 490/490 passing (was 469; +21 new).

**Production blockers cleared:** none of §A's named blockers (there is no open P0). **Production-
readiness impact:** 59.60% → 59.80% ≈ 60% — see §A for the full row-by-row accounting. Exactly one
category moved ("Rule extraction/encoding"); "Reasoning engine capability" deliberately held, since
`dasa_disposition` is architecturally the same *kind* of capability `strength` already established.

**Why this milestone matters, and why it stops here.** It closes the largest clean, source-backed
slice of chapter 20 without inventing any timing arithmetic the classical text does not itself
state — the discipline the master prompt most emphasized. Everything genuinely still in chapter 20
is now individually named and tracked, several as well-scoped, buildable-without-antardasa future
candidates (v.26, v.27, v.24's ordinal clauses, vv.56-57's degree-position doctrine) rather than one
undifferentiated "rest of the chapter" backlog line. `dep.antardasa` is a real, named, correctly
unimplemented dependency, not a gap that would silently look resolved the next time someone builds
any dasa-adjacent capability. Do not proceed to chapter 21 or another engine capability from this
session — `MILESTONES.md`'s own resume point (§D) governs the next session's starting point.

---

### Milestone 32 — Phaladeepika chapter 20 v.27 encoded; zero new engine capability

**Phase:** 3 (knowledge)
**Scope:** 2 new cards in the existing chapter file (`Rules/phaladeepika/ch20.json`, 0 reference, 2
firing), 1 `Rules/deferred.json` entry flipped from `deferred` to `resolved`, 2 reports
regenerated (`Reports/PHASE3_BACKLOG.md`, `Reports/PHASE3_PLAN.md`), 19 new tests in the existing
`Engine/tests/test_chapter_twenty.py`, `test_slice.py`'s demo-chart accounting updated. No
`Engine/*.py` file touched.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**Source, read directly rather than trusted from the prior deferral note.** Milestone 31 logged
v.27 at "printed p.186"; re-reading `Knowledge/phaladeepika.md` directly (chapter 20 spans lines
4081-4344) found the page anchor immediately preceding the verse is `phaladeepika/p0187`, not
p.186 — a small locus error in the original deferral entry, corrected on resolution rather than
propagated. The verse itself, in full: *"27. All benefics if placed in their sign of debilitation,
inimical signs or the 6th or 12th house, they will produce only adverse results while malefic
similarly placed will cause miseries during their dasa periods."* No Notes accompany it and no
authority is named — unlike v.14, v.24, v.34-39, this is a bare, self-contained sentence with
nothing to preserve separately per §11 of the master prompt.

**Scope matrix.** One sentence, two symmetric clauses joined by "while," sharing one condition:

| Clause | Subject | Condition | Timing | Effect | Authority | Executable? |
|---|---|---|---|---|---|---|
| 1st | benefics (`nature`=benefic) | debilitated OR inimical OR in house 6 OR in house 12 | own dasa (`mahadasa_lord`) | "produce only adverse results" | none named | yes, zero new capability |
| 2nd | malefics (`nature`=malefic) | same four-way disjunction ("similarly placed") | own dasa (`mahadasa_lord`) | "cause miseries" | none named | yes, zero new capability |

**The one interpretive step, taken and recorded.** v.27 names *exactly* the 6th and 12th house —
not the 8th. This store already has two broader groupings that would have been easy, wrong
substitutes: v.14's own `dasa_disposition` (adverse clause: debilitated, inimical, OR any
dusthana — 6th, 8th, **and 12th**) and the reference `house_class` table's own `dusthana`
definition (also 6, 8, 12). Reusing either would silently assert an 8th-house clause the verse
never states. Per the master prompt's own §9 instruction and the precedent
`PD.20.Parasara.UpachayaLordEvil` already set in Milestone 31 (naming exactly houses 3, 6, 11
against the broader `upachaya` class, which also includes the 10th), the condition is written
directly with two literal `in_house` leaves (6 and 12) rather than any house-class lookup, and this
is now a named, tested regression (`test_benefic_in_house_eight_alone_does_not_satisfy_the_
benefic_card` / the malefic equivalent, using a real placement — the Moon in Leo, a friend's sign,
falling in this chart's own 8th house). The verse also states no local disposition criterion of
its own the way v.14 does (no own-sign/exaltation/retrograde counterweight is offered), so this is
encoded as a flat four-way disjunction directly on `dignity`/`in_house`, not as a reuse of
`dasa_disposition` or `strength` — per the same concept:strength-criterion-scope precedent
Milestone 31 already established for v.14 and v.40 respectively.

**Two cards, split at the sentence's own clause boundary — not one, not four.** `PD.20.Placement.
BeneficAdverse` quotes "27. All benefics if placed in their sign of debilitation, inimical signs or
the 6th or 12th house, they will produce only adverse results"; `PD.20.Placement.MaleficMiseries`
quotes the remainder, "while malefic similarly placed will cause miseries during their dasa
periods." — the identical split-at-"while" pattern `PD.20.Parasara.KendraLordBenefic`/
`.KendraLordMalefic` already used in Milestone 31 for a structurally identical sentence, so the two
cards do not share a byte-identical quote (`dupes.py`'s own SAME-QUOTE check, confirmed clean).
Each card's `predicts.polarity` is the verse's own word for its own clause — `"adverse"` for
benefics, `"miseries"` for malefics — deliberately not collapsed to one shared generic value,
matching what each clause actually asserts (per the master prompt's §10 instruction against
overstating or flattening a source's own distinct language). Both conditions are otherwise
identical: `nature(?g,<benefic|malefic>)` AND `any[dignity(?g,debilitated), dignity(?g,inimical),
in_house(?g,6), in_house(?g,12)]` AND `mahadasa_lord(?g)` — the same `any`-nested-in-`all` shape
`PD.20.Maraka`/`PD.20.Vargottama.Mixed` already use in this chapter. "Inimical signs" reads as
`dignity(?g,inimical)`, sourced from `_dignity_friendship` rather than `_dignity` — the same fact
PD.20.Disposition's own note already established, confirmed again here rather than assumed.

**Engine: zero changes.** `nature`, `dignity`, `in_house` and `mahadasa_lord` are reused exactly as
declared in the deferred registry's own original assessment (`passage:phaladeepika.20.p027`,
`requires: ["dep.none"]`) — confirmed true before writing anything, not merely repeated. No
`Engine/*.py` file was touched this milestone.

**Dependency resolved.** `passage:phaladeepika.20.p027` flips from `deferred` to `resolved` in
`Rules/deferred.json`, its `reason` field rewritten to record the resolution, the corrected page
locus, and the 8th-house interpretive step (replacing the original entry's own imprecise "a
dusthana" paraphrase, which was the encoder's gloss and not something the verse states). No card
was released by this resolution: `backlog.py`'s "newly unblocked" list (9 entries, unchanged from
before this milestone, all pre-existing chapter/passage/concept entries stale since Milestones 22
and 31) names **0 cards**, so §13's re-diagnosis step found nothing to activate.

**Testing (`Engine/tests/test_chapter_twenty.py`, 19 new).** Source fidelity (verse "27", page
anchor `phaladeepika/p0187` — not the p.186 originally logged — the two quotes split at the clause
boundary with adjacent, non-overlapping spans, and the two `polarity` values confirmed to be the
verse's own distinct words). Condition semantics: each of the four disjuncts (debilitated,
inimical, house 6, house 12) isolated on a real placed graha and confirmed to satisfy its own card
independently, on both the benefic side (Jupiter, Venus) and the malefic side (Mars, Saturn) — all
placements are real chart configurations via `place()` on the standing DEMO chart, not synthetic
fixtures. The 8th-house boundary explicitly pinned NOT to satisfy either card (Moon in Leo/house 8
for the benefic side, Mars in Leo/house 8 for the malefic side, neither debilitated nor inimical).
False positives: a benefic and a malefic each satisfying none of the four clauses fire neither
card. `nature` confirmed to gate each card to its own polarity exclusively (a debilitated benefic
does not satisfy the malefic card and vice versa). Real-chart validation: the standing DEMO
nativity (1987-03-14, Thanjavur) has three malefics independently inimical — Sun, Rahu and Saturn,
the same three `dignity(?g,inimical)` facts `PD.09.Dignity.Inimical` already conditions on — each
firing `PD.20.Placement.MaleficMiseries` under its own correct mahadasa window (Sun 2008-2014,
Rahu 2031-2049, Saturn 2065-2084), confirmed by inspecting actual CLI output
(`python -m Engine.cli`) rendered under the existing "Vimshottari Mahadasa Timeline" section in
correct chronological order alongside every other claim in that graha's own mahadasa; no benefic
fires on this chart (Jupiter house 3/own sign, Moon house 8/friend's sign — the 8th-house exclusion
exercised naturally by a real chart rather than only a synthetic one, Venus house 1/friend's sign
all satisfy none of the four clauses). Every other `PD.20.*` claim count on the demo chart is
confirmed unchanged from Milestone 31 (regression-pinned in its own dedicated test). `test_slice.py`
updated: claim count 98 → 101 (+3, all `PD.20.Placement.MaleficMiseries`), `window_grounding_
passed` 29 → 32 (each new claim also conditions on `mahadasa_lord(?g)`, so `activate.py`'s existing
generic window-carrying-fact scan populates `Claim.window` automatically — no `render.py` change
needed). Full suite: 509/509 passing (was 490; +19 new).

**Verification results.** `Rules/tools/verify.py`: clean — 590 cards (was 588; +2), 283 reference
(unchanged), 14 inert (unchanged), every paragraph of chapter 20 either quoted by a card or
claimed by a deferred-passage entry. `Rules/tools/dupes.py`: no duplicate candidates. `Rules/
tools/backlog.py`: 173 entries (unchanged in count — one status flip, no new dependency), 97
available now (was 98 — v.27 stops being counted there once resolved, the same accounting
Milestones 25-27 already gave for their own resolved passages). `Rules/tools/leverage.py`:
regenerated, unaffected (v.27 needed `dep.none`, never appeared in the ranking). Full suite:
509/509 passing.

**Production blockers cleared:** none of §A's named blockers (there is no open P0). **Production-
readiness impact:** 59.80% ≈ 60%, unchanged — see §A for the full row-by-row accounting. 2 cards
is below "Rule extraction/encoding"'s own rounding (the same size as Milestone 26's own held
2-card move), and no engine mechanism was built at all, so "Reasoning engine capability" holds
exactly as declared rather than merely unmoved by rounding.

**Why this milestone matters, and why it stops here.** It closes a second clean, source-backed
chapter-20 passage using only capability the engine already had, and in doing so it names and
tests a real interpretive boundary (the 6th/12th-only condition, distinct from every existing
dusthana-shaped grouping in the store) rather than silently smoothing it into a more convenient
existing concept — exactly the discipline §7 and §9 of the master prompt asked for. Chapter 20's
remaining doctrine is unchanged in kind from Milestone 31's own accounting: v.26 is the next
zero-new-capability candidate, and everything else stays correctly blocked on a named, unimplemented
dependency. No new card was released, no source ambiguity required a human decision, and no
architectural change was needed — so per §22 of the master prompt, this is a natural stopping
point (case A: v.27 source-verified, encoded, tested and validated; case B: the "newly unblocked"
backlog list was checked and named 0 releasable cards). Do not proceed to v.26 or another chapter-20
passage from this session — `MILESTONES.md`'s own resume point (§D) governs the next session's
starting point.

---

### Milestone 33 — Phaladeepika chapter 20 v.24 items (1)-(3),(5) encoded; `dep.mahadasa-ordinal` built

**Phase:** 2 (engine completion) + 3 (knowledge)
**Scope:** `Engine/facts.py` gains one predicate (`mahadasa_ordinal`, ~10 lines including the new
`VOCABULARY` entry and its comment); 4 new cards in `Rules/phaladeepika/ch20.json` (0 reference, 4
firing); 3 existing cards (`PD.20.Strong.House6`/`.House8`/`.House12`) gain a reciprocal
`contradicts` field and a note; `Rules/deferred.json` gains one new dependency
(`dep.dasa-last-degree`) and one split-out passage entry
(`passage:phaladeepika.20.p024-lastdegree`), with `passage:phaladeepika.20.p024` and
`dep.mahadasa-ordinal` itself both flipped to resolved/implemented; 2 reports regenerated
(`Reports/PHASE3_BACKLOG.md`, `Reports/PHASE3_PLAN.md`); 27 new tests across
`Engine/tests/test_dasa.py` (6) and `Engine/tests/test_chapter_twenty.py` (21), plus small
regression updates to `test_adjudication.py`, `test_slice.py` and `test_chapter_twenty.py`'s own
demo-chart accounting.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**Source, read directly.** Ch. 20 v.24 in full (`Knowledge/phaladeepika.md`, printed p.186):
*"24. The following dasas will bring misery and trouble :- (1) The dasa of Saturn if it is the
fourth in the order of main dasas. (2) The dasa of Jupiter if it is the sixth (3) The dasa of the
Mars and Rahu if they are fifth. (4) The dasa of a planet who is placed in the last degree of a
sign. (5) The dasas of the lords of the 6th, 8th and 12th houses. Notes — If any body is born in
the dasa of Mars, Saturn's dasa will be the fourth for him. For one born in the dasa of Venus, Rahu
dasa will be fifth and Jupiter's dasa the sixth for him. For one born in the dasa of Ketu, Mars
dasa will be the fifth for him."* Located precisely via `Rules/tools/backlog.py`'s own `paragraphs()`
helper: paragraph 34 is the shared intro, 35-39 are items (1)-(5) one paragraph each, 40 is the
Notes — confirmed against the actual corpus text, not assumed from the deferred entry's own
paragraph list (which already had this right).

**Pre-implementation source matrix.**

| Clause | Subject | Condition | Timing | Effect | Executable now? |
|---|---|---|---|---|---|
| (1) | Saturn | ordinal position 4 in the birth-fixed mahadasa sequence | own dasa | misery and trouble | yes, `dep.mahadasa-ordinal` |
| (2) | Jupiter | ordinal position 6 | own dasa | misery and trouble | yes, `dep.mahadasa-ordinal` |
| (3) | Mars or Rahu | ordinal position 5 | own dasa | misery and trouble | yes, `dep.mahadasa-ordinal` |
| (4) | any graha | placed in the last degree of a sign | own dasa | misery and trouble | no — no numeral, no Notes, source gives no exact threshold |
| (5) | lords of houses 6, 8, 12 | none (unconditional) | own dasa | misery and trouble | yes, existing `lord_of_house` + `mahadasa_lord` |

Items (1)-(3) and (5) are the milestone's own scope; item (4) is split out and deferred (below).
None of the four are Antardasa-scoped — each names only "the dasa of X," never an antar dasa lord,
unlike vv.22-23/28-29/42-54's own cluster.

**Ordinal semantics, established from the Notes' own three worked examples, not assumed.** "Fourth
in the order of main dasas" is **not** a universal per-graha table (Saturn is not always the
fourth dasa of anyone's life) — it is a graha's 1-based position in the birth-fixed nine-period
Vimshottari sequence, **counted from the dasa the native was born in as position 1**. Verified
against all three worked examples directly: born in Mars's dasa, the sequence from
`PD.19.VimshottariPeriods`' own order (Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury, Ketu,
Venus) runs Mars(1), Rahu(2), Jupiter(3), **Saturn(4)** — matches "Saturn's dasa will be the
fourth." Born in Venus's dasa: Venus(1), Sun(2), Moon(3), Mars(4), **Rahu(5)**, **Jupiter(6)** —
matches both remaining clauses of that example. Born in Ketu's dasa: Ketu(1), Venus(2), Sun(3),
Moon(4), **Mars(5)** — matches the third example. All three checks pass exactly, confirming the
reading before a line of engine code was written, per the master prompt's own §8 instruction not to
assume a universal ordinal without the source establishing one.

**`dep.mahadasa-ordinal` built — the smallest source-backed capability, not a generic mechanism.**
`Engine/dasa.py::MahadasaPeriod` already carried an `ordinal` field (1..9, "order the periods run
in from birth") — built in Milestone 30 for `dep.dasa` and used internally by `mahadasa_sequence()`
itself, but never exposed as its own fact. `Engine/facts.py::_dasa` now emits a second fact per
period, `mahadasa_ordinal(graha, ordinal)`, alongside the existing `mahadasa_lord(graha)`, in the
same loop, reusing the same evidence dict — no new arithmetic, no new doctrine accessor (the order
is still read from `PD.19.VimshottariPeriods` via the same `Doctrine.vimshottari_periods()` call
`mahadasa_lord` already uses), no antardasa mechanism, no generic ranking or list-indexing facility.
`ordinal` is matched against a literal integer exactly the way `occupant_count`/
`seven_graha_sign_count` already match `n` — no new condition-language combinator. Confirmed, before
writing any card, that every relevant graha (all nine, including Rahu/Ketu) gets a unique 1-9
ordinal, deterministically, birth-fixed (no query-date input anywhere in `_dasa`, matching
`mahadasa_lord`'s own already-established invariant) — see `Engine/tests/test_dasa.py`'s six new
tests.

**Four cards.** `PD.20.MiseryDasa.SaturnFourth` (`mahadasa_ordinal(Saturn,4)` AND
`mahadasa_lord(Saturn)`), `.JupiterSixth` (`mahadasa_ordinal(Jupiter,6)` AND
`mahadasa_lord(Jupiter)`), `.MarsRahuFifth` (an `any`-of-two-`all` over Mars-ordinal-5 and
Rahu-ordinal-5, each binding its own graha across both conjuncts — the same shape
`PD.20.Parasara.EighthLordSunMoon` already established for Sun/Moon in one clause), and
`.DusthanaLords` (item (5): `lord_of_house` any-of-6/8/12 AND `mahadasa_lord`, zero new predicates,
the same explicit-literal-list discipline `PD.20.Parasara.UpachayaLordEvil` already set for its own
3rd/6th/11th list rather than importing the broader `house_class`/`dusthana` table). Both `mahadasa_
ordinal` and `mahadasa_lord` are always conditioned together on the same literal graha, so
`activate.py`'s generic window-carrying-fact scan (which looks for any bound fact whose evidence
carries `start`/`end`) and its Stage-9 window-grounding re-derivation (which specifically parses a
bound `mahadasa_lord(...)` key to recover the graha) both resolve correctly without any
`Engine/activate.py` change — confirmed by inspection of that module before writing the cards, not
assumed. Each ordinal card's quote is authored as two parts (the shared intro sentence plus the
item's own numbered clause), joined by the corpus's own ellipsis convention, so each card cites the
verse's own effect wording ("will bring misery and trouble") rather than asserting an effect its own
quote never states; `predicts.polarity` is `"misery_and_trouble"` on all four cards, the verse's own
compound phrase rather than a collapsed single word.

**The one interpretive step, taken and recorded.** `PD.20.MiseryDasa.DusthanaLords`'s claim is
unconditional — v.24 states no disposition, strength, or placement qualifier for item (5), unlike
vv.2-13's own house-lord dasa doctrine (gated by v.14's `dasa_disposition`). This means the card can
co-fire with `PD.20.Strong.House6`/`.House8`/`.House12` (vv.7/9/13, each gated on
`dasa_disposition: auspicious`) for a chart where a 6th/8th/12th lord is both strong and its own
mahadasa lord, asserting opposite outcomes (good vs. misery) for the identical graha's dasa.
Neither verse states which governs the other, and nothing in v.24 confines item (5) to a weak lord
the way v.14's own gate reads for vv.2-13's positive cases. Per the project's standing
preserve-disagreement discipline (`CLAUDE.md`: *"encode both as separate cards linked by
`contradicts`/`parallel_of`, and let `Engine/adjudicate.py` report the relationship"*), three
`contradicts` links were added both ways rather than left for Stage 3's lexical pass to silently
report the two as unrelated — exactly the defect `Engine/adjudicate.py`'s own docstring names as
its reason for existing. This reuses Stage 7's existing reading mechanism (Milestone 23) on a new
pair of cards; no new relationship type or weighting mechanism was built, and no adjudication was
invented — confirmed live on the real DEMO chart's own CLI output, where the relationship is
reported as `recorded` (the Strong.House6/8/12 side does not fire on this particular chart) rather
than `unresolved` or silently dropped. No tension exists against `PD.20.Weak.House6`/`.House8`/
`.House12` (vv.15-20's own adverse-disposition cards) — both predict a negative outcome for the
same graha, and are left independently co-firing exactly as the store already lets the Parasara
cluster and vv.2-21 cards overlap elsewhere without a link.

**Item (4) deferred, not silently dropped.** "The dasa of a planet who is placed in the last degree
of a sign" carries no numeral and no Notes — unlike items (1)-(3)'s three worked examples, nothing
in ch. 20 or ch. 4 states what band of degrees "last degree" means (the final whole degree,
29°-30°? a narrower Gandanta-style band? something else?). Per the master prompt's own §9
instruction not to invent an interval the source withholds, this is registered as a new dependency,
`dep.dasa-last-degree` (`Rules/deferred.json`, effort 2, `implemented: false`), and
`passage:phaladeepika.20.p024` is split: the original entry is resolved for items (1)-(3)/(5)
(paragraphs 34-37, 39-40), and a new entry, `passage:phaladeepika.20.p024-lastdegree` (paragraph
38), carries item (4) forward, `requires: ["dep.dasa-last-degree"]` — so the now-resolved portion
does not hide the genuinely still-open one behind a stale catch-all, per §17 of the master prompt.
This is deliberately a *different* gap from `dep.degree-position-quality` (vv.56-57's
Arohini/Avarohini doctrine, which compares a graha's longitude to its own exaltation/debilitation
points) — item (4) is about proximity to a sign's own boundary, not to those two fixed points, and
conflating the two would have been inventing a shared mechanism the source does not connect.

**Dependencies resolved.** `dep.mahadasa-ordinal` flips to `implemented: true` (`predicate:
"mahadasa_ordinal"`, so `Rules/tools/backlog.py::dependency_state` derives this automatically from
`Engine/facts.py` rather than trusting a hand-set flag). `passage:phaladeepika.20.p024` flips to
`resolved` for its own now-encoded scope. No card besides the four new ones was released:
`backlog.py`'s "newly unblocked" list (9 entries, unchanged in membership from before this
milestone, all pre-existing chapter/passage/concept entries stale since Milestones 22 and 31) names
**0 cards**, so §13's re-diagnosis step found nothing further to activate.

**Testing.** `Engine/tests/test_dasa.py` (+6): nine `mahadasa_ordinal` facts emitted per chart, each
of 1-9 present exactly once; all three of the Notes' own worked examples reproduced directly
against the extractor (not just `mahadasa_sequence()` in isolation); birth-fixed/deterministic
regardless of how many times the extractor is called; provenance (`evidence["doctrine"]`) identical
to `mahadasa_lord`'s own doctrine set; a direct cross-check against `mahadasa_sequence()` itself,
independent of the extractor's doctrine plumbing. `Engine/tests/test_chapter_twenty.py` (+21):
source fidelity (verse "24", page anchor `phaladeepika/p0186`, each ordinal card's quote confirmed
to carry the shared intro plus its own item, not one or the other alone); positive and negative
cases for each ordinal card via a synthetic `FactSet` isolating the condition logic from chart
geometry (already covered at the raw-extractor level in `test_dasa.py`); a cross-binding guard for
the Mars-or-Rahu `any`-of-`all` (mirroring the existing `EighthLordSunMoon` binding test) plus a
malformed-FactSet check that a missing `mahadasa_lord` pairing does not let the ordinal alone
satisfy a card; `.DusthanaLords` confirmed to fire for all three of a real chart's own 6th/8th/12th
lords and explicitly not for its lagna lord; the condition's own house list pinned to exactly
{6,8,12}; the three `contradicts` links confirmed present both ways; every firing claim on the DEMO
chart confirmed to carry a window. **Real-chart validation.** On the standing Thanjavur DEMO chart
(1987-03-14), Mars (this chart's own ordinal-5 mahadasa) fires `PD.20.MiseryDasa.MarsRahuFifth`
once, and the chart's three distinct 6th/8th/12th house lords (Mercury, Sun, Jupiter) each fire
`.DusthanaLords` once — `SaturnFourth`/`JupiterSixth` correctly do not fire (this birth's own
sequence does not put Saturn at 4 or Jupiter at 6), a genuine negative case rather than an untested
gap. Beyond DEMO, a direct ephemeris search (`SwissEphemerisDLL`, 40-year daily sweep from
1970-01-01) found two real birth instants for the ordinal cases DEMO does not exercise:
**1970-01-19** (Moon in Mrigashira, born in Mars's own dasa) fires `PD.20.MiseryDasa.SaturnFourth`;
**1970-01-16** (Moon in Bharani, born in Venus's own dasa) fires both `.JupiterSixth` and the Rahu
branch of `.MarsRahuFifth` — each run through the full `Engine.pipeline.run()` with
`verification.ok` confirmed `True` (quote integrity, condition re-evaluation, numeric grounding and
window grounding all pass), and the full `Engine.cli` output for the DEMO chart inspected directly,
confirming correct citation, page anchor, claim binding, and the `contradicts` relationship
correctly surfaced under "How the applicable passages stand to one another" (reported `recorded`,
not `unresolved`, since `Strong.House6`/`.House8`/`.House12` do not fire on this particular chart).
`test_adjudication.py` updated for the three new catalogued pairs; `test_slice.py`'s claim count
(101 → 105, +1 MarsRahuFifth +3 DusthanaLords) and `window_grounding_passed` (32 → 36) updated with
the full per-card accounting; `test_chapter_twenty.py`'s own demo-chart PD.20 tally (20 → 24). Full
suite: 536/536 passing (was 509; +27 new).

**Verification results.** `Rules/tools/verify.py`: clean — 594 cards (was 590; +4), 283 reference
(unchanged), 14 inert (unchanged), every paragraph of chapter 20 either quoted by a card or claimed
by a deferred-passage entry. `Rules/tools/dupes.py`: no duplicate candidates across 594 cards.
`Rules/tools/backlog.py`: 174 entries (+1, the last-degree split), 97 available now (unchanged —
item (4) was already counted there before the split and is counted there again under its new id).
`Rules/tools/leverage.py`: regenerated; `dep.mahadasa-ordinal` has dropped off the ranking entirely
(implemented), `dep.dasa-last-degree` appears with 0 blocked cards (nothing yet declares it besides
the split-out passage entry itself). Full suite: 536/536 passing.

**Production blockers cleared:** none of §A's named blockers (there is no open P0). **Production-
readiness impact:** 59.80% ≈ 60%, unchanged — see §A for the full row-by-row accounting. 4 cards is
below "Rule extraction/encoding"'s own rounding; the one new predicate is a pure lookup into an
already-computed value, held under the same "same mechanism, more instances" precedent that has
governed "Reasoning engine capability" since Milestone 24; the three new `contradicts` links reuse
Stage 7's existing reading mechanism, the same reasoning that held "Contradiction handling" for
Milestone 25's own second cluster.

**Why this milestone matters, and why it stops here.** It closes the ordinal-dasa clauses the
project's own dependency registry had named as the next well-scoped, source-safe chapter-20
candidate since Milestone 31, confirms the ordinal reading against all three of the verse's own
worked examples before writing a line of engine code (rather than importing the conventional
Vimshottari ordinal reading from outside the corpus), and surfaces a genuine same-book doctrinal
tension (item (5) vs. vv.7/9/13) as a recorded relationship instead of two claims that would
otherwise have silently disagreed on a real chart. Item (4) is a clean stopping point in its own
right (master prompt §23, case B: the source does not provide enough evidence for exact executable
semantics) rather than a reason to invent a threshold and keep going. No architectural decision was
needed, and the "newly unblocked" backlog list named 0 releasable cards, so per §22 of the master
prompt this is a natural stopping point. Do not proceed to v.25/v.26 or another chapter-20 passage
from this session — `MILESTONES.md`'s own resume point (§D) governs the next session's starting
point.

---

### Milestone 34 — Phaladeepika chapter 20 v.26 encoded (`PD.20.WealthDasa.Venus`); zero new engine capability

**Phase:** 3 (knowledge)
**Scope:** 1 new card in `Rules/phaladeepika/ch20.json` (0 reference, 1 firing); `Rules/deferred.json`'s
combined `passage:phaladeepika.20.p025-026-033` entry split into three (`p025`, `p026` resolved,
`p033`); 2 reports regenerated (`Reports/PHASE3_BACKLOG.md`, `Reports/PHASE3_PLAN.md`); 19 new
tests in `Engine/tests/test_chapter_twenty.py`. No `Engine/*.py` change.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**Source, read directly.** Ch. 20 v.26 in full (`Knowledge/phaladeepika.md`, printed pp.186-187,
the sentence crossing the page break mid-word): *"26. If Venus be in his sign of exaltation or in
his own sign and be posited in the 10th, 11th or the 12th house, uneclipsed and free from the
influence of a malefic, the native during his dasa, will become very wealthy, will be full of
glory and splendour and will be endowed with gold and precious stones etc., will be widely praised
and enjoy all comforts."* Located via `Rules/tools/backlog.py`'s own `paragraphs()` helper:
paragraph 42 is the sentence's first half (up to the page break), 43 is its continuation — the
paragraph splitter treats the mid-sentence page anchor as its own boundary, confirmed by direct
inspection rather than assumed from the original deferred entry's combined paragraph list
(`[41, 42, 43, 52]`, which turned out to be v.25(41) + v.26(42-43) + v.33(52) exactly, with v.27-32
each already separately tracked elsewhere in the registry). No Notes and no competing authority
accompany v.26 — confirmed by reading the surrounding text directly, not assumed from the original
deferral's silence on the point.

**Scope confirmation.** The master prompt's default scope (v.26 only) was verified, not assumed:
v.25 (Mars/Urdhvamukha) and v.33 (Jupiter-kendra / Shirshodaya-Ubhayodaya-Prishtodaya) each still
need a sign classification this store has never built (`dep.urdhvamukha-sign-class`,
`dep.rising-order-sign-class` respectively), so pulling either in would have meant inventing a
sign-class table the source does not yet make queryable — declined, per the master prompt's own
§3 instruction not to expand scope without the source and architecture justifying it.

**Pre-implementation source matrix.**

| Clause | Subject | Condition | Timing | Effect | Executable now? |
|---|---|---|---|---|---|
| dignity | Venus | exalted OR own sign | — | (gates the claim) | yes, existing `dignity` |
| placement | Venus | in house 10, 11 or 12 | — | (gates the claim) | yes, existing `in_house` |
| uneclipsed | Venus | not combust | — | (gates the claim) | yes, existing `combust` |
| unafflicted | Venus | not conjunct/aspected by a malefic | — | (gates the claim) | yes, existing `conjunct`/`aspects`/`nature` |
| dasa | Venus | (the four gates above) | Venus's own mahadasa | very wealthy, glory, splendour, gold and precious stones, widely praised, all comforts | yes, existing `mahadasa_lord` |

One rule, five conjuncts, one graha, one effect sentence — not multiple independent clauses, and
not split further: the verse states one continuous condition for one continuous effect.

**Primitive mapping, each read from the book's own words, not imported.** "His sign of exaltation
or in his own sign" is `dignity: exalted` OR `dignity: own` — `Engine/doctrine.py`'s own table
gives Venus's exaltation sign (Pisces) and owned signs (Taurus, Libra), not hand-derived here.
"10th, 11th or the 12th house" is `in_house` 10/11/12, Venus's own placement counted from the
lagna — the same frame every other chapter-20 placement card already uses, and the verse says only
"house," not house *ownership*. "Uneclipsed" is `not combust(Venus)`, corroborated **twice inside
this same chapter** rather than imported from outside it: v.19's own parenthetical ("If a planet be
combust (eclipsed by the Sun's rays)...") and v.22's second sentence ("is in his sign of
deblitation or is eclipsed by the Sun's rays," already encoded as `combust` on
`PD.20.Vargottama.Mixed`, Milestone 31) both equate "eclipsed by the Sun's rays" with `combust` in
this book's own vocabulary. "Free from the influence of a malefic" is read as NOT (conjunct with a
malefic OR aspected by a malefic) — the book's own equivalence for "influence," found at ch.9's
"hemmed in between malefics or be associated with or aspected by malefics... devoid of any
influence of benefics" (corpus line 3338, an unencoded passage but the only other place in the
whole corpus where "influence" pairs with "malefic"/"benefic"): "associated with" = `conjunct`,
"aspected by" = `aspects`, so "influence" is their disjunction, negated here. The negation is a
`not` wrapping an `any` of two `all`s, each over a free `?m` — the identical negation-as-failure-
over-a-variable idiom `PD.06.PanchaMahapurusha.Ruchaka` already uses for its own "not conjunct with
a malefic" clause, and `Engine/rules.py`'s own `not`-combinator docstring names exactly this use
("if there is no planet in the Ascendant"). No `nature` gate is placed on Venus itself — Venus is
the sole named subject, not a free graha variable the way v.27's benefic/malefic cards are.
"During his dasa" is `mahadasa_lord(Venus)`, exactly as v.22's and v.27's own cards already read
the same phrase. **Zero new predicates, zero engine change**: `dignity`, `in_house`, `combust`,
`conjunct`, `aspects`, `nature` and `mahadasa_lord` are all pre-existing, confirmed against
`Engine/facts.py` before authoring rather than assumed from the deferred entry's own (correct)
prediction. `predicts.polarity` is `"very_wealthy"`, the verse's own lead effect word — matching
the terse source-drawn tokens (`misery_and_trouble`, `adverse`, `miseries`, `mixed`) already used
elsewhere in this chapter rather than a synthesised summary of the fuller sentence; the full
sentence (glory, splendour, gold, precious stones, being widely praised, all comforts) is preserved
verbatim in the quote, not compressed into `predicts`.

**One card.** `PD.20.WealthDasa.Venus`: `dignity(Venus,{exalted,own})` AND
`in_house(Venus,{10,11,12})` AND `not combust(Venus)` AND
`not (conjunct(Venus,?m) AND nature(?m,malefic)) OR (aspects(?m,Venus) AND nature(?m,malefic))`
AND `mahadasa_lord(Venus)`. No Notes, no competing authority, and no existing card in the store
conditions on a literal Venus placement the way this one does, so there was nothing to preserve
separately and no duplicate or contradiction to record (`Rules/tools/dupes.py`: clean across 595
cards).

**Deferred entry split, not silently resolved as a whole.** The original combined entry,
`passage:phaladeepika.20.p025-026-033` (Milestone 30), covered three unrelated verses under one
`requires` list naming both sign-class dependencies — a catch-all the master prompt's §19
instruction flags directly. It is now three entries: `passage:phaladeepika.20.p025` (v.25,
`requires: ["dep.urdhvamukha-sign-class"]`, paragraph 41), `passage:phaladeepika.20.p026` (v.26,
now `resolved`, paragraphs 42-43), and `passage:phaladeepika.20.p033` (v.33, `requires:
["dep.rising-order-sign-class"]`, paragraph 52) — the same split-a-resolved-portion-out-of-a-
combined-entry pattern Milestone 33 used for v.24's own item (4). v.33's first sentence (Jupiter/
Moon-sign-lord/lagna-lord in kendra) is not itself sign-class-gated, but re-splitting that verse's
own two clauses is a genuine encoding decision left for whichever future session actually resolves
`dep.rising-order-sign-class` or decides to encode v.33's first sentence on its own — not a
bookkeeping correction to make in passing here, and recorded as such in `p033`'s own `reason`
field so it is not silently lost.

**No card newly released.** `Rules/tools/backlog.py`'s "newly unblocked" list (9 entries, unchanged
in membership from Milestone 33 — the same pre-existing chapter/passage/concept entries stale since
Milestones 22 and 31) names **0 cards**, confirming §15's re-diagnosis step found nothing further
to activate. v.26 built no new dependency and no new predicate, so nothing else in the registry
could have been unblocked by it.

**Testing.** `Engine/tests/test_chapter_twenty.py` (+19): source fidelity (verse "26", page anchor
`phaladeepika/p0186`, quote starts "26. If Venus be in his sign of exaltation" and ends "enjoy all
comforts.", no `contradicts`/`extends`/`parallel_of`); each of the five conjuncts isolated with a
synthetic `FactSet` (`_venus_factset`, mirroring `_ordinal_factset`'s own isolation rationale) —
exalted+house10 fires, own+house11 fires, own+house12 fires, debilitated does not, own-sign-in-
house-9 (a trikona this verse does not name) does not, combust does not, malefic-conjunct does
not, malefic-aspect does not, a **benefic** conjunction does *not* block it (the verse names only a
malefic's influence), and a missing `mahadasa_lord` fact does not; a condition-shape regression pin
confirming the dignity `any` names exactly `{exalted, own}` and the house `any` names exactly
`{10, 11, 12}`, with no `house_class`/`in_house_class` anywhere in the condition. **Real-chart
validation**, both a live regression against the standing DEMO chart and a genuine ephemeris
search: on the real Thanjavur DEMO chart, moving only Venus to Libra (`place(chart, "Venus",
190.0)`) puts it in its own sign in house 10 — but the chart's own unmoved Mars aspects that
degree, so the card correctly withholds the claim, a real (not synthetic) false-positive control.
A direct ephemeris search (`SwissEphemerisDLL`, Chennai, 1990) found three genuine positive birth
instants, one for each named house — **1990-06-26 10:00** (Venus own sign, house 10),
**08:00** (house 11) and **06:00** (house 12) — each run through the full `Engine.pipeline.run()`
with `verification.ok` confirmed `True`, exactly one `PD.20.WealthDasa.Venus` claim, a correctly
bound 20-year Venus mahadasa window (2002-06-30 to 2022-06-30), and the claim correctly grouped
under the "Venus mahadasa" heading in the real `Engine.cli` consultation output (inspected
directly). The same search also produced a genuine negative control, **1990-04-30 05:00** —
Venus exalted in house 12, otherwise qualifying, but Saturn aspects it, so no claim fires
(`verification.ok` still `True`). A final regression pin confirms the DEMO chart's own
PD.20.* claim count is unchanged at 24 (`PD.20.WealthDasa.Venus` does not fire there — Venus is
neither exalted nor own-sign on that chart) and every other PD.20 card is unaffected. Full suite:
**555/555 passing** (was 536; +19, all in `test_chapter_twenty.py`, confirmed by isolating the
file's own count before and after via `git stash`).

**Verification results.** `Rules/tools/verify.py`: clean — 595 cards (was 594; +1), 283 reference
(unchanged), 14 inert (unchanged), every paragraph of chapter 20 either quoted by a card or claimed
by a deferred-passage entry. `Rules/tools/dupes.py`: no duplicate candidates across 595 cards.
`Rules/tools/backlog.py`: 176 entries (+2, the three-way split of the combined entry), 97 available
now (unchanged — the split moved paragraph-level bookkeeping, not availability). `Rules/tools/
review.py --queue`: 593/595 cards signed off (283 structural + 310 interpretive, was 592/594),
the same two standing holdouts (`PD.01.Kalapurusha.Strength`, `PD.04.Lagna.TripedSign`)
unchanged. `Rules/tools/leverage.py`: regenerated; `dep.urdhvamukha-sign-class` and
`dep.rising-order-sign-class` both still show 0 cards solely blocked (each still names exactly the
one card it always did — v.25 and v.33 respectively — the split changed which passage entry
declares the requirement, not how many cards are waiting on it).

**Production blockers cleared:** none of §A's named blockers (there is no open P0). **Production-
readiness impact:** 59.80% ≈ 60%, unchanged — see §A for the full row-by-row accounting. 1 card is
smaller than every prior addition this table has ever credited, well below "Rule extraction/
encoding"'s own rounding; zero new predicates or engine change leaves "Reasoning engine capability"
untouched; the +19 tests are proportionally smaller than the deltas that have moved "Test coverage"
before and match this row's own established "held, not moved" precedent (Milestones 24, 26, 31,
32, 33).

**Why this milestone matters, and why it stops here.** It closes the one member of the three-verse
`p025-026-033` deferral that the registry had correctly named as fully executable since Milestone
30, resolves it without silently carrying its two still-blocked neighbours along under a stale
combined entry, and demonstrates (twice, inside the same chapter) that "eclipsed by the Sun's rays"
is this book's own name for `combust` rather than an assumption imported from outside the source —
the same discipline Milestone 33 applied to its own ordinal-dasa worked examples. Both v.25 and
v.33 remain clean stopping points in their own right (master prompt §24, case B: each needs a
genuinely unbuilt sign classification, not a guessed interval), not a reason to invent a
classification and keep going. No architectural decision was needed, and the "newly unblocked"
backlog list named 0 releasable cards, so per §24 of the master prompt this is a natural stopping
point. Do not proceed to v.25, v.33, v.24 item (4), Antardasa, or another chapter-20 passage from
this session — `MILESTONES.md`'s own resume point (§D) governs the next session's starting point.

---

### Milestone 35 — Developer frontend + local API adapter (`Api/`, `Frontend/`); zero doctrine change, one small additive engine plumbing helper

**Phase:** infrastructure (not Phase 3 knowledge work — see §31's own instruction not to treat a
frontend milestone as astrology progress). Driven by a separate master prompt
(`Vedic_AI_Frontend_Consultation_Interface_Master_Prompt.md`), not by the leverage-ranked backlog.
**Scope:** new `Api/` package (FastAPI adapter, 5 files + 5 test files, 24 tests), new `Frontend/`
package (Vite + React + TypeScript, 12 components + 5 test files, 21 tests), new `docs/FRONTEND.md`,
new root `requirements.txt` (none existed before), `.gitignore` extended for `Frontend/node_modules/`
/`Frontend/dist/`/`.env`. One additive `Engine/dasa.py` function
(`chart_mahadasa_timeline`), `Engine/activate.py`'s `_recompute_window` refactored to call it instead
of duplicating its own two lines of doctrine lookup. No `Rules/*.json` change, no new predicate, no
new card, no doctrine read or written.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**What was built.** A local developer inspection UI over the existing 11-stage engine —
`Birth Input (React) -> POST /consult (FastAPI) -> Engine.pipeline.run() [unchanged] -> Api/
serialize.py -> 13 React views over one JSON payload`. `Api/app.py` exposes `GET /health`,
`POST /consult`, `GET /cards/{card_id}`, `GET /deferred`, and `GET`/`POST /cases` (local, uncommitted
test-chart manifests under `Cases/<slug>/chart.json`, reusing the existing gitignored `Cases/`
convention rather than inventing a parallel one). `Api/serialize.py` extends `Engine/cli.py`'s own
existing `--json` dataclass-to-dict adapter (which covered `chart`/`facts`/`claims`/`coverage`/
`verification`) to also cover `adjudications`, `sentences`/`synthesis`, `audit`, and a new
`dasa_timeline` array — the full nine-period Vimshottari sequence with each period's own claims
attached by exact `Claim.window` match, pure JSON grouping over data the engine already produced.
`Frontend/` renders all 13 required views (birth input, chart summary, claims explorer with full
provenance, dasa timeline, adjudication view, a deferred/unsupported view that keeps "not
triggered"/"not computable"/"reference only"/"source unresolved" visibly separate rather than
merging them into one invented status, fact inspector, rule inspector, verification view,
comparison mode, chart view, and local test-chart save/load) as a plain view of that one JSON
payload — no astrology computation exists anywhere in `Frontend/` or `Api/`.

**The one engine change, and why it is not a doctrine change.** §10's dasa-timeline view needs the
full nine-period Vimshottari sequence; `Engine/activate.py::_recompute_window` already computed
exactly that sequence internally (for Stage 9's own window re-derivation) and then discarded every
period but one. `Engine.dasa.chart_mahadasa_timeline(chart, cards)` is those same two calls
(`Doctrine.from_cards(cards).vimshottari_periods()` then `mahadasa_sequence(...)`) pulled out as
their own function, returning `[]` rather than raising where the doctrine is absent or the Moon is
missing — the same two "no periods" cases `_recompute_window` already treated identically.
`_recompute_window` was rewritten to call it and filter to one graha, removing the duplicate copy of
the same arithmetic rather than adding a second one. Zero new predicate, zero new card, zero
behavior change for any existing caller, verified by the full existing `Engine/tests` suite passing
unchanged (559/559, was 555/555 — the +4 are new tests *for* this function, in `Engine/tests/
test_dasa.py`, not evidence anything changed for an existing consumer) plus a direct cross-check
against `mahadasa_sequence` and against the golden chart's own `PD.19.Dasa.*` claim windows.

**Architecture decisions, each made from the repository's own state rather than assumed.** Two
parallel reconnaissance passes plus direct reads of `Engine/pipeline.py`, `activate.py`,
`adjudicate.py`, `dasa.py`, `chart.py`, `facts.py`, `rules.py` established: the repo had zero web
framework, zero `requirements.txt`, zero existing frontend (no `package.json`, no JS/HTML/CSS
anywhere), and zero existing server code — a blank slate with nothing to reuse and nothing to
conflict with. `Engine.pipeline.run(BirthRecord, ...) -> Result` was already a single, directly
importable entrypoint; no code change to the engine's own call contract was needed to reach it.
FastAPI + uvicorn were chosen for the thin adapter (typed request validation distinguishing
`BirthDataError`/`EphemerisError`/`PipelineError`'s two distinct failure messages from each other,
with no new server plumbing beyond `.venv`); Vite + React + TypeScript for the frontend (Node/npm
already installed and otherwise idle; the 13 required views are stateful enough — expand/collapse
trees, a two-chart comparison mode — to make plain server-rendered HTML unwieldy to keep correct,
not stateful enough to justify a router or a state library). No `/chart` endpoint was built: the
engine has no cheaper partial-pipeline entrypoint, so a chart view is a client-side projection of
`/consult`'s one response, the correct reading of the master prompt's own "only create endpoints
actually needed."

**A stale fixture found, not silently trusted.** `Cases/demo/trace.json` (the project's own standing
demo-chart snapshot) shows 9 claims for the Thanjavur 1987-03-14 birth record; both the live CLI and
the live API produce 105 claims for the identical input today. The file predates most of the current
595-card store and was never regenerated as chapters were added — confirmed by running the live CLI
against the same input during this milestone, not assumed. `Api/tests/test_regression_vs_cli.py`
therefore compares live CLI output to live API output *in the same test run* rather than pinning
against that stale file, which would have asserted agreement with something already known wrong.

**Testing.** `Api/tests/` (24 tests, 5 files): health; `/consult` response shape against every field
the master prompt's screens need; the live CLI-vs-API regression comparison (claim ID sets, rule
cards, chart `bundle_id`, verification status, coverage counts — all equal); `/cases` round-tripping
against a `tmp_path`-monkeypatched root (real `Cases/` never touched by the suite); the full error
taxonomy (`BirthDataError`->400, `EphemerisError`->502, rule-store/groundedness/generic
`PipelineError`->500 with distinct `error_type`s, pydantic validation->422). `Frontend/` (21 tests,
5 files, Vitest + React Testing Library): birth-form validation/submit states, loading/error states
with `fetch` mocked, claims-explorer expand/collapse, dasa-timeline nine-period rendering, and
`ComparisonMode`'s diff logic tested as a plain exported function independent of React (claims are
diffed by `(rule_card, bound variables)`, not by `claim_id` — confirmed by reading
`Engine/activate.py::_claim` that `clm-0001` is a per-run sequential index, not a stable identity
across two different charts, so a raw-id diff between two charts would have been meaningless noise).

**Real end-to-end verification, in a real browser.** Both servers were started locally
(`.venv/Scripts/python.exe -m uvicorn Api.app:app`, `npm run dev` in `Frontend/`) and driven with a
headless Chromium (Playwright) through the full flow against the real Thanjavur demo birth record:
filled the birth form, submitted, and confirmed the Chart Summary (105 claims, 0 warnings, "OK —
grounded"), Claims Explorer (105 expandable claims with full quote/provenance), Dasa Timeline (9
periods, "Antardasa not implemented — deferred" labelled explicitly), Adjudications (13, grouped by
resolution), Deferred view (per-chart inert/reference/not-covered sections kept visually separate
from the repository-wide `/deferred` registry), Verification ("GROUNDED — every check passed" in an
unmistakable success state), and Chart view (houses 1-12, graha placements) all rendered real data
correctly, with zero browser console errors. Screenshots taken at each step, inspected directly —
this is genuine visual verification, not a build/type-check standing in for one.

**Verification results.** `Rules/tools/verify.py`/`dupes.py`/`backlog.py`/`leverage.py`: all clean,
identical output to Milestone 34's own (595 cards, 176 backlog entries, 97 available now — nothing
here touches doctrine). `.venv/Scripts/python.exe -m pytest Engine/tests Api/tests -q`: **583/583
passing** (559 engine + 24 api). `npm test` in `Frontend/`: **21/21 passing**.
`npm run build`: zero TypeScript errors.

**Production blockers cleared:** none of §A's named blockers (there is no open P0) — this milestone
touched none of them by design. **Production-readiness impact:** "CLI/API/user-facing readiness"
moves 40%→60% (+0.01 × 20 = +0.20 pts on the 59.80 baseline, 59.80 + 0.20 = 60.00 ≈ 60% — the
headline figure does not visibly move, because this row's weight is 1%): the row's own stated gap,
"no API, no UI, no packaging," is now half-closed — a working local API and a working local
developer UI covering every view the master prompt specified now exist, verified end-to-end in a
real browser. Not higher, because the row's remaining gap is real and untouched: no packaging or
installer, no authentication or multi-user surface, no production deployment or hosting, and no
external/systematic user testing beyond this session's own verification. Every other row is
untouched by this milestone for the same reason Milestone 28's read-only investigation held every
row: no card was added, removed, or reworded (Corpus completeness, Rule extraction, Multi-book
corroboration all untouched); no new predicate or stage was built for the engine's own doctrine
reasoning (Reasoning engine capability untouched — `chart_mahadasa_timeline` is a pure refactor of
existing arithmetic, not new capability); no relationship type or card changed (Contradiction
handling untouched); no card's quote or hash changed (Provenance/auditability untouched at
593/595); the "Test coverage" row is scoped to `Engine/tests` by this table's own established
convention and that suite's own pass count (559, was 555) moved only by the +4 tests *for* the one
additive dasa-timeline helper, smaller than the deltas that have moved that row before; "End-to-end
validation" is scoped to chart-space evidence about the doctrine, not the presence of a UI (the new
`Api`/`Frontend` test suites are a different kind of evidence, credited above under "CLI/API/
user-facing readiness" rather than double-counted here).

**Why this milestone matters, and why it stops here.** It gives the project a real, working
transparent inspection surface — every one of the master prompt's 36 sections' requirements are met
end-to-end and verified, not merely built — without touching a single rule card, predicate, or
doctrine reading, and without inflating the astrology-progress percentage the way §31 explicitly
warns against. Per the master prompt's own §35/§36, this stops here: do not proceed into another
astrology milestone from this session. `MILESTONES.md`'s Phase-3 resume point (§D, below) is
untouched by this milestone and remains exactly where Milestone 34 left it.

---

### Milestone 36 — Phaladeepika chapter 7 slice 1: the Neechabhanga Raja Yoga family (vv.26-30)

**Phase:** 3 (knowledge extraction), zero Phase 2/4 change
**Scope:** New `Rules/phaladeepika/ch07.json` (6 cards); `Rules/phaladeepika/manifest.json` (chapter 7
added to `chapters_extracted`, one `known_defects` entry); `Rules/deferred.json` (3 new dependencies,
23 new passage entries replacing the one blanket `chapter:phaladeepika.07` entry); new
`Engine/tests/test_chapter_seven_neechabhanga.py` (14 tests); one line fixed in
`Engine/tests/test_slice.py` (a stale negative-control example). `Reports/PHASE3_BACKLOG.md` and
`Reports/PHASE3_PLAN.md` regenerated. Zero `Engine/*.py` change.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**Why chapter 7, and why this slice.** Reconnaissance at the start of this session compared every
serious Phase 3/4 candidate the repository's own tooling and reports surfaced: `leverage.py`'s own
top-ranked item (`dep.triped-sign-class`) is a standing human reading question, not implementation,
per Decision 0d's own repeated finding; Phase 4 (integration) was found substantially settled by
Milestone 23 already, with the two remaining items (reinforcement, `concept:parallel-of-overloaded`)
either genuinely unscoped by any source yet or an explicit standing human decision, not something a
session should resolve unilaterally; Brihat Jataka has two cards against Phaladeepika's 595 and
starting a second book's own extraction pipeline from nothing is a materially larger, riskier body of
work than continuing an already-proven one. Among the "ready now" Phaladeepika chapters
(5, 7, 11, 12, 14, 15, 16, 17, 27, plus newly-unblocked 11 and 18), chapter 7 (RAJA YOGAS) measured
roughly 2-3× denser than its nearest rivals by raw corpus length and is the direct thematic
continuation of chapter 6 (YOGAS, fully encoded on its testable doctrine since Milestone 27), sharing
its lordship/house-class/dignity/aspect vocabulary. A full verse-by-verse read of all 30 verses (not
a skim) found the Neechabhanga Raja Yoga family (vv.26-30) uniquely well-suited to open the chapter
with: self-contained, classically prominent, zero new engine capability required, and the source
itself supplies a worked numerical example (the p.90 Note) that doubles as this milestone's own
real-chart validation case — a stronger starting slice than reading the chapter strictly in verse
order would have produced, the same "pick the clean cluster first" posture Milestone 34 already took
splitting v.26 off from v.25/v.33.

**What was built.** Five firing cards, `PD.07.Neechabhanga.LordOrExaltedInSign`/`.MutualKendra`/
`.AspectedByLord`/`.LordOrExaltLordKendra`/`.PlanetItselfKendra` (vv.26-30), each an existential
("any") over the seven classical grahas rather than five per-graha named cards — Neechabhanga carries
one name for a general condition on "a planet," unlike Pancha Mahapurusha's five separately named
yogas, so the existential-over-a-fixed-set shape `PD.20.MiseryDasa.DusthanaLords` already established
(Milestone 33) was the closer precedent to follow than the per-graha-card one. Zero new engine
capability: `dignity`, `in_house_class`, `in_house_from`, `in_house` and `aspects` are all reused
exactly as declared in `Engine/facts.py`'s existing vocabulary. What is new is entirely in the rule
store — a per-graha table (debilitation-sign lord, the graha exalted in the debilitation sign, and
the debilitated graha's own exaltation-sign lord) read by hand from the store's own
`PD.01.SignLord.*`/`PD.01.Exaltation.*` reference cards at authoring time and hardcoded into each
card's condition, the same "literal graha names inside a rule card" precedent Pancha Mahapurusha's own
cards (`PD.06.Malavya` etc.) already set; a dedicated regression test (below) guards this table
against drift in the reference cards it was read from. A sixth, non-firing reference card,
`PD.07.Neechabhanga.UchchanathaNote` (`activation: "reference"`), quotes the translator's Note in
full: it independently resolves two genuine interpretive forks v.26's own prose leaves open (which
graha "the planet exalted in the sign" names — a per-graha lookup distinct from the sign's own ruling
lord, confirmed by the Note's own worked example — and whether the verse's "or" is disjunctive or
cumulative, against a named dissenting commentator, Pt. Gopesh Kumar Ojha), the same "the translator
has already adjudicated this within the source itself" posture Decision 0c took for Adhiyoga, so no
competing `contradicts` card was authored for the rejected reading.

**Item 1 vs. item 4, disambiguated by the source's own five-fold Notes summary, not invented.** v.26's
prose ("the lord of the sign of debilitation... or the planet that is exalted in the sign") and v.29's
prose ("the lord of the sign so occupied or the lord of the planet's exaltation sign") read close
enough to collide on a casual pass. The chapter's own closing "Notes — Thus there are five kinds of
Neechabhanga Raja Yogas" paragraph keeps them distinct by naming two different second candidates: item
1's second candidate is the graha whose *own* exaltation sign is the debilitated planet's *depression*
sign (undefined for the Moon, since no classical graha among Sun-Saturn exalts in Scorpio and
Mantreswara's own chapter 1 is silent on Rahu/Ketu's exaltation — the Moon's item-1 branch therefore
carries only its debilitation-sign lord, Mars, confirmed correct by a dedicated test rather than
assumed); item 4's second candidate is the sign lord of the debilitated planet's *own* exaltation sign
(always defined, via `PD.01.SignLord`, the same table item 2's mutual-Kendra test already reads). Both
readings were cross-checked against the Note's own worked example (Saturn debilitated in Aries: item
1's two candidates are Mars, Aries's own lord, and Sun, the graha exalted in Aries — both confirmed
"in Kendra to the Lagna and the Moon" in the example's own words) before being encoded, an
INTERPRETIVE STEP TAKEN AND RECORDED in both cards' own `note` fields.

**Chapter 7's remainder, deferred honestly, not left as one stale blanket entry.** The old
`chapter:phaladeepika.07` backlog entry (`dep.none`, unencoded) no longer describes reality once any
card exists in the chapter, so it was removed and replaced by 23 new `passage:phaladeepika.07.*`
entries, one per verse or verse-cluster, covering every one of the 59 paragraphs `verify.py`'s own
paragraph-coverage check flagged as newly unclaimed once chapter 7 was added to the manifest — nothing
silently dropped, the identical discipline chapters 3 and 20 already established across their own
multi-milestone slicing. Reading all 30 verses directly (not stopping once vv.26-30 were scoped)
surfaced three genuinely new engine-capability gaps, each registered as its own dependency rather than
folded into an existing one it does not actually match: **`dep.graha-condition-count`** (vv.1-4,8,12
each gate on counting how many of a fixed graha set simultaneously satisfy a compound per-graha test
against a literal threshold — "three or more," "five or more" — a genuinely different shape from
`dep.universal-quantification`, which is about testing every member of a chart-*dependent*
classification such as "all benefics," not counting a fixed, doctrine-named set the way
`seven_graha_sign_count` (Milestone 27) already does; this dependency generalises that precedent's
shape to an arbitrary per-card compound condition rather than one fixed test); **`dep.digbala`**
(v.4's own Notes table directional strength by graha, distinct from both `strength` and ch.4's
unrelated biped-sign Bhava Dik Bala row); and **`dep.parivartana`** (v.9's second yoga, mutual
sign-exchange between two house lords — no predicate compares two lords' placements against each
other the way this doctrine needs). Four already-registered dependencies were newly matched to real
chapter-7 blockers rather than reused loosely: **`dep.paksha`** (the "full Moon" clause recurring in
vv.7,11,12,17,22); **`dep.day-night`** (v.16's "the birth be at night"); **`dep.compound-friendship`**
(v.23's "Adhimitra" Navamsa, the same Panchadha Maitri gap `PD.06.Pushkala` already carries); and
**`dep.lagna-strength`**'s own architecture gap (`ChartBundle` never treats the Lagna as a member of
`chart.bodies` — Decision 0b's own finding, here applied to a Vargottama test rather than a strength
verdict, for v.5). Two passages need a human re-reading rather than a capability: v.6 names "the lord"
twice with an unclear second referent, and v.15 is the chapter's own "somewhat confusing and
complicated" verse (the Notes' own words), carrying two commentators' materially different worked
reconstructions of the same chart — genuine Decision-0-style territory, not a routine encoding call a
single slice should settle in passing. The remaining 8 clusters (vv.10,13,14,18,19,20,24-25, plus the
chapter's own tier-3 chart illustration and colophon) were found independently close to encodable with
*zero* new capability and are tagged `dep.none` specifically so a future session can find "chapter 7
slice 2" by that marker rather than re-reading the whole chapter again — vv.24-25 in particular
(five sub-yogas by placement, conjunction and lordship alone) read as the cleanest remaining material
in the chapter.

**Testing and real-chart validation.** 14 new tests in `Engine/tests/test_chapter_seven_neechabhanga.py`,
against a real ephemeris chart (the project's own Thanjavur nativity) with the Lagna and select bodies
overridden — the same discipline `test_strength.py`'s `place()` helper already established for edge
cases that do not occur on any convenient real birthday, extended here to also override the Lagna
(`dataclasses.replace`) since the worked example needed a specific one the demo nativity does not
happen to have. The primary case reconstructs the source's own worked example (Lagna Leo; Saturn
debilitated in Aries; Mars in the 7th, Sun in the 4th, both Kendra to the Lagna) and confirms item 1
fires exactly as the Note states. Every card gets at least one positive and one negative case; the
Moon's item-1 single-candidate collapse is confirmed by construction (Mars alone suffices; no second
candidate exists to test); item 1 and item 4 are distinguished on Mercury specifically, where the two
cards' own second candidates genuinely differ (Venus vs. Mercury itself); a doctrine-drift regression
test cross-checks the cards' own hardcoded per-graha table against live `Doctrine.sign_lord`/
`.exaltation` reads of `PD.01.*`; and a seven-graha "every graha exalted, nothing fires" sweep pins the
negative discipline every one of the five cards shares (each branch begins with
`dignity(g,"debilitated")`). **One authoring bug was caught by a failing test, not shipped**: the
condition language's variable-name regex is lowercase-only (`Rules/rules.py`'s
`^\?[a-z][a-z0-9_]*$`), so the per-graha variable names first drafted (`?hSaturn`, `?hMercury`, ...)
silently matched as *literal strings* rather than variables, making item 3's aspect test vacuously
false for every graha — found immediately by `test_debilitated_planet_aspected_by_its_own_lord_fires_item_three`
failing, diagnosed by isolating the exact minimal two-clause repro, and fixed by lowercasing every
per-graha variable name across the card family before the chapter file was finalized. Two further test
arithmetic errors (a mis-computed "mutual Kendra" house offset, and moving the debilitated planet
itself out of its own debilitation sign while trying to test a *different* card's Kendra clause) were
each caught the same way and corrected. `Engine/tests/test_slice.py`'s own "chapters already encoded"
negative-control assertion, which had named chapter 7 as its example of an chapter *not yet* encoded,
was updated to name chapter 5 instead — the only pre-existing test this milestone touched, a
tooling-example staleness the milestone's own change created, not a defect the milestone found.
`.venv/Scripts/python.exe -m Engine.cli` was also run end-to-end against the Thanjavur demo nativity
after the change: the pipeline completes with zero errors (the demo chart has no debilitated graha, so
no Neechabhanga claim fires on it — expected, not a gap).

**Verification results.** `Rules/tools/verify.py`: clean (601 cards, 198 backlog entries, 108
available now, every quote byte-exact, every deferred item accounted for). `dupes.py`: no duplicate
candidates. `backlog.py --write`/`leverage.py --write`: reports regenerated, clean. `review.py
--queue`: 599/601 interpretive+structural cards signed off, the same two pre-existing holdouts.
`.venv/Scripts/python.exe -m pytest Engine/tests -q`: **573/573 passing** (was 559/559 — +14 new,
zero regressions, one pre-existing test's stale example corrected).

**Production blockers cleared:** none of §A's named blockers (there is no open P0) — this milestone
touched none of them by design. **Production-readiness impact:** held at 60.00% ≈ 60% exactly — see
§A's own Milestone 36 note for the full row-by-row accounting; every row's own delta this milestone
falls below that row's own established rounding threshold, the same posture Milestones 26, 32 and 34
already established for a correct, fully-verified, sub-threshold addition.

**Why this milestone matters, and why it stops here.** Chapter 7 is now open, its densest and best
thematic continuation of chapter 6 begins with a fully closed, well-tested, zero-new-capability slice,
and the chapter's own remainder is honestly and individually tracked rather than left as one vague
blanket entry — with a third of it already flagged, by dependency tag, as ready for a session that
wants to continue chapter 7 directly rather than pick a fresh chapter. Per this session's own master
prompt (§16/§20), this stops here: one milestone, fully checkpointed, rather than continuing into an
unrelated second one. `MILESTONES.md`'s own resume point (above, in the header) names the exact next
candidates — chapter 7 slice 2, or a fresh chapter — rather than leaving the choice to a future
session's own re-derivation.

---

### Milestone 37 — Phaladeepika chapter 7 slice 2: ten further Raja Yoga cards (vv.13, 18, 20(b)-(d), 24, 25)

**Phase:** 3 (knowledge extraction), zero Phase 2/4 change
**Scope:** `Rules/phaladeepika/ch07.json` (+10 cards, appended); `Rules/deferred.json` (one new
dependency, `dep.own-or-benefic-dignity-in-varga`; `p020`/`p038`/`p055` flipped to `resolved`; `p040`
split into a `resolved` remainder and a newly-deferred `p040-royalfamily`; `p039`'s reason and
`requires` corrected); new `Engine/tests/test_chapter_seven_slice_two.py` (23 tests). `Reports/PHASE3_BACKLOG.md`
and `Reports/PHASE3_PLAN.md` regenerated. Zero `Engine/*.py` change.
**Status:** COMPLETE
**Commit:** this milestone's own commit (see `git log`)
**Remote:** pending this commit's push

**Why this slice, and why not the whole eight-verse candidate list.** Milestone 36 flagged eight
`dep.none`-tagged verse clusters as "chapter 7 slice 2" material (vv.10,13,14,18,19,20,24-25). Per the
master prompt for this session, the exact slice was re-derived from the current repository state
rather than assumed unchanged, and the eight candidates were re-read individually against the actual
engine vocabulary (`Engine/facts.py`'s `VOCABULARY` table) before any card was authored. Three did not
hold up: **v.10**'s "the Sun in conjunction with the Moon... in the middle of Sagittarius... a very
powerful Mars" needs a judgement call this store has not yet made anywhere else — whether "middle of"
and "very powerful" are testable degree/strength conditions or untestable descriptive colour (the
precedent for the latter, `PD.07.Neechabhanga.AspectedByLord`'s own "auspicious case" clause, exists,
but deciding this deserved its own attention rather than a decision folded silently into a five-verse
slice); **v.14 and v.21** both need "aspected by or associated with a friendly planet" — natural
friendship is fully computed doctrine (`dep.dignity-friendship`, implemented) but `_dignity` only
consumes it internally to classify a graha's own dignity, and never emits it as its own queryable
`(graha, other, relation)` fact the condition language could bind two grahas against; and **v.19**'s
"own or benefic Varga" turned out to need a capability the Milestone 36 note claimed already existed
(`dignity_in_varga`) but does not: that predicate was built Milestone 29 deliberately narrow, emitting
only `"debilitated"` (see its own `dep.dignity-in-varga` registry entry), because ch. 2 v.36, the verse
it was built for, names no other value. Discovering this before authoring — not after — is exactly
what "search the existing engine thoroughly" (§4 of the master prompt) is for. The remaining five
clusters (vv.13, 18, 20, 24, 25) were re-verified clean against the actual vocabulary and encoded in
full.

**What was built.** Ten firing cards, zero new predicates:
- `PD.07.Emperor.VargottamaMoonAspectedNoMalefic` (v.13) — the Moon Vargottama, aspected by a strong
  planet, with no malefic in the Lagna. "No malefic in the Lagna" is a correlated `not` over a fresh
  variable (`nature(?m,malefic)` AND `in_house(?m,1)`), the same existential-absence shape
  `PD.06.Kemadruma` already uses for "if the above three Yogas are absent."
- `PD.07.King.JupiterMoonKendraVenusAspectedNoDebilitation` (v.18) — Jupiter and the Moon in kendra,
  aspected by Venus, with no graha anywhere debilitated. INTERPRETIVE STEP TAKEN AND RECORDED: "aspected
  by Venus" is read as governing the compound subject "Jupiter and the Moon" (Venus aspects both), a
  plain-grammar reading of the printed English sentence rather than an import of outside convention —
  recorded as a reading, not a source-confirmed resolution, since no Note or worked example in this
  book corroborates it the way v.26's own disjunctive "or" was corroborated in Milestone 36.
- `PD.07.King.JupiterLagnaNotCapricorn` / `.StrongLagnaLordKendra` / `.StrongMercuryKendraAspectedJupiter`
  (v.20 items (b)-(d)) — three of the verse's own four numbered sub-yogas (its own heading claims
  "Five Yogas" but only four are ever printed; transcribed as printed, no fifth invented). Item (a)
  (Venus aspected by Jupiter, gated on the native being "born in a royal family") is split out as its
  own deferred entry — `BirthRecord` carries no family-status field and no verse in this corpus states
  how to derive one astrologically, the same gap `passage:phaladeepika.07.p001` already named for
  vv.1-2, so this is not a temporal-ordering deferral expected to resolve on its own.
- `PD.07.RajaYoga.MaleficsThirdSixthEleventh` / `.MarsMercurySecond` / `.SunVenusFourth` /
  `.MarsSaturnJupiterTenthEleventhLagna` (v.24 items (1)-(4)) — four Raja Yogas by placement and
  conjunction. INTERPRETIVE STEP TAKEN AND RECORDED on item (1): "the 3rd, 6th and 11th house counted
  from the house occupied by the lord of Lagna, Moon or from the Lagna" is read as three *alternative*
  reference points (`any`), each requiring malefics in *all three* of the 3rd/6th/11th from that one
  reference (the printed "and" read conjunctively, a plain-grammar reading distinct from v.26's own
  named word-choice dispute, since no Note addresses this sentence at all). The Lagna-lord reference
  binds a fresh variable via `lord_of_house(?ll,1)` and reuses it as `in_house_from`'s own `reference`
  argument — `dep.graha-frame`'s general graha-to-graha mechanism exercised with a *variable* second
  party for the first time in this store (every prior card used a literal, almost always `"Moon"`),
  not a new capability.
- `PD.07.RajaYoga.HouseLordKendraFromMoonJupiterOwnership` (v.25) — one of the 11th/9th/2nd lords in
  Kendra from the Moon, with Jupiter separately owning the 2nd, 5th or 11th house; the two clauses are
  independent (the verse states Jupiter's ownership as its own condition, not tied to which lord
  satisfies the first).

**Bookkeeping corrected, not just extended.** `passage:phaladeepika.07.p020`, `.p038` and `.p055` move
to `resolved`. `passage:phaladeepika.07.p040` is split: the resolved remainder covers items (b)-(d);
a new `passage:phaladeepika.07.p040-royalfamily` carries item (a)'s own still-genuine birth-record gap
forward, the same "split so a genuine remainder does not hide behind a resolved entry" discipline
Milestone 33 established for ch. 20 v.24's own item (4). `passage:phaladeepika.07.p039`'s `reason` and
`requires` are corrected in place (not silently overwritten — the old text is quoted and marked
"CORRECTED" in the new one) from the too-optimistic Milestone 36 note to the newly registered
`dep.own-or-benefic-dignity-in-varga`. That new dependency deliberately carries **no `predicate`
field** — the same reason `dep.lagna-strength` withheld one at Milestone 24: `dignity_in_varga`
already *is* a derivable predicate name (`dep.dignity-in-varga` emits it), so naming it here would
have reported this entry falsely resolved the instant it was declared, exactly the false-positive
`backlog.py` trap Milestone 22 first had to catch for `dep.strength` itself. This was caught in this
session, before commit, by `backlog.py`'s own "newly unblocked" line flagging `p039` immediately after
the dependency was first registered with a `predicate` field — fixed by removing it and re-running,
not discovered after the fact.

**Testing.** 23 new tests in `Engine/tests/test_chapter_seven_slice_two.py`, against the same real
Thanjavur nativity Milestone 36 used, with individual bodies moved via `Engine.tests.test_strength.place`.
Every card gets at least one positive and one negative case. Several cards needed a genuinely different
Lagna (v.20(b)'s own Capricorn-exclusion test, v.20(d), v.25); this file's own `lagna()` helper
recomputes `chart.houses["signs"]` and every body's own `.house` field together with
`ascendant_sign`/`ascendant_sign_index`, unlike the shallow helper of the same name in
`test_chapter_seven_neechabhanga.py`, which only replaces the ascendant fields and leaves every
unmoved body's `.house` stale — `in_house`, `in_house_class`, `aspects` and `lord_of_house` all read
`.house`/`chart.houses["signs"]` directly rather than deriving them from `ascendant_sign_index` on
demand, confirmed by reading `Engine/chart.py`'s own `compute_chart` and `Engine/facts.py`'s
extractors before writing a single test. This was a real latent gap in Milestone 36's own helper,
caught here rather than inherited silently, and happened not to matter there only because every test
using it re-placed every body its own conditions referenced. Three authoring bugs were caught by
failing assertions during authoring and fixed before commit: two whole-sign house-table arithmetic
errors (Scorpio, not Sagittarius, is the 11th house from a Capricorn Lagna — a hand-computation slip,
corrected by re-deriving the table exhaustively from the house formula rather than trusting the first
pass) affecting the v.24-item-(1) and v.24-item-(4) tests; and one test whose intended "negative" case
was not actually negative for v.25 — a 2nd-house-lord (Jupiter) placement chosen to sit outside
Kendra-from-the-Moon still let the card fire, because the unmoved, real-chart 11th-house lord
(Mercury) independently happened to sit in Kendra-from-the-Moon and the card's own first clause is a
disjunction over all three house-lords, not just the 2nd's — the card's logic was correct; the test's
premise was wrong, and it was replaced with a construction (the real, unmoved Capricorn Lagna, under
which Jupiter owns none of the 2nd/5th/11th) that fails the card's *second* clause outright,
independent of any lord's placement, isolating what the test actually meant to check.
`.venv/Scripts/python.exe -m pytest Engine/tests -q`: **596/596 passing** (was 573/573 — +23 new, zero
regressions).

**Verification results.** `Rules/tools/verify.py`: clean (611 cards, 199 backlog entries, 104
available now, every quote byte-exact, every deferred item accounted for). `dupes.py`: no duplicate
candidates. `backlog.py --write`/`leverage.py --write`: reports regenerated, clean (the one
"newly unblocked" false-positive on `dep.own-or-benefic-dignity-in-varga`, caused by giving that entry
a `predicate` field, was caught and fixed in-session before this final run — see above). `review.py
--queue`: 609/611 interpretive+structural cards signed off, the same two pre-existing holdouts
(`PD.01.Kalapurusha.Strength`, `PD.04.Lagna.TripedSign`).

**Production blockers cleared:** none of §A's named blockers (there is no open P0) — this milestone
touched none of them by design. **Production-readiness impact:** held at 60.00% ≈ 60% exactly — see
§A's own Milestone 37 note for the full row-by-row accounting; every row's own delta this milestone
falls below that row's own established rounding threshold, the same posture Milestones 26, 32, 34 and
36 already established for a correct, fully-verified, sub-threshold addition.

**Why this milestone matters, and why it stops here.** Chapter 7's own general Raja Yoga material
(vv.1-25) is now roughly half closed by verse count, and — as important as what was built — three of
the eight candidates flagged ready were found, on closer inspection against the actual engine
vocabulary, not actually ready, and were deferred honestly with corrected bookkeeping rather than
forced through to hit a larger card count. `p039`'s own correction is a genuine finding: a prior
milestone's optimistic note is not ground truth, and this session's own "search the existing engine
thoroughly" pass caught it before it became a wrong card rather than after. Per this session's own
master prompt, this stops here: one milestone, fully checkpointed. `MILESTONES.md`'s own resume point
(above, in the header) names the exact remaining chapter-7 material and its exact blockers, rather
than leaving a future session to re-derive them.

---

## D. CURRENT MILESTONE

**Nothing is currently in progress.** Milestone 37 above is fully committed, tested, verified, and
pushed — Phaladeepika chapter 7 slice 2 (vv.13, 18, 20(b)-(d), 24, 25, 10 firing cards), zero new
engine capability, one new dependency registered (`dep.own-or-benefic-dignity-in-varga`). **No single
next milestone is forced.** Milestones 35-37 all left chapter 20's own remainder exactly as Milestone
34 left it: v.25 (Mars/Urdhvamukha placement, `passage:phaladeepika.20.p025`) and v.33 (Jupiter-kendra
/ Shirshodaya-Ubhayodaya-Prishtodaya life-timing, `passage:phaladeepika.20.p033`) each need their own
unencoded sign classification (`dep.urdhvamukha-sign-class`, `dep.rising-order-sign-class`
respectively); v.24 item (4) (last-degree placement) needs a degree threshold the source does not
print (`dep.dasa-last-degree`); vv.56-57 need a new degree-position predicate
(`dep.degree-position-quality`, a different gap from item (4)'s own); v.30 hits the standing
no-invented-numeric-weighting refusal directly (`dep.adjudication`); everything Antardasa-scoped
stays correctly blocked on `dep.antardasa`, unimplemented by design. Chapter 3 is not complete — 8
of its 9 doctrine clusters remain, each tracked individually in `Rules/deferred.json`
(`passage:phaladeepika.03.p003` through `.p054`) — and chapter 6's testable doctrine remains
complete (see Milestone 27's own "Chapter 6 accounting"). **Chapter 7 is roughly half closed by verse
count** (Milestones 36-37): slices 1 (vv.26-30) and 2 (vv.13, 18, 20(b)-(d), 24, 25) both closed in
full. What remains is genuinely blocked, not merely unpicked: `dep.graha-condition-count`
(vv.1-4,8,12), `dep.digbala` (v.4), `dep.parivartana` (v.9's second yoga), `dep.paksha`
(vv.7,11,12,17,22), `dep.day-night` (v.16), `dep.compound-friendship` (v.23), `dep.lagna-strength`'s
own architecture gap (v.5), `dep.own-or-benefic-dignity-in-varga` (v.19, newly registered this
milestone), the friendship-exposure gap shared by v.14 and v.21 (natural friendship is computed but
not exposed as its own queryable fact — see Milestone 37's own write-up), v.10's own
descriptive-vs-testable judgement call, and two passages needing a human re-reading (v.6, v.15).
Decision 0e (below) is untouched by Milestones 34-37.

**Eight decisions are owed by a human.** None blocks the next milestone; each should be
settled before the work it touches is extended. Milestone 29 opened one (0e) and closed none;
Milestone 28 opened one (0d, though its underlying question dates to Milestone 21) and closed
none; Milestone 30 opened and closed none of these eight (it resolved a different, mechanical
defect — the `PD.09.Dignity.Inimical` sentinel bug — which needed no human judgement call);
Milestone 31 likewise opened and closed none of these eight — its own two source tensions (the
ch.1/ch.20 "trikona" discrepancy, v.43-44's apparent conflict with vv.2-21) were each resolved by
reading the source directly rather than left as standing human decisions, and are recorded in full
in Milestone 31's own write-up and in the relevant cards' `note` fields. Milestone 32 opened and
closed none of these eight either — v.27's one interpretive step (the literal 6th/12th-only house
list) was resolved by reading the verse directly, the same way Milestone 31 resolved its own two
tensions, and is recorded in full in Milestone 32's own write-up and in
`PD.20.Placement.BeneficAdverse`'s own `extraction.verified_by` field. Milestone 33 likewise opened
and closed none of these eight — its own interpretive step (recording `PD.20.MiseryDasa.
DusthanaLords`'s collision with `PD.20.Strong.House6`/`.House8`/`.House12` as `contradicts` links)
was a card-authoring judgement using Stage 7's existing mechanism, not a standing question left for
a future human ruling, and is recorded in full in Milestone 33's own write-up and in that card's
own `note`/`extraction.verified_by` fields. Milestone 34 likewise opened and closed none of these
eight — v.26 carried no genuine interpretive fork the way v.24/v.27's cards did; its two primitive
mappings ("uneclipsed" = `combust`, "influence" = `conjunct`/`aspects`) were each corroborated
directly from the book's own words (twice, inside chapter 20 itself, for the first; ch.9's own
"associated with or aspected by" for the second) rather than argued from a plausibility case the
way Decision 0e's Varga question was, so nothing here rises to a standing human decision. Milestone 35
(infrastructure) opened and closed none of these eight by construction — it touched no doctrine.
Milestone 36 likewise opened and closed none of these eight — v.26's own interpretive step (which
graha "the planet exalted in the sign" names, and whether v.26's "or" is disjunctive or cumulative)
was resolved by the source's own Note, which explicitly states a preference and supplies a worked
example confirming it, the same "the translator has already adjudicated this" posture Decision 0c
took for Adhiyoga rather than a standing question left for a future human ruling; recorded in full in
`PD.07.Neechabhanga.LordOrExaltedInSign`'s own `note` field and in
`PD.07.Neechabhanga.UchchanathaNote`.

### Decision 0e (Milestone 29) — `dep.varga-ownership` / `PD.10.Venus.VargaMarsSaturn`

**Which divisional chart "the Varga of Mars or Saturn" (ch. 10 v.4) means, if it can ever be
settled at all.** The verse: *"The native will have illicit relations with other people's wives if
Venus be in the Varga of Mars or Saturn or be aspected by these planets."* "Varga of" a graha reads
naturally as *ownership* of a division (as ch. 3 v.4 defines for Drekkana: "lords of the sign
itself, of the 5th house and of the 9th house"), not occupancy of one of its signs — but the verse
never says *which* of the ten divisions it means, and neither Phaladeepika ch. 3 nor Brihat Jataka
ch. 21 (both read in full this milestone, specifically to try to settle this) states an ownership
doctrine that would disambiguate it.

**What Milestone 29 did and did not resolve.** The condition was rewritten from a wrong-shaped test
(D9 sign occupancy) to a right-shaped one (ownership, `varga_owned_by(Venus,?v,Mars/Saturn)`),
existentially quantified over which division — matching the verse's own silence rather than
picking one. `varga_owned_by` is declared in `Engine/facts.py`'s vocabulary with no extractor, so
the card stays correctly inert. This is a *representation* fix, not a resolution of the underlying
question; the card cannot fire until both (a) an ownership calculator exists for at least one
division and (b) a human decides which division(s) the existential should range over, or whether
it should range over all ten.

**Two defensible positions:**
1. **Leave it exactly as re-diagnosed.** The existential over `?v` is honest about not knowing, and
   costs nothing further until a human or a new source settles it.
2. **Narrow it to Drekkana specifically**, on the strength of ch. 3 v.4's own worked ownership rule
   (sign/5th-lord/9th-lord) being the only *ownership* doctrine either source states for any
   division — accepting that this is a plausibility argument, not a textual one, since the verse
   itself never names Drekkana.

**Recommendation: (1), unchanged.** Two source chapters were read specifically to try to settle
this and neither does; narrowing to Drekkana on the strength of an argument-by-elimination would be
exactly the kind of substitution the project's standing rule (Decision 0d, Milestone 28) already
declines to make for a different card. Building `dep.varga-ownership` for Drekkana regardless (it
would be needed anyway if chapter 3's own Drekkana-ownership doctrine, `passage:phaladeepika.03
.p008`, is ever encoded) would still leave this specific card's `?v` existential exactly as open as
it is now.

### Decision 0d (originated Milestone 21, formally investigated Milestone 28) — `dep.triped-sign-class` / `PD.04.Lagna.TripedSign`

**Whether "triped" (ch.4 v.6, printed p.44) is a misprint for "biped," or a genuine term this
project's corpus simply does not define.** The verse: *"The first house gets one Rupa of
strength if it is a triped sign. If it be Vrischika it gets 1/4 Rupa as its strength. In any
other sign the strength will be 1/2 Rupa."* No class named "triped" (or any spelling near it)
appears anywhere else in Phaladeepika or in Brihat Jataka, the only two converted books.

**What Milestone 28 added over Milestone 21's original finding.** Milestone 21 confirmed
"triped" against a rendered page image and stopped there. This session went one step further:
`Books/Mantreswara_s__Phaladeeplka_.pdf` page index 43 (0-indexed; printed p.44) was reopened
directly with PyMuPDF and inspected at both the text-layer and the glyph level — not just
re-rendered. Two things rule out extraction defects specifically, not just confirm the word:
1. **The book's text layer is `pdf_text` direct extraction from a clean digital source**
   (`Pipeline/profiles/phaladeepika.json`: *"Clean digital text layer... Goes through
   producers/pdf_text.py, not OCR"*), so there is no scan-to-glyph guessing step where a
   "b"/"t" confusion could be introduced the way it could for Brihat Jataka's actual OCR pipeline.
2. **The PDF's own font metadata for this exact span is a single unbroken `TimesNewRomanPSMT`
   run reading "triped"** — confirmed by both extracting the raw text layer and reading the
   `page.get_text("dict")` span data, then independently rendering a 600dpi crop of just this
   line and reading the image directly. All three (text layer, font/span data, rendered glyphs)
   agree: the page prints "triped," not "biped" with a smudged or misrendered glyph.

**Why "biped" is the leading candidate but not a safe substitution.** Ch.4's own Bhava Dik Bala
rule (a) — *"Gemini, Virgo, Libra and first part of Sagittarius are biped signs. If these signs
be in the Lagna, they obtain one Rupa of strength"* — states exactly the headline clause v.6
would state if "triped" were "biped": biped-in-Lagna, one full Rupa. But that rule is the
**translator's survey of "other ancients"** (`PD.04.Frame.OtherAncients`), a different authority
from the verse `PD.04.Lagna.TripedSign` quotes (Mantreswara's own doctrine,
`PD.04.Frame.Mantreswara`), and it does not state — and nothing else in the corpus states — the
verse's own second clause, "if it be Vrischika it gets 1/4 Rupa." That clause has zero source
corroboration under any reading. Silently correcting to "biped" would therefore be encoding a
guess for the clause that matters most (the general case) while leaving a second, unexplained
clause (the Vrischika exception) exactly as unsupported as it was before the "correction" — a
partial fix that would look more resolved than it is.

**Two defensible positions, both the human's to pick:**
1. **Leave it inert, as encoded.** `dep.triped-sign-class` (`Rules/deferred.json`, effort 1,
   `implemented: false`) stays open; `PD.04.Lagna.TripedSign` stays `activation: "inert"`,
   `requires: ["dep.triped-sign-class"]`. Nothing in any consultation is wrong, because nothing
   is asserted.
2. **Encode "triped" as "biped," on the strength of the internal parallel above**, accepting that
   the Vrischika clause remains a documented, uncorroborated detail of Mantreswara's own verse
   rather than something the correction explains. Doing this would also require, separately,
   encoding `PD.01.SignBodyForm.Table`'s sign→class mapping as queryable data for the first
   time — that table currently states only the four class names (`classes: [human, quadruped,
   centiped, watery]`, `PD.01.SignBodyForm.Table`), not a per-sign table, precisely because the
   Milestone 16 verification pass that confirmed the table's *layout* deliberately left encoding
   its *contents* to a future Phase 3 session rather than a verification pass. So even choosing
   (2) does not make `PD.04.Lagna.TripedSign` executable by itself — it would clear the term
   question but leave a second, independent, and genuinely still-open encoding task.

**Recommendation: (1), unchanged, now on stronger evidence.** Two independent sessions, seven
milestones apart, reading the primary source by two different methods (page-image rendering,
then text-layer/font/glyph triple-check) reached the identical conclusion. That convergence is
evidence the term is genuinely unresolved, not evidence a diagnosis was rushed the first time. A
future session should not re-open this by trusting `leverage.py`'s ROI ranking alone — see the
header's "Exact resume point" for why that ranking is a known false signal for this one entry.

### Decision 0c (Milestone 26) — `concept:adhiyoga-distribution-strictness`

**Whether the Notes' rejected "some authors" reading of Adhiyoga should be encoded as a
competing active card.** V.42's own text states no distribution requirement at all: Mercury,
Jupiter and Venus each individually within houses 6, 7 or 8 satisfies it, however they are
distributed among the three houses. The Notes report an unnamed narrower reading — all three
houses must be individually occupied, none left vacant — and the translator explicitly calls it
incorrect in the same sentence, endorsing Shruti Kirti's (per Vyas) confirmation of the loose
reading instead. `PD.06.Adhiyoga` encodes the loose reading; `PD.06.Adhiyoga.ShrutiKirti`
(reference) preserves both sides of the dispute in the source's own words; no `contradicts` card
exists for the rejected side.

**Why this is a decision and not a closed question.** The rejected reading is independently
*expressible* with predicates already in the vocabulary — nothing here is blocked on missing
engine capability. It was left unencoded for a structural reason: its actual claim is that
Adhiyoga does *not* form when a house is left vacant, and the card schema has no mechanism for a
card to assert the *absence* of another card's yoga as a firing rule. Every narrower-condition
sibling already in the store predicts something for a chart that satisfies its *own* condition;
none of them predict the non-formation of a *different* card's yoga.

**Two defensible positions:**
1. **Leave it as encoded.** The translator has already adjudicated this dispute within the
   source itself — a materially different posture from `PD.09.Dignity.Exalted` vs. its own
   Notes, where both sides are left standing. Building a negation-of-formation mechanism for one
   clause would be speculative architecture the project has repeatedly declined elsewhere (the
   distinct-graha quantifier Milestone 25 declined for `PD.06.Parashara.EighthLordInTwelfth`,
   the universal quantifier `PD.06.Vasumati` still lacks).
2. **Build the mechanism anyway.** If a human decides the rejected reading is worth representing
   as a live, chart-dependent finding (not merely quoted apparatus), a negation-of-another-card's
   -formation predicate would need to be designed — carefully, since nothing else in the store
   needs one yet, and getting its semantics wrong (e.g., silently treating "condition not met" as
   "yoga positively denied") would misrepresent doctrine rather than encode it.

**Recommendation: (1), unchanged from how it was encoded.** The translator's own resolution of
the dispute, plus the schema's genuine inability to assert a denial-of-formation without new
architecture, both point the same way. This is not a precedent-setting call the way Decision 0a
is — it is closer to Decision 0b's "no source, no capability" shape, except here the *source*
is present and points to a *specific* schema gap rather than an absent one.

### Decision 0b (Milestone 24) — `concept:p009-lagna-or-moon-clause`

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
obligation. `leverage.py` still ranks `dep.triped-sign-class` first (cost 1, +1 card) and that is
a human's reading (whether "Triped" is a misprint for "biped") rather than an implementation, so
the ranked list does not settle it either — unchanged since Milestone 21, re-confirmed as recently
as Milestone 30 in passing.

*(This subsection's own "recommended" line named `passage:phaladeepika.06.p168` until Milestone 36 —
that passage was resolved in Milestone 27, nine milestones ago; the recommendation below replaces it
rather than leaving a stale pointer to already-completed work sitting next to the header's own
current resume point.)*

**Recommended: continue chapter 7 (`passage:phaladeepika.07.*`, `dep.none`-tagged remainder) — or
open a fresh "ready now" chapter, whichever a human prefers; both are genuinely close.** Milestone 36
opened chapter 7 with a clean, self-contained slice (Neechabhanga, vv.26-30) and, by reading the
whole chapter directly, found roughly a third of its own still-deferred verses
(vv.10,13,14,18,19,20,24-25 — `passage:phaladeepika.07.p015`/`.p020`/`.p021`/`.p038`/`.p039`/`.p040`/
`.p055`) independently close to encodable with existing predicates alone. Continuing here needs no
fresh reconnaissance (the chapter is already read, the blockers already diagnosed) and would let the
chapter accumulate toward "fully encoded on its testable doctrine" the way chapter 6 already is.
**Equally defensible: open chapter 5 or chapter 11/18** (the latter two newly unblocked — sex-scoped
cards can now fire per `dep.native-sex`, and conjunction cards per `dep.conjunct`) — smaller, fresh
material with no compounding per-verse judgement calls of chapter 7's own remaining kind (v.6's
unclear referent, v.15's two-commentator dispute). Neither choice is forced; a human should pick
based on whether the next session's appetite is "finish what's open" or "start clean."

**Two further alternatives, each defensible, carried forward unchanged from before Milestone 27
closed the passage this subsection used to recommend:**

1. **`dep.compound-friendship`** (cost 3). The Adhimitra/Adhishatru tiers, which the book
   defines in ch. 2 and then uses without definition in ch. 6 v. 19, ch. 7 v. 23 (Milestone 36),
   ch. 10 v. 23 and six rows of the ch. 4 survey. Cheap, well-sourced, and releases
   `PD.06.Pushkala`'s and chapter 7's own v.23 remaining obstacle at once.
2. **`concept:parallel-of-overloaded`** (Decision 0a) — an encoding pass over chapter 6's notes
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
| Ch.5 — Source of livelihood | none | new chapter, rule-dense | ready |
| Ch.7 — RAJA YOGAS, slice 2 (vv.10,13,14,18,19,20,24-25) | none (each tagged `dep.none` in `Rules/deferred.json`) | closes roughly a third of the chapter's still-deferred verses; slice 1 (Neechabhanga, vv.26-30) closed in Milestone 36 | ready |
| Ch.12 — Progeny (5th house) | none | new chapter, rule-dense | ready |
| Ch.14 — Diseases, Death, Past/Future births | none, but sensitive-content policy applies | new chapter | ready |
| Ch.15 — Assessment of houses | none | feeds future Stage 7 weighting | ready |
| Ch.16 — General effects of the twelve houses | none | would replace `HOUSE_LABEL_UNSOURCED` in the renderer | ready |
| Ch.17 — Exit from the world | none, sensitive-content gate | new chapter | ready |
| Ch.27 — Sanyasa yogas | none | new chapter | ready |
| `chapter:phaladeepika.11` (Female Horoscopy), `chapter:phaladeepika.18` (graha-pair conjunction effects), `passage:phaladeepika.08.p057` | now unblocked (`dep.lord-of-house`, `dep.aspects`, `dep.dignity` etc. are implemented) | see `Reports/PHASE3_BACKLOG.md` "Newly unblocked" | ready — flagged by `backlog.py` as newly unblocked, not yet acted on |

### Blocked

**Ch.6 vv.39-41, the seven-planets-in-N-signs family, is no longer blocked** — it needed the
distinct-sign-count fact this table used to list as its blocker; the fact was built and the
passage encoded in Milestone 27 (see §C). Removed from this table rather than left stale.

| Description | Blocked on | What would unblock it | Status |
|---|---|---|---|
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
| **Distinct-sign-count over a doctrine-named set of grahas** | **Implemented (Milestone 27)** | `Engine/facts.py::_seven_graha_sign_count`, `Engine/doctrine.py::seven_grahas` — one chart-wide fact, `seven_graha_sign_count(n)`, matched against a literal `n` the same way `occupant_count` already is; the member set (Sun-Saturn) is read from `PD.06.SevenGrahas`, not a Python literal | the seven-planets-in-N-signs family, `PD.06.Vallaki`/`.Dharma`/`.Hasha`/`.Kendra`/`.Shula`/`.Yuga`/`.Gola` |
| **Varga (divisional chart) engine — D9 (Navamsa) only** | **Implemented (Milestone 29)** | `Engine/facts.py::_varga`, `Engine/doctrine.py::varga_division_count`/`navamsa_start_offset` — division count and counting-start rule both read from `PD.03.Dasavarga`/`PD.03.Navamsa.Start`, never a Python literal. D3/D2/D12/Trimsamsa etc. deliberately not built; nothing in the corpus consumes them yet | `PD.09.Vargottama`, `PD.10.Venus.VargaMarsSaturn` (partially, via its aspect branches only) |
| **Vargottama extractor** | **Implemented (Milestone 29)** | `Engine/facts.py::_varga`, `Engine/doctrine.py::vargottama_definition` — same sign in D1/D9, the comparison read from `PD.03.Vargottama.Definition` rather than hardcoded | `PD.09.Vargottama` (released) |
| **Dignity read against a divisional placement** | **Implemented (Milestone 29)** | `Engine/facts.py::_varga` (folded into the same loop as the two rows above) — `dignity_in_varga(graha,varga,dignity)`, narrowly emitting only "debilitated" against D9, the one value ch. 2 v.36 names | `PD.02.AdverseDisposition` (released) |

### Deliberately not implemented (deferred, with reason)

| Capability | Status | Why |
|---|---|---|
| Numeric Shadbala / Bhava Bala | Not implemented, and **not implementable from the encoded corpus** | `dep.shadbala-arithmetic`. Phaladeepika ch. 4 states the six components and explicitly withholds the arithmetic for three of them (Yudha, Chesta, Drig), so no Pinda can be computed from this book at all; Bhava Bala additionally needs a Bhava madhya whole-sign houses do not have. This is a *source* gap. Superseded the previous "Stage 4 not built" row when Milestone 22 built the verdict half. |
| Varga *ownership* (a divisional sign ruled by a named graha, as opposed to occupied) | Not implemented | `dep.varga-ownership` (Milestone 29). "Venus in the Varga of Mars or Saturn" (ch. 10 v.4) names ownership, not occupancy — a different fact from the row above — and which division it means is unresolved even with ch. 3 and Brihat Jataka ch. 21 both read. Blocks `PD.10.Venus.VargaMarsSaturn`'s first branch; see Decision 0e in §D. |
| Ordinal strength (which graha is *strongest*) | Not implemented | `dep.strength-ranking`. The encoded doctrine states a verdict, not an order, and ranking two grahas that are both merely "strong" would be the engine inventing an order the source never supplies. Blocks `PD.10.WifeDirection.Strongest` and `PD.10.Marriage.StrongerDasha`. |
| Compound (Panchadha maitri) friendship | Not implemented | `dep.compound-friendship`. The Adhimitra/Adhishatru tiers, which the book defines in ch. 2 and then uses without definition in ch. 6 v. 19, ch. 10 v. 23 and six rows of the ch. 4 survey. Cheap (cost 3) and well-sourced; identified in Milestone 22 as `PD.06.Pushkala`'s real blocker. |
| House-to-body-part correspondence | Not implemented | `dep.body-part-significator`. Nothing in the store maps a house to a limb, so `PD.01.Kalapurusha.Strength` would emit a claim naming no body part. |
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
**Chapters partially encoded:** 6 (through v.38 of ~70 verses); 3 (Milestone 29, slice 1: v.1's
Dasavarga/Vargottama definitions and v.4's Navamsa-start rule only — 8 of 9 doctrine clusters
remain, see `passage:phaladeepika.03.*` in `Rules/deferred.json`)
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
| `passage:phaladeepika.06.p168` | vv.39-41 seven-planets-in-N-signs family | RESOLVED, Milestone 27 — closed chapter 6's testable doctrine outright | n/a | No | Resolved |
| `passage:phaladeepika.06.p175` | vv.42-43 Adhiyoga | RESOLVED, Milestone 26 — see `concept:adhiyoga-distribution-strictness` for the one judgement call left open | n/a | No | Resolved |
| `passage:phaladeepika.06.p202` | vv.57-69, twelve dusthana-lord yogas | RESOLVED, Milestone 25 — see its own contradiction/qualification/parallel-authority relationships against Parashara's counter-doctrine | n/a | No | Resolved |
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

- **Run `dupes.py` before treating a multi-card split as final, not just at the end of a
  session.** A first draft of chapter 6's Adhiyoga split one verse's Lagna-or-Moon disjunction
  into two cards, `.Lagna` and `.Moon`; both necessarily quoted identical text, since neither the
  naming clause nor the effect differs by reference frame, and `dupes.py` flagged the first
  same-book, full-`quote_sha256` duplicate this project has ever recorded. The fix was one card
  with the disjunction as its own condition, not two cards with a manufactured distinction.
  Check for a distinguishing quote *before* finalizing a split modeled on a worked example's
  naming, not just when the source states two names. (Milestone 26.)
- **A claim about a corpus "defect" is itself a claim — check the actual codepoint before
  writing it down.** An OCR-defect note ("U+FFFD replacement character") was written for a
  character that turned out, on direct inspection, to be a valid em dash (U+2014) rendering
  oddly in a terminal font. Caught by a test asserting the exact string before that test was
  committed, and corrected in the card, its `extraction.verified_by`, and the test together —
  not left as a permanent, false claim about the source. (Milestone 26.)
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
- **vv.39-41's small new engine capability was built and used** (distinct-sign-count of the 7
  classical grahas, `seven_graha_sign_count`) — `passage:phaladeepika.06.p168` resolved,
  Milestone 27, closing chapter 6's testable doctrine.
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
