"""The deferred-knowledge registry: validate it, resolve it, publish it.

Nothing may be silently deferred. That is a strong claim, and it is only worth
making if a machine enforces it, so as much of the backlog as possible is
*derived* rather than written down:

  * **Deferred cards** are read out of the rule store. A card marked inert is
    an entry by construction -- it cannot be forgotten, and its dependencies
    are the ones it actually declares.
  * **Deferred passages** are found by coverage. Every paragraph of an encoded
    chapter that no card's char_span touches is deferred text, and this tool
    finds it whether or not anyone remembered to record it. Each one must be
    claimed by an entry in `Rules/deferred.json` or verification fails.
  * **Deferred chapters** are found by difference: every chapter heading in the
    corpus that the book's manifest does not declare extracted.

Only the *reasons* are hand-authored, because a reason is a judgement. The
existence of every deferred item is computed.

Resolution is computed too. A dependency of kind `predicate` is implemented
when Engine/facts.py actually emits that predicate; the rest carry an explicit
`implemented` flag. An entry whose blocking dependencies are all implemented is
reported as resolvable, together with how much executable knowledge it unlocks
-- which is the number this phase is trying to move.

Usage:  python Rules/tools/backlog.py [--write] [--json]
Exit:   0 = the registry accounts for everything, 1 = something is undocumented
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
sys.path.insert(0, str(ROOT / "Rules" / "tools"))

from Engine.rules import load_cards                                  # noqa: E402
from build_chapter import chapter_bounds, load_corpus                # noqa: E402

RULES_DIR = ROOT / "Rules"
REGISTRY = RULES_DIR / "deferred.json"
REPORT = ROOT / "Reports" / "PHASE3_BACKLOG.md"

# A paragraph shorter than this, or made only of layout, is not deferred
# knowledge and does not need an entry. Kept deliberately small: it is better
# to have to write off a colophon explicitly than to let a rule slip through.
TRIVIAL = 40
LAYOUT = re.compile(r"^(?:<!--|\||```|\+[-+]+\+|#{1,6}\s)")

REQUIRED_ENTRY_KEYS = ("id", "kind", "book", "chapter", "locus", "what",
                       "reason", "requires", "phase", "status")


class BacklogError(RuntimeError):
    pass


# --- what the engine can actually do today ----------------------------------

def derivable_predicates() -> set[str]:
    """Predicates the fact extractor emits. Read from the source, not listed."""
    src = (ROOT / "Engine" / "facts.py").read_text(encoding="utf-8")
    return set(re.findall(r'make_fact\(\s*\n?\s*"([a-z_]+)"', src))


def dependency_state(registry: dict) -> dict[str, bool]:
    """dep id -> implemented?  Computed where it can be, declared where not."""
    derivable = derivable_predicates()
    state = {}
    for dep_id, dep in registry["dependencies"].items():
        if dep_id == "dep.none":
            state[dep_id] = True
        elif dep.get("predicate"):
            state[dep_id] = dep["predicate"] in derivable
        else:
            state[dep_id] = bool(dep.get("implemented", False))
    return state


# --- derived entries ---------------------------------------------------------

def paragraphs(text: str, lo: int, hi: int) -> list[tuple[int, int, str]]:
    """(start, end, text) for each paragraph of a chapter, absolute offsets."""
    out, pos = [], lo
    for m in re.finditer(r"(?:\r\n){2,}", text[lo:hi]):
        s, e = lo + m.start(), lo + m.end()
        if text[pos:s].strip():
            out.append((pos, s, text[pos:s]))
        pos = e
    if text[pos:hi].strip():
        out.append((pos, hi, text[pos:hi]))
    return out


def deferred_cards(cards, registry: dict) -> list[dict]:
    """Every inert card, as a backlog entry. Derived; never authored."""
    deps = registry["dependencies"]
    entries = []
    for c in sorted(cards, key=lambda c: c.id):
        if c.activation != "inert":
            continue
        # A card's phase is its slowest blocker's: it becomes executable when
        # the last thing it waits on exists, not the first.
        phases = sorted({deps[d]["phase"] for d in c.raw.get("requires", [])
                         if d in deps})
        entries.append({
            "phase": " + ".join(phases) if phases else "unknown",
            "id": f"card:{c.id}",
            "kind": "card",
            "book": c.book_id,
            "chapter": c.chapter,
            "locus": f"v. {c.verse}",
            "what": c.raw.get("predicts", {}).get("effect")
                    or c.quote_display[:70],
            "reason": c.raw.get("note", ""),
            "requires": list(c.raw.get("requires", [])),
            "status": "deferred",
            "card_id": c.id,
        })
    return entries


def deferred_passages(cards, book_id: str, chapters: list[int]) -> list[dict]:
    """Paragraphs of an encoded chapter that no card quotes."""
    text = load_corpus(book_id)
    spans = [c.char_span for c in cards if c.book_id == book_id]
    found = []
    for ch in sorted(chapters):
        lo, hi = chapter_bounds(text, ch)
        for i, (s, e, body) in enumerate(paragraphs(text, lo, hi)):
            if any(cs < e and s < ce for cs, ce in spans):
                continue
            stripped = body.strip()
            if len(stripped) < TRIVIAL or LAYOUT.match(stripped):
                continue
            found.append({
                "book": book_id, "chapter": ch, "paragraph": i,
                "excerpt": " ".join(stripped.split())[:70],
            })
    return found


def unencoded_chapters(book_id: str, extracted: list[int]) -> list[int]:
    text = load_corpus(book_id)
    all_ch = [int(m.group(1))
              for m in re.finditer(r"^## Chapter (\d+) — ", text, re.MULTILINE)]
    return [c for c in all_ch if c not in set(extracted)]


# --- validation --------------------------------------------------------------

def validate(registry, cards, authored, problems: list[str]) -> None:
    deps = registry["dependencies"]
    seen_ids: set[str] = set()

    for e in authored:
        missing = [k for k in REQUIRED_ENTRY_KEYS if k not in e]
        if missing:
            problems.append(f"{e.get('id', '<no id>')}: missing field(s) {missing}")
            continue
        if e["id"] in seen_ids:
            problems.append(f"{e['id']}: duplicate entry -- each item gets exactly one")
        seen_ids.add(e["id"])
        if not e["reason"].strip():
            problems.append(f"{e['id']}: empty reason")
        if not e["requires"]:
            problems.append(f"{e['id']}: no dependency; use dep.none if it is "
                            f"deferred only by ordering")
        for dep in e["requires"]:
            if dep not in deps:
                problems.append(f"{e['id']}: unknown dependency {dep!r}")
        if e["status"] not in ("deferred", "resolved"):
            problems.append(f"{e['id']}: status must be deferred or resolved")

    # Inert cards must declare dependencies the catalogue knows.
    for c in cards:
        if c.activation != "inert":
            continue
        req = c.raw.get("requires", [])
        if not req:
            problems.append(f"{c.id}: inert but declares no dependency")
        for dep in req:
            if dep not in deps:
                problems.append(f"{c.id}: unknown dependency {dep!r}")


def claim_index(authored) -> set[tuple[str, int, int]]:
    """(book, chapter, paragraph) triples an authored entry accounts for."""
    claimed = set()
    for e in authored:
        for p in e.get("paragraphs", []):
            claimed.add((e["book"], e["chapter"], p))
    return claimed


# --- report ------------------------------------------------------------------

def render(registry, entries, state, resolvable, available, counts) -> str:
    deps = registry["dependencies"]
    L: list[str] = []
    A = L.append
    A("# Phase 3 — deferred-knowledge backlog")
    A("")
    A("Generated by `Rules/tools/backlog.py`. **Do not edit by hand** — the "
      "reasons live in `Rules/deferred.json`, and everything else is derived "
      "from the rule store and the corpus on every run.")
    A("")
    A("Nothing may be silently deferred. Inert cards are read out of the store, "
      "deferred passages are found by checking which paragraphs of an encoded "
      "chapter no card quotes, and unencoded chapters are found by difference "
      "against each book's manifest. An item that is not accounted for here "
      "fails verification.")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| Backlog entries | **{len(entries)}** |")
    for k in ("card", "passage", "chapter", "concept"):
        n = sum(1 for e in entries if e["kind"] == k and e["status"] == "deferred")
        if n:
            A(f"| — of kind `{k}` | {n} |")
    A(f"| Resolved | {sum(1 for e in entries if e['status'] == 'resolved')} |")
    A(f"| Cards in store | {counts['cards']} |")
    A(f"| Firing | {counts['firing']} |")
    A(f"| Inert | {counts['inert']} |")
    A("")

    A("## Dependencies")
    A("")
    A("What the deferred knowledge is waiting for. A `predicate` dependency is "
      "marked implemented when `Engine/facts.py` actually emits it — the flag "
      "cannot be set by hand and cannot drift.")
    A("")
    A("| Dependency | Kind | Implemented | Entries blocked | Cards blocked | Phase |")
    A("|---|---|---|---|---|---|")
    blocked = defaultdict(list)
    for e in entries:
        if e["status"] == "deferred":
            for d in e["requires"]:
                blocked[d].append(e)
    for dep_id in sorted(deps, key=lambda d: (-len(blocked[d]), d)):
        rows = blocked[dep_id]
        if not rows and dep_id == "dep.none":
            continue
        cards_n = sum(1 for e in rows if e["kind"] == "card")
        A(f"| `{dep_id}` — {deps[dep_id]['title']} | {deps[dep_id]['kind']} | "
          f"{'yes' if state[dep_id] else 'no'} | {len(rows)} | {cards_n} | "
          f"{deps[dep_id]['phase']} |")
    A("")

    if resolvable:
        A("## Newly unblocked")
        A("")
        A("Every blocking dependency of these entries is now implemented. Each "
          "card here becomes executable knowledge the moment its `activation` "
          "is lifted.")
        A("")
        for e in resolvable:
            A(f"- `{e['id']}` — {e['what']}")
        A("")

    if available:
        A("## Available now")
        A("")
        A(f"{len(available)} entr(y/ies) are deferred by ordering alone — "
          f"nothing blocks them. This is the Phase 3 work queue.")
        A("")

    A("## Entries")
    A("")
    for kind, title in (("chapter", "Chapters not yet encoded"),
                        ("passage", "Passages inside encoded chapters"),
                        ("concept", "Cross-cutting"),
                        ("card", "Rule cards recorded but not firing")):
        rows = [e for e in entries if e["kind"] == kind]
        if not rows:
            continue
        A(f"### {title} ({len(rows)})")
        A("")
        A("| Entry | Book | Chapter | Locus | Deferred | Reason | Blocked on | Phase | Status |")
        A("|---|---|---|---|---|---|---|---|---|")
        for e in sorted(rows, key=lambda e: (e["book"], e["chapter"], e["id"])):
            reason = " ".join(str(e["reason"]).split())
            if len(reason) > 160:
                reason = reason[:157] + "…"
            req = ", ".join(f"`{d}`" for d in e["requires"])
            A(f"| `{e['id']}` | {e['book']} | {e['chapter']} | {e['locus']} | "
              f"{e['what']} | {reason} | {req} | {e['phase']} | {e['status']} |")
        A("")
    return "\n".join(L)


# --- main --------------------------------------------------------------------

def build() -> tuple[list[dict], dict, dict, list[dict], list[str]]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cards = load_cards(RULES_DIR)
    authored = registry["entries"]
    problems: list[str] = []

    validate(registry, cards, authored, problems)

    entries = list(authored) + deferred_cards(cards, registry)

    # Unencoded chapters must each be accounted for.
    claimed_chapters = {(e["book"], e["chapter"])
                        for e in authored if e["kind"] == "chapter"}
    for manifest_path in sorted(RULES_DIR.glob("*/manifest.json")):
        m = json.loads(manifest_path.read_text(encoding="utf-8"))
        book = m["book_id"]
        extracted = m.get("chapters_extracted", [])
        for ch in unencoded_chapters(book, extracted):
            if (book, ch) not in claimed_chapters:
                problems.append(
                    f"{book} ch. {ch} is not encoded and has no backlog entry")
        # Deferred passages inside the chapters that *are* encoded.
        claimed = claim_index(authored)
        for p in deferred_passages(cards, book, extracted):
            if (p["book"], p["chapter"], p["paragraph"]) not in claimed:
                problems.append(
                    f"{p['book']} ch. {p['chapter']} para {p['paragraph']} is "
                    f"quoted by no card and claimed by no backlog entry: "
                    f"\"{p['excerpt']}\"")

    state = dependency_state(registry)

    # "Resolvable" must mean a capability landed, not that nothing was ever
    # blocking. An entry whose only dependency is dep.none was always available
    # -- counting it here would drown the signal this report exists to give.
    resolvable = [e for e in entries
                  if e["status"] == "deferred"
                  and any(d != "dep.none" for d in e["requires"])
                  and all(state.get(d, False) for d in e["requires"])]
    available = [e for e in entries
                 if e["status"] == "deferred"
                 and e["requires"] == ["dep.none"]]

    counts = {
        "cards": len(cards),
        "firing": sum(1 for c in cards if c.activation != "inert"),
        "inert": sum(1 for c in cards if c.activation == "inert"),
    }
    return entries, registry, state, resolvable, available, problems, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                    help="refresh Reports/PHASE3_BACKLOG.md")
    ap.add_argument("--json", action="store_true", help="dump entries as JSON")
    args = ap.parse_args()

    try:
        entries, registry, state, resolvable, available, problems, counts = build()
    except (BacklogError, KeyError, OSError) as exc:
        print(f"FAIL: backlog will not build: {exc}")
        return 1

    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return 0

    print(f"backlog entries ......... {len(entries)}")
    for k in ("chapter", "passage", "concept", "card"):
        n = sum(1 for e in entries if e["kind"] == k)
        if n:
            print(f"  {k:10s} {n:4d}")
    print(f"cards ................... {counts['cards']} "
          f"({counts['firing']} firing, {counts['inert']} inert)")

    unmet = [d for d, ok in state.items() if not ok and d != "dep.none"]
    print(f"dependencies ............ {len(state)} "
          f"({len(state) - len(unmet)} implemented, {len(unmet)} outstanding)")

    print(f"available now ........... {len(available)} "
          f"(deferred by ordering; nothing blocks them)")

    if resolvable:
        cards_freed = sum(1 for e in resolvable if e["kind"] == "card")
        print(f"\nNEWLY UNBLOCKED: {len(resolvable)} entr(y/ies), "
              f"{cards_freed} card(s) can become executable")
        for e in resolvable:
            print(f"  {e['id']} - {e['what']}")

    if args.write:
        REPORT.write_text(
            render(registry, entries, state, resolvable, available, counts) + "\n",
            encoding="utf-8")
        print(f"\nwrote {REPORT.relative_to(ROOT)}")

    if problems:
        print(f"\nFAIL: {len(problems)} item(s) deferred without an entry")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("\nOK: every deferred item is accounted for.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
