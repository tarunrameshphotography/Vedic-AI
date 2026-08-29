# VEDIC-AI — working notes for Claude Code

## What this project is

An AI that reads a Vedic birth chart the way a traditional astrologer would:
every predictive sentence traces to a rule printed in a real classical text,
applied to a quantity the engine actually computed. The governing rule,
stated in `MILESTONES.md` and enforced by the rule-card schema and the
verification tools, is:

> **The system may compute, and it may quote — it may not invent.**

## The project's epistemic stance — read this before editing doctrine

This project is not built from a position of "astrology is unproven, treat
it skeptically" or "astrology is true, encode it uncritically." It's built
from a third position, and it's deliberate: **transcribe the classical
tradition faithfully now; test what it actually predicts, rigorously, later.**

The project's author has family lineage in traditional Vedic astrological
practice (multiple generations of hereditary practice, in the Kerala
tradition among others) and has asked that this project not default to
casual skepticism about the tradition's claims. That request is honored not
by suspending judgment about outcomes, but by the discipline already built
into this codebase:

- Every claim the engine makes is cited to an exact quote, chapter and verse
  — never a paraphrase, never an inference the source doesn't state.
- Where classical authorities disagree (a yoga's definition, a dasa-balance
  method, a body's exaltation degree), **both readings are preserved as
  separate cards**, not resolved by the engine picking a winner. See any
  `contradicts`-linked pair in `Rules/`, or `Engine/adjudicate.py`'s own
  docstring: *"There is no authority ranking, no confidence, no precedence
  table, and no mechanism by which the engine can decide that one book is
  more correct than another."*
- `Phases.txt` plans a real validation phase (Phase 6) against hundreds of
  known and celebrity charts, and a research platform (Phase 7) for
  questions like "which yogas have the strongest historical support?" — with
  an honest caveat already on record: *"a model finding patterns in
  retrospective data doesn't by itself establish that planets cause life
  outcomes... you'll need rigorous study design to separate genuine signal
  from coincidence, selection effects, and confirmation bias."*

So: don't add hedging language to rule cards or claims ("astrology suggests,"
"traditionally believed to," disclaimers the source text doesn't carry) —
that would be *editorializing* skepticism into a citation, exactly the kind
of invention the schema forbids in the other direction. Equally, don't
invent numeric confidence, authority weighting, or "which book is right"
adjudication that isn't in the source — that would be inventing certainty.
Quote what the book says, compute what the chart supports, and leave the
question of whether it *works* to the validation phase that's designed to
answer it properly, when its time comes.

## Engineering conventions (read `Engine/doctrine.py`'s module docstring first)

- **No doctrine as Python literals.** A graha name, sign name, house
  classification, or numeric table used as a value in `Engine/*.py` running
  code is a smuggled fact — it should be read from a `reference`-activation
  rule card via a `Doctrine` accessor instead. `Engine/tests/test_doctrine.py`
  enforces this by AST-walking `facts.py`/`doctrine.py` for exactly this.
- **No book name in the engine.** `Engine/*.py` must never mention a book id,
  author, or translator by name (`test_engine_names_no_book`) — adding a
  second book must never require an engine change.
- **Preserve disagreement, don't resolve it.** When a source states two
  competing methods or two authorities disagree, encode both as separate
  cards linked by `contradicts`/`parallel_of`, and let `Engine/adjudicate.py`
  report the relationship rather than picking a side.
- **A card that can't fire yet is `inert`, not omitted.** Every deferred
  passage, unbuilt capability, or blocked card is tracked in
  `Rules/deferred.json` and shows up in `Reports/PHASE3_BACKLOG.md` — nothing
  is silently dropped.
- **Extend additively.** New engine capability (a predicate, a `Claim` field)
  should be additive to existing structures where possible, not a rewrite —
  check `git log` for the most recent milestone's diff as the style
  precedent before adding a new mechanism.

## Workflow

- Card authoring: write minimal card specs (id, verse, quote, conditions,
  predicts) into `Rules/<book>/ch<NN>.json`, then run
  `python Rules/tools/build_chapter.py <book> <chapter>` (dry run) and
  `--write` — it locates the quote in the corpus, computes the span/hash/page
  anchor. Never hand-write a `char_span` or `quote_sha256`.
- Before considering any change done, run in order:
  `python Rules/tools/verify.py`, `python Rules/tools/dupes.py`,
  `python Rules/tools/backlog.py`, `python Rules/tools/leverage.py`, then
  `.venv/Scripts/python.exe -m pytest Engine/tests -q` (the system `python`
  on this machine has no `pytest` installed — use the repo's `.venv`).
- Reports under `Reports/` (`PHASE3_BACKLOG.md`, `PHASE3_PLAN.md`,
  `VERIFICATION_QUEUE.md`) are generated, never hand-edited — regenerate with
  `backlog.py --write`, `leverage.py --write`, `review.py --queue`.
- `MILESTONES.md` is the living source of truth for project state, current
  phase, and the exact resume point for the next session — read its header
  before picking a next task, and update it (plus the reports above) at the
  end of any milestone.
- Do **not** pick the next milestone solely from the top of `leverage.py`'s
  ranking — it measures mechanical ROI, not source clarity or architectural
  risk. `dep.triped-sign-class` ranked #1 for several milestones running
  while being a genuinely unresolved source ambiguity requiring a human
  reading, not an implementation.
