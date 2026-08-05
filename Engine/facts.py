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
from .doctrine import DoctrineError

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
    # Classifications, each derived from reference cards rather than declared
    # here. The engine knows the predicate names; the books supply the members.
    "in_sign_class": ("graha", "klass"),
    "house_sign_class": ("house", "klass"),
    "house_class": ("house", "klass"),
    "in_house_class": ("graha", "klass"),
    "graha_class": ("graha", "klass"),
    # Counting, reference frames and nature. `n` is bound by a variable rather
    # than compared against, which is the whole of the arithmetic here: a card
    # asks "how many?" and receives the number the chart produced.
    "occupant_count": ("house", "n"),
    "conjunct_count": ("graha", "n"),
    "in_house_from": ("graha", "reference", "house"),
    "nature": ("graha", "nature"),
    "nature_occupancy": ("house", "nature"),
    "nature_count": ("house", "nature", "n"),
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


class DoctrineReport:
    """What each extractor read, and what it could not.

    Every doctrine-backed extractor names the reference cards it consulted, so
    a fact derived from the books can be walked back to them the same way a
    claim can. An extractor whose doctrine is missing is recorded as skipped
    with the reason, never quietly omitted.
    """

    def __init__(self):
        self.consulted: dict[str, list[str]] = {}
        self.skipped: dict[str, str] = {}
        self.partial: dict[str, str] = {}

    def used(self, extractor: str, cards) -> None:
        got = set(self.consulted.get(extractor, ())) | set(cards)
        self.consulted[extractor] = sorted(got)

    def skip(self, extractor: str, reason: str) -> None:
        self.skipped[extractor] = reason

    def incomplete(self, extractor: str, reason: str) -> None:
        """The doctrine was found, read, and does not cover everything.

        Distinct from `skip`, which means the doctrine is absent altogether. An
        extractor that classifies five of seven grahas has not failed and has
        not succeeded either, and reporting it as either would be false.
        """
        self.partial[extractor] = reason

    @property
    def cards(self) -> list[str]:
        out: set[str] = set()
        for ids in self.consulted.values():
            out.update(ids)
        return sorted(out)

    def to_dict(self) -> dict:
        return {"consulted": dict(self.consulted), "skipped": dict(self.skipped),
                "partial": dict(self.partial), "cards_total": len(self.cards)}


class FactSet:
    """Facts indexed by canonical key.

    Membership is exact-match by design. "Mars in the 7th" and "Mars in the 8th"
    are different keys, and no amount of surface similarity brings them
    together -- which is the whole reason retrieval is keyed on these rather
    than on embeddings.
    """

    def __init__(self, facts: list[Fact], doctrine: DoctrineReport | None = None):
        self._by_key: dict[str, Fact] = {f.key: f for f in facts}
        self._facts = facts
        self.doctrine = doctrine or DoctrineReport()

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


def _sep(a: float, b: float) -> float:
    """Shortest angular separation between two longitudes, in degrees."""
    return abs(((a - b + 180.0) % 360.0) - 180.0)


def _lordship(chart, doc, rep, frame) -> list[Fact]:
    """dep.lord-of-house — which graha rules each house of *this* chart.

    Lordship is a property of a sign; a house has a lord only once the lagna
    fixes which sign it is. Both halves come from the store: the sign in the
    house from the chart, the lord of that sign from a reference card.
    """
    out = []
    for house, sign in enumerate(chart.houses["signs"], start=1):
        graha, cards = doc.sign_lord(sign)
        rep.used("lord_of_house", cards)
        out.append(make_fact(
            "lord_of_house", {"graha": graha, "house": house}, frame,
            {"sign": sign, "house": house, "doctrine": list(cards)},
        ))
    return out


def _sign_classes(chart, doc, rep, frame) -> list[Fact]:
    """dep.sign-class — the attributes of each sign, projected onto the chart.

    Emitted twice over: once per graha, because rules say "the lord of the 7th
    in a dual sign", and once per house, because they also say "the 7th house
    be an even sign".
    """
    out = []
    for house, sign in enumerate(chart.houses["signs"], start=1):
        attrs, cards = doc.sign_attributes(sign)
        rep.used("sign_class", cards)
        for klass in attrs.values():
            out.append(make_fact(
                "house_sign_class", {"house": house, "klass": klass}, frame,
                {"sign": sign, "doctrine": list(cards)},
            ))
    for b in chart.bodies.values():
        attrs, cards = doc.sign_attributes(b.sign)
        rep.used("sign_class", cards)
        for klass in attrs.values():
            out.append(make_fact(
                "in_sign_class", {"graha": b.body, "klass": klass}, frame,
                {"sign": b.sign, "doctrine": list(cards)},
            ))
    return out


