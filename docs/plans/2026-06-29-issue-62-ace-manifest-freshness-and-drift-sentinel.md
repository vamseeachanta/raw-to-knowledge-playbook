# Plan for #62: ACE Cross-Wave Manifest Freshness and Drift Sentinel

> **Status:** plan-approved
> **Complexity:** T2
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** see Artifact Map below; final no-MAJOR round is r3

---

## Resource Intelligence Summary

### Existing repo code/docs

- `docs/16-corpus-lifecycle.md` will provide the source-freshness rationale: source changes reset trust, and downstream artifacts need explicit freshness evidence.
- `docs/plans/README.md` will remain the portfolio gate source for `ACE_SHARE_ROOT`, share-relative manifest keys, bounded sampling, and public/private artifact safety.
- `docs/plans/ace-share-ingestion-wave-coordination.md` will remain the coordination source for the six named manifest sources: `INDEX.md`, `assets.json`, `docs/master-index.jsonl`, `_cad-index/index-summary.json`, `_cad-index/cad-readability-index.tsv`, and `.ace-knowledge/index.db`.
- `artifacts/ace-wave0-ledger-schema.json` will provide the machine-readable canonical wave registry. Issues #52-#60 already carry `requires_manifest_snapshot_id=true`; #62 itself is a `manifest_freshness_gate` and does not sample source content.
- `scripts/validate_ace_epic_wave_coordination.py` and `scripts/validate_ace_wave0_schema_contract.py` will remain the parent validators that #62 must not weaken.
- `.github/workflows/validate.yml` will need a repo-local #62 validator step and explicit public-scan paths for #62 artifacts.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic for the ACE ingestion waves.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains the wave-0 umbrella, but #62 will consume the implemented [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema rather than waiting on the #51 umbrella plan.
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) owns the canonical wave registry and the `requires_manifest_snapshot_id` boolean that identifies which downstream waves need manifest evidence.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) remains fail-closed for operational downstream sampling until #62 defines this evidence contract and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) imports it into #67.
- [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) is downstream of #62. It will ratify #67/#62 integration after #62 is approved and implemented; #62 will not implement #67's operational allow-path.
- [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) is a follow-on integration issue, not a #65 canonical wave or wave-0 split row. #62 will record the evidence contract that #70 consumes without adding #70 to the #65 schema registry.
- [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) will cite #62 snapshot evidence before manifest-backed pilot sampling.

### Source inventory

- Candidate manifest sources will be the closed six-key set from the coordination ledger: `INDEX.md`, `assets.json`, `docs/master-index.jsonl`, `_cad-index/index-summary.json`, `_cad-index/cad-readability-index.tsv`, and `.ace-knowledge/index.db`.
- Runtime source access will use `ACE_SHARE_ROOT` plus the closed share-relative manifest key enum. Public docs, reports, issue comments, and review artifacts will not include host paths, raw source IDs, raw source hashes, raw private lookup keys, or exact private corpus snippets.
- Public evidence records will carry opaque manifest snapshot tokens and bounded status fields only. Exact file stats, raw digests, row counts for private manifests, and any lookup material will remain private-sidecar data consumed by the validator at runtime and not committed to public artifacts.
- Full-manifest content fingerprints and row-count values will be accepted only when supplied by a bounded precomputed sidecar or when the manifest is explicitly under named caps: `max_header_bytes`, `max_under_cap_bytes`, and `max_under_cap_rows`.
- Above-cap manifests without a sidecar content signal will classify `content_fingerprint_status` as `unavailable`; size or timestamp evidence alone must not produce a `compatible` drift verdict.
- Public-scanned #62 artifacts will avoid scan-hostile source-root examples: negative traversal/read examples will be assembled from neutral token fragments at test runtime, and docs/comments will keep the source-root environment token separate from share-relative manifest keys.

### Gaps identified

- No repo-tracked #62 evidence contract exists for #70 to import.
- No reusable manifest snapshot ID exists for downstream waves.
- No drift severity policy exists for comparing broad manifests, master indexes, CAD indexes, and knowledge-store indexes.
- No validator exists to prevent downstream plans from mixing incompatible manifest counts without reconciliation.
- No public/private evidence split exists for exact source stats and raw digests.

### Evidence

**Issue status** (verified 2026-07-01 before formal review):

```text
#62 OPEN ACE cross-wave: manifest freshness and drift sentinel labels=strengthening,lane:codex,priority:high
```

**File existence** (verified 2026-07-01):

