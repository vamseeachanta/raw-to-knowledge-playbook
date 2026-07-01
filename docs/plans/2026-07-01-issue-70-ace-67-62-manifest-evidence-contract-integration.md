# Plan for #70: ACE #67/#62 Manifest Evidence Contract Integration

> **Status:** plan-approved
> **Complexity:** T3
> **Date:** 2026-07-01
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-07-01-plan-70-claude-r2.md | scripts/review/results/2026-07-01-plan-70-codex-r2.md | scripts/review/results/2026-07-01-plan-70-gemini-r2.md

---

## Resource Intelligence Summary

### Existing repo code/docs

- `config/ace-manifest-evidence-contract.json` will be the #62-owned contract that #70 consumes. It records `owner_issue=62`, `downstream_consumer_issue=70`, `blocked_operational_issue=67`, the six manifest source keys, the #70-facing operational evidence fields, `authorization_status` enum values, and the five closed drift pair IDs.
- `scripts/ace_manifest_freshness_operational.py` already exposes the validation surface #70 should import: `REQUEST_POINTER_FIELDS`, `validate_request_pointer(pointer)`, `validate_operational_evidence(record)`, and `validate_operational_evidence_file(path)`. It enforces a minimal pointer shape, closed operational evidence root fields, artifact-ref grammar, symlink/path containment, source issue, record id, validator command, exit status, snapshot IDs, source statuses, drift pair verdicts, reconciliation refs, and authorization status.
- `scripts/validate_ace_manifest_freshness.py` already wires the #62 contract validator and operational evidence validator behind `--evidence` and `--emit-evidence`.
- `tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json` is a public-safe compatible fixture that passes the #62 validator. #70 will use it only as controlled fixture evidence; operational allow-path tests must distinguish fixture refs from real operational artifact refs.
- `docs/case-studies/ace-manifest-freshness-drift-sentinel.md` documents that #70 will import the #62 reusable contract into operational sampling.
- `docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md` explicitly defers #67's first operational allow-path to #70. #67 will accept only metadata-only self-check fixture records in its own approval unit and will fail closed for downstream manifest-backed requests until #70 imports the #62 evidence contract.
- The #67 implementation artifacts do not exist yet: `config/ace-bounded-sampling-firewall-contract.json`, `scripts/ace_bounded_sampling_firewall.py`, `scripts/validate_ace_bounded_sampling_firewall.py`, and `tests/test_validate_ace_bounded_sampling_firewall.py` are missing in the current checkout.
- #70 must not be added to the #65 wave-0 split registry or the child wave ledger. It is a follow-on integration issue that consumes #62 and #67 artifacts.

### Related issues

- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) is `status:plan-approved` and has implemented the manifest freshness evidence contract. It remains blocked from closeout because the repo-local legal/security scan script from [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) is not available yet.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) is `status:plan-approved` with `.planning/plan-approved/67.md` present, but it has not implemented the bounded sampling firewall artifacts yet. #70 implementation must not start until #67 artifacts exist.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) is `status:plan-approved` and owns the repo-local legal/security scan gate needed for final closeout.
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) remains the approved parent epic. It authorizes coordination and planning only, not child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains the wave-0 umbrella. #70 will be a follow-on integration issue, not a new wave-0 split row in the #65 schema registry.

### Source inventory

- #70 will not read the ACE share or private source content during planning or CI validation.
- #70 will consume public-safe #62 evidence artifacts and synthetic fixtures only.
- Operational evidence pointers will carry only `source_issue`, `record_id`, and `evidence_artifact_ref`; request payloads must not copy the full #62 evidence body, command proof, snapshot map, drift verdicts, private sidecar material, source paths, raw digests, or exact private inventory counts.
- Operational sampling will require trusted repo-reviewed evidence, not request self-attestation. The implementation will distinguish test fixtures under `tests/fixtures/ace-manifest-freshness/` from operational artifacts under `artifacts/ace-manifest-freshness/`.

### Gaps identified

