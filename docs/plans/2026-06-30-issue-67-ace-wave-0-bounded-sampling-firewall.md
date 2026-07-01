# Plan for #67: ACE Wave 0 Bounded Sampling Firewall

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-30
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** r5 Claude/Codex MAJOR; Gemini unavailable

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
- Source: [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) `bound_skill_groups`
  - Finding: The inherited method surface is exactly `format-coverage-ledger`, `public-private-routing`, `content-triage-and-exclusion`, `page-shape-contract`, and `adversarial-verify-loop`. [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will not substitute `source-extraction-coverage` for `page-shape-contract`; any reusable extraction-coverage method gap will be routed to a follow-on issue unless a later approved schema change adds that skill group.

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

- Before this draft, no standalone [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) plan existed; this plan fills that planning gap but remains unreconciled after r5 MAJOR review until the next patch/re-review cycle passes.
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
| Conditional skill docs | `skills/format-coverage-ledger/SKILL.md`, `skills/public-private-routing/SKILL.md`, `skills/content-triage-and-exclusion/SKILL.md`, `skills/page-shape-contract/SKILL.md`, `skills/adversarial-verify-loop/SKILL.md` |
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
| Provider stderr sidecars | not retained unless normalized, scanned, and explicitly listed |

---

## Deliverable

After approval and implementation, [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will provide a repo-local bounded sampling firewall contract, executable-context classifier, validator, fixtures, tests, and CI wiring that reject unbounded ACE sampling commands while allowing metadata-only bounded sampling requests with recorded [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence where required.

---

## Proposed Contract Shape

The implementation will create a closed JSON contract with these top-level fields:

| Field | Proposed rule |
|---|---|
| `contract_id` | exactly `ace-bounded-sampling-firewall` |
| `contract_version` | semver under `1.0.x` |
| `owner_issue` | exactly `67` |
| `depends_on_schema_issue` | exactly `65` |
| `allowed_manifest_sources` | exactly the six public metadata keys listed in this plan's Source inventory |
| `required_sampling_fields` | target issue, manifest source, seed, sort rule, per-bucket row cap, maximum files touched, maximum bytes touched, request class, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence requirement, output shape, and either a #65 target wave class for operational requests or a #67 fixture scope for metadata-only fixtures |
| `maximum_caps` | per-bucket row cap no greater than `200`, maximum files touched no greater than `25`, maximum bytes touched no greater than `1048576`, matching the coordination ledger bounded-read contract |
| `request_classes` | `control_plane_proof`, `downstream_manifest_backed_sampling`, and `metadata_only_fixture`; request class must match the closed mapping table below |
| `target_issue_gate` | target issues [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) must use `downstream_manifest_backed_sampling`; exempt classes are invalid for those issues |
| `seed_rule` | fixed, reviewable seed identifiers only; random, clock-derived, user-local, or unstated seeds fail |
| `sort_rule` | exactly the closed JSON shape in `Sort Rule Shape`; #65 private schema terms may appear only as array values; no raw private values, raw private-key assignments, or unknown sort keys are allowed |
| `downstream_snapshot_gate` | [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) fail closed for operational sampling until [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) defines an evidence contract and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) imports it into [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) |
| `snapshot_evidence_schema` | neutral keys for evidence mode, source issue, blocked-by issue, follow-on issue, reason code, optional shape-only artifact reference, and recorded-at date |
| `metadata_fixture_scope` | exactly `firewall_validator_self_check`; valid only when `target_issue=67` and `request_class=metadata_only_fixture` |
| `executable_context_triggers` | closed enum for markdown fence, markdown list command, markdown inline command, workflow run block, Python string passed to classifier, and JSON request field |
| `command_verb_classes` | closed enum for traversal, broad search/list, manifest query, raw manifest read, full-file fingerprint/count, and full materialization |
| `source_root_token_classes` | closed enum for ACE root abstraction, manifest key token, and synthetic fixture token |
| `manifest_operation_classes` | closed enum for bounded metadata probe, bounded sample selection, snapshot evidence check, and denied unbounded operation |
| `denied_executable_classes` | recursive traversal, broad list/search over the source root, unrestricted manifest query, raw manifest read, full-file hashing/counting of large manifests, and unbounded materialization |
| `public_safety_notes` | no private source content, raw host paths, raw source values, raw digests, exact private inventory counts, client identifiers, personal identifiers, or publication destinations |

The implementation will not create public tokens, private lookup maps, durable storage locations, manifest freshness snapshots, public-output canaries, legal/security scans, docs navigation, or publication outputs.

### Request Class Mapping

| Target issue set | Target wave class or fixture scope | Allowed request class | Snapshot gate |
|---|---|---|---|
| [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) | `ingestion_wave` | `downstream_manifest_backed_sampling` | full [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) recorded evidence required |
| [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) | `control_plane` | `control_plane_proof` | no live [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) execution required |
| [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) | `storage_lifecycle_gate` | `control_plane_proof` | no live [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) execution required |
| [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) | `manifest_freshness_gate` | `control_plane_proof` | no self-dependency on [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence |
| [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) | `public_canary_gate` | `control_plane_proof` | no live [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) execution required |
| [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) | `fixture_scope=firewall_validator_self_check` | `metadata_only_fixture` | shape-only fixture; invalid for [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) and cannot authorize operational sampling |

Operational requests must use a `target_wave_class` imported from the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) canonical wave registry. The [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) metadata-only fixture row intentionally uses `fixture_scope` instead of `target_wave_class` because [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) is a split control-plane validator issue, not a canonical ingestion wave. Any request whose `target_issue`, target class/scope, and `request_class` do not match this table will fail.

[#64](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/64) is a planning placeholder outside the #65 canonical wave registry and the wave-0 split registry; it is not a sampling-request target. [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66), [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68), and [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) are split control-plane support issues that own token fixtures, public-surface scanning, and legal/security scanning. They will fail closed as sampling-request targets unless a later approved plan explicitly adds metadata-only fixture scopes for them.

### Snapshot Evidence Shape

For `downstream_manifest_backed_sampling`, the request will carry a `snapshot_evidence` object with these neutral fields:

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
| Markdown fenced code | fence language is shell-like, Python-like, SQL-like, JSON-query-like, YAML workflow-like, or explicitly tagged as a command/proof block |
| Markdown list command | the list item begins with a shell prompt marker or a command verb and is under a command/proof/run heading |
| Markdown inline code | the surrounding sentence introduces it as a command to run, proof command, allowed command, rejected command, or script invocation |
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
  manifest source is present and allowed
  seed is present, fixed, reviewable, and not random or clock-derived
  sort rule has exactly strategy, term_refs, direction, and tie_breaker keys
  sort term_refs use #65 private schema terms as values only
  unknown sort keys, raw private value expressions, and assigned private-key forms fail
  per-bucket cap, max files touched, and max bytes touched are positive integers
  caps do not exceed 200 rows, 25 files, or 1048576 bytes
  output shape is metadata-only and route/store values come from #65 schema
validate downstream sampling gate:
  target issues #52-#60 require downstream_manifest_backed_sampling
  target issues #52-#60 reject control_plane_proof and metadata_only_fixture
  #64, #66, #68, and #69 are explicitly non-targets unless later approved scopes exist
  downstream_manifest_backed_sampling requires a complete snapshot_evidence object
  operational ingestion-wave requests fail closed with MISSING_62_EVIDENCE_CONTRACT
  operational ingestion-wave requests record blocked_by_issue=62 and follow_on_issue=70
  request-provided operational_live evidence fails because #70 owns that parser
  controlled fixtures, not ambient repo state, cover missing-#62 negative cases
  shape-only fixtures can pass schema parsing but cannot authorize sampling
  placeholder, negated, pending, not-run, forged, or expected-only evidence fails
  control-plane proof and metadata-only fixture classes do not require live #62 execution
validate executable contexts:
  markdown, workflow, Python, and JSON contexts are classified by closed rule families
  executable_context_triggers, command_verb_classes, source_root_token_classes,
  and manifest_operation_classes are closed enums in the contract
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
  full-file hashing/counting of large manifests fails unless a later approved issue
  explicitly supplies a bounded precomputed sidecar contract
validate public-safety boundaries:
  no raw private source paths, raw source values, source-like digest assignments,
  client identifiers, personal identifiers, proprietary snippets, or exact private counts
validate public-surface path list using parent scanner:
  this plan, README, coordination ledger, schema split registry, contract JSON,
  classifier, validator, unit tests, safe fixtures, workflow, changed skill docs,
  approval marker when present, and retained plan-67 review artifacts
  provider stderr sidecars are either deleted or explicitly normalized and scanned before retention
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
| Conditional modify or follow-on | Bound skill docs listed in Artifact Map | Update only if implementation reveals a reusable method gap and changed skill docs pass the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) public scan; otherwise file a follow-on issue |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_contract_file_is_json_and_owned_by_67` | Contract is machine-readable and issue-scoped | Contract JSON | Loads with `contract_id`, version, owner issue, schema dependency, and public-safety notes |
| `test_contract_imports_65_schema_terms` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) consumes, not redefines, [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) terms | Contract plus #65 schema | Route/store/success/private-term references and bound skill groups match #65 exactly |
| `test_allowed_manifest_sources_are_closed` | Manifest source set cannot drift | Contract manifest source list | Exactly the six public metadata keys are allowed |
| `test_bounded_sampling_fields_are_required` | Sampling request grammar is complete | Synthetic request missing one field at a time | Missing target issue, operational target wave class or fixture scope, manifest source, seed, sort rule, per-bucket cap, max files, max bytes, request class, or output shape fails |
| `test_sampling_caps_are_enforced` | Caps cannot exceed the coordination-ledger bounded-read contract | Synthetic requests with above-limit caps | Requests over 200 rows, 25 files, or 1048576 bytes fail |
| `test_request_class_mapping_covers_every_allowed_target` | Mapping table is explicit for all allowed target classes and explicit non-targets | Contract mapping table | #51, #52-#60, #61, #62, #63, and the #67 fixture scope are covered; #64, #66, #68, and #69 fail with non-target reasons |
| `test_request_class_must_match_target_wave` | Downstream waves cannot self-select an exempt class | Synthetic request for [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) with exempt request class | Fails with target issue/wave mismatch |
| `test_downstream_sampling_requires_62_snapshot_evidence` | Manifest-backed ingestion waves cannot sample without [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence | Synthetic downstream request without complete evidence | Fails with [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) gate error |
| `test_downstream_shape_only_fixture_accepts_complete_62_evidence_shape` | Positive #62 evidence shape is parseable without authorizing sampling | Shape-only [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) fixture with complete public-safe evidence object | Passes schema parsing and remains invalid for operational downstream sampling |
| `test_downstream_sampling_fails_with_missing_62_evidence_fixture` | Missing authoritative [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence fails without depending on ambient repo state | Controlled temp fixture with no #62 evidence artifact | Fails with missing-evidence-contract error |
| `test_downstream_operational_sampling_blocked_until_70` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) does not invent the [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence parser | Synthetic downstream request with `operational_live` evidence claims | Fails with `MISSING_62_EVIDENCE_CONTRACT` and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) reference |
| `test_placeholder_snapshot_evidence_fails` | Placeholder gate evidence cannot satisfy [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) requirement | Synthetic request using pending/not-run/expected wording | Fails with placeholder evidence error |
| `test_control_plane_fixture_does_not_require_live_62` | CI can validate #67 before #62 implementation | Metadata-only control-plane fixture | Passes without `ACE_SHARE_ROOT` and without live [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) execution |
| `test_validator_refuses_private_reads_when_ace_share_root_is_set` | The firewall does not read private source content even when a root abstraction is configured | Temp `ACE_SHARE_ROOT` with sentinel files plus metadata-only fixture | Passes without reading sentinel content and fails any attempted source-root traversal |
| `test_seed_rule_rejects_unstable_values` | Seed grammar is deterministic | Synthetic requests with random, clock-derived, empty, or user-local seeds | Fails with seed rule error |
| `test_sort_rule_references_65_private_terms_safely` | Sort grammar does not invent row-key semantics or expose private values | Synthetic sort rule fixtures | Exact keys `strategy`, `term_refs`, `direction`, and `tie_breaker` pass; unknown keys, private-term keys, assigned private values, or raw values fail |
| `test_manifest_source_authority_matches_coordination` | Six-key source enum comes from the coordination ledger | Contract and coordination ledger | Contract source list matches coordination keys exactly |
| `test_parent_manifest_helper_is_not_67_source_authority` | Parent scanner helper cannot silently narrow #67 source enum or require broad generic filename matching | Parent validator constants and #67 contract | #67 treats the contract and coordination ledger as source authority and does not require parent helper expansion |
| `test_denied_vocabularies_sync_with_parent_scanner` | #67 does not fork the parent scanner's denied vocabulary silently | Parent scanner constants plus #67 contract | Shared denied classes match or a deliberate #67-only extension is listed with a test |
| `test_classifier_vocabularies_are_closed` | The classifier's core vocabularies are contract data, not implementation guesswork | Contract executable trigger, command verb, source-root token, and operation-class lists | Exact closed enum sets are present; unknown values fail |
| `test_markdown_fenced_command_context_is_executable` | Fenced command examples are scanned as executable | Runtime-built markdown fixture | Runnable denied source-root expression fails |
| `test_markdown_policy_prose_context_is_non_executable` | Policy prose can name denial classes safely | Policy paragraph with no runnable source-root expression | Passes classifier |
| `test_workflow_run_context_is_executable` | Workflow run blocks are scanned | Runtime-built workflow fixture | Runnable denied source-root expression fails |
| `test_python_literal_context_is_executable_when_fed_to_classifier` | Test/code strings sent to classifier cannot hide denied commands | Runtime-assembled Python string fixture | Denied command fixture fails |
| `test_json_request_command_context_is_executable` | Request fields carrying commands are scanned | Runtime-built JSON request | Denied command fixture fails |
| `test_unknown_runnable_context_fails_closed` | Ambiguous executable-looking text cannot bypass the firewall | Synthetic unknown context | Fails closed |
| `test_recursive_traversal_class_is_denied` | Recursive source-root traversal is blocked | Runtime-assembled denied fixture | Fails validation |
| `test_broad_source_root_search_class_is_denied` | Broad list/search over the source root is blocked | Runtime-assembled denied fixture | Fails validation |
| `test_unrestricted_manifest_query_class_is_denied` | Unbounded manifest query is blocked | Runtime-assembled denied fixture | Fails validation |
| `test_raw_manifest_read_class_is_denied` | Raw manifest read examples are blocked | Runtime-assembled denied fixture | Fails validation |
| `test_full_file_hashing_or_counting_class_is_denied` | Full-file hashing/counting of large manifests is blocked | Runtime-assembled denied fixture | Fails unless bounded sidecar contract is explicitly cited |
| `test_committed_fixtures_are_public_scan_clean` | Safe fixtures do not self-block public scan | Committed fixture directory | Parent public scanner returns no errors |
| `test_negative_fixtures_are_runtime_only` | Deny examples are not committed as public strings | Test source and fixture files | Denied examples are assembled from fragments or temp files |
| `test_classifier_source_is_public_scan_clean` | Detection source survives parent scanner without broad exemptions | Classifier, validator, tests, and contract source text | Parent scanner passes; denied command, source-root, and recursive API examples are assembled from fragments at runtime |
| `test_validator_source_avoids_unbounded_discovery` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator does not need broad self-exemptions | Validator/test source text | No unbounded repo/source-root traversal APIs are used for discovery |
| `test_public_safety_rejects_private_leaks` | Public artifacts do not expose private/source-like values | Runtime-built leak fixtures | Raw paths, private values, source-like digest assignments, personal identifiers, client identifiers, and proprietary snippets fail |
| `test_public_scan_paths_cover_67_artifacts` | Self-scan cannot omit a public artifact | Validator public path list | Plan, README, coordination, schema split registry, contract, classifier, validator, tests, fixtures, workflow, changed skills, approval marker when present, and retained review artifacts are included |
| `test_wave0_split_registry_records_67_plan_status` | The #67 split row cannot remain stale after implementation | #65 schema artifact and #67 plan/status inputs | #67 `plan_path`, `status_snapshot`, and `implementation_ready` match the current gate state |
| `test_review_sidecars_are_not_retained_unscanned` | Provider stderr sidecars cannot bypass public scan | Review output directory with sidecars | Sidecars are deleted or normalized and scanned before retention |
| `test_ci_invokes_67_validator_and_unit_tests` | CI will enforce the contract after implementation | Workflow YAML | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator and unit test commands are present |
| `test_schema_and_parent_validators_still_pass` | [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) does not regress existing gates | Existing validators | #65 schema validator and parent coordination validator pass |

---

## Acceptance Criteria

- [ ] A standalone issue plan exists for [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67), passes adversarial plan review, and remains blocked from implementation until user approval.
- [ ] `config/ace-bounded-sampling-firewall-contract.json` defines a closed [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) contract with owner issue, schema dependency, allowed manifest sources, required sampling fields, cap maxima, request classes, denied executable classes, downstream [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence rules, and public-safety notes.
- [ ] Every operational sampling request records a target issue and target wave class imported from the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) canonical wave registry; [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) metadata-only fixtures record `fixture_scope=firewall_validator_self_check` instead and cannot authorize operational sampling.
- [ ] Downstream wave requests for [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) cannot use exempt request classes to bypass [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot evidence.
- [ ] Request-class mapping is explicit for `control_plane`, `ingestion_wave`, `storage_lifecycle_gate`, `manifest_freshness_gate`, `public_canary_gate`, and the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) synthetic fixture scope.
- [ ] [#64](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/64), [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66), [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68), and [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) fail closed as sampling-request targets with explicit non-target reasons unless a later approved plan adds scopes for them.
- [ ] The contract defines closed enums for executable triggers, command verb classes, source-root token classes, and manifest operation classes.
- [ ] Seed grammar rejects random, clock-derived, empty, user-local, or otherwise non-reviewable seeds.
- [ ] Sort grammar uses exactly `strategy`, `term_refs`, `direction`, and `tie_breaker`; #65 private schema terms appear only as `term_refs` values; unknown sort keys, raw private values, and assigned private-key forms fail.
- [ ] Manifest source authority is the six-key set in `docs/plans/ace-share-ingestion-wave-coordination.md`; parent scanner helper patterns are explicitly tested as non-authoritative for [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) source enumeration.
- [ ] [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) imports or reads [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema vocabulary and fails on drift rather than duplicating route/store/success/private-term enums.
- [ ] The executable-context classifier distinguishes policy prose from runnable shell, Python, query, workflow, inline command, and JSON request contexts using closed rules.
- [ ] Unknown runnable-looking contexts fail closed when they carry a source-root abstraction and command-like syntax.
- [ ] Denied executable classes cover recursive traversal, broad source-root list/search, unrestricted manifest query, raw manifest read, full-file hashing/counting of large manifests, and unbounded materialization.
- [ ] Bounded sampling requests require target issue, manifest source, deterministic seed, sort rule, per-bucket row cap, max files touched, max bytes touched, request class, metadata-only output shape, and either operational target wave class or metadata-only fixture scope.
- [ ] Sampling caps are bounded to no more than 200 rows per bucket, 25 files touched, and 1048576 bytes touched, matching the coordination-ledger bounded-read contract, unless a later approved issue changes that contract.
- [ ] Manifest-backed downstream waves fail closed with `MISSING_62_EVIDENCE_CONTRACT`, `blocked_by_issue=62`, and `follow_on_issue=70` until [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) defines an evidence schema and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) imports it; shape-only fixtures and request self-attestation cannot satisfy this gate.
- [ ] [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) does not implement [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) freshness, [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) token generation, [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) reusable public-surface scanning, [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) legal/security scanning, [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) durable storage, or [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) publication certification.
- [ ] The validator passes with `ACE_SHARE_ROOT` unset and refuses to read private source content when `ACE_SHARE_ROOT` is set to a temp sentinel tree.
- [ ] Public artifacts do not publish raw private source paths, raw source values, source-like digest assignments, exact private inventory counts, client identifiers, personal identifiers, proprietary snippets, or publication destinations.
- [ ] Negative fixtures are generated at runtime or written to temp files outside the repo tree; committed fixtures and scanner-triggering API-token examples remain scan-clean.
- [ ] The [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator invokes the parent public scanner over the complete [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) public path list, including `artifacts/ace-wave0-ledger-schema.json`, and does not create the generalized scanner owned by [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68).
- [ ] The #67 row in `artifacts/ace-wave0-ledger-schema.json` records this plan path, gate-accurate `status_snapshot`, and `implementation_ready=false` until the user approval and implementation gates advance.
- [ ] Provider stderr sidecars are not retained unless normalized, explicitly listed, and scanned.
- [ ] `.github/workflows/validate.yml` runs the [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) validator and unit tests after implementation.
- [ ] `uv run python scripts/validate_ace_bounded_sampling_firewall.py` passes after implementation.
- [ ] `uv run python -m unittest tests.test_validate_ace_bounded_sampling_firewall` passes after implementation.
- [ ] `uv run python scripts/validate_ace_wave0_schema_contract.py` still passes after implementation.
- [ ] `uv run python scripts/validate_ace_epic_wave_coordination.py` still passes after implementation.
- [ ] `uv run skills/validate_skill.py` still passes after implementation.
- [ ] If implementation reveals a reusable method gap, the bound skill docs are updated or a follow-on issue is filed before closeout.
- [ ] If `scripts/legal/legal-sanity-scan.sh` is still unavailable at closeout, full closeout remains blocked; the issue comment records `NO_LEGAL_SCAN_SCRIPT` and points to [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).

---

## Focused Self-Scan Before Formal Review

- [ ] Closed grammar fields are enumerated, including [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence fields.
- [ ] Executable-context rules are parseable and closed.
- [ ] Denied executable classes are complete without embedding runnable denied examples in committed public files.
- [ ] Dependencies stay narrow: [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) required, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) required for downstream sampling evidence, [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66)/[#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)/[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) not required.
- [ ] CI and public-scan paths include every [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) artifact and no broad whole-directory exemption.
- [ ] Public artifacts carry no private-source assignment, source-like digest assignment, raw local path, personal identifier, or concrete client/project identifier.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Found self-scanner contradiction, under-specified classifier rule, manifest-source authority drift, stale Files-to-Change wording, CI command mismatch, and registry scan reflexivity. Current draft patches these findings; re-review required. |
| Codex r1 | MAJOR | Found #62 gate bypass by request-class self-selection, missing sort-key contract, weak seed/sort tests, legal-scan closeout downgrade, missing review-sidecar disposition, and stale plan-existence wording. Current draft patches these findings; re-review required. |
| Gemini r1 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r2 | UNAVAILABLE | CLI invocation failed before returning a usable review; no signal. |
| Codex r2 | MAJOR | Found missing request-class mapping, missing closed classifier vocabularies, no positive #62 evidence schema/fixture, and open-ended legal-scan deferral. Current draft patches these findings; re-review required. |
| Gemini r2 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r3 | MAJOR | Found nonexistent #67 wave-class mapping, retained legal-scan deferral, parent-helper blast-radius risk, incomplete self-block mitigation, missing downstream shape fixture, and stale review artifact inventory. Current draft patches these findings; re-review required. |
| Codex r3 | MAJOR | Found nonexistent #67 wave-class mapping, synthetic #62 evidence bypass, unclosed sort grammar, and stale retained-artifact inventory. Current draft patches these findings; re-review required. |
| Gemini r3 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r4 | MAJOR | Found #65 bound-skill drift, guessed #62 interface, environment-coupled #62 absence test, uncited cap authority, status-only #62 semantics, incomplete fixture inventory, and unexplained non-target issues. Current draft patches these findings; re-review required. |
| Codex r4 | MAJOR | Found malformed approval-marker bypass risk, self-attested #62 evidence gap, and incomplete downstream shape fixture inventory. Current draft patches these findings; re-review required. |
| Gemini r4 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |
| Claude r5 | MAJOR | Found unresolved #62 evidence-artifact schema ownership, missing private-read-refusal test, parent-test coupling, and possible denied-vocabulary drift. Current draft patches these findings; re-review required. |
| Codex r5 | MAJOR | Found missing schema split registry public-scan coverage and missing TDD assertion for the #67 split-registry plan/status update. Current draft patches these findings; re-review required. |
| Gemini r5 | UNAVAILABLE | Installed client returned unsupported/ineligible-tier authentication error; no usable review signal. |

**Overall result:** MAJOR - draft only; not ready for `status:plan-review`.

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
