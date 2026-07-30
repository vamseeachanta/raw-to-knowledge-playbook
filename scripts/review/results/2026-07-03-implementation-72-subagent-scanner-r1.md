# Implementation Review: Issue 72 Selector/Snapshot

- Issue: #72
- Stage: implementation
- Reviewer lane: subagent-scanner
- Verdict: MAJOR
- Post-review disposition: RESOLVED in main-session patch set before closeout.

## Findings

1. Standalone `issue_comment` snapshots with `phase=pre_post` could bypass URL validation.
2. Allow-context paths could contain both an allowed issue token and an unlisted issue token and still inherit suppression.
3. Allow-context issue checks used the default contract instead of the supplied `contract_path`.

## Resolution

- Added snapshot source-kind/phase validation and URL checks for `issue_comment` records outside the allowed post-refetch shape.
- Changed allow-context parsing to require exactly one relevant `issue-<n>` or `plan-<n>` token and reject mixed-token filenames.
- Threaded `contract_path` through public-surface path scans into allow-context validation.
- Added focused regression tests for all three defect classes.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_public_surface_scan` passed.
- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_public_surface_scan.py --review-issue 72 --review-phase plan --review-provider claude --review-round r2 --include-sidecars` passed.
- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_public_surface_scan.py --review-issue 64 --review-phase plan --review-provider claude --review-round r1` denied as expected.
