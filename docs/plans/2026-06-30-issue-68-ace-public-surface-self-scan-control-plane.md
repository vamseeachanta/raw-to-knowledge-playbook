# Plan for #68: ACE Wave 0 Public-Surface Self-Scan for Control-Plane Artifacts

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-30
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-30-plan-68-claude-r1.md | scripts/review/results/2026-06-30-plan-68-codex-r1.md | scripts/review/results/2026-06-30-plan-68-gemini-r1.md

---

## Resource Intelligence Summary

### Existing repo code/docs

- `scripts/validate_ace_epic_wave_coordination.py` will remain the parent coordination validator and will delegate its public-artifact scan entry point to the reusable #68 scanner after implementation.
- `scripts/validate_ace_wave0_schema_contract.py` will remain the #65 schema validator and will use the #68 scanner for schema/control-plane public surfaces after #68 is approved and implemented.
- `.github/workflows/validate.yml` will run repo-local validators only; it will not require live GitHub authentication for stock CI.
- `docs/07-data-governance.md`, `docs/18-security-and-pii.md`, and `docs/19-trust-boundary-and-private-mode.md` will remain policy sources for fail-closed public/private routing, but #68 will encode only the control-plane public-surface scanner contract.
- `skills/public-private-routing/SKILL.md`, `skills/page-shape-contract/SKILL.md`, `skills/source-extract-fidelity/SKILL.md`, `skills/adversarial-verify-loop/SKILL.md`, and `skills/verify-batch/SKILL.md` will be the bound skill group. Any reusable method gap found during implementation will be promoted into these skill docs or into a follow-on issue before closeout.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) will remain the approved parent epic for coordination and planning.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will remain the wave-0 umbrella. It delegates implementation-sized slices to [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) provides the committed schema/validator surface that #68 will generalize for public-surface scanning.
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) will define token fixtures and private-field placeholder contexts. This draft will not advance to `status:plan-review` until that dependency is planned/approved or the #68 scope is explicitly narrowed.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will consume the #68 self-scan contract for repo-local legal/security scan config safety. #69 will not define its own blanket exemptions.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will remain the owner of maintained private deny-lists, publication/comment certification, public-output canary behavior, and external publication exposure.

### Source inventory

- #68 will not read private ACE content and will not require source-root environment variables.
- The scanner will inspect repo-local public/control-plane artifacts, retained review artifacts, same-stem sidecars, and operator-supplied issue/comment body snapshot files.
- Issue/comment snapshots will be supplied as files by the operator or test fixtures. The scanner will not call live GitHub from stock CI.
- Negative fixtures will be synthetic and either generated at runtime or enclosed in machine-parseable sentinel contexts so committed public files do not self-block.

### Gaps identified

- The current parent public scan is embedded in the coordination validator rather than reusable by #65, #69, review artifact closeout, and issue/comment workflows.
- The current scan path model is opt-in and does not define a candidate contract for review artifacts, same-stem sidecars, or operator-fetched issue/comment body files.
- The current allow behavior is ad hoc. It does not define closed context IDs, heading/path constraints, token classes, start/end sentinels, maximum line budgets, or fail-closed malformed block handling.
- The #65 implementation review promoted a reusable bypass class: source-like provenance/digest field terms must be rejected as public JSON keys regardless of placeholder value shape.
- The repo has no #69 legal/security wrapper yet. #68 must define the self-scan-safe config boundary that #69 will consume without a blanket file exemption.
- #66 has not yet supplied the token fixture and private-field placeholder contract needed for final review of #68's placeholder contexts.

### Evidence

**Issue status** (verified 2026-06-30):

```text
#68 OPEN ACE wave 0 split: public-surface self-scan for control-plane artifacts labels=strengthening,lane:claude,priority:high
#66 OPEN ACE wave 0 split: public-token fixtures and private-field placeholders labels=strengthening,lane:codex,priority:high
```

**File existence** (verified 2026-06-30):

```text
EXISTS docs/plans/README.md
EXISTS docs/plans/ace-share-ingestion-wave-coordination.md
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS tests/test_validate_ace_epic_wave_coordination.py
EXISTS tests/test_validate_ace_wave0_schema_contract.py
EXISTS .github/workflows/validate.yml
EXISTS docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md
MISSING scripts/ace_public_surface_scan.py
MISSING scripts/validate_ace_public_surface_scan.py
MISSING tests/test_validate_ace_public_surface_scan.py
MISSING config/ace-public-surface-self-scan-contract.json
MISSING .planning/plan-approved/68.md
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md` |
| Scanner contract | `config/ace-public-surface-self-scan-contract.json` |
| Scanner library | `scripts/ace_public_surface_scan.py` |
| Scanner CLI | `scripts/validate_ace_public_surface_scan.py` |
| Unit tests | `tests/test_validate_ace_public_surface_scan.py` |
| Synthetic fixture directory | `tests/fixtures/ace-public-surface-self-scan/` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Workflow | `.github/workflows/validate.yml` |
| Review artifact - Claude r1 | `scripts/review/results/2026-06-30-plan-68-claude-r1.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-06-30-plan-68-codex-r1.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-06-30-plan-68-gemini-r1.md` |

