# #68 Plan Review - Workflow and Status r2

Reviewer: Codex subagent workflow lane
Scope: `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md`
Mode: read-only adversarial re-review
Verdict: MAJOR

## Findings

1. MAJOR - The coordination row wording made `tests/test_validate_ace_wave0_schema_contract.py::test_split_registry_uses_68_plan_body_when_coordination_status_is_silent` vacuous because the replacement target no longer matched the row. Required fix: keep the row prefix that the test intentionally replaces, or update the test with an assertion that the replacement changed the fixture.

2. MINOR - One remaining plan line still called #69 a downstream legal/security gate. Required fix: change that wording to the implemented sibling #69 gate.

## Verified r1 Fixes

- #66 import boundary is explicit in pseudocode, contract details, TDD, and acceptance criteria.
- #69 is mostly reframed as an implemented sibling gate and CI preservation is required.
- Plan-review transition checklist now requires schema/index/coordination update, `implementation_ready=false`, scanned planned comment, posted refetch scan, remote-head verification, and no approval marker.
- Stock CI no-live-GitHub-auth coverage is specified.
- Current state remains non-authorizing: #68 is not approved and has no approval marker.

## Limitations

- This was a Codex subagent review, not a distinct provider review.
- No labels, comments, commits, or file edits were performed by the reviewer.
