# Plan for #52: ACE Wave 1 LLM-Native Text, Markup, Code, and Small JSON Bootstrap

> **Status:** plan-review
> **Complexity:** T2
> **Date:** 2026-07-02
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** `scripts/review/results/2026-07-02-plan-52-claude-r1.md` | `scripts/review/results/2026-07-02-plan-52-codex-r1.md` | `scripts/review/results/2026-07-02-plan-52-gemini-r1.md` | `scripts/review/results/2026-07-02-plan-52-claude-r2.md` | `scripts/review/results/2026-07-02-plan-52-codex-r2.md` | `scripts/review/results/2026-07-02-plan-52-gemini-r2.md`

---

## Resource Intelligence Summary

### Repo contracts this plan will consume

- `artifacts/ace-wave0-ledger-schema.json` and `scripts/validate_ace_wave0_schema_contract.py` from [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will provide the closed route vocabulary, wave registry, skill bindings, and success-field names.
- `config/ace-public-token-fixture-contract.json`, `config/ace-bounded-sampling-firewall-contract.json`, `config/ace-public-surface-self-scan-contract.json`, and `scripts/legal/legal-sanity-scan.sh` from [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will provide placeholder, bounded-read, public-scan, and legal/security gates.
- `config/ace-manifest-evidence-contract.json`, `scripts/validate_ace_manifest_freshness.py`, `artifacts/ace-manifest-freshness/trusted-evidence-registry.json`, and `tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json` from [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62)/[#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) will provide manifest snapshot evidence before any implementation samples ACE manifest-backed source families.
- `docs/01-document-taxonomy.md` will provide content-first type classification and extraction levels.
- `docs/10-structured-data-and-model-files.md` will provide structured/config fragility rules: dialect, conventions, and content validation before trusting a parse.
- `docs/14-chunking-and-embedding.md`, `docs/15-retrieval-evaluation.md`, and `docs/16-corpus-lifecycle.md` will be referenced only through [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) once that cross-wave contract is approved.
- `skills/content-triage-and-exclusion/SKILL.md`, `skills/source-extraction-coverage/SKILL.md`, `skills/source-extract-fidelity/SKILL.md`, `skills/page-shape-contract/SKILL.md`, and `skills/public-private-routing/SKILL.md` will be the always-used and updated skill group for this wave.

### Related issues and live status

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic and authorizes progressive planning, not child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains an open umbrella issue with no `status:*` label and no local approval marker. This plan will not treat the [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) umbrella as approved.
- [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) remains open with no `status:*` label and no local approval marker.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is in `status:plan-review` and remains unapproved. Durable stores, target paths, retrieval metadata, lifecycle state, and persistent success metrics will stay blocked until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved and implemented.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) is closed with `status:plan-approved`, `.planning/plan-approved/62.md`, an implemented manifest freshness validator, and a recorded valid evidence fixture. Operational downstream sampling still requires a trusted [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) evidence-registry pointer; if `artifacts/ace-manifest-freshness/trusted-evidence-registry.json` has no trusted evidence entry for the requested snapshot, [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) sampling fails closed.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is in `status:plan-review` and remains unapproved. Public-facing reports, docs navigation, `mkdocs.yml`, `llm-wiki`, GitHub-public corpus summaries, and external publication exposure will stay blocked until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved and implemented.
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) are closed wave-0 split contracts that this wave will consume for route/schema, placeholder, bounded sampling, public scan, and legal scan. [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) is the closed manifest-evidence integration contract consumed separately for trusted [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) pointers.
- [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) is in `status:plan-review`; until approved and implemented, this plan will use only generic `--scan-public-path` public-surface scans and will not claim selector/snapshot review support.

### Source inventory boundary

- Prior ACE manifest rollup represented text/markup as roughly 1.48M files / 6.4 GB after treating engineering `.rst` as simulation rather than prose.
- Prior ACE manifest rollup represented code/scripts as roughly 43.8k files / 0.36 GB.
- Prior ACE manifest rollup represented about 1.43M `.json` files as tiny and likely generated, so `.json` will not imply useful content.
- Plan-review work will not read `ACE_SHARE_ROOT`, crawl manifests, count private rows, hash raw source files, copy source snippets, or materialize ACE source inventories.
- Implementation sampling, if later approved, will be bounded by [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) and will require both [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot evidence and a [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) trusted registry pointer before any manifest-backed source family is touched.
- Public artifacts will use only public-safe aggregate ranges, opaque snapshot IDs, validator paths, command status, and synthetic fixtures.

### Gaps identified

- No deterministic generated/repetitive JSON rule exists in the playbook.
- No ACE wave-1 text/config pilot report exists.
- No helper self-test exists for hand-authored text, markup, small config JSON, repetitive generated JSON, and low-value source-tree triage.
- No wave-1 validator exists to enforce sample caps, closed route enum use, extraction estimate/yield presence, zero-denominator behavior, public/private routing, and scan-clean fixtures.
- Current skill docs describe content triage, extraction coverage, fidelity, page shape, and public/private routing, but they do not yet contain wave-1 JSON/config/code-source examples or eval fixtures.

### Evidence

**Live issue status** (verified 2026-07-02):

```text
#52 OPEN labels=strengthening,lane:codex,priority:high; no local approval marker
#51 OPEN labels=strengthening,lane:claude,priority:high; no local approval marker
#61 OPEN labels=strengthening,status:plan-review,lane:claude,priority:high; no local approval marker
#62 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high; local marker exists
#63 OPEN labels=strengthening,status:plan-review,lane:claude,priority:high; no local approval marker
#65-#69 CLOSED with status:plan-approved labels and local approval markers; #70 CLOSED with status:plan-approved label and local approval marker as manifest-evidence integration
#72 OPEN labels=strengthening,status:plan-review,lane:claude,priority:medium
```

**File existence**:

```text
EXISTS docs/01-document-taxonomy.md
EXISTS docs/10-structured-data-and-model-files.md
EXISTS docs/14-chunking-and-embedding.md
EXISTS docs/15-retrieval-evaluation.md
EXISTS docs/16-corpus-lifecycle.md
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS artifacts/ace-manifest-freshness/trusted-evidence-registry.json
EXISTS config/ace-manifest-evidence-contract.json
EXISTS config/ace-bounded-sampling-firewall-contract.json
EXISTS config/ace-public-surface-self-scan-contract.json
EXISTS config/ace-public-token-fixture-contract.json
EXISTS scripts/validate_ace_manifest_freshness.py
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS scripts/validate_ace_public_surface_scan.py
EXISTS scripts/legal/legal-sanity-scan.sh
EXISTS skills/content-triage-and-exclusion/SKILL.md
EXISTS skills/source-extraction-coverage/SKILL.md
EXISTS skills/source-extract-fidelity/SKILL.md
EXISTS skills/page-shape-contract/SKILL.md
EXISTS skills/public-private-routing/SKILL.md
MISSING docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md
MISSING config/ace-wave1-text-json-contract.json
MISSING skills/content-triage-and-exclusion/resources/text_json_triage.py
MISSING scripts/validate_ace_wave1_text_json.py
MISSING tests/test_validate_ace_wave1_text_json.py
MISSING tests/fixtures/ace-wave1-text-json/
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-29-issue-52-ace-wave-1-llm-native-text-markup-code-small-json-bootstrap.md` |
| Plan index | `docs/plans/README.md` |
| ACE coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Wave-1 public-safe synthetic methodology report | `docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md` |
| Wave-1 contract | `config/ace-wave1-text-json-contract.json` |
| Triage helper | `skills/content-triage-and-exclusion/resources/text_json_triage.py` |
| Wave-1 validator | `scripts/validate_ace_wave1_text_json.py` |
| Wave-1 tests | `tests/test_validate_ace_wave1_text_json.py` |
| Synthetic fixtures | `tests/fixtures/ace-wave1-text-json/` |
| Required fixture names | `manual-config.json`, `generated-repetitive-json.json`, `generated-lockfile-like.json`, `hand-authored-markdown.md`, `hand-authored-rst.rst`, `source-tree-docstring.py`, `source-tree-vendored-minified.js`, `sample-manifest.json`, `expected-routing.json` |
| Skill eval updates | `skills/content-triage-and-exclusion/evals/evals.json`, `skills/source-extraction-coverage/evals/evals.json`, `skills/source-extract-fidelity/evals/evals.json`, `skills/page-shape-contract/evals/evals.json`, `skills/public-private-routing/evals/evals.json` |
| Plan-review artifacts | `scripts/review/results/2026-07-02-plan-52-*-r*.md` |

---

## Deliverable

[#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) will deliver a bounded wave-1 bootstrap lane for LLM-native text, markup, code-adjacent docs, and small JSON/config metadata. The lane will classify candidates into the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) closed route targets, prove generated/repetitive JSON detection by content and schema signals, record extraction estimate/yield fields for kept rows, calculate `% ingested success` using the canonical numerator and denominator fields, and update reusable playbook skills/evals.

This issue will not publish ACE-derived content to `llm-wiki`, docs navigation, or external surfaces. Any committed `docs/` methodology page will be synthetic-fixture-only and will not contain measured ACE corpus results, exact private inventory counts, source snippets, or GitHub-public corpus summaries. Operational measured results will remain private sidecar output and will not be committed, commented, added to docs navigation, added to `mkdocs.yml`, pushed to `llm-wiki`, or externally published unless [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved and implemented before [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) implementation reaches a publication step.

---

## Contract Details Required Before Implementation

| Contract | Required rule |
|---|---|
| Route targets | Use only [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) route vocabulary: `public_llm_wiki`, `private_sidecar`, `metadata_only`, `excluded_no_ingest` |
| Candidate classes | Distinguish hand-authored prose/markup, code documentation, small config JSON, generated JSON, dependency/build/source-tree noise, and hard-excluded private/security material |
| Generated JSON detection | Use schema/content signals such as repeated key shape, high path/list cardinality, package/cache/lockfile signatures, generated timestamp markers, minified bulk arrays, and near-duplicate object templates; never route by `.json` alone |
| Code-source handling | Do not recursively ingest source trees; route code files to metadata/docstring/config extraction only when they carry durable knowledge value and pass exclusion gates |
| Extraction estimate/yield | For kept rows, record pre-extract estimate and post-extract yield; generated/noise exclusions do not count as extraction shortfalls |
| Success metric | Compute `successful_routed_items / eligible_candidate_items * 100`; report `% excluded` separately and use closed zero-denominator status if no eligible candidates exist |
| Sampling | Require [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) valid snapshot evidence, [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) trusted evidence-registry pointer, and [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) bounded sampling before touching manifest-backed ACE families |
| Public routing | Require affirmative public clearance before `public_llm_wiki`; otherwise route to `private_sidecar`, `metadata_only`, or `excluded_no_ingest` |
| Publication | Keep docs nav, `mkdocs.yml`, `llm-wiki`, GitHub-public corpus summaries, and external publication blocked until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved and implemented |

---

## Pseudocode

```text
read #52, #50, #51, #61, #62, #63, closed split contracts #65-#69, and closed integration contract #70
verify #52 has user approval and local approval marker before implementation starts
load #65 route/schema vocabulary and #62 manifest evidence contract
load #70 trusted evidence registry; if no trusted pointer covers the requested #62 evidence, reject operational sampling
build repo-local synthetic fixtures for text, markup, code-doc, config-json, generated-json, source-tree-noise, and exclusion cases
write failing unit tests for wave-1 contract, helper, validator, fixtures, and skill eval coverage
implement text_json_triage helper against fixtures first
if operational ACE sampling is authorized:
  require #62 snapshot evidence, #70 trusted evidence pointer, and #67 bounded sampling request
  cap sampled manifest-backed candidates per bucket and bytes touched
  never crawl ACE_SHARE_ROOT or materialize broad manifests
for each candidate:
  classify by content and schema, not extension or folder
  apply hard exclusions before value ranking
  detect generated/repetitive JSON and source-tree noise before extraction
  choose one closed route target
  for kept rows, record extraction_estimate and extraction_yield
  block public route without affirmative public clearance
compute successful_routed_items / eligible_candidate_items * 100
report generated/noise/hard exclusions separately
write scan-clean synthetic methodology report, contract, fixtures, validator, skill docs, and skill eval updates
keep measured ACE-derived pilot results private-sidecar-only unless #63 is approved and implemented
run public-surface scan and legal scan over every changed public artifact and review artifact
commit and push the plan, coordination docs, and review artifacts before any status label change
write planned issue comment body to repo-local scanner-visible path scripts/review/results/2026-07-02-plan-52-issue-comment.md
scan that issue-comment body with public-surface and legal scanners before posting it
post the scanned issue-comment body, then delete the local comment-body scratch file before final diff-only scan
keep implementation stopped until #52 user approval; keep durable output blocked until #61; keep publication blocked until #63
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md` | Public-safe synthetic methodology and fixture/canary report only; measured ACE-derived corpus results remain private-sidecar-only until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) approval, implemented canary, and passing evidence |
| Create | `config/ace-wave1-text-json-contract.json` | Machine-readable route, generated-JSON, source-tree, estimate/yield, metric, and fixture contract |
| Create | `skills/content-triage-and-exclusion/resources/text_json_triage.py` | Deterministic classifier/self-test helper for text, markup, code-adjacent docs, and small JSON/config |
| Create | `scripts/validate_ace_wave1_text_json.py` | Validator for sample caps, route enum, generated/noise classification, extraction fields, metric fields, and scan-clean fixture policy |
| Create | `tests/test_validate_ace_wave1_text_json.py` | TDD coverage for the contract, helper, validator, and negative cases |
| Create | `tests/fixtures/ace-wave1-text-json/` | Synthetic scan-clean fixtures named `manual-config.json`, `generated-repetitive-json.json`, `generated-lockfile-like.json`, `hand-authored-markdown.md`, `hand-authored-rst.rst`, `source-tree-docstring.py`, `source-tree-vendored-minified.js`, `sample-manifest.json`, and `expected-routing.json` |
| Modify | `skills/content-triage-and-exclusion/SKILL.md` | Add generated/repetitive JSON, source-tree, and config/text triage rules |
| Modify | `skills/source-extraction-coverage/SKILL.md` | Add text/markup/code/JSON estimate-yield recipes |
| Modify | `skills/source-extract-fidelity/SKILL.md` | Add text/config/code traceability checks and overclaim cases |
| Modify | `skills/page-shape-contract/SKILL.md` | Add wave-1 page/row shape requirements for estimate/yield, route target, parse status, visibility, and public token abstraction |
| Modify | `skills/public-private-routing/SKILL.md` | Add wave-1 public/private route checks for JSON/config/code-derived output |
| Modify | skill eval JSON files listed in Artifact Map | Add executable cases for the always-used wave-1 skill group |
| Modify | `docs/01-document-taxonomy.md` | Clarify LLM-native text/markup/code/config lane classification |
| Modify | `docs/10-structured-data-and-model-files.md` | Add small JSON/config metadata handling and generated JSON exclusion guidance |
| Conditional modify or follow-on | `docs/14-chunking-and-embedding.md`, `docs/15-retrieval-evaluation.md`, `docs/16-corpus-lifecycle.md` | If [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved and implemented before [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) implementation, add small text/config/code handling for chunking, eval exclusion, and trust reset; otherwise record this as a follow-on rather than redefining [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) |
| Modify | `.github/workflows/validate.yml` | Run `uv run python scripts/validate_ace_wave1_text_json.py` and related tests |
| Modify | `docs/plans/README.md` | Update [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) status once review evidence exists |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Update the [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) ledger row once review evidence exists |
| Edit or comment | [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) | Correct or explicitly supersede the stale issue-body blocker that attributes wave-0 ledger/routing to [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50); after the reviewed commit is pushed, record commit SHA, review artifacts, validation evidence, and implementation block before applying `status:plan-review` |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_contract_imports_route_targets_from_wave0_schema` | Route vocabulary imports [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) instead of redefining it | Wave-0 schema and wave-1 contract | Only canonical route targets pass |
| `test_sampling_request_uses_downstream_manifest_backed_class_for_issue_52` | [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) remains an ingestion wave requiring manifest snapshot evidence | Wave registry and sample manifest fixture | `requires_manifest_snapshot_id=true` and canonical success fields are enforced |
| `test_operational_sampling_fails_closed_without_trusted_62_pointer` | Operational sampling cannot rely on self-attested [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence | Empty trusted evidence registry and sample request | Validator rejects operational sampling |
| `test_cap_violating_sampling_request_is_rejected` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) sampling caps are enforced | Request exceeding row, file, or byte caps | Validator rejects request |
| `test_generated_json_detected_by_shape_not_extension` | Generated JSON routing is content/schema-based | Manual config JSON and repetitive generated JSON fixtures | Config routes `metadata_only`; generated routes `excluded_no_ingest` |
| `test_manual_small_json_routes_metadata_only` | Hand-authored config JSON is not treated as prose ingest by extension | `manual-config.json` | Candidate routes `metadata_only` unless explicitly cleared |
| `test_repetitive_json_excluded_by_content_signals` | Repetitive generated JSON is excluded by shape/content | `generated-repetitive-json.json` and `generated-lockfile-like.json` | Candidates route `excluded_no_ingest` |
| `test_source_tree_not_bulk_ingested` | Source trees are not recursively dumped | `source-tree-docstring.py` and `source-tree-vendored-minified.js` | Source-tree noise routes exclude/metadata-only; doc-bearing code routes metadata-only unless explicitly cleared |
| `test_exclusions_precede_value_ranking` | Security/routing beats usefulness | Useful-looking synthetic fixture with exclusion marker placeholder | Candidate routes private/excluded before value scoring |
| `test_kept_rows_require_extraction_estimate_and_yield` | Kept rows carry coverage fields | Kept text/config rows | `extraction_estimate` and `extraction_yield` are present and non-empty |
| `test_route_targets_use_closed_enum` | Candidate rows cannot invent route targets | Candidate rows with valid and invalid routes | Invalid route fails |
| `test_success_metric_uses_successful_routed_items_over_eligible_candidate_items` | `% ingested success` uses canonical numerator/denominator | Normal pilot rows and zero-eligible fixture | Numerator, denominator, status, threshold, and command fields pass |
| `test_public_route_requires_63_gate_or_demotes` | Public route is blocked unless [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) certification exists | Missing [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) canary evidence | Public candidate demotes or fails |
| `test_durable_output_fields_require_61_gate` | Durable target paths, retrieval metadata, lifecycle state, and persistent metrics stay blocked while [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is unapproved | Candidate rows carrying durable store or lifecycle fields without [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) implemented evidence | Validator rejects or strips durable fields |
| `test_committed_fixtures_are_public_scan_safe` | Public artifacts and fixtures remain scan-clean | Plan, report, contract, validator, tests, fixtures, skill docs/evals, review artifacts | Public-surface and legal scans pass |

---

## Plan-Review Verification Commands

These checks will run before the issue can move to `status:plan-review`. The final review round may be r2 or later; replace the review artifact paths below with the final no-MAJOR round before posting evidence. Gemini unavailability is acceptable only as an explicit `UNAVAILABLE` artifact; two usable active-provider results with no MAJOR are required. The plan, coordination docs, and final review artifacts must be committed and pushed before the evidence comment and label change.

```bash
ISSUE_52_COMMENT_BODY=scripts/review/results/2026-07-02-plan-52-issue-comment.md
uv run python scripts/validate_ace_epic_wave_coordination.py
uv run python scripts/validate_ace_wave0_schema_contract.py
uv run python scripts/validate_ace_public_surface_scan.py \
  --scan-public-path docs/plans/2026-06-29-issue-52-ace-wave-1-llm-native-text-markup-code-small-json-bootstrap.md \
  --scan-public-path docs/plans/README.md \
  --scan-public-path docs/plans/ace-share-ingestion-wave-coordination.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-52-claude-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-52-codex-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-52-gemini-r2.md \
  --scan-public-path ${ISSUE_52_COMMENT_BODY}
bash scripts/legal/legal-sanity-scan.sh \
  --scan-public-path docs/plans/2026-06-29-issue-52-ace-wave-1-llm-native-text-markup-code-small-json-bootstrap.md \
  --scan-public-path docs/plans/README.md \
  --scan-public-path docs/plans/ace-share-ingestion-wave-coordination.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-52-claude-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-52-codex-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-52-gemini-r2.md \
  --scan-public-path ${ISSUE_52_COMMENT_BODY}
bash scripts/legal/legal-sanity-scan.sh --diff-only
git diff --check
```

If [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) is still unimplemented at review time, only generic `--scan-public-path` mode will be claimed.

---

## Acceptance Criteria

- [ ] The wave-1 contract classifies every candidate into `public_llm_wiki`, `private_sidecar`, `metadata_only`, or `excluded_no_ingest` without redefining the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) route vocabulary.
- [ ] Generated/repetitive JSON is detected by schema/content signals, not `.json` extension alone.
- [ ] Code/source-tree material is never bulk-ingested recursively; code files are routed to metadata/docstring/config extraction only when they carry durable knowledge value and pass exclusion gates.
- [ ] Hard exclusions and public/private routing run before value ranking and before public target selection.
- [ ] Kept rows record extraction estimate and extraction yield.
- [ ] `% ingested success` uses `successful_routed_items / eligible_candidate_items * 100`; generated/noise/hard exclusions are reported separately and zero-denominator cases use a closed status.
- [ ] Manifest-backed sampling records [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot evidence, uses a [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) trusted evidence-registry pointer, and passes [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) bounded sampling controls before sample selection; an empty or missing trusted registry entry fails closed.
- [ ] Durable stores, target paths, retrieval metadata, lifecycle state, and persistent metrics remain blocked until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) has user approval, local approval marker, implemented validator, and recorded passing-command evidence.
- [ ] Public-facing reports, docs navigation, `mkdocs.yml`, `llm-wiki`, GitHub-public corpus summaries, and external publication exposure remain blocked until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has user approval, local approval marker, implemented canary, and recorded passing-command evidence.
- [ ] Any committed `docs/` wave-1 page is synthetic-fixture-only before [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63); measured ACE-derived corpus results remain private sidecar output and are not committed, commented, or published.
- [ ] The reviewed plan, coordination docs, and final review artifacts are committed and pushed before the [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) evidence comment or `status:plan-review` label.
- [ ] The [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) evidence comment body is rendered to `scripts/review/results/2026-07-02-plan-52-issue-comment.md`, scanned with public-surface and legal scanners before posting, posted to the issue, and removed from the worktree before the final `--diff-only` scan.
- [ ] The stale [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) issue-body blocker is corrected or explicitly superseded.
- [ ] Wave-1 skill updates and eval cases land for `content-triage-and-exclusion`, `source-extraction-coverage`, `source-extract-fidelity`, `page-shape-contract`, and `public-private-routing`.
- [ ] `uv run python scripts/validate_ace_wave1_text_json.py`, `uv run python -m unittest tests.test_validate_ace_wave1_text_json`, `uv run skills/validate_skill.py`, public-surface scan, legal scan, coordination validators, and `git diff --check` pass.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Found unsafe raw Gemini artifact retention, measured `docs/` report publication contradiction, [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) split/integration wording drift, missing [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61)/[#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) negative tests, underspecified plan-review/comment scans, and stale issue-body blocker. Findings patched in this draft. |
| Codex r1 | MAJOR | Found measured `docs/` report publication contradiction, unsafe/missing review-evidence scan set, Gemini state drift, stale issue-body blocker, and missing issue-comment scan. Findings patched in this draft. |
| Gemini r1 | UNAVAILABLE | Gemini CLI failed before returning findings due unsupported-client/ineligible-tier. Raw stderr was not retained because it contained local host paths. |
| Claude r2 | MINOR | Found repo-local issue-comment scan path ambiguity, missing explicit pushed-evidence requirement, and final-round review bookkeeping lag. Findings patched in this draft. |
| Codex r2 | MINOR | Found missing explicit pushed-evidence requirement and repo-local issue-comment scan path ambiguity. Findings patched in this draft. |
| Gemini r2 | UNAVAILABLE | Gemini CLI failed before returning findings due unsupported-client/ineligible-tier. Raw stderr was not retained because it contained local host paths. |

**Overall result:** PLAN-REVIEW READY - r1 returned active-provider MAJOR findings, then r2 returned Claude MINOR and Codex MINOR with no usable active-provider MAJOR. Gemini was unavailable in both rounds. This draft patches the r2 findings and remains blocked from implementation until the user approves [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52), applies `status:plan-approved`, and creates `.planning/plan-approved/52.md`.

---

## Risks and Open Questions

- **Risk:** [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains a draft umbrella. This wave may consume closed split contracts [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) plus closed manifest-evidence integration [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70), but it must not claim the [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) umbrella itself is approved.
- **Risk:** JSON generatedness can be ambiguous; implementation will need false-positive and false-negative fixtures for config JSON versus generated caches, lockfiles, package indexes, and repeated telemetry-like objects.
- **Risk:** [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) validator evidence can exist while [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) trusted evidence registry has no trusted pointer for operational sampling. [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) must treat that as blocked sampling, not as implicit authorization.
- **Risk:** A public-safe methodology report can still leak by prose. The public-surface and legal scans must cover reports, review artifacts, tests, fixtures, and issue comments before commit/comment.
- **Risk:** [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) remains unapproved. [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) can define wave-1 method contracts, but durable output, target paths, retrieval metadata, lifecycle state, and persistent metrics remain blocked.
- **Risk:** [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) remains unapproved. Public exposure remains blocked even if [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) creates scan-clean methodology artifacts.
- **Risk:** [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) remains unimplemented. Review and validation must use generic public scans only.
- **Risk:** `docs/` is deployed through MkDocs/Pages even for pages not listed in navigation. Before [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63), any [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) `docs/` artifact must stay synthetic-fixture-only and must not include measured ACE-derived corpus summaries.
- **Open:** If implementation discovers reusable JSON/schema filtering rules beyond this lane, closeout must either update the relevant skill/doc/eval or file a follow-on issue before close.

---

## Complexity

**T2** - focused docs/skill/resource change with one validator, synthetic fixtures, and no broad ingestion system. Complexity would become T3 only if implementation expands into durable stores, retrieval metadata, or publication surfaces, which are explicitly blocked by cross-wave gates.
