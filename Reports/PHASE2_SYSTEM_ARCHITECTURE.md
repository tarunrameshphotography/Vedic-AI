# Phase 2 — System Architecture

**The AI Vedic Astrologer: reasoning engine design**

| | |
|---|---|
| **Status** | Design. No implementation code exists or should be written against this document until it is approved. |
| **Written** | 2026-08-01 |
| **Supersedes** | The Phase 2/3/4 sketch in `README.md`, which split calculation, retrieval and interpretation into three phases. This document treats them as one system, because they cannot be designed independently. |
| **Depends on** | `Knowledge/brihat-jataka.md`, `Knowledge/phaladeepika.md` (approved corpus), `Reports/PIPELINE_v1.0.md` (frozen conversion pipeline) |

---

## 0. Objective, and what changed

Phase 1 built a corpus. Phase 2 builds an astrologer.

The corpus pipeline is **frozen as of this document**. No further book is converted until Phase 2
produces evidence that a specific piece of knowledge is missing. §7.4 defines the mechanism that
produces that evidence — a gap log — so that "unfreeze the pipeline" becomes a decision driven by
measured coverage failure rather than by the assumption that more books are better.

The system's purpose: given a person's birth details, produce an interpretation of their chart
that an experienced traditional astrologer would recognise as competent, in which **every single
assertion is traceable to a computed quantity and a printed classical passage.**

### 0.1 The governing constraint

The corpus rule that governed Phase 1 — *preserve exactly, never guess, flag what is uncertain* —
carries forward unchanged into Phase 2, restated for a reasoning system:

> **The system may compute, and it may quote. It may not invent.**
>
> Every predictive statement in the output must be the application of a rule that is written in a
> book we hold, to a fact that we calculated. Anything else is a defect, and the system must be
> built so that it is a *detectable* defect, not a matter of trust.

This has one uncomfortable consequence that shapes the whole design, stated plainly here because
everything downstream follows from it:

> **The language model already knows Vedic astrology from pretraining, and it will leak that
> knowledge into the output unless the architecture physically prevents it.**

A model asked to "interpret this chart using these passages" will happily produce fluent,
plausible, correct-sounding astrology that came from its weights rather than from Mantreswara.
This is exactly the failure Phase 1 already met once, in a different guise: Surya inventing fluent
text on blank paper because a faint ghost of print gave it something to read
(`surya-hallucinates-show-through`). It was not detectable from the text — it read as real content
— and it was only caught by measuring the *image* the text claimed to come from.

The same discipline applies here. Groundedness cannot be established by reading the output; it must
be established by checking the output against the thing it claims to derive from. §6 specifies that
check. §4 arranges the pipeline so that the model is never in a position where fabrication is the
easy path.

### 0.2 Design principles

1. **Compute everything computable.** No quantity a language model can get wrong is ever produced
   by a language model. Longitudes, houses, vargas, dasha dates, bindu counts, yoga conditions:
   all deterministic code.
2. **The model writes; it does not decide.** Exactly one stage of the pipeline generates prose.
   Every stage that makes a *decision* is either deterministic code or a model constrained to
   emit a typed label from a fixed set.
3. **Rules are data, not code.** Classical rules live in a versioned rule store as machine-readable
   cards, each bound to a verbatim passage. Adding a book adds cards. The engine does not change.
4. **Retrieval is by structure first, similarity last.** A birth chart generates a precise, finite
   set of conditions. Those conditions are looked up exactly. Embedding similarity is a coverage
   auditing tool, never a source of justification (§3.6).
5. **Attribution over adjudication.** Where the classics disagree, the system reports the
   disagreement with attribution. It does not average, and it does not silently pick a winner
   (§3.8).
6. **Silence is a valid output.** "The texts we hold do not address this" is a first-class result,
   emitted routinely, and is the raw material of the gap log.

---

## 1. Birth data input

### 1.1 The `BirthRecord` — raw user input

```jsonc
{
  "schema": 1,
  "name": "…",                        // optional; never used in reasoning, only in rendering
  "date": "1987-03-14",               // proleptic Gregorian, always; see §1.4
  "time": "04:22:00",                 // local clock time as recorded, 24h
  "time_precision": "minute",         // second | minute | fiveminute | quarterhour | hour | unknown
  "time_source": "birth-certificate", // certificate | hospital | family | memory | rectified | unknown
  "place_query": "Thanjavur, Tamil Nadu, India",
  "latitude": 10.7870,                // decimal degrees, N positive
  "longitude": 79.1378,               // decimal degrees, E positive
  "altitude_m": 59,                   // optional; affects ascendant marginally at high latitude
  "timezone": "Asia/Kolkata",         // IANA identifier, NOT a UTC offset
  "utc_offset_declared": null,        // optional override; see §1.3
  "calendar_note": null               // free text, e.g. "recorded in Tamil calendar as …"
}
```

Two fields carry more weight than they appear to: `time_precision` and `time_source`. They
propagate all the way to §6's confidence annotations, because a rule keyed on the ascendant degree
means something different for a certificate time than for "sometime before dawn, my mother thinks."

### 1.2 Place resolution

`place_query` → coordinates is a **lookup, not an inference**. A geocoding step that guesses is a
silent source of chart error measured in degrees of ascendant.

- Offline gazetteer (GeoNames extract, shipped with the system) is authoritative. No network call
  at reasoning time.
- Ambiguity is **returned to the user, never resolved automatically**. "Springfield" produces a
  disambiguation list; it does not produce Illinois.
- If the user supplies explicit lat/long, that wins and geocoding is skipped; `place_query` becomes
  a display label only.
- Resolution provenance (`gazetteer:geonames-2026-01`, feature id, distance from query centroid) is
  recorded in the case file. Coordinates are rounded to 4 dp (~11 m) — beyond that is false
  precision against a birth time known to the minute.

### 1.3 Time zone and the historical-offset problem

This is the single largest source of wrong charts in amateur astrology software, and it is
entirely avoidable.

- **Never accept a bare UTC offset as primary input.** Accept an IANA zone id and resolve the
  offset *for that instant* through the tz database. India's IST is stable; Europe, the Americas,
  and pre-1950 Asia are not. War-time double summer time, mid-year DST rule changes, and zones
  that shifted their base offset (e.g. `Asia/Kolkata` was +05:53:20 LMT before 1906) are all in the
  tzdata and all invisible to an offset field.
- `utc_offset_declared` exists only for the case where a user has a document stating the offset
  that contradicts tzdata. If supplied and it disagrees with the resolved offset, the system
  **does not choose** — it computes both charts, reports the divergence, and asks. A one-hour error
  moves the ascendant by roughly one sign.
- **Ambiguous and non-existent local times.** During a DST fall-back, a local clock time occurs
  twice; during spring-forward, it does not occur at all. Both are hard errors requiring user
  input, not silently resolved to the first occurrence.
- **LMT.** For births before standard time was adopted at the birth place, the recorded time may be
  local mean time. Flag by date+place against a table of standard-time adoption dates; ask.

Output of this step:

```jsonc
{
  "utc_instant": "1987-03-13T22:52:00Z",
  "julian_day_ut": 2446868.4527777778,
  "offset_applied": "+05:30",
  "offset_source": "tzdata-2026a/Asia/Kolkata",
  "delta_t_seconds": 55.32,            // TT - UT, from Swiss Ephemeris
  "warnings": []
}
```

### 1.4 Calendar

All input dates are proleptic Gregorian. If a user supplies a Julian-calendar date (relevant only
for births before 1582 in Catholic Europe, later elsewhere — realistically never, but the
conversion must not be *wrong*), it is converted at input and the original is preserved in
`calendar_note`. Indian luni-solar calendar dates (Tamil, Vikram Samvat, Shaka) are **not**
auto-converted in Phase 2 — they are captured as text and the user must supply the Gregorian date.
Auto-conversion requires a panchanga engine and regional variant rules; it is a Phase 3 candidate.

### 1.5 Uncertain birth time

Uncertain time is not an error state. It is the normal case, and the architecture treats it as a
first-class mode rather than a degraded one.

**Representation.** A birth time is an interval `[t_early, t_late]` with a nominal point. A
certificate time to the minute is the interval `[t−30s, t+30s]`. "Morning" is `[06:00, 12:00]`.

**Three operating modes, selected by interval width:**

| Mode | Interval | Behaviour |
|---|---|---|
| **Point** | ≤ 4 minutes | Single chart. Standard pipeline. Ascendant-degree-sensitive rules permitted. |
| **Interval** | 4 min – ~2 h | **Stability analysis** (below). Chart computed at nominal time; every fact is tagged stable or unstable across the interval. |
| **Unknown** | > 2 h, or absent | **Chandra-lagna mode.** Chart erected from the Moon's sign as first house. No bhava-dependent rule fires. Ascendant, houses, and all house-derived facts are absent, not guessed. |

**Stability analysis (Interval mode).** The engine computes the chart at the nominal time and at a
sweep of instants across the interval (adaptive: bisect on every fact-changing boundary, so the
sweep is exact rather than sampled). Each fact in the `FactSet` (§4.3) is then labelled:

