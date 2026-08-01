"""Per-chapter verse-sequence audit.

Walks the assembled Markdown chapter by chapter, extracts every verse terminator
(।। N ।।), and reports gaps and out-of-order numbers. A gap means a terminator Surya
rendered in a form the normaliser did not catch -- the verse text itself is present,
only its number is unread, so gaps localise exactly where to look.
"""
import re, sys, collections

sys.stdout.reconfigure(encoding="utf-8")
MD = sys.argv[1]

md = open(MD, encoding="utf-8").read()
lines = md.splitlines()

CHAP = re.compile(r"^## Chapter (\d+)")
# accept the normalised terminator plus the raw forms Surya emits for ।। N ।।
TERM = re.compile(r"(?:।।|\|\||11|II)\s*(\d+)\s*(?:।।|\|\||11|II)")
# Some verses are printed with the closing danda absent in the source itself (e.g.
# chapter 27 verse 28 on page s108b, confirmed against the page image). That is a
# defect of the book, not of the OCR, so the text is preserved as printed and the
# audit accepts the open form rather than the corpus being silently "repaired".
TERM_OPEN = re.compile(r"(?:।।|\|\||11|II)\s*(\d+)\s*$")

chapters = collections.OrderedDict()
cur = None
for i, ln in enumerate(lines):
    m = CHAP.match(ln)
    if m:
        cur = int(m.group(1))
        chapters[cur] = []
        continue
    if cur is None:
        continue
    # A chapter colophon ends "...।। N ।।" where N is the *chapter* number, not a verse.
    # build_book.py emits colophons as italic lines beginning इति.
    if ln.startswith("*इति") or ln.startswith("इति"):
        continue
    hits = list(TERM.finditer(ln))
    if not hits:
        hits = list(TERM_OPEN.finditer(ln))
    for t in hits:
        chapters[cur].append((int(t.group(1)), i, ln))

total, total_gap = 0, 0
print(f"{'ch':>3} {'n':>4} {'max':>4}  gaps / anomalies")
print("-" * 66)
for ch, vs in chapters.items():
    nums = [n for n, _, _ in vs]
    total += len(nums)
    if not nums:
        print(f"{ch:>3} {0:>4} {'-':>4}  NO VERSE NUMBERS FOUND")
        continue
    hi = max(nums)
    missing = [n for n in range(1, hi + 1) if n not in nums]
    dupes = [n for n, c in collections.Counter(nums).items() if c > 1]
    total_gap += len(missing)
    notes = []
    if missing:
        notes.append(f"missing {missing}")
    if dupes:
        notes.append(f"repeated {sorted(dupes)}")
    if nums != sorted(nums):
        notes.append("OUT OF ORDER")
    print(f"{ch:>3} {len(nums):>4} {hi:>4}  {'; '.join(notes) if notes else 'ok'}")

print("-" * 66)
print(f"verse terminators found : {total}")
print(f"numbers missing in-range: {total_gap}")
print(f"implied verse total     : {total + total_gap}")
