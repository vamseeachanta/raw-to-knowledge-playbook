# Failure-Mode Catalog

Every entry below was hit in production. Columns: how it manifests, the root
cause, how it was detected, and the mitigation now in place. Failure modes
are the most valuable artifact of this project — structural checks catch
none of the subtle ones; vision review and adversarial code review caught
them all.

## A. Extraction defects (per-table)

| # | Failure mode | Root cause | Detected by | Mitigation |
|---|---|---|---|---|
| A1 | **Watermark contamination** — watermark glyphs merged into data cells (`t\n9 1/4`) | Diagonal "Draft" watermark drawn as a rotated Form XObject; the text extractor merges its glyphs into the text layer | Vision review (structural checks pass!) | Strip rotated-placement Form XObjects in-memory *before* extraction; config-driven; no-op on clean PDFs |
| A2 | **Transposed / scrambled axes** — rows and columns swapped or shuffled | Table-detection heuristic misreads reading order | Vision review | Defect-classed `deferred`; re-extract with corrected axis mapping |
| A3 | **Row collapse** — multiple source rows stacked into one cell with newlines | Parser stacks multi-line cells | Heuristic: ≥6 newlines in ≥3 columns co-occurring | De-prioritize in batch selection (vision stays the authority — some "collapsed" cells are legitimately multi-valued) |
| A4 | **Header collapse** — N column labels jammed into one cell | Multi-row header rows merged | Vision review | Defect-classed; re-extract with header-splitting |
| A5 | **Truncated table** — only some row groups extracted, rest silently dropped | Detection window ends early | Vision review (row-count mismatch vs page) | Defect-classed; re-extract with exhaustive page walk |
| A6 | **Column misalignment / drift** — values shifted one column right of their headers | Inconsistent per-block column schema | Vision review, **rightmost-column check** | Verify rightmost column explicitly; defect-class on failure |
| A7 | **OCR digit substitution** — `0.()81` for `0.081`, `585,16` for `565,16` | Glyph misrecognition | Vision review, cell-by-cell | Reject/correct; never trust numerically-plausible OCR |
| A8 | **Contaminated merge** — two unrelated tables on one page merged into one CSV | Detection merges adjacent regions | Vision review | Defect-classed; split by source caption |
| A9 | **Duplicate extraction across editions** — same table from a corrupt old scan and a clean newer edition | Corpus contains multiple editions | Vision review + identity audit | Keep the clean edition; never glob-match table IDs across editions |
| A10 | **Page misattribution** — queue points at a page 1–5 off from the actual table | Page mapping drift in multi-page tables | Vision review (rendered page ≠ expected content) | Remap in queue notes; treat page+in-page-order as the mapping key for re-extraction |

## B. Pipeline / data-plumbing defects

| # | Failure mode | Root cause | Detected by | Mitigation |
|---|---|---|---|---|
| B1 | **Queue duplication explosion** (38.6k rows, 46% bloat) | Union-merge driver assumes append-only; a triage pass rewrote every row → branches diverged on every line | Row-count audit | Dedup-on-write (self-healing, idempotent), precedence rules preserve worse-off variants |
| B2 | **Degenerate row identity** — distinct caption-only rows collapse and one is silently dropped | Blank field inside the identity tuple | Design review | Identity tuple must be non-degenerate for *every* row type; validate at ingest |
| B3 | **CRLF normalization phantom diffs** | Text-mode I/O on mixed-line-ending CSV | `git diff --numstat` discipline | Binary-faithful I/O; per-row terminator recovery; assert diff size = 2× edited rows |
| B4 | **Embedded-newline time bomb** | `splitlines()`-based parsing would shatter a quoted multi-line cell | Pre-emptive review | Stream-based CSV reader + logical-row→physical-line mapping, fixed before the first occurrence |
| B5 | **Unknown status mangled** | Queue normalizer coerces unrecognized status values | Batch audit | Register every new status in the known-set before first use |
| B6 | **Vocabulary cross-write** — verdicts written into the structural column | Prompt under-specification for batch agents | Next-batch audit | Hard-specify allowed values per column in every batch prompt |
| B7 | **Duplicate batch selection** | Selector reads main; prior batch unmerged | Two batches with identical rows | Serialize select→merge per domain |
| B8 | **PR-less stranded commits** | Mid-publisher exception after commit, before PR | Adversarial code review | Per-publisher containment + PR creation for already-committed chunks |
| B9 | **Stacked-branch divergence** | Chained per-publisher branches merged into each other | Ref audit | Abandon chaining; single shared branch, serial |
| B10 | **Canonical-id fragmentation** — one standard ingested under several truncated ids | Filename-based id heuristic truncates inconsistently | Corpus dedup audit | Canonical id = publisher + standard number; edition kept as a separate field; one-off migration |

