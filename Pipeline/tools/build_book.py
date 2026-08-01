"""Assemble one book's IR pages into Markdown.

Generic engine. Everything book-specific comes from profiles/<book_id>.json; everything
page-specific comes from fingerprint-bound sidecars. Nothing here knows what book it is
processing, and nothing can reach a page belonging to a different book.

    python tools/build_book.py <book_id> [--out PATH] [--no-anchors]

Page anchors (`<!-- page <book>/pNNNN -->`) are emitted by default so that any line of
the corpus can be traced back to the printed page it came from. `--no-anchors` produces
the corpus without them, which is what the migration used to prove byte-identical output
against the pre-migration draft.
"""
import argparse
import collections
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir, profile, sidecar
from corpuslib.normalize import clean_line, dehyphenate, has_deva, verse_number

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENTINEL = "\x00VERIFIED\x00"
DANDA_ANY = re.compile(r"।|॥|\|\||11|II")


def build(book_id, outfile, anchors=True):
    prof = profile.load(ROOT, book_id)
    all_pages = ir.load_book(ROOT, book_id)
    side = sidecar.load_all(ROOT, book_id, all_pages)

    # ---- roles: drop publisher front/back matter ---------------------------------
    roles = side["roles"]
    pages = [p for p in all_pages if p["page_id"] not in roles]
    print(f"pages in book      : {len(all_pages)}")
    print(f"excluded by role   : {len(roles)}")

    raw = {p["page_id"]: [dict(l) for l in p["lines"]] for p in pages}
    order = [p["page_id"] for p in pages]

    # ---- hallucinated lines ------------------------------------------------------
    halluc = 0
    for pid in order:
        drop = set(side["ink"].get(pid, []))
        if drop:
            raw[pid] = [l for i, l in enumerate(raw[pid]) if i not in drop]
            halluc += len(drop)
    print(f"hallucinated lines : {halluc} removed")

    # ---- verified corrections ----------------------------------------------------
    applied = 0
    for c in side["corrections"]:
        if c["page_id"] in roles:
            continue
        hits = 0
        for l in raw.get(c["page_id"], []):
            if c["find"] in l["text"]:
                hits += l["text"].count(c["find"])
                l["text"] = l["text"].replace(c["find"], c["replace"])
        if hits != c["expect"]:
            raise SystemExit(
                f"corrections: {c['page_id']} expected {c['expect']} hit(s) for "
                f"{c['find']!r}, found {hits}. Refusing to build a corpus with an "
                f"unverified correction.")
        applied += hits
    print(f"corrections applied: {applied}")

    # ---- vision-verified figures -------------------------------------------------
    nfig = 0
    for pid, spec in side["verified"].items():
        if pid in roles:
            continue
        drop = set(spec.get("exclude_lines", []))
        anchor = spec.get("insert_after", -1)
        marker = {"text": SENTINEL + spec["markdown"], "bbox": [0, 0, 0, 0]}
        kept = [l for i, l in enumerate(raw[pid]) if i not in drop]
        at = len([i for i in range(anchor + 1) if i not in drop])
        raw[pid] = kept[:at] + [marker] + kept[at:]
        nfig += 1
    print(f"figures spliced    : {nfig}")

    # ---- gutter bleed-through ----------------------------------------------------
    _x0 = sorted(l["bbox"][0] for p in order for l in raw[p])
    _x1 = sorted(l["bbox"][2] for p in order for l in raw[p])
    body_l = _x0[int(len(_x0) * 0.30)]
    body_r = _x1[int(len(_x1) * 0.70)]
    gm = prof["gutter_margin"]
    bleed = 0
    for pid in order:
        keep = []
        for l in raw[pid]:
            if l["text"].startswith(SENTINEL):
                keep.append(l)
                continue
            if l["bbox"][2] < body_l - gm or l["bbox"][0] > body_r + gm:
                bleed += 1
                continue
            keep.append(l)
        raw[pid] = keep
    print(f"gutter bleed       : {bleed} removed (body x=[{body_l},{body_r}])")

    # ---- running headers ---------------------------------------------------------
    hc = collections.Counter()
    for pid in order:
        for l in raw[pid][:2]:
            t = re.sub(r"\s+", " ", clean_line(l["text"])).strip()
            if re.fullmatch(r"[A-Za-z&'.\- ]{3,40}", t):
                hc[t.lower()] += 1
    running = {t for t, c in hc.items() if c >= prof["running_header_min_pages"]}

    x0s = [l["bbox"][0] for p in order for l in raw[p]]
    margin = collections.Counter(round(x / 15) * 15 for x in x0s).most_common(1)[0][0]
    indent_lo = margin + prof["indent_min_offset"]
    indent_hi = margin + prof["indent_max_offset"]

    chap_title = prof.chapter_title
    colophon = prof.colophon
    pagenum = re.compile(r"\d{1,%d}" % prof["page_number_max_digits"])

    stats = dict(book_id=book_id, pages=0, chapters=[], verses=[], colophons=[],
                 unclear=0, dup_lines=[], excluded=roles)

    # In a Devanagari book the chapter title is set in Devanagari and the number sits
    # alone above it. In a Latin-script book the printed line carries both ("Chapter 12:
    # Birth of children"). The engine must not assume the first case -- that assumption
    # was the reason chapter detection silently found nothing on the first Latin book.
    script_deva = prof["script"] == "devanagari"

    def is_chapter_opener(t):
        return bool(chap_title.match(t)) and (has_deva(t) if script_deva else True)

    pn_pos = prof["page_number_position"]

    def _is_furniture(t):
        return bool(pagenum.fullmatch(t)
                    or re.fullmatch(r"[ivxlc]{2,6}", t.lower())
                    or t.lower() in running)

    def trim_tail(lines):
        """Strip a page number / running footer printed at the foot of the page."""
        if pn_pos not in ("bottom", "both"):
            return lines
        end = len(lines)
        for i in range(len(lines) - 1, max(-1, len(lines) - 3), -1):
            t = clean_line(lines[i]["text"]).strip()
            if _is_furniture(t):
                end = i
            else:
                break
        return lines[:end]

    def head_split(pid):
        lines = raw[pid]
        if not lines:
            return None, []
        txts = [clean_line(l["text"]).strip() for l in lines]
        for j in range(min(3, len(txts))):
            if is_chapter_opener(txts[j]):
                chno = None
                if script_deva:
                    for i in range(j):
                        m = re.search(r"\b(\d{1,2})\b", txts[i])
                        if m:
                            chno = int(m.group(1))
                else:
                    m = re.search(r"\b(\d{1,3})\b", txts[j])
                    if m:
                        chno = int(m.group(1))
                return (chno if chno is not None else -1), trim_tail(lines[j:])
        start = 0
        if pn_pos in ("top", "both"):
            for i in range(min(2, len(txts))):
                if _is_furniture(txts[i]):
                    start = max(start, i + 1)
        return None, trim_tail(lines[start:])

    # ---- chapter numbers from sequence, printed numeral used as a check ----------
    chapter_no, seen, read_numerals = {}, 0, 0
    for pid in order:
        c, _ = head_split(pid)
        if c is not None:
            seen += 1
            chapter_no[pid] = seen
            if c != -1:
                read_numerals += 1
                if c != seen:
                    print(f"  WARNING: {pid} printed numeral {c} != position {seen}")
    print(f"chapter openers    : {seen} ({read_numerals} numerals read from page)")

    out = [f"# {prof.title}", ""]
    marks = []                      # (index into out, page_id)
    require_danda = prof["verse_requires_danda"]

    for pid in order:
        chno, lines = head_split(pid)
        if chno is not None:
            chno = chapter_no[pid]
        stats["pages"] += 1
        marks.append((len(out), pid))
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
                    stats["verses"].append((pid, n))
                verse.clear()

        if chno is not None:
            flush_prose(); flush_verse()
            eng = deva = ""
            if script_deva:
                for l in lines[:3]:
                    t = clean_line(l["text"]).strip()
                    if has_deva(t) and chap_title.match(t) and not deva:
                        deva = t
                    elif "<b>" in l["text"] and not eng and not has_deva(t):
                        eng = t
                stats["chapters"].append((chno, deva, eng, pid))
                out.append(f"## Chapter {chno} — {deva}" + (f" · {eng}" if eng else ""))
                consumed = {deva, eng}
            else:
                # The opener line carries only "Chapter N"; the title is on the bold
                # line(s) that follow it, and may run to two lines.
                opener = clean_line(lines[0]["text"]).strip()
                parts = []
                for l in lines[1:4]:
                    t = clean_line(l["text"]).strip()
                    if t and "<b>" in l["text"] and not is_chapter_opener(t):
                        parts.append(t)
                    else:
                        break
                title = " ".join(parts)
                stats["chapters"].append((chno, "", title, pid))
                out.append(f"## Chapter {chno}" + (f" — {title}" if title else ""))
                consumed = {opener} | set(parts)
            out.append("")
            lines = [l for l in lines
                     if clean_line(l["text"]).strip() not in consumed]

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
            if prev_txt and len(t) > 25:
                if difflib.SequenceMatcher(None, prev_txt, t,
                                           autojunk=False).ratio() > 0.85:
                    stats["dup_lines"].append((pid, t[:60]))
            prev_txt = t

            bold = "<b>" in l["text"]
            indented = indent_lo < l["bbox"][0] <= indent_hi
            is_verse = has_deva(t) and (not require_danda or DANDA_ANY.search(t))

            if is_verse:
                flush_prose()
                if colophon.match(t):
                    flush_verse()
                    stats["colophons"].append((pid, t))
                    out.extend([f"*{t}*", ""])
                else:
                    verse.append(t)
            else:
                flush_verse()
                if bold and len(t) < prof["heading_max_len"]:
                    flush_prose()
                    out.extend([f"### {t}", ""])
                else:
                    if indented and prose:
                        flush_prose()
                    prose.append(t)
        flush_verse(); flush_prose()

    if anchors:
        for at, pid in reversed(marks):
            out.insert(at, f"<!-- page {pid} -->")

    md = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    os.makedirs(os.path.dirname(os.path.abspath(outfile)), exist_ok=True)
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"pages assembled    : {stats['pages']}")
    print(f"chapters           : {len(stats['chapters'])} -> "
          f"{[c[0] for c in stats['chapters']]}")
    print(f"colophons          : {len(stats['colophons'])}")
    print(f"verse markers      : {len(stats['verses'])}")
    print(f"[UNCLEAR]          : {stats['unclear']}")
    print(f"dup-line flags     : {len(stats['dup_lines'])}")
    stats["anchors"] = anchors
    with open(os.path.join(ir.book_dir(ROOT, book_id), "build_stats.json"),
              "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
    return md


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("--out")
    ap.add_argument("--no-anchors", action="store_true")
    a = ap.parse_args()
    # Default output is the book's working draft, NOT Knowledge/. Knowledge/ holds the
    # approved corpus; a book only moves there once its verification is signed off.
    out = a.out or os.path.join(ir.book_dir(ROOT, a.book_id), "draft.md")
    build(a.book_id, out, anchors=not a.no_anchors)
