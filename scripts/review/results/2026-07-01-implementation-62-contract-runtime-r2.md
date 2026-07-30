# Issue 62 Implementation Review r2 — Contract Runtime

Verdict: MAJOR

Scope: read-only review after the r1 fix wave.

Findings:

1. MAJOR — runtime emission did not classify mismatched comparable counts as drift. The emitter only checked missing or unavailable evidence modes, so mismatched under-cap manifest counts still produced `compatible` verdicts and `sampling_allowed`.

2. MAJOR — malformed operational maps did not fully fail closed. A non-object drift verdict map could skip exact-pair validation, and a non-object nested source status could crash later pair-support validation instead of returning a DENY error.

3. MAJOR — emitted operational evidence recorded a non-replayable command. The default `validator_command` used `--emit-evidence` without the required share-root and reviewed-commit inputs, so replaying the recorded argv failed.

4. MINOR — reconciliation refs were too loose. Non-numeric issue URLs and missing repo-relative paths satisfied the requirement.

Checked:

- #62 validator with fixture evidence
- #62 contract/runtime unittest modules
- temp-only malformed-map, mismatched-count, command-replay, and reconciliation-ref probes

Disposition:

- r3 implementation adds bounded internal count comparison, closes malformed shape paths, records replayable `--evidence` commands, and tightens reconciliation-ref grammar/existence checks.