```text
EXISTS docs/16-corpus-lifecycle.md
EXISTS docs/plans/README.md
EXISTS docs/plans/ace-share-ingestion-wave-coordination.md
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS .github/workflows/validate.yml
MISSING config/ace-manifest-evidence-contract.json
MISSING scripts/validate_ace_manifest_freshness.py
MISSING tests/test_validate_ace_manifest_freshness.py
MISSING tests/fixtures/ace-manifest-freshness/
MISSING docs/case-studies/ace-manifest-freshness-drift-sentinel.md
MISSING .planning/plan-approved/62.md
```

**Related issue existence** (verified 2026-07-01 UTC with `gh issue view`):

```text
#65 OPEN/implemented schema slice evidence available locally via artifacts/ace-wave0-ledger-schema.json and .planning/plan-approved/65.md
#67 OPEN status:plan-review; operational downstream sampling remains fail-closed pending #62/#70
#70 OPEN ACE #67/#62 integration: ratify manifest evidence contract
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-29-issue-62-ace-manifest-freshness-and-drift-sentinel.md` |
| Evidence contract | `config/ace-manifest-evidence-contract.json` |
| Sentinel case study | `docs/case-studies/ace-manifest-freshness-drift-sentinel.md` |
| Validator | `scripts/validate_ace_manifest_freshness.py` |
| Unit tests | `tests/test_validate_ace_manifest_freshness.py` |
| Synthetic fixtures | `tests/fixtures/ace-manifest-freshness/` |
| Workflow | `.github/workflows/validate.yml` |
| Lifecycle doc | `docs/16-corpus-lifecycle.md` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Review artifact - Claude r1 | `scripts/review/results/2026-07-01-plan-62-claude-r1.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-07-01-plan-62-codex-r1.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-07-01-plan-62-gemini-r1.md` |
| Disagreement report r1 | `scripts/review/results/2026-07-01-plan-62-disagreement-r1.md` |
| Review artifact - Claude r2 | `scripts/review/results/2026-07-01-plan-62-claude-r2.md` |
| Review artifact - Codex r2 | `scripts/review/results/2026-07-01-plan-62-codex-r2.md` |
| Review artifact - Gemini r2 | `scripts/review/results/2026-07-01-plan-62-gemini-r2.md` |
| Disagreement report r2 | `scripts/review/results/2026-07-01-plan-62-disagreement-r2.md` |
| Review artifact - Claude r3 | `scripts/review/results/2026-07-01-plan-62-claude-r3.md` |
| Review artifact - Codex r3 | `scripts/review/results/2026-07-01-plan-62-codex-r3.md` |
| Review artifact - Gemini r3 | `scripts/review/results/2026-07-01-plan-62-gemini-r3.md` |
| Disagreement report r3 | `scripts/review/results/2026-07-01-plan-62-disagreement-r3.md` |

---

## Deliverable

After approval and implementation, #62 will provide a repo-local manifest evidence contract, validator, synthetic fixture set, public-safe case study, and CI wiring that produce and validate opaque manifest snapshot IDs for the six configured manifest sources. The output will let downstream waves cite reviewed snapshot evidence without exposing raw source paths or raw digest material. #62 will define the evidence contract only; #70 will later import it into #67's operational sampling firewall.

---

## Evidence Contract Shape

The implementation will create `config/ace-manifest-evidence-contract.json` with this proposed shape:

