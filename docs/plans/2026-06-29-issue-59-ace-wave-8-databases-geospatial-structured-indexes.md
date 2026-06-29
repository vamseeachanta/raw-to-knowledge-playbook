# Plan for #59: ACE Wave 8 Databases, Geospatial Files, and Structured Archive Indexes

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/59
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-06-29-plan-59-claude.md | scripts/review/results/2026-06-29-plan-59-codex.md | scripts/review/results/2026-06-29-plan-59-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/10-structured-data-and-model-files.md` requires structured readers, dialect/schema checks, content hashes, and convention sidecars.
- `docs/18-security-and-pii.md` and `docs/19-trust-boundary-and-private-mode.md` require fail-closed routing where table names, field names, coordinates, or row examples can reveal private facts.
- `skills/source-extraction-coverage/SKILL.md`, `skills/source-extract-fidelity/SKILL.md`, and `skills/independent-oracle-validation/SKILL.md` define extraction coverage, fidelity, and oracle practices.

### Related issues
- [#59](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/59) covers databases/geospatial/indexes.
- [#6](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/6) and [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) are method anchors.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) provides the route/ledger dependency.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable structured stores, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- Databases: about 7.4k files / 19.9 GB.
- Geospatial: about 2.2k files / 5.4 GB.
- Known indexes include `ACE_SHARE_ROOT/docs/master-index.jsonl`, `ACE_SHARE_ROOT/.ace-knowledge/index.db`, and CAD index artifacts.
- Expected routed success target: 60-85% for eligible schema/geospatial metadata candidates; full row/example extraction remains gated by routing and #61.

### Gaps identified
- No database/geospatial lane doc, skill, or canary exists.
- No schema-summary/no-dump rule exists for ACE database sources.
- Doc 12 lacks database/geospatial reader/tool decisions for this lane.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#59 OPEN ACE wave 8: databases, geospatial files, and structured archive indexes labels=strengthening,lane:codex,priority:medium
```

