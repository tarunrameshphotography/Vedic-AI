"""Tests for Stage 4 -- `dep.strength`, the strong/weak verdict extractor.

The capability under test is deliberately small, and most of these tests are
about keeping it that way. Phaladeepika chapter 4 prints two different criteria
for "strong": verses 22-23 define it as a Shadbala Pinda reaching a per-graha
threshold, and verses 4-5 say "strong" and "weak" outright about conditions a
chart settles. Only the second is computable -- the chapter withholds the
arithmetic for three of the six components the Pinda needs -- so what the engine
emits is the book's verdict on the book's stated grounds, and never a number.

So the assertions that matter most here are the negative ones: that no fact
carries a score, that a component of strength is not read as a verdict, that
retrogression does not make the nodes strong, and that a graha two verses call
strong and weak respectively gets no verdict at all rather than a chosen one.

Run:  python -m pytest Engine/tests -q
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from Engine.chart import SIGNS, BirthRecord, compute_chart, resolve_birth
from Engine.doctrine import Doctrine, DoctrineError
from Engine.ephemeris import SwissEphemerisDLL
from Engine.facts import DoctrineReport, chart_frame, extract_facts, _strength
from Engine.pipeline import run
from Engine.rules import load_cards

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "Rules"

# The five cards verses 4-5 supply, and nothing else may join them without a
# verse that says "strong" or "weak" outright.
VERDICT_CARDS = {
    "PD.04.Strength.Exalted",
    "PD.04.Strength.RetrogradeFive",
    "PD.04.Strength.RetrogradeInDebilitation",
    "PD.04.Weakness.Combust",
    "PD.04.RahuKetu.StrongSigns",
}


def _mumbai(date: str, time: str) -> BirthRecord:
    return BirthRecord(
        date=date, time=time, timezone="Asia/Kolkata",
        latitude=19.0760, longitude=72.8777, place_name="Mumbai",
        time_precision="minute", time_source="memory", sex="male")


# A chart with no strength-conditioned rule firing on it, used throughout as
# the negative control: it is the project's standing demo nativity.
DEMO = BirthRecord(
    date="1987-03-14", time="04:22", timezone="Asia/Kolkata",
    latitude=10.7870, longitude=79.1378, place_name="Thanjavur",
    time_precision="minute", time_source="certificate", sex="male",
)

# Real instants found by scanning, each exercising one newly-released card.
MARS_YOUTHFUL = _mumbai("1986-06-10", "21:15")     # Mars retrograde in the lagna
WEAK_MOON_5 = _mumbai("1985-04-19", "21:15")
LORD7_BENEFIC = _mumbai("1985-01-28", "02:15")
EVEN_SIGNS = _mumbai("1985-01-31", "07:15")
RETRO_COMBUST = _mumbai("1985-03-29", "02:15")     # Mercury retrograde AND combust


@pytest.fixture(scope="module")
def provider():
    return SwissEphemerisDLL()


@pytest.fixture(scope="module")
def cards():
    return load_cards(RULES)


@pytest.fixture(scope="module")
def doctrine(cards):
    return Doctrine.from_cards(cards)


@pytest.fixture(scope="module")
def chart(provider):
    return compute_chart(resolve_birth(DEMO, provider), provider)


@pytest.fixture(scope="module")
def registry():
    with open(RULES / "deferred.json", encoding="utf-8") as fh:
        return json.load(fh)


def place(chart, graha: str, lon: float, retrograde: bool | None = None):
    """The same chart with one body moved to an absolute sidereal longitude.

    Edge cases here are placements, not fixtures: a combust exalted Mars or a
    retrograde debilitated Saturn is a real configuration that simply does not
    occur on any convenient birthday. Moving one body on a real chart keeps
    every other quantity -- the Sun's position, the lagna, the house frame --
    exactly what the ephemeris produced, so what is being tested is the
    extractor and not a hand-built world.
    """
    b = chart.bodies[graha]
    idx = int(lon // 30) % 12
    moved = replace(
        b, lon=lon % 360.0, sign=SIGNS[idx], sign_index=idx,
        deg_in_sign=lon % 30.0,
        retrograde=b.retrograde if retrograde is None else retrograde,
        house=((idx - chart.ascendant_sign_index) % 12) + 1)
    return replace(chart, bodies={**chart.bodies, graha: moved})


def strengths(chart, doctrine) -> dict[str, str]:
    rep = DoctrineReport()
    out = _strength(chart, doctrine, rep, chart_frame(chart))
    return {f.args["graha"]: f.args["strength"] for f in out}


def report_for(chart, doctrine) -> DoctrineReport:
    rep = DoctrineReport()
    _strength(chart, doctrine, rep, chart_frame(chart))
    return rep


# --- doctrine ----------------------------------------------------------------

def test_the_verdicts_come_from_exactly_the_five_cards_that_state_one(doctrine):
    """The doctrine accessor's whole job is this filter.

    `graha_strength` is carried by six cards, and one of them -- the Dik Bala
    table -- quantifies a *component* without reaching a verdict. Reading it as
    one would call the Sun strong on roughly a twelfth of all charts for no
    defensible reason.
    """
    rows, cards = doctrine.graha_strength_verdicts()
    assert set(cards) == VERDICT_CARDS
    assert "PD.04.DikBala.Houses" not in cards
    assert {r["verdict"] for r in rows} == {"strong", "weak"}


def test_every_verdict_names_the_card_book_and_authority_it_came_from(doctrine):
    """Provenance is per verdict, not per extractor run.

    A fact that cited "chapter 4" would be unfalsifiable. Each row has to carry
    the one card that says it, so a claim resting on it can be walked back to a
    byte-exact quote.
    """
    rows, _ = doctrine.graha_strength_verdicts()
    for r in rows:
        assert r["card"] in VERDICT_CARDS
        assert r["book"] == "phaladeepika"
        assert r["authority"] == "Mantreswara"
        assert r["basis"]


def test_the_doctrine_is_read_and_never_hardcoded():
    """Remove the cards and the capability goes with them.

    This is the test that would fail if someone later 'fixed' a gap by writing
    the exaltation or retrogression rule into Python. The engine must have no
    opinion about strength that a card did not give it.
    """
    kept = [c for c in load_cards(RULES) if c.id not in VERDICT_CARDS]
    with pytest.raises(DoctrineError) as exc:
        Doctrine.from_cards(kept).graha_strength_verdicts()
    assert "has not been encoded yet" in str(exc.value)


def test_an_unreadable_condition_raises_rather_than_being_skipped(chart, doctrine):
    """A clause the extractor does not understand must not be dropped.

    Silently ignoring an unrecognised key would let a card fire on a weaker
    condition than it states -- the one failure mode a strength verdict cannot
    be allowed to have. So the extractor refuses the whole run instead, and the
    run reports the extractor as skipped.
    """
    rows, cards = doctrine.graha_strength_verdicts()
    hacked = [{**r, "when": {"phase": "full"}} if r["card"] == "PD.04.Strength.Exalted"
              else r for r in rows]

    class Stub:
        def graha_strength_verdicts(self):
            from Engine.doctrine import Sourced
            return Sourced(hacked, tuple(cards))

        def __getattr__(self, name):
            return getattr(doctrine, name)

    with pytest.raises(DoctrineError) as exc:
        _strength(chart, Stub(), DoctrineReport(), chart_frame(chart))
    assert "does not know how to read" in str(exc.value)


# --- calculation --------------------------------------------------------------

def test_an_exalted_graha_is_strong(chart, doctrine):
    """Verse 5: "All planets are strong when they are posited in their sign of
    exaltation." Saturn's is Libra, per the encoded exaltation table."""
    c = place(chart, "Saturn", 190.0)          # Libra 10, well clear of the Sun
    assert strengths(c, doctrine)["Saturn"] == "strong"


