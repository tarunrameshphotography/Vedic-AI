"""Tests for the dignity-override mechanism (dep.dignity-override).

"A retrograde planet produces the same effect as if exalted" is not a claim
about a nativity -- it changes the dignity another card's condition is keyed
on. Two things are tested: the mechanism in isolation, against a synthetic
store built the same way `test_doctrine.py` builds one, and the real card
against a real chart with a retrograde graha, so the wiring in `pipeline.py`
is exercised too, not just the function in isolation.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import FactSet, make_fact
from Engine.overrides import apply_overrides
from Engine.pipeline import run
from Engine.rules import load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

FRAME = {"reference": "lagna", "varga": "D1", "house_system": "whole_sign"}

# Mars and Mercury are both retrograde and in a sign with no natural dignity;
# the nodes are retrograde too, on every chart, by construction.
RETROGRADE_DEMO = BirthRecord(
    date="2023-01-05", time="12:00", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)


def synthetic_store(tmp_path, override_cards, doctrine_cards=()):
    """A minimal rule store on disk: some reference doctrine, one meta card.

    Loaded through `load_cards`, the same path the engine uses, so these
    tests exercise real `RuleCard` objects rather than hand-built ones.
    """
    cards = []
    for i, (relation, predicts) in enumerate(doctrine_cards, start=1):
        cards.append({
            "id": f"XX.09.Doctrine{i:03d}", "schema": 1,
            "source": {"book_id": "phaladeepika", "chapter": 9, "verse": "1",
                       "page_anchor": None, "tier": 1, "quote": f"d{i}",
                       "quote_display": f"d{i}", "quote_sha256": "0" * 64,
                       "char_span": [0, 2], "span_trimmed": None},
            "scope": {}, "activation": "reference",
            "conditions": {"all": []},
            "predicts": {"relation": relation, **predicts},
            "timing": "natal", "weight": 1.0, "specificity": 1,
        })
    for i, card in enumerate(override_cards, start=1):
        cards.append({
            "id": card.get("id", f"XX.09.Override{i:03d}"), "schema": 1,
            "source": {"book_id": "phaladeepika", "chapter": 9, "verse": "20",
                       "page_anchor": None, "tier": 1, "quote": f"o{i}",
                       "quote_display": f"o{i}", "quote_sha256": "0" * 64,
                       "char_span": [0, 2], "span_trimmed": None},
            "scope": {}, "activation": card.get("activation", "reference"),
            "kind": "meta",
            "conditions": card["conditions"],
            "predicts": {"domain": "meta", "effect": card["effect"]},
            "timing": "natal", "weight": 1.0, "specificity": 1,
        })
    d = tmp_path / "synthetic"
    d.mkdir(parents=True, exist_ok=True)
    (d / "ch09.json").write_text(
        json.dumps({"book_id": "phaladeepika", "chapter": 9, "cards": cards}),
        encoding="utf-8")
    return load_cards(tmp_path)


class _FakeHouses(dict):
    def __getitem__(self, k):
        return "whole_sign" if k == "system" else super().__getitem__(k)


class _FakeChart:
    """Only `chart.houses["system"]` is read by `apply_overrides`."""
    houses = {"system": "whole_sign"}


# --- unit: the mechanism in isolation ----------------------------------------

def test_a_graha_with_grounds_gains_the_overridden_dignity(tmp_path):
    cards = synthetic_store(
        tmp_path,
        override_cards=[{"conditions": {"all": [{"retrograde": {"graha": "?g"}}]},
                         "effect": "treat_as_exalted"}],
        doctrine_cards=[("exaltation", {"graha": "Mercury",
                                        "exaltation_sign": "Virgo",
                                        "debilitation_sign": "Pisces"})],
    )
    doctrine = Doctrine.from_cards(cards)
    facts = FactSet([make_fact("retrograde", {"graha": "Mercury"}, FRAME)])
    out = apply_overrides(cards, doctrine, facts, _FakeChart())
    assert "dignity(Mercury,exalted)" in out
    ev = out.get("dignity(Mercury,exalted)").evidence
    assert ev["override_card"].startswith("XX.09.Override")
    assert "XX.01.Exaltation" not in ev["doctrine"]  # only real card ids travel


def test_a_graha_with_no_exaltation_card_is_left_alone(tmp_path):
    """The store's silence about a graha's dignity must stay silence."""
    cards = synthetic_store(
        tmp_path,
        override_cards=[{"conditions": {"all": [{"retrograde": {"graha": "?g"}}]},
                         "effect": "treat_as_exalted"}],
        doctrine_cards=[("exaltation", {"graha": "Mercury",
                                        "exaltation_sign": "Virgo",
                                        "debilitation_sign": "Pisces"})],
    )
    doctrine = Doctrine.from_cards(cards)
    facts = FactSet([make_fact("retrograde", {"graha": "Rahu"}, FRAME)])
    out = apply_overrides(cards, doctrine, facts, _FakeChart())
    assert "dignity(Rahu,exalted)" not in out
    assert len(list(out)) == len(list(facts))  # nothing was added at all


def test_an_existing_dignity_is_not_duplicated_or_overwritten(tmp_path):
    """A graha already exalted naturally must not gain a second, redundant fact."""
    cards = synthetic_store(
        tmp_path,
        override_cards=[{"conditions": {"all": [{"retrograde": {"graha": "?g"}}]},
                         "effect": "treat_as_exalted"}],
        doctrine_cards=[("exaltation", {"graha": "Mercury",
                                        "exaltation_sign": "Virgo",
                                        "debilitation_sign": "Pisces"})],
    )
    doctrine = Doctrine.from_cards(cards)
    natural = make_fact("dignity", {"graha": "Mercury", "dignity": "exalted"},
                        FRAME, {"doctrine": ["XX.natural"]})
    facts = FactSet([make_fact("retrograde", {"graha": "Mercury"}, FRAME), natural])
    out = apply_overrides(cards, doctrine, facts, _FakeChart())
    assert len(out.by_predicate("dignity")) == 1
    assert out.get("dignity(Mercury,exalted)").evidence["doctrine"] == ["XX.natural"]


def test_an_unrecognised_effect_name_is_ignored(tmp_path):
    """The effect vocabulary is fixed; a card outside it does nothing here."""
    cards = synthetic_store(
        tmp_path,
        override_cards=[{"conditions": {"all": [{"retrograde": {"graha": "?g"}}]},
                         "effect": "something_else"}],
    )
    doctrine = Doctrine.from_cards(cards)
    facts = FactSet([make_fact("retrograde", {"graha": "Mercury"}, FRAME)])
    out = apply_overrides(cards, doctrine, facts, _FakeChart())
    assert out is facts


def test_a_card_that_is_not_reference_activation_is_not_consulted(tmp_path):
    """Only doctrine the engine reads drives an override -- a card written
    `activation: "active"` would be evaluated by Stage 6 as an ordinary
    claim instead, and must not also be read here."""
    cards = synthetic_store(
        tmp_path,
        override_cards=[{"conditions": {"all": [{"retrograde": {"graha": "?g"}}]},
                         "effect": "treat_as_exalted", "activation": "active"}],
        doctrine_cards=[("exaltation", {"graha": "Mercury",
                                        "exaltation_sign": "Virgo",
                                        "debilitation_sign": "Pisces"})],
    )
    doctrine = Doctrine.from_cards(cards)
    facts = FactSet([make_fact("retrograde", {"graha": "Mercury"}, FRAME)])
    out = apply_overrides(cards, doctrine, facts, _FakeChart())
    assert out is facts


# --- end-to-end: the real card against a real chart --------------------------

@pytest.fixture(scope="module")
def golden():
    return run(RETROGRADE_DEMO)


def test_golden_retrograde_grahas_gain_the_exalted_dignity(golden):
    """Mars and Mercury are retrograde here in signs with no natural dignity."""
    assert golden.chart.bodies["Mars"].retrograde
    assert golden.chart.bodies["Mercury"].retrograde
    assert "dignity(Mars,exalted)" in golden.facts
    assert "dignity(Mercury,exalted)" in golden.facts
    for g in ("Mars", "Mercury"):
        ev = golden.facts.get(f"dignity({g},exalted)").evidence
        assert ev["override_card"] == "PD.09.Retrograde.AsExalted"
        assert "PD.01.Exaltation." + g in ev["doctrine"]


def test_golden_the_nodes_gain_no_override_despite_being_retrograde(golden):
    """No singular exaltation card exists for Rahu or Ketu; the override
    must stay silent rather than assert a dignity no card in the store backs."""
    assert golden.chart.bodies["Rahu"].retrograde
    assert golden.chart.bodies["Ketu"].retrograde
    assert "dignity(Rahu,exalted)" not in golden.facts
    assert "dignity(Ketu,exalted)" not in golden.facts


def test_golden_the_override_card_never_becomes_a_claim(golden):
    """Reference doctrine, not a rule: the same treatment every lookup table
    the engine reads already gets."""
    assert not [c for c in golden.claims
                if c.derived["rule_card"] == "PD.09.Retrograde.AsExalted"]


def test_golden_the_downstream_dignity_card_fires_for_the_overridden_grahas(golden):
    """The whole point: an unrelated card conditioned on dignity=exalted
    fires for Mars and Mercury without being rewritten to know about
    retrogression at all."""
    got = {c.derived["variables"]["?g"] for c in golden.claims
           if c.derived["rule_card"] == "PD.09.Dignity.Exalted"}
    assert {"Mars", "Mercury"} <= got
    assert not got & {"Rahu", "Ketu"}


def test_golden_still_verifies(golden):
    assert golden.verification.ok
