# #68 Plan Review - Scanner Contract r1

Reviewer: Codex subagent scanner lane
Scope: `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md`
Mode: read-only adversarial review
Verdict: MAJOR

## Findings

1. MAJOR - The plan covered source-like digest JSON keys but did not require the same key denial for imported private source terms regardless of value shape. Required fix: add a deny class and tests covering every imported private source term used as a JSON key with placeholder, safe string, null, array, and object values.

2. MAJOR - The allow-context model asserted closed contexts but did not define exact context IDs, token classes, sentinel grammar, numeric budgets, heading anchors, or malformed block behavior. Required fix: add a normative contract table and tests for unknown IDs, wrong path, wrong heading, wrong token class, missing sentinels, nested blocks, over-budget blocks, and EOF-malformed blocks.

3. MAJOR - Review artifact and sidecar scanning lacked selector grammar, sidecar suffix set, missing-sidecar semantics, symlink/path traversal rules, and tracked/untracked handling. Required fix: define exact review selectors and fail-closed selection behavior before artifacts can be cited.

4. MAJOR - Issue/comment snapshot handling lacked a closed metadata schema and pre-post/refetch pairing proof. Required fix: define snapshot keys, phase/source enums, comment IDs, URLs, timestamps, body hash checks, and mismatch rejection tests.

5. MAJOR - The self-scan test only named test files, not every #68 artifact. Required fix: require scanner self-scan over contract, scanner library, CLI, workflow, plan, README, coordination, schema row, review artifacts, and sidecars.

## Verified Checks

- Read the target plan with line-oriented review.
- Verified #68 implementation artifacts and approval marker are still absent.
- Ran parent public scan and legal scan over the #68 plan; both passed before this revision.
- Checked existing #65 key-bypass validation, #66 placeholder contract, and #69 legal scan precedent.
- Read live issue metadata for #68, #66, and #69.

## Limitations

- This was a Codex subagent review, not a distinct provider review.
- No labels, comments, commits, or file edits were performed by the reviewer.
