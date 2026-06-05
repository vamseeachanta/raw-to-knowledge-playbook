# Office Formats: Excel, Word, PowerPoint — Ingesting Logic and Format, Not Just Content

PDF ingestion (docs 01–04) deals with **frozen** documents: the only thing
to extract is content. Office formats are **live artifacts** — they carry
three separable kinds of value, and a pipeline that only extracts "the text"
throws away most of it:

| Dimension | What it is | Where it lives |
|---|---|---|
| **D1 — Content** | Data values, prose, results | Cell values, paragraphs, slide text |
| **D2 — Logic** | The calculation itself | Excel formulas, named ranges, cross-sheet dependency graphs, VBA/macros |
| **D3 — Format** | The reporting concept | Workbook layout conventions, Word styles/templates, deck narrative structure, chart designs |

The extraction *levels* (L0–L5 in
[01-document-taxonomy.md](01-document-taxonomy.md)) still apply, but each
dimension climbs the ladder separately. A workbook can be L1 on content
(values dumped) while its logic is still L0 (formulas never captured) — and
the logic is usually why the file exists.

---

## Excel workbooks (the calculation lane)

The most valuable and most mature lane. Observed corpus: thousands of legacy
engineering-calculation workbooks (one inventory: 4,125 files concentrated
in three analysis domains), each a *de facto* validated calculation tool.

### Pipeline: discovery → triage → extraction → code → round-trip

```
1. INVENTORY   auto-scan every workbook (openpyxl-class tooling):
               sheet names, dimensions, formula counts, function
               histogram, cross-sheet references
2. TIER        rank by priority (P0–P2) × complexity tier (1–6);
               budget extraction effort per tier
3. EXTRACT     formulas + named ranges + input blocks + worked examples
4. COMPRESS    detect row/column repetition patterns → emit loops,
               not cell-by-cell transliterations (observed 2.5×–44×
               compression of formula count to code lines)
5. PORT        generate code in the target library, with tests
6. ROUND-TRIP  every code artifact records its source workbook
               (workbook → code mapping is the provenance chain)
```

### Excel-specific rules (all incident-backed)

**Cached values are not ground truth.** A workbook saved without
recalculation carries stale or missing cached results. For test oracles,
classify each cell — `cached_ok` / `cached_missing` / `cached_suspect` —
and emit assertions only for `cached_ok` cells. Blindly asserting cached
values makes TDD against the workbook infeasible.

**Extract the algorithm, not the cells.** A formula region that repeats
down 500 rows is one loop, not 500 expressions. Pattern detection before
code generation is what makes conversion tractable (and is also the right
*scope estimator*: compression ratio predicts conversion effort).

**Wire extractions into live code before extracting more.** A pipeline that
extracted 656K+ formulas from just 6 workbooks produced stubs that sat
unintegrated — extraction outpaces integration by orders of magnitude.
Highest ROI is always: integrate what's extracted, *then* widen the funnel.

**Strip client context; keep methodology.** Legacy workbooks mix validated
engineering logic with client-confidential data. The extraction target is
the *generic* methodology: equations, input ranges, validation cases,
worked examples (which become TDD fixtures for the ported code). Client
identifiers, project names, and proprietary data never leave the boundary;
a deny-list scan runs before anything is archived. Never copy the raw
workbook forward — only the distilled logic.

**Expect format variation within one source family.** Even a single tool's
exports can use two different XLSX layouts (block-structured matrices vs
flat tables) requiring dual-path parsing. Probe the structure; don't assume.

### What "verified" means for a calculation

The vision-verification model from PDFs translates as:

| PDF lane | Excel lane |
|---|---|
| Render page ↔ CSV cell-by-cell | Re-execute ported code ↔ workbook outputs on `cached_ok` cells |
| `verified` table | Calculation reproduces workbook results across worked examples |
| Defect-classed `deferred` | Formula regions pending macro/VBA or circular-reference handling |

---

## Word documents (the report lane)

Word documents in an engineering ecosystem are mostly **reports and
specifications** — prose plus embedded tables, with the *format* (section
structure, style conventions) often as reusable as the content.

- **Content (D1):** DOCX is a ZIP of XML — when a parsing library isn't
  available in the environment, stdlib `zipfile` + XML parsing of
  `word/document.xml` extracts paragraphs/runs with zero added
  dependencies. Tables extract more reliably than from PDF (they're
  explicit XML structures, not detected regions) — but still enter as
  provisional.
- **Logic (D2):** rare (embedded OLE/Excel objects — route those to the
  Excel lane).
- **Format (D3):** heading hierarchy, caption conventions, and boilerplate
  sections constitute a *report template* — extract once per document
  family and store as a reporting-concept page, so generated reports can
  target the same shape.
- Track changes / comments are content too: they record engineering
  decisions. Capture or consciously discard them — never silently lose
  them.

## PowerPoint decks (the reporting-concepts lane)

Decks carry the least verbatim data and the most **distilled reporting
concepts**: what gets summarized, in what order, with what visuals. This
lane is the least mature in our practice — treat the guidance below as
design intent pending field validation (per
[CONTRIBUTING.md](../CONTRIBUTING.md), it graduates to a GP only with
evidence).

- **Content (D1):** slide text + speaker notes (notes often contain the
  real explanation); tables on slides are usually pasted images → route to
  the vision lane, same as PDF figures.
- **Format (D3) is the prize:** the narrative skeleton (problem → method →
  results → recommendation), the chart types chosen per result kind, and
  the summary-table layouts are reusable *reporting templates*. Extract
  them as named report concepts, not as one-off slide dumps.
- Junk filter applies double: most decks are presentation-of-record;
  ingest the few that define how results should be communicated.

---

## Updated type × dimension × method map

| Source | D1 content | D2 logic | D3 format | Method |
|---|---|---|---|---|
| Excel calc workbook | values (low value alone) | **primary target** — formula graph → code + tests | layout conventions for calc reports | Iterative: inventory → tier → convert; serialize integration with extraction |
| Excel data export | **primary target** | n/a | dual-path parse variants | Single-shot per format family, then automate |
| Word report/spec | prose + explicit tables | embedded objects → Excel lane | **report template** (extract once per family) | Single-shot per family |
| PowerPoint deck | notes + key claims | n/a | **reporting concepts** (narrative + visuals) | Single-shot, highly selective |
| PDF (docs 01–04) | text + tables | n/a | n/a | Iterative campaign |

The common thread with the PDF lane is unchanged: **deterministic tools
extract; everything enters provisional; verification re-derives the result
from the source** (re-execution for logic, vision for values, human review
for format concepts).
