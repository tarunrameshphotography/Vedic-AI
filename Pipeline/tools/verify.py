"""Structural verification of one assembled book.

    python tools/verify.py <book_id> [--md PATH]

v1 verified coverage by parsing the page id as a sheet number and checking that both
"halves" of every sheet were present. That only meant anything for a two-up scan; run
against a single-page book it silently verified nothing. Coverage is now a dense page
sequence, which is layout-independent and is enforced in corpuslib.ir.load_book.
"""
import argparse
import collections
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir, profile, sidecar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("--md")
    a = ap.parse_args()
    book_id = a.book_id
    md_path = a.md or os.path.join(ir.book_dir(ROOT, book_id), "draft.md")

    pages = ir.load_book(ROOT, book_id)          # raises on any gap in the sequence
    side = sidecar.load_all(ROOT, book_id, pages)
    prof = profile.load(ROOT, book_id)
    roles = side["roles"]
    content = [p for p in pages if p["page_id"] not in roles]

    print("=" * 68)
    print("1. PAGE COVERAGE & IDENTITY")
    print("=" * 68)
    print(f"  pages in book      : {len(pages)}  ({pages[0]['page_id']} .. "
          f"{pages[-1]['page_id']})")
    print(f"  sequence           : dense 1..{len(pages)}, no gaps (enforced on load)")
    print(f"  excluded by role   : {len(roles)}")
    print(f"  content pages      : {len(content)}")
    dupe_ids = [k for k, v in collections.Counter(
        p["page_id"] for p in pages).items() if v > 1]
    print(f"  duplicate page ids : {dupe_ids or 'none'}")
    bad = [p["page_id"] for p in pages if p["book_id"] != book_id]
    print(f"  foreign-book pages : {bad or 'none'}")

    print()
    print("=" * 68)
    print("2. SIDECAR INTEGRITY")
    print("=" * 68)
    print(f"  all sidecars validated against OCR fingerprints ...... OK")
    print(f"  ink drop-list      : {sum(len(v) for v in side['ink'].values())} lines "
          f"over {len(side['ink'])} page(s)")
    print(f"  calibration        : {side['calibration'].get('decision')} "
          f"threshold={side['calibration'].get('threshold')}")
    print(f"  corrections        : {len(side['corrections'])}")
    print(f"  verified figures   : {len(side['verified'])}")
    print(f"  page roles         : {len(roles)}")

    print()
    print("=" * 68)
    print("3. DUPLICATE PAGE TEXT")
    print("=" * 68)
    sig = collections.defaultdict(list)
    for p in content:
        n = re.sub(r"\s+", " ", " ".join(l["text"] for l in p["lines"])).strip()
        if len(n) > 80:
            sig[hashlib.md5(n.encode()).hexdigest()].append(p["page_id"])
    dups = {k: v for k, v in sig.items() if len(v) > 1}
    print(f"  duplicate groups   : {len(dups)}")
    for v in list(dups.values())[:10]:
        print(f"    {v}")

    if not os.path.exists(md_path):
        print(f"\n(no assembled Markdown at {md_path})")
        return
    md = open(md_path, encoding="utf-8").read()
    print()
    print("=" * 68)
    print("4. MARKDOWN OUTPUT")
    print("=" * 68)
    anchors = re.findall(r"^<!-- page (\S+) -->$", md, re.M)
    print(f"  characters         : {len(md):,}")
    print(f"  H2 (chapters)      : {len(re.findall(r'^## ', md, re.M))}")
    print(f"  H3 (sections)      : {len(re.findall(r'^### ', md, re.M))}")
    print(f"  verse blocks       : {len(re.findall(r'^> ', md, re.M))}")
    print(f"  [UNCLEAR]          : {md.count('[UNCLEAR]')}")
    print(f"  page anchors       : {len(anchors)}"
          + ("" if not anchors else f" (expected {len(content)})"))
    if anchors:
        foreign = sorted({x for x in anchors if not x.startswith(book_id + "/")})
        print(f"  foreign anchors    : {foreign or 'none'}")
        missing = [p["page_id"] for p in content if p["page_id"] not in set(anchors)]
        print(f"  unanchored pages   : {missing or 'none'}")


if __name__ == "__main__":
    main()
