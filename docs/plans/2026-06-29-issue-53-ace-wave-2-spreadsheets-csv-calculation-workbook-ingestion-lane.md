# Plan for #53: ACE Wave 2 Spreadsheets, CSV, and Calculation Workbook Ingestion Lane

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/53
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-06-29-plan-53-claude.md | scripts/review/results/2026-06-29-plan-53-codex.md | scripts/review/results/2026-06-29-plan-53-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/09-office-formats.md` distinguishes D1 content, D2 logic, and D3 report/template extraction for Office files.
- `docs/10-structured-data-and-model-files.md` requires CSV dialect probing, field-count validation, row content hashes, and convention sidecars.
- `skills/xlsx-input-code-output-canary/SKILL.md` and `skills/format-coverage-ledger/SKILL.md` already encode workbook canary and loss-ledger workflows.

### Related issues
- [#53](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/53) covers 37.6k spreadsheet/data files / 48.7 GB.
- [#5](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/5), [#6](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/6), [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12), and [#33](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/33) are method anchors.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) must provide the upstream ledger/routing contract.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable datasets, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- Spreadsheet/data rollup: 37.6k files / 48.7 GB.
- Extensions include `.xls`, `.xlsx`, `.xlsm`, and `.csv`.
- Expected useful ingestion is 75-90% for well-formed tables, lower for macro-heavy/protected workbooks; pilot threshold is at least 75% routed success for eligible flat-data rows, with guarded/unsupported exclusions reported separately.

### Gaps identified
- Workbook class migration is not yet encoded for ACE: existing canary classes are `data`, `calculation`, `mixed`, `guarded`, and `unsupported`; the ACE lane must map these to data workbook, calculation workbook, mixed/report workbook, or `excluded_no_ingest` without losing current behavior.
- No CSV dialect/field-count/hash canary exists under `format-coverage-ledger`.
- No ACE spreadsheet case study exists.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#53 OPEN ACE wave 2: spreadsheets, CSV, and calculation workbook ingestion lane labels=strengthening,lane:codex,priority:high
```

