# Implementation Review: Issue 63 Public/Legal Safety

- Issue: #63
- Stage: implementation
- Reviewer lane: public-legal
- Verdict: MAJOR
- Post-review disposition: RESOLVED in main-session patch set before closeout.

## Findings

1. CI ran the #63 validator without the exact public-surface path list; the explicit path list was only passed to the #68 public-surface scanner.
2. Issue-comment closeout scanning existed as a CLI option but had no exercised CI fixture or operator-facing exact command.
3. The source-hash sweep was incomplete and missed public routing-skill guidance that still described a digest pointer as a public source reference.
4. The routing skill told operators to run the default canary only, which could omit changed publication surfaces.

## Resolution

- Updated `.github/workflows/validate.yml` so the #63 canary receives the same exact public path set as the #68 scanner.
- Added a safe issue-closeout body fixture and wired it through `--issue-comment-body-file` in CI.
- Rewrote the routing skill to require exact `--scan-public-path` surfaces and planned issue-comment body files.
- Removed digest-pointer public-source language from the routing skill.
- Rebuilt `artifacts/ace-source-hash-policy-sweep.md` from the validator-derived live docs/skills hit keys.

## Verification

- Exact-surface #63 canary passed with all CI-listed paths and the safe issue-comment body fixture.
- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_public_surface_scan.py` passed over the exact #63 path set.
- `bash scripts/legal/legal-sanity-scan.sh --scan-public-path ...` passed over the exact #63 path set.
- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` passed.
