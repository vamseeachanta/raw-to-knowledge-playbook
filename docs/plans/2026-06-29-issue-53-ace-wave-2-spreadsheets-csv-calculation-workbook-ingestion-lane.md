# Plan for #53: ACE Wave 2 Spreadsheets, CSV, and Calculation Workbook Ingestion Lane

> **Status:** plan-approved
> **Complexity:** T3
> **Date:** 2026-07-02
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/53
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-07-02-plan-53-claude-r1.md | scripts/review/results/2026-07-02-plan-53-codex-r1.md | scripts/review/results/2026-07-02-plan-53-gemini-r1.md | scripts/review/results/2026-07-02-plan-53-claude-r2.md | scripts/review/results/2026-07-02-plan-53-codex-r2.md | scripts/review/results/2026-07-02-plan-53-gemini-r2.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/09-office-formats.md` defines the Excel lane as content, logic, and format extraction, with formula-graph-to-code conversion only when there is a traceable input contract and output proof.
- `docs/10-structured-data-and-model-files.md` requires CSV/delimited dialect probing, field-count validation, row/content digests, and convention sidecars for units, sign conventions, coordinate frames, and producer quirks.
- `skills/xlsx-input-code-output-canary/SKILL.md` requires manifest validation, offline self-test, external cache use for raw workbooks, workbook inventory, closed workbook classes, and a triplet contract before promotion.
- `skills/xlsx-input-code-output-canary/resources/xlsx_canary.py` already implements manifest validation, inventory, classification, self-test fixtures, and the current closed classes `data`, `calculation`, `mixed`, `guarded`, and `unsupported`.
- `skills/format-coverage-ledger/SKILL.md` records spreadsheet known-loss facts: text/CSV extraction captures computed values but loses formulas, named ranges, charts/plots unless a richer lane handles them.
- `skills/source-extraction-coverage/SKILL.md`, `skills/source-extract-fidelity/SKILL.md`, `skills/independent-oracle-validation/SKILL.md`, and `skills/public-private-routing/SKILL.md` define the estimate/yield, fidelity, oracle, and routing gates this lane will consume.

### Related issues and live gate state
- [#53](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/53) has user approval recorded in `.planning/plan-approved/53.md`; implementation still requires the live `status:plan-approved` label and this plan's dependency gates.
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic; it does not approve child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains the unapproved wave-0 umbrella. Its split implementation issues [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) are implemented/closed and may be consumed as closed contracts.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) has approval and an implemented manifest freshness validator, but operational sampling for downstream waves must still fail closed unless the request supplies a trusted evidence pointer accepted by [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70).
- [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) implemented trusted-evidence integration, but `artifacts/ace-manifest-freshness/trusted-evidence-registry.json` currently has an empty `trusted_evidence` list. Therefore [#53](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/53) may plan synthetic fixtures and validators, but operational ACE sampling remains blocked until a trusted [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence row exists.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) bounds downstream sampling requests. Any approved implementation of this plan must prove per-bucket caps, maximum files/bytes, deterministic seed/sort, and metadata-only request shape before touching operational manifests.
- [#71](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/71) is implemented/closed and may be consumed for validator hardening around non-ready rows, manifest source membership, and scan-safe negative fixtures.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) has user approval recorded in `.planning/plan-approved/61.md`. Durable stores, target paths, retrieval metadata, lifecycle state, persistent metrics, and durable ingested-success reporting remain blocked pending [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) implemented validator evidence.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has user approval recorded in `.planning/plan-approved/63.md`. Public docs navigation, `mkdocs.yml`, `llm-wiki`, GitHub-public corpus summaries, measured ACE-derived case studies, and external publication remain blocked pending [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) implemented canary evidence.

### Source inventory
- The issue-body inventory states an approximate spreadsheet/data rollup of 37.6k files / 48.7 GB, including `.xls`, `.xlsx`, `.xlsm`, and `.csv`.
- This plan will not traverse the ACE source root, raw manifests, or private workbooks. It treats the issue-body rollup as an upstream assertion until [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62), [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67), and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) supply trusted, bounded operational evidence.

### Extension/type map

| Extension/type | Content class | Expected useful ingestion | Detailed content analysis | Success measurement | Ease/difficulty |
|---|---|---:|---|---|---:|
| `.csv` | Flat tabular data export | 80-95% when dialect/schema are stable | Detect delimiter, quote rules, encoding, line endings, header shape, row width, typed columns, units/sign/coordinate sidecars, and row/content digests. | `successful_routed_items / eligible_candidate_items * 100`; ragged/ambiguous rows excluded with reason. | 3/11 |
| `.tsv`, `.psv`, generic delimited `.txt`/`.dat` | Delimited data export | 70-90% when producer conventions are known | Same as CSV, plus explicit producer family and delimiter evidence; route unknown dialects to provisional or excluded status. | Same success metric; unknown producer conventions counted separately from hard parse failures. | 4/11 |
| `.xlsx` data workbook | OpenXML workbook with tables/ranges | 75-90% for data-heavy sheets | Inventory sheets, tables, merged ranges, date system, formulas, charts, named ranges, protection, external links, and parser versions before extraction. | A workbook is successful only after class, route, known losses, and table/range proof are recorded. | 3/11 |
| `.xlsx` calculation/report workbook | Formula/reporting workbook | 40-80% depending formula/chart complexity | Separate visible values from formulas, named ranges, dependency graph, charts, and layout/reporting concepts; cached values are evidence only. | Successful calculation ingestion requires input contract, code/evaluator artifact, and independent output proof. | 4/11 |
| `.xls` | Legacy binary Excel workbook | Metadata-only/deferred until an approved parser adapter exists | Current `xlsx_canary.py` is OpenXML-first and does not prove `.xls` content extraction. The approved implementation may inventory extension-level metadata and must file or cite a follow-on adapter issue before counting `.xls` content as eligible. | Excluded from content-ingestion denominator unless an approved `.xls` adapter and tests land. | 5/11 |
| `.xlsm` | Macro-enabled workbook | 35-75% for non-macro data/formulas after macro/external-link inventory support lands | Inventory formulas, macro presence, external-link presence, workbook structure, and protection state, but do not execute macros. VBA/macro logic is metadata-only unless a future approved method issue authorizes static analysis/porting. | Data/formula pieces may route if independently verified; macro-dependent logic is excluded or deferred. | 5/11 |
| `.xlsb`, `.ods`, other spreadsheet-like files if discovered | Non-primary spreadsheet formats | Metadata-only/deferred until a parser path is approved | Treat as out-of-baseline discovery: metadata-only inventory, route decision, and follow-on issue unless a synthetic fixture proves safe parser behavior. | Excluded from content-ingestion denominator until a parser path is approved and tested. | 6/11 |

### Gaps identified
- The existing workbook canary closed classes (`data`, `calculation`, `mixed`, `guarded`, `unsupported`) need an ACE-facing mapping to issue vocabulary without breaking current canary behavior. `excluded_no_ingest` remains a route target only; the workbook class will use `excluded_workbook` to avoid enum collision with the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) route vocabulary.
- No repo-local CSV/delimited dialect probe exists under `skills/format-coverage-ledger/resources/`.
- No issue-scoped validator exists yet at `scripts/validate_ace_wave2_spreadsheet_csv.py`.
- No scan-safe #53 fixtures exist for workbook class mapping, CSV dialect/ragged-row behavior, formula-cache rejection, macro/protected-workbook deferral, [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) cap enforcement, [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) durable-output blocking, or [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) public-output blocking.
- The issue body says "#50 wave 0 ledger/routing contract should be planned first"; that blocker is stale. The current dependency story is [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) approved parent, [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) unapproved umbrella, closed split contracts [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69), [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) trusted-evidence integration with an empty trusted registry, and [#71](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/71) closed validator hardening.

### Evidence

**Issue status** (verified 2026-07-02):
```
#53 OPEN labels=strengthening,lane:codex,priority:high
```

**File existence** (verified 2026-07-02):
```
EXISTS docs/09-office-formats.md
EXISTS docs/10-structured-data-and-model-files.md
EXISTS skills/xlsx-input-code-output-canary/SKILL.md
EXISTS skills/xlsx-input-code-output-canary/resources/xlsx_canary.py
EXISTS skills/xlsx-input-code-output-canary/evals/evals.json
EXISTS skills/format-coverage-ledger/SKILL.md
EXISTS scripts/ace_bounded_sampling_firewall.py
EXISTS scripts/ace_manifest_evidence_trust.py
EXISTS artifacts/ace-manifest-freshness/trusted-evidence-registry.json
MISSING skills/format-coverage-ledger/resources/csv_dialect_probe.py
MISSING scripts/validate_ace_wave2_spreadsheet_csv.py
MISSING tests/test_validate_ace_wave2_spreadsheet_csv.py
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-53-ace-wave-2-spreadsheets-csv-calculation-workbook-ingestion-lane.md |
| Planned validator | scripts/validate_ace_wave2_spreadsheet_csv.py |
| Planned validator tests | tests/test_validate_ace_wave2_spreadsheet_csv.py |
| Planned committed fixtures | tests/fixtures/ace-wave2-spreadsheet-csv/ |
| Workbook canary skill | skills/xlsx-input-code-output-canary/SKILL.md |
| Workbook canary helper | skills/xlsx-input-code-output-canary/resources/xlsx_canary.py |
| Workbook canary evals | skills/xlsx-input-code-output-canary/evals/evals.json |
| CSV/delimited probe helper | skills/format-coverage-ledger/resources/csv_dialect_probe.py |
| Format coverage skill | skills/format-coverage-ledger/SKILL.md |
| Public measured ACE report | Deferred until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) approval and implemented canary evidence |
| Private measured ACE sidecar | Deferred until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) approval plus implemented durable-output validator evidence, and then only through an approved private/off-public route |
| Review artifact - Claude r1 | scripts/review/results/2026-07-02-plan-53-claude-r1.md |
| Review artifact - Codex r1 | scripts/review/results/2026-07-02-plan-53-codex-r1.md |
| Review artifact - Gemini r1 | scripts/review/results/2026-07-02-plan-53-gemini-r1.md |
| Review artifact - Claude r2 | scripts/review/results/2026-07-02-plan-53-claude-r2.md |
| Review artifact - Codex r2 | scripts/review/results/2026-07-02-plan-53-codex-r2.md |
| Review artifact - Gemini r2 | scripts/review/results/2026-07-02-plan-53-gemini-r2.md |