| Field | Proposed rule |
|---|---|
| `contract_id` | exactly `ace-manifest-evidence-contract` |
| `contract_version` | semver under `1.0.x` |
| `owner_issue` | JSON integer exactly `62` |
| `depends_on_schema_issue` | JSON integer exactly `65` |
| `downstream_consumer_issue` | JSON integer exactly `70`; #67 consumption stays blocked until #70 |
| `manifest_source_keys` | exactly the six-key enum from the coordination ledger |
| `manifest_source_roles` | closed key-to-role map: `INDEX.md` = `root_inventory_index`, `assets.json` = `asset_manifest`, `docs/master-index.jsonl` = `master_record_index`, `_cad-index/index-summary.json` = `cad_summary_index`, `_cad-index/cad-readability-index.tsv` = `cad_readability_index`, `.ace-knowledge/index.db` = `knowledge_store_index` |
| `source_root_env_var` | exactly `ACE_SHARE_ROOT` |
| `public_snapshot_id_grammar` | literal prefix `ams_` plus opaque generated suffix; committed fixtures may name the grammar but must not contain live corpus-derived IDs |
| `snapshot_id_generation` | exact grammar `ams_` plus 32 lowercase hexadecimal characters generated from random bytes or a private-sidecar keyed digest over canonical bounded evidence; no raw source path, raw source ID, raw digest, or private lookup key may be embedded or recoverable from the public ID |
| `public_evidence_fields` | `snapshot_id`, `manifest_source_key`, `source_root_env_var`, `captured_at_utc`, `schema_marker_status`, `generated_timestamp_status`, `content_fingerprint_status`, `row_count_status`, `drift_severity`, `evidence_mode`, and `validator_version` |
| `operational_evidence_fields` | #70-facing evidence artifacts must include `record_schema_version`, `record_id`, `source_issue`, `evidence_artifact_ref`, `validator_ref`, `validator_env`, `validator_command`, `validator_exit_status`, `recorded_at_utc`, `reviewed_commit`, `authorization_status`, `snapshot_ids_by_manifest_source`, `source_status_by_manifest_source`, `drift_verdicts_by_manifest_source_pair`, and `reconciliation_refs` |
| `trusted_reference_rule` | operational request evidence must match the public-safe evidence artifact named by `evidence_artifact_ref`; request payload fields alone cannot certify freshness |
| `drift_eligible_pairs` | closed pair set listed in Drift Comparison Model below; non-listed source pairs are not comparable and cannot emit `compatible` |
| `private_sidecar_fields` | exact file stats, raw digest values, exact private row counts, and private lookup material; never committed to public docs or review artifacts |
| `bounded_caps` | `max_header_bytes`, `max_under_cap_bytes`, and `max_under_cap_rows` |
| `content_fingerprint_status` | closed enum `available_sidecar`, `available_under_cap`, `unavailable`, `not_present` |
| `row_count_status` | closed enum `available_sidecar`, `available_under_cap`, `unavailable`, `not_present` |
| `drift_severity` | closed enum `compatible`, `warning`, `blocker`, `unavailable` |
| `evidence_mode` | closed enum `public_safe_summary`, `private_sidecar_validated`, `missing_manifest`, `blocked_unavailable` |
| `authorization_status` | closed enum `sampling_allowed`, `blocked_requires_reconciliation`, `blocked_unavailable` |
| `compatibility_rule` | above-cap manifests without sidecar content signal cannot be marked `compatible` |
| `mixing_rule` | incompatible manifest snapshots block downstream sampling unless a reconciliation note is present |
| `public_safety_notes` | no raw host paths, raw source IDs, raw source hashes, private lookup keys, personal identifiers, client identifiers, or proprietary snippets |

---

## Operational Evidence JSON Schema

The implementation will define the #70-facing evidence artifact as a closed JSON object with no additional properties. Downstream requests will reference this artifact; they will not satisfy #62 freshness by copying its fields into a request payload.

| Field | JSON type | Required rule |
|---|---|---|
| `record_schema_version` | string | semver under `1.0.x` |
| `record_id` | string | `ace62-` plus lowercase letters, digits, dots, or hyphens; unique within the referenced artifact set |
| `source_issue` | integer | exactly `62` |
| `evidence_artifact_ref` | string | repo-relative POSIX ref under `artifacts/ace-manifest-freshness/` or `tests/fixtures/ace-manifest-freshness/`, ending in `.json`; absolute paths and parent traversal are invalid |
| `validator_ref` | string | exactly `scripts/validate_ace_manifest_freshness.py` unless a later reviewed contract revision changes the validator |
| `validator_env` | object | closed object; only allowed key is `UV_CACHE_DIR`, and the only committed value is `.claude/state/uv-cache` |
| `validator_command` | array of strings | argv-style tokens, not a shell string; must invoke `uv run python scripts/validate_ace_manifest_freshness.py` and the referenced evidence artifact without embedding raw source-root values |
| `validator_exit_status` | integer | exactly `0` for evidence that can satisfy #70; nonzero records are diagnostic only and cannot authorize sampling |
| `recorded_at_utc` | string | UTC RFC3339 timestamp ending in `Z` |
| `reviewed_commit` | string | 40-character lowercase hexadecimal git commit SHA |
| `authorization_status` | string | `sampling_allowed` only when every pair verdict is `compatible`; `blocked_requires_reconciliation` when any pair is `warning` or `blocker`; `blocked_unavailable` when any pair is `unavailable` |
| `snapshot_ids_by_manifest_source` | object | exactly the six manifest source keys; each value matches `ams_` plus 32 lowercase hexadecimal characters |
| `source_status_by_manifest_source` | object | exactly the six manifest source keys; each value is a closed object with `content_fingerprint_status`, `row_count_status`, `evidence_mode`, and `captured_at_utc` |
| `drift_verdicts_by_manifest_source_pair` | object | exactly the five `drift_eligible_pairs` IDs; each value is an object with `left_source`, `right_source`, `left_snapshot_id`, `right_snapshot_id`, `drift_severity`, `evidence_mode`, and `reconciliation_required` |
| `reconciliation_refs` | object | keys are only pair IDs whose verdict is `warning` or `blocker`; values are non-empty arrays of repo-relative artifact refs or GitHub issue/comment URLs; absolute paths and parent traversal are invalid |

