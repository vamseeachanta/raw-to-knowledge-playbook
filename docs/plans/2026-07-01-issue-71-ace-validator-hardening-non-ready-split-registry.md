# Plan for #71: ACE Validator Hardening for Non-Ready Wave 0 Split Registry Rows

> **Status:** plan-approved
> **Complexity:** T3
> **Date:** 2026-07-01
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/71
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-07-01-plan-71-claude-r1.md | scripts/review/results/2026-07-01-plan-71-codex-r1.md | scripts/review/results/2026-07-01-plan-71-gemini-r1.md | scripts/review/results/2026-07-01-plan-71-claude-r2.md | scripts/review/results/2026-07-01-plan-71-codex-r2.md | scripts/review/results/2026-07-01-plan-71-gemini-r2.md | scripts/review/results/2026-07-01-plan-71-claude-r3.md | scripts/review/results/2026-07-01-plan-71-codex-r3.md | scripts/review/results/2026-07-01-plan-71-gemini-r3.md

---

## Resource Intelligence Summary

### Existing repo code/docs

- `scripts/validate_ace_wave0_schema_contract.py` validates the #65 schema, coordination compatibility, and public scan paths. Its `_validate_split_registry()` function currently validates issue membership and dependencies for all rows, but it exits early for every `implementation_ready=false` row before checking `plan_path` or `status_snapshot`.
- `artifacts/ace-wave0-ledger-schema.json` records the wave-0 split rows for #65-#69. #66 and #67 are currently non-ready and have plan paths in the schema. #68 and #69 are also non-ready, but the schema still carries empty plan paths and `plan-required` snapshots even though their repo-local plan files now exist.
- `docs/plans/ace-share-ingestion-wave-coordination.md` has a separate human-facing `## Wave 0 Split Registry` table. The parent coordination validator currently parses only the later `## Child Wave Ledger` table, so this split registry is not a structured comparison source yet.
- `docs/plans/README.md` is the repo-local plan index. The repo policy says stock CI must validate repo-local contracts and snapshots, not depend on live GitHub authentication.
- `scripts/validate_ace_epic_wave_coordination.py` hardcodes the six #62 manifest source keys and validates that the coordination doc names exactly those six sources. It also checks #62 readiness evidence for exact six-source snapshot IDs.
- `config/ace-manifest-evidence-contract.json` is the #62-owned contract that already records the same six manifest source keys plus `depends_on_schema_issue=65`, `downstream_consumer_issue=70`, and `blocked_operational_issue=67`. The parent validator does not currently load that contract, so the manifest-source list and #62 handoff semantics are duplicated.
- `scripts/validate_ace_epic_wave_coordination.py` enforces the #62 row handoff through dependency-cell phrase checks. That is useful but still phrase-level, so implementation should tie the check to the #62 contract fields instead of relying only on prose.
- Parent public-scanner tests in `tests/test_validate_ace_epic_wave_coordination.py` contain several negative examples directly in the test source. The #62 review comment on #71 asks for a scan-safe negative-fixture pattern so future tests can prove denial behavior while allowing the test source itself to be scanned.

### Related issues

- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) implemented the wave-0 schema contract and validator. #71 will harden that validator; it will not reopen #65 implementation scope beyond this approved follow-on.
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) is `status:plan-review` and produced the review finding that non-ready split rows can drift.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) is `status:plan-review`. The reported regression was a #66/#67 swapped-row shape, so tests must cover that exact class.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) owns the manifest freshness evidence contract and the six-source manifest inventory. #71 will make the parent validator consume that contract as the source of truth.
- [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) consumes the #62 evidence contract for #67 integration. #71 will keep that #62-to-#70 handoff enforceable through a contract-backed check.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) is still the repo-local legal/security scan gate. #71 will keep its own public-surface scan clean and will include the #69 scan in closeout once that script exists.

### Source inventory

- #71 will not read ACE source data or private corpus material.
- #71 will operate on repo-local public methodology artifacts only: validators, tests, schema JSON, the plan index, coordination docs, and optional CI wiring.
- Negative scanner examples will be assembled from neutral string fragments at runtime and written only to temporary test files. Committed tests will not store raw hostile assignment examples that make the test module fail its own public scan.

