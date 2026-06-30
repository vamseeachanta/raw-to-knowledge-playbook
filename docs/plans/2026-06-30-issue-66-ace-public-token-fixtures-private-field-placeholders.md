# Plan for #66: ACE Wave 0 Public-Token Fixtures and Private-Field Placeholders

> **Status:** draft
> **Complexity:** T2
> **Date:** 2026-06-30
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** see Artifact Map below for r1-r3 artifacts

---

## Resource Intelligence Summary

### Existing repo code/docs

- `artifacts/ace-wave0-ledger-schema.json` will provide the route targets, logical target stores, public-token field name, private source field terms, and split dependency order that #66 must consume.
- `scripts/validate_ace_wave0_schema_contract.py` will remain the #65 schema validator. #66 will add a separate fixture validator rather than weakening #65's schema-local public scan.
- `scripts/validate_ace_epic_wave_coordination.py` will remain the parent coordination validator and current public-surface fallback scanner until #68 generalizes that scanner.
- `.github/workflows/validate.yml` will be extended with a repo-local #66 validator and unit test. CI will not require live GitHub or private source roots.
- `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` will record #66 as a draft plan with implementation readiness false.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) will remain the approved parent epic for coordination and planning.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will remain the wave-0 umbrella. It delegates this fixture-only scope to #66.
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) provides the committed schema and route-store matrix that #66 will import.
- [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) will use #66's placeholder grammar as an input to the generic public-surface self-scan contract.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) will remain the owner of durable token lookup persistence and private storage behavior.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) co-owns the broader public-token policy and will remain the owner of public-output certification and production/publication canary behavior.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63)'s future `config/ace-public-output-contract.json` will be authoritative for production/publication token policy. #66's fixture contract will be subordinate and must reconcile with it when that #63 config exists.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will remain the owner of the repo-local legal/security scan command. #66 closeout will record `NO_LEGAL_SCAN_SCRIPT` and remain blocked from full close if that command is still absent.

### Source inventory

- #66 will not read private ACE content and will not require source-root environment variables.
- Fixture inputs will be synthetic generation request files and runtime-generated positive/negative fixture rows.
- Committed good fixtures will contain generation request markers, not hand-authored concrete public token values.
- Committed tests will build unsafe token/private-field cases from fragments at runtime or write them to temp files so public scan artifacts do not self-block.

### Gaps identified

- No fixture-only token contract exists yet.
- No validator exists to prove that fixture token generation ignores source/path/name/hash/key inputs.
- No closed placeholder grammar exists for private-only ledger fields in synthetic good fixtures.
- No test harness proves deterministic source-derived token examples and private-field value leaks fail.
- No CI step currently binds #66 to the #65 schema field vocabulary.
- #68 remains blocked until #66 supplies this placeholder grammar or #68 is explicitly narrowed before review.

### Evidence

**Issue status** (verified 2026-06-30):

```text
#66 OPEN ACE wave 0 split: public-token fixtures and private-field placeholders labels=strengthening,lane:codex,priority:high
```

**File existence** (verified 2026-06-30):