def test_the_verdict_cites_the_card_and_says_it_is_not_a_pinda(chart, doctrine):
    """What a consultation is allowed to claim rests on this evidence block."""
    c = place(chart, "Saturn", 190.0)
    fact = next(f for f in _strength(c, doctrine, DoctrineReport(), chart_frame(c))
                if f.args["graha"] == "Saturn")
    assert fact.evidence["doctrine"] == ["PD.04.Strength.Exalted"]
    assert fact.evidence["authorities"][0]["basis"] == "exalted"
    assert "not a Shadbala Pinda" in fact.evidence["criterion"]


def test_retrogression_alone_makes_the_five_strong(chart, doctrine):
    """Verse 5's second clause, restricted to the five it names.

    Saturn is placed in Gemini deliberately: not its exaltation, not its
    debilitation, not a sign it owns, and far from the Sun. Retrogression is
    then the only thing in the chapter that can produce a verdict, so the
    direct case yielding no verdict and the retrograde case yielding "strong"
    isolates this clause instead of re-testing exaltation.
    """
    direct = place(chart, "Saturn", 75.0, retrograde=False)
    assert "Saturn" not in strengths(direct, doctrine)

    retro = place(chart, "Saturn", 75.0, retrograde=True)
    fact = next(f for f in _strength(retro, doctrine, DoctrineReport(),
                                     chart_frame(retro))
                if f.args["graha"] == "Saturn")
    assert fact.args["strength"] == "strong"
    assert fact.evidence["doctrine"] == ["PD.04.Strength.RetrogradeFive"]


