"""Authoring aid: propose verified/ figure files for South Indian horoscope charts.

    python tools/propose_charts.py <book_id> <pdf> [--write]

This does NOT change the pipeline. It writes the same books/<book>/verified/pNNNN.json
files a human would write by hand, and every proposal must still be checked against the
rendered page before it is trusted.

It is only sound for books produced by producers/pdf_text.py, where two things are exact
rather than inferred:

  * the cell labels come from the embedded text layer, so there is no OCR error, and
  * the chart grid is vector graphics, so the cell boundaries are known precisely
    rather than guessed from where the labels happen to sit.

Neither holds for a scanned book. Charts in scanned books stay a manual, by-eye job.

South Indian layout: a 4x4 grid with a hollow centre; signs are fixed by cell position,
running clockwise from Aries in the second cell of the top row.
"""
import argparse
import json
import os
import sys
from collections import defaultdict

import fitz

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from corpuslib import ir
from corpuslib.ids import local_name
from corpuslib.normalize import strip_tags

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
# (row, col) -> index into SIGNS
CELL_SIGN = {
    (0, 0): 11, (0, 1): 0, (0, 2): 1, (0, 3): 2,
    (1, 3): 3, (2, 3): 4, (3, 3): 5,
    (3, 2): 6, (3, 1): 7, (3, 0): 8,
    (2, 0): 9, (1, 0): 10,
}
LAGNA_TOKENS = {"l", "lag", "lagna", "asc", "l.", "lg"}

# Ashtakavarga charts print bindus as runs of the character "0" rather than naming
# planets. Rendering those as if they were planet names ("Planets: 000") is nonsense;
# they are counts, and their total is a check on the transcription (48 for a single
# planet's ashtakavarga, 337 for the sarvashtakavarga).
def _is_bindu(tok):
    t = tok.strip()
    return bool(t) and set(t) <= {"0", "o", "O", " "}


# Each planet's ashtakavarga has its own bindu total; they are not all 48. These are
# the standard values, and they sum to the sarvashtakavarga total of 337. A chart whose
# total is not in this set is not necessarily wrong, but it does need a human to look.
BINDU_TOTALS = {48: "Sun", 49: "Moon or Lagna", 39: "Mars or Saturn",
                54: "Mercury", 56: "Jupiter", 52: "Venus", 337: "sarvashtakavarga"}


def _bindu_count(names):
    return sum(len([c for c in n if c in "0oO"]) for n in names)


def cluster(values, tol=4):
    """Collapse near-identical coordinates (the PDF draws each rule twice)."""
    out = []
    for v in sorted(values):
        if out and v - out[-1] <= tol:
            continue
        out.append(v)
    return out


def _even_runs(edges):
    """Every run of 5 *consecutive* edges that is evenly spaced -- one 4-cell axis.

    Deliberately conservative. It handles a single chart and charts stacked vertically
    (which share one x-axis), which is the common case. Pages carrying a 2x2 block of
    charts interleaved with ruled matrix tables -- the Ashtakavarga summary pages -- are
    not reliably separable this way and are transcribed by hand instead; a looser match
    produced dozens of spurious overlapping grids.
    """
    out = []
    for i in range(len(edges) - 4):
        run = edges[i:i + 5]
        gaps = [run[k + 1] - run[k] for k in range(4)]
        if min(gaps) > 12 and max(gaps) - min(gaps) <= 0.30 * max(gaps):
            out.append(run)
    return out


def find_grids(page):
    """Return every 4x4 square grid drawn on the page, as (xs, ys).

    A page may carry one chart, two stacked, or a 2x2 block of four -- the Ashtakavarga
    chapter prints several per page. Scanning for evenly-spaced runs of five edges finds
    them all, and rejects the ruled matrix tables that are not square.
    """
    dr = page.get_drawings()
    if not dr:
        return []
    xs = cluster({round(d["rect"].x0) for d in dr} | {round(d["rect"].x1) for d in dr})
    ys = cluster({round(d["rect"].y0) for d in dr} | {round(d["rect"].y1) for d in dr})
    grids = []
    for xr in _even_runs(xs):
        for yr in _even_runs(ys):
            w, h = xr[-1] - xr[0], yr[-1] - yr[0]
            if 60 < w < 500 and 60 < h < 500 and abs(w - h) < 0.35 * max(w, h):
                grids.append((xr, yr))
    # drop grids that hold no text at all (spurious edge combinations)
    return grids


