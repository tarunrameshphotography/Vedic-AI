"""Sign-off tracking for `extraction.verified_by` across the whole rule store.

Machine verification (`verify.py`) already proves every quote is byte-exact in
the corpus. That is necessary but not sufficient: it proves the *words* are
real, not that the *card* reads them correctly. Only 4 of 404 cards carry a
human sign-off (`extraction.verified_by`) today, and there has never been a
systematic way to work through the rest -- verification has happened only
when a card was unusually disputed (see `Rules/phaladeepika/manifest.json`
`known_defects`).

This tool draws the one distinction that actually matters for sign-off:

  * **structural** cards (`activation: "reference"`) are tables and
    classifications quoted directly out of the book -- "Second house -- the
    face", the natural-friendship table, the sign/graha/house classifications.
    There is no interpretive layer between the quote and the card: reading the
    quote *is* reading the card. `verify.py`'s byte-exact check is already the
    complete verification such a card can receive, so it is signed off here as
    automated, not left permanently null waiting for a human step that would
    only repeat the same byte comparison a person already trusts a computer to
    do correctly.

  * **interpretive** cards (everything else -- `active` and `inert`) attach a
    condition/effect structure to a quote. Getting that binding right is a
    judgment call a machine cannot make: does `lord_of_house` really capture
    what "lord of the 7th" meant in that sentence, does the quoted effect
    match what `predicts` claims. These are queued for a human(+Claude)
    reading pass, in the same recorded style already used for the 4 cards
    that have one (`Rules/phaladeepika/ch02.json`, `ch09.json`, `ch10.json`).

Usage:
  python Rules/tools/review.py                 dry run: counts only, no writes
  python Rules/tools/review.py --sign-structural   sign off structural cards, write files
  python Rules/tools/review.py --queue          write Reports/VERIFICATION_QUEUE.md
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Engine.rules import RuleStoreError, load_cards   # noqa: E402

RULES_DIR = ROOT / "Rules"
REPORT_PATH = ROOT / "Reports" / "VERIFICATION_QUEUE.md"

STRUCTURAL_SIGNOFF = (
    "automated (Rules/tools/review.py): reference/table card -- the quote is "
    "the fact itself, with no interpretation between quote and card; "
    "byte-exact verification (verify.py) is the complete check such a card "
    "can receive"
)


def is_structural(card_raw: dict) -> bool:
    return card_raw.get("activation") == "reference"


def chapter_files() -> list[Path]:
    return sorted(RULES_DIR.rglob("*.json"))


def sign_structural(apply: bool) -> tuple[int, int]:
    """Sign off every unverified structural card. Returns (signed, already)."""
    signed = already = 0
    today = datetime.date.today().isoformat()

    for path in chapter_files():
        if path.name == "manifest.json":
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for card in doc.get("cards", []):
            if not is_structural(card):
                continue
            extraction = card.get("extraction", {})
            if extraction.get("verified_by"):
                already += 1
                continue
            signed += 1
            if apply:
                extraction["verified_by"] = STRUCTURAL_SIGNOFF
                extraction["verified_date"] = today
                card["extraction"] = extraction
                changed = True
        if changed and apply:
            path.write_text(
                json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
    return signed, already


def build_queue() -> tuple[list[dict], int, int]:
    """Every interpretive card still missing a sign-off, in card order.

    Returns (queue_entries, total_interpretive, already_verified_interpretive).
    """
    try:
        cards = load_cards(RULES_DIR)
    except (RuleStoreError, KeyError) as exc:
        raise SystemExit(f"FAIL: rule store will not load: {exc}")

    queue, total, verified = [], 0, 0
    for card in cards:
        if is_structural(card.raw):
            continue
        total += 1
        extraction = card.raw.get("extraction", {})
        if extraction.get("verified_by"):
            verified += 1
            continue
        queue.append({
            "id": card.id,
            "activation": card.activation,
            "verse": card.verse,
            "quote_display": card.quote_display,
            "conditions": card.conditions,
            "predicts": card.predicts,
            "note": card.raw.get("note"),
        })
    return queue, total, verified


def render_queue(queue: list[dict]) -> str:
    lines = [
        "# Verification queue -- interpretive cards awaiting sign-off",
        "",
        "Generated by `Rules/tools/review.py --queue`. **Do not edit by hand.**",
        "",
        "Structural (reference/table) cards are excluded -- they are signed off",
        "automatically by the same tool; see `Rules/tools/review.py` for why.",
        "Each entry below needs a human(+Claude) reading pass: does `conditions`",
        "and `predicts` actually say what the quoted text says. Record a real",
        "sign-off in the card's `extraction.verified_by` in the style already",
        "used for `PD.02.*`, `PD.09.*`, `PD.10.*` -- reviewer name(s) plus a short",
        "description of what was checked -- not a blanket approval.",
        "",
        f"**{len(queue)} card(s) queued.**",
        "",
    ]
    for entry in queue:
        lines.append(f"## `{entry['id']}` (v. {entry['verse']}, {entry['activation']})")
        lines.append("")
        lines.append(f"> {entry['quote_display']}")
        lines.append("")
        lines.append(f"- conditions: `{json.dumps(entry['conditions'])}`")
        lines.append(f"- predicts: `{json.dumps(entry['predicts'])}`")
        if entry["note"]:
            lines.append(f"- note: {entry['note']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sign-structural", action="store_true",
                     help="write automated sign-off onto unverified structural cards")
    ap.add_argument("--queue", action="store_true",
                     help="write Reports/VERIFICATION_QUEUE.md")
    args = ap.parse_args()

    signed, already = sign_structural(apply=args.sign_structural)
    if args.sign_structural:
        print(f"structural cards signed off ... {signed}")
        print(f"structural cards already signed  {already}")
    else:
        print(f"structural cards to sign off ... {signed} (dry run -- rerun with --sign-structural)")
        print(f"structural cards already signed  {already}")

    queue, total, verified = build_queue()
    print(f"\ninterpretive cards ............. {total}")
    print(f"interpretive cards verified ..... {verified}")
    print(f"interpretive cards queued ....... {len(queue)}")

    if args.queue:
        REPORT_PATH.write_text(render_queue(queue), encoding="utf-8")
        print(f"\nwrote {REPORT_PATH.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
