# Plan for #63: ACE Cross-Wave Public-Output Redaction and Identifier Canary

> **Status:** plan-approved
> **Complexity:** T3
> **Date:** 2026-07-02
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-07-02-plan-63-claude-r1.md | scripts/review/results/2026-07-02-plan-63-codex-r1.md | scripts/review/results/2026-07-02-plan-63-gemini-r1.md | scripts/review/results/2026-07-02-plan-63-claude-r2.md | scripts/review/results/2026-07-02-plan-63-codex-r2.md | scripts/review/results/2026-07-02-plan-63-gemini-r2.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/07-data-governance.md`, `docs/18-security-and-pii.md`, and `docs/19-trust-boundary-and-private-mode.md` will supply the public/private boundary, PII/security, and private-mode principles.
- `artifacts/ace-wave0-ledger-schema.json` and `scripts/validate_ace_wave0_schema_contract.py` will be consumed as the implemented #65 source for route/store schema, wave classes, and publication-certification ownership.
- `config/ace-public-token-fixture-contract.json` and `scripts/validate_ace_public_token_fixtures.py` will be consumed as the implemented #66 source for `public_source_token`, `pst_` token grammar, forbidden source-request keys, private source terms, and placeholder values.
- `config/ace-public-surface-self-scan-contract.json`, `scripts/validate_ace_public_surface_scan.py`, and `scripts/ace_public_surface_*.py` will be consumed as the implemented #68 public-surface scanner contract. #63 will not fork or redefine the #68 scanner rule engine.
- `.legal-deny-list.yaml`, `scripts/legal/legal-sanity-scan.sh`, and `scripts/legal/legal_sanity_scan.py` will be consumed as the implemented #69 legal/security scan gate. The committed legal config already declares `private_runtime_config_owner_issue: 63` and intentionally contains no real private/client inventories.
- `.github/workflows/validate.yml` already runs #66, #68, and #69 validators; #63 implementation will add the public-output canary and its unit tests to that workflow.
- `scripts/ace_public_token_fixtures.py` already enforces the #66/#63 handoff: once `config/ace-public-output-contract.json` exists, `config/ace-public-token-fixture-contract.json` must set `provisional_fixture_contract` to `false` and the #63 token grammar/field policy must match #66.
- Current #66 baseline verification is not green: `uv run python scripts/validate_ace_public_token_fixtures.py` fails on `tests/test_validate_ace_public_token_fixtures.py` because the test source contains a literal forbidden request-key example. #63 implementation must repair that scan-clean baseline before completing the #66/#63 handoff.

### Related issues and live status
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic and remains open as the tracker.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains an open umbrella issue with no `status:*` label and no local approval marker. #63 will consume the implemented split contracts rather than treating the #51 umbrella as approved.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) has user approval recorded in `.planning/plan-approved/61.md`; #63 no longer needs an independent canary-only exception for the approval dependency, but durable certification work remains subject to #61 implemented validator evidence where this plan requires it.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#71](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/71) are closed implemented split contracts that #63 will consume where relevant.
- [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) has user approval recorded in `.planning/plan-approved/72.md`; until it is implemented, #63 will use explicit `--scan-public-path` inputs and will not depend on generalized review selector/snapshot modes.
- [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) are downstream wave plans that must not publish docs, `mkdocs.yml` entries, `llm-wiki` outputs, issue closeout summaries, or external public artifacts without the #63 canary passing.

### Source inventory boundary
- #63 will scan repo-local public artifacts, issue-comment body snapshots, review artifacts, and synthetic canary fixtures only.
- #63 will not read `ACE_SHARE_ROOT`, crawl private source directories, inspect raw ACE files, copy title blocks/BOM rows, extract EXIF/GPS metadata from real media, or commit private/client/project/customer name inventories.
- Committed deny lists will stay generic and schema-like. Private runtime deny-list inputs, if used later, will be external local inputs and will not be committed.
- Negative fixtures will remain scan-clean: tests will synthesize forbidden-looking values at runtime or store neutral placeholders with deterministic fixture markers. No tracked bad fixture will contain a raw private path, raw digest, real public token value, email, phone, real client/project/customer identifier, or copied private snippet.

### Gaps identified
- No #63 public-output certification contract exists that ties #66 token policy, #68 public-surface scanner, #69 legal scan, issue-comment scanning, and publication/closeout gates together.
- No `scripts/validate_ace_public_artifacts.py` canary exists for publication and closeout surfaces.
- No #63 synthetic canary fixture set exists for EXIF/GPS, title-block/BOM, unsafe field/table names, copied-private-snippet sentinels, issue comments, or public-summary bodies.
- No source-hash/source-digest policy sweep report exists to classify repo-tracked public methodology references and prevent raw source hashes from being treated as public source references.
- No CI step invokes a #63 public-output canary.
- No #63 review artifacts exist under `scripts/review/results/`.
- Existing #66 public-token fixture validation currently fails on a scan-cleanliness issue in `tests/test_validate_ace_public_token_fixtures.py`; #63 must either repair that baseline before the handoff or remain blocked.

### Evidence

**Live issue status** (verified 2026-07-02):
```text
#63 OPEN labels=strengthening,lane:claude,priority:high
#51 OPEN labels=strengthening,lane:claude,priority:high; no local approval marker
#61 OPEN labels=strengthening,status:plan-approved,lane:claude,priority:high; local marker exists
#62 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high; local marker exists
#65 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high
#66 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high
#67 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high
#68 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high
#69 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high
#70 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high
#71 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:medium
#72 OPEN labels=strengthening,status:plan-approved,lane:claude,priority:medium; local marker exists
```

**File existence**:
```text
EXISTS docs/07-data-governance.md
EXISTS docs/18-security-and-pii.md
EXISTS docs/19-trust-boundary-and-private-mode.md
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS config/ace-public-token-fixture-contract.json
EXISTS config/ace-public-surface-self-scan-contract.json
EXISTS .legal-deny-list.yaml
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS scripts/validate_ace_public_token_fixtures.py
EXISTS scripts/validate_ace_public_surface_scan.py
EXISTS scripts/legal/legal-sanity-scan.sh
EXISTS scripts/legal/legal_sanity_scan.py
EXISTS tests/test_validate_ace_public_token_fixtures.py
EXISTS tests/test_validate_ace_public_surface_scan.py
EXISTS tests/test_legal_sanity_scan.py
EXISTS skills/public-private-routing/SKILL.md
EXISTS skills/public-private-routing/evals/evals.json
MISSING docs/case-studies/ace-public-output-redaction-contract.md
MISSING artifacts/ace-source-hash-policy-sweep.md
MISSING config/ace-public-output-contract.json
MISSING config/ace-public-surface-deny-list.json
MISSING scripts/ace_public_output_contract.py
MISSING scripts/validate_ace_public_artifacts.py
MISSING tests/test_validate_ace_public_artifacts.py
MISSING tests/fixtures/ace-public-artifact-safety/
EXISTS scripts/review/results/2026-07-02-plan-63-claude-r1.md
EXISTS scripts/review/results/2026-07-02-plan-63-codex-r1.md
EXISTS scripts/review/results/2026-07-02-plan-63-gemini-r1.md
EXISTS scripts/review/results/2026-07-02-plan-63-claude-r2.md
EXISTS scripts/review/results/2026-07-02-plan-63-codex-r2.md
EXISTS scripts/review/results/2026-07-02-plan-63-gemini-r2.md
```

**Baseline validator proof** (verified 2026-07-02):
```text
$ uv run python scripts/validate_ace_public_token_fixtures.py
DENY forbidden-request-key in tests/test_validate_ace_public_token_fixtures.py
FAIL: 1 error(s)
```

**MkDocs/publication evidence**:
```text
mkdocs.yml exists and uses explicit nav.
Current nav lists case-studies/format-coverage-audit.md and case-studies/pdf-large-reader-salvage.md only.
The planned #63 contract doc is not currently published by mkdocs nav.
```

The plan filename date (`2026-06-29`) is the original draft creation date. The header date (`2026-07-02`) is the current revision/review date.

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-29-issue-63-ace-public-output-redaction-and-identifier-canary.md` |
| Public-safe contract narrative | `docs/case-studies/ace-public-output-redaction-contract.md` |
| Source-hash policy sweep report | `artifacts/ace-source-hash-policy-sweep.md` |
| Public-output contract | `config/ace-public-output-contract.json` |
| #66 handoff contract | `config/ace-public-token-fixture-contract.json` |
| #66 baseline scan-clean repair | `tests/test_validate_ace_public_token_fixtures.py` |
| #63 deny-list/publication supplement | `config/ace-public-surface-deny-list.json` |
| Contract loader/helper | `scripts/ace_public_output_contract.py` |
| Public-output canary | `scripts/validate_ace_public_artifacts.py` |
| Canary fixtures | `tests/fixtures/ace-public-artifact-safety/` |
| Canary tests | `tests/test_validate_ace_public_artifacts.py` |
| CI workflow | `.github/workflows/validate.yml` |
| Governance docs | `docs/07-data-governance.md`, `docs/18-security-and-pii.md`, `docs/19-trust-boundary-and-private-mode.md` |
| Skill binding | `skills/public-private-routing/SKILL.md`, `skills/public-private-routing/evals/evals.json` |
| Review artifacts | `scripts/review/results/2026-07-02-plan-63-claude-r1.md`, `scripts/review/results/2026-07-02-plan-63-codex-r1.md`, `scripts/review/results/2026-07-02-plan-63-gemini-r1.md` |
| Review artifacts | `scripts/review/results/2026-07-02-plan-63-claude-r2.md`, `scripts/review/results/2026-07-02-plan-63-codex-r2.md`, `scripts/review/results/2026-07-02-plan-63-gemini-r2.md` |

