# Issue 70 Implementation Review - Security

## Verdict

APPROVE after MAJOR fix.

## Initial Finding

The first pass found a MAJOR symlink authorization bypass in the #70 trust
helper. An artifact ref under `artifacts/ace-manifest-freshness/` could be a
symlink to a fixture or other allowed-root file. Because the helper delegated
path safety to the #62 resolver before checking for symlinks, a registry-pinned
symlink target could authorize downstream sampling.

## Disposition

Fixed in `scripts/ace_manifest_evidence_trust.py` by rejecting any symlink in
the artifact path before `_safe_artifact_path()` reads or resolves the artifact.
The check walks both the file and parent directories.

Regression coverage was added in
`tests/test_validate_ace_manifest_evidence_integration.py` for a symlinked
operational artifact ref. The test failed before the patch with
`AUTHORIZED_62_EVIDENCE` and passes after the patch with a symlink fail-closed
result.

## Re-Review

Targeted re-review returned APPROVE. The reviewer probed direct file symlinks,
parent-directory symlinks, fixture refs, and operational refs; all failed closed
after the patch.
