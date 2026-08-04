"""Verify the whole rule store against the corpus.

Runs the engine's own verifier -- so this checks the same thing the consultation
pipeline checks, not a second opinion -- and then adds the store-level checks
the engine has no reason to care about: naming, chapter/file agreement, manifest
coverage, and predicates that are declared but that no chart can ever produce.

A card whose predicate is undeliverable is not an error. It is knowledge
encoded ahead of the fact extractor, which is the intended order: the books
lead, the engine follows. It is reported so the gap stays visible and cannot be
mistaken for a rule that simply never matched.

Usage:  python Rules/tools/verify.py [--book <book_id>]
Exit:   0 = clean, 1 = problems
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Engine.facts import VOCABULARY                     # noqa: E402
from Engine.rules import RuleStoreError, load_cards, verify_cards   # noqa: E402

RULES_DIR = ROOT / "Rules"
CORPUS_DIR = ROOT / "Knowledge"

CARD_ID_RE = re.compile(r"^[A-Z]{2,4}\.\d{2}\.[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*$")


def derivable_predicates() -> set[str]:
    """Predicates the fact extractor can actually emit.

    Read out of Engine/facts.py rather than hardcoded here, so this tool cannot
    drift from the extractor and quietly stop reporting real gaps.
    """
    src = (ROOT / "Engine" / "facts.py").read_text(encoding="utf-8")
    return set(re.findall(r'make_fact\(\s*\n?\s*"([a-z_]+)"', src))


def predicates_in(node) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("all", "any"):
                for child in v:
                    found |= predicates_in(child)
            elif k == "not":
                found |= predicates_in(v)
            else:
                found.add(k)
    elif isinstance(node, list):
        for child in node:
            found |= predicates_in(child)
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=None)
    args = ap.parse_args()

    try:
        cards = load_cards(RULES_DIR)
    except (RuleStoreError, KeyError) as exc:
        print(f"FAIL: rule store will not load: {exc}")
        return 1

    if args.book:
        cards = [c for c in cards if c.book_id == args.book]

    problems = verify_cards(cards, CORPUS_DIR)

    # --- store-level checks -------------------------------------------------
    for card in cards:
        if not CARD_ID_RE.match(card.id):
            problems.append(f"{card.id}: id does not match the store's naming pattern")
        if f".{card.chapter:02d}." not in card.id:
            problems.append(
                f"{card.id}: id does not carry its own chapter number "
                f"({card.chapter:02d})"
            )
        if not card.quote.strip():
            problems.append(f"{card.id}: empty quote")
        if not card.predicts:
            problems.append(f"{card.id}: no claim -- a rule that predicts nothing is not a rule")

    by_book: dict[str, set[int]] = defaultdict(set)
    for card in cards:
        by_book[card.book_id].add(card.chapter)

    for book_id, chapters in sorted(by_book.items()):
        manifest_path = RULES_DIR / book_id / "manifest.json"
        if not manifest_path.exists():
            problems.append(f"{book_id}: no manifest.json")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        declared = set(manifest.get("chapters_extracted", []))
        if declared != chapters:
            problems.append(
                f"{book_id}: manifest declares chapters {sorted(declared)} but the "
                f"store holds {sorted(chapters)}"
            )
        corpus = CORPUS_DIR / f"{book_id}.md"
        if manifest.get("corpus_file") != f"Knowledge/{book_id}.md" or not corpus.exists():
            problems.append(f"{book_id}: manifest corpus_file does not resolve")

    # --- coverage report (not failures) ------------------------------------
    derivable = derivable_predicates()
    used: dict[str, list[str]] = defaultdict(list)
    for card in cards:
        for pred in predicates_in(card.conditions):
            used[pred].append(card.id)

    pending = {p: ids for p, ids in used.items()
               if p in VOCABULARY and p not in derivable}

    print(f"cards loaded ............ {len(cards)}")
    print(f"books ................... {len(by_book)}")
    print(f"chapters ................ {sum(len(c) for c in by_book.values())}")
    for book_id, chapters in sorted(by_book.items()):
        n = sum(1 for c in cards if c.book_id == book_id)
        print(f"  {book_id:16s} {n:4d} cards over chapters {sorted(chapters)}")

    ref = [c for c in cards if c.raw.get("activation") == "reference"]
    if ref:
        print(f"\nreference (doctrine the engine reads, not rules): {len(ref)}")

    inert = [c for c in cards if c.raw.get("activation") == "inert"]
    if inert:
        print(f"\ninert (recorded, never fires): {len(inert)}")
        for c in inert:
            print(f"  {c.id}")

    if pending:
        total = sum(len(v) for v in pending.values())
        print(f"\npredicates declared but not yet derivable by Engine/facts.py "
              f"({total} card(s) affected):")
        for pred, ids in sorted(pending.items()):
            print(f"  {pred:18s} {len(ids):3d} card(s)  e.g. {ids[0]}")

    # --- the deferred-knowledge registry ------------------------------------
    # Encoding a chapter is only half of Phase 3; the other half is saying what
    # was left out and why. An unrecorded deferral is a verification failure,
    # not a note for later.
    sys.path.insert(0, str(ROOT / "Rules" / "tools"))
    from backlog import build as build_backlog                    # noqa: E402

    entries, _, _, resolvable, available, backlog_problems, _ = build_backlog()
    problems.extend(backlog_problems)
    print(f"\nbacklog entries ......... {len(entries)} "
          f"({available and len(available) or 0} available now)")
    if resolvable:
        print(f"  newly unblocked ....... {len(resolvable)}")

    if problems:
        print(f"\nFAIL: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("\nOK: every quote is byte-exact in the corpus, every hash matches, "
          "and every deferred item is recorded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