### Gaps identified

- Non-ready split registry rows can point at another issue's plan or carry an invalid status snapshot and still pass `validate_schema()`.
- Current status vocabulary is inconsistent: ready rows use `status:plan-approved`, while non-ready #66/#67 schema rows use `plan-review` without the `status:` prefix.
- The #65 schema validator has no issue-specific expected plan path map for #65-#69, so it cannot reject a #66 row pointing to the #67 plan.
- The #65 schema validator does not compare split-registry snapshots to repo-local `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` state.
- #68 and #69 are live examples of empty-path drift: `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md` and `docs/plans/2026-07-01-issue-69-repo-local-legal-security-scan-gate.md` exist, but the schema rows still say `plan_path=""` and `status_snapshot="plan-required"`.
- The parent validator duplicates the six manifest source keys instead of loading them from `config/ace-manifest-evidence-contract.json`.
- The parent validator validates the #62 handoff by phrase matching, but it does not verify the corresponding #62 contract fields.
- Parent scanner negative tests are not yet safe to include in a self-scan of `tests/test_validate_ace_epic_wave_coordination.py`.

### Evidence

**Issue status**:

```text
$ gh issue view 71 --json number,title,state,labels,url
#71 OPEN ACE validator hardening: enforce non-ready wave0 split registry plan/status snapshots
labels=strengthening,lane:codex,priority:medium
url=https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/71
```

**Parallel work check**:

```text
$ git worktree list --porcelain
worktree /mnt/local-analysis/raw-to-knowledge-playbook
branch refs/heads/docs/ace-ingestion-wave-plans

worktree /mnt/local-analysis/wt-r2k-pages
branch refs/heads/feat/github-pages
```

No active sibling worktree is editing the #71 plan, wave-0 validators, or review artifacts.

**File existence**:

```text
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS tests/test_validate_ace_wave0_schema_contract.py
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS tests/test_validate_ace_epic_wave_coordination.py
EXISTS config/ace-manifest-evidence-contract.json
EXISTS docs/plans/2026-07-01-issue-71-ace-validator-hardening-non-ready-split-registry.md
EXISTS scripts/review/results/2026-07-01-plan-71-claude-r1.md
EXISTS scripts/review/results/2026-07-01-plan-71-codex-r1.md
EXISTS scripts/review/results/2026-07-01-plan-71-gemini-r1.md
EXISTS scripts/review/results/2026-07-01-plan-71-claude-r2.md
EXISTS scripts/review/results/2026-07-01-plan-71-codex-r2.md
EXISTS scripts/review/results/2026-07-01-plan-71-gemini-r2.md
EXISTS scripts/review/results/2026-07-01-plan-71-claude-r3.md
EXISTS scripts/review/results/2026-07-01-plan-71-codex-r3.md
EXISTS scripts/review/results/2026-07-01-plan-71-gemini-r3.md
```

**Reproduction proofs**:

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import copy
import importlib.util
import json
from pathlib import Path

p = Path("scripts/validate_ace_wave0_schema_contract.py")
spec = importlib.util.spec_from_file_location("v", p)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
schema = json.loads(Path("artifacts/ace-wave0-ledger-schema.json").read_text())
rows = {row["issue"]: row for row in schema["wave0_split_registry"]}
mutated = copy.deepcopy(schema)
mut_rows = {row["issue"]: row for row in mutated["wave0_split_registry"]}
mut_rows[66]["plan_path"] = rows[67]["plan_path"]
mut_rows[66]["status_snapshot"] = rows[67]["status_snapshot"]
mut_rows[67]["plan_path"] = ""
mut_rows[67]["status_snapshot"] = "nonsense-stale-status"
for issue in (66, 67):
    mut_rows[issue]["implementation_ready"] = False
