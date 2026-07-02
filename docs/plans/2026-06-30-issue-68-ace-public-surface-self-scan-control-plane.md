# Plan for #68: ACE Wave 0 Public-Surface Self-Scan for Control-Plane Artifacts

> **Status:** plan-approved
> **Complexity:** T3
> **Date:** 2026-06-30
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-07-02-plan-68-claude-r1.md | scripts/review/results/2026-07-02-plan-68-codex-r1.md | scripts/review/results/2026-07-02-plan-68-gemini-r1.md | scripts/review/results/2026-07-02-plan-68-claude-r2.md | scripts/review/results/2026-07-02-plan-68-codex-r2.md | scripts/review/results/2026-07-02-plan-68-gemini-r2.md | scripts/review/results/2026-07-02-plan-68-claude-r3.md | scripts/review/results/2026-07-02-plan-68-codex-r3.md | scripts/review/results/2026-07-02-plan-68-gemini-r3.md

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
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) is implemented and supplies the token fixture/private-field placeholder contract. #68 will consume that contract instead of redefining public-token or placeholder grammar.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) is implemented as the repo-local legal/security scan gate. #68 will provide the broader reusable public-surface scanner and must not weaken #69's stricter legal/security gate.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will remain the owner of maintained private deny-lists, publication/comment certification, public-output canary behavior, and external publication exposure.

### Source inventory

- #68 will not read private ACE content and will not require source-root environment variables.
- The scanner will inspect repo-local public/control-plane artifacts, retained review artifacts, same-stem sidecars, and operator-supplied issue/comment body snapshot files.
- Issue/comment snapshots will be supplied as files by the operator or test fixtures. The scanner will not call live GitHub from stock CI.
- Negative fixtures will be synthetic and either generated at runtime or enclosed in machine-parseable sentinel contexts so committed public files do not self-block.
- `config/ace-public-token-fixture-contract.json` will be the authoritative upstream contract for public token grammar, private source terms, source-like digest terms, placeholder values, placeholder mapping, and owner boundaries. #68 will import those values and will not restate or fork them.
- `.legal-deny-list.yaml`, `scripts/legal/legal_sanity_scan.py`, and `scripts/legal/legal-sanity-scan.sh` are #69-owned legal/security gate artifacts. #68 will preserve that gate and will not apply a separate #68 allow-context model to `.legal-deny-list.yaml`.

### Gaps identified

- The current parent public scan is embedded in the coordination validator rather than reusable by #65, #69, review artifact closeout, and issue/comment workflows.
- The current scan path model is opt-in and does not define a candidate contract for review artifacts, same-stem sidecars, or operator-fetched issue/comment body files.
- The current allow behavior is ad hoc. It does not define closed context IDs, heading/path constraints, token classes, start/end sentinels, maximum line budgets, or fail-closed malformed block handling.
- The #65 implementation review promoted a reusable bypass class: source-like provenance/digest field terms must be rejected as public JSON keys regardless of placeholder value shape.
- #69 now supplies a repo-local legal/security gate. #68 must remain compatible with it without introducing blanket file exemptions or duplicate deny-list ownership.
- #66 now supplies the token fixture and private-field placeholder contract needed for #68 placeholder contexts. Fresh plan review must verify #68 imports that boundary rather than silently redefining it.
- The current #68 draft still under-specifies review artifact selection, sidecar semantics, issue/comment snapshot metadata, and plan-review transition evidence. This revision will make those contracts explicit before another review round.

### Evidence

**Issue status** (verified 2026-06-30):

