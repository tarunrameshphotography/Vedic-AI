# Ephemeris — Swiss Ephemeris Yearly Files

> **Do not process, merge, rename, convert or alter anything in this folder during Phase 1.**
> These files are inputs to the Phase 2 horoscope calculation engine. They are deliberately
> kept as separate yearly files. Nothing here belongs in the `Knowledge/` corpus.

## Inventory

Verified 2026-07-31 (read-only inspection; no file was modified).

| Property | Value |
|---|---|
| Files present | 41 PDFs |
| Distinct years | **40** |
| Year range | **1996 – 2035** |
| Missing years | **None** |
| Total pages | 533 |

Naming follows `ae_<year>d.pdf` (e.g. `ae_2024d.pdf`). Two years break the pattern slightly —
`ae_1998.pdf` and `ae_1999.pdf` carry no `d` suffix — but both are present and correct.

### Known duplicate

`ae_2019d (1).pdf` is **byte-for-byte identical** to `ae_2019d.pdf` (verified by MD5).

It is almost certainly a stray copy from a download. It has been **left in place untouched**,
per the Phase 1 instruction not to modify this folder. When the Phase 2 engine indexes this
directory it should either ignore filenames matching ` (1)` or de-duplicate by checksum, so
that 2019 is not loaded twice.

## Relocation note

At the start of Phase 1 these files were located at `Books/Ephemeris/`, and `ae_2035d.pdf`
was sitting loose in `Books/` alongside the source texts. They were **moved** — not modified —
to this top-level `Ephemeris/` folder so that:

- `Books/` contains only the six classical texts that form the corpus, and
- the ephemeris data sits at the architectural level described in the project README.

File contents and filenames are unchanged.

## Role in the project

Phase 2 will use these tables to compute planetary longitudes for a given birth date, time and
place, producing the rasi chart and the vargas that Phase 3 reasoning will operate on. The
1996–2035 span sets the range of birth dates the engine can serve without additional data.
