# Plan for #72: Generalize Public-Surface Review Selector and Snapshot Modes Beyond Issue 68

> **Status:** plan-approved
> **Complexity:** T2
> **Date:** 2026-07-02
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-07-02-plan-72-claude-r1.md | scripts/review/results/2026-07-02-plan-72-codex-r1.md | scripts/review/results/2026-07-02-plan-72-gemini-r1.md | scripts/review/results/2026-07-02-plan-72-claude-r2.md | scripts/review/results/2026-07-02-plan-72-codex-r2.md | scripts/review/results/2026-07-02-plan-72-gemini-r2.md

---

## Resource Intelligence Summary

### Existing repo code/docs

- Source: `scripts/ace_public_surface_review.py`
  - Finding: the review artifact selector currently rejects every `review_issue` except `68`, and the snapshot validator currently rejects every snapshot whose `issue_number` is not `68`. URL validation also builds GitHub issue/comment URLs with a hard-coded issue number.
- Source: `scripts/ace_public_surface_contract.py`
  - Finding: `REVIEW_ARTIFACT_RE` currently embeds `68` in the review artifact filename grammar. `EXPECTED_PROVIDERS`, `REVIEW_PHASES`, `ROUND_RE`, `SNAPSHOT_KEYS`, and sidecar suffixes are already closed sets and should remain closed.
- Source: `config/ace-public-surface-self-scan-contract.json`
  - Finding: `review_artifact_selector.issue` is currently a single integer value of `68`; the contract has no closed list of additional contract-authorized issue numbers. The allow-context path lists are also still scoped to `*issue-68*` and `*plan-68*`.
- Source: `scripts/ace_public_surface_rules.py`
  - Finding: `_validate_allow_path` currently accepts schema-term allow contexts only for `issue-68` plan/review paths and review-forensics allow contexts only for `plan-68` review artifacts.
- Source: `scripts/validate_ace_public_surface_scan.py`
  - Finding: the CLI already accepts `--review-issue`, `--review-phase`, `--review-provider`, `--review-round`, `--snapshot`, and `--snapshot-pair`; the implementation will keep this CLI shape and change validation semantics underneath it.
- Source: `tests/test_validate_ace_public_surface_review.py`, `tests/test_validate_ace_public_surface_snapshot_urls.py`, and `tests/test_validate_ace_public_surface_contract.py`
  - Finding: existing tests prove #68-specific selection, sidecar scanning, snapshot shape checks, URL pinning, and provider closure. #72 will add failing tests for contract-authorized non-68 issue numbers without weakening unknown-issue rejection.

### Related issues

- Source: [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)
  - Finding: #68 implemented the public-surface self-scan control plane and intentionally pinned selector/snapshot modes to #68 during closeout.
- Source: [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) r28/r30 review artifacts
  - Finding: #51 can use the scanner today only through generic `--scan-public-path` mode. Selector/snapshot support for #51 is explicitly deferred to [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72).
- Source: [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69)
  - Finding: the repo-local legal/security gate remains a sibling gate and must not be weakened by this issue.
- Source: [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63)
  - Finding: maintained publication canaries, maintained private deny-lists, and external publication certification remain out of scope for #72.

### Source inventory

- #72 will inspect repo-local public artifacts only: the #68 scanner contract, scanner modules, validator CLI, unit tests, retained review artifacts, and operator-supplied snapshot JSON files.
- #72 will not read private ACE corpus content, run live GitHub fetches in stock CI, or authorize any `ACE_SHARE_ROOT` traversal.
- Snapshot fixtures will use synthetic bodies and GitHub issue/comment URLs. Review artifact fixtures will be temporary or synthetic files under the bounded review artifact root.
- The initial contract-authorized issue-number set will be exact: `50`, `51`, `52`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, and `72`. GitHub number `64` is an open codex planning PR/meta item, not a canonical docs/plans ACE wave/split/follow-on plan row with retained review artifacts, so it remains excluded until a later reviewed config change adds it.
- Associated reusable skill group: `public-private-routing`, `adversarial-verify-loop`, and `verify-batch`. If implementation exposes a reusable review/snapshot hygiene rule, #72 will update the relevant skill doc or file a follow-on issue before closeout.

