"""Stage 2: ChartBundle -> FactSet.

Where astronomy becomes vocabulary. Continuous quantities become the discrete
predicates classical rules are written in, and each fact carries the computed
evidence that produced it so Stage 9 can answer "how do you know?" with a
number rather than a restatement.

The vocabulary here is deliberately the minimum the current rule store needs.
Predicates are added when a rule card requires one, never speculatively.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .chart import ChartBundle

# Predicate name -> ordered argument names. A rule card referring to a
# predicate absent from this table is inert and reported, never silently true.
VOCABULARY: dict[str, tuple[str, ...]] = {
    "in_house": ("graha", "house"),
    "in_sign": ("graha", "sign"),
    "in_nakshatra": ("graha", "nakshatra"),
    "retrograde": ("graha",),
    "lagna_sign": ("sign",),
    # Declared because rule cards now require them, not because the extractor
    # can produce them yet. The books lead and the engine follows: a card whose
    # predicate is undeliverable is inert and reported, never silently true.
    "dignity": ("graha", "dignity"),
    "combust": ("graha",),
    "vargottama": ("graha",),
    "lord_of_house": ("graha", "house"),
    "conjunct": ("graha", "other"),
    "aspects": ("graha", "target"),
    "hemmed_between": ("graha", "nature"),
    "in_varga_sign": ("graha", "varga", "sign"),
}


@dataclass(frozen=True)
class Fact:
    key: str
    predicate: str
    args: dict[str, Any]
    frame: dict[str, str]
    evidence: dict[str, Any] = field(default_factory=dict)
    stability: str = "stable"


def _key(predicate: str, args: dict[str, Any]) -> str:
    ordered = VOCABULARY[predicate]
    return f"{predicate}(" + ",".join(str(args[a]) for a in ordered) + ")"


def make_fact(predicate: str, args: dict, frame: dict, evidence: dict | None = None,
              stability: str = "stable") -> Fact:
    if predicate not in VOCABULARY:
        raise KeyError(f"predicate {predicate!r} is not in the vocabulary")
    missing = set(VOCABULARY[predicate]) - set(args)
    if missing:
        raise KeyError(f"{predicate} missing argument(s) {sorted(missing)}")
    return Fact(_key(predicate, args), predicate, args, frame, evidence or {}, stability)


class FactSet:
    """Facts indexed by canonical key.

    Membership is exact-match by design. "Mars in the 7th" and "Mars in the 8th"
    are different keys, and no amount of surface similarity brings them
    together -- which is the whole reason retrieval is keyed on these rather
    than on embeddings.
    """

    def __init__(self, facts: list[Fact]):
        self._by_key: dict[str, Fact] = {f.key: f for f in facts}
        self._facts = facts

    def __contains__(self, key: str) -> bool:
        return key in self._by_key

    def __len__(self) -> int:
        return len(self._facts)

    def __iter__(self):
        return iter(self._facts)

    def get(self, key: str) -> Fact | None:
        return self._by_key.get(key)

    def keys(self) -> list[str]:
        return list(self._by_key)

    def by_predicate(self, predicate: str) -> list[Fact]:
        return [f for f in self._facts if f.predicate == predicate]


def extract_facts(chart: ChartBundle) -> FactSet:
    """Derive every fact the vocabulary can express from this chart."""
    frame = {
        "reference": "lagna",
        "varga": "D1",
        "house_system": chart.houses["system"],
    }
    facts: list[Fact] = [
        make_fact(
            "lagna_sign", {"sign": chart.ascendant_sign}, frame,
            {"ascendant_lon": round(chart.ascendant, 6),
             "deg_in_sign": round(chart.ascendant % 30.0, 6)},
        )
    ]

    for b in chart.bodies.values():
        ev = {
            "lon_sidereal": round(b.lon, 6),
            "sign": b.sign,
            "deg_in_sign": round(b.deg_in_sign, 6),
            "house_system": chart.houses["system"],
            "lagna_sign": chart.ascendant_sign,
        }
        facts.append(make_fact("in_house", {"graha": b.body, "house": b.house}, frame, ev))
        facts.append(make_fact("in_sign", {"graha": b.body, "sign": b.sign}, frame, ev))
        facts.append(make_fact(
            "in_nakshatra", {"graha": b.body, "nakshatra": b.nakshatra}, frame,
            {**ev, "pada": b.pada},
        ))
        if b.retrograde:
            facts.append(make_fact(
                "retrograde", {"graha": b.body}, frame,
                {**ev, "speed_lon": round(b.speed_lon, 6)},
            ))

    return FactSet(facts)