def _house_classes(chart, doc, rep, frame) -> list[Fact]:
    """dep.house-class — kendra, trikona, dusthana and the rest."""
    table, cards = doc.house_classes()
    rep.used("house_class", cards)
    out = []
    for klass, houses in table.items():
        for house in houses:
            out.append(make_fact(
                "house_class", {"house": house, "klass": klass}, frame,
                {"doctrine": list(cards)},
            ))
            for b in chart.bodies.values():
                if b.house == house:
                    out.append(make_fact(
                        "in_house_class", {"graha": b.body, "klass": klass},
                        frame, {"house": house, "doctrine": list(cards)},
                    ))
    return out


def _graha_classes(chart, doc, rep, frame) -> list[Fact]:
    """dep.graha-class — the male/female/eunuch classification."""
    table, cards = doc.graha_classes()
    rep.used("graha_class", cards)
    out = []
    for klass, grahas in table.items():
        for graha in grahas:
            if graha in chart.bodies:
                out.append(make_fact(
                    "graha_class", {"graha": graha, "klass": klass}, frame,
                    {"doctrine": list(cards)},
                ))
    return out


def _aspects(chart, doc, rep, frame) -> list[Fact]:
    """dep.aspects — full drishti only, onto houses and onto grahas.

    The texts give every graha a quarter, half and three-quarter glance as well
    as a full one, and three grahas full aspects where others glance partly.
    Only the *full* aspects become facts. That is an engine choice and is
    recorded as one: a rule saying "aspected by a malefic" means full drishti,
    and emitting the fractional glances as `aspects` would make almost every
    such rule true of almost every chart. The fractions are kept in evidence so
    nothing is lost.
    """
    out = []
    for b in chart.bodies.values():
        table, cards = doc.aspect_offsets(b.body)
        rep.used("aspects", cards)
        full = sorted(h for h, strength in table.items() if strength >= 1.0)
        for offset in full:
            target_house = ((b.house - 1 + offset - 1) % 12) + 1
            ev = {"from_house": b.house, "offset": offset,
                  "glance": table[offset], "partial_glances": table,
                  "interpretation": "full drishti only",
                  "doctrine": list(cards)}
            out.append(make_fact(
                "aspects", {"graha": b.body, "target": target_house}, frame, ev))
            for other in chart.bodies.values():
                if other.house == target_house and other.body != b.body:
                    out.append(make_fact(
                        "aspects", {"graha": b.body, "target": other.body},
                        frame, {**ev, "target_house": target_house}))
    return out


def _combustion(chart, doc, rep, frame) -> list[Fact]:
    """dep.combust — within the per-graha orb of the Sun.

    A graha the orb table does not name cannot be combust here. The Sun is
    excluded because the doctrine is stated as distance *from* the Sun, and the
    nodes because the table is silent about them -- silence, not zero.
    """
    out = []
    source, src_cards = doc.combustion_source()
    rep.used("combust", src_cards)
    sun = chart.bodies.get(source)
    if sun is None:
        return out
    for b in chart.bodies.values():
        if b.body == source:
            continue
        orb, cards = doc.combustion_orb(b.body, b.retrograde)
        rep.used("combust", cards)
        if orb is None:
            continue
        gap = _sep(b.lon, sun.lon)
        if gap <= float(orb):
            out.append(make_fact(
                "combust", {"graha": b.body}, frame,
                {"separation_from_sun": round(gap, 6), "orb": orb,
                 "retrograde": b.retrograde, "doctrine": list(cards)},
            ))
    return out