- No standalone #70 plan exists before this draft.
- No #67 bounded sampling firewall implementation exists to patch yet.
- #67 currently has no approval marker, so #70 implementation is dependency-blocked even if this plan later reaches `status:plan-review`.
- #62 validation can prove an artifact shape is valid, but #70 still needs a #67-facing trust boundary that prevents a request from satisfying freshness by supplying copied or forged evidence fields.
- #62 validation does not query GitHub issue comments. #70 needs a CI-safe trust anchor for `reviewed_commit`, validator command, and issue-comment evidence instead of treating any schema-valid JSON file under an allowed root as operationally trusted.
- No reviewed #62-produced operational evidence artifact exists under `artifacts/ace-manifest-freshness/` in the current checkout. If such an artifact is still absent when #70 reaches implementation, #70 must implement fail-closed wiring only and must not claim the operational allow-path is enabled.
- No #67 tests currently exercise a positive operational downstream allow-path using #62 `authorization_status=sampling_allowed`.
- No #67 tests currently prove `blocked_requires_reconciliation`, `blocked_unavailable`, malformed pointer, fixture-only pointer, mismatched record id, mismatched artifact ref, nonzero validator exit, and self-attested copied evidence all fail closed.

### Evidence

**Issue status**:

```text
$ gh issue view 70 --json number,title,state,labels,url
#70 OPEN ACE #67/#62 integration: ratify manifest evidence contract labels=strengthening,lane:codex,priority:high

$ gh issue view 67 --json number,title,state,labels,url
#67 OPEN ACE wave 0 split: bounded sampling firewall labels=strengthening,status:plan-review,lane:codex,priority:high

$ test -f .planning/plan-approved/67.md && echo APPROVAL_67_EXISTS || echo APPROVAL_67_MISSING
APPROVAL_67_MISSING
```

**File existence**:

```text
MISSING docs/plans/2026-07-01-issue-70-ace-67-62-manifest-evidence-contract-integration.md
MISSING scripts/review/results/2026-07-01-plan-70-claude-r1.md
MISSING scripts/review/results/2026-07-01-plan-70-codex-r1.md
MISSING scripts/review/results/2026-07-01-plan-70-gemini-r1.md
MISSING scripts/validate_ace_bounded_sampling_firewall.py
MISSING scripts/ace_bounded_sampling_firewall.py
MISSING config/ace-bounded-sampling-firewall-contract.json
MISSING tests/test_validate_ace_bounded_sampling_firewall.py
```

**Reproduction proofs**:

```text
$ PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_manifest_freshness.py --evidence tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json
PASS: ACE manifest freshness contract valid

$ PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py
PASS: ACE epic wave coordination valid

$ PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_schema_contract.py
PASS: ACE wave 0 schema contract valid
```

---

## Implementation Preconditions

#70 implementation will not start until all of these are true:

- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) has `status:plan-approved`.
- `.planning/plan-approved/67.md` exists.
- #67 has implemented `config/ace-bounded-sampling-firewall-contract.json`, `scripts/ace_bounded_sampling_firewall.py`, `scripts/validate_ace_bounded_sampling_firewall.py`, and `tests/test_validate_ace_bounded_sampling_firewall.py`.
- The #67 validator and tests pass before #70 changes them.
- The #62 manifest freshness validator still passes against `tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json`.
- At least one reviewed #62-produced operational evidence artifact exists under `artifacts/ace-manifest-freshness/`, or #70 implementation scope is explicitly reduced to fail-closed wiring with no positive operational allow-path.
- A trusted-evidence registry row exists for that operational artifact only after human review verifies the matching #62 issue evidence comment, reviewed commit, validator command, and exit status.

If #67's implemented artifact names or boundaries differ from the approved #67 plan, #70 must re-enter planning review before implementation instead of guessing an integration point.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-07-01-issue-70-ace-67-62-manifest-evidence-contract-integration.md` |
| Review artifact - Claude | `scripts/review/results/2026-07-01-plan-70-claude-r1.md` |
| Review artifact - Codex | `scripts/review/results/2026-07-01-plan-70-codex-r1.md` |
| Review artifact - Gemini | `scripts/review/results/2026-07-01-plan-70-gemini-r1.md` |
| #62 evidence contract consumed by #70 | `config/ace-manifest-evidence-contract.json` |
| #62 operational validator consumed by #70 | `scripts/ace_manifest_freshness_operational.py` |
| #62 validator CLI | `scripts/validate_ace_manifest_freshness.py` |
| #67 firewall contract to modify after #67 lands | `config/ace-bounded-sampling-firewall-contract.json` |
| #67 firewall library to modify after #67 lands | `scripts/ace_bounded_sampling_firewall.py` |
| #67 validator CLI to modify after #67 lands | `scripts/validate_ace_bounded_sampling_firewall.py` |
| #67 test suite to extend after #67 lands | `tests/test_validate_ace_bounded_sampling_firewall.py` |
| #67 fixture directory to extend after #67 lands | `tests/fixtures/ace-bounded-sampling-firewall/` |
| Operational evidence artifact directory | `artifacts/ace-manifest-freshness/` |
| #70 trusted evidence registry | `artifacts/ace-manifest-freshness/trusted-evidence-registry.json` |
| Plan index | `docs/plans/README.md` |
| Case study update if needed | `docs/case-studies/ace-manifest-freshness-drift-sentinel.md` |