```text
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS .github/workflows/validate.yml
EXISTS docs/plans/README.md
EXISTS docs/plans/ace-share-ingestion-wave-coordination.md
EXISTS docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md
MISSING config/ace-public-token-fixture-contract.json
MISSING scripts/ace_public_token_fixtures.py
MISSING scripts/validate_ace_public_token_fixtures.py
MISSING tests/test_validate_ace_public_token_fixtures.py
MISSING tests/fixtures/ace-public-token-fixtures/good-request.json
MISSING .planning/plan-approved/66.md
MISSING scripts/legal/legal-sanity-scan.sh
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md` |
| Fixture contract | `config/ace-public-token-fixture-contract.json` |
| Fixture library | `scripts/ace_public_token_fixtures.py` |
| Fixture validator | `scripts/validate_ace_public_token_fixtures.py` |
| Unit tests | `tests/test_validate_ace_public_token_fixtures.py` |
| Synthetic request fixtures | `tests/fixtures/ace-public-token-fixtures/` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Workflow | `.github/workflows/validate.yml` |
| Review artifact - Claude r1 | `scripts/review/results/2026-06-30-plan-66-claude.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-06-30-plan-66-codex.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-06-30-plan-66-gemini.md` |
| Review artifact - disagreement r1 | `scripts/review/results/2026-06-30-plan-66-disagreement.md` |
| Review artifact - Claude r2 | `scripts/review/results/2026-06-30-plan-66-claude-r2.md` |
| Review artifact - Codex r2 | `scripts/review/results/2026-06-30-plan-66-codex-r2.md` |
| Review artifact - Gemini r2 | `scripts/review/results/2026-06-30-plan-66-gemini-r2.md` |
| Review artifact - disagreement r2 | `scripts/review/results/2026-06-30-plan-66-disagreement-r2.md` |
| Review artifact - Claude r3 | `scripts/review/results/2026-06-30-plan-66-claude-r3.md` |
| Review artifact - Codex r3 | `scripts/review/results/2026-06-30-plan-66-codex-r3.md` |
| Review artifact - Gemini r3 | `scripts/review/results/2026-06-30-plan-66-gemini-r3.md` |
| Review artifact - disagreement r3 | `scripts/review/results/2026-06-30-plan-66-disagreement-r3.md` |

---

## Deliverable

After approval and implementation, #66 will provide a fixture-only public-token generation request contract, closed private-field placeholder grammar, synthetic good/bad fixture harness, and repo-local validator that downstream #68 can use without allocating durable tokens for real records, accepting source-derived token inputs, or persisting private token lookup maps.

---

## Pseudocode