---

## Deliverable

A repo-local, CI-validated #63 public-output certification contract and canary will gate ACE-derived public artifacts before publication or closeout. It will import #66 token/private-field rules, #68 public-surface scanning, and #69 legal/security scanning; add #63 publication-specific fixtures and source-hash policy sweep; and keep real private deny-list inventories outside tracked repo state.

---

## Proposed Contract Shape

### Public-Output Contract

`config/ace-public-output-contract.json` will define:
- imported #66 token contract path, version, owner issue, `public_source_token` field name, and `pst_` grammar;
- imported private-only source terms and source-like digest terms from #66;
- exact #66 handoff keys enforced by `scripts/ace_public_token_fixtures.py`: `public_token_field_name`, `public_token_grammar`, `public_safe_source_reference_fields`/`public_source_reference_fields`, `private_only_provenance_fields`, `private_only_fields`, `banned_public_fields`, `source_like_raw_digest_terms`, and `source_hash_private_terms`;
- git governance exceptions for commit SHAs, restricted to explicit governance fields such as `reviewed_commit_sha`, `commit_sha`, and `git_commit_sha`;
- public artifact surface classes: `docs`, `skills`, review artifacts, issue-comment snapshots, closeout summaries, `mkdocs.yml`, and future `llm-wiki` outputs;
- allowed sanitized aggregate count contexts and examples;
- required evidence fields for publication certification: canary command, exit code, scanned paths, contract version, and timestamp.