def _dignity(chart, doc, rep, frame) -> list[Fact]:
    """dep.dignity, the encoded half only.

    Exaltation, debilitation, own sign and Moolatrikona are all sourced.
    Natural friendship is not: the table that carries it did not survive the
    scan, so no friendly, neutral or inimical fact is emitted at all rather
    than a guessed one.

    Deep exaltation is a *point*, not a range. The texts give a degree, not an
    orb, so no card asserts "deeply exalted"; the degree and the arc from it
    travel in the evidence of the exaltation fact, where a strength
    calculation can use them without anyone having invented a threshold.
    """
    out = []
    for b in chart.bodies.values():
        try:
            ex, cards = doc.exaltation(b.body)
        except DoctrineError:
            continue                      # the store is silent for this graha
        rep.used("dignity", cards)

        deep = {}
        try:
            deep_val, deep_cards = doc.deep_exaltation(b.body)
            rep.used("dignity", deep_cards)
            deep = deep_val
        except DoctrineError:
            deep_cards = ()

        ev = {"sign": b.sign, "deg_in_sign": round(b.deg_in_sign, 6),
              "doctrine": sorted(set(cards) | set(deep_cards))}
        if b.sign == ex["exaltation_sign"]:
            e = dict(ev)
            if deep:
                e["deep_exaltation_degree"] = deep["exaltation_degree"]
                e["arc_from_deep_point"] = round(
                    abs(b.deg_in_sign - deep["exaltation_degree"]), 6)
            out.append(make_fact("dignity", {"graha": b.body,
                                             "dignity": "exalted"}, frame, e))
        if b.sign == ex["debilitation_sign"]:
            e = dict(ev)
            if deep:
                e["deep_debilitation_degree"] = deep["debilitation_degree"]
                e["arc_from_deep_point"] = round(
                    abs(b.deg_in_sign - deep["debilitation_degree"]), 6)
            out.append(make_fact("dignity", {"graha": b.body,
                                             "dignity": "debilitated"}, frame, e))

        try:
            owned, own_cards = doc.signs_ruled_by(b.body)
        except DoctrineError:
            owned, own_cards = (), ()
        if owned:
            rep.used("dignity", own_cards)
            if b.sign in owned:
                out.append(make_fact(
                    "dignity", {"graha": b.body, "dignity": "own"}, frame,
                    {**ev, "doctrine": sorted(set(ev["doctrine"]) | set(own_cards))}))

        try:
            mt, mt_cards = doc.moolatrikona(b.body)
        except DoctrineError:
            continue
        rep.used("dignity", mt_cards)
        if b.sign == mt["sign"] and mt.get("portion_resolved"):
            span = mt.get("portion") or []
            if len(span) == 2 and float(span[0]) <= b.deg_in_sign <= float(span[1]):
                out.append(make_fact(
                    "dignity", {"graha": b.body, "dignity": "moolatrikona"},
                    frame, {**ev, "portion": span, "doctrine": list(mt_cards)}))
    return out


def _occupant_count(chart, doc, rep, frame) -> list[Fact]:
    """dep.occupant-count — how many grahas occupy each house.

    Several verses are counting rules rather than categorical ones: "as many
    women as the number of planets posited in the 7th house", "the 11th house
    is occupied by two planets". Neither can be written as a membership test.

    The count leaves here as an ordinary predicate argument, so a card asks for
    it with a variable -- `{"occupant_count": {"house": 7, "n": "?n"}}` -- and
    the number arrives in the claim as that variable's binding. There is still
    no arithmetic in the condition language: nothing compares, adds or
    thresholds a count. A card can learn what the number is and say so; it
    cannot compute with it.

    Only houses with at least one occupant are emitted. An empty house would
    bind `?n` to zero and let a counting verse assert something about a chart
    it never addressed -- "the native will associate with 0 women" is not what
    the passage says. The absence is already expressible as `not in_house`.
    """
    tally: dict[int, list[str]] = {}
    for b in chart.bodies.values():
        tally.setdefault(b.house, []).append(b.body)
    out = []
    for house, grahas in sorted(tally.items()):
        out.append(make_fact(
            "occupant_count", {"house": house, "n": len(grahas)}, frame,
            {"grahas": sorted(grahas), "house": house,
             "interpretation": "occupied houses only; an empty house emits no count"},
        ))
    return out


def _graha_frame(chart, doc, rep, frame) -> list[Fact]:
    """dep.graha-frame — houses counted from a graha instead of the lagna.

    "If Mars and Saturn be in the 7th from the Venus and Moon." The lagna is
    only the commonest reference point, not the only one, and a card written in
    another frame cannot be expressed in this one at all.

    Counting is inclusive in the classical manner: the reference graha's own
    sign is the 1st from itself, so the 7th from Venus is six signs on. Under
    whole-sign houses a sign and a house coincide, which is why this is a count
    of signs; it would need restating under any other house system, and the
    frame each fact carries records which one produced it.

    Self-reference is not emitted. `in_house_from(Mars, Mars, 1)` is true of
    every chart ever cast and would say nothing about this one.
    """
    out = []
    for b in chart.bodies.values():
        for ref in chart.bodies.values():
            if b.body == ref.body:
                continue
            house = ((b.sign_index - ref.sign_index) % 12) + 1
            out.append(make_fact(
                "in_house_from",
                {"graha": b.body, "reference": ref.body, "house": house}, frame,
                {"graha_sign": b.sign, "reference_sign": ref.sign,
                 "counting": "inclusive; the reference graha's own sign is the 1st",
                 "house_system": chart.houses["system"]},
            ))
    return out


