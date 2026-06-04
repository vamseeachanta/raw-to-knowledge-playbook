# Skills Catalog: Packaging Workflows for Agents

Once a workflow stabilizes, it gets promoted from "remembered procedure" to a
**skill** — a versioned, parameterized instruction file an agent can execute
on demand. This page catalogs the skills built for the ingestion campaign and
the design lessons they encode.

## Why skills (vs. memory or docs)

| Mechanism | Good for | Fails at |
|---|---|---|
| Memory notes | One-off facts, incident lessons | Multi-step procedures drift in retelling |
| Docs/runbooks | Human reference | Agents skim; steps get skipped |
| **Skills** | Repeatable multi-step agent workflows | — (but require maintenance like code) |

The tell that something should become a skill: you've explained the same
procedure to an agent three times, or a batch failed because a step was
improvised differently than last time.

## The flagship: `verify-batch`

Invoked as `/verify-batch [--n N] [--bucket ok|flagged|no-csv] [--domain D]`.
Encodes the entire vision-verification loop:

1. Fetch + create an isolated worktree off origin/main.
2. Run the batch selector (density-ranked, collapse-deprioritized) →
   manifest + rendered page PNGs.
3. Vision review per row: compare PNG ↔ CSV at the **exact** csv_path;
   verdict per the decision tree (verified / rejected / deferred).
4. Update the queue with **binary-faithful I/O**; record verifier +
   verification notes.
5. Commit (per-file pathspec), push, open PR.
6. Report: PR link + verdict table + running totals.
7. Clean up the worktree.

Design lessons baked in after incidents:
- The skill *hard-specifies* the allowed values for each status column
  (a batch once wrote verdicts into the wrong column).
- It pins the OCR-noise policy (header noise → verified-with-note; any
  glyph in a data cell → reject).
- It embeds the serialize-per-domain rule and the diff-size assertion.

## Companion research skills (4, interlocking)

1. **Page-shape contract** — the wiki page structure rules (layered
   input/output split, public/private abstraction gate). Governs what a
   well-formed page looks like.
2. **Audit feedback loop** — anchored-text feedback inbox with explicit
   resolution states; feedback is never silently deleted.
3. **Source-extraction coverage** — doc-type-aware extraction recipes
   (PDF/DOCX/XLSX/HTML/scanned) with a frontmatter contract:
   `extraction_estimate` declared *before* extraction,
   `extraction_yield` recorded *after*. The estimate/yield pair makes
   shallow extraction visible (this is how the 2%-coverage problem was
   caught).
4. **Public/private routing** — the firewall rules between the public store
   and per-client private stores, with the abstraction-by-default naming
   policy.

## Enforcement gradient

Skills mature along a gradient:

| Level | Form | Example |
|---|---|---|
| L1 | Callable skill (agent follows instructions) | All four research skills at birth |
| L2 | Backed by a checking script | Frontmatter validator run by the skill |
| L3 | Pre-commit / CI hook (can't merge violations) | Visibility-routing check, deny-list scan |

Promote a rule up the gradient when violations recur. Instructions catch
intent; hooks catch everything.

## Anatomy of a good skill file

- **Trigger:** exact invocation + parameters.
- **Preconditions:** what must be true (fetched remote, merged prior batch).
- **Steps:** imperative, with exact commands and *closed-set values* for any
  field the agent writes.
- **Verification:** how the agent proves it worked (diff-size assertion,
  verdict-table report).
- **Cleanup:** what must not be left behind.
- **Incident appendix:** the failures that shaped each rule — agents follow
  rules better when the why is attached.
