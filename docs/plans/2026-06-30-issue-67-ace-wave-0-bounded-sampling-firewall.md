# Plan for #67: ACE Wave 0 Bounded Sampling Firewall

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-30
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** r9 Claude MINOR, Codex MAJOR; Gemini unavailable

---

## Resource Intelligence Summary

### Existing repo code/docs

- Source: `artifacts/ace-wave0-ledger-schema.json`
  - Finding: [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will consume the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema contract for route, store, field-group, private-term, success-field, canonical-wave, and split-registry vocabulary; it will not redefine those enums.
- Source: `scripts/validate_ace_wave0_schema_contract.py`
  - Finding: [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will import or read the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema as the authoritative dependency surface and will keep [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) `implementation_ready=false` until the issue has user approval and a local approval marker.
- Source: `scripts/validate_ace_epic_wave_coordination.py`
  - Finding: The parent validator already carries public-surface denial primitives for bounded-read prose, metadata-evidence rows, private/source-like leak checks, and unbounded traversal patterns. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will build a narrower executable-context sampling firewall and will reuse the parent public scanner by explicit path list rather than creating the generalized public-surface scanner owned by [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68). New classifier source will avoid self-blocking by constructing denied command, source-root, and scanner-triggering API tokens from string fragments at runtime, not by committing runnable denied expressions.
- Source: `docs/plans/README.md`
  - Finding: ACE portfolio gates already require bounded sampling to name manifest source, seed/sort rule, per-bucket row cap, maximum files/bytes touched, and denied traversal patterns; [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will make that contract machine-checkable for executable examples and sampling request records.
- Source: `docs/plans/ace-share-ingestion-wave-coordination.md`
  - Finding: The coordination ledger names the six public manifest-source keys and the structural wave registry marks [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) as manifest-backed ingestion waves. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will use that ledger, not the README summary, as the manifest-source authority. It will require recorded [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot evidence before downstream manifest-backed sampling, but it will not implement [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62)'s freshness validator.
- Source: [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) `bound_skill_groups` and live [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) issue body
  - Finding: The schema-bound method surface is exactly `format-coverage-ledger`, `public-private-routing`, `content-triage-and-exclusion`, `page-shape-contract`, and `adversarial-verify-loop`. The live [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) issue-required skill set is `content-triage-and-exclusion`, `source-extraction-coverage`, `format-coverage-ledger`, `public-private-routing`, and `adversarial-verify-loop`; it includes `source-extraction-coverage` and omits `page-shape-contract` relative to #65. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will use and scan the union of those six skill docs, but only the #65 set will populate contract `bound_skill_groups`; `source-extraction-coverage` remains an issue-required supporting skill unless a later approved schema change adds it to #65. The live issue also binds method issues [#1](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/1) and [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12), which [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will record as `method_issue_bindings`.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic. It authorizes coordination and planning only; it does not approve child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains the wave-0 umbrella. It delegates implementation-sized slices to [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) provides the schema dependency that [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) needs for planning and implementation.
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) owns public-token fixtures and private-field placeholders. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will not implement token grammar, placeholder grammar, lookup maps, or durable token fixtures.
- [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) owns the reusable public-surface self-scan. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will use explicit self-scan path lists for its own public artifacts only.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) owns the repo-local legal/security scan gate. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) full closeout will remain blocked if that script is unavailable.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) will own manifest freshness and snapshot IDs. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will require recorded [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence for downstream manifest-backed sampling requests and will fail closed when that evidence is missing or placeholder-only.
- [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) will own the post-[#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) integration that ratifies the #62 evidence contract and teaches [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) to parse and compare operational evidence. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will not implement that parser in this approval unit.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) will own durable private storage and lifecycle. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will not write durable stores, route public outputs, or publish derived summaries.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will own publication certification and public-output canaries. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will not authorize public docs nav, `mkdocs.yml`, `llm-wiki`, or external publication exposure.

### Source inventory

- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will not read private ACE content and will pass with `ACE_SHARE_ROOT` unset.
- Test fixtures will be synthetic and metadata-only. They will not contain raw private source paths, raw source identifiers, raw digests, client identifiers, personal identifiers, exact private inventory counts, or proprietary snippets.
- Allowed manifest source names will be the public metadata keys named by `docs/plans/ace-share-ingestion-wave-coordination.md`: `INDEX.md`, `assets.json`, `docs/master-index.jsonl`, `_cad-index/index-summary.json`, `_cad-index/cad-readability-index.tsv`, and `.ace-knowledge/index.db`.
- Runtime negative fixtures will assemble denied command, source-root, and scanner-triggering API-token examples from fragments or write them to temporary files outside the repo tree so committed public artifacts do not self-block their own scanner.

### Gaps identified

- Before this draft, no standalone [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) plan existed; this plan fills that planning gap but remains unreconciled after r9 MAJOR review until the next patch/re-review cycle passes.
- No repo-local sampling firewall contract exists for executable contexts.
- No executable-context classifier exists to distinguish policy prose from runnable shell, Python, query, workflow, or inline command examples.
- No [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator exists to reject unbounded traversal, full-manifest materialization, full-file hashing/counting of large manifests, unrestricted raw manifest reads, or missing bounded-sampling fields.
- No [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) fixture set exists for safe bounded sampling requests, missing [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence, or runtime-generated deny examples.
- CI does not yet run a [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator or its unit tests.

### Evidence

**Issue status** (verified 2026-06-30):

```text
#67 OPEN ACE wave 0 split: bounded sampling firewall labels=strengthening,lane:codex,priority:high
```

**Dependency evidence** (verified 2026-06-30):

```text
#65 carries status:plan-approved and a local approval marker at .planning/plan-approved/65.md.
#67 has no status label, no local approval marker, and no existing plan file before this draft.
#66 and #68 remain draft/blocked-draft and are not prerequisites for #67 unless this plan expands into token fixtures or reusable public-surface scanner behavior.
```

**File existence** (verified 2026-06-30):

```text
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS tests/test_validate_ace_wave0_schema_contract.py
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS tests/test_validate_ace_epic_wave_coordination.py
MISSING config/ace-bounded-sampling-firewall-contract.json
MISSING config/
MISSING scripts/ace_bounded_sampling_firewall.py
MISSING scripts/validate_ace_bounded_sampling_firewall.py
MISSING tests/test_validate_ace_bounded_sampling_firewall.py
MISSING tests/fixtures/ace-bounded-sampling-firewall/good-request.json
MISSING tests/fixtures/ace-bounded-sampling-firewall/downstream-shape-only-request.json
```

**Reproduction proofs**:
N/A - governance/control-plane issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md` |
| Sampling firewall contract | `config/ace-bounded-sampling-firewall-contract.json` |
| Executable-context classifier | `scripts/ace_bounded_sampling_firewall.py` |
| Contract validator | `scripts/validate_ace_bounded_sampling_firewall.py` |
| Unit tests | `tests/test_validate_ace_bounded_sampling_firewall.py` |
| Safe fixture directory | `tests/fixtures/ace-bounded-sampling-firewall/` |
| Safe happy-path fixture | `tests/fixtures/ace-bounded-sampling-firewall/good-request.json` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Schema split registry update | `artifacts/ace-wave0-ledger-schema.json` |
| Workflow | `.github/workflows/validate.yml` |
| Safe shape-only downstream fixture | `tests/fixtures/ace-bounded-sampling-firewall/downstream-shape-only-request.json` |
| Schema-bound skill docs | `skills/format-coverage-ledger/SKILL.md`, `skills/public-private-routing/SKILL.md`, `skills/content-triage-and-exclusion/SKILL.md`, `skills/page-shape-contract/SKILL.md`, `skills/adversarial-verify-loop/SKILL.md` |
| Issue-required supporting skill doc | `skills/source-extraction-coverage/SKILL.md` |
| Review artifact - Claude r1 | `scripts/review/results/2026-06-30-plan-67-claude-r1.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-06-30-plan-67-codex-r1.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-06-30-plan-67-gemini-r1.md` |
| Disagreement report r1 | `scripts/review/results/2026-06-30-plan-67-disagreement-r1.md` |
| Review artifact - Claude r2 | `scripts/review/results/2026-06-30-plan-67-claude-r2.md` |
| Review artifact - Codex r2 | `scripts/review/results/2026-06-30-plan-67-codex-r2.md` |
| Review artifact - Gemini r2 | `scripts/review/results/2026-06-30-plan-67-gemini-r2.md` |
| Disagreement report r2 | `scripts/review/results/2026-06-30-plan-67-disagreement-r2.md` |
| Review artifact - Claude r3 | `scripts/review/results/2026-06-30-plan-67-claude-r3.md` |
| Review artifact - Codex r3 | `scripts/review/results/2026-06-30-plan-67-codex-r3.md` |
| Review artifact - Gemini r3 | `scripts/review/results/2026-06-30-plan-67-gemini-r3.md` |
| Disagreement report r3 | `scripts/review/results/2026-06-30-plan-67-disagreement-r3.md` |
| Review artifact - Claude r4 | `scripts/review/results/2026-06-30-plan-67-claude-r4.md` |
| Review artifact - Codex r4 | `scripts/review/results/2026-06-30-plan-67-codex-r4.md` |
| Review artifact - Gemini r4 | `scripts/review/results/2026-06-30-plan-67-gemini-r4.md` |
| Disagreement report r4 | `scripts/review/results/2026-06-30-plan-67-disagreement-r4.md` |
| Review artifact - Claude r5 | `scripts/review/results/2026-06-30-plan-67-claude-r5.md` |
| Review artifact - Codex r5 | `scripts/review/results/2026-06-30-plan-67-codex-r5.md` |
| Review artifact - Gemini r5 | `scripts/review/results/2026-06-30-plan-67-gemini-r5.md` |
| Disagreement report r5 | `scripts/review/results/2026-06-30-plan-67-disagreement-r5.md` |
| Review artifact - Claude r6 | `scripts/review/results/2026-06-30-plan-67-claude-r6.md` |
| Review artifact - Codex r6 | `scripts/review/results/2026-06-30-plan-67-codex-r6.md` |
| Review artifact - Gemini r6 | `scripts/review/results/2026-06-30-plan-67-gemini-r6.md` |
| Disagreement report r6 | `scripts/review/results/2026-06-30-plan-67-disagreement-r6.md` |
| Review artifact - Claude r7 | `scripts/review/results/2026-06-30-plan-67-claude-r7.md` |
| Review artifact - Codex r7 | `scripts/review/results/2026-06-30-plan-67-codex-r7.md` |
| Review artifact - Gemini r7 | `scripts/review/results/2026-06-30-plan-67-gemini-r7.md` |
| Disagreement report r7 | `scripts/review/results/2026-06-30-plan-67-disagreement-r7.md` |
| Review artifact - Claude r8 | `scripts/review/results/2026-06-30-plan-67-claude-r8.md` |
| Review artifact - Codex r8 | `scripts/review/results/2026-06-30-plan-67-codex-r8.md` |
| Review artifact - Gemini r8 | `scripts/review/results/2026-06-30-plan-67-gemini-r8.md` |
| Disagreement report r8 | `scripts/review/results/2026-06-30-plan-67-disagreement-r8.md` |
| Review artifact - Claude r9 | `scripts/review/results/2026-06-30-plan-67-claude-r9.md` |
| Review artifact - Codex r9 | `scripts/review/results/2026-06-30-plan-67-codex-r9.md` |
| Review artifact - Gemini r9 | `scripts/review/results/2026-06-30-plan-67-gemini-r9.md` |
| Disagreement report r9 | `scripts/review/results/2026-06-30-plan-67-disagreement-r9.md` |
| Provider stderr sidecars | not retained unless normalized, scanned, and explicitly listed |

---

## Deliverable

After approval and implementation, [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will provide a repo-local bounded sampling firewall contract, executable-context classifier, validator, fixtures, tests, and CI wiring that reject unbounded ACE sampling commands, accept only [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) metadata-only self-check fixture records in this approval unit, and return fail-closed metadata-only result records for downstream manifest-backed requests until [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) defines an evidence contract and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) imports it. This unit will not authorize operational downstream sampling; [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) will own the first operational allow-path.

---

## Proposed Contract Shape

The implementation will create a closed JSON contract with these top-level fields:

| Field | Proposed rule |
|---|---|
| `contract_id` | exactly `ace-bounded-sampling-firewall` |
| `contract_version` | semver under `1.0.x` |
| `owner_issue` | exactly `67` |
| `depends_on_schema_issue` | exactly `65` |
| `method_issue_bindings` | exactly [#1](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/1) and [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12), matching the live [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) issue body |
| `allowed_manifest_sources` | exactly the six public metadata keys listed in this plan's Source inventory |
| `required_sampling_fields` | target issue, manifest source, seed, sort rule, per-bucket row cap, maximum files touched, maximum bytes touched, request class, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence requirement, output shape, route target, logical target store, and either a #65 target wave class for operational requests or a #67 fixture scope for metadata-only fixtures |
| `maximum_caps` | per-bucket row cap no greater than `200`, maximum files touched no greater than `25`, maximum bytes touched no greater than `1048576`, matching the coordination ledger bounded-read contract |
| `request_classes` | `control_plane_proof`, `downstream_manifest_backed_sampling`, and `metadata_only_fixture`; request class must match the closed mapping table below |
| `target_issue_gate` | target issues whose [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) `requires_manifest_snapshot_id=true` must use `downstream_manifest_backed_sampling`; exempt classes are invalid for those issues |
| `seed_rule` | fixed, reviewable seed identifiers only; random, clock-derived, user-local, or unstated seeds fail |
| `sort_rule` | exactly the closed JSON shape in `Sort Rule Shape`; #65 private schema terms may appear only as array values; no raw private values, raw private-key assignments, or unknown sort keys are allowed |
| `requires_manifest_snapshot_id_gate` | imported from the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) canonical wave registry and used as the single source of truth for which target issues require [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence |
| `downstream_snapshot_gate` | target issues with [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) `requires_manifest_snapshot_id=true` fail closed for operational sampling until [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) defines an evidence contract and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) imports it into [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) |
| `snapshot_evidence_schema` | neutral keys for evidence mode, source issue, blocked-by issue, follow-on issue, reason code, optional shape-only artifact reference, and recorded-at date; allowed on downstream requests and on #67 metadata-only fixtures used solely for shape parsing |
| `metadata_fixture_scope` | exactly `firewall_validator_self_check`; valid only when `target_issue=67` and `request_class=metadata_only_fixture` |
| `output_shape_route_store` | exactly `output_shape=metadata_only_request_record`, `route_target=metadata_only`, and `logical_target_store=metadata_ledger_store`; every other #65 route/store value, including public, private, excluded, or mismatched route/store pairs, fails in this approval unit |
| `request_outcomes` | only [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) `metadata_only_fixture` requests pass; control-plane proof and downstream rows are recognized to produce explicit fail-closed outcomes, not accepted sampling authorization |
| `manifest_source_read_denial_tokens` | every allowed manifest source key, including `INDEX.md`, is paired with every #67 raw-read operator token family in runtime deny fixtures; no source key can rely only on the inherited parent scanner pattern |
| `denied_token_matrix` | concrete runtime-assembled token fragments for source-root traversal, broad source-root discovery, manifest query, raw manifest read, full-file count, full-file digest, recursive Python walk, and recursive path-glob APIs; each token family maps to a denied executable class |
| `executable_context_triggers` | closed enum for markdown fence, markdown list command, markdown inline command, workflow run block, Python string passed to classifier, and JSON request field |
| `command_verb_classes` | closed enum for traversal, broad search/list, manifest query, raw manifest read, full-file fingerprint/count, and full materialization |
| `source_root_token_classes` | closed enum for ACE root abstraction, manifest key token, and synthetic fixture token |
| `manifest_operation_classes` | closed enum for bounded metadata probe, bounded sample selection, snapshot evidence check, and denied unbounded operation |
| `denied_executable_classes` | recursive traversal, broad list/search over the source root, unrestricted manifest query, raw manifest read, full-file hashing/counting of large manifests, and unbounded materialization |
| `public_safety_notes` | no private source content, raw host paths, raw source values, raw digests, exact private inventory counts, client identifiers, personal identifiers, or publication destinations |

The implementation will not create public tokens, private lookup maps, durable storage locations, manifest freshness snapshots, public-output canaries, legal/security scans, docs navigation, or publication outputs.

### Request Class Mapping

| Target issue set | Target wave class or fixture scope | Recognized request class | #67 outcome |
|---|---|---|---|
| [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) | `ingestion_wave` | `downstream_manifest_backed_sampling` | fails closed with `MISSING_62_EVIDENCE_CONTRACT` until [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) imports a reviewed [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence contract |
| [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) | `control_plane` | `control_plane_proof` | recognized as a non-sampling proof and fails closed with `CONTROL_PLANE_PROOF_NOT_SAMPLING_REQUEST` if submitted for sampling authorization |
| [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) | `storage_lifecycle_gate` | `control_plane_proof` | recognized as a non-sampling proof and fails closed with `CONTROL_PLANE_PROOF_NOT_SAMPLING_REQUEST` |
| [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) | `manifest_freshness_gate` | `control_plane_proof` | recognized as a non-sampling proof and fails closed with `CONTROL_PLANE_PROOF_NOT_SAMPLING_REQUEST` |
| [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) | `public_canary_gate` | `control_plane_proof` | recognized as a non-sampling proof and fails closed with `CONTROL_PLANE_PROOF_NOT_SAMPLING_REQUEST` |
| [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) | `fixture_scope=firewall_validator_self_check` | `metadata_only_fixture` | passes as a validator self-check fixture; invalid for [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) and cannot authorize operational sampling |

Operational requests must use a `target_wave_class` imported from the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) canonical wave registry. The [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) metadata-only fixture row intentionally uses `fixture_scope` instead of `target_wave_class` because [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) is a split control-plane validator issue, not a canonical ingestion wave. Matching this table is necessary but not sufficient for an accepted request: only the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) metadata-only fixture row passes in this approval unit. Every other recognized row returns the listed fail-closed outcome, and any request whose `target_issue`, target class/scope, and `request_class` do not match this table fails with a mismatch reason.

[#64](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/64) is a planning placeholder outside the #65 canonical wave registry and the wave-0 split registry; it is not a sampling-request target. [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66), [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68), and [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) are split control-plane support issues that own token fixtures, public-surface scanning, and legal/security scanning. They will fail closed as sampling-request targets unless a later approved plan explicitly adds metadata-only fixture scopes for them.

### Output Shape and Route/Store Boundary

The contract will import the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) route/store vocabulary for compatibility checks, but [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will allow only the metadata-only route/store pair in passing self-check fixtures:

| Field | Only valid value in #67 |
|---|---|
| `output_shape` | `metadata_only_request_record` |
| `route_target` | `metadata_only` |
| `logical_target_store` | `metadata_ledger_store` |

The validator will reject `public_llm_wiki`, `private_sidecar`, `excluded_no_ingest`, `public_llm_wiki_store`, `private_sidecar_store`, `excluded_no_store`, missing route/store fields, or any route/store mismatch as accepted output shapes. Fail-closed control-plane and downstream results use the same metadata-only request/result shape; they are failure records, not publication, private-storage, or operational-ingestion records.

### Snapshot Evidence Shape

For `downstream_manifest_backed_sampling`, the request will carry a `snapshot_evidence` object with these neutral fields and will fail closed in this plan. A `metadata_only_fixture` may carry `snapshot_evidence` if and only if `evidence_mode=shape_only_fixture`; this is parser coverage only and cannot authorize operational sampling. `snapshot_evidence` with any other evidence mode is invalid on `metadata_only_fixture`.

| Field | Rule |
|---|---|
| `evidence_mode` | `shape_only_fixture` for [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) metadata-only fixtures or `blocked_pending_62_contract` for operational downstream requests; `operational_live` is reserved for [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) and invalid in this plan |
| `source_issue` | exactly `62` |
| `blocked_by_issue` | exactly `62` when evidence mode is `blocked_pending_62_contract` |
| `follow_on_issue` | exactly `70` when evidence mode is `blocked_pending_62_contract` |
| `reason_code` | exactly `MISSING_62_EVIDENCE_CONTRACT` until [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) is planned, approved, and implemented |
| `shape_only_artifact_ref` | optional repo-relative public-safe fixture reference; ignored for operational authorization |
| `recorded_at` | ISO date for the evidence record |

Shape-only fixtures will prove this object shape can be parsed with synthetic public-safe values, but they will not satisfy operational downstream sampling. Operational downstream sampling will fail closed with `MISSING_62_EVIDENCE_CONTRACT` and a pointer to [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70). This plan will not parse checker paths, passing-command evidence, exit codes, snapshot IDs, or snapshot artifact contents from a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) artifact; [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) will add that behavior after [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) owns a reviewed evidence schema. The validator will still reject placeholder, negated, pending, not-run, missing, forged, or expected-only evidence.

The discriminator between the recognized blocked state and rejected placeholder wording is exact enum matching: `evidence_mode=blocked_pending_62_contract` plus `reason_code=MISSING_62_EVIDENCE_CONTRACT` is recognized only as the expected fail-closed operational result, and the validator returns failure/nonzero rather than authorizing sampling. Free-text `pending`, `not-run`, `expected`, `todo`, or equivalent placeholder wording in any evidence field fails.

### Fixture Payload Contract

| Fixture | Required target fields | Snapshot evidence | Expected result |
|---|---|---|---|
| `good-request.json` | all required sampling fields; distinguishing fields are `target_issue=67`, `request_class=metadata_only_fixture`, `fixture_scope=firewall_validator_self_check`, `output_shape=metadata_only_request_record`, `route_target=metadata_only`, and `logical_target_store=metadata_ledger_store` | absent | Passes as metadata-only fixture |
| `downstream-shape-only-request.json` | all required sampling fields; distinguishing fields are `target_issue=67`, `request_class=metadata_only_fixture`, `fixture_scope=firewall_validator_self_check`, `output_shape=metadata_only_request_record`, `route_target=metadata_only`, and `logical_target_store=metadata_ledger_store` | present with `evidence_mode=shape_only_fixture` and `source_issue=62` | Passes schema parsing only; cannot authorize sampling |
| Runtime downstream blocked fixture | all required sampling fields; distinguishing fields are target issue in [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60), `target_wave_class=ingestion_wave`, `request_class=downstream_manifest_backed_sampling`, `output_shape=metadata_only_request_record`, `route_target=metadata_only`, and `logical_target_store=metadata_ledger_store` | present with `evidence_mode=blocked_pending_62_contract`, `blocked_by_issue=62`, `follow_on_issue=70`, and `reason_code=MISSING_62_EVIDENCE_CONTRACT` | Fails closed with the same reason code |

### Sort Rule Shape

`sort_rule` will be an object with exactly these keys:

| Key | Rule |
|---|---|
| `strategy` | exactly `stable_private_term_order` |
| `term_refs` | non-empty array; every value must match a [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) private schema term |
| `direction` | one of `ascending` or `descending` |
| `tie_breaker` | exactly `public_manifest_row_ordinal` |

Unknown keys fail. Private schema terms may appear only as `term_refs` values; they may not be used as object keys or assigned to raw private values.

---

## Executable-Context Classifier Contract

The classifier will classify only these public artifact contexts as executable:

| Context | Executable when |
|---|---|
| Markdown fenced code | fence info string is exactly one of `sh`, `bash`, `zsh`, `shell`, `python`, `py`, `sql`, `jq`, `jsonpath`, `yaml-workflow`, `workflow-run`, `command`, or `proof`; unlabeled or `text` fences fail closed when they contain both a source-root abstraction and command-like syntax |
| Markdown list command | the list item begins with `$ `, `> `, `run:`, `command:`, `proof command:`, `allowed command:`, or `rejected command:` and is under a heading whose normalized text is exactly `commands`, `proof`, `validation`, `run`, or `rejected commands` |
| Markdown inline code | the inline code span is immediately preceded in the same sentence by exactly `run:`, `command:`, `proof command:`, `allowed command:`, `rejected command:`, or `script invocation:`; inline code under other prose fails closed when it contains both a source-root abstraction and command-like syntax |
| GitHub workflow YAML | a `run` block or inline run command contains the text |
| Python source or tests | string literals passed into classifier/validator APIs and subprocess-like call sites are executable examples; policy constant names and docstrings are prose unless explicitly fed to the classifier in a test |
| JSON fixtures | request fields carrying command, query, source root, manifest operation, or sampling expression are executable examples |

The classifier will classify policy prose as non-executable only when it names denial classes without a runnable source-root expression. Unknown contexts will fail closed when they contain a source-root abstraction plus command-like syntax. Denied examples in committed tests will be built from string fragments at runtime or written to temporary files outside the repo tree.

The classifier will use this closed discrimination rule:

| Rule family | Closed rule |
|---|---|
| Source-root token | The root abstraction token will be constructed from fragments inside classifier/test sources so committed source remains public-scan clean while runtime fixtures still exercise the full token. |
| Command verb class | Command verbs will be represented as neutral enum values in the contract and assembled from fragments in runtime deny fixtures; committed source will not carry runnable source-root expressions. |
| Recursive API token | Scanner-triggering recursive API names will be represented as neutral enum values and assembled from fragments only in runtime deny fixtures, because the parent scanner treats those tokens as unconditional denials. |
| Executable triggers | A context is executable only when a closed syntax trigger and a closed source/manifest operation class both appear in an executable artifact context. |
| Policy-prose anchors | Non-executable policy prose is limited to named headings or rows that describe denial classes without runnable source-root expressions. |
| Unknown contexts | Unknown contexts containing both a source-root abstraction and command-like syntax fail closed. |
| Exemption policy | No whole-file or whole-directory scanner exemption will be added. Any future allow-context must be line-scoped, path-restricted, and covered by tests, but the default implementation path is fragment assembly rather than exemption. |

### Concrete Denied Token Matrix

The contract will define concrete token fragments for each denied class. The implementation will assemble the executable examples only at runtime so committed public artifacts remain scan-clean, but the token matrix itself will be closed and testable.

| Denied class | Runtime-assembled token families | Required coverage |
|---|---|---|
| Recursive traversal | shell recursive search/list/size families, Python recursive walk API family, path recursive glob API family | Every family maps to recursive traversal and fails in executable contexts |
| Broad source-root discovery | shell broad search/list families against the source-root token class | Every source-root discovery family fails unless a later approved issue adds a bounded manifest-sidecar contract |
| Unrestricted manifest query | JSON/query tool family against every allowed manifest source key | Every allowed manifest source key is covered, including `INDEX.md` |
| Raw manifest read | raw file reader family against every allowed manifest source key | Every allowed manifest source key is covered, including `INDEX.md` |
| Full-file counting | line/byte/word counting family against source-root and manifest-source token classes | Full-file counting fails unless the bounded precomputed sidecar exception is explicitly cited by a later approved issue |
| Full-file digest | digest/fingerprint family against source-root and manifest-source token classes | Full-file digest fails unless the bounded precomputed sidecar exception is explicitly cited by a later approved issue |

The #67 token matrix will not rely on the inherited parent scanner's manifest-path pattern for completeness because that pattern is not the #67 source authority. The #67 validator will pair each allowed manifest source from the coordination ledger with each raw-read/query/count/digest token family in runtime fixtures; a missing pair fails tests before approval.

---

## Pseudocode

```text
load #65 schema contract
assert #67 split row depends only on #65 and remains implementation_ready=false
load #67 sampling firewall contract
validate contract metadata:
  owner issue, schema dependency, method issue bindings, exact #65 bound skill groups
validate allowed manifest source enum:
  exact public metadata key set from coordination ledger
  parent manifest path helper is treated as non-authoritative for #67 source enumeration
  no parent scanner broadening around generic manifest filenames is required for #67
validate bounded sampling grammar:
  target issue is present
  operational requests carry a #65 target wave class
  #67 metadata-only fixtures carry fixture_scope instead of target wave class
  request class is closed
  target issue, target class/scope, and request class match the request-class mapping table
  only #67 metadata_only_fixture requests pass
  control_plane_proof rows fail closed as non-sampling proofs
  downstream_manifest_backed_sampling rows fail closed until #70 imports #62 evidence
  manifest source is present and allowed
  seed is present, fixed, reviewable, and not random or clock-derived
  sort rule has exactly strategy, term_refs, direction, and tie_breaker keys
  sort term_refs use #65 private schema terms as values only
  unknown sort keys, raw private value expressions, and assigned private-key forms fail
  per-bucket cap, max files touched, and max bytes touched are positive integers
  caps do not exceed 200 rows, 25 files, or 1048576 bytes
  output_shape is exactly metadata_only_request_record
  route_target is exactly metadata_only
  logical_target_store is exactly metadata_ledger_store
  the metadata_only to metadata_ledger_store pair matches the #65 route-store matrix
  public/private/excluded route targets, public/private/excluded stores, and mismatched pairs fail
validate downstream sampling gate:
  target issues whose #65 requires_manifest_snapshot_id is true require downstream_manifest_backed_sampling
  those target issues reject control_plane_proof and metadata_only_fixture
  #65 requires_manifest_snapshot_id is the single source of truth and is tested for sync
  #64, #66, #68, and #69 are explicitly non-targets unless later approved scopes exist
  downstream_manifest_backed_sampling requires a complete snapshot_evidence object
  operational ingestion-wave requests fail closed with MISSING_62_EVIDENCE_CONTRACT
  operational ingestion-wave requests record blocked_by_issue=62 and follow_on_issue=70
  blocked_pending_62_contract is a failure result, never an authorization result
  request-provided operational_live evidence fails because #70 owns that parser
  controlled fixtures, not ambient repo state, cover missing-#62 negative cases
  shape-only fixtures can pass schema parsing but cannot authorize sampling
  placeholder, negated, pending, not-run, forged, or expected-only evidence fails
  control-plane proof and metadata-only fixture classes do not require live #62 execution
validate executable contexts:
  markdown, workflow, Python, and JSON contexts are classified by closed rule families
  executable_context_triggers, command_verb_classes, source_root_token_classes,
  and manifest_operation_classes are closed enums in the contract
  concrete denied-token fragments are closed and assembled only in runtime fixtures
  denied vocabularies are imported from or checked against the parent scanner constants
  #67 adds executable-context classification around the shared denied vocabulary
  policy prose naming denied classes is allowed only when no runnable source-root expression exists
  unknown runnable-looking contexts fail closed
  classifier/test sources assemble denied command, source-root, and recursive API fixtures from fragments
  no whole-file or whole-directory scanner exemption is introduced
validate denied executable classes:
  recursive traversal over source root fails
  broad list/search over source root fails
  unrestricted manifest query fails
  raw manifest read fails
  every allowed manifest source key, including INDEX.md, is covered by raw-read/query fixtures
  every inherited parent denied-token family has a #67 runtime fixture or an explicit #67-only rationale
  full-file hashing/counting of large manifests fails unless a later approved issue
  explicitly supplies a bounded precomputed sidecar contract
validate source-root refusal boundary:
  any representative source-root-touching operation routes through the refusal helper
  ACE_SHARE_ROOT set to a temp sentinel tree returns ACE_SOURCE_ROOT_ACCESS_FORBIDDEN
  no sentinel content, stat metadata, directory iteration, globbing, or scanner entrypoint is touched
validate public-safety boundaries:
  no raw private source paths, raw source values, source-like digest assignments,
  client identifiers, personal identifiers, proprietary snippets, or exact private counts
derive the #67 public-scan manifest using bounded rules:
  static plan-owned paths: this plan, README, coordination ledger, schema split registry,
  contract JSON, classifier, validator, unit tests, safe fixtures, workflow,
  changed skill docs, and approval marker when present
  review artifacts: prefix-scoped files matching the retained plan-67 review artifact naming
  convention under scripts/review/results/
  provider stderr sidecars are either deleted or explicitly normalized and scanned before retention
  any retained rN review artifact missing from the derived manifest fails before scanning
validate CI public-scan wiring:
  workflow runs the #67 validator and unit tests
  #67 validator forwards each derived manifest path to the parent scanner as an explicit
  --scan-public-path argument; CI does not hand-maintain a growing rN artifact list
validate schema split registry:
  #67 plan_path records this plan path
  #67 status_snapshot records draft/review/approval transitions only when gates advance
  #67 implementation_ready remains false until user approval and implementation
run parent coordination validator and #65 schema validator
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create directory if absent | `config/` | Parent directory for the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) contract file; absent in the current checkout |
| Create | `config/ace-bounded-sampling-firewall-contract.json` | Machine-readable [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) bounded sampling grammar, executable-context rules, denied classes, caps, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence requirement, and public-safety notes |
| Create | `scripts/ace_bounded_sampling_firewall.py` | Reusable executable-context classifier and bounded sampling validator library for repo-local artifacts and synthetic request records |
| Create | `scripts/validate_ace_bounded_sampling_firewall.py` | CLI validator for the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) contract, fixtures, public-surface path list, [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema compatibility, and parent coordination compatibility |
| Create | `tests/test_validate_ace_bounded_sampling_firewall.py` | Unit tests for contract loading, bounded grammar, executable-context classification, denied pattern runtime fixtures, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) gate semantics, public-safety scan, and CI path coverage |
| Create | `tests/fixtures/ace-bounded-sampling-firewall/good-request.json` | Safe metadata-only happy-path request fixture that contains no private source values and no live source-root reads |
| Create | `tests/fixtures/ace-bounded-sampling-firewall/downstream-shape-only-request.json` | Safe shape-only [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence fixture that exercises schema parsing but cannot authorize operational sampling |
| Modify | `.github/workflows/validate.yml` | Run the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator and unit tests after approved implementation |
| Modify after review/status changes | `docs/plans/README.md` | The draft row exists; later changes will record review/approval/implementation status only after the gate actually advances |
| Modify after review/status changes | `docs/plans/ace-share-ingestion-wave-coordination.md` | The draft split row exists; later changes will record review/approval/implementation status only after the gate actually advances |
| Modify | `artifacts/ace-wave0-ledger-schema.json` | Record the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) plan path/status in the split registry without changing [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) route/store/schema terms |
| Avoid broad modify | `scripts/validate_ace_epic_wave_coordination.py` | Do not expand parent scanner helper patterns around generic manifest filenames for [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67); #67 source enumeration will come from its contract and coordination ledger |
| Avoid modify | `tests/test_validate_ace_epic_wave_coordination.py` | Keep #67-specific source-authority and schema-registry assertions in the #67 test module while still running the parent suite as a regression check |
| Conditional modify or follow-on | Schema-bound and issue-required skill docs listed in Artifact Map | Update only if implementation reveals a reusable method gap and changed skill docs pass the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) public scan; otherwise file a follow-on issue |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_contract_file_is_json_and_owned_by_67` | Contract is machine-readable and issue-scoped | Contract JSON | Loads with `contract_id`, version, owner issue, schema dependency, and public-safety notes |
| `test_contract_imports_65_schema_terms` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) consumes, not redefines, [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) terms | Contract plus #65 schema | Route/store/success/private-term references and bound skill groups match #65 exactly |
| `test_issue_required_skill_groups_are_available_and_scanned` | The plan honors the live [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) issue body without polluting #65 schema-bound groups | Skill doc paths from Artifact Map plus live issue bindings | The issue-required five-skill set and the #65 bound five-skill set reconcile to the scanned six-skill union; `source-extraction-coverage` is not inserted into contract `bound_skill_groups`; method issue bindings are exactly [#1](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/1) and [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) |
| `test_allowed_manifest_sources_are_closed` | Manifest source set cannot drift | Contract manifest source list | Exactly the six public metadata keys are allowed |
| `test_bounded_sampling_fields_are_required` | Sampling request grammar is complete | Synthetic request missing one field at a time | Missing target issue, operational target wave class or fixture scope, manifest source, seed, sort rule, per-bucket cap, max files, max bytes, request class, or output shape fails |
| `test_output_shape_route_store_is_metadata_only` | #67 imports #65 route/store terms without accepting publication or private-storage output shapes | Synthetic requests using each #65 route target/store value and mismatched route/store pairs | Only `output_shape=metadata_only_request_record`, `route_target=metadata_only`, and `logical_target_store=metadata_ledger_store` pass the shape check; public, private, excluded, missing, or mismatched values fail |
| `test_sampling_caps_are_enforced` | Caps cannot exceed the coordination-ledger bounded-read contract | Synthetic requests with above-limit caps | Requests over 200 rows, 25 files, or 1048576 bytes fail |
| `test_request_class_mapping_covers_every_recognized_target_outcome` | Mapping table is explicit about pass vs fail-closed outcomes | Contract mapping table | Only the #67 metadata-only fixture row passes; #51/#61/#62/#63 control-plane proof rows fail closed as non-sampling proofs; #52-#60 downstream rows fail closed pending #70; #64/#66/#68/#69 fail with non-target reasons |
| `test_requires_manifest_snapshot_id_imports_65_gate` | #67 does not duplicate the #62 snapshot-gate discriminator | #65 canonical registry plus #67 contract | Every target with `requires_manifest_snapshot_id=true` requires downstream snapshot gating; false targets do not |
| `test_request_class_must_match_target_wave` | Downstream waves cannot self-select an exempt class | Synthetic request for [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) with exempt request class | Fails with target issue/wave mismatch |
| `test_downstream_sampling_requires_62_snapshot_evidence` | Manifest-backed ingestion waves cannot sample without [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence | Synthetic downstream request without complete evidence | Fails with [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) gate error |
| `test_downstream_shape_only_fixture_accepts_complete_62_evidence_shape` | Positive #62 evidence shape is parseable without authorizing sampling | Shape-only [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) fixture with complete public-safe evidence object | Passes schema parsing and remains invalid for operational downstream sampling |
| `test_downstream_sampling_fails_with_missing_62_evidence_fixture` | Missing authoritative [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence fails without depending on ambient repo state | Controlled temp fixture with no #62 evidence artifact | Fails with missing-evidence-contract error |
| `test_downstream_operational_sampling_blocked_until_70` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) does not invent the [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence parser | Synthetic downstream request with `operational_live` evidence claims | Fails with `MISSING_62_EVIDENCE_CONTRACT` and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) reference |
| `test_blocked_pending_62_contract_is_failure_result_not_authorization` | The exact blocked [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) state cannot become a false positive allow-path | Synthetic downstream request with `evidence_mode=blocked_pending_62_contract`, `blocked_by_issue=62`, `follow_on_issue=70`, and `reason_code=MISSING_62_EVIDENCE_CONTRACT` | Returns failure/nonzero with the same reason code and never reports the request as authorized |
| `test_placeholder_snapshot_evidence_fails` | Placeholder gate evidence cannot satisfy [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) requirement | Synthetic request using pending/not-run/expected wording | Fails with placeholder evidence error |
| `test_metadata_only_fixture_does_not_require_live_62` | CI can validate #67 before #62 implementation without inventing a control-plane/metadata hybrid | #67 metadata-only fixture | Passes without `ACE_SHARE_ROOT` and without live [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) execution |
| `test_validator_refuses_private_reads_when_ace_share_root_is_set` | The firewall has an observable refusal boundary instead of a caller-less helper | Representative source-root-touching operation routed through the source-root boundary/refusal helper with temp `ACE_SHARE_ROOT` plus mocked guards for file open, path read helpers, existence checks, stat calls, directory iteration, globbing, and scanner entrypoints under the sentinel tree | Returns `ACE_SOURCE_ROOT_ACCESS_FORBIDDEN` before any filesystem metadata or content access under the sentinel tree; the test fails if the representative operation bypasses the helper |
| `test_seed_rule_rejects_unstable_values` | Seed grammar is deterministic | Synthetic requests with random, clock-derived, empty, or user-local seeds | Fails with seed rule error |
| `test_sort_rule_references_65_private_terms_safely` | Sort grammar does not invent row-key semantics or expose private values | Synthetic sort rule fixtures | Exact keys `strategy`, `term_refs`, `direction`, and `tie_breaker` pass; unknown keys, private-term keys, assigned private values, or raw values fail |
| `test_manifest_source_authority_matches_coordination` | Six-key source enum comes from the coordination ledger | Contract and coordination ledger | Contract source list matches coordination keys exactly |
| `test_parent_manifest_helper_is_not_67_source_authority` | Parent scanner helper cannot silently narrow #67 source enum or require broad generic filename matching | Parent validator constants and #67 contract | #67 treats the contract and coordination ledger as source authority and does not require parent helper expansion |
| `test_denied_vocabularies_sync_with_parent_scanner` | #67 does not fork the parent scanner's denied vocabulary silently | Parent scanner constants plus #67 contract | Shared denied classes match or a deliberate #67-only extension is listed with a test |
| `test_denied_token_matrix_covers_parent_and_67_extensions` | Closed command grammar is concrete at token-family level, not only category level | Contract denied-token matrix plus parent scanner denied families | Every inherited parent denied family and every #67-only manifest-source extension has a runtime fixture or explicit rationale; unknown token families fail |
| `test_classifier_vocabularies_are_closed` | The classifier's core vocabularies are contract data, not implementation guesswork | Contract executable trigger, command verb, source-root token, and operation-class lists | Exact closed enum sets are present; unknown values fail |
| `test_markdown_fenced_command_context_is_executable` | Fenced command examples are scanned as executable | Runtime-built markdown fixture | Runnable denied source-root expression fails |
| `test_markdown_unlabeled_or_text_fence_denied_expression_fails` | Non-whitelisted fences cannot hide runnable denied examples | Runtime-built unlabeled and `text` fence fixtures | Fails closed when source-root abstraction and command-like syntax both appear |
| `test_markdown_examples_heading_denied_list_item_fails` | Non-command headings cannot hide runnable denied list examples | Runtime-built list fixture under non-command heading | Fails closed when source-root abstraction and command-like syntax both appear |
| `test_markdown_inline_example_denied_expression_fails` | Inline explanatory prose cannot hide runnable denied examples | Runtime-built inline fixture using non-trigger prose | Fails closed when source-root abstraction and command-like syntax both appear |
| `test_markdown_policy_prose_context_is_non_executable` | Policy prose can name denial classes safely | Policy paragraph with no runnable source-root expression | Passes classifier |
| `test_workflow_run_context_is_executable` | Workflow run blocks are scanned | Runtime-built workflow fixture | Runnable denied source-root expression fails |
| `test_python_literal_context_is_executable_when_fed_to_classifier` | Test/code strings sent to classifier cannot hide denied commands | Runtime-assembled Python string fixture | Denied command fixture fails |
| `test_json_request_command_context_is_executable` | Request fields carrying commands are scanned | Runtime-built JSON request | Denied command fixture fails |
| `test_unknown_runnable_context_fails_closed` | Ambiguous executable-looking text cannot bypass the firewall | Synthetic unknown context | Fails closed |
| `test_recursive_traversal_class_is_denied` | Recursive source-root traversal is blocked | Runtime-assembled denied fixture | Fails validation |
| `test_broad_source_root_search_class_is_denied` | Broad list/search over the source root is blocked | Runtime-assembled denied fixture | Fails validation |
| `test_unrestricted_manifest_query_class_is_denied` | Unbounded manifest query is blocked | Runtime-assembled denied fixture | Fails validation |
| `test_raw_manifest_read_class_is_denied_for_every_manifest_source` | Raw manifest read examples are blocked for every allowed manifest source key, not only the parent scanner's pattern set | Runtime-assembled matrix of every allowed manifest source key crossed with every raw-read token family | Every pair fails validation, including the `INDEX.md` source key |
| `test_full_file_hashing_or_counting_class_is_denied` | Full-file hashing/counting of large manifests is blocked | Runtime-assembled denied fixture | Fails unless bounded sidecar contract is explicitly cited |
| `test_committed_fixtures_are_public_scan_clean` | Safe fixtures do not self-block public scan | Committed fixture directory | Parent public scanner returns no errors |
| `test_negative_fixtures_are_runtime_only` | Deny examples are not committed as public strings | Test source and fixture files | Denied examples are assembled from fragments or temp files |
| `test_classifier_source_is_public_scan_clean` | Detection source survives parent scanner without broad exemptions | Classifier, validator, tests, and contract source text | Parent scanner passes; denied command, source-root, and recursive API examples are assembled from fragments at runtime |
| `test_validator_source_avoids_unbounded_discovery` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator does not need broad self-exemptions | Validator/test source text | No unbounded repo/source-root traversal APIs are used for discovery |
| `test_public_safety_rejects_private_leaks` | Public artifacts do not expose private/source-like values | Runtime-built leak fixtures | Raw paths, private values, source-like digest assignments, personal identifiers, client identifiers, and proprietary snippets fail |
| `test_public_scan_manifest_derives_67_artifacts` | Self-scan cannot omit a public artifact by stale hand-maintained enumeration | Derived validator public-scan manifest | Static #67 artifacts plus every prefix-scoped retained plan-67 review artifact are included; unrelated review files are excluded |
| `test_review_artifact_discovery_blocks_unscanned_rerun_artifacts` | A new rN review artifact cannot escape scan coverage after another re-review wave | Temp review-results directory containing a synthetic retained plan-67 artifact plus an unnormalized sidecar | The retained artifact is auto-included in the scan manifest; the sidecar blocks unless deleted or normalized and scanned |
| `test_wave0_split_registry_records_67_plan_status` | The #67 split row cannot remain stale after implementation | #65 schema artifact and #67 plan/status inputs | #67 `plan_path`, `status_snapshot`, and `implementation_ready` match the current gate state |
| `test_review_sidecars_are_not_retained_unscanned` | Provider stderr sidecars cannot bypass public scan | Review output directory with sidecars | Sidecars are deleted or normalized and scanned before retention |
| `test_ci_invokes_67_validator_unit_tests_and_parent_scan` | CI will enforce the contract and public-scan every #67 artifact after implementation | Workflow YAML plus validator entrypoint | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator, unit tests, and the validator-mediated parent scanner invocation over the derived manifest are present |
| `test_schema_and_parent_validators_still_pass` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) does not regress existing gates | Existing validators | #65 schema validator and parent coordination validator pass |

---

## Acceptance Criteria

- [ ] A standalone issue plan exists for [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67), the latest same-round adversarial review has at least two usable provider results and no usable provider returns MAJOR, and implementation remains blocked until user approval.
- [ ] `config/ace-bounded-sampling-firewall-contract.json` defines a closed [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) contract with owner issue, schema dependency, allowed manifest sources, required sampling fields, cap maxima, request classes, denied executable classes, downstream [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence rules, and public-safety notes.
- [ ] Every operational sampling request records a target issue and target wave class imported from the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) canonical wave registry, but operational rows fail closed in this approval unit; [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) metadata-only fixtures record `fixture_scope=firewall_validator_self_check` instead and cannot authorize operational sampling.
- [ ] Downstream wave requests whose [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) `requires_manifest_snapshot_id=true` cannot use exempt request classes to bypass [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot evidence.
- [ ] Request-class mapping is explicit for `control_plane`, `ingestion_wave`, `storage_lifecycle_gate`, `manifest_freshness_gate`, `public_canary_gate`, and the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) synthetic fixture scope, including whether each row passes or fails closed.
- [ ] [#64](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/64), [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66), [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68), and [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) fail closed as sampling-request targets with explicit non-target reasons unless a later approved plan adds scopes for them.
- [ ] Output shape is closed to `metadata_only_request_record`, `route_target=metadata_only`, and `logical_target_store=metadata_ledger_store`; public, private, excluded, missing, and mismatched route/store values fail.
- [ ] The contract defines closed enums for executable triggers, command verb classes, source-root token classes, and manifest operation classes.
- [ ] Seed grammar rejects random, clock-derived, empty, user-local, or otherwise non-reviewable seeds.
- [ ] Sort grammar uses exactly `strategy`, `term_refs`, `direction`, and `tie_breaker`; #65 private schema terms appear only as `term_refs` values; unknown sort keys, raw private values, and assigned private-key forms fail.
- [ ] Manifest source authority is the six-key set in `docs/plans/ace-share-ingestion-wave-coordination.md`; parent scanner helper patterns are explicitly tested as non-authoritative for [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) source enumeration.
- [ ] [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) imports or reads [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema vocabulary and fails on drift rather than duplicating route/store/success/private-term enums; issue-required `source-extraction-coverage` remains a supporting skill doc, not a #65 bound-skill enum.
- [ ] The executable-context classifier distinguishes policy prose from runnable shell, Python, query, workflow, inline command, and JSON request contexts using closed rules.
- [ ] Unknown runnable-looking contexts fail closed when they carry a source-root abstraction and command-like syntax.
- [ ] Denied executable classes cover recursive traversal, broad source-root list/search, unrestricted manifest query, raw manifest read, full-file hashing/counting of large manifests, and unbounded materialization.
- [ ] Bounded sampling requests require target issue, manifest source, deterministic seed, sort rule, per-bucket row cap, max files touched, max bytes touched, request class, metadata-only output shape, metadata-only route/store pair, and either operational target wave class or metadata-only fixture scope.
- [ ] Sampling caps are bounded to no more than 200 rows per bucket, 25 files touched, and 1048576 bytes touched, matching the coordination-ledger bounded-read contract, unless a later approved issue changes that contract.
- [ ] Manifest-backed downstream waves fail closed with `MISSING_62_EVIDENCE_CONTRACT`, `blocked_by_issue=62`, and `follow_on_issue=70` until [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) defines an evidence schema and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) imports it; shape-only fixtures and request self-attestation cannot satisfy this gate.
- [ ] [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) does not implement [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) freshness, [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) token generation, [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) reusable public-surface scanning, [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) legal/security scanning, [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) durable storage, or [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) publication certification.
- [ ] The validator passes with `ACE_SHARE_ROOT` unset, and a representative source-root-touching operation routes through the named source-root boundary helper, returning `ACE_SOURCE_ROOT_ACCESS_FORBIDDEN` before touching private source content or metadata when `ACE_SHARE_ROOT` is set to a temp sentinel tree.
- [ ] Public artifacts do not publish raw private source paths, raw source values, source-like digest assignments, exact private inventory counts, client identifiers, personal identifiers, proprietary snippets, or publication destinations.
- [ ] Negative fixtures are generated at runtime or written to temp files outside the repo tree; committed fixtures and scanner-triggering API-token examples remain scan-clean.
- [ ] Denied token coverage is concrete at token-family level: every inherited parent denied family and every #67 manifest-source extension, including `INDEX.md`, has runtime fixture coverage for raw-read/query/count/digest cases.
- [ ] The [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator derives a bounded public-scan manifest for the complete [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) public path list, including `artifacts/ace-wave0-ledger-schema.json` and retained plan-67 review artifacts, forwards each path to the parent public scanner as an explicit `--scan-public-path` argument, and does not create the generalized scanner owned by [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68).
- [ ] The #67 row in `artifacts/ace-wave0-ledger-schema.json` records this plan path, gate-accurate `status_snapshot`, and `implementation_ready=false` until the user approval and implementation gates advance.
- [ ] Provider stderr sidecars are not retained unless normalized, explicitly listed, and scanned.
- [ ] `.github/workflows/validate.yml` runs the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator, unit tests, and validator-mediated parent public scanner over the derived full [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) public artifact manifest after implementation.
- [ ] `uv run python scripts/validate_ace_bounded_sampling_firewall.py` passes after implementation.
- [ ] `uv run python -m unittest tests.test_validate_ace_bounded_sampling_firewall` passes after implementation.
- [ ] `uv run python scripts/validate_ace_wave0_schema_contract.py` still passes after implementation.
- [ ] `uv run python scripts/validate_ace_epic_wave_coordination.py` still passes after implementation.
- [ ] `uv run skills/validate_skill.py` still passes after implementation.
- [ ] If implementation reveals a reusable method gap, schema-bound or issue-required skill docs are updated or a follow-on issue is filed before closeout.
- [ ] If `scripts/legal/legal-sanity-scan.sh` is still unavailable at closeout, full closeout remains blocked; the issue comment records `NO_LEGAL_SCAN_SCRIPT` and points to [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).

---

## Focused Self-Scan Before Formal Review

- [ ] Closed grammar fields are enumerated, including [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence fields.
- [ ] Executable-context rules are parseable and closed.
- [ ] Denied executable classes are complete without embedding runnable denied examples in committed public files.
- [ ] Dependencies stay narrow: [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) required, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) required for downstream sampling evidence, [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)/[#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)/[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) not required.
- [ ] CI and derived public-scan manifest include every [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) artifact and no broad whole-directory exemption.
- [ ] Public artifacts carry no private-source assignment, source-like digest assignment, raw local path, personal identifier, or concrete client/project identifier.

---

## Plan Review Gate Rule

Plan review will be considered passable only when the same review round has at least two usable provider results and no usable provider returns MAJOR. A provider that fails before returning findings may be recorded as `UNAVAILABLE` with the exact reason and does not count toward the usable-provider total. With Gemini currently returning ineligible-tier failures, the effective gate is both Claude and Codex returning no-MAJOR in the same round. If Gemini becomes usable again, its result is no longer advisory: any usable Gemini MAJOR blocks advancement under the same "no usable MAJOR" rule, while a Gemini no-MAJOR can satisfy the usable-provider floor alongside any other no-MAJOR provider. If fewer than two providers are usable, or if any usable provider returns MAJOR, [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) remains `draft` and must not move to `status:plan-review`.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Found self-scanner contradiction, under-specified classifier rule, manifest-source authority drift, stale Files-to-Change wording, CI command mismatch, and registry scan reflexivity. Patch attempt recorded; re-review required. |
| Codex r1 | MAJOR | Found #62 gate bypass by request-class self-selection, missing sort-key contract, weak seed/sort tests, legal-scan closeout downgrade, missing review-sidecar disposition, and stale plan-existence wording. Patch attempt recorded; re-review required. |
| Gemini r1 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r2 | UNAVAILABLE | CLI invocation failed before returning a usable review; no signal. |
| Codex r2 | MAJOR | Found missing request-class mapping, missing closed classifier vocabularies, no positive #62 evidence schema/fixture, and open-ended legal-scan deferral. Patch attempt recorded; re-review required. |
| Gemini r2 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r3 | MAJOR | Found nonexistent #67 wave-class mapping, retained legal-scan deferral, parent-helper blast-radius risk, incomplete self-block mitigation, missing downstream shape fixture, and stale review artifact inventory. Patch attempt recorded; re-review required. |
| Codex r3 | MAJOR | Found nonexistent #67 wave-class mapping, synthetic #62 evidence bypass, unclosed sort grammar, and stale retained-artifact inventory. Patch attempt recorded; re-review required. |
| Gemini r3 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r4 | MAJOR | Found #65 bound-skill drift, guessed #62 interface, environment-coupled #62 absence test, uncited cap authority, status-only #62 semantics, incomplete fixture inventory, and unexplained non-target issues. Patch attempt recorded; re-review required. |
| Codex r4 | MAJOR | Found malformed approval-marker bypass risk, self-attested #62 evidence gap, and incomplete downstream shape fixture inventory. Patch attempt recorded; re-review required. |
| Gemini r4 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r5 | MAJOR | Found unresolved #62 evidence-artifact schema ownership, missing private-read-refusal test, parent-test coupling, and possible denied-vocabulary drift. Patch attempt recorded; re-review required. |
| Codex r5 | MAJOR | Found missing schema split registry public-scan coverage and missing TDD assertion for the #67 split-registry plan/status update. Patch attempt recorded; re-review required. |
| Gemini r5 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r6 | MAJOR | Found shape-only fixture contract contradiction, unspecified fixture target fields, under-specified inline/fenced classifier triggers, blocked-state discriminator gap, private-read test observability gap, and self-attested patch wording. Patch attempt recorded; re-review required. |
| Codex r6 | MAJOR | Found live issue skill-binding mismatch, snapshot-evidence request-class ambiguity, and missing `config/` directory creation. Patch attempt recorded; re-review required. |
| Gemini r6 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r7 | MAJOR | Found vacuous snapshot-evidence discriminator, duplicated #62 snapshot-gate source, missing review quorum rule, under-specified CI public-scan wiring, and skill-validation command inconsistency. Patch attempt recorded; re-review required. |
| Codex r7 | MAJOR | Found Markdown non-whitelisted-context bypass tests missing, incomplete private source-root access instrumentation, and metadata/control-plane fixture ambiguity. Patch attempt recorded; re-review required. |
| Gemini r7 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r8 | MAJOR | Found overstated operational allow-path, missing operational accept/defer declaration, hand-maintained review-artifact scan drift, vacuous private-read test, self-referential quorum wording, and skill-validation command mismatch. Patch attempt recorded; re-review required. |
| Codex r8 | MAJOR | Found under-specified metadata-only output shape/route/store grammar and missing fail-closed test for `blocked_pending_62_contract`. Patch attempt recorded; re-review required. |
| Gemini r8 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r9 | MINOR | Found stale overall review summary wording, under-listed fixture fields, residual source-root helper invocation ambiguity, skill/method-binding prose mismatch, and Gemini-recovery gate ambiguity. Patch attempt recorded; re-review required. |
| Codex r9 | MAJOR | Found request-class pass/fail contradiction, missing per-source raw-read denial coverage for `INDEX.md`, and category-only denied-token grammar. Patch attempt recorded; re-review required. |
| Gemini r9 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |

**Overall result:** MAJOR - Codex r9 blockers remain patched for the next review cycle; draft only; not ready for `status:plan-review`.

---

## Risks and Open Questions

- **Risk:** The executable-context classifier could be too broad and block policy prose. The plan will mitigate this with closed context rules and tests for prose naming denial classes without runnable source-root expressions.
- **Risk:** The classifier could be too narrow and allow runnable unbounded sampling examples. The plan will mitigate this with runtime-generated negative fixtures for markdown, workflow, Python, and JSON request contexts.
- **Risk:** [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) could accidentally reimplement [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62), [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68), or [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69). The plan will keep those responsibilities as evidence requirements or explicit non-goals.
- **Risk:** Committed negative fixtures could self-block public scans. The plan will require runtime construction or temp-file fixtures outside the repo tree.
- **Open:** Formal provider review may require another split if the executable-context classifier and sampling grammar are still too much for one approval unit.

---

## Complexity

**T3** - security-sensitive control-plane validator with cross-wave dependencies, executable-context classification, CI wiring, and public/private safety constraints, but no private content ingestion and no durable output writes.
