# Document Taxonomy: Types × Extraction Levels × Storage × Method

The single most important design decision in a document-ingestion pipeline is
recognizing that **different document types deserve different extraction
depths, storage forms, and processing methods**. Treating every PDF the same
way wastes effort on junk and under-extracts the valuable material.

This taxonomy has four independent axes:

1. **Document type** — what the document *is*
2. **Extraction dimension (D1–D3)** — *what kind of value* you extract:
   **D1 content** (data, prose), **D2 logic** (calculations: formulas,
   dependency graphs, macros), **D3 format** (report/template structure,
   reporting concepts). Frozen formats (PDF) only have D1; live Office
   formats carry all three — see
   [09-office-formats.md](09-office-formats.md).
3. **Extraction level (L0–L5)** — how deep you go (each dimension climbs
   the ladder independently)
4. **Method** — single-shot vs iterative processing

---

## Axis 1 — Document types

| Type | Characteristics | Typical target level | Notes |
|---|---|---|---|
| **Standard / code** | Normative clauses, dense data tables, revision-controlled | L4–L5 | Highest value; tables carry engineering constants |
| **Technical paper** (conference/journal) | Prose-heavy, few tables, figures matter | L1–L3 | Verbatim text + caption-only figures usually suffice |
| **Project / regulatory report** | Mixed prose + data, often client-confidential | L1–L4 | Route through confidentiality firewall first |
| **Form / blank template** | Proforma grids, no filled data | **Reject at L3** | Structurally table-like but carries zero data — the #1 false positive |
| **Figure/chart-dominant doc** | Imagery is the content | L0–L2 caption-only | Queue figures for a separate vision pass; text extraction is noise |
| **Scanned / image-only PDF** | No text layer | L0, or OCR→L1 with low trust | Word-count gate detects these; don't paginate noise into the wiki |
| **Datasheet / spreadsheet export** | Tabular by construction | L2–L4 | Often cleaner than PDF tables; verify units columns; expect dual export layouts within one source family |
| **Excel calculation workbook** | Live formulas, named ranges, cross-sheet graphs, macros | D2 logic → code + tests | The formula graph is the asset, not the cell values — see [09-office-formats.md](09-office-formats.md) |
| **Word report / specification** | Styled prose + explicit XML tables + tracked changes | L1–L3 + D3 template | Tables are explicit structures (more reliable than PDF detection); extract the report template once per family |
| **PowerPoint deck** | Narrative skeleton, speaker notes, pasted-image tables | D3 reporting concepts | Highly selective; pasted tables route to the vision lane like PDF figures |
| **CSV / delimited data file** | "Already structured" — silently fragile | L3–L4 + convention sidecar | Probe dialect, validate field counts, capture units/sign conventions — see [10-structured-data-and-model-files.md](10-structured-data-and-model-files.md) |
| **Analysis-model input deck** (solver ASCII/keyword files) | Model definition = engineering decisions | D2 logic → externalized YAML config | Parse to config, regenerate the deck; assumption ledger for defaults |
| **Solver output listing / export** | Block-marked text structure, multi-format per solver | L2–L4 | Auto-detect format by header inspection; sanity-gate values before use |
| **Web article / post** (blog, LinkedIn) | Short, ephemeral, link-rotted | L1 + archived source | Archive the source off-repo; cite filename not private path |
| **Catalog / brochure / minutes / newsletter** | Marketing or administrative | **Filter out pre-ingest** | Junk filter on filename + content keywords |

**Practice: route by content, not by folder.** Source archives are misfiled
grab-bags — a folder labeled with one publisher will contain papers from
another domain entirely. Classify each document by its *extracted topic*
(keyword/domain classifier on actual text), never by where it was stored.

---

## Axis 2 — Extraction levels (L0–L5)

Each level is a strict superset of the one below it. A document's frontmatter
records which level it reached (`extraction_policy`), so consumers know how
much to trust it.

### L0 — Metadata-only stub
- **What:** identity (canonical code id), publisher, revision, title,
  jurisdiction, pointer to the off-repo source file.
- **When:** image-only PDFs, junk-adjacent docs worth indexing but not
  extracting, license-restricted material.
- **Storage:** one landing page with frontmatter; no body text.

### L1 — Raw text capture
- **What:** full verbatim text via a *deterministic* extractor (PyMuPDF /
  pdftotext). Chunked into part files (~120 KB each) preserving paragraph
  structure, with page-number citations back to the source.
- **Why deterministic:** LLM-based extraction of copyrighted standards is
  refused by model guardrails and, even when it runs, yields shallow
  summaries (~2% coverage observed). A tool has no such limits and runs in
  seconds per document.
- **Storage:** landing page + `<id>-part-NNN.md` files.

### L2 — Structural extraction
- **What:** tables → one CSV each (via `find_tables()`-class detection);
  figures → caption-only queue entries (`no-csv`); watermark stripping
  *before* extraction (rotated Form-XObject watermarks silently merge their
  glyphs into table cells otherwise).
- **Trust state:** every CSV enters as `parse_status: provisional-unverified`.
- **Storage:** `datasets/<id>-table-NNN.csv` + a row in the append-only
  verification queue.