errors = v.validate_schema(mutated)
print("mutated non-ready #66/#67 errors:", errors)
print("error_count:", len(errors))
PY
mutated non-ready #66/#67 errors: []
error_count: 0
```

This is the red proof for #71: the current validator accepts a non-ready #66 row pointing at the #67 plan and a non-ready #67 row with an invalid status snapshot.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-07-01-issue-71-ace-validator-hardening-non-ready-split-registry.md` |
| Plan index | `docs/plans/README.md` |
| Wave-0 schema | `artifacts/ace-wave0-ledger-schema.json` |
| Wave-0 schema validator | `scripts/validate_ace_wave0_schema_contract.py` |
| Wave-0 schema validator tests | `tests/test_validate_ace_wave0_schema_contract.py` |
| Parent coordination validator | `scripts/validate_ace_epic_wave_coordination.py` |
| Parent coordination validator tests | `tests/test_validate_ace_epic_wave_coordination.py` |
| #62 manifest evidence contract | `config/ace-manifest-evidence-contract.json` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Workflow | `.github/workflows/validate.yml` |
| Review artifact - Claude r1 | `scripts/review/results/2026-07-01-plan-71-claude-r1.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-07-01-plan-71-codex-r1.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-07-01-plan-71-gemini-r1.md` |
| Review artifact - Claude r2 | `scripts/review/results/2026-07-01-plan-71-claude-r2.md` |
| Review artifact - Codex r2 | `scripts/review/results/2026-07-01-plan-71-codex-r2.md` |
| Review artifact - Gemini r2 | `scripts/review/results/2026-07-01-plan-71-gemini-r2.md` |
| Review artifact - Claude r3 | `scripts/review/results/2026-07-01-plan-71-claude-r3.md` |
| Review artifact - Codex r3 | `scripts/review/results/2026-07-01-plan-71-codex-r3.md` |
| Review artifact - Gemini r3 | `scripts/review/results/2026-07-01-plan-71-gemini-r3.md` |

---

## Deliverable

After approval and implementation, #71 will harden the repo-local ACE validators so non-ready wave-0 split registry rows still have issue-correct plan paths and valid repo-local status snapshots, while parent manifest-source and #62 handoff checks are driven by the #62 evidence contract and scanner negative fixtures remain self-scan safe.

---

## Proposed Validation Contract

### Wave-0 split registry

The implementation will update `_validate_split_registry()` so every #65-#69 row is validated before the approval-marker branch:

- Issue membership will remain exactly #65-#69.
- Dependencies will be exact per the target dependency map in this plan. #69 will move from the stale `[68]` dependency to `[65]` to match the reviewed #69 dependency-correction plan and the current README/coordination surfaces. User approval of #71 approves this limited #69 dependency correction for the schema/validator contract. Because #69 is now also user-approved, the committed schema will record #69 as implementation-ready with `status:plan-approved`; synthetic no-marker tests will still prove the validator can represent the prior non-ready state without requiring approval markers.
- Each row will use a uniformly prefixed canonical status snapshot vocabulary: `status:plan-approved`, `status:plan-review`, `status:blocked-draft`, `status:draft`, and `status:plan-required`. Implementation will normalize existing non-ready rows to the prefixed vocabulary and will not accept both prefixed and unprefixed forms indefinitely.
- The validator will maintain an issue-specific expected plan path map for #65-#69. If the expected plan file exists on disk, the schema row's `plan_path` must equal that expected path. An empty `plan_path` will be rejected for #68 and #69 because their expected plan files already exist.
- If the expected plan file does not exist on disk, the row must carry `plan_path=""`, `status_snapshot="status:plan-required"`, and `implementation_ready=false`.
- Repo-local status normalization for the wave-0 split registry will use this precedence order: local approval marker plus `status:plan-approved`, then the coordination `## Wave 0 Split Registry` plan-status phrase, then a plan body overall result such as `BLOCKED-DRAFT`, then `docs/plans/README.md` Plan Index status. This makes #68 deterministic: the coordination phrase `blocked-draft` and the #68 plan's `BLOCKED-DRAFT` overall result normalize to `status:blocked-draft`.
- Lower-precedence surfaces may be compatible coarsenings, not automatic drift errors. For #68, README's generic `draft` status is compatible with the higher-precedence `status:blocked-draft` because the README status column cannot encode blocked-draft. For #65, the coordination phrase beginning with `implemented:` is compatible with `status:plan-approved` when the local approval marker exists and `implementation_ready=true`; it is an implementation-progress note, not a replacement for the approval-state snapshot.
- The validator will emit drift errors only when a lower-precedence surface contradicts, rather than coarsens, the highest-precedence status. `plan-review` normalizes to `status:plan-review`; `plan-approved` normalizes to `status:plan-approved`; plain `draft` normalizes to `status:draft` unless a higher-precedence blocked-draft signal exists; `plan-required` normalizes to `status:plan-required`.
- `implementation_ready=true` will still require `status:plan-approved` plus a valid local approval marker. #71 will not require approval markers for non-ready rows.
- The validator will reject the #66/#67 swapped-row regression where a non-ready #66 row points at #67's plan or a non-ready #67 row has a stale or invalid snapshot.

