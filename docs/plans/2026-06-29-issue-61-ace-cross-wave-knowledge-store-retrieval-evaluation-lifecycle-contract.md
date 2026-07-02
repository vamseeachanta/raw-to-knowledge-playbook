# Plan for #61: ACE Cross-Wave Knowledge-Store, Retrieval, Evaluation, and Lifecycle Contract

> **Status:** plan-review
> **Complexity:** T3
> **Date:** 2026-07-02
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-07-02-plan-61-claude-r1.md | scripts/review/results/2026-07-02-plan-61-codex-r1.md | scripts/review/results/2026-07-02-plan-61-gemini-r1.md | scripts/review/results/2026-07-02-plan-61-claude-r2.md | scripts/review/results/2026-07-02-plan-61-codex-r2.md | scripts/review/results/2026-07-02-plan-61-gemini-r2.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/14-chunking-and-embedding.md` will supply structure-aware chunking, citation ID, chunk trust metadata, and table-preservation guidance.
- `docs/15-retrieval-evaluation.md` will supply the retrieval/eval gate: golden sets outside the ingest path, citation grounding, judge meta-eval, and tiered evaluation cadence.
- `docs/16-corpus-lifecycle.md` will supply content-hash docstore, two-level identity, supersede-by-append, trust reset, manifest freshness, and edition-aware retrieval rules.
- `docs/07-data-governance.md` and `docs/19-trust-boundary-and-private-mode.md` will supply raw-source firewall, provenance, visibility, private-mode, and public-boundary constraints.
- `docs/03-verification-playbook.md` and `docs/20-measured-outcomes.md` will supply extraction verification states, verification bottleneck framing, and progress measurement patterns.
- `artifacts/ace-wave0-ledger-schema.json` and `scripts/validate_ace_wave0_schema_contract.py` will be consumed as the implemented #65 source for route targets, logical target stores, canonical wave classes, and success-field vocabulary.
- `config/ace-manifest-evidence-contract.json`, `scripts/validate_ace_manifest_freshness.py`, and the valid operational evidence fixture will be consumed as the implemented #62 manifest freshness contract.
- `config/ace-public-surface-self-scan-contract.json`, `scripts/validate_ace_public_surface_scan.py`, and `scripts/legal/legal-sanity-scan.sh` will provide public-surface and legal/security scan gates for #61 artifacts.

### Related issues and live status
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic and remains open as the tracker.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains an open umbrella issue with no `status:*` label and no local approval marker. #61 will not treat the #51 umbrella as approved.
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) are the closed/implemented split contracts that #61 will consume for route/store schema, public token fixture boundaries, bounded sampling firewall, public-surface scan, legal/security scan, and manifest evidence integration.
- [#71](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/71) is closed and will be consumed only for split-registry status/plan consistency rules.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) is closed with `status:plan-approved`, `.planning/plan-approved/62.md`, an implemented manifest freshness validator, and a recorded valid evidence fixture.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) remains open with no approval marker and no implemented public-output canary. #61 will not authorize docs navigation, `mkdocs.yml`, `llm-wiki`, GitHub-public summaries, or external publication exposure.
- [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) is in `status:plan-review`; until it is approved and implemented, #61 will use only generic `--scan-public-path` public-surface scans and will not claim review selector/snapshot mode support.
- [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) remains the method anchor for storage-format research. #61 will define logical contracts and adapter requirements, not a permanent physical database/vector-store choice.

### Source inventory boundary
- Issue #61 names ACE share source-of-truth candidates such as manifest files, CAD indexes, an existing knowledge index, and wiki docs under `ACE_SHARE_ROOT`.
- Implementation will not read `ACE_SHARE_ROOT`, run operational sampling, crawl manifests, count rows, hash raw source files, or materialize raw inventories.
- #61 validators will operate only on repo-local synthetic fixtures, contract files, docs, and implemented public-safe evidence artifacts.
- Negative leak/bypass fixtures will remain scan-clean: tests will synthesize forbidden-looking values at runtime or store scanner-safe fixture templates with neutral placeholders. No tracked bad fixture will contain a raw private path, raw digest, real public token value, email, phone, client/project/customer identifier, or source-content snippet.
- Manifest-backed evidence will be referenced only through #62 opaque snapshot IDs, status enums, validator path, command, exit code, and public-safe evidence references.
- The plan filename date (`2026-06-29`) is the original draft creation date. The header date (`2026-07-02`) is the current revision/review date.

### Gaps identified
- No #61 JSON contract exists for logical storage forms, required metadata, chunk/retrieval fields, lifecycle states, and private/public boundary transitions.
- No #61 ingested-success metric validator exists that imports #65 success-field vocabulary and enforces cross-wave comparability.
- No #61 tests exist for lifecycle enum closure, route/lifecycle/verification/parse-status separation, public/private leak prevention, golden-set exclusion from ingest, or zero-denominator metric behavior.
- No CI step invokes the #61 validators.
- Existing docs use related but not identical vocabulary for extraction verification, page parse status, chunk parse status, and lifecycle states; #61 must reconcile these as separate enums instead of merging them.
- Physical private-sidecar backing storage remains undefined; #61 must keep this at the logical contract/adapter layer and defer engine selection to #12 or a follow-on issue.

### Evidence

**Live issue status** (verified 2026-07-02):
```text
#61 OPEN labels=strengthening,lane:claude,priority:high
#51 OPEN labels=strengthening,lane:claude,priority:high; no local approval marker
#62 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high; local marker exists
#63 OPEN labels=strengthening,lane:claude,priority:high; no local approval marker
#65 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high
#66 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high
#67 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high
#68 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high
#69 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high
#70 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high
#71 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:medium
#72 OPEN labels=strengthening,status:plan-review,lane:claude,priority:medium
```

**File existence**:
```text
EXISTS docs/14-chunking-and-embedding.md
EXISTS docs/15-retrieval-evaluation.md
EXISTS docs/16-corpus-lifecycle.md
EXISTS docs/07-data-governance.md
EXISTS docs/19-trust-boundary-and-private-mode.md
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS config/ace-manifest-evidence-contract.json
EXISTS config/ace-public-surface-self-scan-contract.json
EXISTS config/ace-bounded-sampling-firewall-contract.json
EXISTS scripts/validate_ace_manifest_freshness.py
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS scripts/validate_ace_bounded_sampling_firewall.py
EXISTS scripts/validate_ace_public_surface_scan.py
EXISTS scripts/legal/legal-sanity-scan.sh
EXISTS skills/validate_skill.py
EXISTS tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json
EXISTS tests/test_validate_ace_wave0_schema_contract.py
EXISTS tests/test_validate_ace_manifest_freshness.py
EXISTS tests/test_validate_ace_manifest_freshness_runtime.py
EXISTS tests/test_validate_ace_manifest_freshness_security.py
EXISTS tests/test_validate_ace_bounded_sampling_firewall.py
EXISTS tests/test_validate_ace_manifest_evidence_integration.py
EXISTS tests/test_validate_ace_public_surface_scan.py
EXISTS tests/test_legal_sanity_scan.py
EXISTS skills/page-shape-contract/evals/evals.json
EXISTS skills/source-extraction-coverage/evals/evals.json
EXISTS skills/source-extract-fidelity/evals/evals.json
EXISTS skills/verify-batch/evals/evals.json
EXISTS skills/independent-oracle-validation/evals/evals.json
EXISTS skills/public-private-routing/evals/evals.json
EXISTS skills/stacked-batch-prs/evals/evals.json
MISSING docs/case-studies/ace-share-knowledge-store-contract.md
MISSING config/ace-knowledge-store-contract.json
MISSING config/ace-ingested-success-metric-contract.json
MISSING scripts/validate_ace_knowledge_store_contract.py
MISSING scripts/validate_ace_ingested_success_metric.py
MISSING tests/test_validate_ace_knowledge_store_contract.py
MISSING tests/test_validate_ace_ingested_success_metric.py
MISSING tests/fixtures/ace-knowledge-store-contract/
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-29-issue-61-ace-cross-wave-knowledge-store-retrieval-evaluation-lifecycle-contract.md` |
| Public contract narrative | `docs/case-studies/ace-share-knowledge-store-contract.md` |
| Knowledge-store JSON contract | `config/ace-knowledge-store-contract.json` |
| Ingested-success metric JSON contract | `config/ace-ingested-success-metric-contract.json` |
| Knowledge-store contract validator | `scripts/validate_ace_knowledge_store_contract.py` |
| Ingested-success metric validator | `scripts/validate_ace_ingested_success_metric.py` |
| Knowledge-store validator tests | `tests/test_validate_ace_knowledge_store_contract.py` |
| Ingested-success validator tests | `tests/test_validate_ace_ingested_success_metric.py` |
| Knowledge-store fixtures | `tests/fixtures/ace-knowledge-store-contract/` |
| CI workflow | `.github/workflows/validate.yml` |
| Chunk/retrieval/lifecycle docs | `docs/14-chunking-and-embedding.md`, `docs/15-retrieval-evaluation.md`, `docs/16-corpus-lifecycle.md` |
| Governance/private-boundary docs | `docs/07-data-governance.md`, `docs/19-trust-boundary-and-private-mode.md` |
| Skill eval updates | `skills/page-shape-contract/evals/evals.json`, `skills/source-extraction-coverage/evals/evals.json`, `skills/source-extract-fidelity/evals/evals.json`, `skills/verify-batch/evals/evals.json`, `skills/independent-oracle-validation/evals/evals.json`, `skills/public-private-routing/evals/evals.json`, `skills/stacked-batch-prs/evals/evals.json` |
| Review artifacts | `scripts/review/results/2026-07-02-plan-61-claude-r1.md`, `scripts/review/results/2026-07-02-plan-61-codex-r1.md`, `scripts/review/results/2026-07-02-plan-61-gemini-r1.md` |
| Review artifacts | `scripts/review/results/2026-07-02-plan-61-claude-r2.md`, `scripts/review/results/2026-07-02-plan-61-codex-r2.md`, `scripts/review/results/2026-07-02-plan-61-gemini-r2.md` |

---

## Deliverable

A repo-local, CI-validated #61 contract will define logical ACE knowledge storage forms, metadata requirements, chunk/retrieval/evaluation rules, lifecycle states, invalidation rules, private/public boundary transitions, and `% ingested success` semantics for downstream waves. It will consume implemented #65-#71 contracts, avoid raw ACE-share reads, and leave physical storage-engine selection to #12 or a follow-on issue.

---

## Proposed Contract Shape

### Logical Storage Forms

The contract will define a closed logical storage-form set:

| Storage form | Purpose | Boundary rule |
|---|---|---|
| `landing_page` | Human-readable source summary and route metadata | ACE corpus content lands publicly only when #63 canary passes; a scan-clean methodology contract doc may remain in this repo before #63 |
| `part_file` | Bounded derived text/page part | Visibility follows source class; no raw source file |
| `dataset_table` | Extracted table or tabular dataset | Requires provenance, verification, and route target |
| `media_descriptor` | Image/scan/plot descriptor and evidence-series metadata | Descriptor only unless source is public-safe |
| `geometry_metadata` | CAD/geometry metadata and native-export pointers | Metadata only; no native binary in public repo |
| `private_sidecar_record` | Private provenance and lookup material | Private-sidecar-only; never public artifact content |
| `exclusion_record` | Deliberate no-ingest/no-store decision | Public-safe only if it contains no private identifiers |
| `retrieval_chunk` | Chunk/index unit for query surfaces | Carries visibility, lifecycle, citation, and parse status |
| `eval_case` | Golden/silver retrieval test case | Explicitly outside ingest and chunk-store paths |

The implementation will distinguish **public-safe methodology artifacts** from **published ACE-derived corpus output**. `docs/case-studies/ace-share-knowledge-store-contract.md` will be a public-safe methodology/contract document that contains no ACE corpus content, no raw source identifiers, no real public-token values, and no private lookup material. #63 will still block public docs navigation, `mkdocs.yml`, `llm-wiki`, GitHub-public corpus summaries, and external publication exposure for ACE-derived content.

### Required Metadata

Each storage form will declare required public-safe fields for:
- identity: opaque public token or internal logical key, never raw private lookup values in public artifacts;
- routing: #65 route target and logical target store;
- lifecycle: #61 lifecycle state and transition evidence;
- verification: extraction verification state, page/shape parse state, validator path, review evidence, and confidence class;
- provenance: citation ID, edition/revision, content hash reference, manifest snapshot reference where applicable, and private provenance bundle pointer;
- evaluation: retrieval eligibility, golden-set exclusion status, and answer-side eval coverage;
- success: #65 numerator/denominator vocabulary and #61 eligibility rules.

### Enum Ownership

The implementation will keep these enums separate:

| Enum | Owner | Contract rule |
|---|---|---|
| Route targets and logical stores | #65 / #51 split contract | Imported; never redefined in #61 |
| Lifecycle states | #61 | Closed set: `candidate`, `provisional`, `verified`, `rejected`, `superseded`, `stale_requires_rescreen`, plus explicit migration tests if changed |
| Extraction verification states | doc 03 / #65 control plane | Mapped to lifecycle but not merged with it |
| Page/shape parse states | `page-shape-contract` and #65 external vocabulary | Imported and reconciled; no silent synonym drift |
| Manifest freshness states | #62 | Referenced through public-safe evidence only |
| Publication certification states | #63 | Consumed later; not implemented in #61 |

### Retrieval and Evaluation Gate

The contract will require:
- chunk boundaries that preserve table/section structure and do not split decision-critical tables;
- chunk metadata for citation, logical document key, edition/revision, current/as-of retrieval, visibility, lifecycle, parse status, and hash reference;
- hybrid retrieval support for numeric/standards content where applicable;
- golden/silver eval sets outside ingest paths and outside chunk stores;
- continuous citation/grounding checks, CI regression checks, and periodic deeper evaluation;
- a fail-closed rule: no bulk downstream ingestion may scale beyond pilot until #61 validators pass and downstream wave plans bind the success/eval contract.

### Lifecycle and Invalidation Gate

The contract will implement a closed lifecycle transition table:

```text
candidate -> provisional -> verified
candidate -> stale_requires_rescreen
candidate -> rejected
rejected -> stale_requires_rescreen
provisional -> rejected
provisional -> stale_requires_rescreen
verified -> superseded
verified -> stale_requires_rescreen
stale_requires_rescreen -> provisional after confidentiality re-screen
stale_requires_rescreen -> rejected after re-screen failure
superseded -> stale_requires_rescreen only for audit correction
```

Any source-content change, route target change, visibility change, private/public boundary change, chunker/parser change, or manifest freshness drift will reset affected derived artifacts to `stale_requires_rescreen`, including pre-extraction `candidate` records and previously `rejected` records whose rejection evidence has been invalidated by source replacement or audit correction. A completed confidentiality re-screen will move the artifact to `provisional`; independent verification will be required before it can return to `verified`. The `superseded -> stale_requires_rescreen` path will require `transition_reason=audit_correction` plus a `rescreen_evidence_ref`; otherwise superseded records remain audit-only. The `rejected -> stale_requires_rescreen` path will be limited to source replacement or audit-correction evidence and will not reopen ordinary rejected records.

### Success Metric Gate

`% ingested success` will be defined for ingestion waves as:

```text
successful_routed_items / eligible_candidate_items * 100
```

Hard exclusions will be reported separately as `% excluded`. Control-plane/gate issues will use `success_metric_applicability=not_applicable_control_plane` with explicit zero numerator/denominator/threshold behavior. A successful routed item will require closed route target, allowed lifecycle state, public/private boundary pass, shape/fidelity checks, and required #62/#63 evidence when applicable.

The metric status vocabulary will be closed:

| Metric status | Allowed when |
|---|---|
| `measured` | `eligible_candidate_items > 0` and a percentage is emitted |
| `no_eligible_candidates` | ingestion wave has zero eligible candidates and emits no percentage |
| `no_classified_items` | `total_classified_items == 0`; no `% excluded` value is emitted |
| `not_applicable_control_plane` | control/gate issue uses zero numerator, denominator, threshold, and no percentage |
| `invalid_metric` | validator-only failure state, never valid committed evidence |

`% excluded` will use `hard_excluded_items / total_classified_items * 100` only when `total_classified_items > 0`; when `total_classified_items == 0`, the validator will require `metric_status=no_classified_items` and no emitted exclusion percentage. `eligible_candidate_items` will equal `total_classified_items - hard_excluded_items`.

---

## Pseudocode

```text
load #65 route/store schema
load #62 manifest evidence contract and trusted evidence fixture
load #68/#69 scan contracts for public/legal verification
assert #61 production validators do not read ACE_SHARE_ROOT or raw manifests
allow bounded repo-local fixture traversal only under tests/fixtures/ace-knowledge-store-contract/