### Gaps identified

- The scanner needs a closed contract-authorized issue-number list, not a free-form selector.
- The review artifact filename parser needs to parse an issue number from the filename and compare it against the requested issue instead of embedding issue `68` in the regex.
- Snapshot validation needs to accept only contract-authorized issue numbers and build URL expectations from each snapshot's issue number.
- Snapshot pairs need to keep enforcing equal issue numbers and equal body hashes across pre-post and post-refetch records.
- Allow-context path validation needs to move from issue-68/plan-68 string checks to the same closed issue-number contract, otherwise non-68 review artifacts that need forensic allow contexts will fail or invite unsafe exemptions.
- Tests need to prove both positive non-68 behavior and fail-closed unknown issue behavior.

### Evidence

**Issue status** (verified 2026-07-02):

```text
#72 OPEN labels=strengthening,lane:claude,priority:medium
#68 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high
#51 OPEN labels=strengthening,lane:claude,priority:high
```

**File existence** (verified 2026-07-02):

```text
EXISTS config/ace-public-surface-self-scan-contract.json
EXISTS scripts/ace_public_surface_contract.py
EXISTS scripts/ace_public_surface_review.py
EXISTS scripts/ace_public_surface_rules.py
EXISTS scripts/ace_public_surface_scan.py
EXISTS scripts/validate_ace_public_surface_scan.py
EXISTS tests/ace_public_surface_test_helpers.py
EXISTS tests/test_validate_ace_public_surface_contract.py
EXISTS tests/test_validate_ace_public_surface_review.py
EXISTS tests/test_validate_ace_public_surface_rules.py
EXISTS tests/test_validate_ace_public_surface_snapshot_urls.py
EXISTS tests/test_validate_ace_public_surface_scan.py
EXISTS docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md
NEW docs/plans/2026-07-02-issue-72-generalize-public-surface-review-selector-snapshot-modes.md
EXISTS .planning/plan-approved/72.md after user approval
```

**Reproduction proofs** (verified 2026-07-02):

```text
$ uv run python scripts/validate_ace_public_surface_scan.py --review-issue 72 --review-phase plan --review-provider claude --review-round r1
DENY  review-issue: #68 scanner accepts only issue 68 selectors

FAIL: 1 error(s)
```

```text
$ uv run python - <<'PY'
import hashlib, json, tempfile
from pathlib import Path
from scripts.ace_public_surface_review import validate_issue_comment_snapshot_file
body = "safe body\n"
payload = {
    "schema_version": "1.0.0",
    "issue_number": 72,
    "comment_id": None,
    "url": "https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72",
    "source_kind": "planned_comment",
    "phase": "pre_post",
    "fetched_at": "2026-07-02T00:00:00Z",
    "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
    "body": body,
}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
    json.dump(payload, handle)
    path = Path(handle.name)
try:
    for error in validate_issue_comment_snapshot_file(path):
        print(error.split(" at ", 1)[0])
finally:
    path.unlink()
PY
snapshot-issue: issue_number must be 68
snapshot-url: issue_body URL mismatch
```

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-07-02-issue-72-generalize-public-surface-review-selector-snapshot-modes.md` |
| Plan index | `docs/plans/README.md` |
| Scanner contract | `config/ace-public-surface-self-scan-contract.json` |
| Scanner contract constants | `scripts/ace_public_surface_contract.py` |
| Review/snapshot scanner logic | `scripts/ace_public_surface_review.py` |
| Public-surface rule engine | `scripts/ace_public_surface_rules.py` |
| Scanner facade | `scripts/ace_public_surface_scan.py` |
| Scanner CLI | `scripts/validate_ace_public_surface_scan.py` |
| Test helpers | `tests/ace_public_surface_test_helpers.py` |
| Contract tests | `tests/test_validate_ace_public_surface_contract.py` |
| Review selector and snapshot tests | `tests/test_validate_ace_public_surface_review.py` |
| Public-surface rules tests | `tests/test_validate_ace_public_surface_rules.py` |
| Snapshot URL tests | `tests/test_validate_ace_public_surface_snapshot_urls.py` |
| Aggregate scanner test module | `tests/test_validate_ace_public_surface_scan.py` |
| Review artifact - Claude r1 | `scripts/review/results/2026-07-02-plan-72-claude-r1.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-07-02-plan-72-codex-r1.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-07-02-plan-72-gemini-r1.md` |
| Review artifact - Claude r2 | `scripts/review/results/2026-07-02-plan-72-claude-r2.md` |
| Review artifact - Codex r2 | `scripts/review/results/2026-07-02-plan-72-codex-r2.md` |
| Review artifact - Gemini r2 | `scripts/review/results/2026-07-02-plan-72-gemini-r2.md` |

---

## Deliverable

After approval and implementation, the #68 public-surface scanner will support review artifact selection and issue/comment snapshot validation for a closed contract-authorized set of issue numbers beyond #68, while preserving exact provider names, bounded review roots, sidecar scanning, snapshot pairing, and fail-closed unknown issue behavior.

---

## Pseudocode

```text
load config/ace-public-surface-self-scan-contract.json
validate review_artifact_selector:
  root remains scripts/review/results
  phase_enum remains closed
  provider_enum remains closed
  round_pattern remains r[0-9]+
  allowed_issue_numbers equals [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69, 70, 71, 72]
  stale singular issue key is rejected if it remains beside allowed_issue_numbers
  unknown or non-integer issue selectors fail closed