def test_retrogression_does_not_make_the_nodes_strong(chart, doctrine):
    """The card names five grahas and the nodes are not among them.

    Rahu and Ketu are retrograde on every chart ever cast. Reading verse 5 as
    "whatever is retrograde" would hand both of them a permanent strength
    verdict the verse never gives, on every nativity.
    """
    # Move both nodes off the three signs that *do* make Ketu strong, so the
    # only thing that could make them strong here is their retrogression.
    c = place(chart, "Rahu", 100.0)        # Cancer -- strong for Rahu
    c = place(c, "Ketu", 280.0)            # Capricorn -- not in Ketu's list
    assert c.bodies["Ketu"].retrograde is True
    assert "Ketu" not in strengths(c, doctrine)


def test_the_nodes_are_strong_only_in_the_signs_the_table_names(chart, doctrine):
    """Verse 5's own table, and only its whole-sign entries.

    Ketu's "latter half of Sagittarius" and its Parivesha/Indrachapa clause are
    quoted by the card and asserted by nothing; a Ketu in Sagittarius must
    therefore get no verdict here. See concept:ketu-strength-clauses.
    """
    c = place(chart, "Ketu", 340.0)                     # Pisces -- named
    assert strengths(c, doctrine)["Ketu"] == "strong"
    c = place(chart, "Ketu", 260.0)                     # Sagittarius, latter half
    assert "Ketu" not in strengths(c, doctrine)


def test_combustion_makes_a_graha_weak(chart, doctrine):
    """Verse 4, and the one verdict of weakness in the chapter."""
    sun = chart.bodies["Sun"].lon
    c = place(chart, "Saturn", sun + 2.0, retrograde=False)
    assert strengths(c, doctrine)["Saturn"] == "weak"


def test_combustion_overrides_exaltation_because_the_verse_says_so(chart, doctrine):
    """The one piece of ordering logic in Stage 4, and it is the source's.

    Verse 4 prints the override in the same sentence as the weakness -- weak
    "even though he may be posited in his sign of exaltation, in his own or a
    friend's sign" -- so an extractor applying it is following the book rather
    than adjudicating between two cards. The override list travels on the card;
    the engine does not carry it.
    """
    # Put the Sun in Libra and Saturn beside it: Saturn is then exalted AND
    # combust, which no ordinary birthday supplies.
    c = replace(chart, bodies={**chart.bodies,
                               "Sun": replace(chart.bodies["Sun"], lon=190.0,
                                              sign="Libra", sign_index=6,
                                              deg_in_sign=10.0)})
    c = place(c, "Saturn", 191.0, retrograde=False)
    fact = next(f for f in _strength(c, doctrine, DoctrineReport(), chart_frame(c))
                if f.args["graha"] == "Saturn")
    assert fact.args["strength"] == "weak"
    assert fact.evidence["doctrine"] == ["PD.04.Weakness.Combust"]
    overridden = fact.evidence["overridden"]
    assert [o["card"] for o in overridden] == ["PD.04.Strength.Exalted"]


