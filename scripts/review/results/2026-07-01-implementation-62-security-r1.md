# Issue 62 Implementation Review r1 — Security and Public Surface

Verdict: MAJOR

Scope: read-only review of the initial #62 implementation artifacts before the r2 patch wave.

Findings:

1. MAJOR — `validator_command` evidence was not closed. The validator accepted alternate commands that included unrelated contract arguments as long as the expected prefix and evidence path appeared. Impact: command evidence could be ambiguous and undermine the env/argv separation boundary.

2. MAJOR — evidence artifact refs were lexical-only and could escape allowed roots through a symlink placed under the allowed fixture directory. Impact: request-pointer validation could read a JSON record outside the allowed artifact roots.

3. MAJOR — reconciliation refs were not validated against the intended root object. This overlapped with the contract-runtime review and caused valid warning refs to fail while compatible records could retain refs.

4. MAJOR — the repo-local legal scan script was missing, so the required legal/security gate could not be enforced in this repository. Manual public-surface probing did not find retained raw/private values, but the gate itself was unavailable.

Checked:

- #62 validator command with the fixture evidence
- #62 unittest module
- parent public-scan invocation over #62 paths
- parent coordination validator
- wave-0 schema validator
- skill validator
- `git diff --check`
- legal scan script presence probe

Disposition:

- r2 implementation closed the command grammar, resolved evidence refs with symlink checks, hardened reconciliation refs, and preserves the missing legal scan as a closeout gap tied to #69.
