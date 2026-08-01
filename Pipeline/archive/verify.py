"""Verification pass over an assembled book: pages, chapters, verses, duplicates."""
import os, re, sys, json, hashlib, collections
sys.stdout.reconfigure(encoding="utf-8")

OCRDIR = sys.argv[1]
MD = sys.argv[2]

pages = sorted(p[:-4] for p in os.listdir(OCRDIR) if p.endswith(".txt"))
texts = {p: open(os.path.join(OCRDIR, p + ".txt"), encoding="utf-8").read() for p in pages}

print("=" * 66)
print("1. PAGE COVERAGE")
print("=" * 66)
spreads = sorted({int(p[1:4]) for p in pages})
gaps = [s for s in range(spreads[0], spreads[-1] + 1) if s not in spreads]
missing_half = [f"s{s:03d}{h}" for s in spreads for h in "ab" if f"s{s:03d}{h}" not in pages]
print(f"  half-pages OCR'd : {len(pages)}")
print(f"  spreads covered  : {spreads[0]}–{spreads[-1]} ({len(spreads)})")
print(f"  spread gaps      : {gaps or 'none'}")
print(f"  missing halves   : {missing_half or 'none'}")
empty = [p for p, t in texts.items() if len(t.strip()) < 20]
print(f"  near-empty pages : {empty or 'none'}")

print()
print("=" * 66)
print("2. DUPLICATE PAGES")
print("=" * 66)
sig = collections.defaultdict(list)
for p, t in texts.items():
    n = re.sub(r"\s+", " ", t).strip()
    if len(n) > 80:
        sig[hashlib.md5(n.encode()).hexdigest()].append(p)
dups = {k: v for k, v in sig.items() if len(v) > 1}
print(f"  duplicate groups : {len(dups)}")
for v in list(dups.values())[:10]:
    print(f"    {v}")

print()
print("=" * 66)
print("3. CHAPTER MARKERS  (इति ... अध्यायः colophons)")
print("=" * 66)
colophon = re.compile(r"इति\s+श्री.*?(\d+)\s*।।")
found = []
for p in pages:
    for m in re.finditer(r"इति[^\n]*", texts[p]):
        nums = re.findall(r"\d+", m.group(0))
        found.append((p, nums[-1] if nums else "?", m.group(0)[:70]))
print(f"  colophons found  : {len(found)}")
for f in found[:35]:
    print(f"    {f[0]}  ch {f[1]:>3}   {f[2]}")

print()
print("=" * 66)
print("4. VERSE NUMBERING")
print("=" * 66)
vn = re.compile(r"।।\s*(\d+)\s*।।")
seq = []
for p in pages:
    for m in vn.finditer(texts[p]):
        seq.append((p, int(m.group(1))))
print(f"  verse markers    : {len(seq)}")
# find resets (chapter boundaries) and non-monotonic jumps within a run
breaks, prev = [], None
for p, n in seq:
    if prev is not None and n != prev + 1 and n != 1:
        breaks.append((p, prev, n))
    prev = n
print(f"  numbering breaks : {len(breaks)}")
for b in breaks[:30]:
    print(f"    {b[0]}: {b[1]} -> {b[2]}")

if os.path.exists(MD):
    md = open(MD, encoding="utf-8").read()
    print()
    print("=" * 66)
    print("5. MARKDOWN OUTPUT")
    print("=" * 66)
    print(f"  characters       : {len(md):,}")
    print(f"  H2 (chapters)    : {len(re.findall(r'^## ', md, re.M))}")
    print(f"  H3 (sections)    : {len(re.findall(r'^### ', md, re.M))}")
    print(f"  verse blocks     : {len(re.findall(r'^> ', md, re.M))}")
    print(f"  [UNCLEAR]        : {md.count('[UNCLEAR]')}")
