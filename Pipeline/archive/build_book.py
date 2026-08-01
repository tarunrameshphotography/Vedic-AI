"""Assemble Surya per-page OCR into a structured Markdown book (Brihat Jataka layout).

Page anatomy learned from the source:
  * chapter opener : [chapter number] / <Devanagari>अध्यायः / <b>English Title</b>
  * normal verso   : <page no> / <book title>
  * normal recto   : <chapter English title> / <page no>
  * colophon       : इति श्री... ।। N ।।   (content - preserved)
"""
import os, re, json, sys, collections, difflib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import clean_line, has_deva, dehyphenate, verse_number

OCRDIR, OUTFILE, TITLE = sys.argv[1], sys.argv[2], sys.argv[3]

HERE = os.path.dirname(os.path.abspath(__file__))
pages = sorted(p[:-5] for p in os.listdir(OCRDIR) if p.endswith(".json"))

# ---- drop publisher front/back matter --------------------------------------------
# Covers, advertisements for other titles and the promotional blurbs are not part of
# the work. page_roles.json records each excluded page and the reason, so the omission
# is documented rather than silent.
ROLES = os.path.join(HERE, "page_roles.json")
excluded = {}
if os.path.exists(ROLES):
    excluded = json.load(open(ROLES, encoding="utf-8")).get("exclude", {})
    kept = [p for p in pages if p not in excluded]
    print(f"front/back matter excluded: {len(pages) - len(kept)} page(s) "
          f"-> {sorted(set(pages) - set(kept))}")
    pages = kept

raw = {p: json.load(open(os.path.join(OCRDIR, p + ".json"), encoding="utf-8")) for p in pages}

# ---- drop hallucinated lines ----------------------------------------------------
# Surya invents fluent text when reading the faint show-through of the reverse of a
# thin page. scan_ink.py identifies those lines from the page image by local contrast;
# indices below are into the *original* per-page JSON, so this must run before any
# other line filtering. Without this the corpus silently gains invented sentences.
INK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ink_report.json")
halluc = 0
if os.path.exists(INK):
    _ink = json.load(open(INK, encoding="utf-8"))
    for p in pages:
        drop = set(_ink.get(p, {}).get("drop", []))
        if drop:
            raw[p] = [l for i, l in enumerate(raw[p]) if i not in drop]
            halluc += len(drop)
    print(f"hallucinated lines removed: {halluc}")
else:
    print("WARNING: ink_report.json missing - hallucinated lines NOT removed")

# ---- apply verified single-character corrections ---------------------------------
# The project rule is that an OCR error is corrected only where the surrounding context
# makes the correction certain. Each entry in corrections.json records the evidence and
# is asserted to fire exactly the expected number of times, so a silent no-op (caused by
# upstream normalisation changing the text) fails loudly instead of passing unnoticed.
CORR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corrections.json")
if os.path.exists(CORR):
    applied = 0
    for c in json.load(open(CORR, encoding="utf-8")):
        hits = 0
        for l in raw.get(c["page"], []):
            if c["find"] in l["text"]:
                hits += l["text"].count(c["find"])
                l["text"] = l["text"].replace(c["find"], c["replace"])
        if hits != c["expect"]:
            raise SystemExit(
                f"corrections.json: {c['page']} expected {c['expect']} hit(s) for "
                f"{c['find']!r}, found {hits}. Refusing to build a corpus with an "
                f"unverified correction.")
        applied += hits
    print(f"verified corrections applied: {applied}")

