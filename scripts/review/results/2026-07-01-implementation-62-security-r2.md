# Issue 62 Implementation Review r2 — Security and Public Surface

Verdict: MAJOR

Scope: read-only review after the r1 fix wave.

Findings:

1. MAJOR — direct `--evidence` file validation still accepted caller-supplied absolute paths because only request-pointer artifacts used the safe artifact resolver. Impact: a local absolute JSON file could be accepted as authoritative #62 evidence.

2. MAJOR — evidence emission could write through an allowed-looking symlink under the artifact roots because output used the raw repo path after only lexical ref validation. Impact: an emit command could overwrite outside the allowed artifact roots.

3. MAJOR — the repo-local legal scan script was still missing. The #62 public scanner found no retained raw/private values in the reviewed files, but the required repository-wide legal scan gate remained unavailable.

Checked:

- #62 validator with fixture evidence
- parent coordination validator
- #62 unittest modules
- evidence-path and symlink-output probes
- legal scan script presence probe

Disposition:

- r3 implementation routes evidence-file reads through safe existing artifact resolution and routes emission writes through safe output artifact resolution. The missing legal scan remains a repo-wide closeout blocker outside #62 scope.