Each pair verdict object will be closed:

| Pair verdict field | JSON type | Required rule |
|---|---|---|
| `left_source` | string | equals the pair's left manifest source key |
| `right_source` | string | equals the pair's right manifest source key |
| `left_snapshot_id` | string | equals `snapshot_ids_by_manifest_source[left_source]` |
| `right_snapshot_id` | string | equals `snapshot_ids_by_manifest_source[right_source]` |
| `drift_severity` | string | one of `compatible`, `warning`, `blocker`, or `unavailable` |
| `evidence_mode` | string | one of `public_safe_summary`, `private_sidecar_validated`, `missing_manifest`, or `blocked_unavailable` |
| `reconciliation_required` | boolean | true when severity is `warning` or `blocker`; false only for `compatible` or `unavailable` |

Legal pair verdict combinations:

| `drift_severity` | Legal `evidence_mode` values | Authorization effect |
|---|---|---|
| `compatible` | `public_safe_summary`, `private_sidecar_validated` | allowed only when every pair is compatible and all per-source statuses are sidecar/under-cap backed |
| `warning` | `public_safe_summary`, `private_sidecar_validated` | blocks authorization until reconciliation refs exist and a later reviewed record becomes compatible |
| `blocker` | `public_safe_summary`, `private_sidecar_validated` | blocks authorization until reconciliation refs exist and a later reviewed record becomes compatible |
| `unavailable` | `missing_manifest`, `blocked_unavailable` | blocks authorization; reconciliation refs are not sufficient because evidence is absent |

Trusted-reference matching rules:

- A #70 request may carry only `source_issue=62`, `record_id`, and `evidence_artifact_ref` as its #62 freshness pointer.
- The validator will load `evidence_artifact_ref`, verify the root object schema above, and require the loaded `record_id` and `source_issue` to match the request pointer.
- If the request payload duplicates `validator_command`, `validator_exit_status`, snapshot IDs, drift verdicts, or reconciliation refs instead of relying on the loaded artifact, the validator will reject it as self-attested evidence.
- If any loaded artifact field differs from the request pointer or uses a non-closed key, ref, timestamp, commit, pair ID, status, or severity, the validator will reject it.
- Artifact trust is anchored in `reviewed_commit`, `validator_ref`, `validator_env`, `validator_command`, and `validator_exit_status`; #70 must reject artifacts whose referenced commit or command evidence is missing from the reviewed #62 issue evidence comment.

---

## Drift Comparison Model

The implementation will use this closed key-to-role map:

| Manifest source key | Source role | Count/fingerprint policy |
|---|---|---|
| `INDEX.md` | `root_inventory_index` | Presence, generated marker, and bounded header/status only; no row-count compatibility claim |
| `assets.json` | `asset_manifest` | Asset count is comparable only when under cap or private-sidecar backed |
| `docs/master-index.jsonl` | `master_record_index` | Master record count is comparable only when under cap or private-sidecar backed |
| `_cad-index/index-summary.json` | `cad_summary_index` | CAD summary count is comparable only when under cap or private-sidecar backed |
| `_cad-index/cad-readability-index.tsv` | `cad_readability_index` | CAD readability row count is comparable only when under cap or private-sidecar backed |
| `.ace-knowledge/index.db` | `knowledge_store_index` | Knowledge-store coverage count is comparable only through a bounded sidecar or under-cap synthetic fixture |

Only these source pairs will produce `drift_verdicts_by_manifest_source_pair` entries:

