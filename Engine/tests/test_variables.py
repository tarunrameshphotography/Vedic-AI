"""Tests for quantified conditions.

Variables exist because the classics quantify. "A planet in his sign of
exaltation" and "the lord of the 7th occupies the 5th" cannot be written with
literals, and instantiating them per graha would make each card's own words
deny its own condition.

What is deliberately *not* here is as important as what is. There is no
arithmetic, no comparison, no disjunction inside a leaf, and no way to bind
anything but a value the FactSet already contains. Each of the three features
below -- a shared variable, an existential, and one negation -- is justified by
a rule card that was blocked without it, and nothing else was added.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

from pathlib import Path

import pytest

from Engine.chart import BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import FactSet, extract_facts, make_fact
from Engine.pipeline import run
from Engine.rules import evaluate, is_variable, load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

FRAME = {"reference": "lagna", "varga": "D1", "house_system": "whole_sign"}

DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)


def facts(*specs) -> FactSet:
    """A FactSet from (predicate, args) pairs."""
    return FactSet([make_fact(p, a, FRAME) for p, a in specs])


@pytest.fixture(scope="module")
def golden():
    return run(DEMO)


# --- what counts as a variable ----------------------------------------------

def test_variable_syntax_is_narrow():
    assert is_variable("?g") and is_variable("?x2") and is_variable("?lord")
    for not_a_var in ("g", "?G", "?", "Mars", 7, None, "??g", "any"):
        assert not is_variable(not_a_var), not_a_var


def test_the_old_any_sentinel_is_not_a_variable():
    """Cards still carrying `"any"` must stay inert, not start matching."""
    ev = evaluate({"all": [{"in_house": {"graha": "any", "house": 1}}]},
                  facts(("in_house", {"graha": "Venus", "house": 1})))
    assert not ev.satisfied


# --- existential quantification ---------------------------------------------

def test_a_variable_matches_any_graha():
    ev = evaluate({"all": [{"in_house": {"graha": "?g", "house": 1}}]},
                  facts(("in_house", {"graha": "Venus", "house": 1})))
    assert ev.satisfied
    assert ev.solutions[0].as_dict() == {"?g": "Venus"}
    assert ev.solutions[0].bindings == ("in_house(Venus,1)",)


def test_one_solution_per_satisfying_graha():
    """Three exalted grahas are three findings, not one."""
    ev = evaluate({"all": [{"dignity": {"graha": "?g", "dignity": "exalted"}}]},
                  facts(("dignity", {"graha": "Mars", "dignity": "exalted"}),
                        ("dignity", {"graha": "Venus", "dignity": "exalted"}),
                        ("dignity", {"graha": "Moon", "dignity": "own"})))
    assert len(ev.solutions) == 2
    assert {s.as_dict()["?g"] for s in ev.solutions} == {"Mars", "Venus"}


def test_a_variable_domain_comes_from_the_facts_not_a_table():
    """With no facts of that predicate there is nothing to bind, and no match."""
    ev = evaluate({"all": [{"dignity": {"graha": "?g", "dignity": "exalted"}}]},
                  facts(("in_house", {"graha": "Venus", "house": 1})))
    assert not ev.satisfied and ev.solutions == ()


# --- a variable shared across leaves ----------------------------------------

def test_the_same_variable_must_mean_the_same_graha():
    """The content of "the lord of the 7th occupies the 5th"."""
    cond = {"all": [{"lord_of_house": {"graha": "?g", "house": 7}},
                    {"in_house": {"graha": "?g", "house": 5}}]}
    hit = facts(("lord_of_house", {"graha": "Moon", "house": 7}),
                ("in_house", {"graha": "Moon", "house": 5}))
    assert evaluate(cond, hit).satisfied

    # The lord of the 7th is the Moon, but it is Venus that sits in the 5th.
    miss = facts(("lord_of_house", {"graha": "Moon", "house": 7}),
                 ("in_house", {"graha": "Venus", "house": 5}))
    assert not evaluate(cond, miss).satisfied


def test_bindings_name_both_facts_that_made_it_true():
    cond = {"all": [{"lord_of_house": {"graha": "?g", "house": 7}},
                    {"in_house": {"graha": "?g", "house": 5}}]}
    ev = evaluate(cond, facts(("lord_of_house", {"graha": "Moon", "house": 7}),
                              ("in_house", {"graha": "Moon", "house": 5})))
    assert sorted(ev.solutions[0].bindings) == [
        "in_house(Moon,5)", "lord_of_house(Moon,7)"]


def test_distinct_variables_bind_independently():
    """"The lord of the 5th or the 8th be in the 7th" -- two lordships."""
    cond = {"any": [
        {"all": [{"lord_of_house": {"graha": "?g", "house": 5}},
                 {"in_house": {"graha": "?g", "house": 7}}]},
        {"all": [{"lord_of_house": {"graha": "?h", "house": 8}},
                 {"in_house": {"graha": "?h", "house": 7}}]}]}
    ev = evaluate(cond, facts(("lord_of_house", {"graha": "Sun", "house": 8}),
                              ("lord_of_house", {"graha": "Venus", "house": 5}),
                              ("in_house", {"graha": "Sun", "house": 7})))
    assert ev.satisfied
    assert [s.as_dict() for s in ev.solutions] == [{"?h": "Sun"}]


def test_a_partly_satisfied_conjunction_yields_nothing():
    cond = {"all": [{"lord_of_house": {"graha": "?g", "house": 7}},
                    {"in_house": {"graha": "?g", "house": 5}}]}
    assert not evaluate(
        cond, facts(("lord_of_house", {"graha": "Moon", "house": 7}))).satisfied


# --- negation ----------------------------------------------------------------

def test_negation_asks_whether_any_binding_exists():
    """"If there is no planet in the Ascendant" -- a negated existential."""
    empty = {"not": {"in_house": {"graha": "?x", "house": 1}}}
    assert evaluate(empty, facts(("in_house", {"graha": "Venus", "house": 2}))).satisfied
    assert not evaluate(empty, facts(("in_house", {"graha": "Venus", "house": 1}))).satisfied


def test_a_negated_variable_exports_no_binding():
    """Variables inside a `not` are local; nothing escapes to the outer scope."""
    cond = {"all": [{"not": {"in_house": {"graha": "?x", "house": 1}}},
                    {"lord_of_house": {"graha": "?g", "house": 1}}]}
    ev = evaluate(cond, facts(("lord_of_house", {"graha": "Saturn", "house": 1}),
                              ("in_house", {"graha": "Venus", "house": 2})))
    assert ev.satisfied
    assert ev.solutions[0].as_dict() == {"?g": "Saturn"}


# --- the guards that must survive --------------------------------------------

def test_an_unknown_predicate_is_still_inert_with_variables():
    ev = evaluate({"all": [{"exalted": {"graha": "?g"}}]},
                  facts(("in_house", {"graha": "Sun", "house": 1})))
    assert not ev.satisfied and ev.missing == ("exalted",)


def test_adjacent_houses_are_still_never_confused():
    cond = {"all": [{"lord_of_house": {"graha": "?g", "house": 7}},
                    {"in_house": {"graha": "?g", "house": 7}}]}
    assert not evaluate(
        cond, facts(("lord_of_house", {"graha": "Moon", "house": 7}),
                    ("in_house", {"graha": "Moon", "house": 8}))).satisfied


# --- golden chart -------------------------------------------------------------
#
# Capricorn lagna. Venus alone in the 1st; Saturn in the 11th aspecting the 1st
# by its 3rd; Jupiter combust; Mars in Aries and Jupiter in Pisces in their own
# signs; nothing exalted or debilitated.

def test_golden_one_claim_per_graha_in_its_own_sign(golden):
    own = [c for c in golden.claims
           if c.derived["rule_card"] == "PD.09.Dignity.OwnSign"]
    assert len(own) == 2
    assert {c.derived["variables"]["?g"] for c in own} == {"Mars", "Jupiter"}


def test_golden_quantified_claims_name_their_graha(golden):
    expected = {
        "PD.02.LagnaGraha.BestowsQualities": {"Venus"},
        "PD.02.LagnaAspect.InjectsQualities": {"Saturn"},
        "PD.09.Combust": {"Jupiter"},
    }
    for card, want in expected.items():
        got = {c.derived["variables"]["?g"] for c in golden.claims
               if c.derived["rule_card"] == card}
        assert got == want, card


def test_golden_lagna_is_not_empty_so_the_lord_rule_stays_silent(golden):
    """Venus is in the 1st, so "if there is no planet in the Ascendant" fails."""
    assert not [c for c in golden.claims
                if c.derived["rule_card"] == "PD.02.LagnaEmpty.LordGivesQualities"]


def test_golden_lord_of_the_seventh_is_not_in_the_fifth(golden):
    """The Moon rules the 7th and sits in the 8th, so the rule must not fire."""
    assert "lord_of_house(Moon,7)" in golden.facts
    assert "in_house(Moon,8)" in golden.facts
    assert not [c for c in golden.claims
                if c.derived["rule_card"] == "PD.10.Lord7.In5"]


def test_golden_nothing_exalted_so_the_exaltation_rules_stay_silent(golden):
    for card in ("PD.09.Dignity.Exalted", "PD.09.Dignity.Exalted.Notes"):
        assert not [c for c in golden.claims if c.derived["rule_card"] == card]


def test_golden_every_quantified_claim_is_verified(golden):
    assert golden.verification.ok
    quantified = [c for c in golden.claims if c.derived.get("variables")]
    assert len(quantified) >= 5
    assert golden.verification.checks["conditions_reevaluated_passed"] == \
        len(golden.claims)


def test_golden_each_quantified_claim_reaches_the_report(golden):
    for c in golden.claims:
        if c.derived.get("variables"):
            assert c.claim_id in golden.consultation


# --- Stage 9 ------------------------------------------------------------------

def test_verification_rejects_a_claim_whose_binding_is_not_a_solution(golden):
    """A quantified card is satisfied by *particular* grahas, not in general."""
    from dataclasses import replace
    from Engine.activate import verify_claims

    target = next(c for c in golden.claims
                  if c.derived["rule_card"] == "PD.09.Dignity.OwnSign")
    tampered = replace(target, derived={
        **target.derived,
        "conditions_satisfied": ["dignity(Saturn,own)"],
    })
    result = verify_claims([tampered], golden.facts, golden.chart,
                           load_cards(RULES), ROOT / "Knowledge")
    assert not result.ok
    assert any("no re-derived solution" in f for f in result.failures)
