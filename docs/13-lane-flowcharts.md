# Lane Flowcharts: One per Raw Data Type

Operational flowcharts for every source type in the taxonomy (doc 01).
Rendered natively by GitHub (Mermaid). Each chart encodes the lane's docs +
GPs; chart titles link back to the governing doc.

## 0. Master routing — every raw file enters here

```mermaid
flowchart TD
    A[Raw file in archive] --> B{Junk filter<br>catalog/brochure/minutes?}
    B -- junk --> Z1[Skip + record reason<br>_skipped log]
    B -- keep --> C{Probe actual content<br>not folder or filename}
    C -- "PDF, has text layer" --> D1[PDF lane — chart 1]
    C -- "PDF, no text layer<br>(word-count gate)" --> D2[Scanned lane — chart 2]
    C -- "image file" --> D3[Photo lane — chart 3]
    C -- "xlsx/xls: formula-dense" --> D4[Calculation Excel — chart 4]
    C -- "xlsx/xls: data-dense" --> D5[Data Excel/CSV — chart 5]
    C -- "xlsx: image-canvas" --> D3
    C -- "docx" --> D6[Word lane — chart 6]
    C -- "pptx" --> D7[Deck lane — chart 7]
    C -- "solver input deck" --> D8[Model-file lane — chart 8]
    C -- "solver output/listing" --> D9[Results lane — chart 9]
    C -- "html/url" --> D10[Web lane — chart 10]
    D2 -. GP-39 reclassify by scanned structure .-> C
```

## 1. Born-digital PDF (standards / codes / papers) — [docs 01–03]

```mermaid
flowchart TD
    A[PDF] --> B[Decrypt if needed]
    B --> C[Strip rotated watermarks<br>in-memory only — GP-03]
    C --> D[Deterministic extraction<br>text + tables — GP-01]
    D --> E[Landing page L0-L1<br>frontmatter + part files]
    D --> F[Table CSVs — L2<br>parse_status: provisional]
    F --> G[Structural triage — L3<br>ok / flagged / no-csv]
    G --> H[Queue, append-only<br>dedup-on-write — GP-12]
    H --> I[Batch select ~12 rows<br>by data density — GP-06]
    I --> J[Render page PNG<br>vision verify cell-by-cell<br>rightmost column! — GP-07]
    J -- values match --> K[verified — L4]
    J -- non-table / garble --> L[rejected + defect class]
    J -- real data, bad extraction --> M[deferred]
    L & M --> N{Extractor improved?}
    N -- yes --> O[Re-parse affected class<br>map by page + order — GP-11]
    O --> F
    K --> P[L5 enrichment<br>citations, RAG chunks]
    J -. GP-08 serialize per domain, merge before next select .-> I
```

## 2. Scanned document — [doc 11]

```mermaid
flowchart TD
    A[Image-only PDF / scan] --> B[Quality gate<br>OpenCV blur score, deskew]
    B -- too poor --> Z[L0 metadata stub<br>+ source pointer]
    B --> C{Content value<br>justifies OCR?}
    C -- no --> Z
    C -- yes --> D[OCR<br>output labeled ocr-interpreted<br>NEVER raw-extracted — GP-38]
    D --> E[Declare extraction_estimate<br>record extraction_yield]
    D --> F{Tables present?}
    F -- yes --> G[Enter verification queue<br>expect high reject rate]
    G -- high-value table --> H[Manual digitization<br>+ vision verification]
    F -- drawing --> I[Describe: title block verbatim,<br>revision, what it depicts]
    E & H & I --> J[Wiki pages marked<br>as interpretation]
```

## 3. Photograph — [doc 11]

```mermaid
flowchart TD
    A[Photo] --> B[Extract capture metadata<br>EXIF: date, location]
    B --> C[Perceptual-hash dedup<br>against existing series]
    C -- near-duplicate --> Z[Link to existing frame]
    C -- new --> D[Vision description record:<br>falsifiable observations — GP-10/38<br>verbatim legible text<br>uncertainties listed]
    D --> E[Separate observation<br>from inference]
    E --> F[Independent 2nd description<br>adversarial spot-check]
    F -- conflict --> G[Prefer verdict citing<br>falsifiable specifics]
    F -- agree --> H[Description record published<br>extraction_policy: described]
    H --> I[Dated-series index<br>evidence timeline]
```

## 4. Calculation Excel — [doc 09]

