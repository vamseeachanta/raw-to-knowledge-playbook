# Issue 70 Implementation Review - Contract Semantics

## Verdict

APPROVE after MAJOR fix.

## Initial Finding

The first pass independently found the same MAJOR symlink authorization class:
the #70 acceptance criteria require symlink evidence to fail closed, but the
initial trust helper could authorize a registry-pinned symlink artifact ref.

## Disposition

Fixed by adding pre-read symlink rejection in
`scripts/ace_manifest_evidence_trust.py`. The helper now rejects fixture refs
directly, rejects symlinked operational artifact refs before loading bytes, then
validates the parsed record through #62-owned evidence validation.

The operation-level API remains explicitly fail-closed:
`validate_manifest_operation("INDEX.md", "bounded_sample_selection")` still
returns `MISSING_62_EVIDENCE_CONTRACT` with blocked-by #62 and follow-on #70.
The #70 change opens only the sampling request validator path when a trusted
registry row is present.

## Re-Review

Targeted re-review returned APPROVE. Manual probes for direct and parent
symlinks failed closed with `INVALID_62_EVIDENCE_POINTER`, and literal fixture
refs failed closed with `FIXTURE_62_EVIDENCE_NOT_OPERATIONAL`.