---

## Deliverable

This issue will produce a spreadsheet/CSV ingestion-lane pilot plan and, after user approval only, a test-first implementation that classifies workbook and delimited sources, blocks unsafe sampling/publication/durable-output paths, adds a CSV dialect probe, updates the workbook canary without breaking existing class behavior, and records known spreadsheet/data extraction losses.

The approved implementation will use synthetic scan-safe fixtures by default. Under the current [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) contract, downstream operational requests are metadata-only request records; they do not authorize reading workbook/CSV content bytes for measured ingestion. Therefore this issue's executable success metrics will be measured on synthetic fixtures unless a later approved issue extends the sampling firewall to content-byte pilots. Any measured ACE-derived private sidecar, target path, lifecycle field, durable metric, or persistent store write remains blocked until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved and implemented. Any public output remains blocked until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved and implemented.

### Workbook Class and Route Mapping

The approved implementation will keep existing canary classes intact and add separate ACE-facing fields. It will not rename or overload the existing canary class enum.

| Existing canary class | ACE `workbook_class` | Route implication | Notes |
|---|---|---|---|
| `data` | `data_workbook` | Route from visibility/routing policy | Eligible for table/range parser proof. |
| `calculation` | `calculation_workbook` | Route from visibility/routing policy | Requires input contract, code/evaluator artifact, and independent output proof. |
| `mixed` with formula/table/chart evidence | `calculation_workbook` | Route from visibility/routing policy, never from class alone | Formula-bearing mixed workbooks remain calculation workbooks; if `summary.chart_count > 0`, the ACE record may also carry `report_evidence=true` for later report-lane triage, but `workbook_class` stays `calculation_workbook`. |
| `guarded` | `excluded_workbook` | Usually `excluded_no_ingest` unless access review authorizes metadata-only handling | Protection state is an explicit deferral reason. |
| `unsupported` with report evidence | `report_workbook` | Usually `metadata_only` until a report-lane proof exists | Report evidence is defined only from emitted inventory fields: `summary.chart_count > 0` with `summary.formula_count == 0`, or `summary.merged_range_count > 0` with `summary.table_count == 0` and `summary.formula_count == 0`. |
| `unsupported` without report evidence | `excluded_workbook` | Usually `excluded_no_ingest` or `metadata_only` | Unsupported parser, `.xls` without adapter, non-primary binary container without parser, and macro-dependent logic are not content-ingestion successes. |

