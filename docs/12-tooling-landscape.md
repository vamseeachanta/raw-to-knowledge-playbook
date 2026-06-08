# Vetted Tooling Landscape (researched & license-verified, 2026-06)

Open-source tools worth integrating, per lane. Every entry was checked
against its repo for **license**, **maintenance signal** (recent releases /
commit activity), and **fidelity evidence** (benchmarks where they exist).
Verdicts use the trust rubric below. Re-verify before adoption — this
landscape moves fast (snapshot: June 2026).

## Trust rubric

A tool earns **ADOPT** only if it clears all four gates:

| Gate | Test |
|---|---|
| **License** | Permissive (MIT/BSD/Apache-2.0) for anything that might ship; GPL/AGPL tools only process-isolated or internal-only, recorded in a license register |
| **Maintenance** | Release or meaningful commits within ~6 months; not a one-person abandonware risk for a core dependency |
| **Evidence** | Independent benchmark or production reputation, not just a README claim |
| **Integration cost** | Fits as a *component* in our pipeline — we adopt libraries and patterns, never migrate to someone else's framework runtime |

**EVALUATE** = promising, needs a bounded pilot before adoption.
**AVOID** = license, staleness, or lock-in disqualifies it.

---

## Lane 1 — PDF text & layout (docs 01–02)

| Tool | License | Verdict | Why |
|---|---|---|---|
| **Docling** (IBM / Linux Foundation) | MIT (code), Apache-2.0 (VLM) | **ADOPT** | Best fidelity/license/maintenance combo; structured `DoclingDocument` output; 97.9% complex-table cell accuracy in an independent benchmark; peer-reviewed (AAAI 2025) |
| **pdfplumber** | MIT | **ADOPT** | License-clean text + geometry; the natural permissive fallback to PyMuPDF |
| **pypdf** | BSD-3 | **ADOPT** | PDF operations (split/merge); not an extractor |
| **PyMuPDF** | ⚠️ **AGPL-3.0** | **KEEP, FLAGGED** | Fastest extractor (~8–12× pdfplumber) — fine for an internal, non-distributed pipeline, but AGPL obligations trigger on distribution or network service. Record in the license register; keep pdfplumber/Docling as the exit path |
| **MinerU** | ⚠️ Custom Apache-derivative (relicensed from AGPL, 2026-04) | EVALUATE | Strong all-rounder, esp. mixed/scanned; read the custom license clauses first |
| **unstructured** (OSS) | Apache-2.0 | EVALUATE | Great typed-element model (`Title/Table/NarrativeText` + page/coords) for normalization; weak on complex tables; heavy dependency tree — vendor selectively |
| **markitdown** (Microsoft) | MIT | EVALUATE | One-call Office/PDF→Markdown convenience; lossy on complex tables — first-pass only |
| **Apache Tika** | Apache-2.0 | EVALUATE | Format detection + text fallback across 1000+ types; JVM service |
| **marker** | ⛔ GPL + revenue-gated weights | AVOID | License double-bind for integration |
| **MegaParse** | Apache-2.0, stale (no release ~15 mo) | AVOID | Superseded by Docling/MinerU |

## Lane 2 — Table extraction (docs 02–03)

| Tool | License | Verdict | Why |
|---|---|---|---|
| **gmft** | MIT | **ADOPT (pilot first)** | Wraps Microsoft Table-Transformer; CPU-only, light deps; strong on scientific/standards tables; CSV-native — the prime candidate to cut our table defect classes (A2–A6) |
| **Camelot v2** | MIT | **ADOPT (pilot first)** | Deterministic "lattice" extraction for *ruled* tables — ideal for engineering-code tables; new ML flavor for borderless |
| **table-transformer** (Microsoft) | MIT | ADOPT via gmft | The underlying SOTA structure model; use raw only to fine-tune |
| **tabula-py** | MIT, slowing | AVOID | Camelot covers it, fresher |

## Lane 3 — OCR & scans (doc 11)