The contract will not mint durable tokens or define private lookup persistence. #66 owns fixture token grammar; #61 owns durable lookup persistence; #68 owns the public-surface scanner rule engine; #69 owns the legal/security scanner. When #63 creates `config/ace-public-output-contract.json`, implementation will also flip #66's `provisional_fixture_contract` to `false` and keep `uv run python scripts/validate_ace_public_token_fixtures.py` green.

### #63 Deny-List Supplement

`config/ace-public-surface-deny-list.json` will be a generic, public-safe supplement for #63 publication certification. It will:
- import or reference #68 and #69 rule classes rather than duplicate their regex engines;
- declare #63 publication-only classes for EXIF/GPS, title-block/BOM strings, unsafe field/table names, copied-private-snippet sentinels, issue-comment bodies, and external-publication summaries;
- reject real client/project/customer/private-name inventories and raw private values by schema;
- allow optional local private-deny inputs only by environment or CLI argument, never by committed config.

### Source-Hash Policy Sweep

`artifacts/ace-source-hash-policy-sweep.md` will record repo-local public-surface hits for source-hash/source-digest/provenance-pointer language. The sweep will:
- scan only repo-tracked `docs/**/*.md`, `skills/**/*.md`, `docs/plans/**/*.md`, and selected public methodology artifacts;
- emit stable hit keys without publishing raw digest values;
- classify every hit as `modify_public_safe_hash_claim`, `no_change_private_context`, `no_change_git_governance_sha`, or `reject_unclassified`;
- fail closed on unclassified hits;
- rewrite public-facing claims so raw source hashes remain private-sidecar provenance and public artifacts use `public_source_token` references where source references are required.