- `stable` — holds across the entire interval. Rules keyed on it fire normally.
- `unstable` — changes within the interval. Rules keyed on it are activated but **quarantined**:
  they may appear in the report only inside an explicit conditional frame ("if the birth was before
  04:31, then …"), never as an assertion.

This is cheap. The Moon moves ~0.5°/hour, so nakshatra and most varga placements are stable across
an hour; the ascendant moves ~1°/4 min and is the dominant unstable quantity, along with D-9/D-60
placements and house cusps. The output is a **sensitivity report** telling the user exactly what
their time uncertainty costs them — which is genuinely useful information and something most
software does not provide.

**Rectification** is explicitly **out of scope for Phase 2.** Attempting to fit a birth time to
reported life events requires a validated event-to-yoga mapping the system does not have and cannot
have until its predictive rules are themselves trusted. The `BirthRecord` carries
`time_source: "rectified"` so that externally rectified times are marked as such and never
represented as documentary. Life events supplied by the user are stored (§5.3) against the day when
rectification becomes tractable, but are not consumed by the reasoning engine.

---

## 2. Astronomical engine

Pure deterministic computation. No model, no retrieval, no interpretation. Its entire output is one
immutable, content-addressed object: the `ChartBundle`.

### 2.1 Library and data — a correction to the project's stated plan

`Ephemeris/` contains **41 PDFs of printed yearly ephemeris tables** (`ae_1996d.pdf` …
`ae_2035d.pdf`, Astrodienst's published tables). These are *not* Swiss Ephemeris data files. The
Swiss Ephemeris is a C library whose binary data files are named `sepl_18.se1`, `semo_18.se1`,
`seas_18.se1` and similar. The project README states that the 1996–2035 span of these PDFs "sets
the range of birth dates the engine can serve." **That is not correct**, and building to it would
needlessly cripple the system.

Revised plan:

- **Compute** with **pyswisseph**, the Python binding to the Swiss Ephemeris.
- **Data:** ship the `.se1` files (`sepl`, `semo`, `seas` for the −3000…+3000 range is a few tens of
  MB). Fall back to the built-in **Moshier** analytic ephemeris (`SEFLG_MOSEPH`) if data files are
  absent — no external data, accuracy ~0.1 arcsec against JPL over ±3000 years, which is far below
  the resolution at which any classical rule operates. Either way the served date range becomes
  effectively unbounded for human births, not 1996–2035.
- **The PDFs become a test oracle, and a good one.** They are an independently published,
  human-readable table of planetary positions. §8.6's golden-chart suite spot-checks computed
  sidereal longitudes against these printed tables for a sample of dates across the 40 years. This
  is the best use of the folder, and it turns a misfiled input into genuine verification value.
- `ae_2019d (1).pdf` is a byte-identical duplicate (already verified by MD5). Any tooling that
  indexes the folder de-duplicates by checksum.

**Open question to resolve before writing code:** the project's main interpreter is Python 3.14, and
Phase 1 already hit the "no 3.14 wheels" wall for the OCR stack and solved it with a separate 3.12
venv provisioned by `uv`. pyswisseph's 3.14 wheel availability is unverified. Decide early:
confirm a 3.14 wheel exists, or stand the engine up on the 3.12 venv from the start. Discovering
this after the engine is written is the expensive order.

**Licensing note for the record:** the Swiss Ephemeris is AGPL or commercial. For a private research
project this is fine; it constrains any future distribution and should be a conscious decision, not
a discovery.

### 2.2 Ayanamsa

Sidereal longitude = tropical longitude − ayanamsa. The choice of ayanamsa shifts every planet by
roughly 24° and can move a planet across a sign boundary. It is therefore a *material* choice.

**The classical texts do not specify one.** Brihat Jataka and Phaladeepika predate the divergence of
modern ayanamsa definitions entirely. This means the ayanamsa is an **unsourced engineering choice**
— the first of several — and the architecture requires it to be declared as such:

- Configurable; default **Lahiri / Chitrapaksha** (`SE_SIDM_LAHIRI`), being the Indian government
  standard and the basis of most published panchangas.
- Supported alternatives: True Chitra, Raman, Krishnamurti (KP), Yukteshwar, Fagan-Bradley.
- The ayanamsa id **and its computed value at the birth instant** are stored in the `ChartBundle`
  and surfaced in the audit trace, tagged `provenance: engine-choice, unsourced`.
- The system can recompute a chart under an alternate ayanamsa and diff the `FactSet`, showing the
  user precisely which conclusions depend on the choice. Most will not. Those that do should be
  visible.

### 2.3 Planetary positions

Seven grahas plus the nodes. Note that **Brihat Jataka does not use Rahu and Ketu at all** (its own
introduction says so); Phaladeepika does. The engine computes them regardless; the rule layer
determines whether a given book's rules reference them.

For each body: sidereal longitude, latitude, distance, longitude speed (→ retrograde flag), and
derived placements.

```jsonc
{
  "body": "Mars",
  "lon_sidereal": 191.5721,     // degrees 0–360
  "lat": 1.2033,
  "speed_lon": -0.1204,          // negative = retrograde
  "retrograde": true,
  "sign": "Libra", "sign_index": 6, "deg_in_sign": 11.5721,
  "nakshatra": "Swati", "nakshatra_pada": 2, "nakshatra_lord": "Rahu",
  "navamsa_sign": "Sagittarius",
  "dignity": "debilitated",      // exalted | moolatrikona | own | friendly | neutral | inimical | debilitated
  "combust": false,
  "war": null                    // graha yuddha participant, if within the classical orb
}
```

Details that are easy to get wrong and must be pinned in the implementation contract:

- **Node type.** True node vs mean node is configurable (default: true node). They differ by up to
  ~1.7°, enough to change a nakshatra. Ketu is always exactly 180° from Rahu.
- **Combustion orbs** are doctrine, not astronomy. They must come from the corpus as rule cards
  (Phaladeepika ch.2 and ch.4 territory), not from the engine's constants. Where the corpus is
  silent, the engine records "combustion undetermined" rather than applying a value from general
  practice. This is the pattern for *every* doctrinal constant.
- **Dignity tables** likewise. Phaladeepika ch.1 verse 6 gives sign lords, verse 7 gives
  moolatrikona ranges with exact degrees. These are ingested as rule cards and the engine reads them
  from the rule store. Hardcoding an exaltation table is a violation of §0.2's third principle,
  however tempting, because it means one book's doctrine is silently baked into the engine.
- **Graha yuddha** (planetary war) needs a latitude-based or longitude-based winner rule; sources
  differ. Compute the geometry, defer the verdict to rule cards.

### 2.4 Houses

Two distinct things that are routinely conflated, and the conflation is a real bug source:

- **Rasi chart** — the sign a planet occupies. Sign-based.
- **Bhava chalit** — the house a planet occupies under a cusp-based house system. Degree-based.

The engine computes **both, always**, and every fact records which frame it came from.

- **Default house system: whole sign** (`Bhava = Rasi`, first house = ascendant's whole sign). This
  is the correct default for Brihat Jataka and Phaladeepika, whose "houses" are signs counted from
  lagna.
- Also supported: Sripati, equal, Placidus, Koch, KP (Placidus + KP cusps). Available for
  comparison, not for MVP interpretation.
- Ascendant, MC, and the other angles computed via `swe.houses_ex` with the sidereal flag.
- **High-latitude degeneracy.** Above ~66°, Placidus and Koch fail or produce absurd cusps. Whole
  sign always works. The engine detects the condition and refuses cusp-based systems rather than
  emitting nonsense.

### 2.5 Vargas (divisional charts)

Computed as a general function `varga(longitude, D) → sign`, parameterised per divisional scheme
rather than sixteen bespoke functions.

| Varga | Name | Sourced in MVP corpus |
|---|---|---|
| D-1 | Rasi | BJ ch.1, PD ch.1 |
| D-2 | Hora | BJ ch.1, PD ch.3 |
| D-3 | Drekkana | BJ ch.1 & ch.27 (whole chapter), PD ch.3 |
| D-7 | Saptamsa | PD ch.3 |
| D-9 | Navamsa | BJ ch.1, PD ch.3 — heavily used throughout BJ |
| D-12 | Dwadasamsa | BJ ch.1, PD ch.3 |
| D-30 | Trimsamsa | BJ ch.1, PD ch.3 |
| D-4, D-10, D-16, D-20, D-24, D-27, D-40, D-45, D-60 | — | Partly PD ch.21; **verify chapter-by-chapter before claiming coverage** |

The engine computes all sixteen. **It interprets only those the corpus supplies rules for.** This is
the general pattern: computing more than you can interpret is free and harmless; interpreting more
than you can cite is the failure mode.

Two traps: the Drekkana and Trimsamsa assignment schemes differ between authorities, and D-30 has a
distinct odd/even-sign rule. Both must be taken from the corpus (BJ ch.1 and ch.27 give
Varahamihira's), and the scheme identity recorded on every derived fact so a D-3 fact from
Varahamihira's scheme is never silently compared against another's.

### 2.6 Strengths

- **Shadbala** — sthana, dig, kala, chesta, naisargika, drik bala, in rupas. Phaladeepika ch.4 is
  the source and gives the strength thresholds directly in verses 22–23 (Sun 6.5 rupas, Moon 6,
  Mars 5, Mercury 7, Jupiter 8.5, Venus 5.5, Saturn 5).
  > **Corpus caveat, already known:** the *sub-table* of per-component thresholds on printed page 50
  > is one of the ~10 tabular pages still flattened into prose by the Phase 1 conversion. The verse
  > thresholds are clean; the component table is not yet reliable. See §3.9.
- **Ashtakavarga** — BAV per planet, SAV, and the trikona/ekadhipatya reductions. BJ ch.9 and PD
  ch.23–24. The bindu contribution tables must be read out of the corpus, not from memory.
- **Vimsopaka bala** (varga-weighted strength) — verify source before promising.
- **Avasthas** — baladi, deeptadi, and the Chandra-kriya/avastha/vela set from PD ch.4.

Ashtakavarga carries **self-checking invariants**, which make it unusually good regression material:
each planet's BAV has a fixed classical total and the sarvashtakavarga totals 337. These totals
should be *derived from the corpus tables and asserted*, not hardcoded — precisely because Phase 1
already found a page in Phaladeepika (printed page 221) where the printed chart totals 44 instead of
48. That defect was verified by eye, preserved as printed, and flagged in
`verified/p0221.json`. The engine must reproduce the correct computation while the corpus retains
the printed error; the two must not be allowed to contaminate each other.

### 2.7 Dashas

- **Vimshottari** — the primary system. **Confirmed present in the corpus:** Phaladeepika ch.19
  verse 2 gives the nakshatra groups from Krittika and the nine lords with periods (6, 10, 7, 18,
  16, 19, 17, 7, 20 years, totalling 120), and verse 3 gives the balance-at-birth calculation.
  Chapter 20 gives the effects of the dashas of house lords and their antardashas. Computed to at
  least three levels (mahadasha / antardasha / pratyantardasha).

  > **This chapter is also the clearest single illustration of why the rule layer must source from
  > verses and not from flattened tables.** Verse 2 correctly gives Venus 20 years. The *Notes*
  > table that follows it renders "Venus 10" and "Bharani" as "Bhara" — degraded in conversion or
  > in the source. A system that ingested the table would compute every dasha date after Venus
  > wrongly, and would do so with a citation. See §3.4 on provenance tiers.

  Note also that Phaladeepika ch.19 *itself* documents a methodological dispute about the balance
  calculation — Mantreswara divides by 60, "other authorities" divide by the actual nakshatra span,
  and the translator states Mantreswara is wrong. This is a conflict inside a single book, and §3.8
  must handle it. It is not hypothetical.
- **Kalachakra dasha** — PD ch.22.
- **Amsa and Pinda ayurdaya** — BJ ch.7–8. Varahamihira's own longevity/period system, and
  explicitly *not* Vimshottari. Both must be available and never conflated.
- **Ashtottari** — mentioned in BJ's introduction but not taught there. **Not sourceable from the
  MVP corpus.** Candidate gap-log entry.

Dasha computation is pure arithmetic over the Moon's longitude and must be exact to the day, with
timezone-correct date arithmetic. Balance-at-birth is the classic off-by-a-fraction bug; the
120-year total and the proportional-balance property are asserted invariants.

### 2.8 Transits (gochara)

- Planetary transits over natal positions, primarily **counted from the natal Moon** — Phaladeepika
  ch.26 is explicit that this is the reference frame, and it also raises the question of measuring
  from lagna and other planets, which is the doorway to Ashtakavarga transit analysis in ch.23.
- **Vedha** (obstruction) points, where sourced.
- Sade Sati (Saturn's transit of the 12th, 1st, 2nd from natal Moon).
- Transit-to-dasha correlation: the timing model in §4.9.
- Ashtakavarga-filtered transits (PD ch.23–24): a transit's effect graded by the bindus in the
  transited sign.

The reference frame (`from: moon | lagna | sun | natal-planet`) is a **mandatory field** on every
transit fact. Losing it is the most common way transit rules get misapplied.

### 2.9 Yogas

Yogas are **not** computed here and are **not** hardcoded. They are rule cards evaluated by the
generic condition evaluator in §4.5. This is a deliberate and load-bearing decision: the moment
`nabhasa_yogas.py` exists with 32 hand-written functions, the corpus stops being the source of
truth and the engine acquires a doctrine of its own.

What §2 provides is the *vocabulary* the yoga conditions are written against — §4.3's fact
predicates.

### 2.10 The `ChartBundle`

The complete, immutable output. Content-addressed by
`sha256(engine_version ‖ ephemeris_id ‖ ayanamsa_id ‖ house_system ‖ node_type ‖ canonical(ResolvedBirth))`.

```jsonc
{
  "schema": 1,
  "bundle_id": "sha256:9c1f…",
  "engine_version": "2.0.0",
  "ephemeris": { "source": "swisseph/se1", "version": "2.10.03", "delta_t": 55.32 },
  "settings": { "ayanamsa": "lahiri", "ayanamsa_value": 23.6421,
                "house_system": "whole_sign", "node_type": "true" },
  "resolved_birth": { … },            // §1.3 output
  "angles": { "ascendant": 271.3312, "mc": 183.9910, … },
  "bodies": [ { … } ],                // §2.3, one per graha + nodes + upagrahas
  "houses": { "whole_sign": [ … ], "sripati": [ … ] },
  "vargas": { "D9": { "Mars": "Sagittarius", … }, … },
  "strengths": { "shadbala": { … }, "ashtakavarga": { "bav": {…}, "sav": [ … ] } },
  "dashas": { "vimshottari": { "balance_at_birth": {…}, "timeline": [ … ] } },
  "stability": { "mode": "interval", "unstable_facts": [ … ] },   // §1.5
  "invariants_checked": [ "sav_total_337", "vimshottari_total_120y", … ]
}
```

Any invariant failure is a **hard stop**. The engine does not emit a bundle it could not verify.

---

## 3. Knowledge layer

### 3.1 What the corpus actually is

Two approved books, and the design must be honest about their shape:

| | Brihat Jataka | Phaladeepika |
|---|---|---|
| Lines | 6,282 | 5,969 |
| Chapters | 28 | 28 |
| Verse units | 408 (Devanagari + English) | 755 numbered English paragraphs |
| Page anchors | 219 | 265 |
| Script | Devanagari verse + English translation + commentary | English only, no Devanagari at all |
| Verse marker | `।। N ।।` closing a blockquote | `N. ` or `N-M. ` at line start |
| Commentary marker | `Commentary:` (P.S. Sastri) | `Notes —` / `Notes:` (G. S. Kapoor) |

Both carry `<!-- page <book-id>/pNNNN -->` HTML-comment anchors. **These anchors are the foundation
of the entire citation system** — they are the one artefact that ties a string in the Markdown back
to a specific rendered page of a specific scanned book, and the Phase 1 pipeline already guarantees
their integrity.

Four books remain unconverted (BPHS Vol. 1, Jataka Parijata, Uttara Kalamrita, Saravali). Per §0,
they stay unconverted until the gap log justifies one.

### 3.2 Chunking strategy

**Chunk on the book's own structure. Never on token count.** A fixed-window chunker would split a
verse from its translation and a translation from its number, and the citation system would be
worthless.

The atomic retrieval unit is the **verse unit**:

```
VerseUnit
├── locator          book-id, chapter, verse-number(s), page-anchor
├── section_title    the nearest preceding `### …` heading
├── mula             the Devanagari verse text, if present  [BJ only]
├── translation      the English rendering                  [tier 1]
├── commentary       Commentary:/Notes— block, if present    [tier 2 — see §3.4]
├── figures          transcribed tables/charts belonging to this unit
└── scope_context    the inherited reference frame — see below
```

Segmentation is driven by a per-book **chunk profile**, directly analogous to Phase 1's
`profiles/<book-id>.json` and for the same reason: the assembler must carry no book's anatomy as a
default. Phase 1 learned this the hard way when `build_book.py` hardcoded `has_deva()` in the
chapter-opener test and chapter detection could never have fired on a Latin-script book. The same
class of bug is waiting here.

```jsonc
// Corpus/profiles/phaladeepika.chunk.json
{
  "verse_unit_re": "^(\\d{1,3}(?:-\\d{1,3})?)\\.\\s",
  "commentary_re": "^Notes\\s*[—:-]",
  "commentary_tier": 2,
  "commentary_attribution": "G. S. Kapoor (translator)",
  "mula_present": false,
  "section_heading_level": 3,
  "page_anchor_re": "<!--\\s*page\\s+(\\S+)\\s*-->"
}
```

**Hierarchy and expansion.** Chunks form a tree: book → chapter → section → verse unit → {mula,
translation, commentary}. Retrieval returns verse units. Context expansion may pull the parent
chapter's preamble, because classical verses routinely depend on a scoping statement made once at
the top of a chapter.

**`scope_context` is the most important metadata field in the system.** Consider Phaladeepika ch.26:
every transit verse in it is implicitly *"from the natal Moon"*, stated once in the chapter preamble
and never repeated. A verse chunk lifted out of that context is not merely incomplete — it is
**wrong**, and wrong in a way that produces confident, plausible, incorrect output. Therefore:

- Every chunk carries a resolved `scope_context`: the reference frame (`lagna`, `chandra-lagna`,
  `surya-lagna`, a karaka, a specific varga) that its conditions are measured from.
- It is resolved at chunk-build time by inheritance from the chapter, and it is
  **human-verified per chapter** — 56 chapters across the two books, a bounded, one-time,
  high-value task.
- A chunk with an unresolved scope is quarantined and cannot become a rule card.

### 3.3 Metadata

Per chunk:

```jsonc
{
  "chunk_id": "phaladeepika/ch19/v2",
  "book_id": "phaladeepika",
  "book_title": "Phaladeepika",
  "author": "Mantreswara",
  "translator": "Dr. G. S. Kapoor",
  "tradition": "parashari",
  "chapter": 19, "chapter_title": "Dasas and their effects",
  "section_title": null,
  "verse": "2",
  "page_anchor": "phaladeepika/p0174",
  "printed_page": 174,
  "tier": 1,
  "scope_context": { "frame": "moon-nakshatra", "verified_by": "owner", "date": "…" },
  "topics": ["dasha", "vimshottari", "nakshatra"],
  "text_sha256": "…",
  "char_span": [412031, 412894]
}
```

`text_sha256` and `char_span` are what make the citation system verifiable rather than decorative
(§6.3).

### 3.4 Provenance tiers — mula vs bhashya

A distinction the system must never blur:

| Tier | Content | Attribution | Weight |
|---|---|---|---|
| **1** | The verse / its direct translation | The classical author (Varahamihira, Mantreswara) | Primary |
| **2** | `Commentary:` / `Notes —` blocks | The **translator** (P. S. Sastri, G. S. Kapoor), 20th century | Supporting |
| **3** | Ready-made tables, worked examples, editorial apparatus | Translator/publisher | Illustrative only |

Attributing Kapoor's opinion to Mantreswara is a fidelity failure of the same kind as inventing a
verse. And tier 3 is demonstrably the least reliable material in the corpus: the Phaladeepika ch.19
dasha table gives Venus 10 years where the verse it summarises gives 20.

**Rule cards may be extracted from tier 1 and tier 2. Tier 3 may never be the sole basis of a
rule card**, though it may be quoted as supporting illustration.

### 3.5 The rule store — the missing layer

Here is the central architectural claim of this document.

**Prose cannot be executed, and a language model reading prose cannot be trusted to extract the
rule.** Between the corpus and the reasoning engine there must be a layer the corpus does not
contain and the engine cannot supply: a **rule store** of machine-readable rule cards, each derived
from an exact passage, each carrying its citation.

Without it, there are only two options, and both are unacceptable:

- **(a)** Let the model read raw passages and decide what applies. This is unverifiable, and the
  model's pretrained astrology will dominate.
- **(b)** Hardcode astrology into Python. This makes the engine the authority instead of the books,
  and it means every new book requires an engine change — destroying §7.

The rule card is what makes both §6 (explainability) and §7 (extensibility) actually achievable
rather than aspirational.

```yaml
# Rules/phaladeepika/ch08/PD.08.014.yaml
id: PD.08.014.a
schema: 1

source:
  book_id: phaladeepika
  chunk_id: phaladeepika/ch8/v14
  chapter: 8
  verse: "14"
  page_anchor: phaladeepika/p0089
  tier: 1
  quote: >-
    <verbatim substring of Knowledge/phaladeepika.md — byte-exact>
  quote_sha256: "…"
  char_span: [201144, 201502]

scope:
  frame: lagna              # from §3.2 scope_context; never defaulted
  varga: D1

conditions:
  all:
    - in_house: { graha: Sun, house: 10 }

predicts:
  domain: career
  polarity: favourable
  statements:
    - "Success and recognition in occupation; favour from those in authority."

modifiers:                   # how other factors qualify this rule, where the text says so
  - if:   { dignity: { graha: Sun, is: debilitated } }
    then: { weight_multiplier: 0.4, note: "…" }

timing: natal                # natal | dasha | transit
weight: 1.0
tags: [bhava-10, graha-sun, livelihood]

extraction:
  method: assisted           # assisted | manual
  verified_by: owner
  verified_date: 2026-08-??
  notes: "…"
```

**How rule cards are produced.** A model proposes; a human disposes. Exactly the workflow Phase 1
converged on with `propose_charts.py` for Phaladeepika's Ashtakavarga charts — machine-proposed,
checked against the rendered page, and the machine caught two things a human would have missed
while the human caught what the machine could not judge.

1. A model reads one verse unit and proposes zero or more rule cards.
2. It **may not paraphrase**: `quote` must be a byte-exact substring of the corpus file. A build
   step asserts this. If the model cannot ground a proposed rule in a verbatim span, the card is
   rejected automatically, before a human sees it.
3. The human reviews conditions and predictions against the passage. Anything ambiguous is marked
   `needs-review` and does not enter the active store.
4. `rules_verify` runs on every build: every card's `quote_sha256` must still match the corpus, and
   every `char_span` must still resolve. If a book is ever re-converted, stale cards **fail loudly**
   rather than silently citing text that no longer exists.

That last property is the direct descendant of Phase 1's `ocr_fingerprint` mechanism, which made
`build_book.py` refuse to run against stale figure transcriptions. It worked, and it is the right
pattern to carry forward.

**Scale estimate.** 408 + 755 = 1,163 verse units. Not every verse yields a rule (invocations,
colophons, definitions, methodology). A realistic yield is perhaps 600–900 cards from the two
books, with the definitional verses (sign lords, moolatrikona ranges, dasha periods) becoming
**reference tables** rather than predictive cards — the same schema, `predicts: null`, feeding the
engine's doctrinal constants per §2.3.

This is the single largest work item in Phase 2. It is also the one that makes everything else
possible, and it is bounded and checkable.

### 3.6 Retrieval strategy — three indices, sharply separated

**A birth chart is not a natural-language query. It is a precise, finite set of conditions.** Naive
semantic RAG over astrology prose fails badly here, because "Mars in the 7th" and "Mars in the 8th"
embed almost identically while meaning entirely different things. Similarity search cannot
guarantee that a retrieved passage's conditions actually match the chart — and a passage that
doesn't match the chart is not evidence, it is decoration.

| | Index | Mechanism | Used for | May justify a prediction? |
|---|---|---|---|---|
| **1** | **Predicate index** | Exact key lookup: canonical fact key → rule card ids. A plain inverted index. | Primary rule activation. Deterministic, exhaustive, sub-millisecond. | **Yes — the only one that may.** |
| **2** | **Structural index** | book/chapter/verse tree + topic taxonomy | "What does the corpus say about the 7th house?"; report assembly; browsing | Only via cards it surfaces |
| **3** | **Semantic index** | Embeddings over verse units | **(a)** coverage auditing — finding passages that *should* have become rule cards but didn't; **(b)** answering free-text doctrinal questions | **No. Never.** |

The strict exclusion of index 3 from the justification path is what prevents **citation laundering**
— the failure mode where a system generates a prediction and then retrieves a vaguely related
passage to hang beneath it. That output looks impeccably sourced and is not sourced at all.

Index 1's exhaustiveness is worth stating: given a `FactSet`, retrieval returns *every* rule card in
the store whose conditions could match. There is no top-k, no recall cliff, no relevance threshold.
The system knows exactly what its books say about this chart. That is a property naive RAG cannot
offer and an astrologer would take for granted.

### 3.7 Source attribution and the citation system

Every citation resolves to:

```
Phaladeepika, ch. 8, v. 14  ·  Mantreswara, tr. G. S. Kapoor  ·  printed p. 89
  ↳ Knowledge/phaladeepika.md, chars 201144–201502
  ↳ page anchor phaladeepika/p0089
  ↳ Books/Mantreswara_s__Phaladeeplka_.pdf, PDF page 89
```

Four levels of resolution: human-readable reference, exact span in the corpus file, the Phase 1 page
anchor, and the physical page of the original PDF. A user can always get from a sentence in the
output to the scan of the printed page it came from. That is the standard.

**Devanagari is never a citation surface of record.** The Phase 1 status report is explicit that
Brihat Jataka's verse *structure* is fully verified but its *glyphs* are not — individual characters
may still be wrong at roughly the 1.5% rate measured in the OCR benchmark. Therefore: the mula may
be *displayed* alongside a citation, marked as unverified at glyph level, but the rule card's
`quote` is always taken from the **English translation**, which is Latin-script and was measured at
~1.3% CER against a far more forgiving error profile. Sanskrit quotation becomes authoritative only
after a glyph-level verification pass, which is a Phase 1 debt, not a Phase 2 task.

### 3.8 Conflict handling

Four distinct situations, routinely lumped together and requiring different responses:

| Type | Description | Response |
|---|---|---|
| **Silence** | One book covers it, another doesn't | **Not a conflict.** Use what exists. |
| **Refinement** | One rule is a special case of another | Specificity ordering (below). Both cited. |
| **Method divergence** | Different procedures for the same quantity | Owner-configured precedence, both computed, divergence reported. |
| **Contradiction** | Same conditions, incompatible outcomes | **Report both, attributed. Never resolve silently.** |

**Resolution order:**

1. **Specificity wins.** More matched conditions = more specific = higher priority, CSS-style. A
   rule for "Mars in the 7th in Libra debilitated" outranks "Mars in the 7th." The general rule is
   not discarded; it is subordinated, and both remain in the trace.
2. **Configured precedence.** `Rules/precedence.yaml`, set by the project owner, per domain — not
   a global ranking, because a book authoritative on yogas may not be authoritative on dashas.
   Defaults are declared, versioned, and visible in the trace.
3. **Unresolved contradiction → attributed disagreement.** Surfaced in the output as:
   > *On this point the texts differ. Varahamihira (BJ 20.4) holds …; Mantreswara (PD 8.14) holds …*

   The system does **not** average them, and does not pick. This is what a scholar-astrologer
   actually does, it is more useful than a false consensus, and it is the only honest option.
4. **Every conflict is recorded** as a `ConflictRecord` in the case file whether or not it was
   resolved. Accumulated conflict records are a research artefact in their own right.

Note that conflicts arise **within** a single book, not only between books. Phaladeepika ch.19
contains a live methodological dispute over the dasha-balance calculation in which the translator
declares the author's method incorrect (§2.7). The conflict machinery must handle intra-book
tier-1-vs-tier-2 disagreement from day one, because the MVP corpus already contains one.

The only role a model plays here is **classifying** whether two cards genuinely contradict or merely
differ in scope — and its output is a label from a fixed set, not prose.

### 3.9 Known corpus defects the knowledge layer must carry

Inherited from Phase 1 and non-negotiable — the corpus is preserved as printed, so the *knowledge
layer* absorbs these, never by editing `Knowledge/`:

| Defect | Effect on Phase 2 |
|---|---|
| Devanagari not glyph-verified (~1.5% CER) | Mula never a citation of record (§3.7) |
| ~10 Phaladeepika pages still tabular-flattened into prose (incl. the Shadbala component table, p.50) | Those pages are **excluded from rule extraction** until transcribed. Listed in the gap log. |
| 17 Brihat Jataka figures pending transcription (7 tables, 10 charts) | Same exclusion. |
| Phaladeepika printed p.221 Ashtakavarga totals 44, not 48 (source defect, preserved) | Engine computes correctly; corpus retains the error; a test asserts the two stay separate. |
| Brihat Jataka printed p.31 has a duplicated line (typesetting defect, preserved) | Deduplicate at chunk build; do not edit the corpus. |
| Saravali's diacritics destroyed in the source PDF | Not in MVP. Blocks Sanskrit-term matching when that book is added. |

---

## 4. Reasoning engine

The core of the system. A staged pipeline with typed inputs and outputs at every boundary, in which
**exactly one stage generates prose**.

### 4.0 Stage map, and one deliberate reordering

| # | Stage | Engine | Prose? |
|---|---|---|---|
| 0 | Birth resolution | code | no |
| 1 | Chart computation | code | no |
| 2 | Fact extraction | code | no |
| 3 | Yoga identification | code (DSL) | no |
| 4 | Strength determination | code | no |
| 5 | House evaluation | code | no |
| 6 | **Rule activation & retrieval** | code (index) | no |
| 7 | Adjudication, weighting & salience | code + constrained model | no |
| 8 | **Synthesis** | **model** | **yes** |
| 9 | Groundedness verification | code (+ model as second opinion) | no |
| 10 | Rendering | code | no |

**The reordering, and why it matters.** The brief placed *retrieve supporting passages* at stage 7,
after synthesis. This design moves retrieval to stage 6, **before** synthesis, and the change is not
cosmetic:

> If you synthesise first and retrieve second, you have built a citation-laundering machine. The
> conclusions come from the model; the passages are decoration attached afterwards. The output will
> look impeccably sourced and will not be sourced at all — and, worse, it will be *undetectably*
> unsourced, because every sentence has a footnote.

Retrieving first inverts the dependency: the model is handed a closed set of adjudicated,
chart-matched, cited claims and asked to compose them. It cannot introduce a conclusion, because
there is nothing to introduce it from. Synthesis becomes a writing task rather than a reasoning
task, which is the only form of it that can be verified.

This is the same principle that governs the whole design: the model writes, it does not decide.

---

### Stage 0 — Birth resolution

| | |
|---|---|
| **In** | `BirthRecord` (§1.1) |
| **Out** | `ResolvedBirth` — UTC instant, Julian day, coordinates, uncertainty interval, warnings |
| **Engine** | Deterministic. A model may parse messy free-text input into the schema, but the resolved values are always code-derived and shown back to the user for confirmation. |
| **Fails when** | Ambiguous place, ambiguous/non-existent local time, offset conflict. All are user-resolved, never auto-resolved. |

### Stage 1 — Chart computation

| | |
|---|---|
| **In** | `ResolvedBirth` |
| **Out** | `ChartBundle` (§2.10) — content-addressed, immutable, invariant-checked |
| **Engine** | Pure code. Swiss Ephemeris. |
| **Fails when** | Any invariant fails (SAV ≠ 337, Vimshottari ≠ 120y, varga cell count wrong). Hard stop. |

### Stage 2 — Fact extraction

Where astronomy becomes vocabulary. Continuous quantities become the discrete predicates classical
rules are written in.

| | |
|---|---|
| **In** | `ChartBundle` |
| **Out** | `FactSet` — a set of typed, canonically-keyed facts |
| **Engine** | Pure code. |

Every fact:

```jsonc
{
  "key": "in_house(Mars,7)",              // canonical string — the predicate index key
  "predicate": "in_house",
  "args": { "graha": "Mars", "house": 7 },
  "frame": { "reference": "lagna", "varga": "D1", "house_system": "whole_sign" },
  "evidence": { "lon_sidereal": 191.5721, "sign": "Libra", "deg_in_sign": 11.5721 },
  "stability": "stable"                    // §1.5
}
```

`evidence` is what lets §6 answer "how do you know?" with a number rather than a restatement.

**The predicate vocabulary** (`Rules/vocabulary.yaml`, versioned, extensible):

- *Placement* — `in_house`, `in_sign`, `in_nakshatra`, `in_varga_sign`, `in_pada`
- *Rulership* — `lord_of_house`, `lord_of_sign`, `dispositor`, `karaka_for`
- *Relation* — `conjunct`, `aspects`, `mutual_aspect`, `exchange`, `hemmed_between`
- *Condition* — `dignity`, `retrograde`, `combust`, `in_graha_yuddha`, `direction_strength`
- *Quantitative* — `shadbala_rupas`, `bav_bindus`, `sav_bindus`, `avastha`
- *Temporal* — `dasha_lord_at`, `transit_from_moon`, `transit_in_sign`
- *Derived* — `benefic`, `malefic`, `functional_benefic_for_lagna`

Each entry declares arity, argument domains, and — critically — **which frames it is valid in**, so
a rule can never silently compare a D-9 fact against a D-1 rule.

Typical yield: several hundred facts per chart.

### Stage 3 — Yoga identification

| | |
|---|---|
| **In** | `FactSet`, rule store (yoga-typed cards) |
| **Out** | `YogaSet` — instances with the exact bindings that satisfied them |
| **Engine** | Pure code: the generic condition evaluator over rule-card conditions. |

No yoga is hardcoded (§2.9). A detected yoga carries its satisfying bindings, so the trace can
state *why*:

```jsonc
{
  "yoga_id": "BJ.12.003.mala",
  "name": "Mala Yoga",
  "rule_card": "BJ.12.003.a",
  "satisfied_by": [ "in_house(Jupiter,4)", "in_house(Venus,7)", "in_house(Moon,10)" ],
  "cancelled_by": [],
  "citation": { "book": "brihat-jataka", "chapter": 12, "verse": "3", "page_anchor": "brihat-jataka/p0138" }
}
```

**Cancellation (bhanga)** is first-class. Classical yogas are routinely nullified by other
conditions, and a system that reports Raja Yogas without their cancellations is worse than useless.
Cancellation conditions live on the rule card and produce `cancelled_by` bindings; a cancelled yoga
is **retained and reported as cancelled**, never dropped silently.

### Stage 4 — Strength determination

| | |
|---|---|
| **In** | `ChartBundle`, `FactSet`, reference-table rule cards (thresholds) |
| **Out** | `StrengthTable` — per graha and per bhava, absolute and relative, with thresholds applied |
| **Engine** | Pure code. |

Numbers come from §2.6; the *thresholds that make a number mean "strong"* come from the corpus
(PD ch.4 vv.22–23). Output is both the raw rupas and the sourced verdict, with the citation for the
threshold attached.

Strength is what turns a flat list of activated rules into a weighted one. A rule keyed on a
debilitated, combust, weak graha and a rule keyed on an exalted one with 8 rupas are not equally
loud, and Stage 7 needs this table to say so.

### Stage 5 — House evaluation

| | |
|---|---|
| **In** | `FactSet`, `StrengthTable`, `YogaSet` |
| **Out** | `HouseVerdicts` — twelve structured assessments |
| **Engine** | Pure code + rule activation. |

For each bhava, the classical assessment inputs, assembled systematically:

- occupants; the lord and its placement, dignity, strength
- aspects to the bhava and to its lord
- the relevant karaka, and its condition
- bhava bala; SAV bindus in the sign
- yogas involving this house
- the lord's functional nature for this ascendant

Sources: Phaladeepika ch.15 (*Assessment of houses*) and ch.16 (*General effects of the twelve
houses*) are precisely this procedure written down, which is a strong signal that the stage boundary
is drawn in the right place.

Output per house is structured, not prose:

```jsonc
{
  "house": 7, "sign": "Cancer", "lord": "Moon",
  "lord_placement": { "house": 2, "sign": "Aquarius", "dignity": "neutral" },
  "occupants": ["Saturn"], "aspects_received": ["Jupiter"],
  "karaka": { "graha": "Venus", "condition": "strong" },
  "sav_bindus": 24,
  "strength_verdict": { "value": "moderate", "basis": ["…"], "threshold_card": "PD.04.022.a" },
  "yogas": [ … ],
  "activated_rules": [ … ]
}
```

### Stage 6 — Rule activation and retrieval

| | |
|---|---|
| **In** | `FactSet`, `YogaSet`, `StrengthTable`, `HouseVerdicts`, rule store |
| **Out** | `ActivationSet` — every rule card whose conditions evaluate true, with bindings and passages |
| **Engine** | Pure code: predicate index lookup + condition evaluation. **No model.** |

Two steps:

1. **Candidate generation.** Every fact key is looked up in the predicate index. Union of all hits.
2. **Condition evaluation.** Each candidate's full condition expression is evaluated against the
   `FactSet`. Only rules that evaluate **true**, with complete bindings, survive.

Step 2 is not redundant. A card indexed under `in_house(Mars,7)` may require three further
conditions; indexing only guarantees candidacy. **The condition evaluator is the gate through which
all justification passes**, and it is re-run independently in Stage 9 rather than trusted.

Each activation carries its passage inline, so nothing downstream needs corpus access:

```jsonc
{
  "activation_id": "act-0142",
  "rule_card": "PD.08.014.a",
  "bindings": { "graha": "Sun", "house": 10 },
  "supporting_facts": [ "in_house(Sun,10)" ],
  "quote": "<verbatim>",
  "citation": { … },
  "tier": 1,
  "stability": "stable",
  "specificity": 1
}
```

Typical yield: 150–400 activations for a full chart. Far too many for a report — which is exactly
what Stage 7 is for.

### Stage 7 — Adjudication, weighting and salience

The stage that separates a lookup table from an astrologer.

| | |
|---|---|
| **In** | `ActivationSet`, `StrengthTable`, `precedence.yaml` |
| **Out** | `ClaimSet` (weighted, adjudicated) + `ConflictRecord[]` + `CoverageReport` |
| **Engine** | Deterministic for conflict and weight. A model is permitted **only** to classify contradiction-vs-scope-difference, emitting a label from a fixed set — never prose, never a new claim. |

**7a. Conflict adjudication** — §3.8's four types and resolution order.

**7b. Weighting.** Each surviving claim gets a weight from declared, inspectable factors:

- the rule card's own `weight`
- **strength of the significators the rule is keyed on** (Stage 4) — a rule about a 2-rupa Saturn is
  quieter than the same rule about an 8-rupa Saturn
- provenance tier (1 > 2)
- specificity
- stability (§1.5) — an unstable fact's claims are quarantined regardless of weight

**7c. Convergence detection.** This is how real synthesis works, and it must be explicit rather than
left to the model's intuition. Claims are grouped by `(domain, polarity)` and scored by the number
of **independent** rule cards supporting them — independence measured across books and across
distinct chart significators. Three unrelated rules from two books all pointing at difficulty in the
7th house is a *finding*. One rule pointing there is a *mention*. The distinction is the difference
between a competent reading and a horoscope column, and encoding it here means the final report can
honestly say "strongly indicated" and mean something specific by it.

**7d. Salience.** An experienced astrologer does not weight 300 rules equally; they notice what is
striking. Salience = weight × convergence × rarity (how unusual the configuration is across a
reference population of charts) × domain priority. The top-N by salience per domain proceed to
synthesis; the remainder stay in the case file and appear in the full audit view. **Nothing is
discarded** — the distinction is between what is *reported* and what is *recorded*.

**7e. Coverage report.** Domains and houses with **zero** activations. This is not an error; it is
the honest statement of what the corpus does not cover, it drives §6.4's abstention behaviour, and
it accumulates into the gap log (§7.4) that governs whether the corpus freeze is ever lifted.

### Stage 8 — Synthesis

The only stage that generates prose.

| | |
|---|---|
| **In** | `ClaimSet` (adjudicated, weighted, salience-ranked, each with quote + citation), `ConflictRecord[]`, `CoverageReport`, chart summary, report specification |
| **Out** | `Narrative` — prose in which **every sentence carries the claim ids it derives from** |
| **Engine** | Language model, tightly constrained. |

**What the model receives:** only the adjudicated claims and their attached quotes. **Not** the
corpus, **not** the activation set, **not** raw passages beyond the quotes on the claims it is
composing. Minimising what is in context is a control, not an optimisation: a passage the model can
see is a passage it can quote out of scope.

**What the model is asked to do:** organise, sequence, weight in language ("strongly indicated" vs
"a minor supporting factor"), resolve register and repetition, and write in the voice of an
experienced astrologer. That is genuine, valuable work — and it is *writing*, not deciding.

**What the model may not do**, enforced by Stage 9 rather than by instruction:

- introduce any astrological assertion not present in the `ClaimSet`
- state any number not present in the `ChartBundle`
- merge two claims into a conclusion neither supports
- drop a `ConflictRecord` that Stage 7 marked as reportable
- convert an unstable-fact claim into an unconditional statement

Output is structured, not a blob:

```jsonc
{
  "sections": [
    { "id": "career", "title": "Profession and livelihood",
      "sentences": [
        { "text": "The Sun in the tenth house from the ascendant indicates recognition in occupation and the favour of those in authority.",
          "claim_ids": ["clm-0142"], "hedge": "indicated", "conflict_ids": [] }
      ] } ]
}
```

**Prose is generated per claim-cluster, not per report.** A single mega-prompt over 300 claims is
where drift and invention enter. Small, bounded generations over 3–8 related claims are checkable,
regenerable in isolation, and cheap to retry.

### Stage 9 — Groundedness verification

The stage that makes §0.1 true rather than aspirational.

| | |
|---|---|
| **In** | `Narrative`, `ClaimSet`, `FactSet`, `ChartBundle`, corpus |
| **Out** | `VerifiedNarrative`, or a rejection with per-sentence reasons |
| **Engine** | **Deterministic code is authoritative.** A model may act as a second-opinion checker; it can never overrule a code failure. |

Checks, all mandatory:

1. **Sentence coverage** — every sentence maps to ≥ 1 claim id. Zero-claim sentences are rejected
   unless tagged as connective/structural on a whitelist of forms.
2. **Claim validity** — every referenced claim exists in the `ClaimSet`.
3. **Quote integrity** — every claim's `quote_sha256` still matches `Knowledge/<book>.md` at
   `char_span`. Byte-exact.
4. **Condition re-evaluation** — every claim's rule conditions are **re-evaluated from scratch**
   against the `FactSet`. Stage 6's result is not trusted. A claim whose conditions no longer hold
   is a hard failure.
5. **Numeric grounding** — every number appearing in prose is matched against a value in the
   `ChartBundle`. Invented degrees and dates are caught here.
6. **Semantic containment** — does the sentence assert more than its claims support? This is the one
   check code cannot fully perform; a model performs it, and its finding is advisory-flag-for-review,
   never silent acceptance.
7. **Conflict preservation** — every reportable `ConflictRecord` appears in the output.
8. **Stability discipline** — no unstable-fact claim stated unconditionally.

On failure: regenerate that clause (bounded retries), then drop the sentence, then fail the report.
**A report that cannot be verified is not emitted.** There is no "emit with warnings" path for
groundedness failures — that path always becomes the default path.

### Stage 10 — Rendering

| | |
|---|---|
| **In** | `VerifiedNarrative`, `ChartBundle`, `CaseFile` |
| **Out** | Reader view · audit view · JSON trace |
| **Engine** | Pure code. |

Three views over identical data (§6.5). Rendering also applies the presentation policy of §6.6.

---

### 4.9 The timing model

Cutting across the stages: prediction in this tradition has three layers, and conflating them is the
most common way astrological software becomes noise.

| Layer | Question | Source |
|---|---|---|
| **Promise** | What does the chart contain at all? | Natal configuration — Stages 2–5 |
| **Period** | When is it active? | Dasha — PD ch.19–20; BJ ch.7–8 for Varahamihira's own scheme |
| **Trigger** | When precisely does it fire? | Transit — PD ch.26, ch.23–24 |

The rule: **an event not promised natally is not predicted by dasha or transit.** A dasha activates
what the chart contains; it does not create. This is encoded as a hard constraint in Stage 7 —
a dasha- or transit-timed claim must reference a natal claim as its `promise_id`, or it is dropped.

This single constraint eliminates the largest category of bad astrological output: a bare transit
reading with no natal basis.

---

## 5. Memory model

The distinction is not "what is expensive" but **"what is derived and what is given."** Everything
derived is recomputed. Nothing generated is ever treated as evidence.

### 5.1 Always recomputed, never stored as authority

Every astronomical and derived quantity: positions, houses, vargas, strengths, dashas, facts,
activations. All of it is a pure function of `ResolvedBirth` + engine settings, and all of it is
fast (whole-chart computation is milliseconds).

Caching is permitted **only** as content-addressed memoisation keyed on the `bundle_id` hash
(§2.10), which includes the engine version, ephemeris version, ayanamsa, house system and node type.
Change any input and the key changes and the cache misses. A cache that can go stale silently is a
worse bug than no cache: it means two runs of the same chart can disagree and neither is
identifiable as wrong.

### 5.2 Working memory — within one reasoning run

The stage outputs, held for the duration and persisted to the case file: `ResolvedBirth`,
`ChartBundle`, `FactSet`, `YogaSet`, `StrengthTable`, `HouseVerdicts`, `ActivationSet`, `ClaimSet`,
`ConflictRecord[]`, `CoverageReport`, `Narrative`.

**Stage isolation is enforced.** Each stage receives only its declared inputs. Stage 8 cannot read
the corpus; Stage 4 cannot read the narrative. This is not tidiness — it is what makes each stage
independently testable, and it is what stops the model from acquiring context it could hallucinate
from.

### 5.3 Persistent memory — the case file

`Cases/<case-id>/` — durable, versioned, per native:

| Stored | Why |
|---|---|
| `BirthRecord` + `ResolvedBirth` + engine settings | Exact reproducibility. Sufficient to regenerate everything. |
| The claim graph (structured, not prose) | The reasoning is durable and diffable across engine versions. |
| `ConflictRecord[]`, `CoverageReport` | Research value; gap-log input. |
| Rendered narratives, versioned by engine + rule-store version | So a user can see what changed and why. |
| **User-supplied life events** | Held for future rectification and calibration. **Not consumed by the reasoning engine in Phase 2** — see §1.5. |
| Owner overrides and corrections | Human judgment must be recordable and must survive regeneration. |

### 5.4 Never persisted as input

**Generated prose from a previous run must never become an input to a later run.** Only the
structured claim graph is durable across runs.

The reason is specific: if run N's narrative is context for run N+1, the model's phrasings become
premises, small inventions compound, and the system converges on a self-consistent house style that
has drifted from the books. It would be undetectable by inspection, because each successive output
looks like a refinement of the last. Structured claims are immune to this — they either match a
rule card and a fact or they do not.

Corollary for conversation: a follow-up question ("what about my career?") re-enters the pipeline at
Stage 7 with a different report specification. It **does not** continue the previous generation.
The chart is recomputed or restored from its content hash, and the claims are re-derived. Cheap,
and drift-free.

### 5.5 Global memory

Corpus (`Knowledge/`), rule store (`Rules/`), predicate vocabulary, precedence config, gazetteer,
glossary. All versioned. Every case file records the versions it was produced under, so a report can
always be explained in terms of the doctrine that produced it.

---

## 6. Explainability

### 6.1 The requirement

Every prediction traces to: **astronomical calculation → derived rule → source book → passage.**
Not as a footnote convention, but as a structural property enforced by machine.

### 6.2 The claim record

The unit of traceability. All four links mandatory; a claim missing any one cannot be constructed.

```jsonc
{
  "claim_id": "clm-0142",

  // 1 — ASTRONOMICAL
  "astronomical": {
    "bundle_id": "sha256:9c1f…",
    "quantities": [
      { "name": "Sun.lon_sidereal", "value": 271.4412, "unit": "deg",
        "computed_by": "swe.calc_ut(jd=2446868.4528, SE_SUN, SEFLG_SIDEREAL|SEFLG_SWIEPH)",
        "settings": { "ayanamsa": "lahiri", "ayanamsa_value": 23.6421 } }
    ]
  },

  // 2 — DERIVED RULE (facts, with the evidence that produced them)
  "derived": {
    "facts": [ { "key": "in_house(Sun,10)",
                 "frame": { "reference": "lagna", "varga": "D1", "house_system": "whole_sign" },
                 "evidence": { "sign": "Capricorn", "deg_in_sign": 1.4412, "lagna_sign": "Aries" } } ],
    "rule_card": "PD.08.014.a",
    "conditions_satisfied": [ "in_house(Sun,10)" ],
    "evaluator_version": "1.0.0"
  },

  // 3 — SOURCE BOOK
  "source": {
    "book_id": "phaladeepika", "book_title": "Phaladeepika",
    "author": "Mantreswara", "translator": "Dr. G. S. Kapoor",
    "chapter": 8, "verse": "14", "printed_page": 89, "tier": 1
  },

  // 4 — PASSAGE
  "passage": {
    "quote": "<verbatim>",
    "corpus_file": "Knowledge/phaladeepika.md",
    "char_span": [201144, 201502],
    "quote_sha256": "…",
    "page_anchor": "phaladeepika/p0089",
    "source_pdf": "Books/Mantreswara_s__Phaladeeplka_.pdf#page=89"
  },

  "weight": 0.72,
  "convergence": { "independent_supports": 2, "books": ["phaladeepika", "brihat-jataka"] },
  "stability": "stable",
  "conflicts_with": []
}
```

### 6.3 Enforcement, not convention

Groundedness is enforced at three separate points, deliberately redundant:

1. **Build time** — `rules_verify` asserts every rule card's quote is a byte-exact substring of the
   corpus at its span. A card citing text that no longer exists cannot enter the store.
2. **Run time, Stage 6** — a claim can only exist if its conditions evaluated true against facts
   that came from a verified `ChartBundle`.
3. **Run time, Stage 9** — conditions are re-evaluated from scratch and quote hashes re-checked
   against the corpus on disk. Stage 6 is not trusted.

Redundancy is intentional. This is the one property of the system that must not fail quietly, and
the Phase 1 experience is the argument: fabricated OCR text read as real content and survived
review; it was caught only by an independent check against the artefact the text claimed to derive
from.

### 6.4 Abstention

Refusing to answer is a designed behaviour, not a fallback.

- Zero activations for a domain → *"The texts currently in the corpus (Brihat Jataka, Phaladeepika)
  do not address this."* Never filled with general knowledge.
- Every report carries a **coverage map**: which houses and life domains have rule support and which
  do not, with counts.
- A domain covered only by tier-2 commentary is marked as such.
- Where the corpus is silent, the report names the book that would likely cover it *if* that is
  determinable from the books' own cross-references (Brihat Jataka's own introduction, for instance,
  states that female horoscopy "finds elaborate treatment in Saravali"). That is a corpus-sourced
  statement about coverage, not a prediction, and it is exactly the evidence the gap log wants.

### 6.5 Three views, one data set

| View | For | Content |
|---|---|---|
| **Reader** | The person whose chart it is | Prose, chart diagram, unobtrusive citation markers |
| **Audit** | The project owner, review | Every sentence annotated with claim ids, quotes, facts, computed values, weights, conflicts, and everything Stage 7 recorded but did not report |
| **Trace (JSON)** | Machine | The complete case file: bundle, facts, activations, claims, verification results |

The reader view is a *projection* of the audit view. It is never generated separately, so the two
cannot disagree.

### 6.6 Presentation policy for sensitive material

The corpus is a faithful reproduction of texts written between roughly the 6th and 15th centuries.
It contains material on death and longevity (BJ ch.7, ch.25; PD ch.13, ch.17), disease (PD ch.14),
female horoscopy (BJ ch.24, PD ch.11), and social categories — caste, servitude, disability — framed
in the terms of their period.

**Phase 1's fidelity rule is absolute and is not revisited: the corpus is preserved exactly as
printed.** This is a *presentation-layer* policy in Stage 10, and it changes nothing in
`Knowledge/`.

- **Attribution framing throughout.** The system's voice is always *"Phaladeepika 11.6 states…"*,
  never the system asserting a claim about a person as fact.
- **Longevity and death:** never volunteered; behind explicit opt-in; never a date; always framed as
  the classical method's output, with the traditional caveats the texts themselves attach.
- **Health:** classical disease indications are rendered as textual statements, never as diagnosis,
  and never as a reason to act or not act medically.
- **Historically-bound social content:** retained, cited, and marked with a standing editorial note
  distinguishing what a text says from what the system asserts.
- **Non-human birth rules** (BJ ch.3): computed, indexed, excluded from human-chart reports.
- No financial, legal, or medical directives, ever.

None of this is a filter on the corpus. It is the difference between a system that quotes a
6th-century text and a system that speaks in its voice.

---

## 7. Extensibility

The test: **adding a book must not change the reasoning engine.**

### 7.1 The book onboarding contract

Six steps, none of which touches engine code:

1. **Convert** — the frozen Phase 1 pipeline produces `Knowledge/<book-id>.md`. Unchanged.
2. **Chunk profile** — `Corpus/profiles/<book-id>.chunk.json` (§3.2) declares the book's verse-unit
   pattern, commentary markers, tier defaults, and scope-inheritance rules.
3. **Manifest** — `Corpus/books/<book-id>/manifest.json`: title, author, translator, date,
   tradition/school, default provenance tier, known defects.
4. **Scope verification** — human pass over the book's chapters assigning `scope_context` (§3.2).
   Bounded: one pass per chapter.
5. **Rule extraction** — model proposes, human verifies, `Rules/<book-id>/*.yaml`. Any predicate the
   book needs that the vocabulary lacks is added to `Rules/vocabulary.yaml` with a version bump.
6. **Register** — add to `Rules/precedence.yaml`; run `rules_verify` and the regression suite.

### 7.2 Enforcement

Extensibility that is merely intended decays. It is enforced:

- **A test greps the engine source for book identifiers.** Any occurrence of `brihat-jataka`,
  `phaladeepika`, `Mantreswara`, `Varahamihira` etc. outside `Rules/`, `Corpus/` and test fixtures
  **fails the build.** Phase 1 found exactly this class of bug — `build_book.py` hardcoding
  `has_deva()` so chapter detection could never fire on a Latin-script book — and the lesson
  transfers directly.
- **Ablation test.** Remove a book from the store; the suite must still pass, with the coverage
  report shrinking correspondingly and no crash. Run in CI, both books ablated in turn.
- **Additive regression.** Adding a book must not change existing claims except where new cards
  genuinely conflict — and every such change must appear as a `ConflictRecord`, never as a silent
  substitution. This is the direct analogue of Phase 1's rule that Brihat Jataka's output stayed
  byte-identical while Phaladeepika was brought through the pipeline (43/43 regression tests green
  after every change). It worked; keep it.

### 7.3 Extending beyond new books

New *techniques* — Jaimini, Tajika, Nadi — need more than cards: new calculators and new predicates.
The design accommodates this without an engine rewrite:

- **Calculators are plugins** registered against the fact schema. A Jaimini plugin adds
  `chara_karaka`, `arudha_pada`, `rasi_drishti` predicates.
- **The vocabulary is versioned.** Rule cards declare the vocabulary version they need; cards
  requiring an unavailable predicate are inert and reported, not errors.
- **Frames are already parameterised** (`reference`, `varga`, `house_system`), which is what makes a
  parallel system like Jaimini expressible at all.

### 7.4 The gap log — the mechanism that governs the corpus freeze

This is how "do not process another book unless Phase 2 proves specific knowledge is missing"
becomes operational rather than aspirational.

Every run emits a `CoverageReport` (Stage 7e). These accumulate into
**`Reports/CORPUS_GAP_LOG.md`**, generated — never hand-written — from runs over a standing set of
test charts:

| Recorded per gap | |
|---|---|
| Domain / house / technique with zero or tier-2-only coverage | |
| How many test charts hit it | |
| Which book the corpus itself indicates would cover it (§6.4) | |
| Estimated conversion cost for that book | |

**The freeze lifts for a specific book when the gap log shows a specific, recurring, material gap
that book would fill.** Not before, and only for that book.

Predictions I would make now, to be confirmed or refuted by data rather than assumed:

- **BPHS Vol. 1** — will most likely be first, for detailed varga interpretation and dasha variety.
- **Uttara Kalamrita** — karakas and significations, where BJ and PD are thin.
- **Saravali** — female horoscopy and expanded yogas; Brihat Jataka's own introduction points at it.
- **Jataka Parijata** — broad reinforcement; likely lowest marginal value, so likely last.

The point is not the ranking. The point is that the ranking will be produced by measurement.

---

## 8. MVP

The smallest system that meaningfully analyses a birth chart using **only** the Swiss Ephemeris,
Brihat Jataka, and Phaladeepika.

### 8.1 Scope

**In:** Stages 0–10 complete but narrow. Point and Interval birth-time modes. Lahiri ayanamsa,
whole-sign houses, D-1 and D-9 only. Vimshottari to two levels. English output. Reader and audit
views.

**Out:** Chandra-lagna mode; alternative ayanamsas and house systems; vargas beyond D-9; Kalachakra;
Varahamihira's amsa/pinda ayurdaya; transits; rectification; conversational follow-up; any book
beyond the two.

### 8.2 What the MVP can predict — verified against the corpus

Each line below was checked against the actual chapter content in `Knowledge/`, not assumed.

| # | Capability | Sources | Notes |
|---|---|---|---|
| 1 | **Chart and objective facts** — positions, signs, nakshatras + padas, houses, D-9, dignities, retrogradation, combustion | Engine + BJ ch.1, PD ch.1–3 | Foundation for everything else |
| 2 | **Ascendant character** | PD ch.9 (*Effects of different Ascendants*) | Direct, per-lagna |
| 3 | **Planets in houses** | PD ch.8 (318 lines, per planet per house), BJ ch.20 | PD is the substantial source; BJ ch.20 is brief |
| 4 | **Planets in signs; Moon in signs** | BJ ch.18, BJ ch.17 | Moon by sign gets its own chapter |
| 5 | **House-by-house assessment** — lord placement, occupants, aspects, karaka | PD ch.15, ch.16; BJ ch.20 | Stage 5's classical warrant |
| 6 | **Yogas** — Nabhasa, Chandra, Raja, general | BJ ch.11–13, PD ch.6–7 | BJ ch.12 Nabhasa is systematic and unusually well-suited to a condition DSL |
| 7 | **Two-planet conjunctions and aspects** | BJ ch.14, PD ch.18 | All 21 pairs |
| 8 | **Planetary strength** — shadbala with sourced thresholds | PD ch.4 vv.22–23 | Component table on p.50 still flattened; see §8.4 |
| 9 | **Profession and livelihood** | BJ ch.10, PD ch.5 | Requires modernisation framing — BJ's translator says so himself |
| 10 | **Vimshottari dasha timeline + effects** | PD ch.19 (periods + balance), ch.20 (house-lord dasha/antardasha effects) | **Confirmed present.** BJ deliberately does not teach this. |
| 11 | **Ashtakavarga** — BAV, SAV, transit grading | BJ ch.9, PD ch.23–24 | Contribution tables must be readable; see §8.4 |
| 12 | **Marriage / 7th house** | PD ch.10 | Dedicated chapter |
| 13 | **Children / 5th house** | PD ch.12 | Dedicated chapter |
| 14 | **Gulika and upagrahas** | PD ch.25 | Calculation *and* effects both sourced |
| 15 | **Drekkana (D-3) readings** | BJ ch.27 (whole chapter) | Distinctive Varahamihira material |
| 16 | **Longevity** — opt-in only | PD ch.13; BJ ch.7 | §6.6 policy applies. BJ's amsa/pinda deferred past MVP. |
| 17 | **Attributed disagreement** | Both | Must work day one — PD ch.19's internal dasha-balance dispute is already in the corpus |
| 18 | **Coverage map and abstention** | — | Emitted every run; feeds the gap log |

### 8.3 What the MVP explicitly cannot do

Stated so it is never silently faked:

- Ashtottari and most dasha systems beyond Vimshottari and Kalachakra — not in these two books.
- Detailed varga interpretation beyond D-1/D-3/D-9 — thin here; BPHS territory.
- Systematic karaka doctrine — Uttara Kalamrita territory.
- Prashna (horary), muhurta (electional), Jaimini, and synastry — out of scope entirely.
- Rectification.
- Any date-specific event prediction. The MVP gives dasha *periods* and *natal promise*; it does not
  name days.

### 8.4 Corpus work the MVP depends on

Small, bounded, and blocking:

1. **Scope verification** across 56 chapters (§3.2). One pass. Highest-value single task in Phase 2.
2. **Rule extraction** from BJ and PD. The bulk of the effort; ~1,163 verse units in, ~600–900 cards
   out.
3. **Ashtakavarga contribution tables** — confirm they are cleanly readable in PD ch.23 / BJ ch.9.
   If they sit among the flattened-table pages, transcribe those pages first. **Capability 11 is
   blocked until this is confirmed.**
4. **PD printed p.50** Shadbala component table — flattened. Verse thresholds (vv.22–23) are clean,
   so capability 8 works at verse level; the component breakdown does not. Transcribe or scope out.
5. The 17 Brihat Jataka figures and ~10 Phaladeepika tabular pages remain excluded from extraction
   until transcribed (§3.9). They are Phase 1 debt; the gap log will say whether they matter.

### 8.5 Build order

| Step | Deliverable | Gate |
|---|---|---|
| 1 | Resolve the pyswisseph/Python-3.14 question (§2.1) | A chart computes at all |
| 2 | Stages 0–1: `ResolvedBirth` + `ChartBundle`, invariants | Golden charts pass vs `Ephemeris/*.pdf` |
| 3 | Stage 2: predicate vocabulary + `FactSet` | Facts hand-checked against a known chart |
| 4 | Rule card schema + `rules_verify` + condition evaluator | Ten hand-written cards evaluate correctly |
| 5 | Scope verification pass (§8.4.1) | All 56 chapters assigned |
| 6 | Rule extraction, chapter by chapter, PD ch.8 first | Cards verified; quote integrity green |
| 7 | Stages 3–6: yogas, strength, houses, activation | Activations inspectable end to end |
| 8 | Stage 7: adjudication, weighting, convergence, salience | Conflicts surface, incl. PD ch.19's |
| 9 | Stage 9 **before** Stage 8 | The verifier exists before the thing it verifies |
| 10 | Stage 8: synthesis | Zero unsourced sentences on the regression set |
| 11 | Stage 10: three views | Reader view derived from audit view |

Step 9's ordering is deliberate. Building the generator before the verifier means shipping the
generator and deferring the verifier, and then groundedness becomes a thing the system aspires to
rather than a thing it enforces.

### 8.6 Validation

- **Golden charts** — computed sidereal longitudes checked against the printed
  `Ephemeris/ae_*.pdf` tables across the 40-year span, and against an independent implementation.
- **Invariants** — SAV 337, Vimshottari 120y, varga cell counts, house sums. Every run.
- **Quote integrity** — every card, every build.
- **Groundedness regression** — a fixed chart set on which the output must contain zero unsourced
  sentences. Any regression is a build failure.
- **Ablation** — each book removed in turn; no crash, coverage shrinks correctly.
- **Owner review** — a small set of charts read end to end against the books by hand. There is no
  substitute for this, and it is what Phase 1's figure-by-figure verification established as the
  project's standard.

---

## 9. Open decisions for the project owner

Blocking or near-blocking; each changes the work materially.

1. **pyswisseph on Python 3.14, or a 3.12 venv?** (§2.1) Cheap now, expensive later.
2. **Ship `.se1` files or use Moshier?** (§2.1) Affects licensing posture and repo size. Accuracy is
   not the deciding factor — both are far beyond what the rules need.
3. **Confirm Lahiri as default ayanamsa** (§2.2), acknowledging it is an unsourced engineering
   choice the classics do not make.
4. **Rule extraction: how much per session, and what is the review protocol?** (§3.5) This is the
   dominant cost of Phase 2 and deserves the same explicit format approval that the Markdown
   conversion got.
5. **Precedence defaults** (§3.8) — with only two books, is Brihat Jataka or Phaladeepika senior,
   and does that differ by domain? My inclination: no global default at all; force per-domain
   declaration, and let unresolved cases surface as attributed disagreement, which is the more
   honest output anyway.
6. **Confirm the Ashtakavarga contribution tables are readable** (§8.4.3) — blocks capability 11.
7. **Sensitive-content policy** (§6.6) — approve or amend before any output is generated.
8. **MVP output shape** — how long is a report, and which of the 18 capabilities appear in the
   default reader view versus on request?

---

## 10. Summary

The system is a **staged pipeline in which ten of eleven stages are deterministic code, and the one
stage that generates prose is handed a closed set of pre-adjudicated, chart-matched, cited claims
and permitted only to compose them.**

Three decisions carry the design:

1. **The rule store** (§3.5) — a verified, machine-readable layer between prose and engine. Without
   it, either the model invents the rules or the engine hardcodes them; both destroy the project's
   premise. It is what makes explainability and extensibility real rather than intended.
2. **Retrieval before synthesis** (§4.0) — the reversal of the brief's stage order, without which
   the system becomes a citation-laundering machine that is *undetectably* unsourced because every
   sentence has a footnote.
3. **Verification as machinery, not trust** (§6.3) — quote hashes checked against the corpus,
   conditions re-evaluated from scratch, reports refused when they fail. Phase 1 already proved that
   fabricated content reads as genuine and survives review; only an independent check against the
   source artefact catches it.

The corpus pipeline is frozen. §7.4's gap log is the only mechanism that unfreezes it, and only for
a named book against a measured, recurring gap.
