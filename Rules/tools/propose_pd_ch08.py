"""Propose rule cards from Phaladeepika chapter 8 (planets in the twelve houses).

This is a *proposer*, not an authority. It follows the Phase 1 precedent set by
`propose_charts.py`: the machine does the mechanical part exactly, a human
checks the result, and anything the machine cannot determine with certainty is
reported rather than guessed.

What it does deterministically:
  * locates chapter 8 and its per-body sections
  * splits each section into sentences and attaches each to the house it names
  * records a byte-exact quote and its character span in Knowledge/phaladeepika.md

What it refuses to do:
  * paraphrase (the quote is a verbatim substring, asserted before writing)
  * infer a house that no sentence names
  * assign a house positionally -- paragraphs here are not 1:1 with houses

Character spans are offsets into the UTF-8-decoded file with its CRLF newlines
left intact. The verifier decodes identically.

Usage:  python Rules/tools/propose_pd_ch08.py [--write]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "Knowledge" / "phaladeepika.md"
OUT = ROOT / "Rules" / "phaladeepika" / "ch08.json"

BOOK_ID = "phaladeepika"
CHAPTER = 8

# Section heading -> body name, plus the verse range printed at the section head.
SECTIONS = [
    ("Chapter 8 —", "Sun", "1-4"),
    ("### The MOON", "Moon", "5-7"),
    ("### MARS", "Mars", "8-10"),
    ("### MERCURY", "Mercury", "11-13"),
    ("14-16.", "Jupiter", "14-16"),
    ("### VENUS", "Venus", "17-19"),
    ("### SATURN", "Saturn", "20-24"),
    ("### RAHU", "Rahu", "25-27"),
    ("### KETU", "Ketu", "28-33"),
]

ORDINALS = {
    "1st": 1, "first": 1, "lagna": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5,
    "6th": 6, "sixth": 6, "7th": 7, "8th": 8, "9th": 9, "10th": 10,
    "11th": 11, "12th": 12,
}

# "the 5th house", "the 7th at birth", "the 12th makes", "in Lagna".
# Two guards matter here:
#   * an ordinal followed by "degree(s)" is a measurement, not a house
#     (verses 34-35 talk about longitudes), so it is excluded;
#   * bare "Lagna" means the 1st house, but "from the Lagna" is a reference
#     frame and "Lagna point/Rashi/Bhava" is a coordinate -- neither is a
#     house placement, and treating them as one silently resets the group.
HOUSE_RE = re.compile(
    r"\b(?:the\s+)?(1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|first|sixth)\b"
    r"(?!\s+degree)"
    r"(?=\s+(?:house|at\s+birth|bhava|makes|gives|enables|will|produces)|\s*,)"
    r"|(?<!from\s)(?<!from\sthe\s)\b(Lagna)\b(?!\s+(?:point|Rashi|Bhava))",
    re.IGNORECASE,
)

PAGE_ANCHOR_RE = re.compile(r"<!--\s*page\s+(\S+)\s*-->")
SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def load() -> str:
    return CORPUS.read_bytes().decode("utf-8")


def chapter_bounds(text: str) -> tuple[int, int]:
    """Span of chapter 8's planet-in-house material.

    Stops at verse 34, not at chapter 9. Verses 34-35 state a *modifier* -- how
    fully a placement's effect is realised, by the planet's degree relative to
    the lagna point -- and their worked example names houses that belong to no
    body's section. Including them makes the last body's section absorb rules
    that are not about it. That modifier is real doctrine and is captured
    separately; it is simply not a planet-in-house card.
    """
    start = text.index("## Chapter 8 — Effects of planets in different houses")
    end = text.index("\r\n34. The effects produced by a planet", start)
    return start, end


def page_anchor_at(text: str, pos: int) -> str | None:
    """Nearest page anchor at or before pos -- the printed page a quote sits on."""
    last = None
    for m in PAGE_ANCHOR_RE.finditer(text, 0, pos):
        last = m.group(1)
    return last


def section_spans(text: str, lo: int, hi: int) -> list[tuple[str, str, int, int]]:
    marks: list[tuple[str, str, int]] = []
    for needle, body, verses in SECTIONS:
        i = text.index(needle, lo, hi)
        marks.append((body, verses, i))
    marks.sort(key=lambda m: m[2])
    out = []
    for n, (body, verses, i) in enumerate(marks):
        end = marks[n + 1][2] if n + 1 < len(marks) else hi
        out.append((body, verses, i, end))
    return out


def sentences(text: str, lo: int, hi: int):
    """Yield (sentence, abs_start, abs_end) for prose lines only.

    Skips headings, page anchors, tables, fenced blocks and tier-2 Notes --
    Notes are the translator's, not Mantreswara's, and are handled separately.
    """
    in_fence = False
    for m in re.finditer(r"[^\r\n]+", text[lo:hi]):
        line, base = m.group(0), lo + m.start()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            continue
        if line.startswith(("#", "|", ">", "**", "<!--")):
            continue
        if re.match(r"^\s*Notes?\s*[—:-]", line):
            continue
        # Strip a leading printed verse number ("1-4. If the Sun ...").
        vm = re.match(r"^\d{1,3}(?:-\d{1,3})?\.\s+", line)
        off = vm.end() if vm else 0
        body = line[off:]
        cur = base + off
        for s in SENTENCE_END_RE.split(body):
            s = s.strip()
            if not s:
                continue
            i = text.index(s, cur, hi)
            yield s, i, i + len(s)
            cur = i + len(s)


def houses_in(sentence: str) -> list[int]:
    found = []
    for m in HOUSE_RE.finditer(sentence):
        tok = (m.group(1) or m.group(2)).lower()
        h = ORDINALS.get(tok)
        if h and h not in found:
            found.append(h)
    return found


# Manual span trims, each with the evidence for it, in the spirit of Phase 1's
# corrections.json: the corpus is never edited, the span is simply tightened,
# and the tightened text is still a byte-exact substring of the corpus.
# Every entry is asserted to fire exactly once.
TRIMS = {
    ("Mercury", 12): {
        "strip_suffix": " JUPITER",
        "why": "The section heading 'JUPITER' is run onto the end of Mercury's "
               "12th-house paragraph in Knowledge/phaladeepika.md (printed p.96, "
               "line 'He will also suffer from humiliation JUPITER'). It is a "
               "heading, not part of Mercury's rule. The corpus is left as "
               "printed; only this card's span is tightened.",
    },
}
_TRIMS_FIRED: set = set()


def apply_trim(body: str, house: int, text: str, start: int, end: int):
    spec = TRIMS.get((body, house))
    if not spec:
        return start, end, None
    suffix = spec["strip_suffix"]
    if not text[start:end].endswith(suffix):
        raise AssertionError(
            f"trim for {body} house {house} is stale: span does not end with {suffix!r}"
        )
    _TRIMS_FIRED.add((body, house))
    return start, end - len(suffix), spec["why"]


def build() -> tuple[list[dict], list[str]]:
    text = load()
    lo, hi = chapter_bounds(text)
    cards: list[dict] = []
    warnings: list[str] = []

    for body, verses, s_lo, s_hi in section_spans(text, lo, hi):
        # Build *contiguous runs*. A run ends when the house changes or when
        # anything other than whitespace and page anchors intervenes. Taking
        # first-start to last-end instead would let a stray later mention of a
        # house swallow every paragraph in between -- which is exactly what a
        # transcribed chart caption ("Lagna is in Aquarius...") did to Saturn.
        runs: list[tuple[int, int, int]] = []   # (house, start, end)
        current: int | None = None
        prev_end: int | None = None

        for sent, a, b in sentences(text, s_lo, s_hi):
            hs = houses_in(sent)
            if len(hs) > 1:
                warnings.append(
                    f"{body}: sentence names houses {hs} -- attached to {hs[0]}, review: "
                    f"{sent[:70]}..."
                )
            if hs:
                current = hs[0]
            if current is None:
                continue

            gap_clean = prev_end is not None and not PAGE_ANCHOR_RE.sub(
                "", text[prev_end:a]
            ).strip()
            if runs and runs[-1][0] == current and gap_clean:
                runs[-1] = (current, runs[-1][1], b)
            else:
                runs.append((current, a, b))
            prev_end = b

        by_house: dict[int, list[tuple[int, int]]] = {}
        for house, a, b in runs:
            by_house.setdefault(house, []).append((a, b))

        for house in range(1, 13):
            spans = by_house.get(house)
            if not spans:
                warnings.append(f"{body}: no sentence found for house {house} -- NO CARD")
                continue
            if len(spans) > 1:
                extra = [text[a:b][:60] for a, b in spans[1:]]
                warnings.append(
                    f"{body} house {house}: {len(spans)} separate runs; using the first. "
                    f"Ignored: {extra}"
                )
            start, end = spans[0]
            start, end, trim_note = apply_trim(body, house, text, start, end)
            quote = text[start:end]
            cards.append({
                "id": f"PD.08.{body}.{house:02d}",
                "schema": 1,
                "source": {
                    "book_id": BOOK_ID,
                    "chapter": CHAPTER,
                    "verse": verses,
                    "page_anchor": page_anchor_at(text, start),
                    "tier": 1,
                    # `quote` is byte-exact at char_span and is what the
                    # verifier checks. `quote_display` is the same text with
                    # Phase 1 page anchors removed -- those are pipeline
                    # metadata, not words Mantreswara wrote.
                    "quote": quote,
                    "quote_display": " ".join(PAGE_ANCHOR_RE.sub("", quote).split()),
                    "quote_sha256": hashlib.sha256(quote.encode("utf-8")).hexdigest(),
                    "char_span": [start, end],
                    "span_trimmed": trim_note,
                },
                "scope": {"frame": "lagna", "varga": "D1"},
                "conditions": {"all": [{"in_house": {"graha": body, "house": house}}]},
                "predicts": {"domain": "general", "subject": body, "house": house},
                "timing": "natal",
                "weight": 1.0,
                "specificity": 1,
                "extraction": {
                    "method": "assisted",
                    "proposer": "Rules/tools/propose_pd_ch08.py",
                    "verified_by": None,
                    "verified_date": None,
                },
            })
    return cards, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    cards, warnings = build()
    unfired = set(TRIMS) - _TRIMS_FIRED
    if unfired:
        print(f"ERROR: trims declared but never applied: {sorted(unfired)}")
        return 1
    by_body: dict[str, int] = {}
    for c in cards:
        by_body[c["predicts"]["subject"]] = by_body.get(c["predicts"]["subject"], 0) + 1

    print(f"proposed {len(cards)} cards")
    for b, n in by_body.items():
        flag = "" if n == 12 else f"   <-- expected 12"
        print(f"  {b:8s} {n:2d}{flag}")
    if warnings:
        print(f"\n{len(warnings)} item(s) need human review:")
        for w in warnings:
            print("  -", w)

    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(
            json.dumps({"book_id": BOOK_ID, "chapter": CHAPTER, "cards": cards},
                       ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