```mermaid
flowchart TD
    A[Workbook corpus] --> B[Auto-scan inventory — GP-27<br>sheets, formulas, function mix,<br>cross-sheet refs]
    B --> C[Tier: priority P0-P2<br>× complexity 1-6]
    C --> D[Per workbook:<br>read formula graph - openpyxl]
    D --> E[Classify cells — GP-28<br>cached_ok / missing / suspect]
    D --> F[Detect repetition patterns — GP-29<br>formula regions → loops]
    F --> G[Port to code<br>worked examples → TDD fixtures]
    G --> H[Verify: re-execute vs<br>cached_ok cells - oracle]
    H -- mismatch --> F
    H -- match --> I[Strip client context — GP-31<br>deny-list scan]
    I --> J[Commit code + tests with<br>source-workbook traceability]
    J --> K{Integrated into<br>live modules?}
    K -- no --> L[STOP widening funnel — GP-30<br>integrate first]
    K -- yes --> B
```

## 5. Data Excel / CSV / delimited — [doc 10]

```mermaid
flowchart TD
    A[Delimited file / data export] --> B[Probe dialect — GP-32<br>delimiter, quoting, encoding,<br>line endings - CleverCSV-class]
    B --> C{Known export family?}
    C -- new layout --> D[Single-shot: learn layout<br>auto-detect by header inspection]
    C -- known --> E[Field-count validation<br>per row vs header — GP-32]
    D --> E
    E -- mismatch --> Z[Quarantine row + reason]
    E --> F[Content-parity check<br>cell hashes, not row counts — GP-33]
    F --> G[Convention sidecar — GP-34<br>units, signs, frames<br>frictionless-class schema]
    G --> H[Schema asserts in pipeline<br>pandera-class]
    H --> I[Dataset published with<br>provenance + sidecar]
```

## 6. Word report / specification — [doc 09]

```mermaid
flowchart TD
    A[DOCX] --> B[Parse XML structure<br>python-docx / stdlib zip fallback]
    B --> C[Prose → L1 parts<br>with heading hierarchy]
    B --> D[Tables → explicit XML structures<br>still enter provisional]
    B --> E[Tracked changes + comments:<br>capture or consciously discard]
    B --> F{Embedded OLE/Excel?}
    F -- yes --> G[Route to Calculation<br>Excel lane — chart 4]
    C --> H[First doc of a family?<br>Extract report template — D3<br>styles, sections, captions]
    D --> I[Verification queue<br>same as PDF tables]
    H --> J[Reporting-concept page<br>for generated reports]
```

## 7. PowerPoint deck — [doc 09]

```mermaid
flowchart TD
    A[PPTX] --> B{Selective filter:<br>does this deck define how<br>results are communicated?}
    B -- no --> Z[L0 stub or skip]
    B -- yes --> C[Slide text + speaker notes<br>notes often hold the real explanation]
    C --> D{Tables?}
    D -- pasted images --> E[Vision lane<br>same as PDF figures]
    D -- native --> F[Provisional CSVs]
    C --> G[Extract narrative skeleton — D3<br>problem → method → results →<br>recommendation + chart choices]
    G --> H[Named reporting concepts<br>not one-off slide dumps]
```

## 8. Solver input deck — [doc 10]

```mermaid
flowchart TD
    A[Solver ASCII deck] --> B[Parse to externalized<br>YAML config — GP-36<br>no solver license needed]
    B --> C[Round-trip check:<br>config → deck → config<br>must be identity]
    C -- fails --> D[Fix parser/generator<br>before anything else]
    C -- passes --> E[Config = the reviewed,<br>git-tracked artifact]
    E --> F["(a) Q&A: detect missing inputs<br>ask user; defaults provenance-tagged<br>in assumption ledger — GP-37"]
    F --> G["(b) regenerate solver deck<br>from config + ledger"]
    G --> H["(c) run (license needed here only)"]
    H --> I[Output sanity gates:<br>physical range + coverage — GP-37]
    I -- fail --> F
    I -- pass --> J[Results published with<br>assumption ledger attached]
```

## 9. Solver output / results listing — [doc 10]

```mermaid
flowchart TD
    A[Solver output file] --> B[Auto-detect format<br>by header inspection — never filename]
    B -- native export --> C[Block-aware parser<br>text-marked blocks ≠ flat table]
    B -- pipeline export --> D[Clean-column parser]
    C & D --> E[Cross-format parity check<br>when both exist for one run]
    E --> F[Physical-range + coverage<br>sanity gates]
    F -- fail --> Z[Quarantine + investigate<br>never publish]
    F -- pass --> G[Results database with<br>run provenance]
```

## 10. Web article / post — [doc 01]

```mermaid
flowchart TD
    A[URL] --> B[Archive source off-repo<br>link rot is certain]
    B --> C[Extract text + claims — L1]
    C --> D[Source page cites archived<br>filename, never private paths]
    D --> E[Wiki source page<br>with publication metadata]
```

---

### Reading the charts

- **Every lane ends in a labeled trust state** — nothing is published
  without `verified` / `described` / `ocr-interpreted` / sidecar provenance.
- **Dashed edges** are the discipline rules that exist because a batch broke
  without them (the GP references).
- The master router (chart 0) is itself GP-04: classify by probed content,
  never by folder, filename, or extension alone.
