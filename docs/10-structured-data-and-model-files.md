# Structured Data & Analysis-Model Files: CSV, Delimited, Solver ASCII Formats

Beyond documents (PDF, docs 01–04) and live Office artifacts (doc 09), an
engineering ecosystem holds a third population: **machine-oriented text
files** — CSVs and delimited exports, and the ASCII input/output files of
analysis solvers (hydrodynamics, structural, FEA, CFD packages). They look
like the easiest sources ("it's already structured!") and that assumption is
exactly what makes them dangerous: every failure mode in this lane is
*silent*.

In the D1/D2/D3 dimension model ([doc 09](09-office-formats.md)):

| Source | D1 content | D2 logic | D3 format |
|---|---|---|---|
| CSV / delimited file | **primary** — but conventions (units, signs) live outside the file | n/a | column-layout conventions per producer |
| Solver **input** deck | parameters | **primary** — the model definition *is* engineering decisions | card/keyword layout per solver |
| Solver **output** listing/export | **primary** — results | n/a | block-marked text structure per solver/version |

---

## 1. CSV and delimited files

"Structured" is a claim, not a property. Verify it at ingestion:

### Dialect and integrity probing (before any parse)

- **Probe the dialect**: delimiter, quoting, encoding, line endings. Mixed
  CRLF/LF within one file is real (see failure B3) and naive text-mode I/O
  silently rewrites it.
- **Validate field-count per row against the header at ingestion.** Extra
  delimiters in a value silently shift every downstream column for that row
  — the file still parses, the data is garbage.
- **Never invent ad-hoc delimited formats in shell.** A pipe-delimited row
  format corrupted silently the first time user content contained a `|`.
  Use a real CSV writer/reader (proper quoting) for generation and parsing;
  for shell-side state, use keyed structures instead of delimited strings.

### Content validation (not count validation)

Validators that compare only row counts pass files that are wrong: a
header-only CSV paired with a non-empty sibling artifact sailed through a
row-count check in production. **Compare cell contents or deterministic
row hashes**, never just shapes.

### Conventions are data — capture them as provenance

A physics CSV with a negative lever-arm column and positive force column
produces flipped-sign moments downstream. That was *intentional notation*,
not a defect — but nothing in the file says so. Every ingested dataset
carries a sidecar provenance record: units per column, sign conventions,
coordinate frames, and any producer quirks. A convention that lives only in
the original author's head becomes a "bug report" later.

### Effort estimation by density

Dataset volume scales effort non-linearly: one standard with 166 tables +
95 figures cost ~10× a sibling with 2 figures. **Estimate
table/figure/column density before committing** to digitize a delimited or
tabular corpus; density, not document count, predicts the work.

---

## 2. Analysis-model input files (solver decks)

Solver input files (keyword/card-based ASCII, vendor YAML/dat formats) are
the **model definition** — mesh references, material properties, load
cases, analysis options. They are D2 logic in disguise: every value encodes
an engineering decision.

### The canonical practice: parse to config, regenerate the deck

Don't treat the deck as the editable artifact. Parse it into an
**externalized, reviewable config file (YAML)** that holds the engineering
parameters — material constants, safety classes, thresholds, sweep axes,
data locations — and *regenerate* solver inputs from that config.

Why (directive born from building industry deliverables): a hardcoded or
hand-edited deck serves one project; a config-driven generator serves an
industry. The config is git-trackable, diff-reviewable, and a third party
can re-target it by editing YAML with zero code changes. The deck becomes a
build artifact.

### The output-driven contract (a/b/c)

A mature ingestion of a solver domain isn't a file parser — it's a pipeline
defined by the *outcome*:

- **(a) Q&A + assumption ledger** — detect which inputs are missing for the
  requested outcome; ask; where unanswered, supply engineering defaults
  **that are provenance-tagged and surfaced, never silent**. (A parser that
  silently injected defaults had to have them removed; defaults are fine
  when recorded, forbidden when invisible.)
- **(b) prepare solver input** — assemble the deck from config + ledger.
- **(c) sanity-checked output** — results gated by physical-range and
  coverage checks before anyone consumes them.

The assumption ledger is the lane's equivalent of `provisional-unverified`:
it makes the trust state explicit.

### License-independence of extraction

Importing a solver's API or parsing its files proves nothing about license
availability at run time. Design the *extraction* path (parse decks,
read outputs) to work without the solver installed; only the *run* path
(pillar b→c execution) needs the license. This keeps ingestion runnable on
any machine and in CI.

---

## 3. Solver output listings and exports

Solver results arrive as text listings or spreadsheet exports with
**block-marked structure**: repeated text header rows delimit blocks
(e.g., a matrix block per frequency, with mid-column regime changes), DOF
row labels, magnitude/phase column pairs.

Hard-won rules:

- **Expect at least two coexisting formats per solver** — the native GUI
  export (complex, multi-sheet, text-marked blocks) and a
  pipeline-processed format (clean columns). One parser per format,
  **auto-detected by header inspection**, never by filename. Prefer the
  pipeline format for anything new; keep the native parser for legacy.
- **Block-marked text is not a table.** Parsing a frequency-block listing
  as flat tabular data interleaves block headers with values — the same
  class of defect as PDF contaminated merges (failure A8), arriving through
  a "clean" channel.
- Output values feed pillar (c) sanity checks before they feed anything
  else.

---

## What "verified" means in this lane

| Lane | Verifier |
|---|---|
| CSV / delimited | Field-count + content-hash validation; convention sidecar reviewed |
| Solver input deck | Round-trip: config → generated deck → re-parsed config is identity; assumption ledger reviewed |
| Solver output | Physical/range/coverage sanity gates; cross-format parity (native vs pipeline export of the same run) |

Same trust model as every other lane: **nothing is trusted because it
parsed.** Structure is a hypothesis the verifier must confirm.