def test_retrograde_in_debilitation_is_strong_when_the_rays_are_unaffected(
        chart, doctrine):
    """Verse 4's rescue clause, with its own not-combust condition."""
    # Saturn is debilitated in Aries. Keep it far from the Sun.
    c = place(chart, "Saturn", 15.0, retrograde=True)
    fact = next(f for f in _strength(c, doctrine, DoctrineReport(), chart_frame(c))
                if f.args["graha"] == "Saturn")
    assert fact.args["strength"] == "strong"
    assert "PD.04.Strength.RetrogradeInDebilitation" in fact.evidence["doctrine"]


def test_a_retrograde_combust_graha_gets_no_verdict_at_all(doctrine, provider):
    """The collision this milestone found by building the extractor.

    Verse 5 says the five non-luminous planets are strong when retrograde, with
    no further condition. Verse 4 says a planet whose rays are eclipsed is weak
    -- and its override list names dignities, not retrogression, so it does not
    settle this case. Choosing between them would be Stage 7 adjudication,
    which does not exist. So the graha gets no strength fact, the collision is
    reported, and every rule conditioning on its strength correctly does not
    fire. Registered as concept:retrograde-combust-collision.

    This is not a corner case: retrograde Mercury and Venus are often combust.
    """
    c = compute_chart(resolve_birth(RETRO_COMBUST, provider), provider)
    assert c.bodies["Mercury"].retrograde is True
    assert "Mercury" not in strengths(c, doctrine)
    partial = report_for(c, doctrine).partial["strength"]
    assert "Mercury is called strong (retrograde) and weak (combust)" in partial
    assert "PD.04.Strength.RetrogradeFive" in partial
    assert "PD.04.Weakness.Combust" in partial


def test_a_graha_the_doctrine_does_not_speak_about_gets_no_verdict(chart, doctrine):
    """Silence is not weakness.

    Nothing in verses 4-5 makes an ordinarily-placed, direct, uncombust graha
    either strong or weak, and the extractor must not fill that in. A default
    would be indistinguishable in the output from a sourced verdict.
    """
    got = strengths(chart, doctrine)
    assert "Sun" not in got and "Mercury" not in got and "Venus" not in got


def test_no_strength_fact_ever_carries_a_number(provider, doctrine):
    """The invariant that keeps Stage 4 from becoming a Shadbala calculator.

    Rupas, Shastyamsas and Pindas are all in the chapter and none of them may
    reach a fact. If a future session computes one, this fails.
    """
    banned = {"pinda", "rupa", "rupas", "shastyamsa", "score", "total", "value"}
    for rec in (DEMO, MARS_YOUTHFUL, WEAK_MOON_5, EVEN_SIGNS):
        c = compute_chart(resolve_birth(rec, provider), provider)
        for f in _strength(c, doctrine, DoctrineReport(), chart_frame(c)):
            assert f.args["strength"] in ("strong", "weak")
            assert not banned & set(f.evidence), f.evidence
            for v in f.evidence.values():
                assert not isinstance(v, (int, float)) or isinstance(v, bool)


def test_the_same_chart_produces_the_same_verdicts_every_time(chart, doctrine):
    """Determinism, asserted rather than assumed.

    The extractor iterates dictionaries and sets internally; a run whose facts
    differed in order or content between calls would make provenance
    unreproducible.
    """
    a = [(f.key, json.dumps(f.evidence, sort_keys=True))
         for f in _strength(chart, doctrine, DoctrineReport(), chart_frame(chart))]
    b = [(f.key, json.dumps(f.evidence, sort_keys=True))
         for f in _strength(chart, doctrine, DoctrineReport(), chart_frame(chart))]
    assert a == b
    assert [k for k, _ in a] == sorted(k for k, _ in a)


def test_strength_survives_the_full_extractor_run(chart, doctrine):
    """The extractor is wired in, not merely importable."""
    fs = extract_facts(chart, doctrine)
    keys = {f.key for f in fs}
    assert "strength(Jupiter,weak)" in keys       # combust on the demo chart
    assert "strength(Ketu,strong)" in keys        # Virgo, per the nodes' table
    assert "strength" in fs.doctrine.consulted


