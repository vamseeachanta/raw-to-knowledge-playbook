# Reference Pipeline Architecture

```
                 off-repo source archive (raw PDFs — NEVER committed)
                                   │
                          ┌────────▼────────┐   cron, every 6 h
                          │   DISPATCHER    │   chunked, resumable,
                          │  (state file)   │   one PR per tick
                          └────────┬────────┘
              per chunk: isolated git worktree
                                   │
                  ┌────────────────▼─────────────────┐
                  │      MECHANICAL EXTRACTOR        │  deterministic
                  │  decrypt → strip watermarks →    │  (no LLM)
                  │  classify → route → extract      │
                  └───────┬──────────────┬───────────┘
                          │              │
                 landing page +     table CSVs +
                 part files (L1)    queue rows (L2, provisional)
                          │              │
                          │     ┌────────▼─────────┐
                          │     │ STRUCTURAL TRIAGE │  deterministic (L3)
                          │     │ ok│flagged│no-csv │  + dedup-on-write
                          │     └────────┬─────────┘
                          │              │
                          │     ┌────────▼─────────┐
                          │     │ VISION VERIFY    │  LLM with vision (L4)
                          │     │ batch loop, PNG  │  verified│rejected│deferred
                          │     │ vs CSV per cell  │
                          │     └────────┬─────────┘
                          │              │
                          └──────┬───────┘
                                 ▼
                    domain wiki (indexes, logs, RAG chunks)  (L5)
```

## Components

### 1. Cron wrapper
A thin shell script on a 6-hour cadence. Hard-won details:

- **Reconstruct the environment.** Cron strips the interactive shell env;
  the wrapper must rebuild `PATH`/`HOME` (node global bins, Python env) or
  any CLI-based agent dispatch silently fails.
- **Args live in the repo script, not the crontab.** The cron reads the
  on-disk script at launch, so publisher lists and chunk parameters can be
  changed by a normal PR without touching cron. Corollary: a *running* tick
  uses the script as of its launch — a just-merged fix doesn't apply until
  the next tick (this caused a false "fix not working" alarm once).
- **The cron opens PRs but never merges.** Human merge gate, always.

### 2. Dispatcher (state machine)
- **Chunking:** documents grouped by publisher, 5–12 per chunk. A JSON state
  file records completed chunks (keyed by doc-set, with timestamps, commit
  SHAs, attempt counts) → fully idempotent resume after any failure.
- **Worktree isolation:** each chunk runs in a temporary git worktree;
  branch creation uses force-reset-to-ref to avoid stale divergence. A lock
  serializes `worktree add` calls (they race under concurrency).
- **Write-root firewall:** staged paths are validated against an allow-list
  (wiki dirs + reports only); anything else raises and quarantines the chunk.
- **Retry on transient sandbox failures** with exponential backoff (max 3).
- **Concurrency:** capped at 3 workers historically; with fast deterministic
  extraction, **serial (concurrency 1) is sufficient** and eliminates a whole
  class of git-ref races. Don't buy parallelism you don't need.
- **Per-publisher failure containment:** one publisher's exception must not
  abort the tick — and must not strand already-committed chunks without a PR
  (a real bug found in adversarial review: a mid-publisher exception after
  commit left completed work PR-less).

### 3. Mechanical extractor
Per document: decrypt → **strip diagonal watermarks** (neutralize Form
XObjects placed with rotated matrices — in-memory only, the raw PDF is never
modified) → classify domain by content keywords → junk/non-standard filters
→ extract text + tables → emit landing page, parts, CSVs, queue rows, and
index/log appends. Skips are recorded with reasons in a `_skipped.csv`.

### 4. Shared append-only files + union merge + dedup
Queues, indexes, and logs are declared `merge=union` in `.gitattributes` so
concurrent ingest branches merge cleanly. **The trap:** union merge assumes
append-only. The moment any process *rewrites* rows (a triage pass touching
every line), divergent branches union into massive duplication — observed:
38,680 rows where only ~17,900 were unique (46% bloat).

**Fix: dedup-on-write, every write.** Collapse rows by a logical identity
tuple; precedence rules keep the worse-off variant (flagged > no-csv > ok >
blank); idempotent (second run is a no-op). One-time cleanups rot; built-in
self-healing doesn't.

**Identity must be non-degenerate for every row type.** A blank field inside
the identity tuple (e.g., `csv_path` for caption-only rows) lets two distinct
rows collapse into one and silently drop data. Validate identity uniqueness
at ingest.

### 5. Verification queue
One CSV per domain. Lifecycle:

```
provisional-unverified ──triage──▶ structural_status ∈ {ok, flagged, no-csv}
        │
        └──vision──▶ parse_status ∈ {verified, rejected, deferred}   (terminal)
```

- Terminal statuses are **never re-queued**.
- Any new status value must be registered in the queue normalizer's
  known-status set, or it gets mangled on the next rewrite.
- Keep `structural_status` and `parse_status` vocabularies strictly
  separate — writing a verdict into the structural column corrupted a batch
  once and cost a cleanup pass.

## Evolution lessons (what we changed and why)

| Iteration | Design | Why it died |
|---|---|---|
| v1 | LLM-driven extraction per doc | ~2% text coverage, guardrail refusals on copyrighted text, hours per doc |
| v2 | Mechanical extraction, one PR per publisher per tick (up to 13) | Chronic merge churn between shared append-only files across 13 PRs |
| v3 | Chained per-publisher branches | Stacked merges diverged branches from remote; abandoned |
| **v4 (current)** | Mechanical, serial, single shared branch, one PR per tick | Stable; 29 consecutive unattended ticks verified |