The planned validator will enforce separate enum fields for `workbook_class` and `route_target` so `excluded_workbook` cannot be confused with the [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) `excluded_no_ingest` route target.

---

## Pseudocode

```text
require explicit user approval before implementation
load #65 route/store vocabulary and #67 bounded sampling contract
load #62/#70 trusted evidence registry state
if operational ACE sampling requested:
  require trusted #62 evidence pointer accepted by #70
  require #67 metadata-only request shape, fixed seed/sort, per-bucket/file/byte caps
  fail closed while trusted evidence registry is empty
else:
  use synthetic scan-safe fixtures only

for each candidate spreadsheet/delimited record:
  classify source type by structure and parser evidence, not filename alone
  assign closed route target before any output path is selected
  if workbook:
    inventory sheets, formulas, cached values, named ranges, tables, merged ranges,
      charts, date system, external link presence, macro presence, protection flags, parser versions
    classify existing canary class: data | calculation | mixed | guarded | unsupported
    map to ACE workbook_class: data_workbook | calculation_workbook | report_workbook | excluded_workbook
    record known losses in format coverage ledger
    reject verification based only on cached values
    require input contract + code/evaluator artifact + independent output proof for calculation class
    defer/provision macro-dependent or protected logic unless separately authorized
  if delimited:
    detect dialect with a structured parser
    validate row widths and content digests
    require units/sign/coordinate sidecar for numeric engineering data
    route ragged or unknown-producer data as provisional/excluded with reason
  keep operational requests metadata-only until a later approved issue extends #67 for content-byte pilots
  block durable stores, retrieval metadata, lifecycle fields, target paths, private sidecars, and persistent metrics until #61 is approved and implemented
  block docs nav, mkdocs, llm-wiki, public case reports, and external publication until #63 is approved and implemented
  compute success only for eligible candidate items, with hard exclusions reported separately
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | scripts/validate_ace_wave2_spreadsheet_csv.py | Executable validator for class mapping, CSV probe contract, sampling/public/durable gates, and success metric fields |
| Create | tests/test_validate_ace_wave2_spreadsheet_csv.py | Red/green tests for all #53 gate and mapping behavior |
| Create | tests/fixtures/ace-wave2-spreadsheet-csv/ | Scan-safe CSV/delimited text fixtures and workbook inventory JSON fixtures only; raw workbook bytes will be generated in temp dirs at test runtime |
| Modify | skills/xlsx-input-code-output-canary/SKILL.md | Add ACE-facing class mapping and issue #53 use guidance while preserving existing closed classes |
| Modify | skills/xlsx-input-code-output-canary/resources/xlsx_canary.py | Emit ACE class mapping/status fields, macro/external-link presence flags, and legacy `.xls` deferral without accepting cached values as proof |
| Modify | skills/xlsx-input-code-output-canary/evals/evals.json | Add data/calculation/mixed/report/guarded/unsupported scenarios |
| Modify | skills/format-coverage-ledger/SKILL.md | Add CSV/delimited known-loss entries and ACE wave2 ledger fields |
| Create | skills/format-coverage-ledger/resources/csv_dialect_probe.py | Structured dialect/field-count/content-digest helper |
| Modify | docs/09-office-formats.md | Add issue-aligned workbook class mapping and macro/protection deferral rules |
| Modify | docs/10-structured-data-and-model-files.md | Add CSV/delimited sidecar and success-metric requirements |
| Modify | docs/plans/README.md | Update #53 status after review; correct any discovered queue drift |
| Modify | docs/plans/ace-share-ingestion-wave-coordination.md | Update #53 row after review with current gates and review artifact paths |
| Modify | .github/workflows/validate.yml | Run the #53 validator/tests once implemented |

Public `docs/case-studies/` output is intentionally not in the implementation file set until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) supplies public-output authorization and passing canary evidence. Private measured ACE sidecars are also intentionally absent until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) supplies durable-output authorization and passing validator evidence.

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_workbook_classification_closed_values | Workbook class enum stays closed | Synthetic workbook inventories | Only `data_workbook`, `calculation_workbook`, `report_workbook`, `excluded_workbook` |
| test_existing_canary_classes_map_losslessly | Existing canary classes are preserved | `data`, `calculation`, `mixed`, `guarded`, `unsupported` fixtures | ACE class plus original class retained |
| test_report_workbook_class_uses_emitted_inventory_fields | Report classification uses current inventory evidence | Unsupported chart-only and merged-range inventories | Existing canary class remains `unsupported`; ACE `workbook_class=report_workbook` only when chart/merged-range rules match |
| test_mixed_formula_chart_stays_calculation_workbook | Mixed formula/chart workbooks do not get two class dispositions | Mixed formula/chart inventory | `workbook_class=calculation_workbook` plus optional `report_evidence=true` |
| test_workbook_route_enum_is_separate_from_class_enum | Route target is not workbook class | Excluded workbook record | `workbook_class=excluded_workbook`, `route_target=excluded_no_ingest` |
| test_formula_cached_values_not_verification | Cached values are never proof | Formula workbook with cached values only | Verification refused without independent output proof |
| test_calculation_triplet_required | Calculation port requires full triplet | Formula workbook fixture | Input contract, code/evaluator artifact, output proof required |
| test_runtime_generated_workbook_fixtures_only | Raw workbook bytes are not committed | Repo fixture tree | No `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, `.ods`, or other binary spreadsheet containers under tracked fixtures |
| test_xls_requires_adapter_before_content_success | Legacy `.xls` is not overclaimed | `.xls` fixture metadata without approved adapter | Metadata-only/deferred; not counted in eligible content denominator |
| test_macro_and_external_link_flags_are_inventory_only | Macro/external links are surfaced without execution | `.xlsm`/external-link inventory fixture | Flags emitted; macro/external-link-dependent logic deferred |
| test_macro_enabled_logic_is_deferred | Macros are not executed or silently trusted | `.xlsm` fixture metadata | Macro-dependent logic routes to excluded/deferred status |
| test_protected_workbook_is_deferred | Guarded workbooks fail closed | Protected workbook inventory | `workbook_class=excluded_workbook`, route decision, and explicit deferral reason |
| test_csv_dialect_field_count_digests | CSV parser integrity | comma, semicolon, tab, quoted, ragged fixtures | Dialect reported, ragged rows fail, digests emitted |
| test_csv_convention_sidecar_required | Numeric conventions are explicit | Numeric CSV without units/sign/coordinate sidecar | Remains provisional/non-durable |
| test_raw_workbook_bytes_not_repo_local | Raw workbooks are not committed | Repo-local workbook bytes | Validator fails |
| test_routing_before_target_write | Routing precedes target-path selection | Unknown/private fixture | Public/durable target blocked |
| test_67_cap_violation_fails_closed | Bounded sampling caps are enforced | Over-cap sampling request | Request denied with #67 blocker |
| test_67_boundary_caps_import_contract_values | Boundary caps are imported from #67 | Request at 200 rows, 25 files, 1048576 bytes and one-over variants | Boundary accepted when other gates pass; one-over variants fail |
| test_missing_trusted_62_evidence_fails_closed | Empty #70 registry blocks operational sampling | Downstream request without trusted pointer | Sampling denied; synthetic-only path remains allowed |
| test_fixture_62_evidence_cannot_authorize_sampling | Fixture evidence cannot authorize operational run | #62 fixture pointer | Request denied |
| test_61_durable_fields_blocked | Durable outputs remain blocked | Plan/output record with store path/retrieval/lifecycle/persistent metrics before #61 | Validator fails |
| test_63_public_output_blocked | Public surfaces remain blocked | Docs nav, mkdocs, llm-wiki, public case-report path before #63 | Validator fails |
| test_wave2_success_metric_defined | `% ingested success` is measurable | Synthetic pilot ledger | Numerator, denominator, threshold, command, exclusions present |
| test_scan_safe_negative_fixtures | Negative examples do not self-block scanners | Runtime-assembled hostile strings | Tests can assert denials while source files pass public/legal scans |