```text
#68 OPEN ACE wave 0 split: public-surface self-scan for control-plane artifacts labels=strengthening,lane:claude,priority:high
#65 CLOSED ACE wave 0 split: ledger schema and route-store matrix labels=strengthening,status:plan-approved,lane:claude,priority:high
#66 CLOSED ACE wave 0 split: public-token fixtures and private-field placeholders labels=strengthening,status:plan-approved,lane:codex,priority:high
#69 CLOSED ACE wave 0 split: repo-local legal and security scan gate labels=strengthening,status:plan-approved,lane:claude,priority:high
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
EXISTS config/ace-public-token-fixture-contract.json
EXISTS scripts/legal/legal-sanity-scan.sh
EXISTS scripts/legal/legal_sanity_scan.py
EXISTS .legal-deny-list.yaml
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
| Upstream #66 token/placeholder contract | `config/ace-public-token-fixture-contract.json` |
| Existing #69 legal scan shell entrypoint | `scripts/legal/legal-sanity-scan.sh` |
| Existing #69 legal scanner | `scripts/legal/legal_sanity_scan.py` |
| Existing #69 legal scan config | `.legal-deny-list.yaml` |
| Scanner library | `scripts/ace_public_surface_scan.py` |
| Scanner CLI | `scripts/validate_ace_public_surface_scan.py` |
| Unit tests | `tests/test_validate_ace_public_surface_scan.py` |
| Synthetic fixture directory | `tests/fixtures/ace-public-surface-self-scan/` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Workflow | `.github/workflows/validate.yml` |
| Formal review artifact - Claude r1 | `scripts/review/results/2026-07-02-plan-68-claude-r1.md` |
| Formal review artifact - Codex r1 | `scripts/review/results/2026-07-02-plan-68-codex-r1.md` |
| Formal review artifact - Gemini r1 | `scripts/review/results/2026-07-02-plan-68-gemini-r1.md` |
| Formal review artifact - Claude r2 | `scripts/review/results/2026-07-02-plan-68-claude-r2.md` |
| Formal review artifact - Codex r2 | `scripts/review/results/2026-07-02-plan-68-codex-r2.md` |
| Formal review artifact - Gemini r2 | `scripts/review/results/2026-07-02-plan-68-gemini-r2.md` |
| Formal review artifact - Claude r3 | `scripts/review/results/2026-07-02-plan-68-claude-r3.md` |
| Formal review artifact - Codex r3 | `scripts/review/results/2026-07-02-plan-68-codex-r3.md` |
| Formal review artifact - Gemini r3 | `scripts/review/results/2026-07-02-plan-68-gemini-r3.md` |
| Prep review artifact - dependency boundary r1 | `scripts/review/results/2026-07-02-plan-68-subagent-boundary-r1.md` |
| Prep review artifact - scanner contract r1 | `scripts/review/results/2026-07-02-plan-68-subagent-scanner-r1.md` |
| Prep review artifact - workflow/status r1 | `scripts/review/results/2026-07-02-plan-68-subagent-workflow-r1.md` |
| Prep review artifact - dependency boundary r2 | `scripts/review/results/2026-07-02-plan-68-subagent-boundary-r2.md` |
| Prep review artifact - scanner contract r2 | `scripts/review/results/2026-07-02-plan-68-subagent-scanner-r2.md` |
| Prep review artifact - workflow/status r2 | `scripts/review/results/2026-07-02-plan-68-subagent-workflow-r2.md` |
| Prep review artifact - dependency boundary r3 | `scripts/review/results/2026-07-02-plan-68-subagent-boundary-r3.md` |
| Prep review artifact - scanner contract r3 | `scripts/review/results/2026-07-02-plan-68-subagent-scanner-r3.md` |
| Prep review artifact - workflow/status r3 | `scripts/review/results/2026-07-02-plan-68-subagent-workflow-r3.md` |

---

## Deliverable

After approval and implementation, #68 will provide a reusable repo-local public-surface self-scan contract and executable scanner that can be used by control-plane validators, review artifact closeout, sidecar checks, and issue/comment body workflows without reading private source content or assuming publication certification. #69 is an already-implemented sibling legal/security gate; #68 may offer a future optional broader scan integration, but it must not require #69 contract changes or weaken #69's existing stricter scan.

---

## Pseudocode

```text
load config/ace-public-surface-self-scan-contract.json with Python stdlib json
load config/ace-public-token-fixture-contract.json with Python stdlib json
validate contract metadata:
  owner_issue is #68
  upstream_contracts include #66 token fixture/private-field placeholder contract
  sibling_boundaries record #69 as already implemented and #68-optional only
  maintained private deny-list ownership remains #63
  stock CI mode does not require live GitHub access
  no live GitHub API, gh CLI, or GH_TOKEN dependency is allowed in stock CI mode

validate #66 import:
  public token field name, token grammar, generation request marker, private
  source terms, source-like digest terms, placeholder values, placeholder
  mapping rows, fixture set ids, forbidden request keys, and boundary owner
  issues are imported exactly from #66
  drift between #68 contract and #66 contract fails closed
  #68 does not define an alternate public-token grammar, placeholder value set,
  private source term set, source-like digest term set, forbidden request key
  set, fixture set enum, or placeholder map

validate closed deny classes:
  raw host/source paths outside fixed metadata evidence
  generic private-like identifiers
  personal identifiers
  confidentiality-marker phrases
  assigned private source field terms
  assigned source-like digest terms
  private lookup maps
  provider stderr/log sidecar leak traces
  private source field JSON keys regardless of placeholder value shape
  source-like provenance/digest JSON keys regardless of placeholder value shape
  #66 forbidden request keys when used as public JSON keys or assigned values