compile review artifact filename regex:
  parse date, phase, issue, provider, and round from file name
  do not embed a single issue number in the regex
  require parsed issue == requested review_issue
  require requested review_issue in allowed_issue_numbers
  require parsed phase/provider/round equal requested selector fields
  require provider in EXPECTED_PROVIDERS
  require round matches ROUND_RE

select review artifacts:
  bound review_root to scripts/review/results
  reject custom roots and symlink roots
  use exact glob pattern for the requested issue/phase/provider/round
  reject symlink artifacts
  include only closed same-stem sidecar suffixes when requested
  scan every selected artifact and sidecar

validate allow context paths:
  schema-term-policy-prose remains limited to markdown plan/review paths
  review-artifact-forensics remains limited to scripts/review/results paths
  path issue number must parse from issue-<n> or plan-<n>
  parsed issue number must be in allowed_issue_numbers
  issue 64 and unknown future issues fail closed
  whole-file, whole-directory, extension, or rule-class exemptions remain forbidden

validate snapshot record:
  require closed top-level keys
  require semver schema_version
  require source_kind and phase enums
  require issue_number in allowed_issue_numbers
  validate URL against snapshot issue_number
  for planned_comment and issue_body:
    require https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/<issue>
    reject fragments, params, and queries
  for issue_comment post_refetch:
    require comment_id
    require matching issue URL plus #issuecomment-<comment_id>
  require body_sha256 to match body
  scan snapshot body with the existing public-surface rules

validate snapshot pair:
  validate both records independently
  require pre_post -> post_refetch phase transition
  require allowed source_kind pairing
  require equal issue_number across both records
  require equal body_sha256 across both records