## C. Automation / environment defects

| # | Failure mode | Root cause | Detected by | Mitigation |
|---|---|---|---|---|
| C1 | **Cron dispatch silently dead** | Cron strips interactive env; agent CLI not on PATH | Empty tick logs | Wrapper reconstructs PATH/HOME explicitly |
| C2 | **"Fix not taking effect" false alarm** | A running tick uses the on-disk script as of *launch*; the fix merged mid-tick | Timeline reconstruction | Expect one stale tick after any pipeline change |
| C3 | **Empty log misdiagnosed as hang** | Block-buffered stdout + timeout SIGKILL leaves an empty redirected log while work proceeds | Re-probe with unbuffered output | `PYTHONUNBUFFERED=1` + a fault-handler dump before declaring anything hung |
| C4 | **Sandbox transient failures** | Namespace setup races under concurrency | Retry logs | Exponential backoff, ≤3 attempts; cap concurrent sandboxed agents |
| C5 | **Nested agent CPU starvation** | Heavy agent process nested inside another agent's sandbox gets ~5% CPU | Job produced nothing for hours | Route heavy authoring to first-class subagents; nested CLIs only for light review |
| C6 | **Git races under heavy parallelism** | 60+ concurrent git processes; chained `add && commit` | 19-minute D-state hang | Atomic per-file commits (`git commit -- <path>`), orchestrator serializes all git, workers write files only |
| C7 | **Sparse-worktree silent drops** | `git add` skips paths outside the sparse cone without error | Committed tree ≠ disk | `git add --sparse` + verify with `git show HEAD:<path>`, set-equality not counts |

## D. Office-format defects (Excel / Word lanes)

| # | Failure mode | Root cause | Detected by | Mitigation |
|---|---|---|---|---|
| D1 | **Stale cached values used as test oracles** | Workbook saved without recalculation; cached results missing or outdated | Re-execution mismatch audit | Classify cells `cached_ok`/`cached_missing`/`cached_suspect`; assert only `cached_ok` (GP-28) |
| D2 | **Extraction-stub pileup** — formulas extracted at scale but never integrated | Extraction is fast and satisfying; integration is slow | Backlog audit (656K formulas, 0 wired in) | Integrate-before-extract-more gate (GP-30) |
| D3 | **Dual export layouts from one source** — same tool emits block-matrix and flat-table XLSX | Exporter version/mode differences | Parse failures on the second variant | Probe structure per file; dual-path parser; never assume one layout per family |
| D4 | **Keyword-based sheet classification false positives** | Sheet/file names lie about content | Spot-check of classified inventory | Classify on scanned structure (formula density, function mix), not names |
| D5 | **Client data carried forward with the calculation** | Logic and confidential inputs are interleaved in legacy workbooks | Deny-list scan | Extract generic methodology only; scan before archiving; raw workbook never copied (GP-31) |

## The meta-lesson

> **Deterministic checks catch structural problems. Only vision catches value
> problems. Only adversarial review catches process problems.**

Each defect class above survived every cheaper layer of checking below it.
Budget for all three layers from day one.
