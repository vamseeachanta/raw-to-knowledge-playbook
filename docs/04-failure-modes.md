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

## E. Structured-data & model-file defects (CSV / delimited / solver lanes)

| # | Failure mode | Root cause | Detected by | Mitigation |
|---|---|---|---|---|
| E1 | **Silent column shift** — all downstream fields of a row off by one | Extra delimiter inside a value; field-count overflow | Field-count audit vs header | Per-row field-count assertion at ingestion (GP-32) |
| E2 | **Header-only artifact passes validation** | Validator compared row counts, not contents | Content audit | Cell-content or row-hash parity checks (GP-33) |
| E3 | **Ad-hoc delimiter corruption** | `\|`-delimited shell format met content containing `\|` | Reparse failures | Real CSV writer/reader; keyed structures in shell (GP-32) |
| E4 | **Sign-convention misread** — flipped moments downstream | Intentional notation (negative lever-arm) documented nowhere | Downstream physics check | Convention sidecar with units/signs/frames (GP-34) |
| E5 | **One parser, two export formats** | Solvers emit native (block-marked, multi-sheet) and pipeline (clean-column) formats for the same data | Parse failures on the second variant | One parser per format, auto-detected by header inspection, never filename |
| E6 | **Block-marked listing parsed as flat table** | Text header rows delimit matrix blocks (e.g., per-frequency); flat parse interleaves headers with values | Value-range audit | Block-aware parsing; same defect class as A8 arriving through a "clean" channel |
| E7 | **Silent solver-input defaults** | Parser injected engineering defaults with no record | Provenance audit | Assumption ledger; defaults recorded and surfaced or refused (GP-37) |

## F. Raw-archive ingestion & source-extract-fidelity defects (mixed office formats)

Hit ingesting a mixed-office raw archive (docx/xlsx/msg/pdf/pptx → a private
source-extract wiki). These are the `incident_refs` of the
[office-ingestion skills](../skills/README.md). Related prior entries: `B8`/`B9`
(stranded commits, stacked-branch divergence), `D5` (client data carried
forward), `C5` (nested-agent starvation).

| # | Failure mode | Root cause | Detected by | Mitigation |
|---|---|---|---|---|
| `misfiled-grabbag` | The raw "document folder" is a working **company repo** — code/venv/agent/marketing noise mixed with real documents | Source is a live repo, not a curated set | Content triage (classify on structure, not folder/extension) | Triage by content; value-filter code/config/noise out (skill `content-triage-and-exclusion`) |
| `superseded-dupe` | Many near-identical drafts/revisions of one document ingested as distinct items | No dedup; parallel drafts with different titles | Title/size/text-hash clustering | Keep the latest-dated canonical; catalog the rest, don't ingest |
| `pii-leak` | PII (TIN, home address, phone) ingested from routine admin/payment files swept in with documents | Admin files share the source folder | Pre-ingest PII scan | Hard-exclude payment/admin threads at triage — never ingest |
| `third-party-confidential` | Another party's confidential deliverable republished from the archive (e.g. a "do NOT send" vendor deck) | Vendor/partner files sit in the source folder | Folder-signal + provenance review | Ingest only own records; exclude third-party-authored/confidential material |
| `lfs-pointer-offdisk` | A source binary is a **Git LFS pointer stub**, not the file; naive extraction reads the stub | Sparse/LFS checkout; git-lfs not installed | Pointer-format detection (`oid sha256:`/`size` stub) | Fetch via the LFS Batch API + host token; `sha256==oid` verifies (skill `lfs-batch-fetch`) |
| `raw-binary-firewall` | Raw source binary committed into a tracked repo — license/confidential bytes leak | Extractor writes the binary, or an LFS fetch lands inside the worktree | Staged-tree grep for binary extensions; path-prefix assertion | Raw binary to a temp dir **outside any repo**; commit only derived text/CSV + a sha256 pointer |
| `prose-overclaim` | A faithful extract, but the **prose around it claims more than the extract supports** (the dominant defect class) | Author interprets/concludes/summarizes beyond the source | Independent adversarial prose-vs-extract review | Every claim traces to a committed extract; label interpretation as output, not source (skill `source-extract-fidelity`) |
| `crossref-as-quote` | A value only **cross-referenced** in the source is rendered as if quoted here | Author conflates "see X" with "X states" | Quote traceability (no matching verbatim span) | A cross-reference is not a quote — demote it |
| `derived-as-quoted` | A computed / unit-converted figure presented as a **verbatim** source quote | Author recomputes, then presents as stated | `derivation_status` check | Derived/converted numbers are `derived`, never quoted |
| `silent-completeness-gap` | A faithful text/CSV extract **silently hides** that the richest layer was never captured | Text dump drops formulas/diagrams/attachments/images by design | Per-format coverage ledger; format-aware audit | Record each lane's known loss per page; mark `partial` + backlog a richer lane (skill `format-coverage-ledger`) |
| `formula-loss` | Spreadsheet **calc-logic lost** — only computed values captured (`data_only`) | xlsx text/CSV lane reads values, not formulas | Formula-density probe vs extract | Capture formulas (`data_only=False`) + chart series in a richer lane |
| `diagram-loss` | Slide/figure **diagrams — often the engineering content — uncaptured** by slide-text extraction | pptx lane walks shape text only; images/charts/notes dropped | Shape-type audit (picture/chart vs text) | Vision/image-capture + chart-data + speaker-notes lane |
| `attachment-drop` | Email **attachments dropped**; only the body text ingested | msg lane writes header + body only | Attachment-count probe | Recurse attachments through the same pipeline |
| `shared-file-conflict` | Parallel batch branches collide on a **shared file** (e.g. an auto-generated index) | Each batch regenerates the same shared artifact off main | Merge-conflict on the shared file | Stack batch branches (each off the prior tip); generate the index from frontmatter (skill `stacked-batch-prs`) |
| `index-hand-edit` | Two batches hand-append rows to a shared **index table** → add/add conflict | Index maintained by hand | Conflict on the index table | Auto-generate the index from per-page frontmatter; never hand-edit it |
| `merge-cascade-strand` | Top stacked PRs merge into an **already-merged intermediate branch** and strand their content off `main` — silently (every PR shows "merged") | Stacked-PR bases don't retarget to `main` in time | Verify `main`'s **tree** after merging a stack (not just PR status) | Confirm `main` has the top batches' files post-merge; land any stranded superset branch via one PR |

## The meta-lesson

> **Deterministic checks catch structural problems. Only vision catches value
> problems. Only adversarial review catches process problems.**

Each defect class above survived every cheaper layer of checking below it.
Budget for all three layers from day one.