Target schema row normalization after implementation:

| Issue | Expected plan path | Target status snapshot | Implementation ready | Target dependencies |
|---|---|---|---|---|
| #65 | `docs/plans/2026-06-30-issue-65-ace-wave-0-ledger-schema-route-store-matrix.md` | `status:plan-approved` | true | `[]` |
| #66 | `docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md` | `status:plan-review` | false | `[65]` |
| #67 | `docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md` | `status:plan-review` | false | `[65]` |
| #68 | `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md` | `status:blocked-draft` | false | `[65, 66]` |
| #69 | `docs/plans/2026-07-01-issue-69-repo-local-legal-security-scan-gate.md` | `status:plan-approved` | true | `[65]` |

### Parent manifest-source contract

The implementation will update the parent validator so the six manifest source keys come from `config/ace-manifest-evidence-contract.json`:

- The contract must be readable JSON with the required handoff fields present.
- The parent validator will not maintain a second hardcoded tuple for `owner_issue`, `depends_on_schema_issue`, `downstream_consumer_issue`, or `blocked_operational_issue`. It will load those values from the contract and compare coordination-row wording to the loaded contract values.
- `manifest_source_keys` must be non-empty, unique, and exact relative to the contract fixture under test. The normal repo test will assert the current six keys in `config/ace-manifest-evidence-contract.json`; drift tests will mutate temporary contract fixtures to prove the validator rejects missing, duplicate, or extra keys without creating a second source of truth in production code.
- The coordination doc's `Named manifest sources` line must match the contract key list exactly.
- #62 snapshot evidence validation must compare against the same loaded contract key list.

### #62 handoff contract

The implementation will keep the #62 coordination-row handoff enforceable by checking both the ledger row and the contract fields:

- The #62 ledger row will be parsed and compared to the loaded contract fields, including the current #65 schema dependency, #70 downstream consumer, and #67 blocked operational boundary. Matching semantics will extract issue-role assertions from the #62 dependency cell: each loaded issue number must appear in a clause whose nearby role terms match the contract field being checked, and the same clause must not contain negators or opposite-state terms. For example, `blocked_operational_issue=67` will require a positive blocked-operational boundary assertion for `#67`, not mere token presence. A cell that says the same issue is unblocked, complete, no longer blocked, or otherwise operationally released will fail even if it still contains the required issue token.
- #51 will remain umbrella context only for this handoff.
- Contradictory or negated prose will be rejected even if it contains the required issue numbers.

### Scan-safe negative fixtures

The implementation will convert parent scanner negative fixtures to a self-scan-safe pattern:

- Denied examples will be built at runtime from neutral fragments.
- Runtime examples will be written into temporary files and passed to `validate_public_artifact_paths()`.
- Before adding the committed parent test source to self-scan, implementation will convert every current denied-literal class in `tests/test_validate_ace_epic_wave_coordination.py`: denied traversal command examples, private source field assignment examples, source-like raw digest examples, and ACE metadata evidence path examples. No residual committed line in that test file may trigger the parent scanner.
- The committed parent test source will be added to a self-scan assertion only after the conversion passes locally.
- If `.github/workflows/validate.yml` is changed, it will run the new self-scan or parent unit test explicitly.

