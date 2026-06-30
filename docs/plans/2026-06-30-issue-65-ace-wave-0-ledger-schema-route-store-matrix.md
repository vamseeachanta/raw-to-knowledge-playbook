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
- `scripts/validate_ace_epic_wave_coordination.py` already validates the parent coordination artifact and includes opt-in public-surface fallback checks. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will not replace that parent validator and will not reuse [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51)'s reserved `scripts/validate_ace_wave0_control_plane.py` executable binding; it will add a narrower schema-contract validator at `scripts/validate_ace_wave0_schema_contract.py`.
- `docs/01-document-taxonomy.md` supplies extraction-level vocabulary and content-first routing discipline.
- `docs/07-data-governance.md` and `docs/19-trust-boundary-and-private-mode.md` require raw-source off-repo handling, public/private routing, provenance, and fail-closed publication boundaries.
- Bound skills `format-coverage-ledger`, `public-private-routing`, `content-triage-and-exclusion`, `page-shape-contract`, and `adversarial-verify-loop` already define the method vocabulary that this schema will make machine-checkable.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic. It authorizes coordination and planning only; it does not approve child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) is the wave-0 umbrella. It delegates implementation-sized slices to [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will define the schema and route-store vocabulary consumed by [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) will own physical private-sidecar storage, lifecycle states, retrieval, and success-metric closeout. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will define only logical target-store classes.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) will own manifest freshness and snapshot evidence. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will record the field and registry requirement, not perform freshness checks.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will own public-output canaries, maintained private deny-lists, publication certification, shared public-output config, and source-hash policy sweep. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will add only the schema-local public-surface checks needed to keep its own public artifacts safe until [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)/[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) generalize the scanner.

### Source inventory