| Tool | License | Verdict | Why |
|---|---|---|---|
| **PaddleOCR / PP-StructureV3** | Apache-2.0 | **ADOPT** | Best permissive accuracy incl. table/layout structure (96.3% OmniDocBench); only friction is the PaddlePaddle dependency |
| **Tesseract** | Apache-2.0 | **ADOPT (baseline)** | Mature CPU fallback for clean printed text |
| **docTR** | Apache-2.0 | EVALUATE | Fully-permissive modular alternative if the Paddle dep is unwanted |
| **olmOCR** (AllenAI) | Apache-2.0 | EVALUATE | Top-tier VLM OCR (equations, hard scans); needs ≥12 GB GPU |
| **OpenCV** preprocessing | Apache-2.0 | **ADOPT** | Deskew/denoise + **Laplacian-variance blur gate** — a cheap, defensible "scan too blurry → stays provisional" signal |
| **surya** | ⚠️ weights free <$5M revenue | EVALUATE | Excellent, but revenue-thresholded weights — check applicability |
| **unpaper** | ⛔ GPL-2.0 | CLI-only if at all | OpenCV covers the need permissively |
| **Nougat** (Meta) | ⛔ NC weights, abandoned | AVOID | Superseded |
| **LayoutParser** | Apache-2.0, discontinued | AVOID | Use Docling/Paddle layout instead |

## Lane 4 — Excel logic & Office (doc 09)

| Tool | License | Verdict | Why |
|---|---|---|---|
| **openpyxl** | MIT | **ADOPT** | Reads formula strings + cell graph; the universal base (slow cadence, stable) |
| **python-calamine** | MIT (Rust core) | **ADOPT** | Fastest bulk *data* reads (pandas `engine="calamine"`) |
| **formulas** | ⚠️ EUPL-1.1 (reciprocal, incl. SaaS) | EVALUATE, arm's length | Best-maintained formula evaluator + dependency DAG; use as a *library/CLI oracle* generating expected outputs for hand-ported code — don't redistribute derivatives; counsel check before bundling |
| **xlcalculator** | MIT | EVALUATE | The only permissive evaluator; narrower function coverage, stale releases — copyleft-free fallback |
| **pycel / koala2** | ⛔ GPL-3.0 | AVOID in product | Internal one-off migration use only |
| **oletools / olevba** | BSD-2 (core) | **ADOPT, caveat** | VBA macro source extraction; ⚠️ its optional `pcodedmp` dep is GPLv3 — skip the P-code path |
| **python-docx / python-pptx** | MIT | **ADOPT** | De-facto structured Word/PPT access (headings, tables, shapes, styles) |
| **mammoth** | BSD-2 | **ADOPT** | docx → *semantic* Markdown via styles — exactly the D3 report-template extraction |