---

## Pseudocode

```text
validate_schema(schema):
    validate_existing_schema_sections()
    validate_split_registry(schema)

validate_split_registry(schema):
    rows = rows_by_issue(schema["wave0_split_registry"])
    assert set(rows) == {65, 66, 67, 68, 69}
    plan_index = parse_docs_plans_readme()
    coordination_rows = parse_wave0_split_registry_section()
    for issue in [65, 66, 67, 68, 69]:
        row = rows[issue]
        require_target_dependencies(issue, row)
        require_allowed_status_snapshot(issue, row)
        expected_path = expected_plan_path(issue)
        require_expected_plan_path_or_plan_required(issue, row, expected_path)
        expected_status = normalized_expected_status(issue, plan_index, coordination_rows, plan_file)
        require_status_snapshot(issue, row, expected_status)
        require_lower_precedence_surfaces_do_not_silently_disagree(issue, plan_index, coordination_rows, plan_file)
        if row.implementation_ready:
            require_status_plan_approved(row)
            require_valid_approval_marker(issue, row.plan_path)

load_manifest_contract():
    record = json_load(config/ace-manifest-evidence-contract.json)
    require_required_handoff_fields_present(record)
    require_unique_manifest_source_keys(record)
    return record

validate_manifest_inventory(text):
    contract = load_manifest_contract()
    sources = parse_named_manifest_sources(text)
    require sources == contract.manifest_source_keys

test_negative_scanner_pattern():
    hostile_text = neutral_fragment_a + neutral_fragment_b + neutral_value
    write hostile_text to temp file
    assert scanner rejects temp file
    assert scanner accepts this committed test file
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `docs/plans/2026-07-01-issue-71-ace-validator-hardening-non-ready-split-registry.md` | Record the #71 plan and review boundary |
| Modify | `docs/plans/README.md` | Index the #71 plan |
| Modify after approval | `scripts/validate_ace_wave0_schema_contract.py` | Validate non-ready split rows for issue-correct plan paths, allowed snapshots, and repo-local consistency |
| Modify after approval | `tests/test_validate_ace_wave0_schema_contract.py` | Add red tests for #66/#67 swapped rows, invalid snapshots, blank/stale snapshots, and non-ready no-marker behavior |
| Modify after approval | `artifacts/ace-wave0-ledger-schema.json` | Normalize status snapshots and plan paths to the contract enforced by the validator |
| Modify after approval | `scripts/validate_ace_epic_wave_coordination.py` | Load the #62 contract for manifest keys and handoff fields |
| Modify after approval | `tests/test_validate_ace_epic_wave_coordination.py` | Add contract drift tests, duplicate/extra/missing manifest-source tests, handoff negation tests, and self-scan-safe negative fixtures |
| Modify after approval if needed | `docs/plans/ace-share-ingestion-wave-coordination.md` | Align split-registry snapshots with the implemented contract |
| Modify after approval if needed | `.github/workflows/validate.yml` | Run any new validator/test surface required by #71 |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_non_ready_split_registry_rejects_wrong_issue_plan_path` | A non-ready row cannot point at another issue's plan | #66 row with #67 plan path | Error naming #66 plan path mismatch |
| `test_non_ready_split_registry_rejects_empty_plan_path_when_expected_file_exists` | Empty path cannot hide a real local plan | #68 or #69 row with empty path while expected plan exists | Error naming missing expected plan path |
| `test_non_ready_split_registry_rejects_invalid_status_snapshot` | Non-ready rows still use a closed status vocabulary | #67 row with invalid snapshot text | Error naming invalid status snapshot |
| `test_non_ready_split_registry_rejects_status_drift_from_readme` | Schema snapshots must match repo-local plan index state | Schema row status differs from README row | Error naming status drift |
| `test_non_ready_split_registry_rejects_status_drift_from_coordination` | Schema snapshots must match the coordination split registry where parseable | Schema row differs from coordination row | Error naming coordination drift |
| `test_split_registry_normalizes_current_68_69_rows` | Current #68/#69 schema drift is corrected | Committed schema rows for #68/#69 | #68 has expected plan path and blocked-draft snapshot; #69 has expected plan path, approved snapshot, and implementation-ready state |
| `test_split_registry_records_69_dependency_correction` | #69 dependency correction is represented with current approval state | #69 schema row and validator dependency map | #69 depends on #65, records `status:plan-approved`, and remains independent of #68 |
| `test_split_registry_allows_65_implemented_note_with_approval_marker` | The #65 coordination implementation-progress note is compatible with approved status | Current #65 schema row, local marker, and coordination split row | No false drift error for #65 |
| `test_split_registry_allows_68_readme_draft_coarsening_when_blocked_draft_source_exists` | README `draft` coarsening does not override stronger blocked-draft evidence | Current #68 README row, coordination row, and plan body | #68 normalizes to `status:blocked-draft` without README drift |
| `test_non_ready_split_registry_allows_no_approval_marker` | Non-ready rows do not require approval markers | #66 non-ready row with valid plan/status and empty approval root | No marker-specific error |
| `test_ready_split_registry_still_requires_approval_marker` | Existing approval gate remains intact | Ready row with no marker | Error naming missing approval marker |
| `test_split_registry_covers_66_67_swapped_regression` | The reported #66/#67 swap fails | #66 uses #67 plan; #67 stale/blank | Validator rejects both defects |
| `test_schema_normalizes_status_snapshot_vocabulary` | Current schema uses one canonical status style | Committed schema row values | No mixed prefixed/unprefixed status drift |
| `test_manifest_sources_loaded_from_62_contract` | Parent validator uses the #62 contract source list | Good coordination doc and contract | No errors |
| `test_manifest_contract_rejects_missing_extra_or_duplicate_sources` | Contract key list is exact and unique | Mutated contract keys | Validator rejects missing, extra, or duplicate source |
| `test_manifest_inventory_rejects_contract_doc_drift` | Coordination inventory must match contract keys | Coordination doc differs from contract | Validator rejects manifest inventory drift |
| `test_issue_62_handoff_uses_contract_fields` | #62 handoff is contract-backed without a second production constant list | Mutated temporary #62 contract fields and unchanged coordination row | Validator rejects doc/contract mismatch |
| `test_issue_62_handoff_rejects_negated_or_contradictory_prose` | Token checks cannot be satisfied by contradictory role assertions | #62 dependency cell with negated, unblocked, complete, or released wording near the contract issue token | Validator rejects handoff |
| `test_parent_negative_scanner_fixtures_are_fragment_built` | Denial examples are runtime-built, not committed as raw hostile fixtures | Parent test source text | Self-scan of test source passes |
| `test_parent_test_source_self_scan_rejects_residual_denied_literals` | Every current denied-literal class is converted before self-scan | Parent test file after conversion | Parent scanner returns no findings |
| `test_parent_self_scan_conversion_avoids_private_leak_patterns` | Fragment-built negative fixtures do not introduce a different scanner class | Converted parent test source | No private-leak scanner findings |
| `test_public_artifact_scan_rejects_runtime_built_negative_examples` | Scanner still rejects the denial classes | Runtime temp files from neutral fragments | Scanner rejects temp files |
| `test_ci_invokes_hardened_validators` | CI covers the new hardening surface | `.github/workflows/validate.yml` | Validator and unit-test commands present |