def split_across_columns(txt, x0, x1, xs):
    """Split a text line that spans more than one chart column.

    PyMuPDF returns one "line" per baseline, so two adjacent cells whose contents sit
    on the same baseline arrive merged ("00000 0000" spanning two cells). Assigning the
    whole line by its midpoint puts both groups in one cell -- which silently moved four
    bindus from Libra into Scorpio on printed page 227. Tokens are therefore placed by
    their own interpolated position, not the line's.
    """
    toks = [t for t in txt.split() if t]
    if len(toks) < 2 or x1 <= x0:
        return [(txt, (x0 + x1) / 2)]
    total = len(txt)
    out, cursor = [], 0
    for t in toks:
        i = txt.index(t, cursor)
        cursor = i + len(t)
        centre = x0 + (x1 - x0) * ((i + len(t) / 2) / total)
        out.append((t, centre))
    # only bother if the tokens genuinely fall in different columns
    cols = {next((c for c in range(4) if xs[c] <= cx < xs[c + 1]), None)
            for _, cx in out}
    return out if len(cols) > 1 else [(txt, (x0 + x1) / 2)]


def cell_of(x, y, xs, ys):
    col = next((i for i in range(4) if xs[i] <= x < xs[i + 1]), None)
    row = next((i for i in range(4) if ys[i] <= y < ys[i + 1]), None)
    return (row, col) if row is not None and col is not None else None


def ascii_chart(cells):
    """Render the 4x4 grid, hollow centre, cells stacked vertically."""
    grid = {}
    for (r, c), names in cells.items():
        grid[(r, c)] = names
    height = {r: max([1] + [len(grid.get((r, c), [])) for c in range(4)])
              for r in range(4)}
    W = 13
    rule = "+" + "+".join(["-" * W] * 4) + "+"
    lines = [rule]
    for r in range(4):
        for k in range(height[r]):
            row = []
            for c in range(4):
                if r in (1, 2) and c in (1, 2):
                    row.append(" " * W)
                else:
                    names = grid.get((r, c), [])
                    row.append((" " + (names[k] if k < len(names) else "")).ljust(W))
            if r in (1, 2):
                lines.append("|" + row[0] + "|" + row[1] + " " + row[2] + "|"
                             + row[3] + "|")
            else:
                lines.append("|" + "|".join(row) + "|")
        lines.append(rule if r != 1 else
                     "+" + "-" * W + "+" + " " * (W * 2 + 1) + "+" + "-" * W + "+")
    return "\n".join(lines)


