# Verification Playbook: The Vision Loop

Auto-extracted tables are **structurally consistent but value-wrong** often
enough that nothing ships as trusted until a vision pass compares the
extracted CSV against the rendered source page. This document is the
operational playbook for that loop, distilled from 80+ batches (~450 tables
verified, ~30 rejected with classified defects).

## The batch loop

```
1. SELECT   ~12 rows from the queue
            --prioritize-data          (numeric-density ranking)
            --deprioritize-rowcollapse (sink collapse suspects to bottom)
2. RENDER   each row's source page → PNG (~200 DPI)
3. VERIFY   vision model compares CSV ↔ PNG cell-by-cell
4. UPDATE   queue verdicts (binary-faithful I/O — see below)
5. COMMIT   one branch per batch → PR → human merges
6. REPEAT   only after the prior batch for that domain is MERGED
```

### Why each step is shaped this way

**Selection is the throughput lever.** File-order/alphabetical selection
yielded 0 verified out of 24 rows (all blank forms and figures at the front
of the bucket). Numeric-data-density ranking immediately produced 5–7
verified per 12-row batch. Spend selection effort before vision effort.

**~12 rows per batch** keeps review load auditable by a human gating the PR.

**Serialize per domain.** The selector reads the queue on the main branch.
If a domain's batch N is unmerged when you select batch N+1, the selector
re-picks the *same* top-priority rows — we shipped two duplicate batches this
way. Different domains can proceed in parallel (their queues are different
files, so no write conflicts); within a domain, strictly merge-then-select.

**When two reviews disagree, prefer the one citing a specific falsifiable
defect.** A duplicated batch produced opposite verdicts on the same table —
the rejection cited an exact value mismatch against the source page
("565,16" on the page vs "585,16" in the CSV); the verification was generic
approval. Specific evidence wins.

## Verdict decision tree

```
Is the rendered region a data table at all?
├── NO → figure / chart / blank form / cover page ............ REJECTED
└── YES
    ├── Do all cell VALUES match the rendered page?
    │   ├── YES, with only OCR noise in HEADERS
    │   │   (e.g. "Iblft" → "lb/ft") ......................... VERIFIED
    │   │                                                       (note the noise)
    │   └── NO
    │       ├── Real data, recoverable extraction defect
    │       │   (page-mismatch, row-collapse, transposed,
    │       │    truncated, header-collapse) .................. DEFERRED
    │       │                                                    (tag defect class)
    │       └── Unrecoverable garble / data loss .............. REJECTED
```

**Strict watermark policy:** a single watermark glyph inside a *data cell*
means the table is not faithful → reject and re-extract with the watermark
stripped. Never "verified-with-note" for in-cell contamination.

**Rejected ≠ discarded.** Every rejection carries a defect class in the
queue's notes field, so a future improved extractor can re-process exactly
the affected class.

## Verification rigor rules

1. **Check the rightmost column, not just the first cell.** Multi-header
   tables can be perfectly aligned on the left and shifted by one column at
   the right. Subagents that "confirm first cell and extrapolate"
   over-verify — in one batch a main-session re-check overrode 6 of 12
   subagent verifications for exactly this defect.
2. **Anchor on the exact CSV path, never a glob or document id.** Different
   editions of the same standard share table IDs; a glob match verifies the
   wrong edition's file.
3. **Adversarial stance for spot-checks.** A second-pass checker's prompt
   must be "find a reason this verdict is wrong," not "confirm this looks
   fine." Charitable re-reads rubber-stamp.
4. **Subagent claims need validation in both directions** — over-verification
   (above) and overclaimed confidentiality screening (a subagent once
   asserted "no confidential identifiers" while its output contained project
   folder names; the orchestrator must grep for known identifiers itself).

## Status lifecycle and queue hygiene

| Field | Values | Owner |
|---|---|---|
| `parse_status` | `provisional-unverified` → `verified` \| `rejected` \| `deferred` | vision pass |
| `structural_status` | `ok` \| `flagged` \| `no-csv` | triage pass |

- The two vocabularies never mix. (A batch that wrote `verified` into
  `structural_status` corrupted the queue and cost a repair PR.)
- Terminal rows are never re-queued.
- Adding a status value requires registering it in the queue normalizer's
  known-set first, or rewrites mangle it.

### Binary-faithful queue edits

Real-world queue CSVs accumulate **mixed line endings** (rows appended by
different tools on different platforms). Text-mode `open()` + `csv` round
trips silently normalize every CRLF row → a 12-row verdict edit produced a
352-line phantom diff.

Rules:
- Read/write the queue in **binary** (`rb` / split on `b"\n"` / `wb`),
  re-emitting each row's original terminator.
- Never `line.split(",")` — notes contain commas; parse single rows with a
  real CSV reader.
- After every edit, assert `git diff --numstat` equals exactly
  2 × rows-you-changed. Any excess means you normalized something.
- Harden the read path for embedded newlines inside quoted cells *before*
  one ever appears (use a stream-based CSV reader, not `splitlines()`).

## Where the figure/no-csv bucket fits

Caption-only rows (figures, images) get their own vision pass: the question
is "does this region contain an extractable data table the mechanical pass
missed?" — mostly no (terminal reject), occasionally yes (manual extraction).
Keep their queue identity non-degenerate (populate a table ordinal even
without a CSV path) or dedup will silently collapse distinct figures on the
same page.
