# Case study — measuring ingestion completeness across a mixed-office archive

> Worked example behind the [`format-coverage-ledger`](../../skills/format-coverage-ledger/SKILL.md)
> skill and [doc 09](../09-office-formats.md). It quantifies the central claim of
> that skill: **a faithful text/CSV extract is not a complete one**, and the gap
> is largest exactly where the document's value is densest.
>
> **Abstraction note (dogfooding [`public-private-routing`](../../skills/public-private-routing/SKILL.md)).**
> The audited corpus is a private client archive. This case study reports only the
> **method and the aggregate / per-format findings** — no document names, no
> corpus identity, no per-document table. That is abstraction-by-default in
> practice: the lesson is public; the corpus stays private.

## Setup

A mixed-office raw archive — **53 documents** across **docx (5), xlsx (16),
msg (7), pdf (1), pptx (24)** — was ingested into a private wiki via deterministic
**text/CSV-only** lanes (docx→txt, xlsx→csv per sheet with `data_only`, msg→txt
thread, pdf→txt, pptx→txt slide-shape text). Raw binaries were never committed.

The audit asks, per document: **what fraction of the document's information did
that text-only pipeline actually capture?** Each source binary was re-opened with
the same libraries the pipeline used (`python-pptx`, `openpyxl` with and without
`data_only`, `python-docx`, `extract-msg`, `pymupdf`) and a format-specific,
measurable signal/loss proxy was probed directly from the bytes.

## The metric — Ingestion Completeness Score (ICS)

`ICS = 100 · S_text / (S_text + S_lost)`, clamped `[0,100]`, where `S_text`
proxies information the text/CSV extract preserved and `S_lost` proxies what it
dropped. The proxies are deliberately simple and reproducible from the binary
alone:

| Format | `S_text` (captured) | `S_lost` (dropped) |
|---|---|---|
| **pptx** | per slide, text frames + tables, area-weighted | pictures, charts (`×1.5`), text-less autoshapes/freeforms (`×0.5`); speaker-notes penalty |
| **xlsx** | start 100, computed values captured | `−35·formula_density − min(30, 6·charts) − min(12, 3·images)` |
| **docx** | `text_chars` (paragraphs + tables) | `1200 ·` (inline-image count) |
| **msg** | `body_chars` | `Σ max(500, attachment_bytes/4000)` (attachments dropped) |
| **pdf** | text-bearing pages | image-only pages (`−0.15` per mixed page) |

(Tune the weights to your corpus; the point is a *reproducible* per-format number,
not a universal constant.)

## Results

**Overall mean ICS: 63.8%** (n = 53). By format:

| Format | n | mean ICS | dominant loss |
|---|--:|--:|---|
| pdf | 1 | 100.0 | image-only pages |
| msg | 7 | 87.5 | dropped attachments |
| docx | 5 | 83.6 | inline figures |
| **xlsx** | 16 | **56.3** | formula calc-logic, charts |
| **pptx** | 24 | **56.3** | diagrams, charts, speaker notes |

The distribution is sharply bimodal by *what the document is*, not what format it
happens to be:

- **Prose** (meeting minutes, email bodies, executive summaries, a text-born PDF)
  and **pure data tables** (a flat reference list) → **85–100%**. Text extraction
  is genuinely complete here.
- **Diagram-built decks** → **28–56%**. The lowest scorers were slides whose
  entire payload is a single engineering schematic with a title and a copyright
  line; the text dump captured the caption and lost the drawing.
- **Formula + chart spreadsheets** → **42–48%**. A multi-scenario model that is
  ~79% formula cells with 6–13 embedded charts keeps its *frozen values* but loses
  the *calc-logic and the plots* — i.e. the analysis itself.

## The lesson

**ICS runs inverse to document value in this corpus.** The lowest scores were not
junk — they were the highest-value engineering content (the schematics, the
scenario calc-logic). Text-only extraction is weakest precisely where the
information is densest. So the score is **not a grade — it is a prioritized
re-ingest backlog**:

- **pptx (decks):** add slide-image / vision capture + chart-data extraction, and
  pull speaker notes (trivially recoverable, currently dropped).
- **xlsx (models):** capture formulas (`data_only=False`) + chart series.
- **msg:** recurse dropped attachments through the same pipeline.
- **docx / pdf:** mostly complete; add OCR / figure-captioning only for
  image-bearing items.

This is the `format-coverage-ledger` skill's reason to exist: record each lane's
**known loss** against every page so a faithful-but-incomplete extract is marked
`partial` and queued for a richer lane — never silently trusted as complete.

## Reproduce

Score your own corpus by re-opening each source binary with the extraction
libraries and measuring captured-vs-lost signal:

```
uv run --with python-pptx --with openpyxl --with python-docx \
        --with extract-msg --with pymupdf python ics_score.py
```

Run it as a **one-off audit** after a campaign (not per-page): it turns "we
extracted everything" into a measured, ranked statement of what the text/CSV
lanes actually captured.