define closed storage_form set
define required metadata per storage_form
define lifecycle state machine and transition table
define enum owner map:
  #65 route/store, #61 lifecycle, doc03/#65 verification,
  page-shape parse status, #62 freshness, #63 publication

for each storage_form:
  require route target from #65
  require lifecycle state from #61
  require verification/parse/eval fields appropriate to form
  require private provenance as opaque bundle pointer only in public contracts
  reject raw private paths, raw digest values, exact private inventory stats,
  real public token values, email/phone/client identifiers, and source content snippets
  keep negative fixtures scan-clean via runtime synthesis or neutral placeholders

define retrieval_chunk contract:
  citation identifier, logical document key, edition/revision, current/as-of flags,
  visibility, lifecycle state, parse status, hash reference, table/section structure

define eval contract:
  golden/silver cases outside ingest path and chunk store
  continuous grounding checks
  CI regression gate
  periodic deep eval

define success metric:
  ingestion waves use successful_routed_items / eligible_candidate_items * 100
  hard exclusions use hard_excluded_items / total_classified_items * 100 only when total_classified_items > 0
  zero classified rows emit metric_status=no_classified_items and no exclusion percentage
  zero eligible ingestion waves emit metric_status=no_eligible_candidates and no percentage
  control/gate rows use metric_status=not_applicable_control_plane with zero values