---

## Deliverable

After approval and implementation, #68 will provide a reusable repo-local public-surface self-scan contract and executable scanner that can be used by control-plane validators, review artifact closeout, sidecar checks, issue/comment body workflows, and the downstream #69 legal/security wrapper without reading private source content or assuming publication certification.

---

## Pseudocode

```text
load config/ace-public-surface-self-scan-contract.json with Python stdlib json
validate contract metadata:
  owner_issue is #68
  downstream_consumers include #65, #69, and #63 boundary notes
  maintained private deny-list ownership remains #63
  stock CI mode does not require live GitHub access

validate closed deny classes:
  raw host/source paths outside fixed metadata evidence
  generic private-like identifiers
  personal identifiers
  confidentiality-marker phrases
  assigned private source field terms
  assigned source-like digest terms
  private lookup maps
  provider stderr/log sidecar leak traces
  source-like provenance/digest JSON keys regardless of placeholder value shape

validate closed allow contexts:
  every context has an id from the committed closed set
  every context declares path constraints, optional heading constraint, token classes,
  start sentinel, end sentinel, and max_lines
  unknown ids fail closed
  missing end sentinel fails closed
  over-budget blocks fail closed
  path or heading mismatch fails closed
  disallowed token classes fail closed
  no whole-file or whole-directory exemption is accepted

resolve public scan candidates:
  start from explicit CLI path arguments
  include same-stem sidecars for each selected review artifact when requested
  include retained review artifacts by exact issue and phase selectors when requested
  include operator-supplied issue body and comment body files when requested
  include operator-supplied refetched issue/comment body files when requested
  use bounded directory listing for known local artifact directories
  avoid full repo traversal and source-root traversal

scan each candidate file:
  read text with replacement for invalid bytes
  ignore compiled cache files
  report path, line number, rule id, and redacted rule summary
  never echo matched private-looking value in logs when the rule class is sensitive
  allow only matched content inside valid allow-context blocks

preserve existing parent CLI:
  keep scripts/validate_ace_epic_wave_coordination.py --scan-public-path usable
  route that option through the #68 scanner after approval
  keep existing parent coordination validations unchanged

upgrade #65 integration:
  route schema-local public-surface scans through the #68 scanner
  scan retained implementation-review artifacts or document a conditional path list
  keep #65 schema ownership separate from the #68 reusable scanner

define #69 handoff:
  expose a config self-scan context for legal/security deny-list declarations
  permit deny-list pattern declarations only in closed schema/policy contexts
  reject assigned private values and private lookup maps in legal/security config
  do not require #69 to invent a blanket exemption

define issue/comment workflow:
  scan body files before posting
  require operator to refetch posted body into a local file
  scan the refetched file before using the comment as status evidence
  keep live GitHub fetching outside stock CI

verify()
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `config/ace-public-surface-self-scan-contract.json` | Closed deny-class, allow-context, sidecar, review-artifact, and issue/comment body scan contract for #68 |
| Create | `scripts/ace_public_surface_scan.py` | Reusable Python stdlib scanner library for repo-local public/control-plane surfaces |
| Create | `scripts/validate_ace_public_surface_scan.py` | Executable CLI for explicit path scans, review artifact selectors, same-stem sidecars, and issue/comment body files |
| Create | `tests/test_validate_ace_public_surface_scan.py` | TDD coverage for deny classes, allow contexts, sidecars, review artifacts, issue/comment body files, and #69 config handoff |
| Create | `tests/fixtures/ace-public-surface-self-scan/` | Synthetic fixture set for public-surface scanner behavior |
| Modify | `scripts/validate_ace_epic_wave_coordination.py` | Preserve existing coordination checks while routing public path scans through the reusable #68 scanner |
| Modify | `scripts/validate_ace_wave0_schema_contract.py` | Use the #68 scanner for #65 public-surface scan sets and retained review artifact coverage |
| Modify | `tests/test_validate_ace_epic_wave_coordination.py` | Preserve parent public-scan CLI behavior through the new scanner |
| Modify | `tests/test_validate_ace_wave0_schema_contract.py` | Verify #65 integration with the #68 scanner and retained implementation-review artifact candidates |
| Modify | `.github/workflows/validate.yml` | Run the #68 scanner over repo-local control-plane scan sets without requiring live GitHub authentication |
| Modify | `docs/plans/README.md` | Record #68 draft plan status and blocked dependency on #66 |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Record #68 draft plan status and keep implementation readiness false |
| Conditional scan-clean modify or follow-on | `skills/public-private-routing/SKILL.md` | Promote scanner usage guidance if implementation exposes a reusable public/private routing method gap |
| Conditional scan-clean modify or follow-on | `skills/page-shape-contract/SKILL.md` | Promote closed context and heading/path constraint guidance if needed |
| Conditional scan-clean modify or follow-on | `skills/source-extract-fidelity/SKILL.md` | Promote source-fidelity public-surface leak guidance if needed |
| Conditional scan-clean modify or follow-on | `skills/adversarial-verify-loop/SKILL.md` | Promote review artifact and sidecar scanning guidance if needed |
| Conditional scan-clean modify or follow-on | `skills/verify-batch/SKILL.md` | Promote batch verification scan hygiene if needed |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_contract_is_json_and_owned_by_68` | Scanner contract is machine-readable and issue-owned | `config/ace-public-surface-self-scan-contract.json` | JSON loads with owner, version, deny classes, allow contexts, and boundary notes |
| `test_blocks_raw_host_and_source_paths` | Public surfaces cannot leak host/source paths outside fixed evidence rows | Synthetic public artifact file | Scanner fails with path-leak rule id and redacted match summary |
| `test_allows_fixed_metadata_evidence_shape_only` | Existing metadata evidence shape remains narrow | Fixed evidence rows and near-miss rows | Known metadata rows pass; unlisted or malformed rows fail |
| `test_blocks_generic_private_like_identifiers` | Generic private-looking identifiers are rejected without real names | Synthetic identifier fixture | Scanner fails without needing maintained private deny-lists |
| `test_blocks_personal_identifier_patterns` | Emails, phone-like values, and personal-id-like values fail | Synthetic public artifact file | Scanner fails with personal identifier rule id |
| `test_blocks_confidentiality_marker_phrases` | Public artifacts cannot contain confidentiality-marker phrases | Synthetic public artifact file | Scanner fails with confidentiality marker rule id |
| `test_blocks_private_source_field_assignments` | Private source terms are allowed only as schema field names, not assigned values | Runtime-generated assignment fixture | Scanner fails |
| `test_blocks_source_like_digest_keys_regardless_of_value_shape` | JSON key bypass promoted from #65 cannot recur | Runtime-generated JSON fixture | Scanner fails even when placeholder value is non-digest-shaped |
| `test_blocks_assigned_source_like_digest_values` | Assigned digest values remain blocked | Runtime-generated fixture | Scanner fails |
| `test_blocks_private_lookup_maps` | Private lookup maps cannot appear in public artifacts | Runtime-generated fixture | Scanner fails |
| `test_blocks_provider_stderr_and_log_sidecar_leaks` | Sidecars cannot expose local auth paths, file URIs, or provider trace paths | Synthetic sidecar file | Scanner fails with sensitive summary redacted |
| `test_allow_context_ids_are_closed` | Unknown allow-context IDs fail | Synthetic sentinel block | Scanner fails closed |
| `test_allow_context_requires_start_and_end_sentinels` | Malformed sentinel blocks fail | Missing-end and missing-start fixtures | Scanner fails closed |
| `test_allow_context_enforces_path_and_heading_constraints` | Contexts are not portable bypasses | Valid block moved to wrong path or heading | Scanner fails closed |
| `test_allow_context_enforces_token_classes_and_max_lines` | Contexts remain bounded and machine-parseable | Over-budget or wrong-token fixture | Scanner fails closed |
| `test_no_blanket_file_or_directory_exemptions` | Exemption model cannot bypass whole files | Contract fixture with whole-file exemption | Scanner fails |
| `test_review_artifact_selector_is_bounded` | Review artifact discovery is exact and non-recursive | Issue/phase selector for local review directory | Only matching retained artifacts are selected |
| `test_same_stem_sidecars_are_scanned` | Adjacent provider outputs cannot bypass review scanning | Review artifact plus same-stem sidecar | Both files are scanned; sidecar leak fails |
| `test_issue_comment_body_files_scan_before_posting` | Comment body workflow has a pre-posting gate | Synthetic body file | Scanner fails unsafe body and passes safe body |
| `test_refetched_issue_comment_body_files_scan_after_posting` | Posted comment evidence is verified after refetch | Synthetic refetched body file | Scanner fails unsafe refetch and passes safe refetch |
| `test_parent_scan_public_path_cli_uses_new_scanner` | Existing parent CLI remains compatible | Parent validator with explicit scan path | Same pass/fail behavior through #68 scanner |
| `test_schema_validator_uses_new_scanner_for_public_paths` | #65 scanner integration is upgraded | #65 validator scan set | Schema validator delegates public-surface scanning to #68 library |
| `test_69_config_self_scan_context_has_no_blanket_exemption` | Legal/security config can declare deny patterns safely | Synthetic #69 config fixture | Closed policy context passes; assigned private values fail |
| `test_63_boundary_is_enforced` | #68 does not claim publication certification or maintained private deny-lists | Contract metadata | #63 ownership remains explicit; #68 scanner remains generic |
| `test_negative_fixtures_are_runtime_generated_or_sentinel_wrapped` | Tests do not commit raw self-blocking examples | Test source and fixture files | Scanner source/fixtures pass committed-file scan |
| `test_ci_invokes_public_surface_scanner` | CI uses the new scanner | `.github/workflows/validate.yml` | Workflow invokes #68 scanner over repo-local public/control-plane targets |

