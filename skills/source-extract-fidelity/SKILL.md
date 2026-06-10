---
name: source-extract-fidelity
description: >
  Independently reviews a batch of source-extract reference pages against the
  source binary so that no prose claims more than the committed extract supports —
  checking hash match, extract fidelity, and that every quoted figure traces to a
  committed extract with a cross-reference treated as not-a-quote and a derived
  number as not-quoted. Use when reviewing extracted/source-derived pages before
  merge, especially text-faithful pages whose prose may overreach.
license: CC-BY-4.0
compatibility: Requires the source binary (or its verified temp copy), the committed extract (txt/CSV) + sha256 pointer, and a closed status vocabulary on pages
metadata:
  version: "1.1"
  enforcement_level: L2            # callable second-pass review + traceability checks
  status: template
  incident_refs: prose-overclaim,crossref-as-quote,derived-as-quoted
  params: "batch:str | round:int=1"   # rounds continue until PASS — 2 is a floor, not a ceiling
---

# source-extract-fidelity

> Template skill (doc 03, doc 04). Extraction can be byte-perfect and the page
> still wrong — because the **prose around** the extract claims more than the
> extract supports. Across a 53-document campaign the dominant defect class was
> not bad extraction but **prose overclaiming beyond the extract**: a number that
> was cross-referenced (not quoted), a value that was derived (not stated), or a
> clause re-ordered so it no longer matches the source. This skill is the
> independent verify loop that catches that.

> **What this gates:** the *batch PR* (a `needs-verify` → `verified` label flow),
> not each page's `parse_status`. Pages may stay `parse_status: provisional` even
> after the batch passes — per-row promotion to `verified` is a separate step.
> This skill is the independent batch review run before the PR is cleared to merge.

## Trigger
`/source-extract-fidelity <batch> [--round 1|2]`

## Preconditions
1. The reviewer is **independent of the producer** — a different agent/pass,
   prompted to *find a reason the page is wrong*, not to confirm it looks fine.
2. The source binary is available as a verified copy (hash matches its pointer);
   for off-disk LFS binaries, fetch via `lfs-batch-fetch` first.
3. Each source's sha256 is recorded in the page's **source table** and in
   `sources/README.md`, and pages use the closed status vocabulary
   (`parse_status` / `trust_label` / `derivation_status`).

## Steps
1. **Hash gate.** Recompute the source sha256 and confirm it matches the value
   recorded in the page's source table / `sources/README.md`. A source that can't
   be reproduced from its recorded hash is invalid before any prose is read.
2. **Extract-fidelity check.** Compare the committed extract (txt/CSV) against the
   source: did the deterministic lane capture what it claims (right sheet/slide/
   thread, no silent truncation)? Note any known-lossy gap (see
   `format-coverage-ledger`) but do not penalize a faithful extract for the
   text/CSV lane's known loss.
3. **Quote traceability — the core check.** For **every** quoted figure, name, or
   clause on the page, find the exact span in the committed extract. Apply the
   closed rules:
   - A **cross-reference** ("per the calc in sheet X") is **NOT a quote** — it
     must not be rendered as if the value were stated here.
   - A **derived number** (computed/rounded/unit-converted from extract values)
     is **NOT "quoted"** — it is `derivation_status: derived`, never a verbatim
     capture.
   - A **quote must match clause order exactly.** Re-ordering clauses to read
     better changes meaning; a re-ordered quote is a defect, not a paraphrase.
4. **Overclaim sweep.** Read every declarative sentence and ask: *does the
   committed extract contain this?* Anything beyond the extract (interpretation,
   conclusion, "this means…") must be labeled output/analysis, never presented as
   source. Unsupported source-claims → flag for correction.
5. **Invariant + vocab check.** Confirm raw binary is not committed (only derived
   parts + pointer), private content hasn't crossed to public, and every status
   value is in the closed set (no invented labels).
6. **Verdict + further rounds until PASS.** Emit a per-page verdict with cited
   defects. Each later round re-checks what the producer corrected, again
   adversarially — a "fixed" page often just moved the overclaim, and a code
   fix can be narrower than the defect class. Two rounds is the **floor**, not
   the ceiling: the loop ends at a clean PASS, never at a round count (GP-42;
   one campaign fix needed a third round, caught by a reviewer-built
   reproducer — see `adversarial-verify-loop`).

## Verification
- Every quoted span on every page resolves to an exact location in the committed
  extract (the traceability map is complete — no orphan quotes).
- No derived/cross-referenced value is presented as a verbatim quote.
- Hash matches; invariants and closed-set vocab hold.
- Defects cite a **specific falsifiable** location ("page says X, extract has Y"),
  not generic approval/disapproval.

## Cleanup
- n/a (read-only review). The fetched source temp copy is removed by the fetch
  skill's cleanup.

## Incident appendix
| Rule | Why |
|---|---|
| Independent, adversarial reviewer | Charitable self-review rubber-stamps; the producer can't see its own overclaim |
| Quote must trace to a committed extract | The #1 defect class: prose claiming more than the extract supports |
| Cross-reference ≠ quote | A pointer to where a value lives is not the value being stated here |
| Derived number ≠ quoted | Computed/converted values are `derived`, never verbatim captures |
| Clause order must match | Re-ordering a quote silently changes its meaning |
| Cite a falsifiable defect | When two reviews disagree, the specific-location claim wins over generic approval |
| Verify until PASS, not for N rounds | A fix can address the cited example but not the invariant; the round that catches it is the loop working |
