"""The rule store: loading, quote verification, and condition evaluation.

This module contains no astrology and names no book. It loads rule cards from a
directory, proves each card's quote is still byte-exact in the corpus, and
evaluates conditions against a FactSet.

Rules are data. The engine's doctrine is whatever the cards say and nothing
else, which is what lets a new book be added without touching this file.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .facts import VOCABULARY, FactSet

COMBINATORS = ("all", "any", "not")

# A condition argument of this shape is a variable, not a literal.
VARIABLE_RE = re.compile(r"^\?[a-z][a-z0-9_]*$")


class RuleStoreError(RuntimeError):
    """A card is malformed, stale, or references something that does not exist."""


@dataclass(frozen=True)
class RuleCard:
    id: str
    book_id: str
    chapter: int
    verse: str
    page_anchor: str | None
    tier: int
    quote: str
    quote_display: str
    quote_sha256: str
    char_span: tuple[int, int]
    span_trimmed: str | None
    scope: dict
    activation: str          # "active" | "inert"
    conditions: dict
    predicts: dict
    timing: str
    weight: float
    specificity: int
    raw: dict
    # A rule is not always printed contiguously. Where a governing sentence
    # states the effect for several dispositions listed beneath it, the card
    # must quote both places or quote a bare condition as though it were a
    # prediction. `spans` and `quote_parts` are parallel: part i is required to
    # be byte-exact at span i. A single-span card has one of each, so every
    # existing card keeps working unchanged.
    spans: tuple[tuple[int, int], ...] = ()
    quote_parts: tuple[str, ...] = ()


@dataclass(frozen=True)
class Solution:
    """One way of satisfying a condition.

    `assignment` names what each variable stood for. A rule written about "a
    planet" has as many solutions as there are grahas that satisfy it, and each
    becomes its own claim -- so the report says which planet, not "some".
    """

    assignment: tuple[tuple[str, str], ...]   # (?g, "Jupiter"), sorted
    bindings: tuple[str, ...]                 # the fact keys that made it true

    def as_dict(self) -> dict:
        return dict(self.assignment)


@dataclass(frozen=True)
class Evaluation:
    satisfied: bool
    bindings: tuple[str, ...]     # the fact keys that made it true
    missing: tuple[str, ...]      # predicates absent from the vocabulary
    solutions: tuple[Solution, ...] = ()


# --- loading ----------------------------------------------------------------

def load_cards(rules_dir: str | Path) -> list[RuleCard]:
    """Load every card under `rules_dir`. Order is deterministic."""
    rules_dir = Path(rules_dir)
    cards: list[RuleCard] = []
    seen: set[str] = set()

    for path in sorted(rules_dir.rglob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for c in doc.get("cards", []):
            s = c["source"]
            if c["id"] in seen:
                raise RuleStoreError(f"duplicate card id {c['id']} in {path}")
            seen.add(c["id"])
            # Normalise both shapes to the multi-span one at the door, so
            # nothing downstream has to ask which kind of card it is holding.
            spans = tuple(tuple(x) for x in s.get("spans", [s["char_span"]]))
            parts = tuple(s.get("quote_parts", [s["quote"]]))
            if len(spans) != len(parts):
                raise RuleStoreError(
                    f"{c['id']}: {len(spans)} span(s) but {len(parts)} quote part(s)"
                )
            cards.append(RuleCard(
                spans=spans,
                quote_parts=parts,
                id=c["id"],
                book_id=s["book_id"],
                chapter=s["chapter"],
                verse=s["verse"],
                page_anchor=s.get("page_anchor"),
                tier=s.get("tier", 1),
                quote=s["quote"],
                quote_display=s.get("quote_display", s["quote"]),
                quote_sha256=s["quote_sha256"],
                char_span=tuple(s["char_span"]),
                span_trimmed=s.get("span_trimmed"),
                scope=c.get("scope", {}),
                activation=c.get("activation", "active"),
                conditions=c["conditions"],
                predicts=c.get("predicts", {}),
                timing=c.get("timing", "natal"),
                weight=float(c.get("weight", 1.0)),
                specificity=int(c.get("specificity", 1)),
                raw=c,
            ))
    return cards


# --- verification -----------------------------------------------------------

def verify_cards(cards: list[RuleCard], corpus_dir: str | Path) -> list[str]:
    """Prove every card still says what it claims the book says.

    Three independent checks per card: the span resolves, the text at that span
    is byte-identical to the stored quote, and the hash matches. If a book is
    ever re-converted, stale cards fail here rather than silently citing text
    that no longer exists.

    Returns a list of problems; empty means everything verified.
    """
    corpus_dir = Path(corpus_dir)
    problems: list[str] = []
    corpora: dict[str, str] = {}

    for card in cards:
        if card.book_id not in corpora:
            path = corpus_dir / f"{card.book_id}.md"
            if not path.exists():
                problems.append(f"{card.id}: corpus file not found: {path}")
                corpora[card.book_id] = ""
                continue
            corpora[card.book_id] = path.read_bytes().decode("utf-8")
        text = corpora[card.book_id]
        if not text:
            continue

        # Every span must resolve and every part must be byte-exact at its own
        # span. A card that quotes two places is only as trustworthy as its
        # weakest span.
        bad = False
        for i, ((start, end), part) in enumerate(zip(card.spans, card.quote_parts)):
            if not (0 <= start < end <= len(text)):
                problems.append(
                    f"{card.id}: span {i} {(start, end)} out of range")
                bad = True
                break
            actual = text[start:end]
            if actual != part:
                problems.append(
                    f"{card.id}: quote part {i} does not match corpus at "
                    f"{(start, end)}\n"
                    f"    stored: {part[:80]!r}\n"
                    f"    corpus: {actual[:80]!r}"
                )
                bad = True
                break
        if bad:
            continue
        digest = hashlib.sha256(card.quote.encode("utf-8")).hexdigest()
        if digest != card.quote_sha256:
            problems.append(f"{card.id}: sha256 mismatch")

        # sorted: _predicates_used returns a set, and problem messages must
        # come out in the same order on every run.
        for pred in sorted(_predicates_used(card.conditions)):
            if pred not in VOCABULARY:
                problems.append(
                    f"{card.id}: condition uses predicate {pred!r} "
                    f"which is not in the vocabulary"
                )
    return problems


def _predicates_used(node: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k in COMBINATORS:
                if k == "not":
                    found |= _predicates_used(v)
                else:
                    for child in v:
                        found |= _predicates_used(child)
            else:
                found.add(k)
    elif isinstance(node, list):
        for child in node:
            found |= _predicates_used(child)
    return found


# --- evaluation -------------------------------------------------------------

def is_variable(value: Any) -> bool:
    """A condition argument written as `?g` stands for whatever satisfies it.

    Variables exist because the classics quantify: "a planet in his sign of
    exaltation", "the lord of the 7th occupies the 5th". Neither can be written
    with literals, and instantiating them per graha would make each card's own
    words deny its own condition.

    This is quantification, not an expression language. A variable ranges over
    the values the FactSet already contains, so its domain comes from the chart
    rather than from any table in Python.
    """
    return isinstance(value, str) and VARIABLE_RE.match(value) is not None


def evaluate(conditions: dict, facts: FactSet) -> Evaluation:
    """Evaluate a condition expression, returning every way it is satisfied.

    The bindings are the point. A trace that says "matched" is worthless; a
    trace that says "matched on lord_of_house(Moon,7) and in_house(Moon,5)"
    can be checked.
    """
    missing: list[str] = []
    solutions = _solve(conditions, facts, missing)
    # An unknown predicate can never count as satisfied.
    if missing:
        return Evaluation(False, (), tuple(sorted(set(missing))), ())
    first = solutions[0].bindings if solutions else ()
    return Evaluation(bool(solutions), first, (), tuple(solutions))


def _consistent(a: dict, b: dict) -> bool:
    return all(a[k] == b[k] for k in set(a) & set(b))


def _merge(sols_a: list[Solution], sols_b: list[Solution]) -> list[Solution]:
    """Join two solution sets, keeping only compatible variable assignments."""
    out: list[Solution] = []
    for x in sols_a:
        ax = x.as_dict()
        for y in sols_b:
            ay = y.as_dict()
            if not _consistent(ax, ay):
                continue
            merged = {**ax, **ay}
            seen, binds = set(), []
            for k in x.bindings + y.bindings:
                if k not in seen:
                    seen.add(k)
                    binds.append(k)
            out.append(Solution(tuple(sorted(merged.items())), tuple(binds)))
    return out


def _dedupe(sols: list[Solution]) -> list[Solution]:
    seen, out = set(), []
    for s in sols:
        key = (s.assignment, s.bindings)
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out


def _solve(node: Any, facts: FactSet, missing: list[str],
           env: dict[str, str] | None = None) -> list[Solution]:
    """Every way `node` is satisfied, given the variables already bound.

    `env` is what makes negation mean what the classics mean by it. "Benefics
    in the 7th will produce good effects *unless* they happen to be lords of
    the 6th, 8th or 12th" excludes the graha that satisfied the first clause,
    not some unrelated graha elsewhere in the chart. Evaluating the `not` in
    ignorance of the current binding asks "is anything the lord of the 8th?",
    which is true of every chart ever cast, so the rule could never fire.

    So a conjunction binds left to right and each child is solved under the
    assignment its predecessors produced. For positive leaves this is the same
    join as before. For a negated one it is the difference between a correlated
    and an uncorrelated reading, and only the correlated one is the rule.
    """
    if not isinstance(node, dict) or len(node) != 1:
        raise RuleStoreError(f"malformed condition node: {node!r}")
    (op, val), = node.items()
    env = env or {}

    if op == "all":
        sols = [Solution((), ())]
        for i, child in enumerate(val):
            nxt: list[Solution] = []
            for s in sols:
                inner_env = {**env, **s.as_dict()}
                for t in _solve(child, facts, missing, inner_env):
                    at, asg = t.as_dict(), s.as_dict()
                    if not _consistent(asg, at):
                        continue
                    seen, binds = set(), []
                    for k in s.bindings + t.bindings:
                        if k not in seen:
                            seen.add(k)
                            binds.append(k)
                    nxt.append(Solution(
                        tuple(sorted({**asg, **at}.items())), tuple(binds)))
            sols = _dedupe(nxt)
            if not sols:
                # Keep walking so that unknown predicates in later branches are
                # still reported rather than hidden by an early failure.
                for rest in val[i + 1:]:
                    _solve(rest, facts, missing, env)
                return []
        return _dedupe(sols)

    if op == "any":
        out: list[Solution] = []
        for child in val:
            out.extend(_solve(child, facts, missing, env))
        return _dedupe(out)

    if op == "not":
        # Negation as failure over the fact set, and only over it. A variable
        # already bound outside is substituted first, so the negation is about
        # that graha; one that is not stays local, which is what lets "if there
        # is no planet in the Ascendant" ask whether any binding exists at all.
        inner = _solve(val, facts, missing, env)
        return [] if inner else [Solution((), ())]

    if op not in VOCABULARY:
        missing.append(op)
        return []

    ordered = VOCABULARY[op]
    if set(val) != set(ordered):
        raise RuleStoreError(f"{op} expects arguments {ordered}, got {sorted(val)}")

    # A variable the environment has already bound is a literal here. Nothing
    # is invented: the value can only have come from a fact matched earlier.
    eff = {a: (env.get(val[a], val[a]) if is_variable(val[a]) else val[a])
           for a in ordered}

    if not any(is_variable(eff[a]) for a in ordered):
        key = f"{op}(" + ",".join(str(eff[a]) for a in ordered) + ")"
        return [Solution((), (key,))] if key in facts else []

    # Enumerate the facts of this predicate that match every literal argument,
    # binding the variables to whatever the chart actually produced.
    out = []
    for f in facts.by_predicate(op):
        assignment = {}
        ok = True
        for a in ordered:
            want = eff[a]
            got = f.args.get(a)
            if is_variable(want):
                assignment[want] = got
            elif str(want) != str(got):
                ok = False
                break
        if ok:
            out.append(Solution(
                tuple(sorted((k, str(v)) for k, v in assignment.items())),
                (f.key,)))
    return _dedupe(out)


def build_predicate_index(cards: list[RuleCard]) -> dict[str, list[str]]:
    """Fact key -> card ids that mention it.

    Candidate generation only. A card surfacing here still has its full
    condition expression evaluated before it can justify anything.
    """
    index: dict[str, list[str]] = {}
    for card in cards:
        for key in _leaf_keys(card.conditions):
            index.setdefault(key, []).append(card.id)
    return index


def _leaf_keys(node: Any) -> set[str]:
    """Index keys for a condition.

    A leaf with no variables indexes on its exact fact key. A leaf that
    quantifies cannot -- it has no single key -- so it indexes on its predicate
    under a wildcard, and any chart producing that predicate makes the card a
    candidate. Candidate generation only; the full condition is still evaluated.
    """
    keys: set[str] = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "not":
                continue          # a negated leaf is not a lookup key
            if k in ("all", "any"):
                for child in v:
                    keys |= _leaf_keys(child)
            elif k in VOCABULARY:
                ordered = VOCABULARY[k]
                if set(v) == set(ordered):
                    if any(is_variable(v[a]) for a in ordered):
                        keys.add(f"{k}:*")
                    else:
                        keys.add(f"{k}(" + ",".join(str(v[a]) for a in ordered) + ")")
    return keys