validate closed allow contexts:
  every context has an id from the committed closed set
  every context declares path constraints, optional heading constraint, token classes,
  start sentinel, end sentinel, and max_lines
  unknown ids fail closed
  missing end sentinel fails closed
  over-budget blocks fail closed
  path or heading mismatch fails closed
  disallowed token classes fail closed
  nested, overlapping, or EOF-malformed blocks fail closed
  no whole-file or whole-directory exemption is accepted

resolve public scan candidates:
  start from explicit CLI path arguments
  include same-stem sidecars for each selected review artifact when requested
  include retained review artifacts by exact issue, phase, provider, and round
  include operator-supplied issue/comment body snapshot files when requested
  include operator-supplied refetched issue/comment body snapshot files when requested
  use bounded directory listing for known local artifact directories
  avoid full repo traversal and source-root traversal
  reject absolute paths, parent traversal, symlinks, unreadable paths, and
  unclassified public-adjacent paths

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

respect #69 sibling gate:
  keep bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces
  wired in CI
  do not replace #69 allow-context semantics for .legal-deny-list.yaml
  when #68 scans workflow/control-plane files, preserve the #69 legal scan step
  run #69 legal scan in #68 verification so the broader scanner cannot weaken it

define issue/comment workflow:
  body snapshots are JSON files with closed metadata schema
  pre-post body snapshot uses phase pre_post and comment_id null
  refetched body snapshot uses phase post_refetch and non-null comment_id/url
  pair validation requires an allowed source_kind transition, same issue_number,
  same body_sha256, and a URL relationship to the posted GitHub object
  scan body snapshot before posting
  require operator to refetch posted body into a local snapshot file
  scan the refetched snapshot before using the comment as status evidence
  keep live GitHub fetching outside stock CI

