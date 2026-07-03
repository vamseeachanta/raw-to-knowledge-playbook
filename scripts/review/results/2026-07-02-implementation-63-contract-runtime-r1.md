# Implementation Review: Issue 63 Contract/Runtime

- Issue: #63
- Stage: implementation
- Reviewer lane: contract-runtime
- Verdict: MAJOR
- Post-review disposition: RESOLVED in main-session patch set before closeout.

## Findings

1. Issue-comment body scans reused #68/#63 text rules but bypassed the #69 legal/security scanner. A secret-assignment-shaped body could pass.
2. Publication-specific #63 checks skipped JSON and Python files, so media metadata and engineering metadata assignments in those public artifacts were not checked.
3. Source-hash sweep validation checked table shape only; it did not prove the live docs/skills methodology hit set was represented.
4. Issue-comment body read failures could include unredacted path material in diagnostics.
5. Diff-only legal closeout could not pass while new public-surface files remained untracked.

## Resolution

- Added `validate_public_output_body_text()` to run #63 text checks and #69 legal/security checks for issue-comment body files.
- Changed issue-comment body diagnostics to use synthetic body labels plus redacted read-failure messages.
- Included JSON and Python in #63 publication-specific text scanning while keeping scanner source scan-clean.
- Added live docs/skills source-hash policy hit enumeration and required the sweep report to classify every live key.
- Added focused tests for issue-comment legal reuse, read-failure redaction, JSON/Python media and engineering metadata denial, and live sweep coverage.
- Staging/commit closeout will resolve the diff-only untracked finding.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_public_artifacts` passed.
- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_public_artifacts.py` passed.
- Exact-surface #63 canary with `--scan-public-path` and `--issue-comment-body-file tests/fixtures/ace-public-artifact-safety/safe-issue-closeout.md` passed.
