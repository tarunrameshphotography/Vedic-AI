# Books — source PDFs

**The PDFs themselves are not in version control.** They are scans of published,
in-copyright works: they are inputs to the pipeline, not products of it, and they
are not ours to redistribute. See `.gitignore`.

What *is* committed is everything derived from them: the corpus in `Knowledge/`,
the per-page OCR and hand-verified figure transcriptions under
`Pipeline/books/`, and the rule cards in `Rules/`.

## Expected contents

To re-run the Phase 1 conversion pipeline, place these files here:

| File | Book | Author | PDF pages |
|---|---|---|---|
| `Maharishi_Parashara_-_Brihat_Parasara_Hora_Sastra_(Vol._1).pdf` | Brihat Parasara Hora Sastra, Vol. 1 | Maharishi Parashara | 482 |
| `jataka-parijata-vol-1.pdf` | Jataka Parijata, Vol. 1 | Vaidyanatha Dikshita | 324 |
| `Mantreswara_s__Phaladeeplka_.pdf` | Phaladeepika | Mantreswara, tr. G. S. Kapoor | 265 |
| `uttkalamrita-kalidas-ps-sastri_compress.pdf` | Uttara Kalamrita | Kalidasa, tr. P. S. Sastri | 256 |
| `Saravali.pdf` | Saravali | Kalyana Varma | 203 |
| `Varaha_Mihira_-_Brihat_Jataka.pdf` | Brihat Jataka | Varahamihira, tr. P. S. Sastri | 115 spreads / 230 pages |

Per-book defects and conversion notes are recorded in `Reports/PROJECT_STATUS.md`.

Nothing here is needed to run the Phase 2 reasoning engine, which reads only
`Knowledge/` and `Rules/`.