validate CI wiring, docs, fixtures, skills, public scan, and legal scan
stop for user approval after plan review; do not implement from this plan draft
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `docs/case-studies/ace-share-knowledge-store-contract.md` | Human-readable #61 contract for storage, retrieval, evaluation, lifecycle, and success metrics |
| Create | `config/ace-knowledge-store-contract.json` | Machine-readable storage forms, metadata fields, enum owners, lifecycle transitions, and boundary rules |
| Create | `config/ace-ingested-success-metric-contract.json` | Machine-readable success metric, denominator/numerator, exclusion, threshold, and zero-denominator rules |
| Create | `scripts/validate_ace_knowledge_store_contract.py` | Validator for #61 storage/retrieval/lifecycle/public-private contract |
| Create | `scripts/validate_ace_ingested_success_metric.py` | Validator for cross-wave success metric consistency |
| Create | `tests/test_validate_ace_knowledge_store_contract.py` | TDD coverage for #61 contract validation |
| Create | `tests/test_validate_ace_ingested_success_metric.py` | TDD coverage for success metric validation |
| Create | `tests/fixtures/ace-knowledge-store-contract/` | Valid and invalid synthetic fixtures |
| Modify | `.github/workflows/validate.yml` | Run #61 validators and tests |
| Modify | `docs/14-chunking-and-embedding.md` | Add ACE chunk metadata hook without changing the general guidance |
| Modify | `docs/15-retrieval-evaluation.md` | Add ACE eval gate hook and golden-set exclusion rule |
| Modify | `docs/16-corpus-lifecycle.md` | Add ACE lifecycle transition and confidentiality re-screen hook |
| Modify | `docs/07-data-governance.md` | Cross-link ACE logical storage forms to provenance/routing |
| Modify | `docs/19-trust-boundary-and-private-mode.md` | Cross-link private-sidecar and publication-boundary behavior |
| Modify | skill eval JSON files listed in the Artifact Map | Add focused eval cases for metadata, fidelity, verification, routing, and batch-collision behavior |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_storage_forms_are_closed_set` | Storage forms cannot drift silently | Contract fixture with extra form | Validator rejects unknown form |
| `test_storage_forms_have_required_metadata` | Every form has identity/routing/lifecycle/verification/provenance/eval/success requirements | Valid and incomplete fixtures | Valid passes; incomplete fixture fails by field group |
| `test_imports_65_route_store_without_redefinition` | #61 consumes #65 route/store values | Mutated route/store fixture | Unknown or physical-path-like store fails |
| `test_lifecycle_state_machine_is_closed` | Lifecycle states and transitions are explicit | Unknown state or forbidden transition | Validator rejects |
| `test_enum_owner_map_requires_explicit_mappings` | Route, lifecycle, verification, and parse status remain owner-scoped without forbidding legitimate shared words | Fixture with unmapped cross-owner alias or missing owner | Validator rejects unmapped owner drift while accepting explicit mapping records |
| `test_boundary_change_requires_confidentiality_rescreen` | Visibility/route/public-private changes reset trust | Fixture with boundary change and no re-screen | Validator rejects |
| `test_source_or_manifest_drift_resets_verified_state` | Source/manifest changes cannot remain verified | Fixture with #62 drift and verified state | Validator rejects |
| `test_rescreen_transition_reaches_verified_again` | Reset artifacts have a valid re-entry path | Lifecycle fixture with stale artifact, re-screen, then verification | `stale_requires_rescreen -> provisional -> verified` passes; direct stale-to-verified fails |
| `test_superseded_audit_correction_requires_evidence` | Superseded records cannot be reopened casually | Transition fixture missing audit reason/evidence | Validator rejects |
| `test_no_ace_share_root_or_raw_manifest_reads` | #61 production validator cannot perform operational sampling | Source scan of all #61 changed artifacts | `ACE_SHARE_ROOT` runtime access, unbounded traversal outside the fixture directory, raw manifest materialization, full-file hashing/counting, unrestricted `jq`, raw manifest reads via `cat`, recursive manifest grep, `os.walk`, and unrestricted `.rglob` fail; bounded fixture reads and scanner-denylist constants are allowed |
| `test_negative_fixtures_are_scan_clean` | Bad cases do not break repo-wide scans | Fixture directory and test source | Tracked fixtures contain neutral placeholders or runtime-synthesis markers only |
| `test_public_contract_uses_private_provenance_bundle_only` | Public contract does not expose private lookup fields or raw digest assignments | Bad JSON/doc fixtures | Validator/public scan rejects |
| `test_public_contract_rejects_real_public_token_values` | Public token field names are allowed only as schema prose, not minted values | Bad fixture with token-looking value | Validator rejects |
| `test_public_contract_doc_is_not_publication_exposure` | Methodology doc is allowed while corpus-publication remains gated | Contract doc plus publication config fixture | Scan-clean contract doc passes; `mkdocs.yml` explicit `nav` does not include the #61 contract doc; docs nav, `llm-wiki`, or public corpus summary remains rejected without #63 |
| `test_retrieval_chunk_metadata_required` | Retrieval chunks carry citation, logical key, edition/revision, current/as-of flags, visibility, lifecycle, parse status, and hash reference | Chunk fixture | Missing fields fail |
| `test_table_chunks_preserve_structure` | Table/section chunk rules are not optional | Contract fixture with table-splitting allowed | Validator rejects |
| `test_golden_eval_excluded_from_ingest_and_chunk_store` | Eval leakage is blocked | Eval fixture routed into ingest/chunk path | Validator rejects |
| `test_success_metric_formula_imports_65_fields` | Formula uses #65 numerator/denominator names | Mutated metric fixture | Wrong fields fail |
| `test_hard_exclusions_are_reported_separately` | Exclusions do not count as ingestion failures | Metric fixture with exclusions in denominator | Validator rejects |
| `test_zero_denominator_behavior_is_explicit` | Empty bounded samples are deterministic | Zero-denominator fixture | Control-plane passes only with `not_applicable_control_plane`; ingestion wave passes only with `no_eligible_candidates` and no percentage; zero classified rows pass only with `no_classified_items` and no exclusion percentage |
| `test_63_publication_gate_blocks_exposure` | Publication remains blocked until #63 canary exists | Contract with publication exposure true and no #63 evidence | Validator rejects |
| `test_72_selector_mode_not_claimed` | #61 uses generic public scans only until #72 implementation | Plan/CI fixture with selector mode for #61 | Validator rejects |
| `test_skill_evals_include_61_metadata_cases` | Bound skills are updated with reusable #61 eval cases | Skill eval JSON | Missing cases fail; every new case must include `issue: 61` metadata and an `id` beginning with `ace-61-` |
| `test_bulk_scale_gate_is_declared` | Downstream waves cannot scale beyond pilot without #61 binding | Downstream wave gate fixture | Missing `bulk_scale_gate_requires_61` record fails |
| `test_ci_runs_61_validators_and_scans` | CI includes #61 validators, unit tests, public scan, legal scan | Workflow text | Required commands present |

---

## Verification Commands

Implementation will run:

```bash
uv run python scripts/validate_ace_knowledge_store_contract.py
uv run python scripts/validate_ace_ingested_success_metric.py
uv run python scripts/validate_ace_wave0_schema_contract.py
uv run python scripts/validate_ace_manifest_freshness.py --evidence tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json
uv run python scripts/validate_ace_bounded_sampling_firewall.py
uv run python scripts/validate_ace_public_surface_scan.py \
  --scan-public-path docs/plans/2026-06-29-issue-61-ace-cross-wave-knowledge-store-retrieval-evaluation-lifecycle-contract.md \
  --scan-public-path docs/case-studies/ace-share-knowledge-store-contract.md \
  --scan-public-path config/ace-knowledge-store-contract.json \
  --scan-public-path config/ace-ingested-success-metric-contract.json \
  --scan-public-path scripts/validate_ace_knowledge_store_contract.py \
  --scan-public-path scripts/validate_ace_ingested_success_metric.py \
  --scan-public-path tests/test_validate_ace_knowledge_store_contract.py \
  --scan-public-path tests/test_validate_ace_ingested_success_metric.py \
  --scan-public-path tests/fixtures/ace-knowledge-store-contract/ \
  --scan-public-path docs/14-chunking-and-embedding.md \
  --scan-public-path docs/15-retrieval-evaluation.md \
  --scan-public-path docs/16-corpus-lifecycle.md \
  --scan-public-path docs/07-data-governance.md \
  --scan-public-path docs/19-trust-boundary-and-private-mode.md \
  --scan-public-path skills/page-shape-contract/evals/evals.json \
  --scan-public-path skills/source-extraction-coverage/evals/evals.json \
  --scan-public-path skills/source-extract-fidelity/evals/evals.json \
  --scan-public-path skills/verify-batch/evals/evals.json \
  --scan-public-path skills/independent-oracle-validation/evals/evals.json \
  --scan-public-path skills/public-private-routing/evals/evals.json \
  --scan-public-path skills/stacked-batch-prs/evals/evals.json \
  --scan-public-path .github/workflows/validate.yml
