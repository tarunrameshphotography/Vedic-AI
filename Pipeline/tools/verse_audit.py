"""Per-chapter verse-sequence audit.

    python tools/verse_audit.py <book_id> [--md PATH]

Walks the assembled Markdown chapter by chapter and checks that verse terminators run
1..N with no gaps, duplicates or reordering. Structural only -- it says nothing about
whether the Devanagari glyphs are correct.
"""
import argparse
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHAP = re.compile(r"^## Chapter (\d+)")
ANCHOR = re.compile(r"^<!-- page \S+ -->$")
TERM = re.compile(r"(?:।।|\|\||11|II)\s*(\d+)\s*(?:।।|\|\||11|II)")
# Some verses are printed with the closing danda absent in the source itself (e.g.
# Brihat Jataka ch27 v28, confirmed against the page image). That is a defect of the
# book, not of the OCR, so the text is preserved as printed and the audit accepts the
# open form rather than the corpus being silently "repaired".
TERM_OPEN = re.compile(r"(?:।।|\|\||11|II)\s*(\d+)\s*$")


def audit(md):
    chapters, cur = collections.OrderedDict(), None
    for i, ln in enumerate(md.splitlines()):
        m = CHAP.match(ln)
        if m:
            cur = int(m.group(1))
            chapters[cur] = []
            continue
        if cur is None or ANCHOR.match(ln):
            continue
        # a colophon ends "...।। N ।।" where N is the CHAPTER number, not a verse
        if ln.startswith("*इति") or ln.startswith("इति"):
            continue
        hits = list(TERM.finditer(ln)) or list(TERM_OPEN.finditer(ln))
        for t in hits:
            chapters[cur].append(int(t.group(1)))
    return chapters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("--md")
    a = ap.parse_args()
    path = a.md or os.path.join(ROOT, "books", a.book_id, "draft.md")
    chapters = audit(open(path, encoding="utf-8").read())

    total = gaps = 0
    bad = []
    print(f"{'ch':>3} {'n':>4} {'max':>4}  gaps / anomalies")
    print("-" * 66)
    for ch, nums in chapters.items():
        total += len(nums)
        if not nums:
            print(f"{ch:>3} {0:>4} {'-':>4}  NO VERSE NUMBERS FOUND")
            bad.append(ch)
            continue
        hi = max(nums)
        missing = [n for n in range(1, hi + 1) if n not in nums]
        dupes = [n for n, c in collections.Counter(nums).items() if c > 1]
        gaps += len(missing)
        notes = []
        if missing:
            notes.append(f"missing {missing}")
        if dupes:
            notes.append(f"repeated {sorted(dupes)}")
        if nums != sorted(nums):
            notes.append("OUT OF ORDER")
        if notes:
            bad.append(ch)
        print(f"{ch:>3} {len(nums):>4} {hi:>4}  {'; '.join(notes) if notes else 'ok'}")
    print("-" * 66)
    print(f"chapters                : {len(chapters)}")
    print(f"verse terminators found : {total}")
    print(f"numbers missing in-range: {gaps}")
    print(f"chapters with anomalies : {bad or 'none'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