---

## Acceptance Criteria

- [ ] Workbooks are classified as `data_workbook`, `calculation_workbook`, `report_workbook`, or `excluded_workbook` before extraction or target selection.
- [ ] Existing canary classes `data`, `calculation`, `mixed`, `guarded`, and `unsupported` are mapped without breaking current workbook canary behavior.
- [ ] `workbook_class` and `route_target` are separate fields, and the validator rejects enum intermixing between workbook classes and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) route targets.
- [ ] Raw workbook bytes are runtime-generated or externally cached only; committed fixtures are CSV/delimited text or workbook inventory JSON, not `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, `.ods`, or other binary spreadsheet container files.
- [ ] `.xls` content ingestion is metadata-only/deferred until an approved adapter exists; it is not counted in the content-ingestion denominator without adapter proof.
- [ ] CSV/delimited files record dialect, field-count validation, units/sign/coordinate convention sidecar state, and content digests.
- [ ] Calculation workbook pilots include input contract, code/evaluator artifact, and independent output proof; cached values alone do not verify the calculation.
- [ ] Macro presence and external-link presence are inventoried, but macro/external-link-dependent logic is deferred unless separately authorized.
- [ ] Macro-enabled or protected workbook logic is deferred/excluded unless separately authorized; macros are not executed by the ingestion validator.
- [ ] Known workbook/CSV extraction losses are recorded in the format coverage ledger.
- [ ] `% ingested success` is calculated as `successful_routed_items / eligible_candidate_items * 100`, with hard exclusions and unsupported classes reported separately.
- [ ] Public/private routing occurs before any derived page, dataset, code artifact, or target path is selected.
- [ ] Operational ACE sampling is blocked unless a [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) bounded request supplies a trusted [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence pointer accepted by [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70).
- [ ] Current operational sampling remains metadata-only under [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67); content-byte pilot sampling requires a future approved firewall-extension issue.
- [ ] Durable stores, retrieval metadata, lifecycle state, persistent metrics, target paths, and private measured sidecars remain blocked until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved and implemented.
- [ ] Public docs navigation, `mkdocs.yml`, `llm-wiki`, measured ACE-derived public summaries, GitHub-public corpus reports, and external publication remain blocked until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is approved and implemented.
- [ ] Plan-review evidence is committed, pushed, and linked in a scanned issue comment before applying `status:plan-review`.
- [ ] The issue-comment body is written to a repo-local temporary review artifact, scanned by `validate_ace_public_surface_scan.py` and `scripts/legal/legal-sanity-scan.sh`, posted via `gh issue comment --body-file`, then removed before final commit/closeout.
- [ ] No `status:plan-approved` label is applied and no `.planning/plan-approved/53.md` marker is created by the planning agent.

---

## Planned Review and Validation Commands

These commands will be run before posting [#53](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/53) plan-review evidence. The review-artifact scan list must match the final materialized artifact set; missing provider artifacts are not referenced. If Gemini is unavailable, the materialized artifact is a sanitized `UNAVAILABLE` record, not raw stderr.

```bash
uv run python scripts/validate_ace_epic_wave_coordination.py
uv run python scripts/validate_ace_wave0_schema_contract.py
uv run python scripts/validate_ace_public_surface_scan.py \
  --scan-public-path docs/plans/2026-06-29-issue-53-ace-wave-2-spreadsheets-csv-calculation-workbook-ingestion-lane.md \
  --scan-public-path docs/plans/README.md \
  --scan-public-path docs/plans/ace-share-ingestion-wave-coordination.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-53-claude-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-53-codex-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-53-gemini-r2.md