# ---- splice in vision-verified figures -------------------------------------------
# Surya scrambles the reading order of table cells, and reads the cells of the square
# horoscope charts as loose words which it then interleaves with the surrounding
# commentary. Neither can be recovered from OCR, so each such figure is transcribed by
# eye from the page image into verified/<page>.json, which lists the OCR lines the
# figure occupies (removed here) and the Markdown to put in their place.
VERIFIED = os.path.join(HERE, "verified")
SENTINEL = "\x00VERIFIED\x00"
nfig = 0
if os.path.isdir(VERIFIED):
    for fn in sorted(os.listdir(VERIFIED)):
        if not fn.endswith(".json"):
            continue
        spec = json.load(open(os.path.join(VERIFIED, fn), encoding="utf-8"))
        p = spec["page"]
        if p in excluded:
            continue
        if p not in raw:
            raise SystemExit(f"verified/{fn}: unknown page {p}")
        drop = set(spec.get("exclude_lines", []))
        anchor = spec.get("insert_after", -1)
        if drop and max(drop) >= len(raw[p]):
            raise SystemExit(f"verified/{fn}: exclude_lines out of range for {p} "
                             f"({len(raw[p])} lines)")
        marker = {"text": SENTINEL + spec["markdown"], "bbox": [0, 0, 0, 0]}
        kept = [l for i, l in enumerate(raw[p]) if i not in drop]
        # place the figure after the anchor line, counting in original indices
        at = len([i for i in range(anchor + 1) if i not in drop])
        raw[p] = kept[:at] + [marker] + kept[at:]
        nfig += 1
    print(f"vision-verified figures spliced: {nfig}")

# ---- strip gutter bleed-through -------------------------------------------------
# Facing-page text creeping in at the extreme left/right edge of a scanned spread.
# Body text occupies a consistent column; anything ending before the body begins
# (or starting after it ends) is a scanning artifact, not content.
_all_x0 = sorted(l["bbox"][0] for p in pages for l in raw[p])
_all_x1 = sorted(l["bbox"][2] for p in pages for l in raw[p])
BODY_L = _all_x0[int(len(_all_x0) * 0.30)]
BODY_R = _all_x1[int(len(_all_x1) * 0.70)]
bleed = 0
for p in pages:
    keep = []
    for l in raw[p]:
        if l["text"].startswith(SENTINEL):
            keep.append(l)
            continue
        x0, x1 = l["bbox"][0], l["bbox"][2]
        if x1 < BODY_L - 60 or x0 > BODY_R + 60:
            bleed += 1
            continue
        keep.append(l)
    raw[p] = keep
print(f"body column x=[{BODY_L},{BODY_R}]  gutter-bleed lines removed: {bleed}")

# chapter title: "...ध्यायः" — tolerate Surya's ध→घ / ध→व misreads of the conjunct
CHAP_TITLE = re.compile(r"^(?!इति)[^\s].{1,44}?[ धघव]्याय[ःः:]\s*$")
COLOPHON = re.compile(r"^इति\s")

# ---- empirical running-header set (appears as line 0/1 on >=4 pages) ----------
hc = collections.Counter()
for p in pages:
    for l in raw[p][:2]:
        t = re.sub(r"\s+", " ", clean_line(l["text"])).strip()
        if re.fullmatch(r"[A-Za-z&'.\- ]{3,40}", t):
            hc[t.lower()] += 1
RUNNING = {t for t, c in hc.items() if c >= 4}

stats = dict(pages=0, chapters=[], verses=[], colophons=[], unclear=0,
             dup_lines=[], pagenos=[])

x0s = [l["bbox"][0] for p in pages for l in raw[p]]
MARGIN = collections.Counter(round(x / 15) * 15 for x in x0s).most_common(1)[0][0]
# A printed paragraph indent is a modest step in from the margin. Text that wraps
# beside a figure starts far further right, and must NOT be read as a new paragraph
# per line -- that shattered the commentary on every page carrying a chart.
INDENT, INDENT_MAX = MARGIN + 25, MARGIN + 130

out = [f"# {TITLE}", ""]
cur_chapter = 0
CHAPTER_NO = {}   # page -> chapter number, resolved in the pre-pass below


def head_split(p):
    """Strip running header / page number. Return (chapter_no_or_None, body_lines)."""
    lines = raw[p]
    if not lines:
        return None, []
    txts = [clean_line(l["text"]).strip() for l in lines]
    # chapter opener: a Devanagari chapter title in the first 3 lines, optionally
    # preceded by a bare chapter number (which may carry <math> noise, e.g. "\cdot 12")
    for j in range(min(3, len(txts))):
        if has_deva(txts[j]) and CHAP_TITLE.match(txts[j]):
            chno = None
            for i in range(j):
                m = re.search(r"\b(\d{1,2})\b", txts[i])
                if m:
                    chno = int(m.group(1))
            return (chno if chno is not None else -1), lines[j:]
    start = 0
    for i in range(min(2, len(txts))):
        t = txts[i]
        if re.fullmatch(r"\d{1,3}", t) or re.fullmatch(r"[ivxlc]{2,6}", t.lower()):
            stats["pagenos"].append(t)
            start = max(start, i + 1)
        elif t.lower() in RUNNING:
            start = max(start, i + 1)
    return None, lines[start:]