def _conjunction(chart, doc, rep, frame) -> list[Fact]:
    """dep.conjunct — two grahas in the same sign.

    No card in the store defines conjunction, so the definition used is an
    engine choice and is recorded as one. Same sign is taken as the criterion
    rather than a degree orb, because under whole-sign houses a sign *is* a
    house and the classics speak of grahas "associated" or "posited together"
    in a bhava. The separation in degrees travels in the evidence so a stricter
    reading can be applied later without re-deriving anything.

    Emitted in both directions: association is symmetric, and a card may name
    either graha first.
    """
    out = []
    for a in chart.bodies.values():
        companions = [b for b in chart.bodies.values()
                      if b.body != a.body and b.sign_index == a.sign_index]
        for b in companions:
            out.append(make_fact(
                "conjunct", {"graha": a.body, "other": b.body}, frame,
                {"sign": a.sign, "house": a.house,
                 "separation_deg": round(_sep(a.lon, b.lon), 6),
                 "criterion": "same sign (engine choice; no card defines "
                              "conjunction)"},
            ))
        # "The number of planets that are in conjunction with the lord of the
        # 7th house and Venus" counts companions, and a count is not a
        # membership test. Emitted only where there is at least one, for the
        # same reason the occupant count skips empty houses.
        if companions:
            out.append(make_fact(
                "conjunct_count", {"graha": a.body, "n": len(companions)},
                frame,
                {"sign": a.sign, "house": a.house,
                 "companions": sorted(b.body for b in companions),
                 "criterion": "same sign (engine choice; no card defines "
                              "conjunction)"},
            ))
    return out


def _phase(chart, graha: str, measured_from: str) -> tuple[str | None, dict]:
    """Waxing or waning, from one body's elongation from another.

    Both bodies are named by the card, never here. Which graha has a phase and
    what its phase is measured against are doctrinal facts, and a pair of names
    written into this function would be exactly the smuggled table the rule
    store exists to prevent.

    The arithmetic is ours and the cut at 180 deg is a convention the text does
    not state, so both are recorded. Shukla paksha runs from new to full and
    Krishna paksha from full to new, so the boundary itself counts as waxing.
    """
    body, ref = chart.bodies.get(graha), chart.bodies.get(measured_from)
    if body is None or ref is None:
        return None, {}
    elong = (body.lon - ref.lon) % 360.0
    return ("waxing" if elong < 180.0 else "waning"), {
        "elongation": round(elong, 6),
        "measured_from": measured_from,
        "convention": "waxing for elongation in [0,180), waning in [180,360) "
                      "(engine choice; the text does not state the boundary)",
    }


def _resolve_nature(chart, doc, rep) -> tuple[dict, list[str], tuple[str, ...]]:
    """Each graha's benefic/malefic status, and who could not be classified.

    Resolved in two passes because the doctrine is genuinely layered. A graha
    named outright, or named under a condition on the Moon's phase, is settled
    from the chart alone. Mercury is not: its nature depends on the nature of
    whatever it sits with, so it can only be settled once the others are. Two
    passes are enough because nothing Mercury's clause depends on depends in
    turn on Mercury.
    """
    rows, cards = doc.graha_natures()
    rep.used("nature", cards)

    companions: dict[str, list[str]] = {}
    for a in chart.bodies.values():
        companions[a.body] = sorted(
            b.body for b in chart.bodies.values()
            if b.body != a.body and b.sign_index == a.sign_index)

    resolved: dict[str, tuple[str, dict]] = {}

    def settle(graha: str, nature: str, evidence: dict) -> None:
        prior = resolved.get(graha)
        if prior and prior[0] != nature:
            # Two cards making a graha both benefic and malefic is a real
            # disagreement or an encoding fault. Either way the engine must not
            # pick; Stage 7 adjudication does not exist yet.
            raise DoctrineError(
                f"the reference store makes {graha} both {prior[0]} and "
                f"{nature}; the engine cannot choose between authorities"
            )
        resolved[graha] = (nature, evidence)

    deferred = []
    for row in rows:
        nature = row["nature"]
        for graha in row["grahas"]:
            if graha in chart.bodies:
                settle(graha, nature, {"basis": "named outright by the text"})
        for cond in row["conditional"]:
            graha, when = cond["graha"], cond["when"]
            if graha not in chart.bodies:
                continue
            if "phase" in when:
                if "measured_from" not in when:
                    raise DoctrineError(
                        f"a phase condition on {graha} does not say what the "
                        f"phase is measured from; the engine will not assume it"
                    )
                phase, phase_ev = _phase(chart, graha, when["measured_from"])
                if phase is not None and when["phase"] == phase:
                    settle(graha, nature,
                           {"basis": f"phase is {phase}",
                            "as_printed": cond.get("as_printed", ""), **phase_ev})
            elif "associated_with" in when or "not_associated_with" in when:
                deferred.append((graha, nature, cond))
            else:
                raise DoctrineError(
                    f"graha_nature condition {sorted(when)} is not one the "
                    f"extractor knows how to read"
                )

    for graha, nature, cond in deferred:
        when = cond["when"]
        wanted = when.get("associated_with") or when.get("not_associated_with")
        keep = "associated_with" in when
        with_them = [o for o in companions.get(graha, ())
                     if resolved.get(o, (None,))[0] == wanted]
        if bool(with_them) is keep:
            settle(graha, nature, {
                "basis": ("associated with " if keep else "not associated with ")
                         + wanted,
                "as_printed": cond.get("as_printed", ""),
                "companions": companions.get(graha, []),
                "companions_of_that_nature": with_them,
            })

    unclassified = sorted(set(chart.bodies) - set(resolved))
    return resolved, unclassified, cards