### Publication Gate

The canary will certify planned public outputs before:
- adding ACE-derived docs to `mkdocs.yml` nav;
- posting GitHub issue closeout comments that summarize ACE-derived content;
- writing future `llm-wiki` outputs;
- exporting public reports or publication summaries.

The #63 public contract doc itself may exist as a scan-clean methodology artifact, but it will not be added to `mkdocs.yml` navigation in this issue unless the #63 canary validates the exact doc/nav change and the plan explicitly records that publication intent.

---

## Pseudocode

```text
load #65 schema registry for publication_certification owner mapping
load #66 token fixture contract for public_source_token grammar and private source terms
load #68 public-surface scan facade
load #69 legal/security scan wrapper/config
assert #63 implementation does not read ACE_SHARE_ROOT or private raw source content

define config/ace-public-output-contract.json:
  import #66 public token field and pst_ grammar
  import #66 private source/source-like digest terms
  define git governance SHA exceptions by explicit field name/context
  define public output surfaces and required certification evidence
  define narrow sanitized aggregate/example allow contexts
update #66 fixture contract provisional_fixture_contract to false
validate #66 token fixture contract still passes after #63 config exists

define config/ace-public-surface-deny-list.json:
  reference #68/#69 rule owners and rule classes
  define #63 publication-only deny classes
  forbid committed private/client/customer/project inventories
  allow optional local private deny-list input only outside tracked repo state

define source hash policy sweep:
  scan repo-tracked public markdown/config surfaces only
  record stable hit keys without raw digest values
  require modify/no-change/reject classification for every hit

define validate_ace_public_artifacts.py:
  accept explicit --scan-public-path paths
  accept explicit issue-comment body files before posting
  reject #63 selector/snapshot mode claims until #72 is implemented
  scan explicit review artifact paths and same-stem sidecars
  run #68 public-surface scan on all candidate text artifacts
  run #69 legal/security scan for repo-tracked/diff/all-tracked modes where applicable
  apply #63 publication-specific checks and source-hash sweep checks
  fail closed on missing #63 contract, unclassified sweep hits, raw private values, real token assignments, or blanket allowlists

validate CI wiring, docs, fixtures, skill binding, public scan, and legal scan
stop for user approval after plan review; do not implement from this plan draft
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `docs/case-studies/ace-public-output-redaction-contract.md` | Human-readable #63 public-output certification contract |
| Create | `artifacts/ace-source-hash-policy-sweep.md` | Public-safe classification report for source-hash/source-digest/provenance language |
| Create | `config/ace-public-output-contract.json` | Machine-readable public-output token/source-hash/publication certification contract |
| Modify | `config/ace-public-token-fixture-contract.json` | Flip `provisional_fixture_contract` to `false` once #63 public-output contract exists and preserve #66/#63 token policy parity |
| Modify | `tests/test_validate_ace_public_token_fixtures.py` | Repair existing #66 scan-clean baseline so `scripts/validate_ace_public_token_fixtures.py` passes before #63 handoff |
| Create | `config/ace-public-surface-deny-list.json` | Public-safe #63 publication deny-list supplement and private-deny input schema |
| Create | `scripts/ace_public_output_contract.py` | JSON loader, owner/import checks, sweep classification helper, and shared canary utilities |
| Create | `scripts/validate_ace_public_artifacts.py` | Executable #63 public-output canary |
| Create | `tests/test_validate_ace_public_artifacts.py` | TDD coverage for #63 contract/canary behavior |
| Create | `tests/fixtures/ace-public-artifact-safety/` | Synthetic scan-clean positive and runtime-synthesized negative fixtures |
| Modify | `.github/workflows/validate.yml` | Run #63 canary and unit tests |
| Modify | `docs/07-data-governance.md` | Cross-link public-output certification and private deny-list residency |
| Modify | `docs/18-security-and-pii.md` | Add ACE public-output canary classes |
| Modify | `docs/19-trust-boundary-and-private-mode.md` | Add publication/issue-comment/llm-wiki gate |
| Modify | `skills/public-private-routing/SKILL.md` | Require #63 canary before public outputs |
| Modify | `skills/public-private-routing/evals/evals.json` | Add issue-tagged #63 canary eval cases |
| Audit/conditional modify | repo-tracked docs/plans/skills returned by source-hash sweep | Rewrite only public-facing raw-hash/source-reference claims or assigned source-like digest values |
| Deferred | `mkdocs.yml` | Do not add #63 or ACE-derived docs to nav unless the #63 canary validates that exact nav change |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_loads_imported_66_and_68_contracts` | #63 imports existing token/scanner contracts | Mutated #66/#68 version or missing path | Validator rejects drift or missing import |
| `test_66_existing_public_scan_baseline_is_clean` | Existing #66 validation baseline is restored before #63 handoff | Current #66 validator/test sources | `uv run python scripts/validate_ace_public_token_fixtures.py` and `tests.test_validate_ace_public_token_fixtures` pass |
| `test_66_provisional_handoff_is_closed` | Creating the #63 public-output contract completes the #66 provisional handoff | #63 contract exists while #66 still has `provisional_fixture_contract=true` or mismatched token grammar | Validator rejects; #66 validator passes after the flag flips to `false` |
| `test_public_output_contract_schema_is_closed` | #63 contract cannot carry private inventories or unknown keys | Contract fixture with inventory keys or raw private values | Validator rejects |
| `test_public_deny_list_supplement_is_public_safe` | Committed deny-list supplement is generic and scan-clean | Deny-list fixture with real/private-like inventory key | Validator rejects |
| `test_optional_private_deny_list_is_runtime_only` | Private deny-list inputs cannot be committed | Config fixture pointing to committed private inventory | Validator rejects; local external input shape is accepted only outside repo |
| `test_blocks_raw_host_paths_and_private_path_fragments` | Path leakage | Runtime-synthesized artifact text with raw host/private path shape | Validation fails without storing the raw value in tracked fixtures |
| `test_blocks_personal_and_private_identifier_patterns` | Email/phone/private identifier leakage | Runtime-synthesized client/project/email/phone-like strings | Validation fails |
| `test_blocks_exif_gps_and_media_metadata` | Media metadata leakage | Synthetic EXIF/GPS marker fixture | Validation fails |
| `test_blocks_title_block_bom_and_field_names` | Engineering metadata leakage | Synthetic title block, BOM, and unsafe field/table examples | Validation fails |
| `test_blocks_raw_source_ids_hashes_private_lookup_maps` | Private provenance leakage | Runtime-synthesized public surface with private source/source-like fields assigned as values | Validation fails |
| `test_allows_schema_terms_only_in_contract_context` | Schema prose can name private terms without assigning values | Contract docs/config with terms under neutral enum/list context | Validation passes |
| `test_blocks_public_source_token_literal_assignment` | Public token literals are not emitted in public artifacts | Runtime-synthesized `public_source_token` assignment with token-looking value | Validation fails |
| `test_allows_git_governance_sha_only_in_named_contexts` | Commit SHAs are distinct from raw source hashes | Fixture with `reviewed_commit_sha` vs source-hash claim | Governance SHA passes; source-hash public claim fails |
| `test_source_hash_policy_sweep_requires_classification` | Every repo-local source-hash/provenance hit is classified | Sweep fixture with unclassified stable hit | Validator rejects |
| `test_source_hash_policy_sweep_redacts_digest_values` | Sweep report does not publish raw digest values | Sweep report with raw digest value | Validator rejects |
| `test_allowlist_is_narrow_and_pattern_restricted` | Exception hygiene | Blanket path/file allowlist or author-controlled sentinel | Validation fails |
| `test_issue_comment_body_files_scan_before_post` | GitHub comment bodies can be scanned without #72 selector/snapshot support | Explicit planned-comment body file with safe and unsafe text | Unsafe body fails; safe body passes through explicit path/body-file scan |
| `test_72_snapshot_modes_are_not_claimed_by_63` | #63 does not duplicate #72 selector/snapshot generalization | #63 config or CI fixture claiming `--review-issue 63`, snapshot, or snapshot-pair support before #72 | Validator rejects the claim |
| `test_review_artifact_names_are_round_scoped_and_issue_63_bound` | Review artifact naming is deterministic even when scanned by explicit paths | Roundless legacy names, wrong issue numbers, unknown providers, symlinks, and missing same-stem sidecar checks | Validator rejects |
| `test_review_artifacts_and_sidecars_are_scanned_explicitly` | Review artifacts cannot leak private/source data | Review artifact and sidecar fixtures | Unsafe artifact or sidecar fails |
| `test_mkdocs_nav_publication_requires_canary` | Docs navigation is gated | `mkdocs.yml` fixture adding ACE-derived doc without canary evidence or without including the doc/nav pair in scan paths | Validator rejects |
| `test_downstream_wave_closeout_requires_canary` | Wave closeout/publication gates bind to #63 | Downstream wave plan/closeout fixture | Missing #63 command/evidence fails |
| `test_no_ace_share_root_or_raw_source_reads` | #63 canary cannot read private source roots | Source scan of #63 changed artifacts | `ACE_SHARE_ROOT`, raw source crawls, and unbounded raw source read/hash/count commands fail; bounded repo fixture reads pass |
| `test_negative_fixtures_are_scan_clean` | Bad cases do not poison repo-wide scans | Fixture directory and test source | Tracked fixtures contain neutral placeholders or runtime-synthesis markers only |
| `test_diagnostics_do_not_echo_synthetic_sensitive_values` | Scanner output stays safe even on failure | Runtime-synthesized unsafe values | Diagnostics report rule IDs and paths but redact the matched sensitive value |
| `test_public_private_routing_skill_eval_cases_are_issue_tagged` | Skill binding is deterministic | Skill eval JSON | New cases require `issue: 63` metadata and IDs beginning with `ace-63-` |
| `test_ci_runs_63_canary_public_scan_and_legal_scan` | CI includes the new gate | Workflow text | Required #63 validator, unit test, public scan, and legal scan commands are present |