```text
load artifacts/ace-wave0-ledger-schema.json with Python stdlib json
load config/ace-public-token-fixture-contract.json with Python stdlib json

validate fixture contract metadata:
  fixture_contract_owner_issue is #66
  public_token_policy_owner_issues are imported from #65 as #66 and #63
  if config/ace-public-output-contract.json exists, fixture token prefix and
  public/private field policy must match that #63-owned contract
  if #63 config does not exist yet, #66 records provisional_fixture_contract=true
  mode is fixture_only
  schema_dependency points to #65 schema artifact
  durable lookup persistence owner remains #61
  publication certification owner remains #63
  public-surface scanner consumer is #68

validate imported schema terms:
  public token field name matches #65 schema
  private source field terms match #65 schema values
  source-like raw digest terms match #65 schema values
  route/store vocabulary comes from #65 schema
  no new route target or logical store enum is introduced

validate generation request grammar:
  committed good fixtures contain a generation request marker
  committed good fixtures do not contain hand-authored concrete public token values
  marker key is public_source_token_request
  marker value is an object with exactly:
    fixture_set_id
    fixture_row_id
    count
  fixture_set_id is a closed enum, initially wave0_public_token_good
  fixture_row_id matches fixture_row_<three digits>
  count is an integer from 1 through 100
  marker contains fixture-local ids only in those exact keys
  committed request markers contain no source identifiers, path fragments, hashes,
  private keys, lookup aliases, or deterministic seeds
  generator accepts fixture count and fixture set id only
  tests may inject a runtime random source to force duplicates and retry behavior
  generator rejects source, path, hash, private key, lookup, or raw provenance inputs
  generator also rejects name-derived inputs as #66 extra hardening, not as a
  #65 schema-derived field class
  concrete runtime token grammar is literal prefix pst_ plus exactly
  32 lowercase hexadecimal characters
  the validator and parent scanner agree this is the concrete-token assignment shape
  committed files may name the grammar but must never contain a concrete token
  literal as a field assignment or expected-output row
  emitted tokens are opaque fixture tokens and cannot be decoded into source-like parts
  duplicate tokens are retried deterministically under injected test randomness

validate private-field placeholder grammar:
  placeholder values are a closed set
  placeholders are accepted only inside parsed synthetic good fixtures
  placeholder fields are mapped to #65 private source field terms
  every committed machine-readable contract/config/fixture artifact represents
  private source field terms only as array/list values under neutral keys, never
  as JSON object keys, map keys, or the left side of a colon/equal assignment
  committed prose may name private source field terms only as policy/schema terms,
  never as assigned values or lookup maps
  placeholders are never treated as durable private values
  placeholder maps keyed by private source field terms are always rejected
  grammar prose is distinguished from parsed fixture content by parser context,
  not by raw substring allowlisting

validate bad fixtures:
  source-derived token attempts fail
  path-derived token attempts fail
  name-derived token attempts fail
  hash-derived token attempts fail
  fixed-seed token attempts fail
  private lookup derived token attempts fail
  hand-authored concrete public token assignments fail
  malformed request markers fail
  unknown placeholder kinds fail
  private-field value leaks fail
  durable token lookup persistence attempts fail

validate public scan safety:
  plan, contract, scripts, tests, request fixtures, workflow, README, coordination,
  approval marker when present, and retained plan review artifacts pass the
  current parent public-surface scan
  raw negative examples are built at runtime or written to temp files
  self-scanned Python modules and tests construct forbidden private-source terms
  and concrete token patterns from string fragments, following the existing
  validators' source-safe idiom
  retained provider stderr/error sidecars are either normalized into public-safe
  review artifacts and scanned, or deleted as transient non-evidence before closeout
  scan path discovery uses explicit path lists and bounded local globs only
  new self-scanned source files avoid recursive traversal helpers until #68 owns
  the tested allow-context mechanism

validate #65 schema cross-link:
  update artifacts/ace-wave0-ledger-schema.json wave0 split row for #66 during
  approved implementation
  set the #66 plan path to this plan
  keep status_snapshot as plan-required and implementation_ready false until the
  plan approval marker exists
  after approval, set status snapshot and implementation readiness using the
  existing approval marker semantics; do not mark implementation_ready true
  before plan approval

validate legal/security closeout:
  if scripts/legal/legal-sanity-scan.sh exists, run it before closeout
  if it is absent, record NO_LEGAL_SCAN_SCRIPT and keep full closeout blocked
  until #69 supplies the repo-local legal/security scan gate or the user records
  an explicit deferral

verify()
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `config/ace-public-token-fixture-contract.json` | Machine-readable fixture-only token and private-field placeholder contract |
| Create | `scripts/ace_public_token_fixtures.py` | Python stdlib helper for generation request parsing, opaque fixture token emission, placeholder validation, and bad-fixture rejection |
| Create | `scripts/validate_ace_public_token_fixtures.py` | Executable validator for the #66 fixture contract, fixture requests, and schema dependency |
| Create | `tests/test_validate_ace_public_token_fixtures.py` | TDD coverage for token input rejection, marker-only good fixtures, placeholder grammar, bad fixtures, and public-scan safety |
| Create | `tests/fixtures/ace-public-token-fixtures/good-request.json` | Synthetic committed request fixture that contains a generation marker only, not a hand-authored concrete public token value |
| Modify | `.github/workflows/validate.yml` | Run the #66 validator, unit test, and explicit parent public-surface scan over #66 plan/contract/scripts/tests/fixture/workflow/approval marker when present |
| Modify | `artifacts/ace-wave0-ledger-schema.json` | Cross-link the #66 split row to this plan and gate status/implementation readiness through the existing approval-marker semantics |
| Modify if status transitions | `docs/plans/README.md` | Update #66 status and review summary only when plan-review or approval status changes |
| Modify if status transitions | `docs/plans/ace-share-ingestion-wave-coordination.md` | Update #66 plan status and implementation readiness only when gate status changes |
| Conditional scan-clean modify or follow-on | `skills/public-private-routing/SKILL.md` | Promote fixture-only token guidance only if implementation exposes a reusable routing method gap |
| Conditional scan-clean modify or follow-on | `skills/format-coverage-ledger/SKILL.md` | Promote ledger fixture guidance only if implementation exposes a reusable coverage-ledger method gap |
| Conditional scan-clean modify or follow-on | `skills/source-extract-fidelity/SKILL.md` | Promote placeholder/source-fidelity guidance only if implementation exposes a reusable fidelity gap |
| Conditional scan-clean modify or follow-on | `skills/page-shape-contract/SKILL.md` | Promote placeholder page-shape guidance only if implementation exposes a reusable shape gap |
| Conditional scan-clean modify or follow-on | `skills/adversarial-verify-loop/SKILL.md` | Promote review-loop guidance if fixture review exposes a reusable defect class |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_fixture_contract_is_json_and_owned_by_66` | Contract is machine-readable and issue-owned | `config/ace-public-token-fixture-contract.json` | JSON loads with owner, mode, schema dependency, and downstream boundaries |
| `test_contract_imports_65_public_token_field` | #66 consumes #65 field vocabulary | #65 schema plus #66 contract | Public token field name matches #65; no duplicate field vocabulary is invented |
| `test_contract_imports_65_public_token_policy_owners` | #66 fixture ownership does not erase #63 co-ownership | #65 schema plus #66 contract | Fixture contract owner is #66 and public token policy owners remain #66 plus #63 |
| `test_fixture_contract_reconciles_with_63_when_present` | Fixture grammar cannot drift from #63 production policy | #66 contract plus optional `config/ace-public-output-contract.json` | If #63 config exists, token prefix and field policy match it; otherwise #66 marks itself provisional fixture-only |
| `test_contract_imports_65_private_source_terms` | Placeholder fields stay aligned with #65 | #65 schema plus #66 contract | Private source term set matches #65 exactly |
| `test_contract_imports_65_source_like_digest_terms` | Raw provenance/digest classes stay aligned with #65 | #65 schema plus #66 contract | Source-like digest term set matches #65 exactly, including provenance-pointer terms |
| `test_contract_does_not_redefine_route_or_store_enums` | #66 cannot drift route/store semantics | #66 contract | No new route target or logical store values are introduced |
| `test_generation_request_marker_shape_is_closed` | Good fixture request marker is machine-checkable | Request marker variants | Exactly `fixture_set_id`, `fixture_row_id`, and `count` are accepted |
| `test_generation_request_marker_values_are_closed` | Fixture-local IDs cannot hide private/source-like values | Runtime-generated request variants | Closed fixture set, row-id pattern, count range, and no source/path/hash-like values are enforced |
| `test_good_fixture_uses_generation_request_marker` | Committed good fixtures are requests, not concrete tokens | Synthetic request fixture | `public_source_token_request` marker validates; no literal token value is hand-authored |
| `test_generator_rejects_schema_source_path_hash_key_inputs` | Token generation is not source-derived | Runtime-generated unsafe request variants | Every #65-derived forbidden input class fails validation |
| `test_generator_rejects_name_inputs_as_66_hardening` | Name-like inputs are rejected without pretending they are #65 schema terms | Runtime-generated name-derived request variants | Every name-like input class fails validation as #66 extra hardening |
| `test_generator_rejects_fixed_seed_inputs` | Fixture requests cannot make deterministic public token allocation an input contract | Runtime-generated fixed-seed request variant | Seed-bearing request fails validation |
| `test_concrete_token_assignment_matches_parent_scanner` | New validator and parent scanner agree on concrete token assignment shape | Runtime-generated concrete token assignment | Assignment form is rejected by both scanner paths |
| `test_bare_concrete_token_literals_are_66_validator_only` | #66 validator is stronger than parent scanner for non-assignment literals | Runtime-generated bare token and expected-output row variants | #66 validator rejects them without claiming parent-scanner parity |
| `test_generator_emits_opaque_fixture_tokens` | Emitted fixture tokens are opaque and fixture-only | Valid synthetic generation request | Tokens validate against fixture grammar and carry no source-like payload |
| `test_duplicate_tokens_retry_with_injected_random_source` | Duplicate handling is testable without source-derived seeds | Monkeypatched runtime random source | Duplicate candidate is retried and final output remains unique |
| `test_generated_tokens_are_not_durable_lookup_entries` | Fixture tokens do not create persistence | Generated fixture rows | No private token lookup file, map, or durable store output is produced |
| `test_private_placeholder_values_are_closed` | Placeholder grammar cannot drift | Contract placeholder set plus bad value variant | Closed values pass; invented placeholder values fail |
| `test_private_source_terms_are_list_values_only` | Contract cannot self-block under parent scanner | Contract JSON shape and runtime negative fixture | Private source terms appear only as neutral-key list values in committed artifacts; key/assignment form fails |
| `test_private_source_term_prose_policy_is_allowed_without_assignment` | Policy prose remains valid under the current parent scanner | Prose-only fixture naming schema terms | Prose naming terms passes; assigned values and maps fail |
| `test_placeholders_are_allowed_only_in_parsed_good_fixtures` | Private-field placeholders are context-bound | Parsed good fixture and public artifact fixture | Good fixture passes; public artifact carrying placeholder-like fields fails |
| `test_grammar_prose_is_not_fixture_content` | Parser context, not substring allowlisting, separates documentation from fixture rows | Contract prose and parsed fixture rows | Schema-term prose passes; assigned public/private fixture content fails |
| `test_bad_fixture_rejects_hand_authored_concrete_public_token` | Good fixtures cannot smuggle concrete tokens | Runtime-generated bad fixture | Validator fails concrete token assignment |
| `test_bad_fixture_rejects_malformed_request_marker` | Marker shape is strict | Runtime-generated malformed marker variants | Validator fails malformed request markers |
| `test_bad_fixture_rejects_unknown_placeholder_kind` | Placeholder kinds are closed | Runtime-generated unknown placeholder variant | Validator fails unknown placeholder |
| `test_bad_fixture_source_derived_token_examples_fail` | Unsafe deterministic token examples are rejected | Runtime-generated bad fixture variants | Validator fails every source/path/hash/key-derived attempt and separately fails name-derived attempts |
| `test_bad_fixture_source_like_digest_terms_fail` | #65 source-like digest terms cannot leak through fixtures | Runtime-generated raw provenance/digest variants | Validator fails every imported source-like digest term, including provenance-pointer terms |
| `test_bad_fixture_private_field_value_leaks_fail` | Private-field values cannot leak through fixtures | Runtime-generated bad fixture variants | Validator fails every private-value leak attempt |
| `test_private_lookup_map_persistence_is_rejected` | Durable lookup persistence remains outside #66 | Runtime-generated persistence attempt | Validator fails and cites #61 ownership boundary |
| `test_private_source_term_keyed_placeholder_maps_are_rejected` | Placeholder maps cannot use private field terms as keys | Runtime-generated map keyed by private source term | Validator fails and parent scanner would reject if committed |
| `test_public_output_certification_is_not_claimed` | #66 does not replace #63 | Contract metadata | Publication certification owner remains #63 |
| `test_68_placeholder_consumer_boundary_is_recorded` | #68 can consume the grammar later | Contract metadata | #68 is listed as scanner consumer with no self-scan implementation in #66 |
| `test_65_schema_split_row_is_cross_linked` | Machine-readable split registry does not remain plan-required after approved #66 implementation | #65 schema plus approval-marker fixtures | #66 row has this plan path and readiness follows parent approval-marker semantics |
| `test_negative_fixtures_are_runtime_generated` | Tests do not commit self-blocking examples | Test source and fixture directory | Raw unsafe examples are assembled at runtime or temp-file scoped |
| `test_public_scan_paths_cover_66_artifacts` | #66 artifacts stay public-scan clean | Planned artifact path list | Plan, contract, scripts, tests, safe fixture file, workflow, README, coordination, approval marker when present, and retained plan review artifacts pass parent scanner when present |
| `test_review_error_sidecars_are_not_retained_unscanned` | Provider stderr cannot become silent public residue | Review artifact directory with `.err` sidecar | Sidecar is normalized and scanned or absent before closeout |
| `test_legal_scan_absence_blocks_full_closeout` | Missing #69 legal gate is not hidden | Repo without `scripts/legal/legal-sanity-scan.sh` | Closeout records `NO_LEGAL_SCAN_SCRIPT` and does not claim full closure |
| `test_self_scanned_source_uses_fragmented_private_terms` | Validator/test source files do not self-block | New Python source text | Private/source-token deny constants are constructed from fragments, not direct assignment-shaped literals |
| `test_ci_invokes_public_token_fixture_validator` | CI gate runs #66 checks | `.github/workflows/validate.yml` | Workflow invokes #66 validator and unit test |
| `test_ci_invokes_parent_public_scan_for_66_paths` | CI enforces parent scanner over #66 artifacts | `.github/workflows/validate.yml` | Workflow passes #66 plan, contract, scripts, tests, fixture file, workflow, and approval marker path to `validate_ace_epic_wave_coordination.py` with explicit scan-path entries |