# ---- resolve chapter numbers ----------------------------------------------------
# The printed chapter numeral sits alone above the Devanagari title, but on 7 of the 28
# openers it is absent or unread, which previously emitted "## Chapter -1". The openers
# are strictly sequential, so number them by position and treat any numeral that *was*
# read as a check on that, not as the source of truth.
_seen = 0
for p in pages:
    _c, _ = head_split(p)
    if _c is not None:
        _seen += 1
        CHAPTER_NO[p] = _seen
        if _c != -1 and _c != _seen:
            print(f"  WARNING: {p} printed chapter numeral {_c} != sequence position {_seen}")
print(f"chapter openers  : {_seen} (numerals read from page: "
      f"{sum(1 for p in pages if head_split(p)[0] not in (None, -1))})")

for p in pages:
    chno, lines = head_split(p)
    if chno is not None:
        chno = CHAPTER_NO[p]
    stats["pages"] += 1
    prose, verse = [], []

    def flush_prose():
        if prose:
            t = re.sub(r"\s+", " ", " ".join(dehyphenate(prose))).strip()
            if t:
                out.extend([t, ""])
            prose.clear()

    def flush_verse():
        if verse:
            out.append("\n".join("> " + v for v in verse))
            out.append("")
            n = verse_number(verse[-1])
            if n is not None:
                stats["verses"].append((p, n))
            verse.clear()

    if chno is not None:
        flush_prose(); flush_verse()
        # English title is the next bold line
        eng = ""
        deva = ""
        for l in lines[:3]:
            t = clean_line(l["text"]).strip()
            if has_deva(t) and CHAP_TITLE.match(t) and not deva:
                deva = t
            elif "<b>" in l["text"] and not eng and not has_deva(t):
                eng = t
        cur_chapter = chno
        stats["chapters"].append((chno, deva, eng, p))
        out.append(f"## Chapter {chno} — {deva}" + (f" · {eng}" if eng else ""))
        out.append("")
        # drop the consumed title lines
        lines = [l for l in lines
                 if clean_line(l["text"]).strip() not in (deva, eng)]

    prev_txt = ""
    for l in lines:
        if l["text"].startswith(SENTINEL):
            flush_verse(); flush_prose()
            out.extend([l["text"][len(SENTINEL):], ""])
            continue
        t = clean_line(l["text"])
        if not t:
            continue
        stats["unclear"] += t.count("[UNCLEAR]")
        # near-duplicate consecutive line (Surya repeat artifact)
        if prev_txt and len(t) > 25:
            if difflib.SequenceMatcher(None, prev_txt, t, autojunk=False).ratio() > 0.85:
                stats["dup_lines"].append((p, t[:60]))
        prev_txt = t

        bold = "<b>" in l["text"]
        indented = INDENT < l["bbox"][0] <= INDENT_MAX

        if has_deva(t):
            flush_prose()
            if COLOPHON.match(t):
                flush_verse()
                stats["colophons"].append((p, t))
                out.extend([f"*{t}*", ""])
            else:
                verse.append(t)
        else:
            flush_verse()
            if bold and len(t) < 70:
                flush_prose()
                out.extend([f"### {t}", ""])
            else:
                if indented and prose:
                    flush_prose()
                prose.append(t)
    flush_verse(); flush_prose()

md = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
open(OUTFILE, "w", encoding="utf-8").write(md)

print(f"pages            : {stats['pages']}")
print(f"chapters detected: {len(stats['chapters'])} -> {[c[0] for c in stats['chapters']]}")
print(f"colophons        : {len(stats['colophons'])}")
print(f"verse markers    : {len(stats['verses'])}")
print(f"[UNCLEAR]        : {stats['unclear']}")
print(f"dup-line flags   : {len(stats['dup_lines'])}")
print(f"running headers  : {sorted(RUNNING)}")
json.dump({k: v for k, v in stats.items()},
          open(OUTFILE + ".stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
