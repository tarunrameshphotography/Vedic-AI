"""Deterministic normalisation of Surya output -> clean Markdown building blocks.

Handles the systematic Surya error classes documented in Reports/ocr_engine_benchmark.md:
  1. visarga  ः  emitted as ASCII ':'
  2. double danda ।। emitted as '11' / 'II' / '।।'
  3. <math>..</math> wrappers
  4. <b>..</b> bold tags
  5. hyphenated line breaks
"""
import re

DEVA = r"ऀ-ॿ"
DEVA_RE = re.compile(f"[{DEVA}]")

# Forms Surya emits for a danda / double danda, longest first so that alternation
# never splits a verse number (e.g. "11" as a number vs "11" standing in for ।।).
_DANDA = r"(?:।।|॥|\|\||11|II|ll|।\s*।|1।|।1|।|\|)"


def has_deva(s):
    return bool(DEVA_RE.search(s))


def strip_tags(s):
    s = re.sub(r"</?math>", "", s)
    s = re.sub(r"</?b>", "", s)
    s = re.sub(r"</?i>", "", s)
    s = re.sub(r"</?sub>|</?sup>", "", s)
    return s


def is_bold(s):
    return "<b>" in s


def fix_devanagari(s):
    """Apply Devanagari-specific normalisations only to Devanagari-bearing text."""
    if not has_deva(s):
        return s
    # 1. visarga: ASCII colon directly after a Devanagari letter is a misread visarga
    s = re.sub(f"(?<=[{DEVA}]):", "ः", s)
    # 2. danda runs: Surya renders ।। as '11', 'II', '| |', '।।' inconsistently.
    #    Normalise the verse terminator  <danda><num><danda>  and trailing dandas.
    s = re.sub(r"(?:\|\||11|II|ll|।।|।\s*।)\s*(\d+)\s*(?:\|\||11|II|ll|।।|।\s*।)",
               r"।। \1 ।।", s)
    # 2b. permissive end-of-line pass for the rarer misreads the strict rule above
    #     misses: single danda ।, true double danda ॥ (U+0965), mixed 1। / ।1, and a
    #     stray hyphen between the number and its terminator (e.g. "।। 3-11").
    #     Anchored to end of line, because only there is "<danda> N <danda>"
    #     unambiguously a verse terminator rather than punctuation inside a pada.
    #     Alternatives are explicit tokens, longest first, so a leading/trailing 1 in
    #     the verse number is never mistaken for a danda substitute.
    s = re.sub(rf"{_DANDA}\s*[-–]?\s*(\d{{1,3}})\s*[-–]?\s*{_DANDA}\s*$",
               r" ।। \1 ।।", s)
    s = re.sub(r"\s*(?:\|\||II|।।|॥|।\s*।)\s*$", " ।।", s)
    # single stray pipe after Devanagari -> single danda
    s = re.sub(f"(?<=[{DEVA}])\\s*\\|(?!\\|)", "।", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


VERSE_END = re.compile(r"।।\s*\d+\s*।।\s*$")


def verse_number(s):
    m = VERSE_END.search(s)
    return int(re.search(r"\d+", m.group(0)).group(0)) if m else None


def dehyphenate(lines):
    """Join 'consid-' + 'ered' across printed line breaks."""
    out = []
    for ln in lines:
        if out and re.search(r"[A-Za-z]-$", out[-1]) and re.match(r"^[a-z]", ln):
            out[-1] = out[-1][:-1] + ln
        else:
            out.append(ln)
    return out


def clean_line(s):
    s = strip_tags(s)
    s = fix_devanagari(s)
    return s.strip()