uv run python -m unittest tests.test_validate_ace_knowledge_store_contract tests.test_validate_ace_ingested_success_metric tests.test_validate_ace_wave0_schema_contract tests.test_validate_ace_manifest_freshness tests.test_validate_ace_manifest_freshness_runtime tests.test_validate_ace_manifest_freshness_security tests.test_validate_ace_bounded_sampling_firewall tests.test_validate_ace_manifest_evidence_integration tests.test_validate_ace_public_surface_scan tests.test_legal_sanity_scan
uv run skills/validate_skill.py
bash scripts/legal/legal-sanity-scan.sh --diff-only
bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces
git diff --check
```

Plan-review verification will run the generic public scan only over the plan and review artifacts; selector/snapshot mode will remain out of scope until #72 is implemented. The plan-review gate may apply `status:plan-review` only after the patched plan, review artifacts, validation evidence, pushed commit, and GitHub evidence comment exist. `status:plan-approved` and `.planning/plan-approved/61.md` remain user-only authorization gates.

---

## Acceptance Criteria

- [ ] The #61 public contract defines logical storage forms, required metadata, lifecycle states, retrieval/chunk fields, evaluation gates, and success metric rules without raw ACE-share reads.
- [ ] #61 imports #65 route targets, logical target stores, wave classes, and success-field vocabulary without redefining them.
- [ ] #61 consumes #62 manifest evidence only through public-safe snapshot IDs, status enums, validator path, command, exit code, and evidence references.
- [ ] #61 validators reject raw private paths, raw private digest assignments, exact private inventory statistics, real public token values, emails, phones, client/project/customer identifiers, and source-content snippets.
- [ ] #61 production validators and changed artifacts reject `ACE_SHARE_ROOT` runtime access, unbounded traversal outside the bounded fixture directory, raw manifest materialization, full-file hashing/counting, unrestricted `jq`, raw manifest reads via `cat`, recursive manifest grep, `os.walk`, and unrestricted `.rglob`; scanner-denylist constants and bounded scan-clean fixture reads do not self-block the implementation.
- [ ] Route target, logical store, lifecycle, extraction verification, parse status, manifest freshness, and publication certification remain separate owner-scoped enums with explicit mapping records where terms overlap.
- [ ] Lifecycle transitions reset trust and require confidentiality re-screen on source-content, manifest, route, visibility, boundary, parser/chunker, or public/private policy changes.
- [ ] Retrieval chunk metadata carries citation, logical document key, edition/revision, current/as-of flags, visibility, lifecycle state, parse status, and hash reference.
- [ ] Golden/silver eval cases are excluded from ingest paths and chunk stores.
- [ ] `% ingested success` is defined as `successful_routed_items / eligible_candidate_items * 100`, `% excluded` is defined as `hard_excluded_items / total_classified_items * 100` only when `total_classified_items > 0`, and zero-denominator behavior uses the closed metric status vocabulary.
- [ ] The scan-clean #61 methodology/contract doc may exist in this repo, but public/docs navigation, `mkdocs.yml` explicit `nav`, `llm-wiki`, GitHub-public corpus summaries, and external ACE-derived publication exposure remain blocked until #63 approval marker, implemented canary, and passing command exist.
- [ ] #61 plan and implementation verification use generic `--scan-public-path` scans only; review selector/snapshot mode claims remain blocked on #72 implementation.
- [ ] CI runs the #61 validators and related unit tests.
- [ ] Bound skill eval JSON files receive focused #61 cases in this issue; missing cases fail the #61 validator.
- [ ] `uv run python scripts/validate_ace_knowledge_store_contract.py`, `uv run python scripts/validate_ace_ingested_success_metric.py`, `uv run skills/validate_skill.py`, public-surface scan, legal scan, unit tests, and `git diff --check` pass.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Lifecycle re-entry, scan-safe negative fixtures, complete evidence, consumption-list consistency, skill-eval oracle, metric definitions, enum overlap, scan coverage, and date/path hygiene needed tightening. Findings patched in this draft. |
| Codex r1 | MAJOR | Source-ban self-blocking, skill-eval contradiction, public-safe contract vs #63 publication ambiguity, missing evidence for bounded-sampling validator, and zero-denominator vocabulary needed tightening. Findings patched in this draft. |
| Gemini r1 | UNAVAILABLE | Gemini CLI failed with unsupported-client/ineligible-tier before returning findings. |
| Claude r2 | MINOR | Lifecycle reset edge coverage, `% excluded` zero denominator, skill-eval oracle, source-ban pattern completeness, MkDocs exposure check, date/path note, and Gemini disposition needed tightening. Findings patched in this draft. |
| Codex r2 | MINOR | Plan-review/approval gate wording, all-changed-artifact source-ban coverage, and `% excluded` zero-total behavior needed tightening. Findings patched in this draft. |
| Gemini r2 | UNAVAILABLE | Gemini CLI failed with unsupported-client/ineligible-tier before returning findings. |

**Overall result:** PLAN-REVIEW READY - r1 returned Claude MAJOR and Codex MAJOR, and r2 active-provider review returned Claude MINOR and Codex MINOR with no usable MAJOR. Gemini was unavailable in both rounds. This draft patches the r2 findings and remains blocked from implementation until the user approves #61, applies `status:plan-approved`, and creates `.planning/plan-approved/61.md`.

---

## Risks and Open Questions

- **Risk:** #61 could accidentally redefine route/store, public-token, manifest freshness, legal scan, or publication contracts already owned by sibling issues. The implementation must consume those contracts by import/reference and test that the values stay aligned.
- **Risk:** The public plan can leak private schema semantics by turning private provenance terms into public fields. The implementation must keep private provenance behind an opaque bundle/reference and rely on public scanners and legal scans.
- **Risk:** Golden Q/A leakage into the ingest path would invalidate retrieval metrics. The implementation must treat eval cases as outside the chunk store.
- **Risk:** Physical storage-engine selection remains unsettled under #12. #61 must avoid selecting a permanent backend without follow-on storage-format research or explicit user approval.
- **Risk:** #51 remains a draft umbrella. #61 may proceed by consuming the closed split contracts #65-#70, but it must not claim the #51 umbrella itself is approved.
- **Risk:** #63 remains unapproved. #61 may define private/internal contracts, but public exposure remains blocked until #63 is approved and implemented.
- **Risk:** #72 remains unimplemented. #61 review and validation must use generic public scans only.

---

## Complexity

**T3** - systemic cross-wave contract touching storage, retrieval, evaluation, lifecycle, governance, skills, CI validation, and multiple implemented sibling contracts.
