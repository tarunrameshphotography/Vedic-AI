"""Duplicate detection across the rule store.

This tool reports. It never merges and never deletes, because in Phase 3 a
duplicate is usually not a mistake:

  * two authorities saying the same thing is *corroboration* and both cards must
    survive independently -- that agreement is evidence Phase 4 will weigh;
  * two authorities saying opposite things is a real classical disagreement and
    both cards must survive untouched;
  * only the same book saying the same thing twice from the same words is a
    genuine encoding error worth fixing.

So findings are graded by what they most likely mean, and the operator decides.

Three independent detectors:
  1. SAME-QUOTE    identical quote_sha256 -- the same words encoded twice
  2. SAME-LOGIC    identical conditions and identical claim
  3. NEAR-TEXT     high textual similarity within one book (catches an
                   overlapping span or a re-encoded verse under a new id)

Usage:  python Rules/tools/dupes.py [--book <book_id>] [--threshold 0.90]
Exit:   0 always for cross-book findings; 1 if a within-book exact duplicate
        exists, since that one is an encoding defect.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Engine.rules import load_cards                      # noqa: E402

RULES_DIR = ROOT / "Rules"


def canonical(node) -> str:
    """A condition expression as a stable string, order-insensitive in all/any.

    "Mars in the 7th and Venus in the 8th" and "Venus in the 8th and Mars in the
    7th" are the same rule. Sorting the branches makes them compare equal.
    """
    if isinstance(node, dict):
        parts = []
        for k in sorted(node):
            v = node[k]
            if k in ("all", "any"):
                parts.append(f"{k}[" + ",".join(sorted(canonical(c) for c in v)) + "]")
            elif k == "not":
                parts.append(f"not({canonical(v)})")
            elif isinstance(v, dict):
                parts.append(f"{k}(" + ",".join(f"{a}={v[a]}" for a in sorted(v)) + ")")
            else:
                parts.append(f"{k}={v}")
        return "&".join(parts)
    if isinstance(node, list):
        return "[" + ",".join(sorted(canonical(c) for c in node)) + "]"
    return str(node)


def claim_key(predicts: dict) -> str:
    return json.dumps(predicts, sort_keys=True, ensure_ascii=False)


def grade(a, b) -> str:
    return "DEFECT" if a.book_id == b.book_id else "CORROBORATION"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=None)
    ap.add_argument("--threshold", type=float, default=0.90)
    args = ap.parse_args()

    cards = load_cards(RULES_DIR)
    if args.book:
        cards = [c for c in cards if c.book_id == args.book]

    findings: list[tuple[str, str, str]] = []   # (kind, grade, message)
    defects = 0

    # 1. same quote --------------------------------------------------------
    by_hash: dict[str, list] = defaultdict(list)
    for c in cards:
        by_hash[c.quote_sha256].append(c)
    for h, group in sorted(by_hash.items()):
        if len(group) > 1:
            g = "DEFECT" if len({c.book_id for c in group}) == 1 else "SHARED-SOURCE"
            defects += g == "DEFECT"
            findings.append((
                "SAME-QUOTE", g,
                f"{len(group)} cards carry identical text ({h[:12]}): "
                + ", ".join(c.id for c in group)
                + f"\n      {group[0].quote_display[:110]}",
            ))

    # 2. same logic --------------------------------------------------------
    by_logic: dict[tuple[str, str], list] = defaultdict(list)
    for c in cards:
        by_logic[(canonical(c.conditions), claim_key(c.predicts))].append(c)
    for (cond, _), group in sorted(by_logic.items()):
        if len(group) > 1:
            g = grade(group[0], group[1])
            defects += g == "DEFECT"
            findings.append((
                "SAME-LOGIC", g,
                f"{len(group)} cards share condition and claim: "
                + ", ".join(f"{c.id}[{c.book_id}]" for c in group)
                + f"\n      when: {cond}",
            ))

    # 3. near text ---------------------------------------------------------
    # Quadratic, so scoped to one book at a time and skipped for pairs whose
    # lengths already rule out the threshold.
    seen_pairs: set[tuple[str, str]] = set()
    for h, group in by_hash.items():
        for c in group:
            for d in group:
                if c.id != d.id:
                    seen_pairs.add(tuple(sorted((c.id, d.id))))

    per_book: dict[str, list] = defaultdict(list)
    for c in cards:
        per_book[c.book_id].append(c)

    for book_id, group in sorted(per_book.items()):
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                key = tuple(sorted((a.id, b.id)))
                if key in seen_pairs:
                    continue
                la, lb = len(a.quote_display), len(b.quote_display)
                if not la or not lb:
                    continue
                if min(la, lb) / max(la, lb) < args.threshold:
                    continue
                ratio = SequenceMatcher(
                    None, a.quote_display, b.quote_display
                ).ratio()
                if ratio >= args.threshold:
                    findings.append((
                        "NEAR-TEXT", "REVIEW",
                        f"{a.id} and {b.id} are {ratio:.0%} textually similar "
                        f"in {book_id}\n      A: {a.quote_display[:100]}"
                        f"\n      B: {b.quote_display[:100]}",
                    ))

    print(f"scanned {len(cards)} cards")
    if not findings:
        print("no duplicate candidates")
        return 0

    for kind in ("SAME-QUOTE", "SAME-LOGIC", "NEAR-TEXT"):
        rows = [f for f in findings if f[0] == kind]
        if not rows:
            continue
        print(f"\n{kind}  ({len(rows)})")
        for _, g, msg in rows:
            print(f"  [{g}] {msg}")

    print(f"\n{len(findings)} candidate(s); {defects} look like encoding defects")
    return 1 if defects else 0


if __name__ == "__main__":
    sys.exit(main())
