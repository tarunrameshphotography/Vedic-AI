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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .facts import VOCABULARY, FactSet

COMBINATORS = ("all", "any", "not")


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
    conditions: dict
    predicts: dict
    timing: str
    weight: float
    specificity: int
    raw: dict


@dataclass(frozen=True)
class Evaluation:
    satisfied: bool
    bindings: tuple[str, ...]     # the fact keys that made it true
    missing: tuple[str, ...]      # predicates absent from the vocabulary


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
            cards.append(RuleCard(
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

        start, end = card.char_span
        if not (0 <= start < end <= len(text)):
            problems.append(f"{card.id}: char_span {card.char_span} out of range")
            continue
        actual = text[start:end]
        if actual != card.quote:
            problems.append(
                f"{card.id}: quote does not match corpus at {card.char_span}\n"
                f"    stored: {card.quote[:80]!r}\n"
                f"    corpus: {actual[:80]!r}"
            )
            continue
        digest = hashlib.sha256(actual.encode("utf-8")).hexdigest()
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

def evaluate(conditions: dict, facts: FactSet) -> Evaluation:
    """Evaluate a condition expression, returning the facts that satisfied it.

    The bindings are the point. A trace that says "matched" is worthless; a
    trace that says "matched on in_house(Sun,10)" can be checked.
    """
    bindings: list[str] = []
    missing: list[str] = []
    ok = _eval(conditions, facts, bindings, missing)
    # An unknown predicate can never count as satisfied.
    if missing:
        ok = False
    return Evaluation(ok, tuple(bindings), tuple(sorted(set(missing))))


def _eval(node: Any, facts: FactSet, bindings: list[str], missing: list[str]) -> bool:
    if not isinstance(node, dict) or len(node) != 1:
        raise RuleStoreError(f"malformed condition node: {node!r}")
    (op, val), = node.items()

    if op == "all":
        return all(_eval(c, facts, bindings, missing) for c in val)
    if op == "any":
        # Evaluate every branch so that bindings from satisfied branches are
        # recorded, rather than short-circuiting and losing the evidence.
        results = [_eval(c, facts, bindings, missing) for c in val]
        return any(results)
    if op == "not":
        inner: list[str] = []
        return not _eval(val, facts, inner, missing)

    if op not in VOCABULARY:
        missing.append(op)
        return False

    ordered = VOCABULARY[op]
    if set(val) != set(ordered):
        raise RuleStoreError(f"{op} expects arguments {ordered}, got {sorted(val)}")
    key = f"{op}(" + ",".join(str(val[a]) for a in ordered) + ")"
    if key in facts:
        bindings.append(key)
        return True
    return False


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
                    keys.add(f"{k}(" + ",".join(str(v[a]) for a in ordered) + ")")
    return keys