---

## Deliverable

After approval and after #67 exists, #70 will integrate the #62 manifest freshness evidence contract into #67 so manifest-backed operational sampling requests can pass only when they carry a minimal pointer to trusted, repo-reviewed #62 evidence whose loaded artifact validates cleanly, matches a registry-pinned artifact integrity digest, and reports `authorization_status=sampling_allowed`. If no reviewed #62-produced operational evidence artifact exists, #70 will ship fail-closed wiring only; it will not claim operational sampling is enabled. All forged, malformed, mismatched, fixture-only, unavailable, reconciliation-required, unregistered, stale-digest, or self-attested evidence will fail closed.

---

## Proposed Integration Contract

The implementation will add a #67 request field for a minimal #62 evidence pointer:

```json
{
  "source_issue": 62,
  "record_id": "ace62-compatible-fixture",
  "evidence_artifact_ref": "artifacts/ace-manifest-freshness/example-operational-evidence.json"
}
```

The implementation will require:

- The request contains the minimal pointer only. #70 will import the #62 `REQUEST_POINTER_FIELDS` constant and map non-minimal pointer failures to `SELF_ATTESTED_62_EVIDENCE`; it will not maintain a divergent local field list.
- #70 will add a wrapper such as `load_and_validate_trusted_62_evidence(pointer)` that loads the artifact bytes once, parses that same byte string once, validates the parsed record with #62 `validate_operational_evidence(record)`, computes `artifact_integrity_digest` as SHA-256 over the exact raw artifact bytes, checks the trusted-evidence registry, and returns that same parsed record for authorization checks. No canonical JSON reserialization will be used for the digest; any byte-level artifact change stales the registry row.
- If implementation needs to call `validate_request_pointer(pointer)` for compatibility, it must not use that call as the authorization-time artifact read because the current #62 function internally opens the artifact and returns only errors. A parse-returning #62 helper requires a separate #62 follow-on unless it is added under an approved #70 implementation scope.
- The loaded artifact has `source_issue=62`, matching `record_id`, matching `evidence_artifact_ref`, valid `validator_ref`, exact `validator_env`, exact `validator_command`, `validator_exit_status=0`, valid `reviewed_commit`, exact six-source snapshot map, exact five-pair drift verdict map, and a valid authorization status.
- The pointer also appears in a #70-owned trusted-evidence registry that records `record_id`, `evidence_artifact_ref`, `artifact_integrity_digest`, `reviewed_commit`, `validator_ref`, `validator_command`, `validator_exit_status`, and a #62 issue evidence comment URL. CI will recompute the digest and validate against this repo-tracked registry; operators will populate or update the registry only after verifying the #62 issue evidence comment.
- The trusted-evidence registry is a human-reviewed allowlist, not a cryptographic authority by itself. Implementation closeout will require a reviewer checklist covering the issue-comment URL, reviewed commit, validator command, exit status, artifact digest, fixture-vs-operational root, and no private/source material. If this repo lacks branch protection or CODEOWNERS for the registry/artifact paths, #70 closeout must record that governance gap and remain blocked or file a follow-on governance issue before enabling operational sampling.
- Operational allow-path requests require `authorization_status=sampling_allowed`.
- `blocked_requires_reconciliation` and `blocked_unavailable` records will remain fail-closed with explicit machine-readable reasons.
- `tests/fixtures/ace-manifest-freshness/` refs are allowed only in controlled test modes. Operational request classes will require refs under `artifacts/ace-manifest-freshness/`.
- A schema-valid artifact that is absent from the trusted-evidence registry will fail closed as untrusted evidence.
- Any #62 contract/schema defect found during #70 implementation will be routed to a follow-on #62 issue instead of silently redefining the #62 evidence contract inside #70.

---

## Pseudocode

