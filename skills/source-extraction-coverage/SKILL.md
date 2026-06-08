---
name: source-extraction-coverage
description: >
  Runs doc-type-aware deterministic extraction on a source and makes shallow
  extraction visible by recording an extraction_estimate before and an
  extraction_yield after, flagging any source whose yield falls short. Use when
  ingesting a new source file (PDF/DOCX/XLSX/HTML/scanned) into the provisional store.
license: CC-BY-4.0
compatibility: Requires a deterministic extractor per doc type (pdfplumber/Docling, python-docx, openpyxl, OCR) and a landing-page frontmatter store
metadata:
  version: "1.0"
  enforcement_level: L2            # callable + frontmatter validator script
  status: template
  incident_refs: coverage-2pct,A-defects,D4
  params: "path:str | type:enum(auto,pdf,docx,xlsx,html,scanned)=auto"
---

# source-extraction-coverage

> Template skill (doc 08, doc 01). The estimate/yield pair is the whole point:
> it is how the 2%-coverage failure (LLM-extracted a doc and silently produced
> ~2% of its text) becomes a loud, machine-checkable signal instead of a silent
> loss.

## Trigger
`/extract-source <path> [--type auto|pdf|docx|xlsx|html|scanned]`

## Preconditions
1. Source lives in the off-repo read-only archive; record its `sha256`.
2. Type is detected by content/structure, **not filename** (incident D4:
   names lie about content).

## Steps
1. **Estimate first.** Before extracting, declare `extraction_estimate` in the
   landing-page frontmatter: roughly how much extractable content this source
   holds (page count, table count, "text-heavy" vs "image-only"). This is a
   commitment made *before* you see the result, so a shortfall is undeniable.
2. **Pick the recipe by type** (use ADOPT-tier permissive tools from doc 12):
   - `pdf` (born-digital): deterministic text+geometry (pdfplumber/Docling);
     `pdf` (scanned/image-only) → route to the `scanned` recipe (OCR as
     labeled interpretation, doc 11).
   - `docx`: structured access (python-docx) + semantic Markdown (mammoth).
   - `xlsx`: formula-graph read (openpyxl) / fast data read (calamine) —
     classify by scanned structure, not sheet names (D4).
   - `html`: typed-element extraction; strip nav/boilerplate.
   - `scanned`: OCR with a blur gate (OpenCV Laplacian-variance → too blurry
     stays provisional); OCR output is a *claim*, not source text.
3. **Extract deterministically.** Tools, not an LLM, do the bulk copy. (LLM
   bulk extraction yielded ~2% coverage — never the bulk path.)
4. **Record yield.** Write `extraction_yield` after extraction (pages/tables
   actually produced, % of estimate).
5. **Flag shortfall.** If `yield << estimate`, mark the source
   `extraction: shallow` and queue it for a different recipe. Do not let it
   pass as "done."

## Verification
- Frontmatter has BOTH `extraction_estimate` (pre) and `extraction_yield`
  (post); a validator script rejects a page missing either.
- Sources flagged `shallow` appear in the re-extraction backlog, not the
  trusted set.

## Cleanup
- Raw source never copied into any repo; only derived parts + a `sources:`
  sha256 pointer.

## Incident appendix
| Rule | Why |
|---|---|
| Estimate before, yield after | The 2%-coverage loss was invisible until the pair made it loud |
| Classify on structure not name | D4: sheet/file names misclassify content |
| OCR output is a claim | doc 11: scanned text is interpretation, enters the provisional gate |
