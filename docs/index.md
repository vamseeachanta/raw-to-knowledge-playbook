# Raw-to-Knowledge Playbook

A field-tested methodology for turning **raw engineering data** (PDFs, scans, office docs, model files) into **trustworthy, AI-ready knowledge** — with verification gates that refuse to fabricate.

This site renders the playbook's 20 documents with native diagrams and full-text search. Everything here is the public, sanitized methodology; no client data.

## Start here

- **[Quickstart](https://github.com/vamseeachanta/raw-to-knowledge-playbook/blob/main/QUICKSTART.md)** — the 15-minute path.
- **[Pipeline Architecture](02-pipeline-architecture.md)** — how raw → provisional → verified → promoted flows.
- **[Lane Flowcharts](13-lane-flowcharts.md)** — the master routing classifier + per-lane flows (Mermaid).
- **[Measured Outcomes](20-measured-outcomes.md)** — the honest numbers: what's resolved, verified, and rejected.

## What makes it credible

- **Verification before promotion** — see the [Verification Playbook](03-verification-playbook.md) and the runnable [`examples/minimal-ingest`](https://github.com/vamseeachanta/raw-to-knowledge-playbook/tree/main/examples/minimal-ingest), which includes a defect-injection mode that shows the gate refusing a corrupted cell.
- **Named failure modes** — the [Failure Modes](04-failure-modes.md) catalog (16+ modes) and the [Good Practices](05-good-practices.md) catalog (GP-01…), each tied to a real incident.
- **Reusable skills** — the [Skills Catalog](08-skills-catalog.md) and the [`skills/`](https://github.com/vamseeachanta/raw-to-knowledge-playbook/tree/main/skills) directory (L1/L2/L3 enforcement + an authoring standard + validator).
- **Honest about completeness** — [Measured Outcomes](20-measured-outcomes.md) reports that only a fraction of tables/docs are fully resolved, by design.

## License

Prose: **CC-BY-4.0**. Code: **MIT**. See [LICENSE](https://github.com/vamseeachanta/raw-to-knowledge-playbook/blob/main/LICENSE.md).