---

## Verification Commands

Implementation will run:

```bash
uv run python scripts/validate_ace_public_artifacts.py
uv run python scripts/validate_ace_public_token_fixtures.py
uv run python scripts/validate_ace_public_surface_scan.py \
  --scan-public-path docs/plans/2026-06-29-issue-63-ace-public-output-redaction-and-identifier-canary.md \
  --scan-public-path docs/case-studies/ace-public-output-redaction-contract.md \
  --scan-public-path artifacts/ace-source-hash-policy-sweep.md \
  --scan-public-path config/ace-public-token-fixture-contract.json \
  --scan-public-path config/ace-public-output-contract.json \
  --scan-public-path config/ace-public-surface-deny-list.json \
  --scan-public-path scripts/ace_public_output_contract.py \
  --scan-public-path scripts/validate_ace_public_artifacts.py \
  --scan-public-path tests/test_validate_ace_public_artifacts.py \
  --scan-public-path tests/fixtures/ace-public-artifact-safety/ \
  --scan-public-path docs/07-data-governance.md \
  --scan-public-path docs/18-security-and-pii.md \
  --scan-public-path docs/19-trust-boundary-and-private-mode.md \
  --scan-public-path skills/public-private-routing/SKILL.md \
  --scan-public-path skills/public-private-routing/evals/evals.json \
  --scan-public-path .github/workflows/validate.yml
uv run python -m unittest tests.test_validate_ace_public_artifacts tests.test_validate_ace_public_token_fixtures tests.test_validate_ace_public_surface_scan tests.test_legal_sanity_scan
uv run skills/validate_skill.py
bash scripts/legal/legal-sanity-scan.sh --diff-only
bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces
git diff --check
```