def _nature(chart, doc, rep, frame) -> list[Fact]:
    """dep.nature — benefic or malefic, entirely as the cards state it.

    The classification is not a table. Verse 27 names five grahas outright, the
    Moon by its phase and Mercury by its company, and the extractor reads all
    three shapes rather than flattening them.

    What it will not do is complete the list. Jupiter and Venus are named by
    neither the verse nor its note, so no fact is emitted for them and every
    rule about benefics under-fires until the chapter that does name them is
    encoded. Inferring "not listed as malefic, therefore benefic" would put the
    engine's own reasoning where a citation belongs.
    """
    resolved, unclassified, cards = _resolve_nature(chart, doc, rep)
    if unclassified:
        rep.incomplete(
            "nature",
            f"the encoded doctrine does not classify {', '.join(unclassified)}; "
            f"no nature fact is emitted for them and rules about benefics "
            f"under-fire accordingly")
    out = []
    for graha, (nature, ev) in sorted(resolved.items()):
        out.append(make_fact(
            "nature", {"graha": graha, "nature": nature}, frame,
            {**ev, "doctrine": list(cards)},
        ))
    return out


def _nature_occupancy(chart, doc, rep, frame) -> list[Fact]:
    """dep.nature-occupancy — houses holding grahas of a given nature.

    "The number of women who will die will be equal to the number of malefics";
    "if the 7th be occupied by malefics". Both need nature and house together,
    and a count as well as a membership test, so both are emitted.

    Only natures actually present in a house are emitted, for the same reason
    the occupant count skips empty houses: a zero here would let a verse about
    malefics afflicting a house speak about a house no malefic touches.
    """
    resolved, _, cards = _resolve_nature(chart, doc, rep)
    rep.used("nature_occupancy", cards)
    tally: dict[tuple[int, str], list[str]] = {}
    for b in chart.bodies.values():
        got = resolved.get(b.body)
        if got is None:
            continue
        tally.setdefault((b.house, got[0]), []).append(b.body)

    out = []
    for (house, nature), grahas in sorted(tally.items()):
        ev = {"grahas": sorted(grahas), "house": house, "nature": nature,
              "doctrine": list(cards)}
        out.append(make_fact(
            "nature_occupancy", {"house": house, "nature": nature}, frame, ev))
        out.append(make_fact(
            "nature_count", {"house": house, "nature": nature,
                             "n": len(grahas)}, frame, ev))
    return out


EXTRACTORS = (
    ("lord_of_house", _lordship),
    ("sign_class", _sign_classes),
    ("house_class", _house_classes),
    ("graha_class", _graha_classes),
    ("aspects", _aspects),
    ("combust", _combustion),
    ("dignity", _dignity),
    ("occupant_count", _occupant_count),
    ("graha_frame", _graha_frame),
    ("conjunct", _conjunction),
    ("nature", _nature),
    ("nature_occupancy", _nature_occupancy),
)


def extract_facts(chart: ChartBundle, doctrine=None) -> FactSet:
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

    # Doctrine-backed facts. Each extractor reads reference cards and records
    # which ones; an extractor whose doctrine is absent is reported as skipped
    # rather than silently producing nothing.
    report = DoctrineReport()
    if doctrine is not None:
        for name, fn in EXTRACTORS:
            try:
                facts.extend(fn(chart, doctrine, report, frame))
            except DoctrineError as exc:
                report.skip(name, str(exc))

    return FactSet(facts, report)