# --- rule activation ----------------------------------------------------------

@pytest.mark.parametrize("record,card_id", [
    (MARS_YOUTHFUL, "PD.02.Form.Mars.Youthful"),
    (WEAK_MOON_5, "PD.10.WeakMoon5.Malefics"),
    (LORD7_BENEFIC, "PD.10.Lord7.BeneficStrong"),
    (EVEN_SIGNS, "PD.10.WifeChildren.EvenSigns"),
])
def test_each_released_card_fires_on_a_real_chart(record, card_id):
    """Every card this milestone activated, shown firing on an actual nativity.

    A card can be made active, pass every structural check, and still never fire
    on any chart because its condition is unsatisfiable -- which is exactly what
    two of these four were before (`lord_of_house(any, 7)` matches no fact,
    because "any" is a literal to the evaluator and not a wildcard). Only a real
    chart shows the difference.
    """
    r = run(record)
    fired = {c.derived["rule_card"] for c in r.claims}
    assert card_id in fired


def test_the_released_claim_cites_the_strength_doctrine_that_supports_it():
    """Provenance end to end: the claim names its card, and the fact that
    satisfied it names the chapter 4 card that produced the verdict."""
    r = run(MARS_YOUTHFUL)
    claim = next(c for c in r.claims
                 if c.derived["rule_card"] == "PD.02.Form.Mars.Youthful")
    assert "strength(Mars,strong)" in claim.derived["conditions_satisfied"]
    fact = next(f for f in claim.derived["facts"]
                if f["key"] == "strength(Mars,strong)")
    assert fact["evidence"]["doctrine"] == ["PD.04.Strength.RetrogradeFive"]
    assert claim.source["chapter"] == 2      # the claim is ch.2's; the fact is ch.4's


def test_no_strength_rule_fires_on_a_chart_that_does_not_qualify():
    """The negative control, and the one that would catch an over-firing card.

    The demo nativity produces strength facts -- Jupiter weak, Ketu strong --
    and still no strength-conditioned rule fires on it, because Mars is neither
    in the lagna nor its lord, the Moon is not in the 5th, and the lord of the
    7th is not a strong benefic. Facts existing is not the same as rules firing.
    """
    r = run(DEMO)
    fired = {c.derived["rule_card"] for c in r.claims}
    assert {f.key for f in r.facts if f.key.startswith("strength(")} == {
        "strength(Jupiter,weak)", "strength(Ketu,strong)"}
    assert not fired & {"PD.02.Form.Mars.Youthful", "PD.10.WeakMoon5.Malefics",
                        "PD.10.Lord7.BeneficStrong", "PD.10.WifeChildren.EvenSigns"}


def test_the_cards_strength_does_not_release_are_still_inert(cards):
    """Four cards named dep.strength and are not freed by it.

    Each is inert for a reason the extractor cannot remove, and each now
    declares the dependency that actually blocks it rather than the one that
    was built. Leaving them declaring dep.strength would have made the backlog
    report them as released.
    """
    by_id = {c.id: c for c in cards}
    still_blocked = {
        "PD.06.Pushkala": {"dep.kendra-togetherness"},
        "PD.01.Kalapurusha.Strength": {"dep.body-part-significator",
                                       "dep.manual-verification"},
        "PD.10.WifeDirection.Strongest": {"dep.strength-ranking"},
    }
    for cid, deps in still_blocked.items():
        card = by_id[cid]
        assert card.activation == "inert", cid
        assert set(card.raw["requires"]) == deps, cid
        assert "dep.strength" not in card.raw["requires"], cid

    dasha = by_id["PD.10.Marriage.StrongerDasha"]
    assert dasha.activation == "inert"
    assert "dep.strength" not in dasha.raw["requires"]
    assert "dep.strength-ranking" in dasha.raw["requires"]


def test_the_superlative_cards_were_not_forced_active(cards):
    """"Strongest" is not "strong", and the difference is the whole reason two
    cards stayed inert while four went active.

    Both of these ask which of several grahas is strongest. The encoded
    doctrine supplies a verdict and no order, so ranking two grahas that are
    both merely strong would be the engine inventing an order the source never
    gives. This asserts the restraint rather than trusting it.
    """
    by_id = {c.id: c for c in cards}
    for cid in ("PD.10.WifeDirection.Strongest", "PD.10.Marriage.StrongerDasha"):
        assert by_id[cid].activation == "inert"
        assert "strength-ranking" in " ".join(by_id[cid].raw["requires"])