| Pair ID | Left source | Right source | Comparable signal | Non-compatible handling |
|---|---|---|---|---|
| `inventory_to_assets_presence` | `INDEX.md` | `assets.json` | existence, generated timestamp/status, schema marker status | warning or blocker requires a reconciliation ref |
| `assets_to_master_records` | `assets.json` | `docs/master-index.jsonl` | asset count versus master record count when both sides are sidecar/under-cap backed | warning or blocker requires a reconciliation ref |
| `master_records_to_cad_summary` | `docs/master-index.jsonl` | `_cad-index/index-summary.json` | CAD subset count from master records versus CAD summary count | warning or blocker requires a reconciliation ref |
| `cad_summary_to_cad_readability` | `_cad-index/index-summary.json` | `_cad-index/cad-readability-index.tsv` | CAD summary count versus CAD readability row count | warning or blocker requires a reconciliation ref |
| `master_records_to_knowledge_store` | `docs/master-index.jsonl` | `.ace-knowledge/index.db` | master record count versus knowledge-store coverage count | warning or blocker requires a reconciliation ref |

All other pairings are `not_comparable` and will not be emitted as compatible drift verdicts. If a downstream validator needs another pair, it must add the pair through a reviewed contract revision rather than inferring one from the six-key enum.

---

## Pseudocode

