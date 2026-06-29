# Plan for #58: ACE Wave 7 Simulation, Solver Input Decks, Solver Outputs, and Engineering Result Files

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/58
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-06-29-plan-58-claude.md | scripts/review/results/2026-06-29-plan-58-codex.md | scripts/review/results/2026-06-29-plan-58-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/10-structured-data-and-model-files.md` requires solver decks to parse to reviewable config, round-trip, and carry assumption ledgers.
- `docs/13-lane-flowcharts.md` includes solver input/output flows: content probe, config round-trip, block parser, cross-format parity, and physical/range/coverage gates.
- `skills/content-triage-and-exclusion/SKILL.md`, `skills/source-extract-fidelity/SKILL.md`, and `skills/independent-oracle-validation/SKILL.md` require triage, fidelity review, and oracle validation.

### Related issues
- [#58](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/58) covers simulation/engineering files.
- [#9](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/9), [#10](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/10), and [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) are method anchors.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) provides the route/ledger dependency.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable solver/result stores, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- Simulation/engineering family: about 116.6k files / 1.99 TB.
- `.sim` alone: 7,314 files / 1.88 TB.
- Large binaries default metadata-only unless parser and verifier are approved.
- Expected routed success target: 20-40% semantic extraction for eligible text/listing/deck candidates and metadata-only success for approved large-binary rows; exclusions reported separately.

### Gaps identified
- No dedicated simulation/engineering lane doc or skill exists.
- No canary exists for solver deck round-trip, output block parsing, and large-binary metadata-only behavior.
- Doc 12 must record solver parser/tool license decisions before semantic extraction.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#58 OPEN ACE wave 7: simulation, solver input decks, solver outputs, and engineering result files labels=strengthening,lane:codex,priority:high
```

**File existence**:
```
EXISTS docs/10-structured-data-and-model-files.md
EXISTS docs/13-lane-flowcharts.md
EXISTS skills/independent-oracle-validation/SKILL.md
MISSING docs/22-simulation-solver-and-engineering-result-files.md
MISSING skills/simulation-engineering-file-lane/SKILL.md
MISSING examples/simulation-engineering-lane/check.py
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-58-ace-wave-7-simulation-solver-engineering-files.md |
| Lane doc | docs/22-simulation-solver-and-engineering-result-files.md |
| Lane skill | skills/simulation-engineering-file-lane/SKILL.md |
| Canary | examples/simulation-engineering-lane/check.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-58-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-58-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-58-gemini.md |

---

## Deliverable

A documented and tested simulation/engineering-file ingestion lane that classifies solver inputs, outputs, result exports, restart files, plots, and large binaries while extracting configs, assumption ledgers, and result summaries only where verified.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
build bounded sample by extension, size, header signature, project path:
  max 20 rows per bucket, deterministic seed/sort, max 160 files or 2 GB touched
route/exclude private, PII, third-party-confidential, low-value noise
classify by content/header:
  input_deck, output_listing, restart_or_result_binary, plot_or_export, exclude
for input decks:
  parse normalized YAML config
  emit assumption ledger
  regenerate deck and reparse to identity
for outputs:
  detect format by header
  parse block-marked sections
  run physical/range/coverage gates and cross-format parity when possible
for large binaries:
  emit metadata/hash/project index only unless parser/verifier approved
record coverage ledger, trust labels, oracle results, and method gaps
compute routed success numerator/denominator for eligible candidate rows
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/22-simulation-solver-and-engineering-result-files.md | Dedicated lane doc |
| Create | skills/simulation-engineering-file-lane/SKILL.md | Runnable lane workflow |
| Create | skills/simulation-engineering-file-lane/evals/evals.json | Skill evals |
| Create | examples/simulation-engineering-lane/check.py | Executable canary |
| Create | examples/simulation-engineering-lane/fixtures/minimal_deck.inp | Synthetic input-deck fixture for round-trip tests |
| Create | examples/simulation-engineering-lane/fixtures/frequency_listing.out | Synthetic output-listing fixture with block markers |
| Create | examples/simulation-engineering-lane/fixtures/minimal_result.sim.meta.json | Synthetic metadata fixture for large-binary discipline without storing a real binary |
| Modify | docs/01-document-taxonomy.md | Add/align simulation lane taxonomy |
| Modify | docs/04-failure-modes.md | Add solver/result failure modes |
| Modify | docs/08-skills-catalog.md | Register new skill |
| Modify | docs/10-structured-data-and-model-files.md | Cross-link dedicated lane |
| Modify | docs/12-tooling-landscape.md | Add solver parser/tool license decisions |
| Modify | docs/13-lane-flowcharts.md | Add/extend solver flowcharts |
| Deferred | docs/index.md | Do not link the new lane doc until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved, the local marker exists, and the public-output canary has a recorded passing result |
| Deferred | mkdocs.yml | Do not publish the new lane doc in site navigation until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved, the local marker exists, and the public-output canary has a recorded passing result |
| Modify | skills/README.md | Register new skill |
| Modify | .github/workflows/validate.yml | Run canary and skill validation |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_classifies_rst_by_header_not_extension | `.rst` semantics | `.rst` with solver restart header | Engineering result, not prose |
| test_solver_deck_requires_round_trip_identity | Deck config proof | Sample deck | YAML config and regenerated deck reparse identical |
| test_silent_defaults_fail_without_assumption_ledger | Defaults explicit | Missing units/defaults | Fails unless ledger records assumptions |
| test_output_listing_is_block_aware | Block parser | Frequency-block listing | Separate result blocks |
| test_large_binary_metadata_only | Binary discipline | `.sim` binary | sha256/size/project metadata only |
| test_public_route_blocks_project_identifiers | Routing | Extract with project/client path | Public route blocked |
| test_wave7_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave7_sample_caps_are_enforced | Bounded sampling | Sample manifest | Per-bucket caps, seed/sort, max files, and max bytes present |

---

## Acceptance Criteria

- [ ] Bounded sample separates solver input decks, output listings, binary result/restart files, plots/exports, and exclude/noise.
- [ ] Bounded sample declares per-bucket caps, deterministic seed/sort, maximum files, and maximum bytes touched.
- [ ] Input extraction targets config plus assumption ledger, never raw deck copying.
- [ ] Output extraction is header-detected, block-aware, sanity-gated, and provenance-backed.
- [ ] Ambiguous extensions are classified by header/content inspection.
- [ ] Large binaries remain metadata-only without approved parser/verifier.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved before durable solver/result stores, target paths, retrieval metadata, or publication writes.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports require [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) `status:plan-approved`, local approval marker, implemented redaction canary, and recorded passing-command result before docs, comments, `llm-wiki`, or external publication.
- [ ] `% ingested success` is calculated for eligible candidate rows, with large-binary metadata-only successes and exclusions reported separately.
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

- **Risk:** Solver-specific parser coverage is unknown.
- **Risk:** Physical sanity gates vary by discipline; generic gates must stay conservative and provisional.
- **Risk:** Some result formats may be too binary/proprietary for semantic extraction.

---

## Complexity

**T3** - huge binary-heavy corpus, solver-specific semantics, security routing, new docs, new skill, canary, and adversarial review.