# --- source integrity ---------------------------------------------------------

def test_the_pinda_criterion_is_still_recorded_as_the_one_not_implemented(registry):
    """The gap between the two senses of "strong" must stay visible.

    Verses 22-23 are the chapter's formal definition and they are not what this
    engine computes. The entry exists so that is never quietly forgotten, and
    it stays deferred because building the extractor did not close it.
    """
    entry = next(e for e in registry["entries"]
                 if e["id"] == "concept:strength-criterion-scope")
    assert entry["status"] == "deferred"
    assert "vv. 22-23 against vv. 4-5" in entry["locus"]


def test_the_collision_found_by_building_it_is_registered(registry):
    """A finding the encoding pass could not have made.

    Chapter 4 was read card by card in Milestone 21 and signed off. This
    conflict is between two of those cards and only appears on a chart that
    satisfies both, which is why it took an extractor to find it.
    """
    entry = next(e for e in registry["entries"]
                 if e["id"] == "concept:retrograde-combust-collision")
    assert entry["status"] == "deferred"
    assert entry["requires"] == ["dep.adjudication"]


def test_house_strength_is_absent_and_recorded_as_absent(registry, chart, doctrine):
    """Bhava Bala is in the chapter and is not in the engine.

    Its formula runs over the same components whose arithmetic the chapter
    withholds, and its Dik Bala half further needs a Bhava madhya that
    whole-sign houses do not have. So no house gets a strength fact, and the
    gap is written down rather than left to be inferred from an absence.
    """
    from Engine.facts import VOCABULARY
    assert "bhava_strength" not in VOCABULARY
    assert VOCABULARY["strength"] == ("graha", "strength")
    entry = next(e for e in registry["entries"]
                 if e["id"] == "concept:strength-is-not-bhava-strength")
    assert entry["status"] == "deferred"
    facts = _strength(chart, doctrine, DoctrineReport(), chart_frame(chart))
    assert all("house" not in f.args for f in facts)


def test_the_mars_row_that_does_not_add_up_never_reaches_the_engine(doctrine):
    """A printed defect stays a printed defect.

    Chapter 4's other-authorities threshold table has a Mars row that fails to
    sum -- 3-53 against a printed 4-13 -- and it is preserved as printed. The
    protection is structural rather than arithmetic: the thresholds card
    asserts no verdict, so nothing in that table is reachable by the extractor
    at all, and no session can accidentally repair the row by computing with
    it. See concept:mars-bala-pinda-row.
    """
    rows, cards = doctrine.graha_strength_verdicts()
    assert "PD.04.BalaPinda.OtherAuthorities" not in cards
    assert "PD.04.BalaPinda.Thresholds" not in cards
    assert all(not r["table"] or set(r["table"]) <= {"Rahu", "Ketu"} for r in rows)


def test_the_withheld_arithmetic_is_named_as_its_own_standing_blocker(registry):
    """Building the extractor must not look like closing the chapter.

    Four chapter 4 questions turn on component arithmetic the source withholds
    -- Yudha, Chesta, Drig -- and they were declared against dep.strength as a
    proxy for "matters once the strength engine exists". With the engine built
    and deliberately not computing those components, that declaration would
    have made the backlog report all four as released. They are not: no encoded
    book supplies the missing methods. The dependency names that gap instead.
    """
    dep = registry["dependencies"]["dep.shadbala-arithmetic"]
    assert dep["implemented"] is False
    for cid in ("concept:yudha-bala-method-not-given",
                "concept:chesta-bala-manda-definitions",
                "concept:bhava-bala-subtraction-scope",
                "concept:mars-bala-pinda-row"):
        entry = next(e for e in registry["entries"] if e["id"] == cid)
        assert entry["requires"] == ["dep.shadbala-arithmetic"], cid
        assert entry["status"] == "deferred", cid