```text
load artifacts/ace-wave0-ledger-schema.json
load config/ace-manifest-evidence-contract.json
verify #65 canonical registry marks #52-#60 as requiring manifest snapshot IDs
verify manifest source enum matches docs/plans/ace-share-ingestion-wave-coordination.md
verify manifest source roles and drift-eligible pairs match the #62 contract
read ACE_SHARE_ROOT from environment only at runtime
for each configured manifest source key:
  resolve ACE_SHARE_ROOT plus the closed share-relative key
  collect direct file metadata when present
  read bounded header/summary bytes only within named caps
  accept raw digest or exact row-count material only from private sidecar evidence
  if manifest is under cap, record under-cap status and bounded provenance
  if manifest is above cap and no sidecar exists, record unavailable status
  emit a public-safe snapshot evidence record with opaque snapshot_id
compare only the closed drift-eligible manifest source pairs:
  classify drift as compatible, warning, blocker, or unavailable
  reject compatible verdicts based only on size/timestamp for above-cap manifests
  reject compatible verdicts for non-comparable source pairs
emit a #70-facing operational evidence record:
  set source_issue to 62
  cite the public-safe evidence artifact ref, record id, validator ref,
    validator env, validator command, validator exit status, reviewed commit,
    authorization status, and recorded UTC timestamp
  include snapshot IDs grouped by manifest source key
  include per-source content/row evidence statuses
  include pairwise drift verdicts only for the closed eligible pairs
  include reconciliation refs for warning or blocker pairs
  enforce the closed JSON schema and trusted-reference matching rules
reject configs or examples that perform unbounded source discovery, unrestricted
  manifest querying, full-manifest materialization, or full-file count/fingerprint
  work over large manifests
assemble deny-pattern test strings from neutral fragments so public-scanned
  source files do not retain scan-hostile source-root examples verbatim
emit public-safe case-study examples using synthetic fixtures only
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `config/ace-manifest-evidence-contract.json` | Machine-readable #62 evidence contract imported later by #70 |
| Create | `scripts/validate_ace_manifest_freshness.py` | Executable snapshot/drift validator |
| Create | `tests/test_validate_ace_manifest_freshness.py` | TDD coverage for manifest source enum, bounded caps, drift severity, public/private evidence split, and downstream gates |
| Create | `tests/fixtures/ace-manifest-freshness/` | Synthetic small/large/sidecar/missing manifest fixtures with no private corpus content |
| Create | `docs/case-studies/ace-manifest-freshness-drift-sentinel.md` | Public-safe explanation of the evidence contract and fail-closed drift behavior |
| Modify | `.github/workflows/validate.yml` | Run #62 validator, unit tests, and explicit parent public-scan paths |
| Modify | `docs/16-corpus-lifecycle.md` | Cross-link source snapshot evidence and trust reset |
| Modify | `docs/plans/README.md` | Update #62 status/review summary only when gate status changes |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Update #62 evidence-contract status only when gate status changes |
| Modify | `scripts/validate_ace_epic_wave_coordination.py` | Enforce the #62 coordination row dependency on #65/#70 and exact six-source manifest membership once #62 lands |
| Modify | `tests/test_validate_ace_epic_wave_coordination.py` | Add scan-clean regression coverage for #62 dependency and manifest-source enforcement without adding public-scan-hostile literals |
| Conditional scan-clean modify or follow-on | `skills/format-coverage-ledger/SKILL.md` | Promote manifest snapshot ID requirements only if implementation exposes a reusable ledger method gap |
| Conditional scan-clean modify or follow-on | `skills/source-extraction-coverage/SKILL.md` | Promote bounded source-freshness evidence guidance only if implementation exposes a reusable extraction-coverage gap |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_contract_is_json_and_owned_by_62` | Evidence contract is machine-readable and issue-owned | `config/ace-manifest-evidence-contract.json` | JSON loads with owner, version, schema dependency, and #70 downstream boundary |
| `test_manifest_source_enum_matches_coordination` | #62 consumes the canonical six manifest keys | Contract plus coordination ledger | Exactly `INDEX.md`, `assets.json`, `docs/master-index.jsonl`, `_cad-index/index-summary.json`, `_cad-index/cad-readability-index.tsv`, `.ace-knowledge/index.db` |
| `test_manifest_source_roles_are_closed` | Every manifest key has one role and no unclassified key | Contract plus six-key enum | Roles match the closed `root_inventory_index`, `asset_manifest`, `master_record_index`, `cad_summary_index`, `cad_readability_index`, and `knowledge_store_index` mapping |
| `test_drift_eligible_pairs_are_closed` | Drift pair space is authorable by #70 | Contract JSON | Exactly the five named pair IDs are eligible; all other source pairs are non-comparable |
| `test_imports_65_manifest_required_waves` | Downstream target set is #65-owned | #65 schema plus contract | #52-#60 require manifest snapshot IDs; #62 does not sample |
| `test_ace_share_root_required` | Host portability | Validator config | Runtime source access uses `ACE_SHARE_ROOT` plus closed share-relative keys |
| `test_public_snapshot_id_is_opaque` | Public evidence does not expose raw source identity | Synthetic evidence record plus generation rule | Snapshot ID matches `ams_` plus 32 lowercase hexadecimal characters and is generated only from random or private-sidecar keyed material, not recoverable source identity |
| `test_public_evidence_excludes_private_sidecar_fields` | Public/private split is enforced | Runtime-built public evidence negative fixture with private-like fields | Validator rejects raw path, raw source ID, raw digest, exact private row-count, or lookup material in public records |
| `test_private_sidecar_fields_are_not_committed` | Private evidence stays out of public repo artifacts | Planned artifact path list | Public scan over plan, contract, docs, tests, fixtures, and review artifacts passes |
| `test_public_scanned_sources_avoid_scan_hostile_examples` | #62 validator/tests/fixtures can be scanned by the parent public scanner | Validator/test/doc sources | Negative source-root and private-field examples are assembled from neutral fragments; retained public files pass parent scan |
| `test_bounded_caps_are_named` | Bounded-read limits are explicit | Contract JSON | `max_header_bytes`, `max_under_cap_bytes`, and `max_under_cap_rows` exist |
| `test_no_unbounded_manifest_operations` | Validator rejects unbounded source operations | Runtime-generated negative examples | Unbounded source discovery, unrestricted manifest query, full materialization, and large-manifest count/fingerprint operations fail |
| `test_large_manifest_without_sidecar_is_unavailable` | Size/timestamp-only evidence cannot pass as compatible | Above-cap fixture without sidecar | `content_fingerprint_status=unavailable`; drift severity cannot be `compatible` |
| `test_under_cap_manifest_can_be_fingerprinted_within_caps` | Small synthetic manifests can be validated without sidecars | Under-cap fixture | Status records bounded provenance and allowed content signal |
| `test_sidecar_hash_and_count_are_private_only` | Sidecar evidence can support compatibility without public leakage | Private-sidecar fixture plus public record | Validator can use sidecar at runtime; public artifact contains only opaque snapshot/status fields |
| `test_operational_evidence_json_schema_is_closed_for_70` | #70 can validate #62 evidence without guessing the contract | Operational evidence artifact fixture | Root object rejects extra keys and enforces exact field types, required fields, ref grammar, timestamp format, commit format, snapshot ID grammar, pair IDs, status enums, and reconciliation-ref shape |
| `test_operational_source_statuses_justify_pair_verdicts` | #70 can verify pair verdicts were not based on size/timestamp only | Operational evidence artifact fixture | Each source has content/row evidence statuses; compatible pairs require sidecar or under-cap backing |
| `test_forged_or_self_attested_operational_evidence_fails` | Request payloads cannot certify their own #62 freshness | Self-attested or mismatched operational evidence fixture plus trusted artifact | Validator loads `evidence_artifact_ref` and rejects request fields that do not match the referenced artifact |
| `test_validator_command_and_exit_status_are_required` | Passing evidence is tied to an executable check | Operational evidence fixture missing command or status | Validator rejects incomplete execution proof |
| `test_validator_env_is_separate_from_argv` | Evidence command is portable and schema-valid | Operational evidence fixture with `UV_CACHE_DIR` shell prefix inside command array | Validator requires env settings in `validator_env` and argv tokens in `validator_command` |
| `test_operational_request_pointer_is_minimal` | #70 requests cannot smuggle full #62 proof fields | Request fixture containing duplicated command, status, snapshots, or drift verdicts | Validator accepts only source issue, record ID, and artifact ref as the freshness pointer |
| `test_unavailable_pair_blocks_authorization` | Missing or above-cap unavailable evidence cannot authorize sampling | Operational artifact with an unavailable pair and exit status 0 | `authorization_status=blocked_unavailable`; #70 cannot treat the record as sampling-allowed |
| `test_drift_severity_evidence_mode_matrix_is_closed` | Cross-field verdict combinations are not guessed downstream | Pair verdict fixtures for every severity/mode combination | Only the legal matrix combinations pass |
| `test_reconciliation_refs_are_required_for_noncompatible_pairs` | Pairwise drift results cannot be waved through by free text | Non-compatible broad/CAD fixture without reconciliation refs | Validator reports blocker until reconciliation refs are present |
| `test_drift_severity_closed_set` | Drift classifier cannot invent severities | Compatible/warning/blocker/unavailable examples | Only closed severity enum accepted |
| `test_incompatible_counts_require_reconciliation` | Mixed manifests fail closed | Broad/CAD synthetic mismatch | Blocker unless reconciliation note is present |
| `test_missing_manifest_is_not_stale` | Missing manifests are distinct from stale or incompatible manifests | Missing source fixture | Evidence mode records missing/unavailable without false stale verdict |
| `test_70_consumes_contract_but_62_does_not_patch_67` | Ownership boundary is explicit | Contract metadata | #70 is the downstream consumer; #62 does not implement #67 operational allow-path |
| `test_ci_invokes_manifest_freshness_validator` | CI runs #62 checks | `.github/workflows/validate.yml` | Workflow invokes #62 validator and unit test |
| `test_ci_invokes_parent_public_scan_for_62_paths` | Public-scan gate covers #62 artifacts | Workflow and scan path list | Explicit scan paths cover plan, contract, validator, tests, fixtures, docs, workflow, and retained review artifacts |
| `test_parent_validator_enforces_62_handoff` | #62 dependency handoff cannot drift silently | Coordination row and validator | #62 row must retain #65 as schema source and #70 as downstream consumer for #67 integration |
| `test_parent_validator_manifest_sources_exact_set` | Parent fixture cannot silently drift to five manifest sources | Coordination source inventory | Validator rejects missing or extra manifest source keys |

