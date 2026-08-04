"""Derive the exact fields of a chapter's rule cards from the corpus.

Phase 3 encodes one chapter at a time. Chapter 8 was produced by a bespoke
proposer because its prose is machine-regular (twelve houses, nine bodies, one
sentence pattern). Almost nothing else in the corpus is: for every other
chapter a human reads the text and authors the cards.

An author writes only what a human can know -- the id, the verse, the quoted
words, the conditions, the claim. This tool fills in everything that must be
exact and must never be typed by hand:

  * proves the quote occurs in that chapter *exactly once*, byte-for-byte
  * records its character span into the corpus file
  * computes the sha256 the verifier re-checks
  * finds the printed page anchor the quote sits on
  * derives quote_display (page anchors removed, whitespace collapsed)

It edits the chapter file in place and is idempotent: it always re-derives from
the `quote` text, never from the span. So it is also the repair tool. If the
corpus is ever rebuilt, run it again and every span is relocated or the card
fails loudly.

Usage:  python Rules/tools/build_chapter.py <book_id> <chapter> [--write]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PAGE_ANCHOR_RE = re.compile(r"<!--\s*page\s+(\S+)\s*-->")

DEFAULT_SCOPE = {"frame": "lagna", "varga": "D1"}

# Keys a card may carry beyond the core schema, in the order they are written.
OPTIONAL_KEYS = ("kind", "activation", "note", "exclusions", "requires",
                 "extends", "contradicts", "parallel_of")


class SpecError(RuntimeError):
    """The authored card does not agree with the corpus. Never guessed around."""


def corpus_path(book_id: str) -> Path:
    return ROOT / "Knowledge" / f"{book_id}.md"


def load_corpus(book_id: str) -> str:
    # Bytes then decode: the corpus keeps CRLF newlines and every span in the
    # rule store is an offset into exactly this string. Path.read_text would
    # translate newlines on some platforms and shift every offset.
    return corpus_path(book_id).read_bytes().decode("utf-8")


def chapter_bounds(text: str, chapter: int) -> tuple[int, int]:
    """Span of one chapter: its heading to the next chapter heading (or EOF).

    Bounding the search by chapter is not just an optimisation. Classical texts
    repeat sentences almost verbatim across chapters, and a quote that is unique
    inside its own chapter is often not unique inside the book. The chapter is
    the unit of authority, so it is the unit of search.
    """
    head = re.search(rf"^## Chapter {chapter} — ", text, re.MULTILINE)
    if not head:
        raise SpecError(f"chapter {chapter} heading not found in corpus")
    nxt = re.search(r"^## Chapter \d+ — ", text[head.end():], re.MULTILINE)
    return head.start(), (head.end() + nxt.start()) if nxt else len(text)


def page_anchor_at(text: str, pos: int) -> str | None:
    """The printed page a position sits on: nearest anchor at or before it."""
    last = None
    for m in PAGE_ANCHOR_RE.finditer(text, 0, pos):
        last = m.group(1)
    return last


def locate(text: str, quote: str, lo: int, hi: int, card_id: str) -> tuple[int, int, str]:
    """Find `quote` in text[lo:hi]. It must occur exactly once.

    A card may be authored with plain "\\n" newlines; the corpus is CRLF. If the
    literal text does not occur, one CRLF variant is tried, and whichever
    variant actually matched is what gets stored. Nothing else is attempted: if
    the words differ from the book, that is an authoring error, not a
    formatting one, and it must surface.
    """
    for candidate in (quote, quote.replace("\r\n", "\n").replace("\n", "\r\n")):
        hits: list[int] = []
        start = lo
        while True:
            i = text.find(candidate, start, hi)
            if i < 0:
                break
            hits.append(i)
            start = i + 1
        if len(hits) == 1:
            return hits[0], hits[0] + len(candidate), candidate
        if len(hits) > 1:
            raise SpecError(
                f"{card_id}: quote occurs {len(hits)} times in the chapter at "
                f"{hits}; extend it until it is unique"
            )
    raise SpecError(
        f"{card_id}: quote not found in chapter {lo}..{hi}. First 90 chars:\n"
        f"    {quote[:90]!r}"
    )


def display_of(quote: str) -> str:
    return " ".join(PAGE_ANCHOR_RE.sub("", quote).split())


def rebuild(book_id: str, chapter: int) -> tuple[dict, list[str]]:
    path = ROOT / "Rules" / book_id / f"ch{chapter:02d}.json"
    if not path.exists():
        raise SpecError(f"no chapter file at {path.relative_to(ROOT)}")
    doc = json.loads(path.read_text(encoding="utf-8"))

    if doc.get("book_id") != book_id or doc.get("chapter") != chapter:
        raise SpecError(f"{path.name}: book_id/chapter disagree with the request")

    text = load_corpus(book_id)
    lo, hi = chapter_bounds(text, chapter)

    out: list[dict] = []
    notes: list[str] = []
    seen: set[str] = set()

    for entry in doc["cards"]:
        cid = entry["id"]
        if cid in seen:
            raise SpecError(f"duplicate id {cid} within {path.name}")
        seen.add(cid)

        src = entry.get("source", {})
        # The authored quote may live at the top level (fresh card) or inside
        # source (already built). The words are the input either way.
        quote = entry.get("quote", src.get("quote"))
        if quote is None:
            raise SpecError(f"{cid}: no quote")
        verse = entry.get("verse", src.get("verse"))
        if verse is None:
            raise SpecError(f"{cid}: no verse reference")

        start, end, matched = locate(text, quote, lo, hi, cid)
        if text[start:end] != matched:          # belt and braces
            raise SpecError(f"{cid}: internal span error")

        card = {
            "id": cid,
            "schema": 1,
            "source": {
                "book_id": book_id,
                "chapter": chapter,
                "verse": verse,
                "page_anchor": page_anchor_at(text, start),
                "tier": entry.get("tier", src.get("tier", 1)),
                "quote": matched,
                "quote_display": display_of(matched),
                "quote_sha256": hashlib.sha256(matched.encode("utf-8")).hexdigest(),
                "char_span": [start, end],
                "span_trimmed": entry.get("span_trimmed", src.get("span_trimmed")),
            },
            "scope": entry.get("scope", dict(DEFAULT_SCOPE)),
            "conditions": entry["conditions"],
            "predicts": entry["predicts"],
            "timing": entry.get("timing", "natal"),
            "weight": float(entry.get("weight", 1.0)),
            "specificity": int(entry.get("specificity", 1)),
            "extraction": entry.get("extraction", {
                "method": "authored",
                "proposer": "Rules/tools/build_chapter.py",
                "verified_by": None,
                "verified_date": None,
            }),
        }
        for k in OPTIONAL_KEYS:
            if k in entry:
                card[k] = entry[k]
        out.append(card)

        if card.get("activation") == "inert":
            notes.append(
                f"{cid}: recorded but never fires -- {card.get('note', 'no reason given')}"
            )

    doc["cards"] = out
    return doc, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("chapter", type=int)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    try:
        doc, notes = rebuild(args.book_id, args.chapter)
    except SpecError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"{args.book_id} ch{args.chapter:02d}: {len(doc['cards'])} card(s) located")
    for n in notes:
        print(f"  note: {n}")

    if args.write:
        out = ROOT / "Rules" / args.book_id / f"ch{args.chapter:02d}.json"
        out.write_text(
            json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"wrote {out.relative_to(ROOT)}")
    else:
        print("(dry run; pass --write to update the chapter file)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
