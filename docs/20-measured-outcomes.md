# Measured Outcomes: Completion & Success Statistics

**Read this before adopting the playbook.** Every other doc tells you *how* the
pipeline works; this one tells you *what it actually achieved*, measured from the
live campaigns the playbook is distilled from. The honest headline:

> **Extraction is fast and near-total. Verification is the bottleneck and the
> budget.** After months of operation and 80+ vision-verification batches, ~10%
> of extracted tables are verified or rejected — and that is the *expected* shape
> of this work, not a failure of it. Plan your corpus, staffing, and promises
> around the verification rate, not the extraction rate.

All numbers are snapshots **as of 2026-06-10** from the two source campaigns:

- **Campaign A** — a private engineering-standards wiki: published PDF standards
  (ISO, API, DNV, NORSOK, …) → markdown pages + per-table CSVs, with the
  provisional→verified lifecycle of [doc 03](03-verification-playbook.md).
- **Campaign B** — a confidential project-archive ingestion: live Office formats
  (docx/xlsx/msg/pptx/pdf) → source-extract wiki pages, scored by ICS
  (information-coverage share: what fraction of the document's information the
  text/CSV lane captured). Tracked publicly as
  [issue #33](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/33).

Both corpora are private; everything below is aggregate statistics only.

## Campaign A — PDF standards, table lane

### Scale and completion

| Metric | Value |
|---|--:|
| Source documents processed (distinct standards) | 696 |
| Candidate tables queued | 23,147 |
| Tables resolved (verified **or** rejected) | 2,275 (**9.8%**) |
| — verified (cell-faithful, promoted) | 1,207 (53% of resolved) |
| — rejected (not a faithful table) | 1,068 (47% of resolved) |
| Still provisional / awaiting verification | 20,872 (90.2%) |

### Per-document completion

Completion is extremely head-heavy: verification effort was *prioritized by
content value*, not spread evenly.

| Share of a document's tables resolved | Documents | % of 696 |
|---|--:|--:|
| 100% (fully resolved) | 14 | 2.0% |
| 75–99% | 5 | 0.7% |
| 50–74% | 19 | 2.7% |
| 25–49% | 45 | 6.5% |
| under 25% (overwhelmingly 0%) | 613 | 88.1% |

If you need a number for planning: expect **~2% of documents fully resolved and
~12% partially resolved** at the point where the verified subset already serves
most real queries. Full-corpus verification is a long-tail program, not a
prerequisite for usefulness — verbatim clause extracts and honest provisional
labeling carry the rest (doc 03).

### Success rate by structural triage class

The mechanical extractor triages every table before any vision model sees it
(`ok` / `flagged` / `no-csv`). That triage is the single best predictor of
verification success:

| Triage class at extraction | Queued | Share | Outcome among resolved rows |
|---|--:|--:|---|
| `ok` (structurally consistent CSV) | 8,411 | 36.3% | **95% verified** (5% rejected) |
| `flagged` (structural anomaly noted) | 7,629 | 33.0% | rejected, unless correctable — corrected rows are re-recorded as `ok`+verified and are inside the 95% above |
| `no-csv` (caption detected, no extractable grid) | 4,095 | 17.7% | requires from-scratch vision extraction; mostly unresolved |
| untriaged backlog | 3,012 | 13.0% | — |

Two planning consequences:

1. **Spend vision budget on the `ok` bucket first.** A pre-filter that
   prioritizes structurally-clean, data-dense tables pushed batch verify rates
   to ~95%; the rejects that remain are genuine non-tables (marked-field grids,
   blank pro-formas, figures parsed as tables, transposed/scrambled grids,
   contaminated merges — see [doc 04](04-failure-modes.md)).
2. **The ~50/50 verified/rejected split of all resolved rows is healthy.** Half
   of "tables" a mechanical extractor finds in standards PDFs are not faithful
   data tables. Rejection is a success of the gate, not a loss — what's
   poisonous is publishing them unverified.

### Per-domain completion (prioritization is visible)

| Domain wiki | Tables | Verified | Rejected | % resolved |
|---|--:|--:|--:|--:|
| pipeline-engineering | 1,115 | 326 | 35 | **32.4%** |
| drilling-engineering | 2,686 | 251 | 138 | 14.5% |
| asset-management | 4,804 | 305 | 235 | 11.2% |
| marine-engineering | 10,666 | 324 | 628 | 8.9% |
| engineering-standards (catch-all) | 3,082 | 1 | 32 | 1.1% |
| production-engineering | 688 | 0 | 0 | 0% |
| offshore-renewables | 102 | 0 | 0 | 0% |
| geotechnical-engineering | 4 | 0 | 0 | 0% |
| **Total** | **23,147** | **1,207** | **1,068** | **9.8%** |

The 1.1% domain is deliberate, and instructive: its queue turned out to be
mostly equations and prose mis-parsed as tables (a near-empty `ok` bucket), so
it was deprioritized. **Measure the `ok`-bucket share per domain before
committing verification budget to it.**

## Campaign B — Office formats, source-extract lane

53 documents ingested end-to-end, every page independently verified (2–3 round
cross-review against the source binary). Fidelity (does the extract match the
source?) was **100% after review** — the interesting number is **completeness**
(ICS): how much of the document's information the text/CSV lane structurally
captures.

**Mean completeness across all 53 documents: 63.8%.**

### Average success by document type

| Lane (format × content type) | N | Completeness (ICS) | Maturity |
|---|--:|--:|---|
| docx · prose (minutes / memos) | 2 | 89–100% | Mature |
| docx · structured Q&A | 1 | 79% | Mature |
| docx · long article draft | 3 | 67–100% | Mature |
| xlsx · flat data table | 2 | 95–100% | Mature |
| xlsx · formula model | 12 | 42% values-only → calc-logic recovered by formula capture | Mature (charts still lost) |
| xlsx · schedule / Gantt | 2 | 92% | Mature |
| msg · plain email thread | 4 | 90–100% | Mature |
| msg · with attachments | 4 | 75% body-only → closed by attachment harvest (inventory + recurse office/pdf attachments through their lanes) | Mature |
| msg · deep quoted history | 2 | 100% | Mature |
| pdf · text-born | 1 | 100% | Mature |
| pdf · image / scanned | 0 | — | **Untested** (no sample) |
| pptx · text deck | ~6 | 88–90% | Mature |
| pptx · table-in-deck | ~4 | 65–73% | Mostly mature |
| pptx · diagram deck | ~14 | **28–56%** | **Partial — diagrams lost** |

Reading this as a planner:

- **Prose, flat tables, emails, and text decks land at 80–100%** out of the box.
- **Loss concentrates exactly where engineering value concentrates**: formula
  workbooks (42% until you capture formulas — [doc 09](09-office-formats.md)),
  attachments (75% until you harvest them), and diagram-heavy decks (28–56%,
  the one still-open gap pending a vision lane). The mean of 63.8% is dragged
  down by these specific, *identifiable* lanes — not by random noise. Measure
  your corpus's format×type mix first and you can predict your mean.
- A live per-lane scorecard pattern (the "conversion-lane confidence matrix")
  is what made these gaps visible and closable one by one; keep one for your
  own campaign.

## Maintain a per-document completion index

The statistics above are corpus-level; what makes the *next* verification wave
cheap to plan is a **per-document index** — one committed row per source
document, regenerated from the verification queues:

```
code_id, domain, tables_total, ok, flagged, no_csv,
verified, rejected, pending, pct_resolved, last_touched
```

This is the wave-selection instrument. Each sweep is then a query, not an
archaeology session:

- **"Next wave = highest-value unfinished docs"** — sort by `ok - verified`
  descending: structurally clean tables nobody has verified yet (the 95%-success
  bucket, doc 03's batch selector in index form).
- **"Revisit after a pipeline fix"** — when an extractor bug is fixed (e.g. a
  watermark-contamination or merge-cascade fix from [doc 04](04-failure-modes.md)),
  filter the index for documents whose rejects carried that failure mode and
  re-queue *only those*.
- **"Skip the noise domains"** — a domain whose index shows a near-empty `ok`
  column (the 1.1% domain above) is excluded from sweeps in one glance.
- **"Report progress honestly"** — the per-document completion distribution
  table earlier in this doc *is* a `groupby` over this index.

Rules that keep it trustworthy:

1. **Derived, never hand-edited.** The queues are the source of truth; the
   index is rebuilt by a script (idempotent, run after every verify batch or
   merge). A hand-edited index silently diverges from the queues.
2. **Committed, not local.** Waves may run weeks apart, on different machines,
   by different agents — the index must travel with the corpus, and its diff in
   a verify-batch PR doubles as the progress report.
3. **Document identity must be stable** across re-ingestion (the two-level
   identity of [doc 16](16-corpus-lifecycle.md)) — otherwise a re-ingested
   edition resets its history and the index lies about coverage.

## Reproducing these statistics

Campaign A's numbers come straight from the verification queues — one
`_verification-queue.csv` per domain wiki, one row per table, with
`parse_status` (provisional/verified/rejected) and `structural_status`
(ok/flagged/no-csv) columns. Group by document id and status; the queue *is*
the progress database (and is what the batch selector reads — doc 03). Campaign
B's come from a per-document ICS audit plus the per-lane confidence matrix.
If you adopt this playbook, you get the same measurability for free: **keep the
queue and the lane matrix as first-class, committed artifacts**, and your
completion statistics are one `groupby` away at any time.
