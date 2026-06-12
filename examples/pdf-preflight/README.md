# PDF preflight example — measure, then pick the load strategy

[GP-49](../../docs/05-good-practices.md) runnable: before extracting anything
from a large PDF, a cheap assessment pass measures the file and routes it to
one of three strategies, so a 100 MB / 1000-page document never gets loaded
whole into a worker that will OOM mid-batch.

```
ASSESS (cheap)                      →  ROUTE
  bytes, pages, bytes/page              full_load      small & simple
  sampled images/fonts → 0-100          stream_pages   the default (generator)
  encryption / page probe / U+FFFD      chunk_batch    big or complex
```

## Run it

Requires [`uv`](https://docs.astral.sh/uv/) (deps declared inline via PEP 723):

```bash
uv run preflight.py ../minimal-ingest/sample/allowable_stress.pdf
uv run preflight.py big.pdf --json    # machine-readable, for a dispatcher
uv run preflight.py --check           # self-test on the bundled sample (CI)
```

Sample output:

```
size       : 0.00 MB  (1 pages, 2 KB/page)
complexity : 0/100
memory     : min 2 MB | recommended 10 MB | peak 24 MB
STRATEGY   : full_load  (chunk_size=1)
issues     : none detected
```

Exit code `2` (assessed, but **critical** issues found — encryption, failed
page probe) lets a shell dispatcher fail closed without parsing output.

## The heuristics, in one table

Rules apply top-down — **first match wins** (so a 500+-page file that is
small and simple still full-loads; the page-count guard exists for files too
big to hold, not merely long ones):

| Signal | Threshold | Consequence |
|---|---|---|
| any **critical** issue | encryption, first/last-page probe failure | force `stream_pages` (careful lane) |
| size & complexity | < 10 MB and score < 50 | `full_load` |
| size, pages, or complexity | ≥ 100 MB, > 500 pages, or score > 70 | `chunk_batch` (5 pages/chunk if complex, else 10) |
| everything else | — | `stream_pages`, one page in memory at a time |
| U+FFFD ratio in sampled text | > 10 % | encoding failure — the text layer is mojibake; route to the OCR lane (doc 11), don't publish it |

Memory estimate: ~5 MB/page baseline, ~10 MB/page when > 200 KB/page on disk
(image-heavy), ~2 MB/page when < 50 KB/page (plain text); peak = base + 10
pages + 20 % overhead.

## What's real vs heuristic (the honest part)

| Piece | Status |
|---|---|
| Structural probe (encryption, page count, first/last-page access) | **real** — pypdf reads the structure without loading content |
| Complexity sampling (images, fonts, U+FFFD on first 3 pages) | **real but sampled** — a document whose late pages differ wildly from its first 3 will be mis-scored |
| Memory estimates | **heuristics** — calibration points from the donor build's memory-bounded tests (streaming 50 medium pages held < 100 MB peak; list-loading the same < 200 MB), not laws |
| Strategy thresholds (10 MB / 100 MB / 500 pages / score 50/70) | **defaults that worked** — re-tune per corpus |

## Provenance

Ported from a retired internal large-PDF reader build — autopsy in
[docs/case-studies/pdf-large-reader-salvage.md](../../docs/case-studies/pdf-large-reader-salvage.md).
The donor ran on PyMuPDF (AGPL-3.0, flagged in the
[doc 12 license register](../../docs/12-tooling-landscape.md)); this port uses
only ADOPT-tier permissive tools (pypdf BSD-3, pdfplumber MIT) so the example
matches the playbook's own license posture.