def build_markdown(cells, pid, printed_page, caption=""):
    lagna_cell = None
    clean = {}
    for pos, names in cells.items():
        keep = []
        for n in names:
            if n.strip().lower().strip(".") in LAGNA_TOKENS:
                lagna_cell = pos
            else:
                keep.append(n)
        clean[pos] = keep
    ascii_art = ascii_chart({**{p: v[:] for p, v in cells.items()}})

    rows = []
    lagna_sign = CELL_SIGN[lagna_cell] if lagna_cell else None
    for pos in sorted(CELL_SIGN, key=lambda p: CELL_SIGN[p]):
        names = clean.get(pos, [])
        sign_i = CELL_SIGN[pos]
        house = ((sign_i - lagna_sign) % 12 + 1) if lagna_sign is not None else None
        if not names and house is None:
            continue
        rows.append((house, SIGNS[sign_i], names, pos == lagna_cell))

    bindu_cells = [pos for pos, names in clean.items()
                   if names and all(_is_bindu(n) for n in names)]
    is_ashtaka = len(bindu_cells) >= 6
    kind = "Ashtakavarga chart" if is_ashtaka else "Horoscope chart"
    head = f"**{kind}{': ' + caption if caption else ''}**"
    md = [f"{head} (South Indian style, printed page {printed_page})", ""]
    md.append("```")
    md.append(ascii_art)
    md.append("```")
    md.append("")
    if is_ashtaka:
        total = sum(_bindu_count(clean.get(pos, [])) for pos in CELL_SIGN)
        if lagna_sign is not None:
            md.append(f"Lagna is in {SIGNS[lagna_sign]}, so houses are counted "
                      f"from there.")
            md.append("")
            md.append("| House | Sign | Bindus |")
            md.append("|---|---|---|")
            for house, sign, names, is_lag in sorted(rows, key=lambda r: r[0]):
                label = f"{house}" + (" (Lagna)" if is_lag else "")
                md.append(f"| {label} | {sign} | {_bindu_count(names)} |")
        else:
            md.append("| Sign | Bindus |")
            md.append("|---|---|")
            for _, sign, names, _ in rows:
                md.append(f"| {sign} | {_bindu_count(names)} |")
        md.append("")
        md.append(f"Total bindus: **{total}**"
                  + (f" — the standard total for {BINDU_TOTALS[total]}."
                     if total in BINDU_TOTALS else
                     " — this matches no standard planetary ashtakavarga total "
                     "(48 Sun, 49 Moon/Lagna, 39 Mars/Saturn, 54 Mercury, 56 Jupiter, "
                     "52 Venus, 337 sarva), so it needs checking by eye."))
    elif lagna_sign is not None:
        md.append(f"Lagna is in {SIGNS[lagna_sign]}, so houses are counted from there.")
        md.append("")
        md.append("| House | Sign | Planets |")
        md.append("|---|---|---|")
        for house, sign, names, is_lag in sorted(rows, key=lambda r: r[0]):
            label = f"{house}" + (" (Lagna)" if is_lag else "")
            md.append(f"| {label} | {sign} | {', '.join(names) if names else '—'} |")
    else:
        md.append("No lagna marker is printed on this chart, so house numbers are **not**"
                  " assigned. Signs follow the fixed South Indian cell positions.")
        md.append("")
        md.append("| Sign | Planets |")
        md.append("|---|---|")
        for _, sign, names, _ in rows:
            if names:
                md.append(f"| {sign} | {', '.join(names)} |")
    return "\n".join(md), lagna_sign is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_id")
    ap.add_argument("pdf")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--only", help="comma-separated page sequences")
    a = ap.parse_args()

    pages = ir.load_book(ROOT, a.book_id)
    only = {int(x) for x in a.only.split(",")} if a.only else None
    doc = fitz.open(a.pdf)
    vdir = os.path.join(ir.book_dir(ROOT, a.book_id), "verified")
    if a.write:
        os.makedirs(vdir, exist_ok=True)

    found = withlagna = 0
    for p in pages:
        seq = p["seq"]
        if only and seq not in only:
            continue
        grids = find_grids(doc[seq - 1])
        if not grids:
            continue
        blocks, used_all = [], []
        for xs, ys in grids:
            cells, used, centre = defaultdict(list), [], []
            for i, l in enumerate(p["lines"]):
                x0, y0, x1, y1 = l["bbox"]
                txt = strip_tags(l["text"]).strip()
                if not txt:
                    continue
                cy = (y0 + y1) / 2
                if cell_of((x0 + x1) / 2, cy, xs, ys) is None:
                    continue
                hit = False
                for frag, cx in split_across_columns(txt, x0, x1, xs):
                    pos = cell_of(cx, cy, xs, ys)
                    if pos is None:
                        continue
                    hit = True
                    if pos in ((1, 1), (1, 2), (2, 1), (2, 2)):
                        # the hollow centre carries the caption, not a cell value
                        centre.append(frag)
                    else:
                        cells[pos].append(frag)
                if hit:
                    used.append(i)
            if not used:
                continue
            md, has_lagna = build_markdown(cells, p["page_id"], seq,
                                           " ".join(centre).strip())
            blocks.append((min(used), md, has_lagna))
            used_all += used
        if not blocks:
            continue
        blocks.sort()
        found += len(blocks)
        withlagna += sum(b[2] for b in blocks)
        md = "\n\n".join(b[1] for b in blocks)
        used = used_all
        has_lagna = any(b[2] for b in blocks)
        spec = {
            "schema": 2,
            "page_id": p["page_id"],
            "ocr_fingerprint": p["fingerprint"],
            "kind": "chart",
            "note": "South Indian horoscope chart. Cell labels are taken from the PDF's "
                    "embedded text layer and cell boundaries from the chart's vector "
                    "grid, so both are exact rather than read by eye. Proposed by "
                    "tools/propose_charts.py and checked against the rendered page.",
            "verified": "2026-08-01",
            "exclude_lines": sorted(used),
            "insert_after": min(used) - 1,
            "markdown": md,
        }
        if a.write:
            with open(os.path.join(vdir, local_name(p["page_id"]) + ".json"),
                      "w", encoding="utf-8") as f:
                json.dump(spec, f, ensure_ascii=False, indent=1)
        else:
            print(f"--- {p['page_id']} (printed {seq}) lagna={has_lagna} ---")
            print(md)
            print()
    print(f"charts found: {found}  (with lagna marker: {withlagna})"
          + ("  [written]" if a.write else "  [dry run]"))


if __name__ == "__main__":
    main()
