# #68 Plan Review - Workflow and Status r1

Reviewer: Codex subagent workflow lane
Scope: `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md`
Mode: read-only adversarial review
Verdict: MAJOR

## Findings

1. MAJOR - The plan said #68 could move to `status:plan-review` after no-MAJOR review, but the schema registry still records #68 as `status:blocked-draft` and the plan did not include the schema row/status tests in the transition scope. Required fix: add plan-review transition steps for the schema row and related tests while keeping `implementation_ready=false`.

2. MAJOR - The plan omitted scanned label-time issue-comment evidence before applying `status:plan-review`. Required fix: require a scanned planned comment, posted comment refetch, scanned refetch, recorded comment URL, and status snapshot before label movement.

3. MINOR - The plan claimed stock CI would not require live GitHub auth, but did not test against `gh`, `GH_TOKEN`, GitHub API, or comment-fetch dependencies in workflow CI. Required fix: add workflow-auth negative coverage.

4. MINOR - The TDD list did not import `config/ace-public-token-fixture-contract.json` despite the #66 dependency claim. Required fix: add import/drift tests for #66 metadata and boundary fields.

## Verified Checks

- Read the #68 plan, README index, coordination ledger, workflow, schema registry, and #66/#69 contract surfaces.
- Ran ACE schema and coordination validators; both passed before this revision.
- Ran the legal scan over all tracked public surfaces; it passed before this revision.
- Read-only issue metadata showed #68 open with no status label, and no #68 approval marker.
- Simulated the local status transition and confirmed schema status drift would fail without a schema-row update.

## Limitations

- This was a Codex subagent review, not a distinct provider review.
- No labels, comments, commits, or file edits were performed by the reviewer.