Plan-review verification will run generic public scans over this plan, `docs/plans/README.md`, and the review artifacts. Review selector/snapshot mode will remain out of scope until #72 is implemented. `status:plan-review` may be applied only after the patched plan and review artifacts are committed, pushed, and linked from a GitHub evidence comment. User approval for `status:plan-approved` is recorded in `.planning/plan-approved/63.md`.

---

## Acceptance Criteria

- [ ] #63 public-output certification imports #66 token/private-source terms, #68 public-surface scanning, and #69 legal/security scanning instead of redefining their rule engines.
- [ ] Creating `config/ace-public-output-contract.json` completes the #66 provisional handoff by setting `config/ace-public-token-fixture-contract.json` `provisional_fixture_contract=false`; `uv run python scripts/validate_ace_public_token_fixtures.py` remains green.
- [ ] `config/ace-public-output-contract.json` defines public output surfaces, source-reference policy, git governance SHA exceptions, sanitized aggregate/example allow contexts, and required certification evidence without private inventories.
- [ ] `config/ace-public-surface-deny-list.json` is a public-safe supplement only: it rejects committed real client/project/customer/private-name inventories and permits private deny-list input only from external untracked runtime sources.
- [ ] Public artifacts use `public_source_token` source references and never publish raw `source_id`, `source_sha256`, `private_lookup_key`, `private_lookup_map`, `share_relative_path_private_only`, `source_hash`, or `provenance_pointer` values.
- [ ] Redaction canary blocks raw host paths, private path fragments, personal identifiers, generic private identifiers, confidentiality markers, EXIF/GPS, title-block/BOM strings, unsafe table/field names, copied-private-snippet sentinels, raw source-hash/source-digest public-reference claims, public token literal assignments, and provider sidecar leaks.
- [ ] Source-hash policy sweep scans only repo-tracked public methodology surfaces, records stable hit keys without raw digest values, classifies every hit, and fails closed on unclassified hits.
- [ ] Git commit SHAs are allowed only in explicit governance contexts and cannot be used as source provenance/public-reference hashes.
- [ ] Issue-comment bodies and review artifacts are scanned by explicit path/body-file inputs before posting while #72 remains unimplemented; #63 does not claim `--review-issue 63`, snapshot, or snapshot-pair support until #72 lands.
- [ ] Review artifacts use deterministic `YYYY-MM-DD-plan-63-{claude,codex,gemini}-rN.md` naming and explicit path scans; roundless legacy names, wrong issue numbers, unknown providers, symlinks, and unscanned same-stem sidecars fail closed.
- [ ] Sanitized aggregate counts and examples are allowed only through narrow committed content-pattern-restricted allowlists; arbitrary line/path sentinels and blanket file/path exemptions fail.
- [ ] #63 canary and changed artifacts do not read `ACE_SHARE_ROOT`, crawl raw source roots, hash/count raw source files, or materialize private source inventories.
- [ ] Canary diagnostics redact matched sensitive values and expose only rule IDs, public-safe relative paths, and line numbers.
- [ ] The #63 contract doc may exist as a scan-clean methodology artifact; `mkdocs.yml` nav additions, `llm-wiki` outputs, GitHub-public corpus summaries, and external ACE-derived publication exposure require #63 canary evidence.
- [ ] Downstream wave plans/closeouts require `uv run python scripts/validate_ace_public_artifacts.py` before publication or issue closeout.
- [ ] `skills/public-private-routing` receives issue-tagged #63 eval cases with `issue: 63` metadata and `ace-63-` IDs.
- [ ] CI runs the #63 canary, #63 unit tests, public-surface scan, legal scan, and skill validation.
- [ ] `uv run python scripts/validate_ace_public_artifacts.py`, `uv run python scripts/validate_ace_public_token_fixtures.py`, public-surface scan, legal scan, unit tests, `uv run skills/validate_skill.py`, and `git diff --check` pass.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MINOR | #72 selector/snapshot overlap, exact #66 handoff key set, and date bookkeeping needed tightening. Findings patched in this draft. |
| Codex r1 | MAJOR | Existing #66 baseline validation failure, #72 selector/snapshot scope overlap, and draft/not-plan-review metadata needed tightening. Findings patched in this draft. |
| Gemini r1 | UNAVAILABLE | Gemini CLI failed with unsupported-client/ineligible-tier before returning findings. |
| Claude r2 | MINOR | Review-artifact file-existence evidence, commit-before-label audit trail, and degraded two-provider review-panel documentation needed tightening. Findings patched in this draft. |
| Codex r2 | MINOR | r1 review artifact file-existence evidence was stale after the r1 artifacts were created. Finding patched in this draft. |
| Gemini r2 | UNAVAILABLE | Gemini CLI failed with unsupported-client/ineligible-tier before returning findings. |

