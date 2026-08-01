# AI Vedic Astrologer

A long-term project to build an AI capable of interpreting Vedic birth charts in the manner
of an experienced traditional astrologer, grounded strictly in authentic classical texts.

## Project Phases

| Phase | Scope | Status |
|---|---|---|
| **Phase 1** | Build a research-grade digital corpus from the classical source books, and establish the project foundation. | **In progress** |
| Phase 2 | Horoscope calculation engine driven by the Swiss Ephemeris data. | Not started |
| Phase 3 | Retrieval and reasoning layer over the corpus. | Not started |
| Phase 4 | Interpretation and synthesis in traditional astrological voice. | Not started |

## Folder Structure

```
Vedic-AI/
├── Books/        Source PDFs (read-only inputs, never modified)
├── Knowledge/    Converted Markdown — one file per book (the corpus)
├── Ephemeris/    Swiss Ephemeris yearly files, 1996–2035 (Phase 2 input, untouched)
└── Reports/      Conversion and verification reports
```

## Phase 1 Conversion Principles

The corpus is intended as a faithful digital reproduction of the source texts, not a
summary or a modernisation. The governing rules:

- Preserve the original wording exactly. No summarising, rewriting, or modernising.
- Omit nothing. Chapter titles, section titles, verse numbers, Sanskrit (Devanagari),
  transliterations, tables, lists, footnotes and appendices are all retained.
- Remove only page numbers, repeated running headers/footers, and scanning artefacts.
- Correct an OCR error only where the surrounding context makes the correction certain.
- Where text is genuinely unreadable, mark it `[UNCLEAR]` rather than guessing.
- Sanskrit verses are transcribed in Devanagari exactly as printed. Transliteration
  (IAST) is deliberately deferred to a later phase.

## Source Books

| Book | Author | Pages (PDF) | Text layer | Conversion method |
|---|---|---|---|---|
| Brihat Parasara Hora Sastra, Vol. 1 | Maharishi Parashara | 482 | OCR, corrupt | Vision OCR |
| Jataka Parijata, Vol. 1 | Vaidyanatha Dikshita | 324 | OCR, severely corrupt | Vision OCR |
| Phaladeepika | Mantreswara | 265 | Clean digital | Direct extraction |
| Uttara Kalamrita | Kalidasa (tr. P.S. Sastri) | 256 | OCR, corrupt + 75 blank pages | Vision OCR |
| Saravali | Kalyana Varma | 203 | Clean digital | Direct extraction |
| Brihat Jataka | Varahamihira (tr. P.S. Sastri) | 115 spreads / 230 pages | OCR, corrupt | Vision OCR |

See `Reports/conversion_report.md` for per-book conversion status and quality findings.

## A Note on the Ephemeris

`Ephemeris/` holds 40 yearly Swiss Ephemeris files covering 1996–2035. These are inputs to
the Phase 2 calculation engine. They are **not** part of the Phase 1 corpus and must not be
processed, merged, renamed or altered. See `Ephemeris/README.md`.