```text
validate_sampling_request(request):
    firewall_errors = validate_67_base_request(request)
    if firewall_errors:
        return fail_closed(firewall_errors)

    if request.target_wave_requires_manifest_snapshot:
        pointer = request.snapshot_evidence
        if pointer is missing:
            return fail_closed("MISSING_62_EVIDENCE_POINTER")
        if set(pointer) != ace_manifest_freshness_operational.REQUEST_POINTER_FIELDS:
            return fail_closed("SELF_ATTESTED_62_EVIDENCE")

        evidence_result = load_and_validate_trusted_62_evidence(pointer)
        if evidence_result.minimal_pointer_error:
            return fail_closed("SELF_ATTESTED_62_EVIDENCE")
        if evidence_result.errors:
            return fail_closed("INVALID_62_EVIDENCE_POINTER", evidence_result.errors)

        evidence = evidence_result.record
        if not evidence_result.registry_match:
            return fail_closed("UNTRUSTED_62_EVIDENCE")
        if request_class is operational and evidence ref is under tests/fixtures:
            return fail_closed("FIXTURE_62_EVIDENCE_NOT_OPERATIONAL")
        if evidence.authorization_status != "sampling_allowed":
            return fail_closed("62_EVIDENCE_NOT_AUTHORIZING")

    return metadata_only_sampling_authorized()
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `docs/plans/2026-07-01-issue-70-ace-67-62-manifest-evidence-contract-integration.md` | Record the #70 plan and dependency boundary |
| Modify | `docs/plans/README.md` | Index the #70 plan |
| Modify after #67 lands | `config/ace-bounded-sampling-firewall-contract.json` | Add #62 evidence pointer and operational evidence authorization rules |
| Modify after #67 lands | `scripts/ace_bounded_sampling_firewall.py` | Import #62 pointer validation and apply #67 operational allow/fail-closed decisions |
| Modify after #67 lands | `scripts/validate_ace_bounded_sampling_firewall.py` | Expose validation and public-scan coverage for the #70 integration |
| Modify after #67 lands | `tests/test_validate_ace_bounded_sampling_firewall.py` | Add #70 positive and negative operational evidence tests |
| Add after #67 lands | `tests/fixtures/ace-bounded-sampling-firewall/*.json` | Add safe sampling request fixtures that point at #62 evidence |
| Add when available | `artifacts/ace-manifest-freshness/*.json` | Store reviewed operational evidence artifacts for non-fixture operational tests |
| Add after #67 lands | `artifacts/ace-manifest-freshness/trusted-evidence-registry.json` | CI-safe trust anchor tying #62 artifact refs to reviewed commit, validator command, and issue-comment evidence |
| Modify if needed | `docs/case-studies/ace-manifest-freshness-drift-sentinel.md` | Document #70 import semantics and fail-closed outcomes |
| Modify after #67 lands | `.github/workflows/validate.yml` | Run the extended #67/#70 validator and unit-test commands explicitly |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_70_preconditions_detect_missing_67_artifacts` | Implementation stops when #67 artifacts are absent | Current checkout before #67 implementation | Explicit dependency-blocked state |
| `test_imports_62_pointer_fields_and_operational_validator` | #67/#70 uses #62-owned pointer and evidence contracts instead of redefining evidence shape | Monkeypatched/import-inspected #67 validator | Imports `REQUEST_POINTER_FIELDS` and `validate_operational_evidence` from `ace_manifest_freshness_operational` |
| `test_valid_operational_62_evidence_allows_downstream_sampling` | First positive downstream allow-path | Valid #67 request pointing at `artifacts/ace-manifest-freshness/*.json` with `authorization_status=sampling_allowed` | Metadata-only sampling authorization result |
| `test_schema_valid_but_untrusted_62_evidence_fails_closed` | Shape validity alone is not enough | Valid artifact absent from trusted registry | `UNTRUSTED_62_EVIDENCE` |
| `test_trusted_registry_matches_artifact_and_issue_comment_metadata` | Trust registry pins reviewed evidence | Registry row, artifact, reviewed commit, validator command, and #62 issue evidence comment URL | Exact match required |
| `test_trusted_registry_rejects_stale_commit_or_command` | Stale or different #62 evidence cannot authorize | Registry row with changed commit or command | Fail closed |
| `test_trusted_registry_rejects_tampered_artifact_digest` | A mutated artifact cannot keep authorization by preserving metadata | Registry row with old digest and modified artifact content | Fail closed with stale digest |
| `test_artifact_integrity_digest_uses_raw_bytes` | Digest algorithm is unambiguous and detects byte-level changes | Same JSON value with different whitespace and ordering | Raw-byte digest changes and stale registry fails |
| `test_load_and_validate_trusted_evidence_uses_single_authorization_parse` | Validation and authorization use the same parsed record | Instrumented #70 artifact loader | One authorization-time byte read and parse supplies validation, digest, registry, and status checks |
| `test_fixture_62_evidence_cannot_authorize_operational_sampling` | Public fixture evidence cannot be mistaken for operational evidence | Operational request pointing at `tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json` | Fail closed with fixture-not-operational reason |
| `test_shape_fixture_can_exercise_validator_without_operational_authorization` | Unit tests can still use controlled fixtures safely | Test-mode request pointing at fixture ref | Validator exercises import path but does not authorize operational sampling |
| `test_missing_62_pointer_fails_closed` | Downstream manifest-backed waves still require #62 evidence | Request omits `snapshot_evidence` | `MISSING_62_EVIDENCE_POINTER` |
| `test_self_attested_62_evidence_body_fails_closed` | Requests cannot satisfy freshness by copying evidence fields | Request includes `validator_command`, snapshots, or drift verdicts inline | `SELF_ATTESTED_62_EVIDENCE` |
| `test_forged_record_id_fails_closed` | Pointer record id must match loaded artifact | Pointer record id differs from artifact | #62 pointer validation error |
| `test_mismatched_artifact_ref_fails_closed` | Pointer artifact ref must match loaded artifact | Pointer ref differs from artifact `evidence_artifact_ref` | #62 pointer validation error |
| `test_invalid_artifact_path_fails_closed` | Path traversal, absolute paths, wrong roots, and symlinks fail | Bad refs and symlink fixture | #62 path validation error |
| `test_nonzero_validator_exit_fails_closed` | Diagnostic evidence cannot authorize sampling | Artifact with `validator_exit_status != 0` | Fail closed |
| `test_blocked_requires_reconciliation_fails_closed` | Warning/blocker drift cannot authorize sampling before reconciliation | Artifact with warning or blocker pair | Fail closed with reconciliation-required reason |
| `test_blocked_unavailable_fails_closed` | Unavailable evidence cannot authorize sampling | Artifact with unavailable pair | Fail closed with unavailable reason |
| `test_reconciliation_refs_are_not_authorization` | A reconciliation link alone cannot bypass drift status | Artifact has reconciliation refs but non-sampling authorization status | Fail closed |
| `test_manifest_source_set_stays_six_key_62_contract` | #70 does not expand or shrink the #62 source universe | Contract and request source maps | Exact six source keys required |
| `test_request_target_wave_must_require_manifest_snapshot` | #70 only opens the downstream manifest-backed allow-path | Non-ingestion/control-plane targets | Fail closed or non-target result |
| `test_public_scan_covers_70_artifacts` | Plan, review artifacts, fixtures, and any #70 evidence artifacts are scanned | Derived #70 public path set | Parent public scanner passes |
| `test_ci_runs_70_extended_firewall_tests` | CI enforces the integration | Workflow and test command | Workflow runs `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_bounded_sampling_firewall.py` and `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_bounded_sampling_firewall` |
| `test_70_public_scan_manifest_is_exact` | #70 public artifacts cannot escape scan coverage | Derived #70 path set | Appends every #70 public path as an explicit `--scan-public-path` argument to `scripts/validate_ace_epic_wave_coordination.py`, including this plan, README row, plan-70 review artifacts, #67/#70 config/scripts/tests/fixtures, `artifacts/ace-manifest-freshness/*.json`, trusted registry, case study, and workflow |

---

## Acceptance Criteria

- [ ] A standalone #70 plan will exist under `docs/plans/`, be indexed in `docs/plans/README.md`, and pass adversarial plan review before implementation.
- [ ] #70 implementation will remain blocked until #67 is `status:plan-approved`, `.planning/plan-approved/67.md` exists, and #67 bounded sampling firewall artifacts exist.
- [ ] #67/#70 will import #62-owned pointer/evidence validation constants and functions from `scripts/ace_manifest_freshness_operational.py` instead of redefining #62 evidence shape.
- [ ] Operational downstream sampling will require a minimal #62 pointer with exactly `source_issue`, `record_id`, and `evidence_artifact_ref`.
- [ ] Sampling requests that copy full #62 evidence fields will fail closed as self-attestation.
- [ ] Valid operational requests will load the referenced artifact and require the artifact to validate under #62 rules.
- [ ] Schema-valid #62 artifacts will not authorize sampling unless a #70-owned trusted-evidence registry records the same artifact ref, record id, artifact integrity digest, reviewed commit, validator command, exit status, and #62 issue evidence comment URL.
- [ ] Operational allow-path requests will require `authorization_status=sampling_allowed`.
- [ ] Stale, unregistered, tampered-digest, or command/commit-mismatched #62 evidence will fail closed as untrusted even if the artifact shape validates.
- [ ] `blocked_requires_reconciliation`, `blocked_unavailable`, malformed, mismatched, fixture-only, nonzero-exit, path-escape, and symlink evidence will fail closed.
- [ ] #70 will distinguish controlled test fixtures from operational artifacts; fixture refs cannot authorize operational sampling.
- [ ] #70 will not modify the #62 contract unless a separate #62 follow-on issue is planned and approved.
- [ ] #70 will not implement #67's base firewall if #67 has not landed; it will only integrate #62 evidence into the approved #67 surface.
- [ ] Public scans will cover the #70 plan, review artifacts, fixtures, and any #70-created public evidence artifacts.
- [ ] CI will run the extended #67/#70 validator and tests after implementation using explicit workflow commands for `scripts/validate_ace_bounded_sampling_firewall.py` and `tests.test_validate_ace_bounded_sampling_firewall`.
- [ ] The #70 public-scan path set will append this plan, README row, plan-70 review artifacts, #67/#70 config/scripts/tests/fixtures, `artifacts/ace-manifest-freshness/*.json`, the trusted registry, case study updates, and workflow edits as explicit `--scan-public-path` arguments to the parent scanner.
- [ ] Enabling operational sampling will require either branch protection/CODEOWNERS coverage for the trusted registry and operational evidence artifact paths or a filed governance blocker documenting the missing write-control boundary.
- [ ] If the approved [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) legal/security scan artifact is unavailable at closeout, #70 closeout will remain blocked and the issue comment will record the missing legal/security gate. If [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) lands under the currently planned `scripts/legal/legal-sanity-scan.sh` path, that command will be used; otherwise #70 will follow the approved #69 artifact path.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude | MINOR | r2 found only clarification issues; raw-byte digest, one authorization-time parse, provisional #69 artifact path, and explicit parent scanner mechanics were patched. |
| Codex | APPROVE | r2 returned no findings after the r1 patch. |
| Gemini | UNAVAILABLE | r1/r2 CLI attempts failed before review with `IneligibleTierError`. |
| Claude r1 | MAJOR | Operational provenance was path-only; trust registry needed human-reviewed allowlist semantics; artifact double-load and duplicate minimal-pointer checks needed tightening. |
| Codex r1 | MAJOR | Registry needed artifact digest pinning; operational allow-path needed a reviewed #62 artifact precondition; CI/public-scan commands needed to be mandatory and exact. |
| Claude r2 | MINOR | Requested clarification of raw-byte artifact digest, one authorization-time parse, provisional #69 scan artifact path, and explicit parent scanner `--scan-public-path` mechanics. |
| Codex r2 | APPROVE | No findings after r1 patch. |

**Overall result:** no usable MAJOR after r2. The user approved this plan on 2026-07-01, and `.planning/plan-approved/70.md` records the approval marker. Implementation remains sequenced after #67 implementation and the #62 operational evidence preconditions.

---

## Risks and Open Questions

- **Risk:** #70 may be approved before #67 implementation exists. The plan will make implementation preconditions explicit and require re-review if #67 lands with different artifact names or integration boundaries.
- **Risk:** A request could self-attest by copying #62 evidence fields into the request. The implementation will accept only a minimal pointer and will load the referenced artifact for authoritative validation.
- **Risk:** A controlled fixture could accidentally become an operational allow-path. The implementation will separate fixture/test modes from operational artifact roots.
- **Risk:** #62's validator can prove evidence shape but not business authorization by itself. #70 will add #67-specific target-wave, request-class, route/store, and operational-root checks around the #62 validator result.
- **Risk:** Live GitHub issue comments are not available in stock CI. The implementation will use a repo-tracked trusted-evidence registry as the CI-safe trust boundary and require issue-comment URL evidence in that registry; any live-GitHub verification happens before updating the registry and in closeout evidence, not during stock CI.
- **Open:** If #67's eventual implementation chooses names or modules that differ from its approved plan, #70 will need a plan patch and fresh review before coding.

---

## Complexity

**T3** - this is a cross-issue operational authorization gate that consumes #62 evidence, patches the future #67 firewall, changes the first downstream sampling allow-path, and must preserve fail-closed public/private and legal/security boundaries.
