---
name: verify-batch
description: >
  Vision-verifies the next batch of auto-extracted tables against rendered page
  images and writes closed-set verdicts with binary-faithful queue I/O, one PR
  per batch. Use when promoting provisional table extractions to a trusted
  (verified) state, correcting flagged rows, or checking no-csv figures.
license: CC-BY-4.0
compatibility: Requires git, Python 3.11+, uv, a vision model, and an ingestion queue with parse_status/structural_status columns
metadata:
  version: "1.0"
  enforcement_level: L2            # callable skill + frontmatter/diff-size checking scripts
  status: template                 # adapt the {{PLACEHOLDERS}} to your corpus before first run
  incident_refs: A1,A6,A7,A9,B3,B5,B6,B7
  params: "n:int=12 | bucket:enum(ok,flagged,no-csv)=ok | domain:str"
---

# verify-batch

> Template skill from the Raw-to-Knowledge Playbook (doc 08, doc 03).
> Replace every `{{PLACEHOLDER}}` with your corpus's paths/commands. The
> **rules** (closed-set values, binary-faithful I/O, serialize-per-domain,
> adversarial spot-check) are the transferable part — keep them verbatim.

## Trigger

`/verify-batch [--n N] [--bucket ok|flagged|no-csv] [--domain D]`

## Preconditions (assert before doing anything)

1. Remote is fetched and the **prior batch for this `--domain` is already
   MERGED** to the main branch. If not, STOP — the selector reads the queue on
   main and will re-pick the same rows (incident B7).
2. Working tree clean; you are about to create an **isolated worktree** off the
   main branch, not edit in place.
3. The queue file for `--domain` exists and its status vocabulary is registered
   in the normalizer's known-set (incident B5).

## Steps

1. **Worktree.** `git fetch origin && git worktree add {{WORKTREE}} origin/{{MAIN}}`.
   All work happens here; the main checkout is never touched.
2. **Select.** Run the batch selector against the `--domain` queue:
   `{{SELECT_CMD}} --bucket {{bucket}} --n {{n}} --prioritize-data --deprioritize-rowcollapse`.
   This ranks by numeric-data density and sinks row-collapse suspects.
   *Never* select in file/alphabetical order — that yielded 0/24 verified
   (all front-of-bucket blank forms). Output: a manifest + rendered page PNGs
   (~200 DPI).
3. **Verify, per row.** For each manifest row, open the PNG and the CSV at the
   row's **exact `csv_path`** (never a glob or document id — editions share
   table IDs, incident A9). Apply the verdict decision tree below. Enforce the
   rigor rules below — especially **check the rightmost column** (incident A6).
4. **Write verdicts — binary-faithful I/O.** Update only `parse_status` (the
   vision vocabulary), record `verifier` + `verification_notes`. Read/write the
   queue in **binary** (`rb` / split on `b"\n"` / `wb`), re-emitting each row's
   original line terminator; parse single rows with a real CSV reader, never
   `line.split(",")`. (Incident B3: text-mode round-trip silently rewrote 340
   CRLF rows → 352-line phantom diff for a 12-row edit.)
5. **Assert diff size.** `git diff --numstat` must equal **exactly
   2 × rows-you-changed**. Any excess means you normalized something — revert
   and redo in binary.
6. **Commit + PR.** Atomic per-file commit (`git commit -- {{QUEUE_PATH}}`),
   push the batch branch, open one PR. A human merges (do not self-merge).
7. **Report.** PR link + a verdict table (row → verdict → defect class if any)
   + running totals for the domain.
8. **Cleanup.** `git worktree remove {{WORKTREE}}`. Leave nothing behind.

## Verdict decision tree (closed-set)

```
Is the rendered region a data table at all?
├── NO → figure / chart / blank form / cover ................ REJECTED
└── YES
    ├── All cell VALUES match the rendered page?
    │   ├── YES, only OCR noise in HEADERS ("Iblft"→"lb/ft") . VERIFIED (note the noise)
    │   └── NO
    │       ├── Real data, recoverable defect
    │       │   (page-mismatch | row-collapse | transposed |
    │       │    truncated | header-collapse) ............... DEFERRED (tag defect class A2–A10)
    │       └── Unrecoverable garble / data loss ............ REJECTED
```

- **Closed sets — do not invent values.**
  `parse_status ∈ {provisional-unverified, verified, rejected, deferred}`.
  `structural_status ∈ {ok, flagged, no-csv}`. **Never** write a `parse_status`
  value into the `structural_status` column or vice versa (incident B6 cost a
  repair PR).
- **Watermark policy (strict):** a single watermark glyph inside a *data cell*
  → REJECT and re-extract with the watermark stripped. Never
  "verified-with-note" for in-cell contamination (incident A1).
- **Rejected ≠ discarded:** every rejection carries a defect class in notes so a
  better extractor can re-process exactly that class later.

## Verification rigor rules (the ones incidents taught)

1. **Check the rightmost column, not just the first cell.** Left-aligned,
   right-shifted tables look fine on cell 1 (incident A6; a re-check once
   overrode 6/12 subagent over-verifications).
2. **Anchor on the exact `csv_path`.** Glob/id matching verifies the wrong
   edition (incident A9).
3. **Adversarial spot-check.** A second-pass checker's prompt is *"find a reason
   this verdict is wrong"*, never *"confirm this looks fine."* Charitable
   re-reads rubber-stamp.
4. **Validate subagent claims both directions.** Over-verification (above) AND
   overclaimed confidentiality screening — the orchestrator greps for known
   identifiers itself; a subagent once asserted "no confidential identifiers"
   while its output held private folder names.
5. **When two reviews disagree, prefer the one citing a specific falsifiable
   defect** (e.g. "page shows 565,16, CSV has 585,16") over generic approval.

## Verification (how this skill proves it worked)

- Diff-size assertion passes (`2 × rows changed`).
- Every changed row has a verdict from the closed set + a verifier + (for
  non-VERIFIED) a defect class.
- The PR report's totals reconcile with the queue's terminal-row count.
- Public batch reports and review notes pass
  `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces`; use
  `--diff-only` before committing verifier outputs.

## Cleanup

- Worktree removed; no stray branches; no PNGs or manifests committed.

## Incident appendix (why each rule exists)

| Rule | Incident | What went wrong |
|---|---|---|
| Density-rank selection | (selection) | File-order selection → 0/24 verified |
| Serialize per domain | B7 | Unmerged prior batch → duplicate batch selected |
| Binary-faithful I/O | B3 | Text-mode round-trip → 352-line phantom diff |
| Closed-set per column | B6 | Verdict written into structural column → repair PR |
| Rightmost-column check | A6 | Right-shift passed first-cell check; 6/12 over-verified |
| Exact csv_path | A9 | Glob matched wrong edition's table |
| Strict watermark | A1 | Draft-overlay glyph merged into a data cell |
| Self-grep identifiers | (D-screening) | Subagent overclaimed "no confidential IDs" |