---

## Acceptance Criteria

- [ ] A standalone issue plan will exist for #62 and will not authorize implementation until adversarial plan review, user approval, `status:plan-approved`, and `.planning/plan-approved/62.md`.
- [ ] `config/ace-manifest-evidence-contract.json` will define the #62 evidence contract and preserve #70 as the downstream consumer for #67 integration.
- [ ] The manifest source enum will match the six-source coordination ledger, including `INDEX.md`.
- [ ] The evidence contract will define a closed manifest-source role map and a closed list of drift-eligible source pairs; non-listed pairs will be non-comparable and cannot be marked `compatible`.
- [ ] The validator will consume #65's `requires_manifest_snapshot_id` booleans for #52-#60 instead of redefining the downstream wave set.
- [ ] Runtime source access will use `ACE_SHARE_ROOT` plus closed share-relative manifest keys.
- [ ] Public evidence records will carry opaque snapshot IDs and bounded status fields only.
- [ ] Public snapshot IDs will be generated only from random or private-sidecar keyed material and will not embed recoverable source identity.
- [ ] #70-facing operational evidence artifacts will be closed JSON objects with exact required fields, JSON types, ref grammar, timestamp format, commit format, snapshot ID grammar, pair IDs, status enums, and reconciliation-ref shape.
- [ ] Operational evidence artifacts will carry per-source content/row evidence statuses and an `authorization_status`; any `warning`, `blocker`, or `unavailable` pair will block #70 authorization until a later reviewed compatible record exists.
- [ ] `UV_CACHE_DIR` will be represented as a closed `validator_env` field, while `validator_command` will remain argv-style tokens.
- [ ] #70 request pointers will carry only `source_issue=62`, `record_id`, and `evidence_artifact_ref`; the validator will load the referenced artifact for the authoritative command, status, snapshots, drift verdicts, and reconciliation refs.
- [ ] Operational evidence will be checked against the public-safe artifact referenced by `evidence_artifact_ref`; request fields alone will not satisfy #62 freshness.
- [ ] Forged, malformed, self-attested, missing-command, missing-status, or artifact-mismatched operational evidence will fail validation.
- [ ] Raw host paths, raw source IDs, raw source hashes, private lookup keys, exact private sidecar values, personal identifiers, client identifiers, and proprietary snippets will be rejected from public artifacts.
- [ ] Freshness checks will use direct file metadata, bounded header/summary probes, under-cap fixtures, or private sidecar evidence only.
- [ ] Large manifests will not be full-counted or full-fingerprinted unless a bounded precomputed sidecar or explicit under-cap declaration is present.
- [ ] Above-cap manifests without sidecar evidence will classify content fingerprint status as `unavailable` and cannot be marked `compatible` from size/timestamp alone.
- [ ] Drift will be classified only as `compatible`, `warning`, `blocker`, or `unavailable`.
- [ ] Incompatible manifest counts will block downstream sampling unless a reconciliation note is present.
- [ ] Public-scanned #62 validator, test, fixture, and documentation sources will avoid retained scan-hostile source-root and private-field examples by assembling negative examples from neutral fragments at runtime.
- [ ] #62 public-scan paths will cover #62-created artifacts only; the existing parent validator test module will remain outside the #62 public-scan path set unless it is separately converted to scan-clean fixtures.
- [ ] #62 will not modify #67's operational sampling allow-path; #70 will own importing this evidence contract into #67.
- [ ] Any reusable method gap exposed by implementation will be promoted to the bound skills or filed as a follow-on issue before closeout.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_manifest_freshness.py` will pass after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_manifest_freshness` will pass after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py`, `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_schema_contract.py`, and `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` will still pass after implementation.

---

## Plan Review Gate Rule

Plan review will be considered passable only when the same review round has at least two usable provider results and no usable provider returns MAJOR. A provider that fails before returning findings may be recorded as `UNAVAILABLE` with the exact reason and does not count toward the usable-provider total. With Gemini currently returning ineligible-tier failures, the effective gate is both Claude and Codex returning no-MAJOR in the same round. If Gemini becomes usable again, its result is no longer advisory: any usable Gemini MAJOR blocks advancement under the same "no usable MAJOR" rule, while a Gemini no-MAJOR can satisfy the usable-provider floor alongside any other no-MAJOR provider. If fewer than two providers are usable, or if any usable provider returns MAJOR, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) remains `draft` and must not move to `status:plan-review`.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Drift model and coordination/evidence-contract gaps |
| Codex r1 | MAJOR | Operational evidence schema under-specified |
| Gemini r1 | UNAVAILABLE | Unsupported local Gemini auth tier |
| Claude r2 | MINOR | Cross-field evidence/status details needed |
| Codex r2 | MAJOR | Public-scan scope and unavailable authorization gaps |
| Gemini r2 | UNAVAILABLE | Unsupported local Gemini auth tier |
| Claude r3 | MINOR | Residual implementation nits only; no blocking defect |
| Codex r3 | APPROVE | No findings in the focused r3 retest scope |
| Gemini r3 | UNAVAILABLE | Unsupported local Gemini auth tier |

**Overall result:** PASSABLE FOR PLAN REVIEW - r3 has two usable provider results and no usable MAJOR. Implementation remains blocked pending explicit user approval, `status:plan-approved`, and `.planning/plan-approved/62.md`.

---

## Risks and Open Questions

- **Risk:** Full counting or fingerprinting of large manifests would violate the bounded-read policy. Implementation will use direct metadata, bounded probes, under-cap fixtures, or private precomputed sidecars.
- **Risk:** Public evidence could accidentally expose private source identity. The contract will split public opaque evidence from private sidecar fields and scan all retained artifacts.
- **Risk:** #62 could drift into #67 operational sampling logic. The plan will keep #67 consumption deferred to [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70).
- **Open:** The exact private sidecar storage location will stay out of public docs until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) defines durable storage/lifecycle behavior.

---

## Complexity

**T2** - This is a bounded cross-wave evidence contract and validator with privacy-sensitive public/private artifact boundaries, but it will not read private content into public artifacts and will not implement #67 operational sampling.
