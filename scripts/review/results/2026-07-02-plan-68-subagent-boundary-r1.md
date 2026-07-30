# #68 Plan Review - Dependency Boundaries r1

Reviewer: Codex subagent boundary lane
Scope: `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md`
Mode: read-only adversarial review
Verdict: MAJOR

## Findings

1. MAJOR - The plan said #68 would consume [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66), but did not make `config/ace-public-token-fixture-contract.json` an authoritative input in pseudocode, artifact map, TDD, or acceptance criteria. Required fix: load #66, add drift tests, and prevent a duplicated #68 token or placeholder grammar.

2. MAJOR - The plan still framed [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) as a downstream wrapper even though #69 is already implemented as a narrower sibling legal/security gate. Required fix: rewrite #68 so #69 is preserved, not redefined or made dependent on #68.

3. MAJOR - #68 allow-context semantics conflicted with the implemented #69 legal scan context model. Required fix: leave `.legal-deny-list.yaml` under #69's same-line sentinel/rule/path semantics or explicitly import those semantics without replacing them.

4. MINOR - The plan proposed workflow edits without a test that preserves the existing #69 CI command. Required fix: add TDD/acceptance coverage that the workflow still runs `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces`.

## Verified Checks

- Checked the #68 plan dependency claims, pseudocode, files-to-change, TDD, acceptance, and risks.
- Checked the #66 plan, `config/ace-public-token-fixture-contract.json`, fixture scripts, and fixture tests.
- Checked the #69 plan, legal scan config, scanner, wrapper, tests, and workflow wiring.
- Verified schema split dependencies: #68 depends on #65 and #66; #69 depends on #65.
- Ran read-only validators for #66 fixtures, #65 schema, and #69 legal scan.

## Limitations

- This was a Codex subagent review, not a distinct provider review.
- No labels, comments, commits, or file edits were performed by the reviewer.