verify()
```

---

## Contract Details Required Before Implementation

### #66 import boundary

#68 will treat `config/ace-public-token-fixture-contract.json` as the only source for:

- public token field name and token grammar;
- generation request marker and required request keys;
- private source terms;
- source-like digest/provenance terms;
- placeholder value enum;
- placeholder mapping rows;
- fixture set ID enum;
- forbidden request key enum;
- boundary owner issues.

The #68 contract may cache these values only with a `source_contract_path`, `source_contract_id`, and `source_contract_version` field. The validator will reload #66 and fail if the cached #68 copy drifts. Deny-class tests will cover every imported private source term, every imported source-like digest/provenance term, and every imported forbidden request key used as a JSON key with these value shapes: #66 placeholder value, safe-looking string, null, array, and object. This closes the key-bypass classes without restating #66 grammar in #68.

### Allow-context contract

The committed contract will define this closed context table:

| context_id | Allowed paths | Heading constraint | Token classes | Embedding | Max lines |
|---|---|---|---|---|---|
| `schema-term-policy-prose` | Markdown plan and Markdown review artifacts for #68 only | `Pseudocode`, `Contract Details Required Before Implementation`, `TDD Test List`, or `Acceptance Criteria` | `schema_term`, `placeholder_value`, `public_token_grammar`, `rule_id` | HTML comment start/end sentinels in Markdown only | 40 |
| `review-artifact-forensics` | `scripts/review/results/*plan-68*.md` and selected text sidecars | N/A | `review_finding_excerpt`, `redacted_path_token`, `rule_id` | HTML comment start/end sentinels for Markdown/text sidecars only | 30 |

The sentinel form is `<!-- ace-public-scan-allow:start context_id=<id> token_class=<class> -->` and `<!-- ace-public-scan-allow:end context_id=<id> -->`. Allowed token classes are a closed enum. Unknown context IDs, unknown token classes, wrong path, wrong heading, missing start, missing end, nested blocks, overlapping blocks, EOF while in a block, and line-budget overflow all fail closed. No context can exempt an entire file, directory, extension, or rule class.

Strict JSON artifacts and Python source files will not use HTML-comment sentinel blocks. JSON artifacts must represent policy terms as neutral structured values and runtime fixtures; Python source/tests must use string fragments or runtime-generated temporary fixtures. #68 tests will reject HTML-comment sentinel usage in strict JSON files and will self-scan Python sources without relying on sentinel comments.

#69 exception: `.legal-deny-list.yaml` remains governed by #69's same-line sentinel and rule/path allow-context semantics. #68 will not apply the table above to `.legal-deny-list.yaml`; tests will verify the #69 legal scan still passes independently after #68 changes.

### Review artifacts and sidecars

Review artifact selection will use explicit arguments, not recursive discovery:

```text
--review-issue 68 --review-phase plan --review-provider <provider> --review-round <rN> [--include-sidecars]
```

The only review directory is `scripts/review/results/`. A selected markdown artifact must match `YYYY-MM-DD-plan-68-<provider>-r<N>.md` after path normalization. Provider names are the closed enum `claude`, `codex`, `gemini`, `subagent-boundary`, `subagent-scanner`, and `subagent-workflow`; adding a new provider ID requires a contract update. Absolute paths, parent traversal, symlinks, unreadable paths, and files outside the review directory fail closed.

Same-stem sidecars are selected only when `--include-sidecars` is present. The suffix set is closed: `.err`, `.stderr`, `.stdout`, `.json`, `.log`, and `.trace`. Existing sidecars are scanned whether tracked or untracked. Missing sidecars are allowed only when the selector records `sidecar_status=none_found`; if a caller marks a sidecar as required, absence fails closed. A selected review artifact cannot be cited as plan/status evidence until the artifact and every selected sidecar pass the scanner and the artifact set is committed and pushed.

### Issue/comment snapshot schema

Issue/comment body inputs will be JSON snapshots with exactly these top-level keys:

```text
schema_version, issue_number, comment_id, url, source_kind, phase,
fetched_at, body_sha256, body
```

`source_kind` is one of `issue_body`, `planned_comment`, or `issue_comment`. `phase` is one of `pre_post` or `post_refetch`. A `pre_post` snapshot must have `comment_id=null`. A refetched snapshot must have a non-null `comment_id` when `source_kind=issue_comment`, a GitHub URL for the target issue/comment, and the same `issue_number` and `body_sha256` as the paired pre-post snapshot.

Allowed pairing transitions are closed:

| Pre-post source_kind | Refetched source_kind | Required relationship |
|---|---|---|
| `planned_comment` | `issue_comment` | Same issue, same body hash, refetched comment URL/comment ID records the posted object |
| `issue_body` | `issue_body` | Same issue, same body hash, refetched issue URL records the issue body object |

Missing, extra, mismatched, undefined-phase, undefined-source-kind, or stale metadata fails closed before the snapshot can be used as status evidence.

### Provider review gate

#68 is T3. The formal plan-review gate requires a same-round provider review set with at least two usable provider results and no usable provider returning MAJOR. Claude and Codex are usable in this environment. Gemini may be recorded as `UNAVAILABLE` only with the exact CLI/auth/quota reason and does not count toward the usable-provider floor. Preparatory Codex subagent artifacts are useful review evidence but do not count as provider-review quorum.

### Plan-review transition checklist

For the `status:plan-review` transition, the operator will:

1. update this plan's header, review artifact list, Adversarial Review Summary, and Overall result to `status:plan-review` / no-MAJOR provider review evidence;
2. update `docs/plans/README.md`, `docs/plans/ace-share-ingestion-wave-coordination.md`, `artifacts/ace-wave0-ledger-schema.json`, and related schema tests so #68 records `status:plan-review` with `implementation_ready=false`;
3. add a schema/status test that rejects `status:plan-review` when any current-state surface still contains `blocked-draft` / `BLOCKED-DRAFT`, and add an assertion that the coordination-row replacement fixture actually changed before validation;
4. run the ACE coordination, schema, legal scan, targeted schema unit test, and whitespace validators;
5. commit and push the updated plan, status artifacts, and final provider review artifacts;
6. verify the remote branch head equals the reviewed/pushed commit;
7. create temporary repo-relative Markdown body files under `artifacts/ace-public-surface-self-scan/plan-review-evidence/`, scan them with the existing parent `--scan-public-path` public scanner and #69 legal scan, post the pre-scan-safe comment, refetch the posted body into the same repo-relative scratch directory, scan the refetch with the same existing scanners, then remove those scratch files before final clean-state verification;
8. record the posted comment URL in the operator notes and only then add `status:plan-review`;
9. stop for user approval without creating `.planning/plan-approved/68.md`.

The future #68 JSON snapshot schema is implementation scope after user approval; it is not a prerequisite for the pre-approval label-time evidence comment because the #68 scanner does not exist before implementation.

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `config/ace-public-surface-self-scan-contract.json` | Closed deny-class, allow-context, sidecar, review-artifact, and issue/comment body scan contract for #68 |
| Create | `scripts/ace_public_surface_scan.py` | Reusable Python stdlib scanner library for repo-local public/control-plane surfaces |
| Create | `scripts/validate_ace_public_surface_scan.py` | Executable CLI for explicit path scans, review artifact selectors, same-stem sidecars, and issue/comment body files |
| Create | `tests/test_validate_ace_public_surface_scan.py` | TDD coverage for deny classes, allow contexts, sidecars, review artifacts, issue/comment body files, and #69 sibling-gate preservation |
| Create | `tests/fixtures/ace-public-surface-self-scan/` | Synthetic fixture set for public-surface scanner behavior |
| Modify | `scripts/validate_ace_epic_wave_coordination.py` | Preserve existing coordination checks while routing public path scans through the reusable #68 scanner |
| Modify | `scripts/validate_ace_wave0_schema_contract.py` | Use the #68 scanner for #65 public-surface scan sets and retained review artifact coverage |
| Modify | `tests/test_validate_ace_epic_wave_coordination.py` | Preserve parent public-scan CLI behavior through the new scanner |
| Modify | `tests/test_validate_ace_wave0_schema_contract.py` | Verify #65 integration with the #68 scanner, retained implementation-review artifact candidates, and the #68 plan-review status transition remaining `implementation_ready=false` |
| Modify | `artifacts/ace-wave0-ledger-schema.json` | Plan-review transition only: record #68 as `status:plan-review` with `implementation_ready=false` after no-MAJOR review evidence is committed and pushed |
| Modify | `.github/workflows/validate.yml` | Run the #68 scanner over repo-local control-plane scan sets without requiring live GitHub authentication and preserve the #69 legal/security scan step |
| Modify | `docs/plans/README.md` | Record #68 draft plan status and dependency-cleared review readiness |
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
| `test_contract_imports_66_without_drift` | #68 imports #66 token, private-term, placeholder, fixture-set, forbidden-key, and boundary metadata instead of redefining it | #68 contract plus `config/ace-public-token-fixture-contract.json` | Exact imported values match #66 or validation fails |
| `test_blocks_raw_host_and_source_paths` | Public surfaces cannot leak host/source paths outside fixed evidence rows | Synthetic public artifact file | Scanner fails with path-leak rule id and redacted match summary |
| `test_allows_fixed_metadata_evidence_shape_only` | Existing metadata evidence shape remains narrow | Fixed evidence rows and near-miss rows | Known metadata rows pass; unlisted or malformed rows fail |
| `test_blocks_generic_private_like_identifiers` | Generic private-looking identifiers are rejected without real names | Synthetic identifier fixture | Scanner fails without needing maintained private deny-lists |
| `test_blocks_personal_identifier_patterns` | Emails, phone-like values, and personal-id-like values fail | Synthetic public artifact file | Scanner fails with personal identifier rule id |
| `test_blocks_confidentiality_marker_phrases` | Public artifacts cannot contain confidentiality-marker phrases | Synthetic public artifact file | Scanner fails with confidentiality marker rule id |
| `test_blocks_private_source_field_assignments` | Private source terms are allowed only as schema field names, not assigned values | Runtime-generated assignment fixture | Scanner fails |
| `test_blocks_private_source_keys_regardless_of_value_shape` | #65 key-bypass class extends to imported #66 private source terms | Runtime-generated JSON fixtures with placeholder, safe string, null, array, and object values | Scanner fails for each imported private source term used as a key |
| `test_blocks_source_like_digest_keys_regardless_of_value_shape` | JSON key bypass promoted from #65 cannot recur | Runtime-generated JSON fixture | Scanner fails even when placeholder value is non-digest-shaped |
| `test_blocks_66_forbidden_request_keys_as_public_keys_or_assignments` | #66 forbidden request keys cannot become public-surface fields | Runtime-generated JSON and text fixtures | Scanner fails for every imported forbidden request key |
| `test_blocks_assigned_source_like_digest_values` | Assigned digest values remain blocked | Runtime-generated fixture | Scanner fails |
| `test_blocks_private_lookup_maps` | Private lookup maps cannot appear in public artifacts | Runtime-generated fixture | Scanner fails |
| `test_blocks_provider_stderr_and_log_sidecar_leaks` | Sidecars cannot expose local auth paths, file URIs, or provider trace paths | Synthetic sidecar file | Scanner fails with sensitive summary redacted |
| `test_allow_context_ids_are_closed` | Unknown allow-context IDs fail | Synthetic sentinel block | Scanner fails closed |
| `test_allow_context_requires_start_and_end_sentinels` | Malformed sentinel blocks fail | Missing-end and missing-start fixtures | Scanner fails closed |
| `test_allow_context_enforces_path_and_heading_constraints` | Contexts are not portable bypasses | Valid block moved to wrong path or heading | Scanner fails closed |
| `test_allow_context_enforces_token_classes_and_max_lines` | Contexts remain bounded and machine-parseable | Over-budget or wrong-token fixture | Scanner fails closed |
| `test_allow_context_rejects_nested_overlapping_and_eof_blocks` | Sentinel parser cannot create implicit bypass windows | Nested, overlapping, and EOF-malformed blocks | Scanner fails closed |
| `test_json_and_python_artifacts_do_not_use_html_comment_sentinels` | Strict JSON and Python self-scan surfaces avoid invalid comment sentinels | #68 contract JSON, snapshot JSON fixtures, scanner source, and tests | JSON/Python sentinel usage fails; neutral structured values and string fragments pass |
| `test_no_blanket_file_or_directory_exemptions` | Exemption model cannot bypass whole files | Contract fixture with whole-file exemption | Scanner fails |
| `test_review_artifact_selector_is_bounded` | Review artifact discovery is exact and non-recursive | Issue/phase/provider/round selector for local review directory | Only matching retained artifacts are selected |
| `test_review_artifact_selector_rejects_traversal_symlinks_and_unknown_provider` | Selector cannot escape the review directory or invent providers | Traversal path, symlink, and unknown provider inputs | Scanner fails closed |
| `test_same_stem_sidecars_are_scanned` | Adjacent provider outputs cannot bypass review scanning | Review artifact plus same-stem sidecar | Both files are scanned; sidecar leak fails |
| `test_sidecar_absence_semantics_are_explicit` | Missing sidecars are not silently confused with scanned sidecars | Required and optional sidecar selector modes | Required missing sidecar fails; optional missing sidecar records `none_found` |
| `test_issue_comment_snapshot_schema_is_closed` | Body evidence files have parseable metadata | Synthetic pre-post and refetched JSON snapshots | Extra/missing keys and invalid phases fail |
| `test_issue_comment_snapshot_pairing_is_enforced` | Posted/refetched evidence corresponds to the scanned pre-post body | Mismatched issue/comment/body hash/source-kind snapshots | Mismatch fails; planned-comment to issue-comment and issue-body to issue-body pairs pass |
| `test_issue_comment_body_files_scan_before_posting` | Comment body workflow has a pre-posting gate | Synthetic pre-post snapshot | Scanner fails unsafe body and passes safe body |
| `test_refetched_issue_comment_body_files_scan_after_posting` | Posted comment evidence is verified after refetch | Synthetic refetched snapshot | Scanner fails unsafe refetch and passes safe refetch |
| `test_parent_scan_public_path_cli_uses_new_scanner` | Existing parent CLI remains compatible | Parent validator with explicit scan path | Same pass/fail behavior through #68 scanner |
| `test_schema_validator_uses_new_scanner_for_public_paths` | #65 scanner integration is upgraded | #65 validator scan set | Schema validator delegates public-surface scanning to #68 library |
| `test_69_legal_scan_remains_sibling_gate` | #68 does not replace or weaken the implemented #69 gate | `.legal-deny-list.yaml`, #69 scanner, and workflow | #69 scan still passes independently and #68 does not apply its own allow contexts to the legal config |
| `test_workflow_preserves_69_legal_scan_step` | #68 workflow edits do not remove the legal/security hard gate | `.github/workflows/validate.yml` | Workflow still runs `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces` |
| `test_stock_ci_has_no_live_github_dependency` | Stock CI cannot depend on live issue/comment auth | `.github/workflows/validate.yml` | Workflow contains no `gh`, `GH_TOKEN`, GitHub API fetch, or comment-refetch dependency for #68 scanner |
| `test_plan_review_transition_updates_schema_without_approval` | Moving to plan-review updates parseable status but not implementation readiness | Schema row, README row, coordination row | #68 records `status:plan-review` and `implementation_ready=false`; no approval marker required |
| `test_plan_review_transition_rejects_lingering_blocked_draft_body` | Status transition cannot leave any current-state surface stale | Plan marked `status:plan-review` while header/body/README/coordination/schema still say `blocked-draft` or `BLOCKED-DRAFT` | Schema/status validation fails |
| `test_coordination_status_silencing_fixture_changes_before_validation` | The existing fallback test cannot become vacuous after row rewording | Temporary coordination fixture replacement | Test asserts replacement changed content before validation |
| `test_plan_review_evidence_comment_uses_existing_scanners_pre_implementation` | Label-time evidence comment is scanned before #68 scanner exists | Temporary repo-relative planned/refetched Markdown body files under `artifacts/ace-public-surface-self-scan/plan-review-evidence/` | Parent public scanner and #69 legal scan pass before label transition; scratch files are removed before clean-state closeout |
| `test_formal_provider_gate_requires_same_round_two_usable_no_major` | Subagent prep does not count as provider quorum | Provider review summary with Claude/Codex/Gemini states | Two usable no-MAJOR providers pass; any usable MAJOR or fewer than two usable providers blocks |
| `test_63_boundary_is_enforced` | #68 does not claim publication certification or maintained private deny-lists | Contract metadata | #63 ownership remains explicit; #68 scanner remains generic |
| `test_negative_fixtures_are_runtime_generated_or_sentinel_wrapped` | Tests do not commit raw self-blocking examples | Test source and fixture files | Scanner source/fixtures pass committed-file scan |
| `test_self_scan_covers_all_68_artifacts` | #68 cannot ship artifacts that fail its own scanner | #68 contract, scanner, CLI, tests, fixtures, workflow, plan, README, coordination, schema row, review artifacts, and selected sidecars | Every #68-created/modified artifact is scanned before CI wiring/closeout |
| `test_ci_invokes_public_surface_scanner` | CI uses the new scanner | `.github/workflows/validate.yml` | Workflow invokes #68 scanner over repo-local public/control-plane targets |

---

## Acceptance Criteria

- [ ] A standalone issue plan will exist for #68 and will not authorize implementation until adversarial plan review, user approval, `status:plan-approved`, and `.planning/plan-approved/68.md`.
- [ ] `config/ace-public-surface-self-scan-contract.json` will define closed deny classes, closed allow contexts, sensitive log redaction behavior, review artifact selectors, sidecar selectors, issue/comment body file handling, and sibling/owner boundaries.
- [ ] #68 will load and validate `config/ace-public-token-fixture-contract.json` as the authoritative #66 input for token grammar, fixture set IDs, forbidden request keys, private/source-like terms, placeholder values, placeholder mappings, and boundary owner issues; drift from #66 will fail closed.
- [ ] `scripts/validate_ace_public_surface_scan.py` will scan explicit public artifact paths and will fail closed on missing paths.
- [ ] The scanner will block raw host/source paths outside the fixed metadata-evidence shape, generic private-like identifiers, personal identifiers, confidentiality-marker phrases, assigned private source field terms, assigned source-like digest terms, private lookup maps, and provider stderr/log sidecar leaks.
- [ ] Imported private source terms, source-like provenance/digest terms, and #66 forbidden request keys will be rejected as public JSON keys regardless of placeholder value shape.
- [ ] Machine-parseable allow contexts will use closed context IDs, path constraints, optional heading constraints, token classes, exact start/end sentinels, maximum line budgets, and fail-closed malformed, nested, overlapping, and EOF block handling; strict JSON and Python artifacts will not rely on HTML-comment sentinels.
- [ ] No allow context will permit whole-file or whole-directory exemption.
- [ ] Review artifacts will be selected by exact issue/phase/provider/round selectors, same-stem sidecars will use a closed suffix set, and every selected artifact/sidecar will be scanned before citation as review/status evidence.
- [ ] Issue/comment body snapshots will use the closed JSON metadata schema, allowed phase/source transition table, and pairing rules before posted/refetched content is used as status evidence after implementation.
- [ ] Stock CI will not require live GitHub authentication; `.github/workflows/validate.yml` will contain no `gh`, `GH_TOKEN`, GitHub API, or comment-refetch dependency for #68.
- [ ] The parent coordination validator will preserve its existing `--scan-public-path` behavior while using the #68 scanner.
- [ ] The #65 schema validator will use the #68 scanner for public-surface scan paths after #68 implementation.
- [ ] The existing #69 legal/security gate will remain wired in CI, and #68 will not replace #69's `.legal-deny-list.yaml` allow-context semantics or require #69 contract changes.
- [ ] #63 will remain the owner of maintained private deny-lists, publication/comment certification, public-output canary behavior, and external publication exposure.
- [ ] Negative fixtures will be runtime-generated or sentinel-wrapped so committed public artifacts, tests, and review artifacts do not self-block.
- [ ] Before #68 moves to `status:plan-review`, the plan-review transition checklist will update the plan/header/body, schema row, README, and coordination row to `status:plan-review` with `implementation_ready=false`, scan and refetch the issue evidence comment using existing scanners, verify the pushed commit, and stop without approval marker creation.
- [ ] Any reusable method gap exposed by implementation will be promoted to the bound skills or filed as a follow-on issue before closeout.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_public_surface_scan.py --scan-public-path docs/plans/README.md` will pass after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_public_surface_scan` will pass after implementation.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py` and `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` will still pass after implementation.

---

## Adversarial Review Summary

| Reviewer | Verdict | Key findings |
|---|---|---|
| Codex subagent prep - dependency boundary r1/r2/r3 | APPROVE by r3 | Prep review forced #66 authoritative import, #69 sibling-gate wording, and provider selector closure before formal provider review. R3 artifact retained at `scripts/review/results/2026-07-02-plan-68-subagent-boundary-r3.md`. |
| Codex subagent prep - scanner contract r1/r2/r3 | APPROVE by r3 | Prep review forced private-source key denial, allow-context grammar, sidecar selectors, issue/comment snapshots, and full #68 self-scan coverage. R3 artifact retained at `scripts/review/results/2026-07-02-plan-68-subagent-scanner-r3.md`. |
| Codex subagent prep - workflow/status r1/r2/r3 | APPROVE by r3 | Prep review forced schema-row transition handling, scanned label-time evidence, and status-integrity test preservation. R3 artifact retained at `scripts/review/results/2026-07-02-plan-68-subagent-workflow-r3.md`. |
| Claude provider r1 | MINOR | Required r2 prep summary bookkeeping, #66 forbidden request key / fixture set import, JSON/Python sentinel clarification, pre-implementation scanner ordering, non-vacuous coordination replacement assertion, and removal of undefined snapshot phase. Patched before r2. |
| Codex provider r1 | MAJOR | Required existing scanners for pre-approval label evidence, plan header/body transition, formal same-round provider gate, source-kind transition table, and #66 forbidden request key import. Patched before r2. |
| Gemini provider r1 | UNAVAILABLE | CLI failed with unsupported-client/ineligible-tier authentication; no usable review signal. |
| Claude provider r2 | MAJOR | Required executable pre-approval evidence scanning, retained r3 prep artifacts for the cited APPROVE claims, and status-token normalization from `draft` to `blocked-draft`. Current draft patches these findings; provider r3 required. |
| Codex provider r2 | MAJOR | Required repo-relative classified scratch evidence paths for #69 legal scan compatibility and retained r3 prep artifacts for cited APPROVE claims. Current draft patches these findings; provider r3 required. |
| Gemini provider r2 | UNAVAILABLE | CLI failed with the same unsupported-client/ineligible-tier authentication condition; no usable review signal. |
| Claude provider r3 | APPROVE | Verified the r2 blockers are patched, the scratch evidence path is classified and executable with existing scanners, r3 prep artifacts are retained, current status is non-authorizing, and gate order is preserved. |
| Codex provider r3 | APPROVE | Verified the r2 blockers are patched, r3 prep artifacts are retained and mapped, #68 remains non-authorizing, the review summary is accurate, and #69 remains a sibling gate. |
| Gemini provider r3 | UNAVAILABLE | CLI failed with the same unsupported-client/ineligible-tier authentication condition; no usable review signal. |

**Overall result:** PLAN-APPROVED - formal provider r3 returned Claude APPROVE, Codex APPROVE, and Gemini UNAVAILABLE. The user approved this plan on 2026-07-02; implementation is authorized under TDD with `status:plan-approved` and `.planning/plan-approved/68.md`.

---

## Risks and Open Questions

- **Risk:** Over-broad patterns could block the scanner contract, tests, or legal/security config. Implementation will use closed allow contexts and runtime-generated fixtures rather than blanket exemptions.
- **Risk:** Under-broad patterns could create false confidence before #63 publication certification exists. #68 will remain generic control-plane scanning and will not replace #63.
- **Risk:** Review artifact selector drift could miss retained provider sidecars. Implementation will use exact issue/phase selectors plus same-stem sidecar discovery in known artifact directories.
- **Risk:** Live issue/comment refetch cannot run in stock CI. Implementation will make the body-file/refetched-body-file scan command executable and keep live fetching as an operator step.
- **Open:** Fresh review must confirm the #68 implementation plan consumes #66 and #69 boundaries instead of duplicating or weakening them.

---

## Complexity

**T3** - This is a security-sensitive reusable scanner contract that affects control-plane artifacts, validators, review evidence, issue/comment workflows, and the implemented sibling legal/security gate.
