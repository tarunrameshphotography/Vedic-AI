"""Doctrine lookups, resolved entirely through the reference store.

This module is the only path by which classical *content* enters the engine,
and it contains none of it. Every table it serves -- which graha rules which
sign, where each is exalted, how far from the Sun a graha is combust, which
houses a graha aspects -- is read out of `reference` rule cards at load time,
so the answer to "why does the engine believe this?" is always a card id and a
byte-exact quote rather than a Python literal.

That is not fastidiousness. A hardcoded lordship table would make the engine
the authority instead of the books, and a second book that disagrees would
become a code change instead of an encoding one. The rule store exists to stop
exactly that, and a table smuggled into Python would go around it.

Nothing here defaults. A lookup whose doctrine is absent raises, because a
silently-defaulted table is indistinguishable from a sourced one in the output.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class DoctrineError(LookupError):
    """The reference store does not carry the doctrine that was asked for."""


@dataclass(frozen=True)
class Sourced:
    """A doctrinal value and the cards it was read from."""

    value: object
    cards: tuple[str, ...]

    def __iter__(self):
        yield self.value
        yield self.cards


@dataclass
class Doctrine:
    """Typed access to whatever the reference cards say.

    Built once per run from the loaded store. Every accessor records the cards
    it consulted, so an extractor can report its own provenance without having
    to know where the doctrine lives.
    """

    _by_relation: dict[str, list] = field(default_factory=dict)
    consulted: set[str] = field(default_factory=set)

    @classmethod
    def from_cards(cls, cards) -> "Doctrine":
        d = cls()
        for c in cards:
            if c.activation != "reference":
                continue
            rel = (c.predicts or {}).get("relation")
            if rel:
                d._by_relation.setdefault(rel, []).append(c)
        return d

    # --- internals ----------------------------------------------------------

    def _rows(self, relation: str) -> list:
        rows = self._by_relation.get(relation)
        if not rows:
            raise DoctrineError(
                f"no reference card carries the relation {relation!r}; the "
                f"doctrine it needs has not been encoded yet"
            )
        return rows

    def _one(self, relation: str, **match):
        """The single reference card matching a relation and field values."""
        hits = [c for c in self._rows(relation)
                if all(c.predicts.get(k) == v for k, v in match.items())]
        if not hits:
            raise DoctrineError(
                f"no {relation} card for {match}; the store does not say"
            )
        if len(hits) > 1:
            # Two cards answering the same question is a real classical
            # disagreement or an encoding fault. Either way the engine must not
            # pick one; adjudication is Stage 7's job and does not exist yet.
            raise DoctrineError(
                f"{len(hits)} {relation} cards match {match} "
                f"({', '.join(sorted(c.id for c in hits))}); the engine cannot "
                f"choose between authorities"
            )
        self.consulted.add(hits[0].id)
        return hits[0]

    def _all(self, relation: str) -> list:
        rows = self._rows(relation)
        self.consulted.update(c.id for c in rows)
        return rows

    def has(self, relation: str) -> bool:
        return bool(self._by_relation.get(relation))

    # --- lordship -----------------------------------------------------------

    def sign_lord(self, sign: str) -> Sourced:
        c = self._one("sign_lord", sign=sign)
        return Sourced(c.predicts["graha"], (c.id,))

    def signs_ruled_by(self, graha: str) -> Sourced:
        rows = [c for c in self._all("sign_lord") if c.predicts["graha"] == graha]
        return Sourced(tuple(c.predicts["sign"] for c in rows),
                       tuple(sorted(c.id for c in rows)))

    # --- dignity (the encoded half) -----------------------------------------

    def exaltation(self, graha: str) -> Sourced:
        c = self._one("exaltation", graha=graha)
        return Sourced({"exaltation_sign": c.predicts["exaltation_sign"],
                        "debilitation_sign": c.predicts["debilitation_sign"]},
                       (c.id,))

    def deep_exaltation(self, graha: str) -> Sourced:
        c = self._one("deep_exaltation", graha=graha)
        p = c.predicts
        return Sourced({"exaltation_sign": p["exaltation_sign"],
                        "exaltation_degree": p["exaltation_degree"],
                        "debilitation_sign": p["debilitation_sign"],
                        "debilitation_degree": p["debilitation_degree"]},
                       (c.id,))

    def moolatrikona(self, graha: str) -> Sourced:
        c = self._one("moolatrikona", graha=graha)
        return Sourced({"sign": c.predicts["sign"],
                        "portion": c.predicts.get("portion"),
                        "portion_resolved": c.predicts.get("portion_resolved",
                                                           False)},
                       (c.id,))

    def _natural_relationship_row(self, graha: str):
        """The (card, row) carrying *graha*'s own friend/neutral/enemy row.

        Two shapes are both in the store and both are read: a single table
        card keyed by `predicts.table[graha]` (the seven classical grahas,
        vv. 21-22) and a card naming the row directly under `predicts.graha`
        (Rahu and Ketu share one row, v. 35, printed separately because the
        seven-graha table does not cover the nodes at all). Neither shape is
        privileged in code; a graha is read from whichever card names it.
        """
        matches = []
        for c in self._rows("natural_relationship"):
            p = c.predicts
            if "table" in p:
                row = p["table"].get(graha)
                if row is not None:
                    matches.append((c, row))
                continue
            names = p.get("graha")
            names = names if isinstance(names, list) else [names] if names else []
            if graha in names:
                matches.append((c, {k: p.get(k, ()) for k in ("friend", "neutral", "enemy")}))
        if not matches:
            raise DoctrineError(
                f"no natural_relationship row for {graha!r}; the store does "
                f"not say"
            )
        if len(matches) > 1:
            raise DoctrineError(
                f"{len(matches)} natural_relationship cards carry a row for "
                f"{graha!r} ({', '.join(sorted(c.id for c, _ in matches))}); "
                f"the engine cannot choose between authorities"
            )
        return matches[0]

    def natural_relationship(self, graha: str, other: str) -> Sourced:
        """*graha*'s own classification of *other* -- friend, neutral or enemy.

        The seven-graha table recovers intact except for one printed defect:
        the Moon's row lists Mercury under both Friend and Neutral. That is
        not a lookup failure to paper over. Two incompatible answers from the
        same doctrine is exactly the case `_one` already refuses to choose
        between when two cards disagree; a table contradicting itself for one
        cell is the same problem at a smaller grain, and gets the same
        answer: raise rather than pick.

        Absence is not enemy. `other` not appearing in any of the three lists
        happens whenever `other` is `graha` itself -- neither card carries a
        self-relation, because "own sign" is a different dignity this method
        does not duplicate -- and the caller must treat that as no claim
        rather than default to a value.
        """
        card, row = self._natural_relationship_row(graha)
        hits = [k for k in ("friend", "neutral", "enemy") if other in row.get(k, ())]
        if not hits:
            return Sourced(None, (card.id,))
        if len(hits) > 1:
            raise DoctrineError(
                f"{graha} classifies {other} as both {' and '.join(hits)} in "
                f"{card.id}; the printed table contradicts itself there and "
                f"the engine cannot choose between them"
            )
        self.consulted.add(card.id)
        return Sourced(hits[0], (card.id,))

    # --- classifications ----------------------------------------------------

    def sign_attributes(self, sign: str) -> Sourced:
        c = self._one("sign_attributes", sign=sign)
        return Sourced({k: v for k, v in c.predicts.items()
                        if k not in ("relation", "sign")}, (c.id,))

    def house_classes(self) -> Sourced:
        rows = self._all("house_class")
        table: dict[str, list[int]] = {}
        for c in rows:
            table[c.predicts["class"]] = list(c.predicts["houses"])
        return Sourced(table, tuple(sorted(c.id for c in rows)))

    def graha_classes(self) -> Sourced:
        c = self._one("graha_sex")
        table = {k: v for k, v in c.predicts.items() if k != "relation"}
        return Sourced(table, (c.id,))

    def graha_natures(self) -> Sourced:
        """Benefic/malefic status, as every `graha_nature` card states it.

        Read with `_all` rather than `_one` on purpose. The classification is
        printed as two complementary statements -- a verse listing the malefics
        and a note listing the benefics -- so asking for a single card would
        raise on doctrine that is not in conflict at all.

        Each row carries the grahas named outright and the grahas named under a
        condition, because the classification is genuinely not a fixed table:
        the Moon's nature turns on its phase and Mercury's on its company. The
        conditions are structured rather than prose so that the extractor reads
        a value instead of parsing a sentence; the printed wording travels
        alongside in `as_printed` so the encoding can be checked against it.
        """
        rows = self._all("graha_nature")
        out = []
        for c in rows:
            p = c.predicts
            if "nature" not in p:
                raise DoctrineError(
                    f"{c.id}: a graha_nature card must say which nature it "
                    f"classifies"
                )
            out.append({
                "nature": p["nature"],
                "grahas": list(p.get("grahas", ())),
                "conditional": [dict(x) for x in p.get("conditional", ())],
                "card": c.id,
                # Which book said it. Carried so the extractor can attribute
                # each graha's nature to the authority that actually classified
                # it, and record agreement between books as corroboration
                # rather than discarding the second one as a duplicate.
                "book": c.book_id,
            })
        return Sourced(out, tuple(sorted(c.id for c in rows)))

    # --- aspects ------------------------------------------------------------

    def aspect_offsets(self, graha: str) -> Sourced:
        """Houses a graha aspects, counted from itself, and how fully.

        The general table gives every graha a fractional glance at six houses
        and a full one at the seventh. The special table promotes three of
        those fractions to full for Saturn, Jupiter and Mars. Both are read
        from cards; the engine knows neither number.
        """
        gen = self._one("aspect")
        table = {int(k): float(v) for k, v in gen.predicts["table"].items()}
        cards = [gen.id]

        special = self._one("aspect_special")
        for g, houses in special.predicts["full"].items():
            if g == graha:
                for h in houses:
                    table[int(h)] = 1.0
                cards.append(special.id)
        return Sourced(table, tuple(cards))

    # --- combustion ---------------------------------------------------------

    def combustion_source(self) -> Sourced:
        """The body combustion is measured from.

        Read rather than assumed. It is the Sun in every text here, but that is
        doctrine, and a hardcoded "Sun" would be the engine asserting it.
        """
        c = self._one("combustion_orb")
        return Sourced(c.predicts["measured_from"], (c.id,))

    def combustion_orb(self, graha: str, retrograde: bool) -> Sourced:
        """Degrees from the Sun within which a graha is combust.

        Mercury and Venus carry a second, tighter orb when retrograde. A graha
        the table does not name -- the Sun itself, and the nodes -- has no orb,
        and the absence is returned rather than substituted.
        """
        c = self._one("combustion_orb")
        table = c.predicts["table"]
        key = f"{graha}_retrograde"
        if retrograde and key in table:
            return Sourced(table[key], (c.id,))
        if graha in table:
            return Sourced(table[graha], (c.id,))
        return Sourced(None, (c.id,))
