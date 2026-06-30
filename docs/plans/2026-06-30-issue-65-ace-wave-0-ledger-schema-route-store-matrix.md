# Plan for #65: ACE Wave 0 Ledger Schema and Route-Store Matrix

> **Status:** draft
> **Complexity:** T2
> **Date:** 2026-06-30
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** PENDING final no-MAJOR round

---

## Resource Intelligence Summary

### Existing repo code/docs

- `docs/plans/README.md` will remain the portfolio gate surface. It already states that [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) owns the route, ledger, and sampling interface, and that [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) each require standalone plans before implementation.
- `docs/plans/ace-share-ingestion-wave-coordination.md` will remain the parseable portfolio registry for #51-#63 and now carries a separate wave-0 split registry for [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- `scripts/validate_ace_epic_wave_coordination.py` already validates the parent coordination artifact and includes public-surface fallback checks. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will not replace that parent validator; it will add the narrower wave-0 schema validator that downstream split issues will consume.
- `docs/01-document-taxonomy.md` supplies extraction-level vocabulary and content-first routing discipline.
- `docs/07-data-governance.md` and `docs/19-trust-boundary-and-private-mode.md` require raw-source off-repo handling, public/private routing, provenance, and fail-closed publication boundaries.
- Bound skills `format-coverage-ledger`, `public-private-routing`, `content-triage-and-exclusion`, `page-shape-contract`, and `adversarial-verify-loop` already define the method vocabulary that this schema will make machine-checkable.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic. It authorizes coordination and planning only; it does not approve child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) is the wave-0 umbrella. It delegates implementation-sized slices to [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will define the schema and route-store vocabulary consumed by [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) will own physical private-sidecar storage, lifecycle states, retrieval, and success-metric closeout. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will define only logical target-store classes.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) will own manifest freshness and snapshot evidence. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will record the field and registry requirement, not perform freshness checks.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will own public-output canaries, maintained private deny-lists, publication certification, shared public-output config, and source-hash policy sweep.

### Source inventory

