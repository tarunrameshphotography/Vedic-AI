"""Tests for the verification-sign-off tool (`Rules/tools/review.py`).

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Rules" / "tools"))

import review  # noqa: E402


def test_structural_is_reference_activation_only():
    assert review.is_structural({"activation": "reference"})
    assert not review.is_structural({"activation": "active"})
    assert not review.is_structural({"activation": "inert"})
    assert not review.is_structural({})


def test_sign_structural_dry_run_does_not_write(tmp_path, monkeypatch):
    """A dry run (apply=False) must never touch a file on disk."""
    chapter = {
        "book_id": "phaladeepika",
        "chapter": 1,
        "cards": [{
            "id": "PD.01.Test",
            "activation": "reference",
            "extraction": {"method": "authored", "verified_by": None,
                            "verified_date": None},
        }],
    }
    path = tmp_path / "ch01.json"
    path.write_text(json.dumps(chapter), encoding="utf-8")

    monkeypatch.setattr(review, "RULES_DIR", tmp_path)
    before = path.read_text(encoding="utf-8")
    signed, already = review.sign_structural(apply=False)
    after = path.read_text(encoding="utf-8")

    assert signed == 1
    assert already == 0
    assert before == after


def test_sign_structural_apply_writes_and_is_idempotent(tmp_path, monkeypatch):
    chapter = {
        "book_id": "phaladeepika",
        "chapter": 1,
        "cards": [
            {
                "id": "PD.01.Ref",
                "activation": "reference",
                "extraction": {"method": "authored", "verified_by": None,
                                "verified_date": None},
            },
            {
                "id": "PD.01.Active",
                "activation": "active",
                "extraction": {"method": "authored", "verified_by": None,
                                "verified_date": None},
            },
        ],
    }
    path = tmp_path / "ch01.json"
    path.write_text(json.dumps(chapter), encoding="utf-8")
    monkeypatch.setattr(review, "RULES_DIR", tmp_path)

    signed, already = review.sign_structural(apply=True)
    assert signed == 1
    assert already == 0

    doc = json.loads(path.read_text(encoding="utf-8"))
    ref_card = next(c for c in doc["cards"] if c["id"] == "PD.01.Ref")
    active_card = next(c for c in doc["cards"] if c["id"] == "PD.01.Active")
    assert ref_card["extraction"]["verified_by"] == review.STRUCTURAL_SIGNOFF
    assert ref_card["extraction"]["verified_date"]
    # An interpretive card is never auto-signed.
    assert active_card["extraction"]["verified_by"] is None

    # Running again finds nothing left to sign -- idempotent.
    signed_again, already_again = review.sign_structural(apply=True)
    assert signed_again == 0
    assert already_again == 1


def test_manifest_json_is_never_touched(tmp_path, monkeypatch):
    manifest = {"book_id": "phaladeepika", "chapters_extracted": [1]}
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(review, "RULES_DIR", tmp_path)

    before = path.read_text(encoding="utf-8")
    signed, already = review.sign_structural(apply=True)
    after = path.read_text(encoding="utf-8")

    assert signed == 0
    assert already == 0
    assert before == after


def test_real_store_queue_excludes_structural_cards():
    """Against the live store: every queued card is interpretive, and every
    reference card has already been signed off (this milestone's own claim)."""
    queue, total, verified = review.build_queue()
    queued_ids = {e["id"] for e in queue}

    cards = review.load_cards(review.RULES_DIR)
    for card in cards:
        if review.is_structural(card.raw):
            assert card.id not in queued_ids
            assert card.raw["extraction"]["verified_by"], (
                f"{card.id} is structural but was not signed off"
            )
        else:
            if not card.raw["extraction"].get("verified_by"):
                assert card.id in queued_ids

    assert total == len(queue) + verified


def test_render_queue_is_stable_markdown():
    entry = {
        "id": "PD.99.Example",
        "activation": "active",
        "verse": "1",
        "quote_display": "an example quote",
        "conditions": {"all": []},
        "predicts": {"relation": "example"},
        "note": None,
    }
    text = review.render_queue([entry])
    assert "PD.99.Example" in text
    assert "an example quote" in text
    assert "1 card(s) queued" in text