**Key finding:** there is **no actively-maintained, permissive, high-coverage
Excel formula evaluator**. The working pattern: `openpyxl` reads the formula
graph → `formulas` (arm's length) recalculates as the *test oracle* → the
ported Python is hand/agent-written and verified against the oracle on
`cached_ok` cells (GP-28).

## Lane 5 — CSV / delimited / validation (doc 10)

| Tool | License | Verdict | Why |
|---|---|---|---|
| **CleverCSV** | MIT | **ADOPT** | Research-grade dialect detection (~97%, +21% over stdlib `Sniffer`) — the front door for every delimited file (GP-32 automated) |
| **frictionless-py** | MIT | **ADOPT** | Table Schema + Data Package **metadata sidecars** — a standard for exactly our GP-34 convention sidecar |
| **pandera** | MIT | **ADOPT** | Lightweight in-pipeline dataframe schema asserts |
| **csvkit** | MIT | ADOPT (CLI tier) | Shell-level inspection/wrangling |
| **Great Expectations** | Apache-2.0 | EVALUATE | Heavyweight; only if a governed expectation catalog is needed |
| **visions** | ⚠️ BSD-4 (advertising clause) | EVALUATE | Type inference; minor compliance friction |

## Lane 6 — Imagery & photo evidence (doc 11)

| Tool | License | Verdict | Why |
|---|---|---|---|
| **ImageHash** | BSD-2 | **ADOPT** | Perceptual hashing (pHash + Hamming threshold) for dated-series dedup |
| **Pillow / ExifRead** | MIT-CMU / BSD-3 | **ADOPT** | In-process EXIF capture metadata |
| **ExifTool** | ⚠️ GPL or Artistic | ADOPT as separate process | Gold standard for full IPTC/XMP/GPS; process isolation keeps our code clear |
| **Qwen-VL family** (open VLM) | Apache-2.0 | **ADOPT (self-host track)** | Strongest open VLM for on-prem photo description of confidential archives |
| Hosted vision (Claude/GPT) | proprietary API | ADOPT (default track) | Highest quality where data sensitivity permits; all VLM output enters the provisional→verified gate as a *claim* |
| **Florence-2** | MIT | EVALUATE | Cheap captioning/region tasks, not rich description |
| **PaliGemma 2** | ⚠️ Gemma license (non-OSI) | EVALUATE | Review use restrictions first |

## Lane 7 — Chunking, retrieval & evaluation patterns (docs 14–15)

Expanded with license-screened verdicts and primary-source evidence in
[doc 14 (chunking & embedding)](14-chunking-and-embedding.md) and
[doc 15 (retrieval evaluation)](15-retrieval-evaluation.md). Patterns to
**borrow** (not frameworks to migrate to):

| Component / pattern | Source | License | Why |
|---|---|---|---|
| **HybridChunker + contextualize()** | Docling | MIT | Structure-aware chunking that never slices tables/headings; metadata-enriched chunk text |
| **Contextual Retrieval** | Anthropic (technique) | n/a | Prepend 50–100-token context per chunk before embedding; ~35–67% retrieval-failure reduction reported |
| **Ingestion dedup via content-hash docstore** | LlamaIndex `IngestionPipeline` | MIT | Borrow the pattern: hash → skip re-ingest |
| **Human-in-the-loop chunk review** | RAGFlow | Apache-2.0 | Visual accept/correct before promotion — mirrors our provisional→verified gate |
| **RAGAS context precision/recall** | RAGAS | Apache-2.0 | Puts a number on "did chunking surface the right material" |
| **Citation ID = doc version + content hash** | RAG-citation writeups | pattern | Provenance bound as structured metadata, not answer text — fabrication-resistant; matches our fail-closed citation contract |
| LangChain loader wrappers | — | — | **AVOID**: indirection + churn; call the underlying libraries directly |
| LlamaParse (SaaS) | — | proprietary | **AVOID** for private archives: data egress + lock-in |

---

## License register (flags to carry)

| Dependency | License | Containment |
|---|---|---|
| PyMuPDF | AGPL-3.0 | Internal-only; never distribute/serve; exit path = pdfplumber/Docling |
| formulas | EUPL-1.1 | Arm's-length oracle use; no derivative redistribution |
| ExifTool | GPL/Artistic | Separate-process invocation only |
| pcodedmp (oletools extra) | GPL-3.0 | Excluded from installs |
| surya weights | OpenRail-M (<$5M rev) | Verify threshold before use |
| marker, pycel, koala2, unpaper | GPL family | Not integrated |

## Credible written resources (verified)

1. Docling technical report (AAAI 2025) — arxiv.org/abs/2501.17887
2. OmniDocBench (CVPR 2025) document-parsing benchmark — github.com/opendatalab/OmniDocBench
3. CleverCSV dialect-detection paper — van den Burg et al., *Data Mining and Knowledge Discovery* 33 (2019)
4. EuSpRIG spreadsheet-risk research & horror stories — eusprig.org (the evidence base for GP-28/30: ~88% of spreadsheets contain errors)
5. Frictionless Data specifications (Table Schema / Data Package) — specs.frictionlessdata.io
6. Anthropic Contextual Retrieval — anthropic.com/news/contextual-retrieval
7. RAGAS retrieval-quality metrics — github.com/explodinggraphs/ragas

---

*Snapshot 2026-06. Tools age; verdicts don't transfer across years. Re-run
the rubric before adopting anything from this page.*
