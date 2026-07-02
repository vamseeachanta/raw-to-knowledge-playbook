# Issue 68 Implementation Review - Public Surface Self-Scan

## Verdict

APPROVE after MAJOR remediation.

## Findings Addressed

- Allow-context blocks originally suppressed assignment-shaped private-source
  lines. The scanner now allows only reference-shaped lines inside allow blocks;
  assignment/table-shaped lines still trigger the deny rules.
- Snapshot URL validation originally accepted self-consistent non-68 issue URLs
  and later accepted non-68 `issue_number` values paired with issue-68 URLs.
  Snapshot records now require `issue_number == 68`, canonical HTTPS GitHub
  issue URLs, no query/params, and exact comment fragments for refetched issue
  comments.
- Parent coordination CLI originally allowed external scan paths because the
  direct helper preserved temp-fixture behavior. The helper now exposes
  `allow_external_paths`, while CLI scans pass `allow_external_paths=False`.
- Retained #68 plan-review artifacts were not scanned by stock CI. The workflow
  now scans r1-r3 artifacts for claude, codex, gemini, subagent-boundary,
  subagent-scanner, and subagent-workflow with `--include-sidecars`.

## Evidence

- Final focused re-review returned APPROVE after verifying the `issue_number`
  pin and snapshot URL tests.
- `uv run python -m unittest tests.test_validate_ace_public_surface_scan tests.test_validate_ace_epic_wave_coordination tests.test_validate_ace_wave0_schema_contract`
  passed with 173 tests.
- `uv run python scripts/validate_ace_public_surface_scan.py` over the #68
  public artifact list passed.
- `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces`
  passed.
- The 18 retained #68 plan-review artifact selector scans passed with
  `--include-sidecars`.

