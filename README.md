# Raw-to-Knowledge Playbook

A field-tested methodology for turning a heterogeneous archive of raw
sources — PDFs (engineering standards, codes, papers, reports), **live
Office artifacts** (calculation and data Excel, Word reports, PowerPoint
decks), **machine-oriented files** (CSV/delimited data, analysis-solver
input decks and output listings), and **imagery** (photographs to be
described, scanned documents to be OCR-interpreted) — into a verified,
citable, LLM-queryable knowledge base — using a **multi-agent pipeline**
that combines deterministic extraction tools with LLM-based verification
and review.

For frozen formats (PDF) the target is *content*; for live formats the
pipeline also extracts **calculation logic** (formula graphs → tested code)
and **reporting concepts** (report/template structure) — three distinct
extraction dimensions (see docs 01 and 09). For imagery there is nothing to
copy at all: photos and scans are **described/interpreted**, and the
playbook keeps that trust distinction explicit end-to-end (doc 11).

Everything here was distilled from a real, ongoing ingestion campaign:

| Scale dimension | Value (as of 2026-06) |
|---|---|
| Wiki pages produced | ~24,000 markdown pages |
| Tables extracted to CSV | ~18,300 |
| Publishers ingested | 13 (ISO, API, ASTM, BSI, DNV, IEC, NORSOK, NACE, NEMA, HSE, MIL, SNAME, OnePetro) |
| Vision-verification batches run | 80+ (≈450 tables verified cell-by-cell) |
| Excel calculation workbooks inventoried | 4,100+ (tiered for logic→code conversion; 656K+ formulas extracted in pilots) |
| Automation cadence | 6-hourly resumable cron, one PR per tick |
| Agent providers used | 3 (Claude for orchestration/verification, Codex for bulk dispatch/review, Gemini for review fallback) |

This is a **living document set**: new practices are appended as the work
continues. See [CONTRIBUTING.md](CONTRIBUTING.md) for how entries are added.

## The core idea

> **Extract deterministically. Verify with vision. Trust nothing by default.**

1. **Deterministic tools (not LLMs) do the bulk extraction.** PDF-to-text
   libraries reproduce 100% of source text in seconds; LLM-based extraction of
   the same document yielded ~2% coverage and is slow, expensive, and
   unreliable for verbatim reproduction.
2. **Everything auto-extracted is `provisional` until verified.** Auto-parsed
   tables are *structurally consistent but value-wrong* often enough that
   publishing them unverified would poison the knowledge base.
3. **LLMs verify, route, and review** — vision models compare rendered source
   pages against extracted CSVs cell-by-cell; reviewer agents adversarially
   audit pipeline code; orchestrator agents batch and serialize the work.

## Start here

New to this? **Run the core idea before reading the docs.**
[`QUICKSTART.md`](QUICKSTART.md) walks you through a real extract → provisional →
verify → promote loop on one table in ~15 minutes, backed by the runnable
[`examples/minimal-ingest/`](examples/minimal-ingest/) (one permissive
dependency, offline). Then come back to the document map below.

## Document map

| Doc | Contents |
|---|---|
| [docs/01-document-taxonomy.md](docs/01-document-taxonomy.md) | Document types × extraction levels × storage forms × method (single-shot vs iterative) |
| [docs/02-pipeline-architecture.md](docs/02-pipeline-architecture.md) | Reference architecture: dispatcher, state machine, union-merge, PR batching |
| [docs/03-verification-playbook.md](docs/03-verification-playbook.md) | The vision-verification loop: batch selection, verdict taxonomy, status lifecycle |
| [docs/04-failure-modes.md](docs/04-failure-modes.md) | 16 documented failure modes with root causes and mitigations |
| [docs/05-good-practices.md](docs/05-good-practices.md) | Numbered, extensible catalog of practices (the living core of this repo) |
| [docs/06-multi-agent-orchestration.md](docs/06-multi-agent-orchestration.md) | Splitting work across agent providers; concurrency, serialization, adversarial review |
| [docs/07-data-governance.md](docs/07-data-governance.md) | Provenance, licensing firewall, public/private routing, citation contracts |
| [docs/08-skills-catalog.md](docs/08-skills-catalog.md) | Reusable agent skills built for this work and how they're structured |
| [docs/09-office-formats.md](docs/09-office-formats.md) | Excel/Word/PowerPoint: extracting calculation logic and reporting formats, not just content |
| [docs/10-structured-data-and-model-files.md](docs/10-structured-data-and-model-files.md) | CSV/delimited files and solver ASCII formats: dialect probing, convention sidecars, deck→config round-trips |
| [docs/11-imagery-and-scans.md](docs/11-imagery-and-scans.md) | Photographs (described, not extracted) and scanned documents (OCR as labeled interpretation) |
| [docs/12-tooling-landscape.md](docs/12-tooling-landscape.md) | Vetted OSS tooling per lane — license-verified, with a trust rubric and license-flag register |
| [docs/13-lane-flowcharts.md](docs/13-lane-flowcharts.md) | One reviewable flowchart per raw data type (master router + 10 lanes, Mermaid) |

## Active research program (start here if you're reviewing/researching)

The open questions are tracked as **research briefs in the issues**:
[Epic #1](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/1)
fans out to one ultra-research issue per raw format (#2–#11) plus the
knowledge-store data-formats assessment (#12). Each brief contains the
baseline (lane doc + flowchart + practices), specific research questions, and
the expected deliverable shape. Ground rules: claims verified against primary
sources/benchmarks (not READMEs), licenses screened per the
[doc 12](docs/12-tooling-landscape.md) trust rubric, and findings land as PRs
against the lane docs. Suggested order: #2 → #12 → #5.

## Who this is for

Engineers and teams who want to make a private document corpus *usable* by
LLMs — with verifiable fidelity, clean provenance, and automation that
survives unattended operation — without committing copyrighted source
material or trusting raw model output.

## License

Documentation: CC-BY-4.0. Code snippets: MIT.