---

## Acceptance Criteria

- [ ] A standalone issue plan will exist for #66 and will not authorize implementation until adversarial plan review, user approval, `status:plan-approved`, and `.planning/plan-approved/66.md`.
- [ ] `config/ace-public-token-fixture-contract.json` will define fixture-only mode, schema dependency, public-token fixture grammar, private-field placeholder grammar, and downstream ownership boundaries.
- [ ] The fixture contract will import the public token field name and private source field terms from `artifacts/ace-wave0-ledger-schema.json` and will not redefine route or logical store enums.
- [ ] The fixture contract will import the full #65 source-like raw digest term set and will test those terms, including provenance-pointer terms.
- [ ] The fixture contract will record #66 as fixture-contract owner and preserve #65's #66/#63 public-token policy ownership.
- [ ] If `config/ace-public-output-contract.json` exists, the #66 fixture contract will match its token prefix and public/private field policy; if it does not exist, #66 will mark the fixture contract provisional and subordinate to #63.
- [ ] The public token generator will take no source, path, name, hash, private key, lookup, or raw provenance inputs.
- [ ] Generation request markers will use `public_source_token_request` with exactly `fixture_set_id`, `fixture_row_id`, and `count`; fixture IDs are closed, row IDs match `fixture_row_<three digits>`, count is 1 through 100, and no deterministic seed inputs appear in committed request files.
- [ ] Committed good fixtures will use a generation request marker rather than hand-authored concrete public token values.
- [ ] Concrete runtime fixture token grammar will be literal prefix `pst_` plus exactly 32 lowercase hexadecimal characters, matching the current parent scanner's concrete-token assignment class for assignment-shaped public token values.
- [ ] Committed artifacts may name the token grammar but will not contain concrete token literals as field assignments or expected-output rows.
- [ ] Assignment-shaped concrete token values will be rejected by both the parent scanner and #66 validator; bare concrete token literals and expected-output row literals will be rejected by the #66 validator without claiming parent-scanner parity.
- [ ] Emitted fixture tokens will be opaque, fixture-only, and non-decodable into source-like parts.
- [ ] Duplicate token handling will be tested through an injected runtime random source, not by accepting source-derived or fixed-seed fixture inputs.
- [ ] Private-only ledger fields will use closed placeholder values only inside parsed synthetic good fixtures.
- [ ] Private source field terms will appear only as array/list values under neutral keys in committed machine-readable contract/config/fixture artifacts, never as JSON object keys, map keys, or the left side of colon/equal assignments.
- [ ] Committed prose may name private source field terms only as policy/schema terms, never as assigned values or lookup maps.
- [ ] Placeholder maps keyed by private source field terms will be rejected.
- [ ] Grammar prose will be distinguished from parsed fixture/control-plane rows by parser context, not raw substring allowlisting.
- [ ] Bad fixtures will prove source-derived token attempts, path-derived token attempts, hash-derived token attempts, private lookup derived token attempts, full source-like digest term attempts, and private-field value leaks fail validation.
- [ ] Bad fixtures will also reject name-derived token attempts as #66 extra hardening, not as a #65 schema-derived field class.
- [ ] Bad fixtures will also prove hand-authored concrete token assignments, malformed request markers, unknown placeholder kinds, and fixed-seed token attempts fail validation.
- [ ] #66 will not allocate durable tokens for real ACE records and will not persist private token-to-source lookup maps.
- [ ] Durable token lookup persistence will remain owned by #61.
- [ ] Public-output certification and production/publication canary behavior will remain owned by #63.
- [ ] #68 will be recorded as the downstream consumer of the placeholder grammar for public-surface self-scan contexts.
- [ ] `artifacts/ace-wave0-ledger-schema.json` will cross-link the #66 split row to this plan and will keep readiness governed by the existing approval-marker semantics.
- [ ] `.github/workflows/validate.yml` will include explicit `--scan-public-path` entries for the #66 plan, contract, scripts, tests, concrete safe fixture file, workflow, retained review artifacts where appropriate, and `.planning/plan-approved/66.md` when present.
- [ ] Retained provider stderr/error sidecars will be normalized into public-safe review artifacts and scanned, or removed as transient non-evidence before closeout.
- [ ] If `scripts/legal/legal-sanity-scan.sh` remains absent, #66 closeout will record `NO_LEGAL_SCAN_SCRIPT` and will not claim full closure until #69 supplies the gate or the user records an explicit deferral.
- [ ] Negative fixtures will be runtime-generated or temp-file scoped so committed public artifacts and tests do not self-block the current parent scanner.
- [ ] Self-scanned Python modules and tests will construct forbidden private-source terms and token patterns from string fragments, matching the existing validators' source-safe idiom.
- [ ] Any reusable method gap exposed by implementation will be promoted to the bound skills or filed as a follow-on issue before closeout.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_public_token_fixtures.py` will pass after implementation; CI will use the repo's existing plain `uv run python` invocation style.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_public_token_fixtures` will pass after implementation; CI will use the repo's existing plain `uv run python` invocation style.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_schema_contract.py`, `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py`, and `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` will still pass after implementation.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Private-source term mapping could self-block under the parent line scanner; token grammar was unpinned; #63 co-ownership and Gemini quorum wording needed clarification. Current draft patches these findings; re-review required. |
| Codex r1 | MAJOR | #65 schema cross-link was undecided; review artifact names did not match generated artifacts; provider error sidecars and legal-scan deferral were underspecified. Current draft patches these findings; re-review required. |
| Gemini r1 | UNAVAILABLE | Installed Gemini CLI returned an unsupported-tier authentication error; no review signal. |
| Claude r2 | MAJOR | Required string-fragment construction for self-scanned validator constants, literal `pst_` prefix, scanner parity wording, CI command wording, header/artifact consistency, and #65 readiness timing. Current draft patches these findings; re-review required. |
| Codex r2 | MAJOR | Required closed request-marker grammar, scoped machine-readable private-term placement rule, and #63/#66 contract precedence. Current draft patches these findings; re-review required. |
| Gemini r2 | UNAVAILABLE | Installed Gemini CLI returned an unsupported-tier authentication error; no review signal. |
| Claude r3 | MAJOR | Required explicit CI parent-scan wiring for #66 artifacts, #65-derived versus #66-hardening wording for name inputs, header/artifact consistency, and a concrete fixture file. Current draft patches these findings; re-review required. |
| Codex r3 | MAJOR | Required `.planning/plan-approved/66.md` in the public-scan path set and full #65 source-like digest term import/test coverage. Current draft patches these findings; re-review required. |
| Gemini r3 | UNAVAILABLE | Installed Gemini CLI returned an unsupported-tier authentication error; no review signal. |