bash scripts/legal/legal-sanity-scan.sh \
  --scan-public-path docs/plans/2026-06-29-issue-53-ace-wave-2-spreadsheets-csv-calculation-workbook-ingestion-lane.md \
  --scan-public-path docs/plans/README.md \
  --scan-public-path docs/plans/ace-share-ingestion-wave-coordination.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-53-claude-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-53-codex-r2.md \
  --scan-public-path scripts/review/results/2026-07-02-plan-53-gemini-r2.md
bash scripts/legal/legal-sanity-scan.sh --diff-only
git diff --check --cached
git diff --check
```

If review produces a later no-MAJOR round, the scan path list will be updated to the final round artifacts before commit and label movement.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | Mapping table/report overlay undefined; raw workbook fixtures contradicted no-workbook-bytes rule; #67 metadata-only boundary contradicted measured content path; Gemini-unavailable scan branch needed; macro/external-link/`.xls` scope under-specified; workbook class/route enum collision. Findings patched in this revision. |
| Codex r1 | MAJOR | `.xls` ingestion overclaimed; private measured sidecar was not gated on #61; raw workbook fixture wording unsafe; #67 caps needed exact imported boundary tests; scan commands referenced missing artifacts. Findings patched in this revision. |
| Gemini r1 | UNAVAILABLE | Gemini CLI failed with unsupported-client/ineligible-tier before returning findings; sanitized artifact retained. |
| Claude r2 | MINOR | Report-workbook mechanism needed one encoding, #53 coordination row stale against r1/r2 evidence, and `.ods`/binary spreadsheet container fixtures needed no-raw-byte coverage. Findings patched in this revision. |
| Codex r2 | MINOR | #53 coordination row needed synthetic-only/deferred-format summary and r2 scan artifacts needed materialization. Findings patched in this revision. |
| Gemini r2 | UNAVAILABLE | Gemini CLI failed with unsupported-client/ineligible-tier before returning findings; sanitized artifact retained. |

**Overall result:** PLAN-APPROVED - active-provider r2 returned no MAJOR findings after this revision patched the remaining MINOR findings. User approval is recorded in `.planning/plan-approved/53.md`; implementation may proceed only after the live issue carries `status:plan-approved` and this plan's dependency gates are satisfied.

---

## Risks and Open Questions

- **Risk:** The [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) trusted evidence registry is empty, so any operational sampling claim must fail closed.
- **Risk:** `.xls`, `.xlsm`, `.xlsb`, protected workbooks, external links, volatile functions, circular references, and macro-dependent logic may require deferral rather than ingestion; `.xls` will remain metadata-only until a concrete adapter is approved and tested.
- **Risk:** Formula-to-code proof can balloon; implementation must stay to a bounded synthetic or trusted-evidence-backed pilot slice.
- **Risk:** Public-facing measured reports are tempting because the issue asks for ingestion percentages, but they remain blocked until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63).
- **Open:** Report workbooks with chart-heavy narrative may need handoff to document/presentation/imagery lanes after classification.

---

## Complexity

**T3** - multi-format spreadsheet/data lane with class migration, formula-proof rules, CSV/delimited probe, routing gates, public/private firewall, durable-output dependency, and cross-skill/doc updates.