---

## Acceptance Criteria

- [ ] Standalone #71 plan exists and passes adversarial review before implementation.
- [ ] `scripts/validate_ace_wave0_schema_contract.py` rejects a non-ready split row whose `plan_path` points to another issue's plan.
- [ ] `scripts/validate_ace_wave0_schema_contract.py` rejects an empty `plan_path` for any #65-#69 issue whose expected repo-local plan file exists.
- [ ] `scripts/validate_ace_wave0_schema_contract.py` rejects a non-ready split row with an invalid or stale status snapshot relative to repo-local tracked status surfaces.
- [ ] Tests cover the #66/#67 swapped-row regression.
- [ ] The committed #68 and #69 schema rows are normalized to the expected plan paths and prefixed status snapshots listed in this plan.
- [ ] The #69 row depends on #65 per the reviewed #69 dependency correction and reflects its current user-approved implementation-ready state.
- [ ] #65's coordination `implemented:` progress note and #68's README `draft` coarsening are positively tested as compatible with the stronger local status evidence.
- [ ] Non-ready rows do not require approval markers.
- [ ] Ready rows still require `status:plan-approved` and a valid local approval marker.
- [ ] Manifest source membership is driven by `config/ace-manifest-evidence-contract.json`, unique, and synchronized with the coordination doc without maintaining a second production source list.
- [ ] The #62 row handoff to the contract-defined schema dependency, downstream consumer, blocked operational issue, and #51 umbrella boundary remains enforceable through contract-backed checks, not only free-text matching.
- [ ] Negative scanner fixtures are assembled from neutral fragments at runtime, every current denied-literal class in the parent test source is converted, the conversion avoids private-leak patterns, and the parent test source can be self-scanned.
- [ ] Public-surface scan remains clean.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Empty-path bypass for #68/#69, missing target rows, undefined status precedence, mixed vocabulary, #62 hardcoding risk, and incomplete self-scan conversion scope. |
| Codex r1 | MAJOR | Stale evidence, empty-path bypass, undefined status precedence, #62 authority risk, and parent test self-scan conversion risk. |
| Gemini r1 | UNAVAILABLE | Gemini CLI failed before review due unsupported client/tier status. |
| Claude r2 | MAJOR | Status precedence still self-contradicted on #68/#65; review evidence and summary were stale; #62 token matching and private-leak avoidance needed definition. |
| Codex r2 | MAJOR | Stale r1 evidence remained; #68 drift rule contradicted the target; #69 dependency correction was not represented. |
| Gemini r2 | UNAVAILABLE | Gemini remained unavailable after r1 tier failure. |
| Claude r3 | MINOR | Requested explicit #69 approval coupling, a stronger #62 contradiction mechanism, positive compatibility tests for #65/#68, and complete r2/r3 artifact metadata. |
| Codex r3 | MINOR | Requested complete r2/r3 artifact metadata in the plan header and artifact map. |
| Gemini r3 | UNAVAILABLE | Gemini remained unavailable due unsupported client/tier status. |