- This plan will not read private ACE content or require `ACE_SHARE_ROOT`.
- The schema implementation will validate repo-tracked schema fixtures and public planning artifacts only.
- Public planning surfaces may retain the fixed metadata-evidence abstraction already used by [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51), but [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will not add new source inventory rows or exact private counts.

### Gaps identified

- No repo-local wave-0 ledger schema artifact exists yet.
- No focused validator exists for the route enum, route-to-logical-store matrix, control-plane verification-state enum, and split registry readiness rules.
- The current parent coordination validator knows only the canonical #51-#63 wave ledger; it does not validate a reusable schema artifact that [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) can import.
- Route target, target store, verification-state, wave-class, method-binding, success-field, and implementation-readiness semantics need one machine-readable home before downstream split plans add token, sampling, public-scan, or legal-scan behavior.
- The [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) umbrella row already reserves `scripts/validate_ace_wave0_control_plane.py`; using that path for [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) would let a narrow schema validator masquerade as the broader [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) control-plane validator.
- The existing parent public scanner is opt-in and its current raw-digest patterns do not fully specify JSON quoted-key cases for schema artifacts. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will add schema-local JSON assignment coverage and will file or update the appropriate public-scan follow-on if implementation finds a reusable scanner gap outside [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)'s artifact set.

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
MISSING scripts/validate_ace_wave0_schema_contract.py
MISSING tests/test_validate_ace_wave0_schema_contract.py
```

**Reproduction proofs**:
N/A - governance/planning issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-30-issue-65-ace-wave-0-ledger-schema-route-store-matrix.md` |
| Schema contract | `artifacts/ace-wave0-ledger-schema.json` |
| Focused validator | `scripts/validate_ace_wave0_schema_contract.py` |
| Unit tests | `tests/test_validate_ace_wave0_schema_contract.py` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Workflow | `.github/workflows/validate.yml` |
| Bound skill docs | `skills/format-coverage-ledger/SKILL.md`, `skills/public-private-routing/SKILL.md`, `skills/content-triage-and-exclusion/SKILL.md`, `skills/page-shape-contract/SKILL.md`, `skills/adversarial-verify-loop/SKILL.md` |
| Review artifact - Claude r1 | `scripts/review/results/2026-06-30-plan-65-claude-r1.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-06-30-plan-65-codex-r1.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-06-30-plan-65-gemini-r1.md` |

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
  public_llm_wiki maps only to public_llm_wiki_store
  private_sidecar maps only to private_sidecar_store
  metadata_only maps only to metadata_ledger_store
  excluded_no_ingest maps only to excluded_no_store
  no physical private path, repo path, host path, wiki path, or relative private path is allowed in #65
validate control_plane_verification_state enum:
  not_verified
  validator_passed
  independent_review_passed
  verification_rejected
  all values are disjoint from #61 lifecycle states and page-shape parse_status values
  disjointness is checked by exact set membership, never substring matching
validate required ledger field groups:
  source identity names are declared as private-only schema terms, never values
  private source field terms are represented as array values under neutral keys, never as JSON object keys
  JSON object keys may not equal private source field names or source-like raw digest field names
  public token field is declared as a downstream contract owned by #66/#63
  route, store, extraction, sensitivity, content class, verification, method binding,
  success metric, validator path, and implementation-readiness fields are required
validate split registry:
  #65 is schema owner
  #66 depends on #65 for token fixture fields
  #67 depends on #65 for wave class and snapshot fields
  #68 depends on #65/#66 for safe public-surface contexts
  #69 depends on #68 for config self-scan boundaries
  every split row is implementation_ready=false unless its own issue has status:plan-approved
  and .planning/plan-approved/<issue>.md passes the parent validate_approval_marker function
  from scripts/validate_ace_epic_wave_coordination.py without re-deriving a weaker subset:
    required fields Approved by, Approval date, Issue, Plan path, Reviewed commit, Review artifacts
    non-empty values except the multiline Review artifacts field
    matching issue URL, exact plan path, 40-character reviewed commit,
    non-empty review artifact paths, and verdict-bearing review artifacts
  stock CI validates only repo-local snapshot/marker evidence; live GitHub labels are pre-label evidence
validate canonical wave registry compatibility:
  #51/#61/#62/#63 remain non-ingestion control/gate rows
  #52-#60 remain ingestion wave rows requiring manifest snapshot evidence
  success field vocabulary matches docs/plans/ace-share-ingestion-wave-coordination.md
validate bound skill references:
  schema artifact records method issues #1 and #12
  schema artifact records the bound skill group names
  changed skill docs link or name the schema contract only if implementation discovers a reusable method gap
validate #65 public-surface scan set:
  invoke the existing parent validate_public_artifact_paths scanner over this explicit #65 path list:
    this plan, docs/plans/README.md, docs/plans/ace-share-ingestion-wave-coordination.md,
    artifacts/ace-wave0-ledger-schema.json, scripts/validate_ace_wave0_schema_contract.py,
    tests/test_validate_ace_wave0_schema_contract.py, .github/workflows/validate.yml,
    every changed bound skill doc, and every retained scripts/review/results/*plan-65*.md artifact
  build no generalized reusable self-scan engine in #65; reusable scan-engine work routes to #68
  do not use os.walk or Path.rglob in the new validator/test sources; use an explicit path list
  or bounded non-recursive glob patterns so committed source files pass their own scan
  additionally reject JSON-style quoted assignments for private source fields and source-like raw digests
  construct negative fixtures at test runtime from token fragments or temp files, not as committed raw examples
run parent coordination validator as a compatibility check
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `artifacts/ace-wave0-ledger-schema.json` | Canonical machine-readable schema, route enum, route-store matrix, verification-state enum, split registry, method bindings, scanner-safe private field term representation, and public-safety notes |
| Create | `scripts/validate_ace_wave0_schema_contract.py` | Focused validator for the schema artifact, schema-local public-surface checks, parent approval-marker semantics, and compatibility with the coordination ledger |
| Create | `tests/test_validate_ace_wave0_schema_contract.py` | TDD coverage for schema loading, closed enums, route-store matrix, split dependencies, implementation-readiness fail-closed behavior, public-scan coverage, JSON quoted-key raw digest rejection, and no physical/private paths |
| Modify | `.github/workflows/validate.yml` | Run the new validator, unit test, and explicit [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) public-scan paths after approved implementation |
| Modify | `docs/plans/README.md` | Mark [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) as planned/reviewed during status transitions and clarify [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) conceptual route ownership versus [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) machine encoding without implying approval |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Point the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) split row at the plan/schema after review and later record implementation evidence |
| Conditional scan-clean modify or follow-on | `skills/format-coverage-ledger/SKILL.md` | Link the schema contract only if implementation exposes a reusable ledger-field guidance gap and the changed skill doc passes the #65 public scan; otherwise file a follow-on issue |
| Conditional scan-clean modify or follow-on | `skills/public-private-routing/SKILL.md` | Link the route-store matrix only if implementation exposes a reusable route-enum guidance gap and the changed skill doc passes the #65 public scan; otherwise file a follow-on issue |
| Conditional follow-on preferred | `skills/content-triage-and-exclusion/SKILL.md` | Do not directly edit this skill in #65 if pre-existing policy prose blocks the public scan; file a follow-on or wait for [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)/[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) scanner allow-context support |
| Conditional scan-clean modify or follow-on | `skills/page-shape-contract/SKILL.md` | Link verification-state and provenance shape guidance only if implementation exposes a reusable page-shape gap and the changed skill doc passes the #65 public scan; otherwise file a follow-on issue |
| Conditional scan-clean modify or follow-on | `skills/adversarial-verify-loop/SKILL.md` | Link method-gap disposition guidance only if implementation exposes a reusable review-loop gap and the changed skill doc passes the #65 public scan; otherwise file a follow-on issue |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_schema_file_is_json_and_versioned` | Schema contract is machine-readable and owned by [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) | `artifacts/ace-wave0-ledger-schema.json` | JSON loads with schema id, version, owner issue, and public-safety notes |
| `test_route_enum_is_closed` | Route targets cannot drift | Schema route target list | Exactly four route targets are accepted |
| `test_logical_store_enum_is_closed` | Store targets cannot drift or imply paths | Schema logical store list | Exactly `public_llm_wiki_store`, `private_sidecar_store`, `metadata_ledger_store`, and `excluded_no_store` are accepted |
| `test_route_to_store_matrix_is_logical_only` | #65 does not invent physical private storage or public/wiki paths | Schema route/store matrix plus negative fixtures | Each route maps to one logical store; physical paths, repo paths, host paths, wiki paths, and relative private paths are rejected |
| `test_control_plane_verification_state_enum_is_closed` | Trust evidence vocabulary is precise and separate from page/lifecycle vocab | Schema verification-state list plus #61 lifecycle and page-shape parse_status samples | Exactly `not_verified`, `validator_passed`, `independent_review_passed`, and `verification_rejected` are accepted; lifecycle/parse_status values are rejected by exact set membership, not substring matching |
| `test_required_field_groups_are_present` | Ledger has the fields downstream split issues need | Schema required field groups | Identity, route, content, method, validation, success, readiness, and downstream contract field groups are present |
| `test_private_source_terms_are_values_not_keys` | Scanner-safe schema representation cannot turn private field terms into JSON assignments | Schema JSON object keys and private source term arrays | Private source field terms may appear only as neutral-key array values, never as JSON object keys |
| `test_private_field_names_are_schema_terms_only` | Public schema does not publish private values | Schema field declarations plus runtime-generated negative fixtures | Private provenance terms appear only as field names/classes; assigned values or maps fail without committing raw deny examples |
| `test_json_source_hash_assignments_are_rejected` | JSON artifacts cannot bypass raw-digest denial | Runtime-generated JSON fixtures with quoted source-like hash keys | Quoted-key raw digest assignments fail validation |
| `test_public_token_field_is_delegated` | #65 does not implement token generation | Schema downstream contract section | Public-token grammar and generation are marked as [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)/[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63)-owned |
| `test_split_registry_dependencies_are_parseable` | Split issue order is executable | Schema split registry | #66/#67 depend on #65, #68 depends on #65/#66, and #69 depends on #68 |
| `test_split_registry_requires_approval_marker_contract` | No split issue can become ready without the repo approval contract | Schema or coordination fixture with ready=true, missing `status:plan-approved` snapshot, or marker cases invalid under parent `validate_approval_marker` semantics | Validator imports/calls the parent marker validator and fails invalid markers, including missing/empty `Approved by:` or `Approval date:` |
| `test_wave_registry_compatibility_matches_coordination` | #65 schema stays compatible with parent coordination | Schema plus `docs/plans/ace-share-ingestion-wave-coordination.md` | Wave classes and success fields match the canonical registry |
| `test_public_scan_paths_cover_65_artifacts` | #65 safety scan cannot omit a public output or become a reusable #68 scanner | Validator path list plus artifact map | Plan, README, coordination, schema, validator, tests, workflow, changed skills, and retained plan-65 review artifacts are passed to the existing parent scanner when present; no generalized self-scan engine is created |
| `test_negative_fixtures_are_not_committed_as_raw_examples` | Public scanner fixtures do not self-block committed files | Test source text and runtime fixture builder | Deny strings are assembled at runtime or written to temp files; committed files do not contain raw private-looking assignments |
| `test_validator_source_avoids_denied_recursive_traversal` | New validator/test sources do not need parent filename-only self-exemptions | Validator and unit test source text | New source files avoid `os.walk` and `Path.rglob`, or fail until an explicit tested self-exemption exists |
| `test_changed_skill_docs_are_scan_clean_or_follow_on` | Conditional skill edits cannot introduce pre-existing scanner blockers into #65 | Changed bound skill doc list | Every changed skill doc passes the #65 public scan, or the method gap is routed to a follow-on issue |
| `test_parent_validator_still_passes` | New validator does not regress parent validator | Existing parent validator command | Parent validator passes |
| `test_ci_invokes_wave0_schema_validator_and_scan` | CI wiring exists after implementation | `.github/workflows/validate.yml` | Workflow invokes new validator, unit test, and explicit #65 public-scan paths |

---

## Acceptance Criteria

- [ ] A standalone issue plan exists for [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65), passes adversarial plan review, and remains blocked from implementation until user approval.
- [ ] `artifacts/ace-wave0-ledger-schema.json` defines schema metadata, required ledger field groups, closed route targets, closed logical target-store values, closed control-plane verification states, split issue dependencies, method issues, skill groups, scanner-safe private field term representation, and success-field vocabulary.
- [ ] The schema records route-target ownership metadata that says [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) owns the umbrella route contract and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) only machine-encodes it for downstream split issues.
- [ ] Route targets are closed to `public_llm_wiki`, `private_sidecar`, `metadata_only`, and `excluded_no_ingest`.
- [ ] Logical store names are closed to `public_llm_wiki_store`, `private_sidecar_store`, `metadata_ledger_store`, and `excluded_no_store`.
- [ ] The route-store matrix uses logical store names only and rejects physical private-sidecar locations, public/wiki paths, host paths, repo paths, and relative private paths because [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) owns physical storage and publication destinations.
- [ ] The `control_plane_verification_state` enum is closed to `not_verified`, `validator_passed`, `independent_review_passed`, and `verification_rejected`, and its values are disjoint from [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) lifecycle states and `page-shape-contract` `parse_status` values.
- [ ] Private source field terms and source-like raw digest terms are represented as neutral-key array values in the schema JSON, never as JSON object keys or assigned values.
- [ ] The schema records downstream ownership boundaries: [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) for token fixture generation, [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) for sampling firewall behavior, [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) for generic public-surface self-scan, [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) for repo-local legal/security scan, [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) for durable private storage, and [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) for publication certification.
- [ ] Split registry validation keeps [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) `implementation_ready=false` unless each issue has a recorded `status:plan-approved` snapshot and `.planning/plan-approved/<issue>.md` passes `scripts/validate_ace_epic_wave_coordination.py::validate_approval_marker` by import/call, including required marker fields, non-empty marker values, matching issue URL, exact plan path, 40-character reviewed commit, non-empty review artifact paths, and verdict-bearing artifact checks.
- [ ] The validator passes with `ACE_SHARE_ROOT` unset and does not read private source content.
- [ ] Public surfaces do not publish private source content, raw host paths, exact private inventory counts, assigned private provenance values, source-like raw digests, client identifiers, or personal identifiers.
- [ ] The schema validator invokes the existing parent public scanner over the complete [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) public-surface path list: this plan, plan README, coordination ledger, schema JSON, validator, unit tests, workflow, changed bound skill docs, and retained `scripts/review/results/*plan-65*.md` artifacts when they exist; it does not build a generalized scanner owned by [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68).
- [ ] JSON quoted-key assignments for private source fields and source-like raw digests fail validation; negative fixtures are generated at runtime or kept in temp files so committed public artifacts do not self-block the scanner.
- [ ] New validator/test source files avoid `os.walk` and `Path.rglob` unless an explicit tested self-exemption is added; the default path discovery is an explicit list plus bounded non-recursive glob patterns.
- [ ] Conditional bound-skill updates are applied only if the changed skill doc passes the #65 public scan; otherwise [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) files or links a follow-on issue instead of carrying a known self-blocker.
- [ ] If implementation reveals a reusable method gap, the bound skill docs are updated or a follow-on issue is filed before closeout.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_schema_contract.py` passes after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_wave0_schema_contract` passes after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py` and `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` still pass after implementation.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Parallel subagent - workflow/schema | MAJOR | r1 found the [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) validator-path collision, loose approval-evidence wording, unsourced enum boundaries, and incomplete CI/public-scan coverage. Current draft patches these issues; formal provider review still required. |
| Parallel subagent - public/private | MAJOR | r1 found incomplete #65 public-surface scan coverage, JSON raw-digest scanner gaps, self-blocking negative-fixture risk, and under-specified path leakage tests. Current draft patches these issues; formal provider review still required. |
| Claude r1 | MAJOR | Found `rejected` enum collision, route ownership drift, and self-scan feasibility gaps. Current draft patches these issues; re-review required. |
| Codex r1 | MAJOR | Found `rejected` enum collision, JSON schema key self-blocker, underspecified approval-marker semantics, conditional skill scan blocker, and route ownership ambiguity. Current draft patches these issues; re-review required. |
| Gemini r1 | UNAVAILABLE | Installed client returned unsupported-tier authentication error; no review performed. |
| Claude r2 | MINOR | Confirmed r1 MAJORs patched; requested exact parent approval-marker call semantics, clearer #65/#68 self-scan boundary, and exact set-membership wording for enum disjointness. Current draft patches these issues; re-review required because the plan changed after r2. |
| Codex r2 | MINOR | Found prompt reviewed-head metadata typo: the r2 prompt named an unresolvable SHA while the actual local head was `ee0ef2221b928f78de50ed150aac2a87b1e6988a`. Next review must use the actual commit. |
| Gemini r2 | UNAVAILABLE | Installed client returned unsupported-tier authentication error; no review performed. |

**Overall result:** NEEDS RE-REVIEW - draft only; formal r1 review returned MAJOR from both active providers and r2 returned MINOR after the r1 patch. Current draft patches the r2 findings and must receive a fresh no-MAJOR provider round on the correct committed head before `status:plan-review`.

---

## Risks and Open Questions

- **Risk:** The schema could grow back into the old [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) monolith. The implementation will reject token generation, sampling firewall rules, public-surface scanner behavior, legal/security scanning, physical storage, and publication certification as out of scope for [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65).
- **Risk:** The schema could expose private provenance values while trying to document private field names. The implementation will treat private provenance names as schema terms only and will test that assigned values or maps fail.
- **Risk:** Scanner negative fixtures could block their own public artifacts. The implementation will construct denied examples at runtime or in temp files and will require the #65 public-surface scan to pass on committed artifacts.
- **Risk:** Scanner-safe schema representation could drift into natural JSON object-key shape. The implementation will test that private source terms remain array values under neutral keys and that private/source-like terms used as JSON keys fail validation.
- **Risk:** The new validator could require parent scanner self-exemptions. The implementation will avoid denied recursive traversal APIs in new source files by default and will add explicit tests before introducing any self-exemption.
- **Risk:** The schema-local JSON scanner could reveal a broader public-scan defect. The implementation will keep the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) fix scoped to #65 artifacts and will update [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)/[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) or file a follow-on for any reusable scanner rule.
- **Risk:** Parent and split registries could drift. The implementation will compare the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema against `docs/plans/ace-share-ingestion-wave-coordination.md`.
- **Open:** Gemini review remains unavailable in current noninteractive runs. [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) cannot move to `status:plan-review` until fresh review evidence is available under the workspace quorum policy.

---

## Complexity

**T2** - focused schema, validator, tests, and CI wiring across a few repo-local files, with security-sensitive public/private boundaries but no private source ingestion and no publication behavior.
