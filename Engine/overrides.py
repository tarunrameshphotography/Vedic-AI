"""Stage 2b: dignity overrides (dep.dignity-override).

Some verses are not claims about a nativity at all; they change the dignity
another card's condition is keyed on. "A retrograde planet produces the same
effect as if exalted" says nothing by itself -- it tells the engine to treat
whichever grahas satisfy *its* condition as exalted wherever dignity is
tested elsewhere. Encoding it as an ordinary card would be the engine
answering "why is this graha exalted?" with the wrong verse.

The mechanism is a small, fixed vocabulary of effect names a `kind: "meta"`
card may declare under `predicts.effect` -- itself no more astrological
content than the `activation` enum already is -- while the condition that
selects the graha, and the graha it selects, remain entirely the card's own.

Every override is gated on the store actually carrying dignity doctrine for
that graha, rather than asserting a state the store is silent about. The
lunar nodes currently have no *single-graha* exaltation card -- three
contradictory authorities are recorded for the pair jointly, in the book that
carries this verse -- so `Doctrine.exaltation` raises for them and this
mechanism never fires there. That is a consequence of what is encoded, not a
graha name written here: if the dispute is ever resolved into a singular
card, the override starts applying to the nodes with no change to this file.
"""

from __future__ import annotations

from .chart import ChartBundle
from .doctrine import Doctrine, DoctrineError
from .facts import Fact, FactSet, chart_frame, make_fact
from .rules import RuleCard, evaluate

# effect name (predicts.effect) -> the dignity it stands in for.
_EFFECTS = {
    "treat_as_exalted": "exalted",
    "treat_as_own_sign": "own",
}


def _grounds(doctrine: Doctrine, graha: str, dignity: str) -> tuple[str, ...] | None:
    """The reference cards that let *this* graha hold *this* dignity, or None.

    None means the store is silent for this graha -- the override must not
    fire, the same silence the ordinary dignity extractor already respects.
    """
    try:
        if dignity == "exalted":
            _, cards = doctrine.exaltation(graha)
            return cards
        if dignity == "own":
            owned, cards = doctrine.signs_ruled_by(graha)
            return cards if owned else None
    except DoctrineError:
        return None
    return None


def apply_overrides(cards: list[RuleCard], doctrine: Doctrine,
                     facts: FactSet, chart: ChartBundle) -> FactSet:
    """Extend the dignity facts per every active dignity-override meta card.

    A meta card is doctrine the engine reads, not a claim about a nativity --
    the same treatment a lordship or exaltation table gets -- so it is
    classified `activation: "reference"` and Stage 6 already never turns a
    reference card into a claim. Its condition is evaluated here instead, and
    each graha it selects gains the overridden dignity fact, so an unrelated
    dignity-conditioned card sees it without being rewritten to know about
    retrogression, vargottama, or whatever selects it.

    Handles single-graha meta cards -- those whose condition binds exactly the
    variable `?g` -- because that is the only shape the corpus has needed so
    far. A meta card written some other way is left alone, not guessed at.
    """
    frame = chart_frame(chart)
    extra: list[Fact] = []
    extra_keys: set[str] = set()

    for card in cards:
        if card.activation != "reference":
            continue
        if card.raw.get("kind") != "meta":
            continue
        predicts = card.raw.get("predicts", {})
        if predicts.get("domain") != "meta":
            continue
        dignity = _EFFECTS.get(predicts.get("effect"))
        if dignity is None:
            continue

        ev = evaluate(card.conditions, facts)
        for solution in ev.solutions:
            graha = solution.as_dict().get("?g")
            if graha is None:
                continue
            grounds = _grounds(doctrine, graha, dignity)
            if grounds is None:
                continue
            key = f"dignity({graha},{dignity})"
            if key in facts or key in extra_keys:
                continue
            extra_keys.add(key)
            extra.append(make_fact(
                "dignity", {"graha": graha, "dignity": dignity}, frame,
                {"basis": f"override by {card.id}", "override_card": card.id,
                 "doctrine": sorted(set(grounds) | {card.id})},
            ))
            facts.doctrine.used("dignity_override", sorted(set(grounds) | {card.id}))

    if not extra:
        return facts
    return FactSet(list(facts) + extra, facts.doctrine)