**File existence**:
```
EXISTS docs/09-office-formats.md
EXISTS docs/10-structured-data-and-model-files.md
EXISTS skills/xlsx-input-code-output-canary/resources/xlsx_canary.py
EXISTS skills/format-coverage-ledger/evals/evals.json
MISSING docs/case-studies/ace-wave-2-spreadsheets-csv-calculation-workbook-lane.md
MISSING skills/format-coverage-ledger/resources/csv_dialect_probe.py
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-53-ace-wave-2-spreadsheets-csv-calculation-workbook-ingestion-lane.md |
| Pilot report | docs/case-studies/ace-wave-2-spreadsheets-csv-calculation-workbook-lane.md |
| Workbook canary | skills/xlsx-input-code-output-canary/resources/xlsx_canary.py |
| CSV canary | skills/format-coverage-ledger/resources/csv_dialect_probe.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-53-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-53-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-53-gemini.md |

---

## Deliverable

A spreadsheet/CSV ingestion-lane pilot that classifies workbooks, validates delimited files, ports one calculation workbook path into a code-backed proof, and records known extraction losses before any public/private target write.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
select bounded sample for xls, xlsx, xlsm, csv, delimited:
  max 20 rows per extension/class bucket, deterministic seed/sort, max 180 files or 250 MB touched
for each candidate row:
  hash source and decide fail-closed visibility route
  if workbook:
    inventory sheets, formulas, cached values, macros, charts, external links
    classify as data_workbook, calculation_workbook, report_workbook, exclude
    record known losses in format coverage ledger
    if calculation_workbook:
      extract input contract, formula graph, code artifact, output proof
      reject proof based only on cached values
  if delimited:
    detect dialect with a real parser
    validate field counts, row hashes, units/sign/coordinate sidecar
  block public target until routing passes and #61 is approved
  compute routed success numerator/denominator for eligible candidate rows
write case study and update docs/skills/evals
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-wave-2-spreadsheets-csv-calculation-workbook-lane.md | Pilot counts, workbook classes, CSV checks, calculation proof |
| Modify | docs/09-office-formats.md | Align workbook class closed set |
| Modify | docs/10-structured-data-and-model-files.md | Tighten CSV/delimited convention sidecar workflow |
| Modify | skills/xlsx-input-code-output-canary/SKILL.md | Add issue-aligned workbook class field |
| Modify | skills/xlsx-input-code-output-canary/resources/xlsx_canary.py | Add workbook class output and self-test fixtures |
| Modify | skills/xlsx-input-code-output-canary/evals/evals.json | Add data/calculation/report/exclude scenarios |
| Modify | skills/format-coverage-ledger/SKILL.md | Add CSV/delimited known-loss ledger entries |
| Create | skills/format-coverage-ledger/resources/csv_dialect_probe.py | CSV dialect/field-count/hash self-test helper |
| Create | scripts/validate_ace_wave2_spreadsheet_csv.py | Executable validator for class migration, sample caps, success metric, and route enum |
| Modify | .github/workflows/validate.yml | Run workbook and CSV self-tests |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_workbook_classification_closed_values | Workbook class enum | Fixtures for four classes | data/calculation/report/exclude only |
| test_existing_canary_classes_mapped_losslessly | Existing class migration | data/calculation/mixed/guarded/unsupported fixtures | ACE class plus route target without dropping old class |
| test_formula_cached_values_not_verification | Cached values are not proof | Workbook with stale cache | Refuses verified proof |
| test_calculation_triplet_required | Calculation port has full proof | Formula workbook | Input contract, code artifact, output proof |
| test_csv_dialect_field_count_hashes | CSV parser integrity | comma/semicolon/quoted/ragged rows | Ragged fails, row hashes emitted |
| test_csv_convention_sidecar_required | Numeric conventions explicit | Numeric CSV without units/sign | Remains provisional |
| test_raw_workbook_cache_not_repo_local | Raw workbook not committed | Workbook bytes under repo | Fails validation |
| test_routing_before_target_write | Routing precedes output path | Private/unknown source | Public target blocked |
| test_wave2_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave2_sample_caps_are_enforced | Bounded sampling | Sample manifest | Per-bucket caps, seed/sort, max files, and max bytes present |

---

## Acceptance Criteria

- [ ] Workbooks are classified as data workbook, calculation workbook, report workbook, or exclude before extraction.
- [ ] Existing canary classes `data`, `calculation`, `mixed`, `guarded`, and `unsupported` are mapped without breaking current workbook canary behavior.
- [ ] CSV/delimited files record dialect, field-count validation, unit/sign convention sidecar, and content hashes.
- [ ] Calculation pilot includes input contract, formula/code artifact, and verified output proof.
- [ ] Known workbook/CSV extraction losses are recorded in the format coverage ledger.
- [ ] `% ingested success` is calculated as successful routed items over eligible candidate items, with guarded/unsupported exclusions reported separately.
- [ ] Public/private routing occurs before any derived page or dataset target is selected, and no durable dataset/path is selected before [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) approval.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports pass the [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) redaction canary before publication.
- [ ] Workbook and CSV self-tests, `uv run python scripts/validate_ace_wave2_spreadsheet_csv.py`, and `uv run skills/validate_skill.py` pass.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude | PENDING | Not yet reviewed |
| Codex | PENDING | Not yet reviewed |
| Gemini | PENDING | Not yet reviewed |

**Overall result:** PENDING - draft only; not ready for `status:plan-review`.

---

## Risks and Open Questions

- **Risk:** This issue is blocked by #51 routing/sampling and #61 durable-output/lifecycle rules.
- **Risk:** `.xls`, macro-heavy, or protected workbooks may need defer/exclude classes.
- **Risk:** Formula-to-code proof can balloon; pilot must stay to one bounded calculation slice.
- **Open:** Report workbooks may need handoff to presentation/imagery lanes.

---

## Complexity

**T3** - multi-format ingestion lane, code-backed calculation proof, CSV validation harness, routing, and cross-skill/doc updates.