**File existence**:
```
EXISTS docs/10-structured-data-and-model-files.md
EXISTS docs/18-security-and-pii.md
EXISTS docs/19-trust-boundary-and-private-mode.md
EXISTS ${ACE_SHARE_ROOT}/docs/master-index.jsonl
EXISTS ${ACE_SHARE_ROOT}/.ace-knowledge/index.db
MISSING docs/23-databases-geospatial-and-structured-indexes.md
MISSING skills/database-geospatial-structured-index-lane/SKILL.md
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-59-ace-wave-8-databases-geospatial-structured-indexes.md |
| Lane doc | docs/23-databases-geospatial-and-structured-indexes.md |
| Lane skill | skills/database-geospatial-structured-index-lane/SKILL.md |
| Canary | examples/database-geospatial-index-lane/check.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-59-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-59-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-59-gemini.md |

---

## Deliverable

A routed database/geospatial/index ingestion lane that emits schema inventories, row counts, candidate entities, geometry/CRS sidecar summaries, provenance hashes, and queryable extracts without blind dumps.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
build bounded sample across sqlite/index DBs, Access-style DBs, DBF/TAB/WLD sidecars, GIS exports, JSONL indexes, noise:
  max 20 rows per bucket, deterministic seed/sort, max 160 files or 500 MB touched
route private/public before exposing table names, field names, row examples, coordinates, or private source paths
for readable databases:
  inspect schema, tables, columns, indexes, row counts, candidate entities, sensitivity state
  use structured readers and safe identifier quoting
for geospatial sidecars:
  record sidecar completeness, CRS assumptions, geometry type, bounded metadata
for indexes:
  validate structure, provenance pointers, hashes, stale/missing source references
emit coverage ledger, trust labels, oracle comparison; retrieval metadata only after #61 approval
compute routed success numerator/denominator for eligible candidate rows
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/23-databases-geospatial-and-structured-indexes.md | Dedicated lane doc |
| Create | skills/database-geospatial-structured-index-lane/SKILL.md | Runnable lane workflow |
| Create | skills/database-geospatial-structured-index-lane/evals/evals.json | Skill evals |
| Create | examples/database-geospatial-index-lane/check.py | Executable canary |
| Modify | docs/01-document-taxonomy.md | Add/align database/geospatial lane taxonomy |
| Modify | docs/04-failure-modes.md | Add structured-store/geospatial failure modes |
| Modify | docs/08-skills-catalog.md | Register new skill |
| Modify | docs/10-structured-data-and-model-files.md | Cross-link dedicated lane |
| Modify | docs/12-tooling-landscape.md | Add database/geospatial tool decisions |
| Modify | docs/13-lane-flowcharts.md | Add database/geospatial flowcharts |
| Deferred | docs/index.md | Do not link the new lane doc until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved, the local marker exists, and the public-output canary has a recorded passing result |
| Deferred | mkdocs.yml | Do not publish the new lane doc in site navigation until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved, the local marker exists, and the public-output canary has a recorded passing result |
| Modify | skills/README.md | Register new skill |
| Modify | .github/workflows/validate.yml | Run canary and skill validation |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_sqlite_schema_summary_no_dump | DB summary only | Temp SQLite | tables/columns/indexes/row counts/hashes, no full dump |
| test_private_routing_before_field_examples | Routing before examples | DB with client-like field names | Private route before examples |
| test_parameterized_reader_rejects_unsafe_identifier | SQL safety | malicious table name | Quoted/rejected, not interpolated |
| test_geospatial_sidecar_completeness | Sidecar contract | `.tab/.dat/.map/.id/.wld` sample | present/missing sidecars and CRS assumption |
| test_common_geospatial_families_are_covered | Geospatial breadth | Shapefile, GeoPackage, KML/KMZ, CRS-missing fixtures | Sidecar/CRS state recorded or claim narrowed |
| test_jsonl_index_provenance_hashes | Index provenance | JSONL rows missing path/hash | Validation fails |
| test_oracle_residuals_are_attributed | Oracle mismatch classification | second-reader mismatch | Cause recorded |
| test_wave8_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave8_sample_caps_are_enforced | Bounded sampling | Sample manifest | Per-bucket caps, seed/sort, max files, and max bytes present |

---

## Acceptance Criteria

- [ ] Bounded sample classifies DBs, index DBs, geospatial sidecars, GIS exports, and exclude/noise.
- [ ] Bounded sample declares per-bucket caps, deterministic seed/sort, maximum files, and maximum bytes touched.
- [ ] Each readable DB gets schema inventory, row counts, candidate entities, and routing state.
- [ ] Extracts preserve provenance/hash evidence and use structured readers.
- [ ] Geospatial summaries cover or explicitly narrow claims for shapefile sidecars, GeoPackage, KML/KMZ, MapInfo sidecars, world files, and CRS-missing cases.
- [ ] Public/private routing runs before table names, field names, row examples, coordinates, or private paths are published.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved before durable structured stores, target paths, retrieval metadata, or publication writes.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports require [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) `status:plan-approved`, local approval marker, implemented redaction canary, and recorded passing-command result before docs, comments, `llm-wiki`, or external publication.
- [ ] `% ingested success` is calculated for eligible schema/geospatial metadata candidates, with exclusions reported separately.
- [ ] Skill evals and executable canary pass in CI.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude | PENDING | Not yet reviewed |
| Codex | PENDING | Not yet reviewed |
| Gemini | PENDING | Not yet reviewed |

**Overall result:** PENDING - draft only; not ready for `status:plan-review`.

---

## Risks and Open Questions

- **Risk:** Field names, coordinates, and row samples can leak client/project facts even when values are not copied.
- **Risk:** Tooling choices need license review before semantic extraction.
- **Risk:** Some database files may require proprietary readers and should stay metadata-only.

---

## Complexity

**T3** - multi-format structured stores, privacy-sensitive schemas/coordinates, new tooling decisions, new lane doc/skill/canary, and adversarial review.