### L3 — Structural triage (automated)
- **What:** deterministic shape checks on each CSV — ragged rows, empty
  cells, single-column traps, row-collapse detection (≥6 stacked newlines in
  ≥3 columns co-occurring = likely collapsed rows).
- **Output:** `structural_status: ok | flagged | no-csv`. This is a
  *prioritization* signal for verification, not a verdict.
- **Cost:** seconds for tens of thousands of rows; always run it before
  spending vision budget.

### L4 — Verified values (vision verification)
- **What:** render the source page to PNG (~200 DPI), have a vision-capable
  model compare the CSV **cell-by-cell** against the rendered page.
- **Verdicts:** `verified` (values match; OCR noise in headers is noted, not
  blocking) / `rejected` (non-table or unrecoverable defect) /
  `deferred` (real data, wrong extraction — route to re-parse).
- **Yield observed:** ~5–7 verified per 12-row batch when batches are
  selected by numeric-data density; near 0 when selected alphabetically.

### L5 — Enriched knowledge
- **What:** cross-links between pages, citation contracts (derived constants
  emit a sidecar citation with code id + publisher + revision, failing closed
  if frontmatter is missing), domain indexes chunked for RAG, entity graphs.
- **When:** only on L4-verified material — enrichment of unverified data
  launders bad values into trusted-looking artifacts.

### Level-by-type matrix

| | L0 stub | L1 raw text | L2 structural | L3 triage | L4 verified | L5 enriched |
|---|---|---|---|---|---|---|
| Standard / code | ✓ | ✓ | ✓ | ✓ | ✓ (tables) | ✓ |
| Technical paper | ✓ | ✓ | optional | optional | rarely | citations only |
| Report | ✓ | ✓ | ✓ | ✓ | high-value tables | per-need |
| Form / template | — | — | (auto-extracted) | **reject here** | — | — |
| Figure-dominant | ✓ | caption-only | queue figures | no-csv bucket | vision pass | — |
| Scanned | ✓ | OCR, low trust | — | — | — | — |
| Excel calc workbook | ✓ | formula dump | formula graph + worked examples | cached-value classification | re-execution vs `cached_ok` cells | ported code + tests |
| Word report | ✓ | ✓ | XML tables | ✓ | high-value tables | report template |
| PowerPoint deck | ✓ | notes + claims | — | — | pasted tables via vision | reporting concepts |
| CSV / delimited | ✓ | n/a (born structured) | dialect-probed parse | field-count + content-hash | convention sidecar reviewed | joined datasets |
| Solver input deck | ✓ | raw deck text | parsed parameters | round-trip identity check | config ↔ deck regeneration | YAML config library |
| Solver output | ✓ | listing text | block-aware parse | format auto-detection | sanity gates + cross-format parity | results database |
| Web article | ✓ | ✓ | — | — | — | link only |

---

## Axis 3 — Method: single-shot vs iterative

### Single-shot
One document, one pass, human-in-the-loop end to end.

- **Fits:** small batches (<20 docs), born-digital documents, exploratory
  ingestion of a new document type (to learn its failure modes before
  automating).
- **Shape:** extract → eyeball → commit. No state file, no queue.
- **Risk:** doesn't scale; tempts you to skip the provisional/verified
  distinction because "I looked at it."

### Iterative (resumable campaign)
A state-machine-driven loop that survives interruption and runs unattended.

- **Fits:** corpora of hundreds-to-tens-of-thousands of documents; anything
  on a cron.
- **Key properties (all four are load-bearing):**
  1. **Chunked work units** (e.g., 5–12 docs/chunk, grouped by publisher)
     with a JSON state file marking completed chunks → idempotent resume.
  2. **Isolated workspaces** per chunk (git worktrees) so parallel or
     interrupted runs never corrupt each other.
  3. **Append-only shared files** (queues, indexes, logs) with a union merge
     driver, so concurrent branches merge without conflicts — *and*
     dedup-on-write to self-heal when union-merge duplicates rows.
  4. **One PR per tick**, never auto-merged. Batching all publishers onto one
     branch per cron tick (instead of one PR each) eliminated chronic
     merge churn. A human gates every merge.

### Iterative verification loops (a second, distinct loop)
Verification is its own iterative process layered on top:

- **Select** a batch (~12 rows) by data density, sinking row-collapse
  suspects to the bottom.
- **Verify** with vision, **commit** verdicts, **PR**, **merge**.
- **Serialize per domain:** never select a domain's next batch until the
  prior batch's PR is merged — the selector reads the main branch, and an
  unmerged batch makes it re-pick the same rows.
- **Re-parse loop:** `rejected`-with-defect-class rows are not dead; they
  route to an improved extractor (e.g., watermark stripper, header-splitter)
  and re-enter at L2.

### Choosing a method

| Situation | Method |
|---|---|
| New document type, unknown failure modes | Single-shot first (5–10 docs), then automate |
| Known type, large corpus | Iterative campaign with state file |
| Table verification at any scale | Iterative batch loop, serialized per domain |
| Post-fix re-extraction | Targeted iterative re-parse over the affected doc only, mapped by page + in-page table order, with shape-preservation as the correctness proof |