**Overall result:** The active-provider r3 review returned no MAJOR findings after this plan revision resolved the remaining MINORs. #71 is `status:plan-approved`; implementation may proceed under TDD.

---

## Risks and Open Questions

- **Risk:** If the implementation uses live GitHub labels for normal validation, CI will become auth-dependent and brittle. Mitigation: use only repo-local `docs/plans/README.md`, `docs/plans/ace-share-ingestion-wave-coordination.md`, schema JSON, and approval markers.
- **Risk:** Tight plan-path checks can become noisy when plan filenames change. Mitigation: encode a single expected-path map for #65-#69 and update it transactionally with plan renames.
- **Risk:** Accepting both prefixed and unprefixed status labels would preserve ambiguity. Mitigation: choose one canonical schema vocabulary and normalize existing rows in the same implementation.
- **Risk:** Contract-backed manifest-source validation can self-deadlock if it hardcodes both sides. Mitigation: load `config/ace-manifest-evidence-contract.json` once and compare docs/evidence against that loaded list.
- **Risk:** Scanner tests can self-block if denied examples are committed literally. Mitigation: fragment-build hostile strings at runtime and add a self-scan test for the parent test file.
- **Risk:** #71's target schema map includes the #69 dependency correction that #69 itself marked as pending user approval. Mitigation: explicit user approval now covers both #69 and #71, so implementation will encode the approved #69 dependency correction and current approved status; if that approval is later rescinded, revert the #69 target dependency and approval snapshot before further implementation.
- **Open:** Whether `.github/workflows/validate.yml` already has sufficient parent validator coverage after test changes or needs an explicit new invocation will be determined during TDD implementation.

---

## Complexity

**T3** - #71 spans two validator surfaces, schema normalization, coordination/index consistency, scanner self-safety, and contract-backed #62 handoff enforcement. It is not an ingestion implementation, but the blast radius includes CI and public artifact safety gates.