verify:
  run focused red tests first
  implement the smallest contract/code changes
  run public-surface unit tests, aggregate validator tests, legal scan, and public-surface scans over changed public artifacts
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Modify | `config/ace-public-surface-self-scan-contract.json` | Replace the singular `review_artifact_selector.issue` key with exact `allowed_issue_numbers`, and update allow-context path patterns so they remain issue-bounded through the same closed set. |
| Modify | `scripts/ace_public_surface_contract.py` | Validate the closed issue-number contract, reject stale singular `issue`, and update review artifact parsing constants so issue number is parsed and compared instead of hard-coded to `68`. |
| Modify | `scripts/ace_public_surface_review.py` | Accept contract-authorized non-68 selectors and snapshots; keep unknown issue numbers, mismatched URLs, unknown providers, custom roots, symlinks, bad sidecars, and bad snapshot pairs fail-closed. |
| Modify | `scripts/ace_public_surface_rules.py` | Generalize allow-context path validation from literal issue-68/plan-68 checks to parsed contract-authorized issue numbers while preserving context type/path restrictions. |
| Modify | `scripts/validate_ace_public_surface_scan.py` | Keep the CLI stable and adjust help/error wording only if needed to describe contract-authorized issue selectors. |
| Modify | `tests/ace_public_surface_test_helpers.py` | Let helper records generate matching URLs for issue numbers beyond #68 without changing the default #68 behavior. |
| Modify | `tests/test_validate_ace_public_surface_contract.py` | Add contract tests for the closed allowed issue set and retention of provider/phase/sidecar closure. |
| Modify | `tests/test_validate_ace_public_surface_review.py` | Add red tests for contract-authorized non-68 review artifact selection, unknown issue rejection, exact requested issue matching, and sidecar scanning on non-68 artifacts. |
| Modify | `tests/test_validate_ace_public_surface_rules.py` | Add allow-context path tests for contract-authorized non-68 issue numbers and unlisted issue rejection beside the existing issue-68 allow-context regression tests. |
| Modify | `tests/test_validate_ace_public_surface_snapshot_urls.py` | Add red tests for non-68 snapshot URL acceptance, issue/URL mismatch rejection, and unlisted issue rejection. |
| Modify | `tests/test_validate_ace_public_surface_scan.py` | Preserve aggregate import coverage after the focused test modules change. |
| Conditional modify or follow-on | `skills/public-private-routing/SKILL.md` | Promote a reusable public issue/comment snapshot hygiene rule if implementation reveals one. |
| Conditional modify or follow-on | `skills/adversarial-verify-loop/SKILL.md` | Promote a reusable review artifact selector/sidecar hygiene rule if implementation reveals one. |
| Conditional modify or follow-on | `skills/verify-batch/SKILL.md` | Promote any batch-review public-surface sidecar rule if implementation reveals one. |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_contract_declares_closed_allowed_issue_numbers` | The scanner contract defines an explicit issue enum rather than a free-form issue selector | Contract JSON with the current ACE set `50`-`63` plus `65`-`72` | Validation passes only when the set is integer-only, exactly matches the reviewed list, includes `68`, excludes `64`, and has no blanket wildcard |
| `test_contract_rejects_stale_singular_issue_key` | The old #68-only contract field cannot coexist with the new enum | Contract JSON containing both `issue` and `allowed_issue_numbers` under `review_artifact_selector` | Validation fails with stale-key error |
| `test_review_artifact_selector_accepts_contract_authorized_non_68_issue` | Review selector supports an allowed issue beyond #68 | Temporary `2099-...-plan-72-claude-r99.md` artifact and selector `issue=72` | Selected artifact passes selector validation |
| `test_review_artifact_selector_rejects_unlisted_issue` | Generalization does not become unbounded | Selector `issue=999` or another unlisted issue | Selector fails before artifact selection |
| `test_review_artifact_selector_matches_requested_issue_exactly` | Selector cannot return a same-provider/round artifact for a different issue | Temporary #68 and #72 artifacts with same phase/provider/round | Selecting #72 returns only the #72 path |
| `test_review_artifact_regex_parses_issue_number` | Filename regex no longer embeds `68` | Review artifact names for #68 and #72 | Parsed issue is compared to the requested selector |
| `test_legacy_roundless_and_disagreement_artifacts_stay_unselectable` | Generalization does not make old non-conforming review files selectable | Existing-style `plan-50-claude.md`, `plan-66-codex.md`, and `plan-51-disagreement-r16.md` names | Selector ignores or rejects them even though those issue numbers are contract-authorized |
| `test_review_artifact_selector_keeps_provider_enum_closed` | Provider generalization does not reopen ad hoc provider names | Unknown provider selector | Fails with provider error |
| `test_non_68_sidecars_are_scanned` | Sidecar logic applies to contract-authorized non-68 artifacts | #72 review artifact with same-stem sidecar containing a synthetic denied trace | Validation reports the sidecar denial |
| `test_allow_context_paths_accept_contract_authorized_issue_numbers` | Allow-context path gating supports non-68 plans/review artifacts without blanket exemptions | #72 plan markdown and `plan-72` review artifact paths with valid sentinels in `tests/test_validate_ace_public_surface_rules.py` | Allow contexts pass only in the correct path/context shape |
| `test_allow_context_paths_reject_unlisted_issue_numbers` | Issue 64 and unknown future issues remain fail-closed for allow contexts | `issue-64`, `plan-64`, and `issue-999` paths with otherwise valid sentinels in `tests/test_validate_ace_public_surface_rules.py` | Validation fails with allow-context path error |
| `test_snapshot_record_accepts_contract_authorized_non_68_issue` | Snapshot validation supports an allowed issue beyond #68 | Synthetic #72 planned-comment and refetched-comment snapshots with matching URLs | Snapshot validation passes when body is safe |
| `test_snapshot_record_rejects_unlisted_issue` | Snapshot issue enum remains fail-closed | Synthetic snapshot for unlisted issue with matching URL | Validation fails with issue error |
| `test_snapshot_url_must_match_snapshot_issue_number` | URL validation is derived from the snapshot issue, not from a constant | Snapshot claims #72 with #68 URL, and snapshot claims #68 with #72 URL | Both fail with URL mismatch |
| `test_snapshot_pair_allows_matching_non_68_issue` | Pairing works for allowed non-68 issue numbers | #72 planned-comment pre-post and #72 issue-comment post-refetch with same body hash | Pair validation passes |
| `test_snapshot_pair_rejects_cross_issue_pair` | Pairing cannot combine snapshots from different issues | #68 pre-post and #72 post-refetch snapshots | Pair validation fails with issue mismatch |
| `test_cli_review_and_snapshot_accept_contract_authorized_issue` | CLI path uses the same contract-authorized issue rules as the library | CLI args for #72 selector and snapshot file | `collect_errors` returns no selector/snapshot errors for safe inputs |
| `test_cli_review_requires_complete_selector_tuple` | Existing all-or-none selector tuple behavior remains intact | Partial selector args | Validation fails with tuple error |
| `test_existing_68_selector_and_snapshot_tests_still_pass` | Backward compatibility for #68 remains intact | Existing #68 tests | Current #68 workflows pass unchanged |

---

## Acceptance Criteria

- [ ] #72 will not authorize implementation until adversarial plan review, explicit user approval, `status:plan-approved`, and `.planning/plan-approved/72.md` exist.
- [ ] The scanner contract will define the closed contract-authorized issue-number set as `50`, `51`, `52`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, and `72`; issue `64` and unknown future issues will fail closed until a later reviewed config change adds them.
- [ ] The old singular `review_artifact_selector.issue` contract key will be removed or rejected; `allowed_issue_numbers` will be the only issue-number authority for review and snapshot modes.
- [ ] `--review-issue` will accept only contract-authorized issue numbers and will reject unknown issue numbers before selecting artifacts.
- [ ] Review artifact filename parsing will support contract-authorized non-68 issue numbers while still requiring exact issue/phase/provider/round matches.
- [ ] Provider names, phases, rounds, review root, and sidecar suffixes will remain closed and fail-closed.
- [ ] Allow-context path validation will support contract-authorized non-68 plan/review artifact paths and will reject issue `64`, unlisted future issues, wrong path classes, and blanket exemptions.
- [ ] Snapshot records will accept contract-authorized non-68 issue numbers only when the GitHub issue/comment URL matches that same issue number.
- [ ] Snapshot records will reject unlisted issues, issue/URL mismatches, missing comment IDs for refetched comments, bad body hashes, bad phases, bad source kinds, and extra/missing keys.
- [ ] Snapshot pairs will require valid individual records, allowed source-kind transitions, matching issue numbers, and matching body hashes.
- [ ] Existing #68 selector, sidecar, snapshot, CI, and unit-test behavior will keep passing.
- [ ] The implementation will not add live GitHub fetching or `GH_TOKEN` requirements to stock CI.
- [ ] Public-surface and legal/security scans will pass over changed docs, tests, scanner modules, config, review artifacts, and any retained sidecars.
- [ ] Any reusable method gap found during review or implementation will be promoted into the associated skill group or filed as a follow-on issue before closeout.
- [ ] Verification after implementation will include:
  - `uv run python -m unittest tests.test_validate_ace_public_surface_scan`
  - `uv run python scripts/validate_ace_public_surface_scan.py --scan-public-path docs/plans/2026-07-02-issue-72-generalize-public-surface-review-selector-snapshot-modes.md --scan-public-path docs/plans/README.md --scan-public-path config/ace-public-surface-self-scan-contract.json --scan-public-path scripts/ace_public_surface_contract.py --scan-public-path scripts/ace_public_surface_review.py --scan-public-path scripts/ace_public_surface_rules.py --scan-public-path scripts/ace_public_surface_scan.py --scan-public-path scripts/validate_ace_public_surface_scan.py --scan-public-path tests/ace_public_surface_test_helpers.py --scan-public-path tests/test_validate_ace_public_surface_contract.py --scan-public-path tests/test_validate_ace_public_surface_review.py --scan-public-path tests/test_validate_ace_public_surface_rules.py --scan-public-path tests/test_validate_ace_public_surface_snapshot_urls.py --scan-public-path tests/test_validate_ace_public_surface_scan.py`
  - `uv run python scripts/validate_ace_public_surface_scan.py --review-issue 72 --review-phase plan --review-provider claude --review-round r1 --include-sidecars`
  - `uv run python scripts/validate_ace_public_surface_scan.py --review-issue 72 --review-phase plan --review-provider codex --review-round r1 --include-sidecars`
  - `uv run python scripts/validate_ace_public_surface_scan.py --review-issue 72 --review-phase plan --review-provider gemini --review-round r1 --include-sidecars`
  - Repeat the same selector/sidecar command for every retained `plan-72` review round and provider present at implementation closeout; if a provider artifact is retained only as a generic unavailable note before selector support exists, scan it explicitly with `--scan-public-path`.
  - `bash scripts/legal/legal-sanity-scan.sh --diff-only`
  - `git diff --check`

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MINOR | Found false #64 rationale, non-runnable snapshot reproduction proof, stale singular contract-key ambiguity, missing legacy-artifact selector test, and omitted aggregate test file in evidence. Current draft patches these findings; r2 review required. |
| Codex r1 | MAJOR | Found non-runnable snapshot reproduction proof, omitted allow-context path hard-coding surface, and too-narrow verification command list. Current draft patches these findings; r2 review required. |
| Gemini r1 | UNAVAILABLE | CLI returned service-unavailable during Code Assist load, then ineligible-tier/unsupported-client; no usable review signal. |
| Claude r2 | MINOR | Found omitted rules test module declaration and round-pinned review-artifact verification. Current draft patches both findings. |
| Codex r2 | MINOR | Found omitted rules test module declaration and missing Gemini selector/sidecar command or classification. Current draft patches both findings. |
| Gemini r2 | UNAVAILABLE | CLI returned the same unsupported-client/ineligible-tier condition; no usable review signal. |

**Overall result:** PLAN-APPROVED - r2 returned Claude MINOR and Codex MINOR with no usable MAJOR; Gemini remained unavailable. The r2 MINOR findings are patched in this draft. User approval is recorded in `.planning/plan-approved/72.md`; implementation may proceed only after the live issue carries `status:plan-approved` and this plan's dependency gates are satisfied.

---

## Risks and Open Questions

- **Risk:** A broad issue enum could become a quiet wildcard. The implementation will keep the enum explicit, integer-only, validated by tests, and changed only through reviewed config edits.
- **Risk:** URL validation could accidentally trust the URL path instead of the snapshot issue field. Tests will cover both mismatch directions.
- **Risk:** Review artifact regex changes could weaken provider closure. Tests will keep provider parsing tied to `EXPECTED_PROVIDERS`.
- **Risk:** Public-surface scans could self-block on retained review artifacts. Implementation will scan retained artifacts and sidecars before commit and will avoid blanket exemptions.
- **Risk:** The exact issue enum could drift when new follow-on issues are created. Later additions will be explicit reviewed config changes, not runtime discovery.

---

## Complexity

**T2** - #72 modifies a focused scanner/contract/test surface with security-sensitive fail-closed semantics, but it does not touch private corpus ingestion, durable stores, or publication behavior.
