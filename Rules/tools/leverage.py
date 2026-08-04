"""Rank the Phase 3 work queue by executable knowledge unlocked per unit of work.

The metric this phase is judged on is not how many cards exist. It is how many
of them the engine can actually run. A card is executable when every dependency
it declares is implemented -- so the question "what should we do next?" is a
measurable one, and this tool measures it instead of arguing it.

Three things are computed, all from the backlog:

  1. **Solo unlock.** Implementing one capability on its own. Usually zero:
     most inert cards declare several dependencies and unlock only when the
     last of them lands. A ranking by "cards blocked" alone is therefore
     actively misleading, which is why that number is reported next to the
     solo unlock rather than instead of it.

  2. **Closure unlock.** Implementing a capability *and everything it itself
     depends on*, including the corpus chapters carrying the doctrine it must
     read. This is the honest cost and the honest return.

  3. **Greedy frontier.** Repeatedly take the closure with the best
     unlocked-per-unit-effort, until nothing unlocks anything.

Effort for code is an estimate, declared in the registry and labelled as one.
Effort for encoding a chapter is measured from the corpus: its paragraph count
against the paragraphs-per-card rate actually observed in the chapters already
encoded. Nothing here is guessed silently.

Usage:  python Rules/tools/leverage.py [--write]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Rules" / "tools"))

from Engine.rules import load_cards                                   # noqa: E402
from backlog import (REGISTRY, build, chapter_bounds, dependency_state,  # noqa: E402
                     load_corpus, paragraphs)

REPORT = ROOT / "Reports" / "PHASE3_PLAN.md"


# --- measuring the encoding work -------------------------------------------

def chapter_sizes(book_id: str) -> dict[int, int]:
    """Paragraphs per chapter -- the only honest proxy for encoding effort."""
    text = load_corpus(book_id)
    out = {}
    for m in re.finditer(r"^## Chapter (\d+) — ", text, re.MULTILINE):
        ch = int(m.group(1))
        lo, hi = chapter_bounds(text, ch)
        out[ch] = len(paragraphs(text, lo, hi))
    return out


def observed_rate(cards, sizes) -> float:
    """Cards per paragraph, measured over the chapters already encoded."""
    done = sorted({c.chapter for c in cards})
    n_cards = sum(1 for c in cards if c.chapter in done)
    n_paras = sum(sizes[ch] for ch in done if ch in sizes)
    return n_cards / n_paras if n_paras else 1.0


# --- the graph ---------------------------------------------------------------

# Surface markers for the capabilities a chapter's rules are written in. A
# paragraph mentioning any of these states its rule in terms the fact extractor
# cannot produce today, so a card encoded from it would be born inert. This is
# a measurement of the corpus, not a prediction about it.
CAPABILITY_MARKERS = (
    (r"lord of|lords of", "dep.lord-of-house"),
    (r"aspect|glance", "dep.aspects"),
    (r"benefic|malefic", "dep.nature"),
    (r"exalt|debilit|own sign|moolatrikona", "dep.dignity"),
    (r"inimical|friend|enem", "dep.dignity-friendship"),
    (r"combust|eclipsed by the Sun", "dep.combust"),
    (r"\bdasa|dasha", "dep.dasa"),
    (r"navamsa|amsa\b|varga", "dep.varga"),
    (r"\bstrength|strong\b|weak\b", "dep.strength"),
)


def projection(book_id: str, encoded: set[int], sizes: dict[int, int],
               rate: float, state: dict[str, bool] | None = None) -> list[dict]:
    """Per chapter: how much of it would be born inert if encoded today.

    Only markers whose capability is still missing count. Implementing an
    extractor therefore moves this number by itself, which is the whole point:
    the same encoding work buys more executable knowledge afterwards than
    before, and this measures how much more.
    """
    state = state or {}
    live = [m for m, dep in CAPABILITY_MARKERS if not state.get(dep, False)]
    text = load_corpus(book_id)
    out = []
    for ch in sorted(sizes):
        lo, hi = chapter_bounds(text, ch)
        bodies = [p[2] for p in paragraphs(text, lo, hi)]
        if not bodies:
            continue
        hit = sum(1 for b in bodies
                  if any(re.search(m, b, re.I) for m in live))
        out.append({
            "chapter": ch, "paragraphs": len(bodies),
            "est_cards": round(len(bodies) * rate),
            "blocked_fraction": hit / len(bodies),
            "encoded": ch in encoded,
        })
    return out


def closure(dep_id: str, deps: dict, seen: set[str] | None = None) -> set[str]:
    """A capability and everything it transitively needs (deps only)."""
    seen = seen if seen is not None else set()
    if dep_id in seen or dep_id not in deps:
        return seen
    seen.add(dep_id)
    for d in deps[dep_id].get("depends_on", []):
        if d.startswith("dep."):
            closure(d, deps, seen)
    return seen


def chapters_needed(dep_ids: set[str], deps: dict) -> set[str]:
    out = set()
    for d in dep_ids:
        for x in deps.get(d, {}).get("depends_on", []):
            if x.startswith("chapter:"):
                out.add(x)
    return out


def unlocked_by(implemented: set[str], inert) -> list:
    """Inert cards whose every declared dependency is in `implemented`."""
    return [c for c in inert
            if c.raw.get("requires")
            and all(d in implemented for d in c.raw["requires"])]


# --- main --------------------------------------------------------------------

def analyse():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    deps = registry["dependencies"]
    cards = load_cards(ROOT / "Rules")
    inert = [c for c in cards if c.activation == "inert"]
    entries, _, state, _, _, problems, counts = build()

    sizes = chapter_sizes("phaladeepika")
    rate = observed_rate(cards, sizes)

    already = {d for d, ok in state.items() if ok}

    # Backlog pressure per dependency, and what implementing it really costs.
    rows = []
    for dep_id, dep in deps.items():
        if dep_id == "dep.none" or state.get(dep_id):
            continue
        blocked_cards = [c for c in inert if dep_id in c.raw.get("requires", [])]
        blocked_entries = [e for e in entries
                           if e["status"] == "deferred" and dep_id in e["requires"]]
        blocked_ch = [e for e in blocked_entries if e["kind"] == "chapter"]
        blocked_pa = [e for e in blocked_entries if e["kind"] == "passage"]

        solo = len(unlocked_by(already | {dep_id}, inert))

        cl = closure(dep_id, deps)
        chs = chapters_needed(cl, deps)
        code_effort = sum(deps[d].get("effort", 0) for d in cl)
        encode_effort = sum(
            max(1, round(sizes.get(int(c.split(".")[-1]), 0) * rate / 4))
            for c in chs)
        total_effort = code_effort + encode_effort
        cl_unlock = len(unlocked_by(already | cl, inert))

        rows.append({
            "dep": dep_id, "title": dep["title"], "kind": dep["kind"],
            "cards_blocked": len(blocked_cards),
            "entries_blocked": len(blocked_entries),
            "chapters_blocked": len(blocked_ch),
            "passages_blocked": len(blocked_pa),
            "solo_unlock": solo,
            "closure": sorted(cl),
            "closure_chapters": sorted(chs),
            "effort": total_effort,
            "code_effort": code_effort,
            "encode_effort": encode_effort,
            "closure_unlock": cl_unlock,
            "roi": cl_unlock / total_effort if total_effort else 0.0,
        })

    # Greedy frontier: take the best closure, bank it, repeat.
    have = set(already)
    frontier, step = [], 0
    while True:
        step += 1
        best = None
        for r in rows:
            if r["dep"] in have:
                continue
            cl = set(r["closure"]) | have
            gain = len(unlocked_by(cl, inert)) - len(unlocked_by(have, inert))
            cost = sum(deps[d].get("effort", 0) for d in set(r["closure"]) - have)
            cost += r["encode_effort"] if not (set(r["closure_chapters"]) & have) else 0
            cost = max(cost, 1)
            if gain > 0 and (best is None or gain / cost > best["roi"]):
                best = {"dep": r["dep"], "title": r["title"], "gain": gain,
                        "cost": cost, "roi": gain / cost,
                        "closure": sorted(set(r["closure"]) - have),
                        "chapters": r["closure_chapters"]}
        if best is None:
            break
        have |= set(best["closure"])
        have |= set(best["chapters"])
        best["step"] = step
        best["cumulative"] = len(unlocked_by(have, inert))
        frontier.append(best)

    encoded = {c.chapter for c in cards}
    proj = projection("phaladeepika", encoded, sizes, rate, state)
    return registry, rows, frontier, counts, sizes, rate, inert, problems, proj


def render(rows, frontier, counts, sizes, rate, inert, proj) -> str:
    L, A = [], None
    L = []
    A = L.append
    A("# Phase 3 — highest-return work order")
    A("")
    A("Generated by `Rules/tools/leverage.py` from the deferred-knowledge "
      "registry. **Do not edit by hand.**")
    A("")
    A(f"The store holds **{counts['cards']}** cards, of which "
      f"**{counts['firing']}** are executable and **{counts['inert']}** are "
      f"recorded but blocked. This document ranks what to build next by how "
      f"much of that blocked knowledge each capability releases.")
    A("")
    A(f"Encoding effort is measured, not guessed: across the chapters already "
      f"encoded the corpus yields **{rate:.2f} cards per paragraph**, and each "
      f"deferred chapter is costed from its own paragraph count at that rate. "
      f"Code effort is an estimate, declared per dependency in "
      f"`Rules/deferred.json` with its basis.")
    A("")

    A("## Why \"cards blocked\" is the wrong ranking")
    A("")
    A("Most inert cards declare several dependencies and become executable only "
      "when the *last* one lands. Implementing the single most-cited capability "
      "on its own therefore usually releases nothing at all. Both numbers are "
      "shown below so the difference is visible.")
    A("")
    A("| Dependency | Kind | Cards blocked | Entries | Solo unlock | Closure unlock | Effort | Return |")
    A("|---|---|---:|---:|---:|---:|---:|---:|")
    for r in sorted(rows, key=lambda r: (-r["roi"], -r["closure_unlock"], r["dep"])):
        A(f"| `{r['dep']}` — {r['title']} | {r['kind']} | {r['cards_blocked']} | "
          f"{r['entries_blocked']} | {r['solo_unlock']} | {r['closure_unlock']} | "
          f"{r['effort']} | {r['roi']:.2f} |")
    A("")
    A("*Solo unlock* — cards that become executable if only this lands. "
      "*Closure unlock* — cards that become executable if this and everything "
      "it itself needs land, including the corpus chapters carrying the "
      "doctrine it must read. *Return* is closure unlock ÷ effort.")
    A("")

    A("## The dependency graph")
    A("")
    A("Edges point from a capability to what it needs. `ch.N` is a corpus "
      "chapter that must be encoded first, because the doctrine the capability "
      "reads is printed there and the engine may not hardcode it.")
    A("")
    A("```mermaid")
    A("graph LR")
    seen = set()
    for r in sorted(rows, key=lambda r: r["dep"]):
        node = r["dep"].replace("dep.", "").replace("-", "_")
        for d in r["closure"]:
            if d == r["dep"]:
                continue
            tgt = d.replace("dep.", "").replace("-", "_")
            edge = (node, tgt)
            if edge not in seen:
                seen.add(edge)
                A(f"  {node} --> {tgt}")
        for c in r["closure_chapters"]:
            ch = "ch" + c.split(".")[-1]
            edge = (node, ch)
            if edge not in seen:
                seen.add(edge)
                A(f"  {node} --> {ch}")
    A("```")
    A("")

    A("## Recommended order")
    A("")
    if not frontier:
        A("No capability releases any currently blocked card. Continue "
          "encoding chapters.")
    else:
        A("| Step | Build | Also requires | Chapters first | Cost | Cards released | Running total executable |")
        A("|---:|---|---|---|---:|---:|---:|")
        for f in frontier:
            also = ", ".join(f"`{d}`" for d in f["closure"] if d != f["dep"]) or "—"
            chs = ", ".join("ch. " + c.split(".")[-1] for c in f["chapters"]) or "—"
            A(f"| {f['step']} | `{f['dep']}` — {f['title']} | {also} | {chs} | "
              f"{f['cost']} | +{f['gain']} | {counts['firing'] + f['cumulative']} |")
        A("")
        total_gain = frontier[-1]["cumulative"]
        total_cost = sum(f["cost"] for f in frontier)
        A(f"Completing this sequence costs **{total_cost} units** and moves "
          f"executable cards from **{counts['firing']}** to "
          f"**{counts['firing'] + total_gain}** — releasing "
          f"**{total_gain} of the {counts['inert']}** currently blocked cards.")
    A("")

    A("## What encoding a chapter today would actually buy")
    A("")
    A("The ranking above counts only cards that already exist. The larger "
      "effect is on the cards not yet written: a chapter whose rules are "
      "stated in lordship, aspect, benefic/malefic, dignity, dasa or varga "
      "terms will be encoded into cards that are born inert. The share of "
      "each chapter's paragraphs that use that vocabulary is measured below.")
    A("")
    A("| Chapter | Paragraphs | Est. cards | Would be born inert | |")
    A("|---:|---:|---:|---:|---|")
    for r in proj:
        A(f"| {r['chapter']} | {r['paragraphs']} | {r['est_cards']} | "
          f"{r['blocked_fraction'] * 100:.0f}% | "
          f"{'encoded' if r['encoded'] else ''} |")
    A("")
    pend = [r for r in proj if not r["encoded"]]
    tot = sum(r["est_cards"] for r in pend)
    blocked = sum(r["est_cards"] * r["blocked_fraction"] for r in pend)
    A(f"Across the {len(pend)} unencoded chapters that is roughly **{tot} "
      f"cards**, of which about **{blocked:.0f} ({blocked / tot * 100:.0f}%) "
      f"would be inert on arrival** if they were encoded before the missing "
      f"capabilities exist.")
    A("")

    A("## Cards that no sequence here releases")
    A("")
    have = set()
    for f in frontier:
        have |= set(f["closure"]) | set(f["chapters"])
    stuck = [c for c in inert if c not in unlocked_by(have | {"dep.none"}, inert)]
    if stuck:
        A(f"{len(stuck)} card(s) remain blocked after every step above, because "
          f"they depend on capabilities with no path that pays for itself yet:")
        A("")
        for c in sorted(stuck, key=lambda c: c.id):
            A(f"- `{c.id}` — {', '.join(c.raw.get('requires', []))}")
    else:
        A("None. The sequence above releases every blocked card.")
    A("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    registry, rows, frontier, counts, sizes, rate, inert, problems, proj = analyse()
    if problems:
        print(f"WARNING: the backlog itself has {len(problems)} problem(s); "
              f"run Rules/tools/backlog.py")

    print(f"cards {counts['cards']} ({counts['firing']} executable, "
          f"{counts['inert']} blocked); measured rate {rate:.2f} cards/paragraph\n")
    print(f"{'dependency':34s} {'blk':>4s} {'solo':>5s} {'clos':>5s} "
          f"{'eff':>4s} {'ROI':>6s}")
    for r in sorted(rows, key=lambda r: (-r["roi"], -r["closure_unlock"])):
        print(f"{r['dep']:34s} {r['cards_blocked']:4d} {r['solo_unlock']:5d} "
              f"{r['closure_unlock']:5d} {r['effort']:4d} {r['roi']:6.2f}")

    print("\nrecommended order:")
    for f in frontier:
        chs = ", ".join("ch." + c.split(".")[-1] for c in f["chapters"]) or "-"
        print(f"  {f['step']}. {f['dep']:28s} cost {f['cost']:3d}  "
              f"+{f['gain']:3d} cards  (chapters: {chs})")

    if args.write:
        REPORT.write_text(
            render(rows, frontier, counts, sizes, rate, inert, proj) + "\n",
            encoding="utf-8")
        print(f"\nwrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