- This plan will not read private ACE content or require `ACE_SHARE_ROOT`.
- The schema implementation will validate repo-tracked schema fixtures and public planning artifacts only.
- Public planning surfaces may retain the fixed metadata-evidence abstraction already used by [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51), but [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will not add new source inventory rows or exact private counts.

### Gaps identified

- No repo-local wave-0 ledger schema artifact exists yet.
- No focused validator exists for the route enum, route-to-logical-store matrix, verification-state enum, and split registry readiness rules.
- The current parent coordination validator knows only the canonical #51-#63 wave ledger; it does not validate a reusable schema artifact that [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) can import.
- Route target, target store, verification-state, wave-class, method-binding, success-field, and implementation-readiness semantics need one machine-readable home before downstream split plans add token, sampling, public-scan, or legal-scan behavior.

### Evidence

**Issue status** (verified 2026-06-30):

```text
#65 OPEN ACE wave 0 split: ledger schema and route-store matrix labels=strengthening,lane:claude,priority:high
```

**File existence** (verified 2026-06-30):

```text
EXISTS docs/plans/README.md
EXISTS docs/plans/ace-share-ingestion-wave-coordination.md
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS tests/test_validate_ace_epic_wave_coordination.py
EXISTS skills/format-coverage-ledger/SKILL.md
EXISTS skills/public-private-routing/SKILL.md
EXISTS skills/content-triage-and-exclusion/SKILL.md
EXISTS skills/page-shape-contract/SKILL.md
EXISTS skills/adversarial-verify-loop/SKILL.md
MISSING artifacts/ace-wave0-ledger-schema.json
MISSING scripts/validate_ace_wave0_control_plane.py
MISSING tests/test_validate_ace_wave0_control_plane_schema.py
```

**Reproduction proofs**:
N/A - governance/planning issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-30-issue-65-ace-wave-0-ledger-schema-route-store-matrix.md` |
| Schema contract | `artifacts/ace-wave0-ledger-schema.json` |
| Focused validator | `scripts/validate_ace_wave0_control_plane.py` |
| Unit tests | `tests/test_validate_ace_wave0_control_plane_schema.py` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Workflow | `.github/workflows/validate.yml` |
| Bound skill docs | `skills/format-coverage-ledger/SKILL.md`, `skills/public-private-routing/SKILL.md`, `skills/content-triage-and-exclusion/SKILL.md`, `skills/page-shape-contract/SKILL.md`, `skills/adversarial-verify-loop/SKILL.md` |
| Review artifact - Claude | `scripts/review/results/2026-06-30-plan-65-claude.md` |
| Review artifact - Codex | `scripts/review/results/2026-06-30-plan-65-codex.md` |
| Review artifact - Gemini | `scripts/review/results/2026-06-30-plan-65-gemini.md` |

---

## Deliverable

After approval and implementation, [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will provide a machine-readable ACE wave-0 ledger schema plus a focused validator that proves the closed route/store/verification/wave registry contract without ingesting content or implementing the downstream token, sampling, public-scan, legal-scan, storage, or publication gates.

---

## Pseudocode

```text
load artifacts/ace-wave0-ledger-schema.json with Python stdlib json
validate schema metadata:
  schema_id, schema_version, owner_issue, status, and public_safety_notes are present
validate closed route targets:
  public_llm_wiki
  private_sidecar
  metadata_only
  excluded_no_ingest
validate logical target-store matrix:
  public route maps to logical public store
  private route maps to logical private sidecar
  metadata-only route maps to logical metadata ledger
  excluded route maps to logical no-store
  no physical private path, repo path, host path, or wiki path is allowed in #65
validate verification-state enum:
  not_verified
  validator_passed
  independent_review_passed
  rejected
validate required ledger field groups:
  source identity names are declared as private-only schema terms, never values
  public token field is declared as a downstream contract owned by #66/#63
  route, store, extraction, sensitivity, content class, verification, method binding,
  success metric, validator path, and implementation-readiness fields are required
validate split registry:
  #65 is schema owner
  #66 depends on #65 for token fixture fields
  #67 depends on #65 for wave class and snapshot fields
  #68 depends on #65/#66 for safe public-surface contexts
  #69 depends on #68 for config self-scan boundaries
  every split row is implementation_ready=false unless its own issue has approval evidence
validate canonical wave registry compatibility:
  #51/#61/#62/#63 remain non-ingestion control/gate rows
  #52-#60 remain ingestion wave rows requiring manifest snapshot evidence
  success field vocabulary matches docs/plans/ace-share-ingestion-wave-coordination.md
validate bound skill references:
  schema artifact records method issues #1 and #12
  schema artifact records the bound skill group names
  changed skill docs link or name the schema contract only if implementation discovers a reusable method gap
run parent coordination validator as a compatibility check
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `artifacts/ace-wave0-ledger-schema.json` | Canonical machine-readable schema, route enum, route-store matrix, verification-state enum, split registry, method bindings, and public-safety notes |
| Create | `scripts/validate_ace_wave0_control_plane.py` | Focused validator for the schema artifact and its compatibility with the coordination ledger |
| Create | `tests/test_validate_ace_wave0_control_plane_schema.py` | TDD coverage for schema loading, closed enums, route-store matrix, split dependencies, implementation-readiness fail-closed behavior, and no physical private paths |
| Modify | `.github/workflows/validate.yml` | Run the new validator and unit test after approved implementation |
| Modify | `docs/plans/README.md` | Mark [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) as planned/reviewed during status transitions without implying approval |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Point the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) split row at the plan/schema after review and later record implementation evidence |
| Conditional modify | `skills/format-coverage-ledger/SKILL.md` | Link the schema contract if implementation exposes a reusable ledger-field guidance gap |
| Conditional modify | `skills/public-private-routing/SKILL.md` | Link the route-store matrix if implementation exposes a reusable route-enum guidance gap |
| Conditional modify | `skills/content-triage-and-exclusion/SKILL.md` | Link fail-closed sensitivity/content-class routing if implementation exposes a reusable triage gap |
| Conditional modify | `skills/page-shape-contract/SKILL.md` | Link verification-state and provenance shape guidance if implementation exposes a reusable page-shape gap |
| Conditional modify | `skills/adversarial-verify-loop/SKILL.md` | Link method-gap disposition guidance if implementation exposes a reusable review-loop gap |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_schema_file_is_json_and_versioned` | Schema contract is machine-readable and owned by [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) | `artifacts/ace-wave0-ledger-schema.json` | JSON loads with schema id, version, owner issue, and public-safety notes |
| `test_route_enum_is_closed` | Route targets cannot drift | Schema route target list | Exactly four route targets are accepted |
| `test_route_to_store_matrix_is_logical_only` | #65 does not invent physical private storage | Schema route/store matrix | Each route maps to one logical store; physical paths, repo paths, or host paths are rejected |
| `test_verification_state_enum_is_closed` | Trust state vocabulary is precise | Schema verification-state list | Exactly four verification states are accepted |
| `test_required_field_groups_are_present` | Ledger has the fields downstream split issues need | Schema required field groups | Identity, route, content, method, validation, success, readiness, and downstream contract field groups are present |
| `test_private_field_names_are_schema_terms_only` | Public schema does not publish private values | Schema field declarations and negative fixtures | Private provenance terms appear only as field names/classes; assigned values or maps fail |
| `test_public_token_field_is_delegated` | #65 does not implement token generation | Schema downstream contract section | Public-token grammar and generation are marked as [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)/[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63)-owned |
| `test_split_registry_dependencies_are_parseable` | Split issue order is executable | Schema split registry | #66/#67 depend on #65, #68 depends on #65/#66, and #69 depends on #68 |
| `test_split_registry_fails_open_readiness` | No split issue can become ready without approval evidence | Schema or coordination fixture with ready=true and no approval marker | Validator fails |
| `test_wave_registry_compatibility_matches_coordination` | #65 schema stays compatible with parent coordination | Schema plus `docs/plans/ace-share-ingestion-wave-coordination.md` | Wave classes and success fields match the canonical registry |
| `test_parent_validator_still_passes` | New validator does not regress parent validator | Existing parent validator command | Parent validator passes |
| `test_ci_invokes_wave0_schema_validator` | CI wiring exists after implementation | `.github/workflows/validate.yml` | Workflow invokes new validator and unit test |

---

## Acceptance Criteria

- [ ] A standalone issue plan exists for [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65), passes adversarial plan review, and remains blocked from implementation until user approval.
- [ ] `artifacts/ace-wave0-ledger-schema.json` defines schema metadata, required ledger field groups, closed route targets, closed logical target-store values, closed verification states, split issue dependencies, method issues, skill groups, and success-field vocabulary.
- [ ] Route targets are closed to `public_llm_wiki`, `private_sidecar`, `metadata_only`, and `excluded_no_ingest`.
- [ ] The route-store matrix uses logical store names only and rejects physical private-sidecar locations because [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) owns physical storage.
- [ ] The verification-state enum is closed to `not_verified`, `validator_passed`, `independent_review_passed`, and `rejected`.
- [ ] The schema records downstream ownership boundaries: [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) for token fixture generation, [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) for sampling firewall behavior, [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) for generic public-surface self-scan, [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) for repo-local legal/security scan, [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) for durable private storage, and [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) for publication certification.
- [ ] Split registry validation keeps [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) `implementation_ready=false` unless each issue has its own approval evidence.
- [ ] The validator passes with `ACE_SHARE_ROOT` unset and does not read private source content.
- [ ] Public surfaces do not publish private source content, raw host paths, exact private inventory counts, assigned private provenance values, client identifiers, or personal identifiers.
- [ ] If implementation reveals a reusable method gap, the bound skill docs are updated or a follow-on issue is filed before closeout.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_control_plane.py` passes after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_wave0_control_plane_schema` passes after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py` and `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` still pass after implementation.

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

- **Risk:** The schema could grow back into the old [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) monolith. The implementation will reject token generation, sampling firewall rules, public-surface scanner behavior, legal/security scanning, physical storage, and publication certification as out of scope for [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65).
- **Risk:** The schema could expose private provenance values while trying to document private field names. The implementation will treat private provenance names as schema terms only and will test that assigned values or maps fail.
- **Risk:** Parent and split registries could drift. The implementation will compare the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema against `docs/plans/ace-share-ingestion-wave-coordination.md`.
- **Open:** Gemini review remains unavailable in current noninteractive runs. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) cannot move to `status:plan-review` until fresh review evidence is available under the workspace quorum policy.

---

## Complexity

**T2** - focused schema, validator, tests, and CI wiring across a few repo-local files, with security-sensitive public/private boundaries but no private source ingestion and no publication behavior.