**Overall result:** MAJOR - draft only; not ready for `status:plan-review` until a fresh active-provider re-review returns no unresolved MAJOR findings. Gemini remains unavailable and must be recorded as unavailable unless restored before re-review.

---

## Risks and Open Questions

- **Risk:** A fixture token generator could accidentally become deterministic from source-like inputs. Implementation will reject every source/path/name/hash/key input class before token emission.
- **Risk:** Good fixtures could hand-author concrete public token values and mask grammar drift. Implementation will require generation request markers in committed good fixtures.
- **Risk:** Private-field placeholders could normalize unsafe public exposure. Implementation will allow placeholders only inside parsed synthetic good fixtures and will keep public artifact exposure blocked.
- **Risk:** A scanner-safe JSON contract could become self-blocking if private source terms are used as object keys. Implementation will represent private source terms only as list values under neutral keys.
- **Risk:** #66 could drift into durable token persistence or publication certification. The contract will keep those boundaries assigned to #61 and #63.
- **Risk:** #66 fixture grammar could drift from #63 public-output policy. #66 will reconcile with `config/ace-public-output-contract.json` when it exists and remain explicitly provisional before then.
- **Risk:** Source-safe validator constants are easy to regress. The plan requires fragmented string construction and self-scan tests for new source files.
- **Risk:** Gemini may remain unavailable. Any transition to `status:plan-review` will need fresh no-MAJOR active-provider evidence plus explicit disclosure of the Gemini unavailable artifact.

---

## Complexity

**T2** - This is a bounded fixture/validator slice with privacy-sensitive failure modes and multiple repo-local integration points, but it will not read private source content or implement the reusable #68 scanner.
