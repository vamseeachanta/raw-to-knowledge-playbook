---
name: stacked-batch-prs
description: >
  Ships an ingestion campaign as one PR per batch on STACKED branches (each off the
  prior tip) to avoid conflicts on shared files like an auto-generated index, and
  guards the merge-cascade hazard where a top stacked PR merges into an already-
  merged intermediate branch and strands content off main. Use when landing many
  sequential ingestion batches that all touch a few shared files.
license: CC-BY-4.0
compatibility: Requires git + a PR host (gh-class), an auto-generated index built from page frontmatter, and a human merge gate
metadata:
  version: "1.0"
  enforcement_level: L2            # callable workflow + a post-merge main-tree check
  status: template
  incident_refs: shared-file-conflict,index-hand-edit,merge-cascade-strand
  params: "batch:str | base:str"
---

# stacked-batch-prs

> Template skill (doc 02, doc 06). When many batches each add pages AND touch the
> same shared files (the index, a queue, a log), parallel branches off main
> collide on every merge. Stacking each branch off the prior tip removes the
> conflict — at the cost of a sharp hazard: merging the stack out of order can
> strand content off `main`. This skill is the discipline that makes stacking safe.

## Trigger
`/stacked-batch-prs <batch-id> [--base <prior-tip-or-main>]`

## Preconditions
1. The index/catalog is **auto-generated from page frontmatter** — never
   hand-edited. (Hand-editing the index is the shared-file conflict generator.)
2. A human merge gate exists; agents open PRs, humans merge.
3. The prior batch's branch tip is known (the base for this batch's branch).

## Steps
1. **Branch off the prior tip, not main.** `git checkout -b batch-<id> <prior-tip>`.
   Each batch sees the prior batch's index/shared-file state, so re-generating the
   index produces a clean superset diff instead of a conflict.
2. **Add pages; regenerate, never hand-edit, the index.** Run the index generator
   so the index is a pure function of frontmatter. A hand edit here re-introduces
   the conflict the stack exists to avoid.
3. **One PR per batch**, targeting the prior batch's PR branch (the stack), with a
   clear "stacked on #<prior>" note so the reviewer/merger knows the order.
4. **Merge bottom-up, in order.** The human merges the **oldest** open PR in the
   stack first. Never merge a higher PR before the one beneath it.
5. **GUARD the merge cascade.** A top stacked PR can auto-target an *already-merged*
   intermediate branch; merging it then lands content onto a dead branch, not
   `main`. After **every** merge in the stack: **verify `main`'s tree actually
   contains the merged pages** (`git fetch && git ls-tree origin/main -- <paths>`),
   and re-target the next PR's base to `main` (or the new tip) if its base was just
   merged.
6. **Rebase trailing PRs if a base moved.** If an earlier PR was squashed/rebased,
   rebase the rest of the stack onto the new main tip before continuing.

## Verification
- After each merge, the merged batch's pages are present in `origin/main`'s tree
  (not just in a merged-away intermediate branch).
- The index on main is the generator's output for the current frontmatter set
  (re-run the generator → empty diff).
- No PR merged out of stack order; no content stranded off main at campaign end.

## Cleanup
- Delete merged batch branches. Confirm `origin/main` is the single source of
  truth and every batch's pages are reachable from it.

## Incident appendix
| Rule | Why |
|---|---|
| Stack off the prior tip | Parallel branches collide on every shared file (index/queue/log) merge |
| Index is generator output, never hand-edited | Hand edits re-create the exact conflict stacking removes |
| Verify main's tree after each merge | A top PR merged into an already-merged base strands content off main |
| Merge bottom-up, re-target moved bases | Out-of-order merges target dead branches |
