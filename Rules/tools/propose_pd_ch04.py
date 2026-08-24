"""Propose the rule cards for Phaladeepika chapter 4 (strengths).

Chapter 4 is not like the chapters encoded before it, and the difference is the
whole reason this proposer exists rather than a hand-typed spec.

The chapter prints **two strength doctrines, by two different authorities**, and
says so itself. Paragraph 1 announces that "before mentioning the view of Shri
Mantreswara, it will be useful to know the views of other ancients", and then
runs eight printed pages of Shastyamsa arithmetic that belongs to those other
ancients -- the same pages name Sripati Padhati, Keshavi Jataka, Brihat Parasara
Hora Shastra and Jataka Padhati as the places to go for the parts it omits.
Only at "Now we come to Shri Mantreswara's views on this subject" do the verses
of Phaladeepika begin, and they state a *different* list of six balas, in a
different order, mostly without numbers.

Encoding the numeric scheme as "what Phaladeepika says about strength" would
therefore attribute to Mantreswara a system the chapter explicitly attributes to
somebody else. So every card here carries `predicts.authority`, exactly as
PD.01.Exaltation.RahuKetu.BPHS already does for a third-party view quoted inside
this translator's Notes, and the two bodies of doctrine never merge.

Why a proposer at all: the chapter is 163 paragraphs of dense numerals, and a
hand-typed quote is a transcription risk on every one of them. Cards here name
their quote by *paragraph index into the chapter*, so the quoted words are
sliced out of the corpus rather than retyped and cannot drift from it. Card
content -- what each passage claims, whether it can be executed, what it is
blocked on -- is authored, not derived.

Usage:  python Rules/tools/propose_pd_ch04.py [--write]

Writes Rules/phaladeepika/ch04.json in *authored* form (quotes as text, no
spans). Run `python Rules/tools/build_chapter.py phaladeepika 4 --write`
afterwards to derive spans, hashes and page anchors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "Knowledge" / "phaladeepika.md"
OUT = ROOT / "Rules" / "phaladeepika" / "ch04.json"

# The chapter's two halves. Paragraph 84 is the sentence that hands over from
# the translator's survey to Mantreswara's verses; everything before it is the
# survey.
HANDOVER_PARA = 84

ANCIENTS = ("other ancients, as reported by the translator (the chapter names "
            "Sripati Padhati, Keshavi Jataka, Brihat Parasara Hora Shastra and "
            "Jataka Padhati by Bhu Deva for the details it omits)")
MANTRESWARA = "Mantreswara"


def paragraphs() -> list[tuple[int, int, str]]:
    """Chapter 4's paragraphs, as (start, end, text) into the corpus string.

    Offsets are into the corpus decoded from bytes, which is what every span in
    the rule store means. Blank-line separated, which is how the converter lays
    the book out.
    """
    text = CORPUS.read_bytes().decode("utf-8")
    lo = text.index("## Chapter 4 — The various kinds of Strengths")
    hi = text.index("## Chapter 5 — Source of livelihood")
    out: list[tuple[int, int, str]] = []
    off = lo
    for block in re.split(r"(?:\r?\n){2,}", text[lo:hi]):
        if not block.strip():
            continue
        i = text.index(block, off)
        out.append((i, i + len(block), block))
        off = i + len(block)
    return out


def quote_for(paras, spec) -> str | list[str]:
    """The exact corpus text a card quotes.

    `paras` as a range is taken *contiguously*, page markers and all, so the
    quote is one uninterrupted stretch of the book even where a sentence runs
    across a page break. build_chapter.py strips the markers from the display
    form, so the reader sees the sentence and the verifier still checks the
    bytes.
    """
    if "text" in spec:
        return spec["text"]
    idx = spec["paras"]
    text = CORPUS.read_bytes().decode("utf-8")
    if isinstance(idx, list) and spec.get("joined"):
        return [text[paras[i][0]:paras[i][1]] for i in idx]
    if isinstance(idx, list):
        return text[paras[idx[0]][0]:paras[idx[-1]][1]]
    return text[paras[idx][0]:paras[idx][1]]


# --- the authored specs -----------------------------------------------------
#
# Each entry: id, paras, verse, tier, predicts, plus optionals. `conditions`
# defaults to the empty conjunction every reference card carries.

REFERENCE = {"all": []}


def ancients(bala: str, **predicts) -> dict:
    return {"relation": "strength_component", "authority": ANCIENTS,
            "bala": bala, **predicts}


# The six-tier Saptavarga table is printed once per varga with the same six
# values. Named rather than repeated so a defect in one row cannot be typed
# differently from the same defect in another.
SAPTAVARGA = {"own": 30, "adhimitra": 22.5, "friend": 15, "neutral": 7.5,
              "enemy": 3.75, "adhishatru": 1.875}
SAPTAVARGA_UNIT = "shastyamsa"

SPECS: list[dict] = []


def add(**spec) -> None:
    SPECS.append(spec)


# =============================================================================
# PART A -- the translator's survey of the views of other ancients (tier 2)
# =============================================================================

add(id="PD.04.Frame.OtherAncients", paras=1, verse="chapter preamble", tier=2,
    predicts={"relation": "authority_frame",
              "authority": ANCIENTS,
              "covers": "chapter 4 paragraphs 1-83 (printed pp.35-42)",
              "handover": "the survey ends at 'Now we come to Shri "
                          "Mantreswara's views on this subject'"},
    activation="reference",
    note="The sentence that makes the rest of the chapter's first eight pages "
         "attributable. Everything from here to the handover is the translator "
         "reporting other authorities' Shadbala scheme, not Mantreswara's "
         "verses -- which matters because that scheme, not Mantreswara's, is "
         "the one carrying the familiar Shastyamsa numbers. Encoded so no "
         "later session can read those numbers as Phaladeepika's own doctrine "
         "without contradicting a card.")

add(id="PD.04.Ancients.SixBalas", paras=[2, 3], verse="chapter preamble", tier=2,
    predicts=ancients("scheme",
                      kinds=["Sthan Bala", "Drik Bala", "Kala Bala",
                             "Chesta Bala", "Naisargik Bala", "Ayana Bala"]),
    activation="reference",
    note="The six-fold scheme as the other ancients order it. Quoted across a "
         "converter artefact: the sentence's tail ('Naisargik Bala, and (6) "
         "Ayana Bala.') was promoted to a markdown heading during conversion, "
         "so the list is split in the corpus although the page prints one "
         "sentence. The span covers both halves. Compare PD.04.SixBalas.Order "
         "-- Mantreswara's own list is a DIFFERENT six: he promotes Uchcha "
         "Bala to a member in its own right and does not count Drik or "
         "Naisargik among the six at all.")

add(id="PD.04.Ancients.Sthana.Uchcha", paras=5, verse="chapter preamble", tier=2,
    predicts=ancients("sthana.uchcha", unit="shastyamsa",
                      at_deep_exaltation=60, at_deep_debilitation=0,
                      interpolation="rule of three"),
    activation="reference",
    note="Uchcha Bala. The engine already carries the deep exaltation and "
         "debilitation degrees as evidence on every dignity fact "
         "(Engine/facts.py::_dignity), so this is the one component of the "
         "numeric scheme whose inputs exist today. It is still not computed: "
         "the scheme it belongs to is another authority's, and no card in the "
         "store asks for a Rupa figure.")

for _pid, _para, _varga in (
    ("Rasi", 6, "rasi"), ("Hora", 7, "hora"), ("Drekkana", 8, "drekkana"),
    ("Saptamsa", [9, 10], "saptamsa"), ("Navamsa", 11, "navamsa"),
    ("Dwadasamsa", 12, "dwadasamsa"), ("Trimsamsa", 13, "trimsamsa"),
):
    _table = dict(SAPTAVARGA)
    _note = (f"Saptavarga Bala, the {_varga} row. One of seven near-identical "
             f"printed paragraphs; the values are the same six-tier ladder "
             f"throughout.")
    if _varga == "rasi":
        _table = {"moolatrikona": 36, **{k: v for k, v in SAPTAVARGA.items()
                                         if k != "own"}}
        _note = ("Saptavarga Bala, the rasi row -- and the one row that breaks "
                 "the pattern: it is keyed on Moolatrikona (36 shastyamsa) "
                 "rather than on 'own sign', and carries no 'own' value at "
                 "all, where the other six rows all begin at 30 for the "
                 "graha's own division. Recorded as printed; the gap is the "
                 "source's, not this card's.")
    if _varga == "saptamsa":
        _note += (" The sentence runs across the p.35/p.36 page break -- its "
                  "last word, 'Adhishatru', is printed on the next page -- so "
                  "the span crosses the page marker.")
    add(id=f"PD.04.Ancients.Sthana.Saptavarga{_pid}", paras=_para,
        verse="chapter preamble", tier=2,
        predicts=ancients("sthana.saptavarga", varga=_varga,
                          unit=SAPTAVARGA_UNIT, table=_table),
        activation="reference", note=_note)

add(id="PD.04.Ancients.Sthana.OjaYugmaRasi", paras=14, verse="chapter preamble",
    tier=2,
    predicts=ancients("sthana.oja_yugma_rasi", unit="shastyamsa", value=15,
                      grahas=["Sun", "Mars", "Mercury", "Saturn"],
                      signs=["Aries", "Gemini", "Leo", "Libra", "Sagittarius",
                             "Aquarius"]),
    activation="reference",
    note="SOURCE DEFECT, confirmed against the printed page (image p0036, "
         "printed p.36): the sentence says 'amongst those five' but names only "
         "four grahas -- the Sun, Mars, Mercury and Saturn. A fifth is missing "
         "from the printed list and the page does not say which. Four are "
         "recorded because four are printed; the fifth is not guessed at. "
         "Registered as concept:oja-yugma-fifth-graha. Note also that the "
         "printed scheme is asymmetric: this rule covers only the odd-sign "
         "case for these grahas and its sibling only the even-navamsa case for "
         "the Moon and Venus, so no rule is printed for the Moon or Venus in "
         "an even *rasi*, nor for these four in an odd *navamsa*.")

add(id="PD.04.Ancients.Sthana.OjaYugmaNavamsa", paras=15,
    verse="chapter preamble", tier=2,
    predicts=ancients("sthana.oja_yugma_navamsa", unit="shastyamsa", value=15,
                      grahas=["Moon", "Venus"],
                      signs=["Taurus", "Cancer", "Virgo", "Scorpio",
                             "Capricorn", "Pisces"]),
    activation="reference",
    note="SOURCE DEFECT in the numbering, confirmed on the printed page: this "
         "paragraph is printed as '(b)', a sub-item of (9), but the list of "
         "Sanskrit names that closes the section counts it as item (10), "
         "'Oja-Yugma navamsa Bala'. There is no paragraph numbered (10) on the "
         "page. Recorded as printed and as item 10 in substance.")

add(id="PD.04.Ancients.Sthana.Kendradi", paras=16, verse="chapter preamble",
    tier=2,
    predicts=ancients("sthana.kendradi", unit="shastyamsa",
                      table={"kendra": 60, "panaphara": 30, "apoklima": 15}),
    activation="reference",
    note="Kendradi Bala. Agrees exactly with Mantreswara's own verse 3 "
         "(PD.04.SthanaBala.Kendradi, 1 / half / quarter Rupa) once Rupas are "
         "converted to Shastyamsa at 60 to the Rupa -- one of the few places "
         "where the chapter's two authorities can be checked against each "
         "other, and they agree. Both are then contradicted by Mantreswara's "
         "own verse 8 (PD.04.SthanaBala.AmongKendras), which does not give "
         "every kendra a full Rupa.")

add(id="PD.04.Ancients.Sthana.Drekkana", paras=[17, 18, 19],
    verse="chapter preamble", tier=2,
    predicts=ancients("sthana.drekkana", unit="shastyamsa", value=15,
                      table={"first": ["Sun", "Mars", "Jupiter"],
                             "second": ["Saturn", "Mercury"],
                             "third": ["Moon", "Venus"]},
                      otherwise="no strength at all"),
    activation="reference",
    note="Dreshtakana Bala, all three printed sub-paragraphs in one span "
         "because they are one table split by typography.")

add(id="PD.04.Ancients.Sthana.Names", paras=[20, 21], verse="chapter preamble",
    tier=2,
    predicts=ancients("sthana.names",
                      names={"1": "Uchcha Bala", "2-8": "Saptavarga Bala",
                             "9": "Oja Yugma Rasi Bala",
                             "10": "Oja-Yugma navamsa Bala",
                             "11": "Kendradi Bala", "12": "Dreshtakana Bala"}),
    activation="reference",
    note="The Sanskrit names of the twelve Sthan Bala components. This is the "
         "card that shows the '(10)' numbering defect above to be a printing "
         "slip rather than a missing rule: the name list counts to twelve and "
         "assigns item 10 to the Oja-Yugma navamsa rule that the body prints "
         "as '(9)(b)'. Split across a converter heading artefact, so the span "
         "covers both halves.")

for _pid, _para, _grahas, _house, _dir, _nil in (
    ("SunMars", 23, ["Sun", "Mars"], 10, "South", 4),
    ("MoonVenus", 24, ["Moon", "Venus"], 4, "North", 10),
    ("MercuryJupiter", 25, ["Mercury", "Jupiter"], 1, "East", 7),
    ("Saturn", 26, ["Saturn"], 7, None, 1),
):
    add(id=f"PD.04.Ancients.DikBala.{_pid}", paras=_para,
        verse="chapter preamble", tier=2,
        predicts=ancients("dik", unit="rupa", full_at_bhava_madhya=_house,
                          nil_at_bhava_madhya=_nil, grahas=_grahas,
                          direction=_dir, interpolation="proportionate"),
        activation="reference",
        note="Directional strength. Two things stop this being computable "
             "today even though the houses are known: it is measured from the "
             "*Bhava madhya* (the house's midpoint), and this chart uses whole "
             "sign houses where a bhava has no midpoint distinct from its "
             "sign; and the value is a proportion between two points, which "
             "nothing in the store asks for. Mantreswara states the same "
             "assignment without the arithmetic in verse 2 "
             "(PD.04.DikBala.Houses), and that one *is* computable. NOTE ON "
             "THE HEADING: the section is printed 'Drik bala (Directional "
             "strength)', but Drik/Drig Bala elsewhere in this same chapter "
             "means strength from *aspect* (PD.04.Ancients.DrigBala). The "
             "chapter uses the two spellings for two different balas; this one "
             "is Dik.")

add(id="PD.04.Ancients.KalaBala.Frame", paras=28, verse="chapter preamble",
    tier=2,
    predicts=ancients("kala", note="an admixture of the kinds below"),
    activation="reference",
    note="Kala Bala is not one measurement but a family; the nine components "
         "that follow are all filed under it, including Yudha Bala, which the "
         "source explicitly calls 'the ninth kind of strength under the "
         "heading Kala Bala'.")

add(id="PD.04.Ancients.KalaBala.Nata.Diurnal", paras=29,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.nata", unit="rupa", grahas=["Sun", "Jupiter", "Venus"],
                      full_at="midnoon", nil_at="midnight",
                      interpolation="proportionate"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.Nata.Nocturnal", paras=30,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.nata", unit="rupa", grahas=["Moon", "Mars", "Saturn"],
                      full_at="midnight", nil_at="midnoon",
                      interpolation="proportionate"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.Nata.Mercury", paras=31,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.nata", unit="rupa", grahas=["Mercury"],
                      full_at="any time during the day time"),
    activation="reference",
    note="Mercury's Nata Bala as printed. Note it is stated for the day only, "
         "where Mantreswara's verse 1 makes Mercury strong through all 24 "
         "hours (PD.04.DayNight.Strength). Recorded, not reconciled.")

add(id="PD.04.Ancients.KalaBala.Paksha.Benefics", paras=32,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.paksha", unit="rupa", of="benefics",
                      full_at="Sun-Moon elongation 180 degrees",
                      nil_at="Sun and Moon together",
                      interpolation="proportionate"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.BeneficList", paras=[33, 34],
    verse="chapter preamble", tier=2,
    predicts={"relation": "kala_bala_benefic", "authority": ANCIENTS,
              "scope": "the Kala Bala computation only",
              "grahas": ["Moon", "Mercury", "Jupiter", "Venus"],
              "dispute": {"Keshavi Jatak": "Mercury with a malefic becomes a "
                                           "malefic",
                          "some Acharyas": "for Kala Bala, Mercury is a "
                                           "benefic",
                          "translator": "supports treating Mercury as a "
                                        "benefic"}},
    activation="reference",
    requires=["dep.strength"],
    note="SCOPED, DELIBERATELY, AND NOT AS GENERAL NATURE DOCTRINE. This is "
         "the sentence Milestone 20 considered and rejected as a source for "
         "the benefic/malefic classification, and the reason is printed in the "
         "next sentence: the passage settles Mercury's treatment 'for "
         "determining kala Bala', in open disagreement with Keshavi Jatak, "
         "which is a scoping statement and not a general one. Read as general "
         "doctrine it would also make the Moon unconditionally benefic and "
         "collide with ch. 2 v. 27's phase rule. The relation is therefore "
         "kala_bala_benefic and never graha_nature; a test "
         "(test_the_kala_bala_benefic_list_is_not_encoded_as_general_nature_"
         "doctrine) fails the build if that is ever changed. Registered as "
         "concept:kala-bala-benefic-scope, which stays deferred: the card "
         "records the definition, but the Kala Bala computation that would "
         "consume it does not exist.")

add(id="PD.04.Ancients.KalaBala.Paksha.Malefics", paras=35,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.paksha", unit="shastyamsa", of="malefics",
                      full_at="Sun and Moon in the same sign and degree",
                      full_value=60,
                      nil_at="Sun-Moon elongation 180 degrees",
                      interpolation="proportionate"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.MaleficList", paras=36,
    verse="chapter preamble", tier=2,
    predicts={"relation": "kala_bala_malefic", "authority": ANCIENTS,
              "scope": "the Kala Bala computation only",
              "grahas": ["Sun", "Mars", "Saturn"]},
    activation="reference",
    requires=["dep.strength"],
    note="The malefic half of the Kala Bala scoping. Unlike its benefic "
         "counterpart it happens to agree with ch. 2 v. 27 and with Brihat "
         "Jataka ch. 2 v. 5 exactly, but it is still filed under "
         "kala_bala_malefic and not graha_nature, because what makes the "
         "benefic half scoped -- being a definition internal to a computation "
         "-- is equally true of this one. Agreement is not a reason to "
         "re-scope a statement.")

add(id="PD.04.Ancients.KalaBala.Paksha.Naming", paras=37,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.paksha", names_as="Paksha Bala",
                      filed_under="Kala Bala"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.Paksha.MoonDoubled", paras=38,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.paksha", graha="Moon", multiplier=2,
                      reason="the Moon is never retrograde and so never gets "
                             "Chesta Bala"),
    activation="reference",
    note="The source gives its own reason for the doubling, which is worth "
         "keeping: it is a compensation for a component the Moon can never "
         "earn. The same argument is made for the Sun's Ayana Bala "
         "(PD.04.Ancients.AyanaBala.SunDoubled).")

add(id="PD.04.Ancients.KalaBala.Tribhaga.Day", paras=39,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.tribhaga", unit="rupa", value=1, period="Dinamana",
                      defined_as="the time between Sunrise and Sunset",
                      thirds={"first": "Mercury", "second": "Sun",
                              "third": "Saturn"}),
    activation="reference",
    note="Named 'Paksha Bala' in the printed text, which cannot be right -- "
         "Paksha Bala is the Sun-Moon elongation component two paragraphs "
         "earlier, and this is the Tribhaga (three-part day) component. "
         "Recorded as printed with the misnomer flagged rather than "
         "silently renamed.")

add(id="PD.04.Ancients.KalaBala.Tribhaga.Night", paras=40,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.tribhaga", unit="rupa", value=1, period="Ratrimana",
                      defined_as="the time between Sunset and Sunrise",
                      thirds={"first": "Moon", "second": "Venus",
                              "third": "Mars"}),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.Tribhaga.Jupiter", paras=41,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.tribhaga", unit="rupa", value=1, graha="Jupiter",
                      period="any time during the 24 hours"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.LordOfYear", paras=42, verse="chapter preamble",
    tier=2,
    predicts=ancients("kala.varsha", unit="shastyamsa", value=15,
                      year_length_days=360, month_length_days=30,
                      lord="the lord of the weekday on which the year begins"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.LordOfMonth", paras=43,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.masa", unit="shastyamsa", value=30,
                      lord="the lord of the weekday on which the month begins"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.LordOfDay", paras=44, verse="chapter preamble",
    tier=2,
    predicts=ancients("kala.dina", unit="shastyamsa", value=45,
                      lord="the lord of the weekday of birth"),
    activation="reference")

add(id="PD.04.Ancients.KalaBala.LordOfHora", paras=45,
    verse="chapter preamble", tier=2,
    predicts=ancients("kala.hora", unit="rupa", value=1,
                      lord="the graha of the hora of birth"),
    activation="reference",
    note="The three lordship components above and this one all need doctrine "
         "the store does not carry: which graha rules each weekday, and the "
         "hora sequence. Neither is stated in this chapter, so neither is "
         "invented here. Registered as dep.weekday-hora-lords.")

add(id="PD.04.Ancients.AyanaBala.Frame", paras=47, verse="chapter preamble",
    tier=2,
    predicts=ancients("ayana",
                      defined_as="declination north or south of the centre "
                                 "line of the sky"),
    activation="reference")

add(id="PD.04.Ancients.AyanaBala.Northern", paras=48, verse="chapter preamble",
    tier=2,
    predicts=ancients("ayana", unit="rupa", grahas=["Sun", "Moon", "Jupiter",
                                                    "Venus"],
                      full_at="24 degrees northern declination",
                      nil_at="24 degrees southern declination",
                      interpolation="proportionate"),
    activation="reference",
    note="SOURCE CONTRADICTION, internal to this section and worth keeping "
         "visible: the Moon is named here as a northern-declination graha and "
         "again in the very next paragraph as a southern one "
         "(PD.04.Ancients.AyanaBala.Southern). Mantreswara's verse 2 "
         "(PD.04.AyanaBala.Course) places the Moon with the southern group, "
         "against this paragraph. Both printed statements are recorded; "
         "neither is dropped to make the pair consistent. Mars is named in "
         "neither paragraph and so has no Ayana Bala rule printed at all.")

add(id="PD.04.Ancients.AyanaBala.Southern", paras=49, verse="chapter preamble",
    tier=2,
    predicts=ancients("ayana", unit="rupa", grahas=["Moon", "Saturn"],
                      full_at="24 degrees southern declination",
                      interpolation="proportionate"),
    activation="reference")

add(id="PD.04.Ancients.AyanaBala.Mercury", paras=50, verse="chapter preamble",
    tier=2,
    predicts=ancients("ayana", unit="shastyamsa", graha="Mercury",
                      at_zero_declination=30, at_24_north=60, at_24_south=60,
                      interpolation="proportionate"),
    activation="reference",
    note="Mercury alone is given a V-shaped rule -- least at zero "
         "declination, full at 24 degrees in either direction -- where every "
         "other graha's Ayana Bala runs monotonically from one pole to the "
         "other.")

add(id="PD.04.Ancients.AyanaBala.SunDoubled", paras=51,
    verse="chapter preamble", tier=2,
    predicts=ancients("ayana", graha="Sun", multiplier=2,
                      reason="the Sun is always direct and never retrograde, "
                             "so gets no Chesta Bala"),
    activation="reference")

add(id="PD.04.Ancients.YudhaBala", paras=53, verse="chapter preamble", tier=2,
    predicts=ancients("kala.yudha",
                      applies_to=["Mars", "Mercury", "Jupiter", "Venus",
                                  "Saturn"],
                      condition="two of them in the same Rasi, degree and "
                                "minute",
                      method_not_given=True,
                      refer_to=["Sripati Padhati", "Keshavi Jataka",
                                "Brihat Parasara Hora Shastra"]),
    activation="reference",
    note="The source states the condition and then declines to give the "
         "method, referring the reader to three other books. Recorded exactly "
         "that way: the condition is encoded, the computation is not, and the "
         "absence is the source's. Registered as "
         "concept:yudha-bala-method-not-given.")

add(id="PD.04.Ancients.ChestaBala.Frame", paras=55, verse="chapter preamble",
    tier=2,
    predicts=ancients("chesta",
                      never_retrograde=["Sun", "Moon"],
                      applies_to=["Mars", "Mercury", "Jupiter", "Venus",
                                  "Saturn"],
                      method_not_given=True,
                      needs=["Mandoucha", "Kshetra", "Kendra"]),
    activation="reference",
    note="The second place the chapter states a component and then withholds "
         "its arithmetic, this time for lack of space. What follows is called "
         "'some information' by the source itself, not the method.")

add(id="PD.04.Ancients.ChestaBala.Values", paras=[56, 63],
    verse="chapter preamble", tier=2,
    predicts=ancients("chesta", unit="shastyamsa",
                      table={"retrograde": 60, "anuvakra": 30, "vikala": 15,
                             "samagama": 30, "manda_direct": 15,
                             "mandatara_direct": 15, "fast_direct": 45,
                             "faster_direct": 30}),
    activation="reference",
    note="SOURCE DEFECT, recorded as printed. The two adjacent motion states "
         "are given the same value (Manda 15, Mandatara 15) while their "
         "printed definitions are mutually inconsistent -- Manda is glossed "
         "'motion be increasing but be less than the medium motion' and "
         "Mandatara 'the motion be decreasing but be more than the medium "
         "motion', which describe overlapping rather than successive states, "
         "and read against their names (slow, slower) look transposed. The "
         "graded ladder they belong to is also non-monotonic as printed: fast "
         "45 but faster 30. No value is corrected and no gloss is swapped; the "
         "reading is registered as concept:chesta-bala-manda-definitions.")

add(id="PD.04.Ancients.NaisargikBala", paras=[65, 66], verse="chapter preamble",
    tier=2,
    predicts=ancients("naisargik", unit="shastyamsa", never_changes=True,
                      table={"Sun": 60, "Moon": 51.3, "Venus": 42.85,
                             "Jupiter": 34.28, "Mercury": 25.70,
                             "Mars": 17.14, "Saturn": 8.57}),
    activation="reference",
    note="The one numeric table in the survey that Mantreswara's own verses "
         "independently corroborate: verse 3 (PD.04.NaisargikBala.Order) gives "
         "the same seven grahas in the same order, Saturn weakest to Sun "
         "strongest, without numbers. Two authorities, one ordering -- and the "
         "agreement is recorded as agreement, not merged into a single "
         "stronger claim.")

add(id="PD.04.Ancients.DrigBala", paras=[68, 69], verse="chapter preamble",
    tier=2,
    predicts=ancients("drig", derived_from="aspect",
                      benefic_aspect="favourable", malefic_aspect="unfavourable",
                      method_not_given=True, refer_to=["Sripati Padhati"]),
    activation="reference",
    note="Aspectual strength -- the bala that the chapter's own heading "
         "spelling collides with, since the directional section eight pages "
         "earlier is headed 'Drik bala'. Third component whose arithmetic the "
         "source declines to give.")

add(id="PD.04.Ancients.BhavaBala.Components", paras=[71, 74],
    verse="chapter preamble", tier=2,
    predicts=ancients("bhava",
                      components=["the strength of the lord of the house",
                                  "the Dik Bala of the house",
                                  "the strength of the benefic aspects"]),
    activation="reference")

for _pid, _para, _klass, _full, _nil in (
    ("Biped", 76, "biped", 1, 7),
    ("Quadruped", 77, "quadruped", 10, 4),
    ("Keeta", 78, "keeta", 7, 1),
    ("Jala", 79, "watery", 4, 10),
):
    add(id=f"PD.04.Ancients.BhavaDikBala.{_pid}", paras=_para,
        verse="chapter preamble", tier=2,
        predicts=ancients("bhava.dik", unit="rupa", sign_class=_klass,
                          full_at_house=_full, nil_at_house=_nil,
                          interpolation="proportionate"),
        activation="reference",
        note="The sign-body classification this depends on is stated in "
             "chapter 1 v. 7 and encoded there as PD.01.SignBodyForm.Table, "
             "which is itself inert -- the mapping from sign to body-form is "
             "not yet queryable reference data. So this rule is blocked on a "
             "table the store holds but cannot read, not on missing doctrine.")

add(id="PD.04.Ancients.BhavaBala.BeneficAspectsExceed", paras=81,
    verse="chapter preamble", tier=2,
    predicts=ancients("bhava.total",
                      when="benefic aspect exceeds malefic aspect",
                      formula="(benefic aspect - malefic aspect) + strength of "
                              "the lord of the house + Bhava Dik Bala"),
    activation="reference",
    note="The printed sentence is genuinely ambiguous about what the "
         "subtraction attaches to: 'deduct quantum of malefic aspect from it "
         "and the strength of the lord of the house and add Bhawa Dik Bala' "
         "can be read as deducting the malefic quantum from the benefic "
         "quantum alone, or from that sum together with the lord's strength. "
         "Its sibling paragraph for the malefic-heavy case is unambiguous and "
         "implies the first reading, which is what is recorded -- and the "
         "ambiguity is registered as concept:bhava-bala-subtraction-scope "
         "rather than treated as settled.")

add(id="PD.04.Ancients.BhavaBala.MaleficAspectsExceed", paras=82,
    verse="chapter preamble", tier=2,
    predicts=ancients("bhava.total",
                      when="malefic aspect exceeds benefic aspect",
                      formula="(strength of the lord of the house + Bhava Dik "
                              "Bala) - (malefic aspect - benefic aspect)"),
    activation="reference")

add(id="PD.04.Ancients.References", paras=83, verse="chapter preamble", tier=2,
    predicts=ancients("references",
                      refer_to=["Jataka Padhati by Bhu Deva", "Keshavi Jataka",
                                "Sripati Padhati"],
                      for_="the quantums of malefic and benefic aspects"),
    activation="reference",
    note="The closing pointer of the survey, and the clearest single statement "
         "of how much of this scheme the chapter does not actually contain.")

# =============================================================================
# PART B -- Mantreswara's verses (tier 1)
# =============================================================================

add(id="PD.04.Frame.Mantreswara", paras=HANDOVER_PARA, verse="4",
    predicts={"relation": "authority_frame", "authority": MANTRESWARA,
              "covers": "chapter 4 verses 1-24 (printed pp.42-50)"},
    activation="reference",
    note="The handover. Everything after this sentence is Phaladeepika's own "
         "text; everything before it is the translator's survey of other "
         "authorities.")

add(id="PD.04.SixBalas.Order", paras=[85, 91], verse="1",
    predicts={"relation": "strength_scheme", "authority": MANTRESWARA,
              "kinds": ["Kala", "Chesta", "Uchcha", "Dik", "Ayana", "Sthana"]},
    activation="reference",
    note="Mantreswara's six balas, and they are NOT the six the survey opened "
         "with. He counts Uchcha Bala as a member in its own right, where the "
         "other ancients fold it in as the first of twelve Sthan Bala "
         "components; and he does not count Drik (aspectual) or Naisargik "
         "(inherent) among the six at all, though he states doctrine about "
         "both elsewhere in the chapter. Anyone implementing 'Phaladeepika's "
         "Shadbala' from the survey's numbers would therefore be implementing "
         "a scheme with a different membership from the one this verse names. "
         "'Kalay or temporal' is printed for 'Kala'; recorded as printed.")

add(id="PD.04.DayNight.Strength", paras=92, verse="1",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "kala.diva_ratri",
              "strong_at_night": ["Mars", "Moon", "Venus"],
              "strong_by_day": ["Sun", "Jupiter", "Saturn"],
              "strong_always": ["Mercury"]},
    activation="reference",
    requires=["dep.day-night"],
    note="Fully stated and not computable: the engine has no sunrise or "
         "sunset, so it cannot say whether a birth was by day or by night. "
         "That is a real gap in the chart layer, not in the doctrine, and it "
         "is registered as dep.day-night rather than approximated -- a "
         "'daytime' guessed from clock hours would silently be wrong near the "
         "poles and at the edges of every timezone. Note Mercury: strong "
         "through all 24 hours here, but strong only by day in the survey's "
         "Nata Bala (PD.04.Ancients.KalaBala.Nata.Mercury).")

add(id="PD.04.Paksha.BeneficMalefic", paras=93, verse="1",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "kala.paksha",
              "benefics_strong_in": "Shukla Paksha (bright half)",
              "malefics_strong_in": "Krishna Paksha (dark half)"},
    activation="reference",
    requires=["dep.paksha"],
    note="Both halves of this are within reach and it is still not executed. "
         "The engine already computes waxing and waning from the Sun-Moon "
         "elongation (Engine/facts.py::_phase) and already classifies grahas "
         "benefic and malefic, so the fortnight and the classification both "
         "exist. What is missing is that no card asks for a paksha predicate, "
         "and this one states a *quantity* of strength rather than a verdict "
         "-- so emitting a fact from it would be building the scoring "
         "framework the project has deliberately not built. Registered as "
         "dep.paksha for whenever a card genuinely needs it.")

add(id="PD.04.LordOfPeriods.Rupas", paras=94, verse="1",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "kala.lordship", "unit": "rupa",
              "table": {"year": 0.25, "month": 0.5, "day": 0.75, "hora": 1.0}},
    activation="reference",
    requires=["dep.weekday-hora-lords"],
    note="Mantreswara's figures for the same four lordships the survey "
         "quantifies in Shastyamsa, and THE TWO DISAGREE ON EVERY ROW. He "
         "gives year 1/4, month 1/2, day 3/4, hora 1 Rupa -- that is 15, 30, "
         "45 and 60 Shastyamsa. The survey gives 15, 30, 45 and 60 too. They "
         "agree exactly. Recorded because the printed word here is 'house' "
         "where the survey and the ascending series both say hora: 'lords of "
         "the year, month, day and house'. Read as 'hora' on the strength of "
         "the series and the survey's parallel paragraph, and that reading is "
         "flagged rather than silently taken -- see "
         "concept:lord-of-house-or-hora.")

add(id="PD.04.ChestaBala.Conditions", paras=95, verse="2",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "chesta",
              "Moon": "when it is full", "Sun": "when on the northern course",
              "others": "when in retrograde motion"},
    activation="reference",
    note="Mantreswara gives the Moon and the Sun a Chesta Bala where the "
         "survey says flatly that neither can ever have one, since neither is "
         "ever retrograde -- and the survey doubles two other components "
         "specifically to compensate for that absence "
         "(PD.04.Ancients.KalaBala.Paksha.MoonDoubled, "
         "PD.04.Ancients.AyanaBala.SunDoubled). This is the sharpest "
         "disagreement between the chapter's two authorities and it is left "
         "standing. The retrograde clause for the other five is the one part "
         "the engine can evaluate, and it is stated again as a verdict in "
         "verse 5, which is where it is executed from "
         "(PD.04.Strength.RetrogradeFive) rather than from here.")

add(id="PD.04.Victorious.NorthNotCombust", paras=96, verse="2",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "uchcha",
              "victorious_when": "in the north and not combust",
              "full_uchcha_bala_when": "in deep exaltation position"},
    activation="reference",
    requires=["dep.declination"],
    note="Half of this is computable and half is not, so none of it is "
         "executed: combustion the engine has, declination it does not. The "
         "deep exaltation clause is the one place Mantreswara himself "
         "quantifies Uchcha Bala, and it agrees with the survey's Uchcha Bala "
         "(PD.04.Ancients.Sthana.Uchcha) on where the maximum sits.")

add(id="PD.04.DikBala.Houses", paras=97, verse="2",
    predicts={"relation": "graha_strength", "authority": MANTRESWARA,
              "bala": "dik", "verdict": None,
              "table": {"Sun": 10, "Mars": 10, "Mercury": 1, "Jupiter": 1,
                        "Saturn": 7, "Moon": 4, "Venus": 4}},
    activation="reference",
    note="Directional strength stated as a house, not as an arc from a bhava "
         "midpoint -- which is why this version is computable where the "
         "survey's (PD.04.Ancients.DikBala.*) is not: a whole-sign chart knows "
         "which house a graha is in. The two agree on all seven assignments. "
         "It is filed as graha_strength but carries verdict null on purpose: "
         "having full Dik Bala is one component of six and is NOT the same as "
         "being strong, so the extractor must not turn this into a strength "
         "verdict. Nothing in the store asks 'has Dik Bala', so no fact is "
         "emitted from it today.")

add(id="PD.04.AyanaBala.Course", paras=98, verse="2",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "ayana", "southern": ["Mercury", "Saturn", "Moon"],
              "northern": "the rest"},
    activation="reference",
    requires=["dep.declination"],
    note="Places the Moon with the southern-course grahas. The survey names "
         "the Moon in BOTH its northern and its southern paragraph "
         "(PD.04.Ancients.AyanaBala.Northern / .Southern), so this verse "
         "agrees with one half of the survey and contradicts the other. The "
         "survey's internal contradiction is the defect; this verse is "
         "consistent.")

add(id="PD.04.SthanaBala.Sources", paras=99, verse="3",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "sthana",
              "from": ["sign of exaltation", "own sign", "friend's sign",
                       "the six vargas"]},
    activation="reference",
    note="Mantreswara names 'the six vargas' where the survey's Saptavarga "
         "Bala counts seven divisions (rasi, hora, drekkana, saptamsa, "
         "navamsa, dwadasamsa, trimsamsa). Recorded as printed; which six is "
         "not stated and is not guessed.")

add(id="PD.04.SthanaBala.Kendradi", paras=100, verse="3",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "sthana.kendradi", "unit": "rupa",
              "table": {"kendra": 1.0, "panaphara": 0.5, "apoklima": 0.25}},
    activation="reference",
    note="Agrees exactly with the survey's Kendradi Bala "
         "(PD.04.Ancients.Sthana.Kendradi) once Rupas are converted at 60 "
         "Shastyamsa to the Rupa. It is contradicted by Mantreswara's own "
         "verse 8 (PD.04.SthanaBala.AmongKendras), which gives the four "
         "kendras four different values rather than one Rupa each -- so a "
         "graha in the 4th house is worth 1 Rupa by this verse and 1/4 Rupa by "
         "that one. Both are recorded and neither is preferred; verse 8 "
         "attributes its version to 'the astrologers', which may or may not "
         "mean Mantreswara is reporting rather than asserting it.")

add(id="PD.04.SexByDegree", paras=101, verse="3",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "sthana.by_degree",
              "table": {"hermaphrodite": [11, 20], "male": [1, 10],
                        "female": [21, 30]}},
    activation="reference",
    requires=["dep.degree-range"],
    note="Both halves exist separately -- the store carries the male / female "
         "/ eunuch classification of the grahas (PD.02, read by "
         "Engine/facts.py::_graha_classes) and every chart carries each "
         "graha's degree within its sign -- but no predicate compares a degree "
         "against a range, so the two cannot be joined. Small and well-scoped; "
         "registered as dep.degree-range. The printed range is '21° to -30°', "
         "with a stray minus sign, and 'hemaphrodite' is printed for "
         "hermaphrodite.")

add(id="PD.04.NaisargikBala.Order", paras=102, verse="3",
    predicts={"relation": "naisargik_order", "authority": MANTRESWARA,
              "weakest_to_strongest": ["Saturn", "Mars", "Mercury", "Jupiter",
                                       "Venus", "Moon", "Sun"]},
    activation="reference",
    note="An ordering without numbers, and it matches the survey's numeric "
         "Naisargik table (PD.04.Ancients.NaisargikBala) rank for rank. This "
         "is the chapter's cleanest cross-authority corroboration and it is "
         "recorded as two authorities agreeing, never as one claim made "
         "twice as strongly. 'Nalsarglk' is printed for Naisargik.")

add(id="PD.04.Strength.RetrogradeInDebilitation", paras=103, verse="4",
    predicts={"relation": "graha_strength", "authority": MANTRESWARA,
              "verdict": "strong", "basis": "retrograde in debilitation",
              "when": {"dignity": "debilitated", "retrograde": True,
                       "not_combust": True}},
    activation="reference",
    requires=["dep.dignity", "dep.combust"],
    note="INTERPRETIVE STEP, FLAGGED FOR SIGN-OFF. The verse's condition is "
         "'if he is retrograde and if his rays are full and brilliant'. 'Rays "
         "full and brilliant' is read here as the complement of combustion, on "
         "the strength of the very next sentence of the same verse, which "
         "defines the opposite state as 'his rays are eclipsed (on account of "
         "being near the Sun)' -- the engine's combustion predicate exactly. "
         "The identification comes from the source's own adjacent gloss and "
         "not from outside, but it is still a reading and it is recorded as "
         "one. If it is wrong, this card over-fires for a retrograde "
         "debilitated graha that is dim for some other reason the text has in "
         "mind. Relationship to PD.09.Retrograde.AsExalted: chapter 9 v. 20 "
         "makes retrogression alone equivalent to exaltation, unconditionally; "
         "this verse conditions the same rescue on the rays as well. Encoded "
         "as `extends` -- the narrower statement -- rather than as a "
         "contradiction, and the pair is registered for a human at "
         "concept:retrograde-rescue-scope.",
    extends=["PD.09.Retrograde.AsExalted"])

add(id="PD.04.Weakness.Combust", paras=104, verse="4",
    predicts={"relation": "graha_strength", "authority": MANTRESWARA,
              "verdict": "weak", "basis": "combust",
              "when": {"combust": True},
              "overrides": ["exalted", "own", "friend"]},
    activation="reference",
    requires=["dep.combust"],
    note="The chapter's one unambiguous statement that a graha IS weak, and "
         "the only one that overrides another verdict: a combust graha is weak "
         "'even though he may be posited in his sign of exaltation, in his own "
         "or a friend's sign or Navamsa'. The override is the source's, "
         "printed in the same sentence, so an extractor applying it is "
         "following the book rather than adjudicating between cards. The verse "
         "then generalises from the Moon to every graha in its own words "
         "('This principle applies to other planets also'), which is what "
         "licenses reading it as a rule about grahas and not about the Moon. "
         "The full-Moon clause -- a debilitated Moon full on Pooran masi night "
         "is strong -- is quoted here and asserted by no card, because the "
         "engine has no fact for the full Moon; see dep.paksha.")

add(id="PD.04.Strength.Exalted", paras=105, verse="5",
    text="5. All planets are strong when they are posited in their sign "
         "of exaltation.",
    predicts={"relation": "graha_strength", "authority": MANTRESWARA,
              "verdict": "strong", "basis": "exalted",
              "when": {"dignity": "exalted"}},
    activation="reference",
    requires=["dep.dignity"],
    note="'All planets are strong when they are posited in their sign of "
         "exaltation' -- a verdict, in the book's own word 'strong', about "
         "every graha, with a condition the engine already computes. This is "
         "the primary warrant for the strength capability existing at all. "
         "The other three clauses of the verse are encoded separately: the "
         "retrograde one as PD.04.Strength.RetrogradeFive, the Sun's Dik Bala "
         "as PD.04.DikBala.Houses (verse 2 states the same thing generally), "
         "and the Moon's Paksha Bala not at all, for want of dep.paksha. "
         "Quotes the verse's first sentence only, so this card and "
         "PD.04.Strength.RetrogradeFive each cite the clause it rests on "
         "rather than sharing the whole verse between them.")

add(id="PD.04.Strength.RetrogradeFive", paras=105, verse="5",
    text="The other five non-luminous planets are strong when they are "
         "retrograde.",
    predicts={"relation": "graha_strength", "authority": MANTRESWARA,
              "verdict": "strong", "basis": "retrograde",
              "grahas": ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"],
              "when": {"retrograde": True}},
    activation="reference",
    requires=[],
    note="'The other five non-luminous planets are strong when they are "
         "retrograde.' The five are named by exclusion of the Sun and Moon, "
         "which the chapter identifies twice as never retrograde "
         "(PD.04.Ancients.ChestaBala.Frame, PD.04.ChestaBala.Conditions), and "
         "the engine asserts the same as a chart invariant. Restricted to "
         "those five explicitly rather than left to 'whatever is retrograde', "
         "because the nodes are retrograde on every chart and this verse is "
         "not about them -- see concept:nodal-retrograde-dignity for the same "
         "question asked of the chapter 9 override. One verse, two independent "
         "verdicts: this card quotes the retrograde clause and "
         "PD.04.Strength.Exalted the exaltation one.")

add(id="PD.04.RahuKetu.StrongSigns", paras=[106, 107], verse="5",
    predicts={"relation": "graha_strength", "authority": MANTRESWARA,
              "verdict": "strong", "basis": "sign",
              "table": {"Rahu": ["Cancer", "Taurus", "Aries", "Aquarius",
                                 "Scorpio"],
                        "Ketu": ["Pisces", "Virgo", "Taurus"]}},
    activation="reference",
    requires=[],
    note="The nodes, which every other strength statement in the chapter "
         "passes over. Two of Ketu's conditions are quoted and not asserted: "
         "'the latter half of Sagittarius', which needs a half-sign predicate "
         "the store does not have, and strength 'in Partvesha and Indrachapa "
         "when the Sun and the Moon are together in the same sign', which "
         "needs the upagraha longitudes computed in this verse's own Notes "
         "(PD.04.Parivesha.Computation) and therefore dep.upagraha. The three "
         "whole signs are recorded; the rest is registered as "
         "concept:ketu-strength-clauses. 'Partvesha' and 'Parivesha' are both "
         "printed for the same upagraha, on the same page.")

add(id="PD.04.Parivesha.Computation", paras=[108, 113], verse="5 (Notes)",
    tier=2,
    predicts={"relation": "upagraha_computation",
              "authority": "Dr. G. S. Kapoor (translator)",
              "steps": ["Dhooma = Sun + 4r 13d 20m",
                        "Vyatipata = Dhooma - 12r",
                        "Parivesha = Vyatipata + 6r",
                        "Indrachapa = Parivesha - 12r"]},
    activation="reference",
    requires=["dep.upagraha"],
    note="The translator's method for the two upagrahas verse 5 names. "
         "Recorded because verse 5 cannot be finished without it, not because "
         "it is executable. THE WORKED EXAMPLE IS DEFECTIVE AS PRINTED and "
         "the defects are the source's, confirmed against the rendered page "
         "(image p0044): step 2 deducts 12 Rasis from a Dhooma of 0-9-31-38, "
         "which is smaller than what is deducted, and the Vyatipata line "
         "subtracts 11-20-28-32 from a figure printed one line above as "
         "11-20-28-22. Preserved as printed rather than repaired; registered "
         "as concept:parivesha-worked-example.")

add(id="PD.04.Lagna.TripedSign", paras=114, verse="6",
    predicts={"relation": "bhava_strength", "authority": MANTRESWARA,
              "house": 1, "unit": "rupa",
              "table": {"triped": 1.0, "Scorpio": 0.25, "any other": 0.5}},
    activation="inert",
    requires=["dep.triped-sign-class"],
    note="AMBIGUOUS AT THE SOURCE, and inert for that reason rather than for a "
         "missing capability. The verse partitions the signs three ways and "
         "names the first class 'triped' -- a category that appears nowhere "
         "else in this book. Chapter 1 v. 7's body-form table "
         "(PD.01.SignBodyForm.Table) classifies signs biped, quadruped, keeta "
         "and watery, with no triped among them, and the survey's own Bhava "
         "Dik Bala earlier in this chapter uses the same four. 'Triped' is "
         "confirmed as the printed word against the rendered page (image "
         "p0044, printed p.44), so it is a defect of the book and not of the "
         "extraction. Whether it is a misprint for 'biped' -- which would make "
         "the verse parallel to the survey's Bhava Dik Bala -- is exactly the "
         "kind of substitution a card must not make on its own. Registered as "
         "dep.triped-sign-class -- the store carries no such class "
         "because the book never gives one.")

add(id="PD.04.Lagna.StrengthOfLord", paras=115, verse="6",
    predicts={"relation": "bhava_strength", "authority": MANTRESWARA,
              "house": 1,
              "equals": "the strength of the lord of the Ascendant",
              "very_powerful_when": [
                  "the lord occupies an Upachaya house (3, 6, 10, 11)",
                  "aspected by its lord, Jupiter or Mercury",
                  "occupied by Venus with no other conjunction or aspect"]},
    activation="reference",
    requires=["dep.lord-of-house", "dep.aspects"],
    note="Encoded as reference and not as a rule, deliberately. 'Very "
         "powerful' is a third degree the chapter never places on the same "
         "scale as its Rupas or its strong/weak verdicts, and inventing a "
         "third value to hold it would be building the scoring framework this "
         "project has not built. The first clause is fully computable today "
         "(lord of the 1st in an upachaya house); it is recorded rather than "
         "fired because what it would assert is a magnitude, not a claim about "
         "the native. The third clause is genuinely under-specified: 'aspected "
         "by its lord Jupiter or Mercury' can be read as a list of three "
         "aspecting bodies or as the lord being one of two named grahas.")

add(id="PD.04.DayNightSigns", paras=116, verse="6",
    predicts={"relation": "bhava_strength", "authority": MANTRESWARA,
              "day_signs_strong_in": "births during day time",
              "night_signs_strong_in": "births during night time"},
    activation="reference",
    requires=["dep.day-night", "dep.sign-class"],
    note="Doubly blocked, and the second block is the interesting one: beyond "
         "having no day/night determination, the store carries no day-sign / "
         "night-sign classification of the twelve rasis at all. The verse "
         "assumes a table the book has not yet given this project.")

add(id="PD.04.SthanaBala.ByDignity", paras=117, verse="7",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "sthana", "unit": "rupa",
              "table": {"exalted": 1.0, "moolatrikona": 0.75, "own": 0.5,
                        "friend": 0.25, "debilitated": 0.0, "combust": 0.0},
              "unquantified": {"enemy": "very little"}},
    activation="reference",
    requires=["dep.dignity", "dep.combust"],
    note="Every input here exists -- the dignity extractor already emits "
         "exalted, moolatrikona, own, friend and debilitated, and combustion "
         "is computed -- and the card is still reference rather than a fact "
         "source, because what it states is a quantity of one component and "
         "not a verdict. The enemy's-sign row is deliberately left in "
         "`unquantified`: 'very little' is not a number and turning it into "
         "one (0.125, say, by continuing the halving) would be inventing "
         "doctrine that reads plausibly. Note the two zero rows: debilitation "
         "and combustion both cancel positional strength entirely, which is "
         "the same doctrine verse 4 states as a verdict and which IS executed, "
         "from PD.04.Weakness.Combust.")

add(id="PD.04.SthanaBala.AmongKendras", paras=118, verse="8",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "sthana.kendra_rank", "unit": "rupa",
              "table": {"1": 1.0, "7": 0.75, "10": 0.5, "4": 0.25},
              "attributed_to": "the astrologers"},
    activation="reference",
    requires=[],
    note="CONTRADICTS PD.04.SthanaBala.Kendradi, three verses earlier in the "
         "same chapter and by the same author: that verse gives every kendra "
         "one Rupa, this one gives the 7th three quarters, the 10th a half and "
         "the 4th a quarter. Both are printed, both are recorded, and the "
         "engine has no way to prefer one -- which is the correct state, not a "
         "gap. The verse hands its own version to 'the astrologers', which may "
         "mean Mantreswara is reporting a distinction rather than asserting "
         "it, and that is precisely the sort of question Stage 7 adjudication "
         "would need to answer and cannot. Registered as "
         "concept:kendra-positional-strength-conflict.",
    contradicts=["PD.04.SthanaBala.Kendradi"])

add(id="PD.04.Aspect.SeventhMostEffective", paras=119, verse="9",
    predicts={"relation": "aspect_preference", "authority": MANTRESWARA,
              "most_effective": "the aspect from the 7th house",
              "in_all_cases": True,
              "dissent": {"who": "some learneds",
                          "claim": "the special aspects of Jupiter (5th, 9th), "
                                   "Mars (4th, 8th) and Saturn (3rd, 10th) are "
                                   "equally competent in all Yogas"}},
    activation="reference",
    note="Bears directly on a table the engine reads every run. "
         "PD.02.Aspect.Special grants Saturn, Jupiter and Mars full drishti on "
         "exactly the six houses this verse names, and Engine/facts.py::"
         "_aspects emits those as full aspects. This verse ranks the 7th-house "
         "aspect above them 'in all cases' and attributes the equal-competence "
         "view to 'some learneds' rather than endorsing it -- so the engine's "
         "current behaviour follows the dissenting opinion, not this verse. "
         "Recorded as `extends` because the verse ranks rather than denies. "
         "Nothing is changed in the extractor on the strength of it: what the "
         "verse asks for is a preference between aspects, which is Stage 7's "
         "job. Registered as concept:special-aspect-parity.",
    extends=["PD.02.Aspect.Special"])

add(id="PD.04.Friendship.NaisargikPreferred", paras=120, verse="10",
    predicts={"relation": "friendship_preference", "authority": MANTRESWARA,
              "prefer": "naisargik (natural)", "over": "tatkalik (temporal)",
              "reason": "the temporal is of changing nature and not permanent"},
    activation="reference",
    note="A verse that ratifies a choice the engine had already made for "
         "engineering reasons: Engine/facts.py::_dignity_friendship reads the "
         "natural friendship table and no temporal one exists. Now there is a "
         "source for the preference. It also names tatkalik friendship as real "
         "doctrine that this project has not encoded -- registered as "
         "concept:tatkalik-friendship.")

add(id="PD.04.Benefics.WardingOffEvil", paras=121, verse="11",
    predicts={"relation": "benefic_potency", "authority": MANTRESWARA,
              "ranking": ["Jupiter", "Venus", "Mercury"],
              "ratios": {"Jupiter": 1.0, "Venus": 0.5, "Mercury": 0.25},
              "Moon": "the foundation of the strength of all the planets"},
    activation="reference",
    note="Ratios rather than quantities: Venus is half of Jupiter and Mercury "
         "half of Venus, with no absolute figure anywhere, so the series can "
         "be ranked but not added to anything. Recorded as reference for that "
         "reason. The closing clause about the Moon is quoted and asserted by "
         "nothing -- 'the foundation of the strength of all the planets' has "
         "no operational reading this project can defend, and guessing one "
         "would be inventing doctrine.")

add(id="PD.04.Chandra.Method", paras=[123, 126], verse="12",
    predicts={"relation": "chandra_method", "authority": MANTRESWARA,
              "input": "Vighatikas elapsed in the birth Nakshatra",
              "divisors": {"Chandrakriya": 60, "Chandra Avastha": 300,
                           "Chandravela": 100},
              "counts": {"Chandrakriya": 60, "Chandra Avastha": 12,
                         "Chandravela": 36}},
    activation="reference",
    requires=["dep.chandra-kriya"],
    note="The chapter's third subject, and it is not strength at all: a "
         "self-contained divination on the elapsed fraction of the birth "
         "nakshatra, yielding 108 numbered effects. It sits between verse 11 "
         "and verse 21 with no connection to the balas on either side. The "
         "method is arithmetically within reach -- the engine already computes "
         "the nakshatra and the pada -- but the printed divisors do not agree "
         "with the printed part-counts: dividing elapsed Vighatikas by 300 "
         "cannot yield a number in 1..12 the way dividing by 60 yields one in "
         "1..60, and the ready-made tables further down divide the "
         "nakshatra's arc rather than any count of Vighatikas. Registered as "
         "dep.chandra-kriya, with the discrepancy at "
         "concept:chandra-divisor-mismatch. The three effect lists are "
         "recorded as reference below so nothing is lost.")

add(id="PD.04.Chandrakriya.Effects", paras=[128, 129], verse="13-15",
    predicts={"relation": "chandra_effects", "authority": MANTRESWARA,
              "kind": "Chandrakriya", "count": 60},
    activation="reference",
    requires=["dep.chandra-kriya"],
    note="All sixty effects, in order, as one reference card rather than sixty "
         "predictive ones. Sixty cards that can never fire would triple this "
         "chapter's card count while adding nothing the store can use; when "
         "dep.chandra-kriya exists they can be split out against a working "
         "index. Registered as concept:chandra-effects-not-predictive. Several "
         "entries are visibly OCR-damaged in the corpus -- '(40) One who falls "
         "down in a Ore' for fire -- and are preserved as extracted.")

add(id="PD.04.ChandraAvastha.Effects", paras=[131, 132], verse="16",
    predicts={"relation": "chandra_effects", "authority": MANTRESWARA,
              "kind": "Chandra Avastha", "count": 12},
    activation="reference",
    requires=["dep.chandra-kriya"])

add(id="PD.04.Chandravela.Effects", paras=[134, 135], verse="17-19",
    predicts={"relation": "chandra_effects", "authority": MANTRESWARA,
              "kind": "Chandravela", "count": 36},
    activation="reference",
    requires=["dep.chandra-kriya"],
    note="Printed '17-10.' for the verse range 17-19. Recorded as printed in "
         "the quote and read as 17-19 in the verse field, since 36 effects "
         "cannot come from a single verse and the neighbouring ranges are "
         "13-15 and 20. Several entries are OCR-damaged ('rating gftee' for "
         "eating ghee, 'anga') and are preserved as extracted.")

add(id="PD.04.Chandra.Tables", paras=[136, 140], verse="16 (Notes)", tier=2,
    predicts={"relation": "chandra_table",
              "authority": "Dr. G. S. Kapoor (translator)",
              "kind": "Chandrakriya", "parts": 60,
              "nakshatra_arc": "13 degrees 20 minutes",
              "part_arc": "13 minutes 20 seconds"},
    activation="reference",
    requires=["dep.chandra-kriya"],
    note="The translator's ready-made table, divided over two printed pages. "
         "It divides the nakshatra's ARC into sixty parts, where verse 12 "
         "divides elapsed VIGHATIKAS by sixty -- the two are the same thing "
         "only if the Moon's motion is taken as uniform, which neither says. "
         "That is the substance of concept:chandra-divisor-mismatch.")

add(id="PD.04.ChandraAvastha.Table", paras=147, verse="16 (Notes)", tier=2,
    predicts={"relation": "chandra_table",
              "authority": "Dr. G. S. Kapoor (translator)",
              "kind": "Chandra Avastha", "parts": 12,
              "part_arc": "1 degree 6 minutes 40 seconds"},
    activation="reference",
    requires=["dep.chandra-kriya"])

add(id="PD.04.Chandravela.Table", paras=150, verse="17-19 (Notes)", tier=2,
    predicts={"relation": "chandra_table",
              "authority": "Dr. G. S. Kapoor (translator)",
              "kind": "Chandravela", "parts": 36,
              "part_arc": "22 minutes 13 seconds 20 thirds"},
    activation="reference",
    requires=["dep.chandra-kriya"],
    note="ARITHMETIC DEFECT in the prose, not in the table. The text says one "
         "part 'will thus come to 13'-13\"-20\"', but 13 degrees 20 minutes "
         "divided by 36 is 22 minutes 13.33 seconds -- and the table's own "
         "first row, 0-22-13-20, gives exactly that. The prose figure is "
         "wrong and the table is right. Recorded as printed. Row (15) reads "
         "5-13-20-0 where the series requires 5-33-20-0, and row (19) reads "
         "6-2-13-20 where it requires 7-2-13-20; both preserved as printed.")

add(id="PD.04.Chandra.UseInPrediction", paras=152, verse="20",
    predicts={"relation": "chandra_method", "authority": MANTRESWARA,
              "applies_to": ["birth", "muhurta", "query"],
              "instruction": "pay particular attention to them before making "
                             "any prediction"},
    activation="reference",
    requires=["dep.chandra-kriya"],
    note="Extends the three Chandra divisions to horary and electional work as "
         "well as natal, which puts part of this passage outside the natal "
         "scope of the engine entirely -- the same boundary that leaves "
         "PD.02.Prashna.ReservoirWater inert under dep.prashna. 'quary' is "
         "printed for query.")

add(id="PD.04.PakshaBala.Importance", paras=153, verse="21",
    predicts={"relation": "strength_component", "authority": MANTRESWARA,
              "bala": "kala.paksha",
              "of_special_importance_to": "the Moon",
              "sthana_bala_of_some_importance_to": "the other planets",
              "additive": True,
              "source_admits_incompleteness": "There are many such types of "
                                              "strength."},
    activation="reference",
    requires=["dep.paksha"],
    note="The chapter's own statement that it is not exhaustive -- 'There are "
         "many such types of strength' -- and the only place it says the "
         "components ADD ('when this strength added to other kinds of strength "
         "of a planet, it will add more strength'). That sentence is the "
         "warrant a numeric Shadbala total would need, and it is the whole of "
         "it: the chapter says the balas add and never says, for Mantreswara's "
         "own six, what any of them is worth in a common unit.")

add(id="PD.04.BalaPinda.Thresholds", paras=[155, 157], verse="22-23",
    predicts={"relation": "strength_threshold", "authority": MANTRESWARA,
              "unit": "rupa",
              "table": {"Sun": 6.5, "Moon": 6.0, "Mars": 5.0, "Mercury": 7.0,
                        "Jupiter": 8.5, "Venus": 5.5, "Saturn": 5.0},
              "below_threshold": "weak"},
    activation="reference",
    requires=["dep.strength"],
    note="THE CHAPTER'S REAL DEFINITION OF STRONG, and the reason the "
         "strength capability built on this chapter is deliberately not a "
         "numeric one. Mantreswara defines a graha as strong when its Shadbala "
         "Pinda reaches these figures and weak below them -- a criterion this "
         "project cannot evaluate, because the six components that would sum "
         "to a Pinda are quantified only in the other authorities' scheme, and "
         "even there three of them (Yudha, Chesta, Drig) have their arithmetic "
         "explicitly withheld. So the strong/weak verdicts the engine does "
         "emit come from verses 4 and 5, which state 'strong' and 'weak' "
         "outright about named conditions, and NOT from this threshold. A "
         "consultation must not imply otherwise. Registered as "
         "concept:strength-criterion-scope.")

add(id="PD.04.BalaPinda.OtherAuthorities", paras=158, verse="23 (Notes)",
    tier=2,
    predicts={"relation": "strength_threshold", "authority": ANCIENTS,
              "unit": "rupa-shastyamsa",
              "components": ["Sthan", "Dik", "Chesta", "Kala", "Ayana"],
              "excludes": "Naisargik Bala, because it is the same in every "
                          "chart",
              "table": {"Sun": {"sthan": "2-45", "dik": "0-35",
                                "chesta": "0-50", "kala": "1-52",
                                "ayana": "0-30", "total": "6-32"},
                        "Moon": {"sthan": "2-13", "dik": "0-50",
                                 "chesta": "0-30", "kala": "1-40",
                                 "ayana": "0-40", "total": "5-53"},
                        "Mars": {"sthan": "1-16", "dik": "0-30",
                                 "chesta": "0-40", "kala": "1-7",
                                 "ayana": "0-20", "total": "4-13"},
                        "Mercury": {"sthan": "2-45", "dik": "0-35",
                                    "chesta": "0-50", "kala": "1-52",
                                    "ayana": "0-30", "total": "6-32"},
                        "Jupiter": {"sthan": "2-45", "dik": "0-35",
                                    "chesta": "0-50", "kala": "1-52",
                                    "ayana": "0-30", "total": "6-32"},
                        "Venus": {"sthan": "2-13", "dik": "0-50",
                                  "chesta": "0-30", "kala": "1-40",
                                  "ayana": "0-40", "total": "5-53"},
                        "Saturn": {"sthan": "1-36", "dik": "0-30",
                                   "chesta": "0-40", "kala": "1-7",
                                   "ayana": "0-20", "total": "4-13"}}},
    activation="reference",
    requires=["dep.strength"],
    note="SOURCE DEFECT: MARS'S ROW DOES NOT ADD UP. Six of the seven rows sum "
         "exactly in Rupas and Shastyamsa at 60 to the Rupa; Mars's does not. "
         "1-16 + 0-30 + 0-40 + 1-7 + 0-20 = 233 Shastyamsa = 3-53, against a "
         "printed total of 4-13. Saturn's row, whose other four cells are "
         "identical to Mars's, carries 1-36 for Sthan and does total 4-13, so "
         "the discrepancy is one digit in one cell and 1-36 would make the row "
         "sum. It is NOT corrected here. The page was rendered and inspected "
         "at the source (image p0050, printed p.50): the table is cleanly laid "
         "out, every column aligns, and 1-16 is what is printed -- so this is "
         "a defect of the book and not of the extraction, and the store's rule "
         "is to preserve those as printed. Registered as "
         "concept:mars-bala-pinda-row. Note also that these totals disagree "
         "substantially with Mantreswara's own (Jupiter 6-32 here against 8.5 "
         "Rupas in verse 22), which the translator's own framing explains only "
         "partly by the exclusion of Naisargik Bala.")

add(id="PD.04.BhavaBala.Formula", paras=159, verse="24",
    predicts={"relation": "bhava_strength", "authority": MANTRESWARA,
              "formula": "1 Rupa + strength of the lord of the bhava + Dik "
                         "Bala of the house + Drig Bala of the house"},
    activation="reference",
    requires=["dep.strength"],
    note="Mantreswara's Bhava Bala, and it differs from the survey's "
         "(PD.04.Ancients.BhavaBala.Components) by the flat 1 Rupa added at "
         "the start, which the survey does not mention. Not computable for the "
         "same reason nothing numeric in this chapter is: two of its three "
         "variable terms are components whose arithmetic the chapter withholds.")

add(id="PD.04.BhavaBala.Notes", paras=160, verse="24 (Notes)", tier=2,
    predicts={"relation": "bhava_strength",
              "authority": "Dr. G. S. Kapoor (translator)",
              "also_count": "association with or aspect from the bhava's lord, "
                            "Jupiter, Venus or Mercury",
              "cross_reference": "verse 6 of this chapter"},
    activation="reference",
    requires=["dep.strength"],
    note="The translator adding a term to Mantreswara's formula, and pointing "
         "at verse 6 for it. Recorded as the translator's, at tier 2, not "
         "folded into the verse's own formula.")


def build() -> dict:
    paras = paragraphs()
    if len(paras) != 163:
        raise SystemExit(
            f"chapter 4 split into {len(paras)} paragraphs, expected 163 -- "
            f"the corpus has changed and every paragraph index in this file "
            f"must be re-checked before it is trusted")
    if not paras[HANDOVER_PARA][2].startswith("Now we come to Shri Mantreswara"):
        raise SystemExit(
            f"paragraph {HANDOVER_PARA} is not the handover sentence; the "
            f"corpus has changed")

    cards = []
    for spec in SPECS:
        entry = {
            "id": spec["id"],
            "verse": spec["verse"],
            "tier": spec.get("tier", 1),
            "quote": quote_for(paras, spec),
            "conditions": spec.get("conditions", REFERENCE),
            "predicts": spec["predicts"],
            "activation": spec.get("activation", "reference"),
        }
        for key in ("note", "requires", "extends", "contradicts", "exclusions"):
            if key in spec:
                entry[key] = spec[key]
        entry.setdefault("exclusions", [])
        entry.setdefault("requires", [])
        cards.append(entry)
    return {"book_id": "phaladeepika", "chapter": 4, "cards": cards}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    doc = build()
    ids = [c["id"] for c in doc["cards"]]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise SystemExit(f"duplicate card ids: {dupes}")

    print(f"proposed {len(doc['cards'])} cards for phaladeepika ch.4")
    tiers = {1: 0, 2: 0}
    for c in doc["cards"]:
        tiers[c["tier"]] += 1
    print(f"  tier 1 (Mantreswara's verses) ......... {tiers[1]}")
    print(f"  tier 2 (translator / other authorities) {tiers[2]}")
    inert = [c["id"] for c in doc["cards"] if c["activation"] == "inert"]
    print(f"  inert ................................. {len(inert)} {inert}")

    if args.write:
        OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)}")
    else:
        print("(dry run; pass --write)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
