---
name: xlsx-input-code-output-canary
description: >
  Classifies XLS/XLSX workbooks before extraction and requires a traceable input
  data or logic contract, code artifact, and verified output artifact for a
  ten-file canary. Use when spreadsheet files may contain formulas, named ranges,
  charts, cached values, protection, or mixed data and calculation logic.
license: CC-BY-4.0
compatibility: Requires Python 3.10+, uv, openpyxl, python-calamine, and cache-only access to online canary workbooks when fetch verification is requested
metadata:
  version: "1.0"
  enforcement_level: L2
  incident_refs: blind-table-dump,cached-value-as-proof,raw-workbook-commit,license-uncertainty
  params: "mode:enum(manifest-check,fetch,inventory,classify,self-test) | cache:external-path"
---

# xlsx-input-code-output-canary

This skill prevents blind spreadsheet extraction. A workbook is not just a
table: it may contain input cells, formulas, named ranges, charts, stale cached
values, protection, or unsupported logic. The canary must prove the whole loop:

`source manifest -> cache/hash check -> inventory -> classification -> code artifact -> output proof`

## Trigger
Use this before broad XLS/XLSX extraction, especially for llm-wiki issue #3 or
any corpus where spreadsheets are being treated as machine-readable high-yield
files.

## Preconditions
1. A user-approved issue plan authorizes this workflow.
2. Raw workbook bytes are not committed. Online samples stay as URLs and hashes;
   fetched bytes go only to an external local cache.
3. Licenses are recorded before a source is used. GPL/EUPL/proprietary projects
   remain reference-only unless explicitly approved.
4. Formula cached values are evidence only. They are never accepted as verified
   calculations.

## Steps
1. **Validate the manifest.**
   ```bash
   uv run skills/xlsx-input-code-output-canary/resources/xlsx_canary.py manifest-check \
     --manifest skills/xlsx-input-code-output-canary/resources/canary_manifest.json
   ```
   The manifest must have exactly five simple and five complex workbooks, with
   URL, license, byte count, sha256, purpose, and expected flags for each source.
2. **Run the offline self-test before online fetch.**
   ```bash
   uv run skills/xlsx-input-code-output-canary/resources/xlsx_canary.py self-test
   ```
   The generated fixtures prove the basic data, calculation, and guarded paths
   without network or raw committed workbooks.
3. **Fetch only when needed, into an external cache.**
   ```bash
   uv run skills/xlsx-input-code-output-canary/resources/xlsx_canary.py fetch \
     --manifest skills/xlsx-input-code-output-canary/resources/canary_manifest.json \
     --cache-dir ~/.cache/raw-to-knowledge-playbook/xlsx-canary
   ```
   The helper refuses repo-local caches unless explicitly overridden for a
   throwaway local run.
4. **Inventory each workbook.**
   ```bash
   uv run skills/xlsx-input-code-output-canary/resources/xlsx_canary.py inventory \
     --workbook ~/.cache/raw-to-knowledge-playbook/xlsx-canary/S1-base-xlsx-base.xlsx \
     --public-fixture-id S1-base-xlsx
   ```
   Inventory records sheet names, formula cells and cached values, named ranges,
   tables, merged ranges, charts, protection flags, parser versions, and sha256.
5. **Classify from inventory.**
   ```bash
   uv run skills/xlsx-input-code-output-canary/resources/xlsx_canary.py classify \
     --inventory /path/to/inventory.json
   ```
   Use only the closed classes: `data`, `calculation`, `mixed`, `guarded`,
   `unsupported`.
   For ACE wave 2 / issue #53, keep that original class and add the separate
   ACE-facing workbook class from `ace_classification_from_inventory()`:
   `data_workbook`, `calculation_workbook`, `report_workbook`, or
   `excluded_workbook`. Use `classify --ace` to emit those ACE fields from the
   CLI. Do not use a workbook class as a route target.
6. **Require the triplet before promotion.**
   - `data`: input schema/ranges -> parser or schema code -> normalized tables.
   - `calculation`: input cells/formula graph -> evaluator or ported code ->
     recomputed output proof.
   - `mixed`: separate data and formula paths before output proof.
   - `guarded` or `unsupported`: explicit deferral artifact with reason.
7. **Apply the ACE #53 deferrals.**
   - `.xls`, `.xlsb`, and `.ods` stay `excluded_workbook` until an approved
     adapter issue lands with tests.
   - `.xlsm` macro presence and external links are inventory facts only; never
     execute macros or trust linked content during ingestion.
   - Protected workbooks route to explicit deferral unless a separate access
     review authorizes metadata-only handling.

## Verification
- `uv run skills/validate_skill.py --strict` passes.
- `manifest-check` passes for `resources/canary_manifest.json`.
- `self-test` passes and proves data, calculation, and guarded paths.
- No raw `.xls`, `.xlsx`, `.xlsm`, or `.xlsb` bytes are committed.
- Every canary source has URL, license note, byte count, and sha256.
- Formula workbooks are never marked verified from cached values alone.
- ACE #53 synthetic fixtures pass
  `uv run python scripts/validate_ace_wave2_spreadsheet_csv.py`.

## Cleanup
- Remove any temporary inventory/output files produced outside committed paths.
- Keep fetched workbooks in an external cache or delete them after the canary run.
- Do not add cache directories or raw workbook bytes to git.

## Incident appendix
| Rule | Why |
|---|---|
| No blind table dump | Spreadsheet knowledge can be formula logic, not visible cells |
| Cached value is not proof | Stale cached results can look authoritative while formulas are wrong |
| Cache-only raw files | Committing third-party workbooks creates license and privacy residue |
| Closed classification vocabulary | Agents otherwise invent reassuring statuses that do not gate scale-up |
| License before source use | Fixture convenience must not override redistribution constraints |