---

## Acceptance Criteria

- [ ] A standalone issue plan will exist for #68 and will not authorize implementation until adversarial plan review, user approval, `status:plan-approved`, and `.planning/plan-approved/68.md`.
- [ ] `config/ace-public-surface-self-scan-contract.json` will define closed deny classes, closed allow contexts, sensitive log redaction behavior, review artifact selectors, sidecar selectors, issue/comment body file handling, and downstream ownership boundaries.
- [ ] `scripts/validate_ace_public_surface_scan.py` will scan explicit public artifact paths and will fail closed on missing paths.
- [ ] The scanner will block raw host/source paths outside the fixed metadata-evidence shape, generic private-like identifiers, personal identifiers, confidentiality-marker phrases, assigned private source field terms, assigned source-like digest terms, private lookup maps, and provider stderr/log sidecar leaks.
- [ ] Source-like provenance/digest terms will be rejected as public JSON keys regardless of placeholder value shape.
- [ ] Machine-parseable allow contexts will use closed context IDs, path constraints, optional heading constraints, token classes, start/end sentinels, maximum line budgets, and fail-closed malformed block handling.
- [ ] No allow context will permit whole-file or whole-directory exemption.
- [ ] Review artifacts and same-stem sidecars will be scanned before they are cited as review/status evidence.
- [ ] Issue/comment body files will be scanned before posting, and operator-refetched issue/comment body files will be scanned before the posted content is used as status evidence.
- [ ] Stock CI will not require live GitHub authentication; live issue/comment refetch will remain an operator workflow with scanned body files.
- [ ] The parent coordination validator will preserve its existing `--scan-public-path` behavior while using the #68 scanner.
- [ ] The #65 schema validator will use the #68 scanner for public-surface scan paths after #68 implementation.
- [ ] #69 will be able to define repo-local legal/security deny-list declarations inside a closed self-scan-safe policy context without a blanket config exemption.
- [ ] #63 will remain the owner of maintained private deny-lists, publication/comment certification, public-output canary behavior, and external publication exposure.
- [ ] Negative fixtures will be runtime-generated or sentinel-wrapped so committed public artifacts, tests, and review artifacts do not self-block.
- [ ] Any reusable method gap exposed by implementation will be promoted to the bound skills or filed as a follow-on issue before closeout.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_public_surface_scan.py --scan-public-path docs/plans/README.md` will pass after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_public_surface_scan` will pass after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py` and `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` will still pass after implementation.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude | PENDING | Not yet reviewed |
| Codex | PENDING | Not yet reviewed |
| Gemini | PENDING | Not yet reviewed |

**Overall result:** BLOCKED-DRAFT - not ready for `status:plan-review` until #66 supplies the token fixture/private-field placeholder contract or the #68 scope is explicitly narrowed.

---

## Risks and Open Questions

- **Risk:** Over-broad patterns could block the scanner contract, tests, or legal/security config. Implementation will use closed allow contexts and runtime-generated fixtures rather than blanket exemptions.
- **Risk:** Under-broad patterns could create false confidence before #63 publication certification exists. #68 will remain generic control-plane scanning and will not replace #63.
- **Risk:** Review artifact selector drift could miss retained provider sidecars. Implementation will use exact issue/phase selectors plus same-stem sidecar discovery in known artifact directories.
- **Risk:** Live issue/comment refetch cannot run in stock CI. Implementation will make the body-file/refetched-body-file scan command executable and keep live fetching as an operator step.
- **Open:** #66 must define the token fixture and private-field placeholder context before this plan can move to formal plan review without a scope reduction.

---

## Complexity

**T3** - This is a security-sensitive reusable scanner contract that affects control-plane artifacts, validators, review evidence, issue/comment workflows, and the downstream legal/security gate.
