# LLM Document-Ingestion Playbook

A field-tested methodology for turning large corpora of technical PDF documents
(engineering standards, codes, papers, reports) into a verified, citable,
LLM-queryable knowledge wiki — using a **multi-agent pipeline** that combines
deterministic extraction tools with LLM-based verification and review.

Everything here was distilled from a real, ongoing ingestion campaign:

| Scale dimension | Value (as of 2026-06) |
|---|---|
| Wiki pages produced | ~24,000 markdown pages |
| Tables extracted to CSV | ~18,300 |
| Publishers ingested | 13 (ISO, API, ASTM, BSI, DNV, IEC, NORSOK, NACE, NEMA, HSE, MIL, SNAME, OnePetro) |
| Vision-verification batches run | 80+ (≈450 tables verified cell-by-cell) |
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

## Who this is for

Engineers and teams who want to make a private document corpus *usable* by
LLMs — with verifiable fidelity, clean provenance, and automation that
survives unattended operation — without committing copyrighted source
material or trusting raw model output.

## License

Documentation: CC-BY-4.0. Code snippets: MIT.