**Overall result:** PLAN-APPROVED - r1 returned Codex MAJOR and Claude MINOR; r2 active-provider review returned Claude MINOR and Codex MINOR with no usable MAJOR. Gemini was unavailable in both rounds, so the T3 review panel degraded to active providers only with explicit UNAVAILABLE artifacts. User approval is recorded in `.planning/plan-approved/63.md`; implementation may proceed only after the live issue carries `status:plan-approved` and this plan's dependency gates are satisfied.

---

## Risks and Open Questions

- **Risk:** #63 could duplicate #68/#69 rule engines and create divergent public-surface behavior. The implementation must import/facade existing scanners and limit #63 to publication certification and #63-specific deny classes.
- **Risk:** Negative fixtures and deny-list examples could self-block public/legal scans. The implementation must use runtime synthesis or neutral placeholders and validate the changed artifacts with both scanners.
- **Risk:** A committed private deny-list could leak the exact private inventory it is meant to block. The plan keeps committed configs generic and requires private runtime inputs to stay outside the repo.
- **Risk:** Source-hash sweep output could publish raw digest values while trying to classify them. The report must record stable hit keys and redacted/classes, not raw source digest values.
- **Risk:** #51 remains a draft umbrella and #61 remains unimplemented. #63 may proceed from approval to implementation only within this plan's dependency gates.
- **Risk:** #72 remains unimplemented. #63 must use explicit scan paths and cannot rely on generalized review selector/snapshot modes yet.

---

## Complexity

**T3** - security-sensitive cross-wave public artifact scanner/certification gate touching configs, validators, tests, docs, skill evals, CI, issue comments, review artifacts, and future publication surfaces.
