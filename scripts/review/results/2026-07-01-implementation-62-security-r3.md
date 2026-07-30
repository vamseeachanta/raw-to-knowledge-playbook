# Issue 62 Implementation Review r3 — Security and Public Surface

Verdict: MAJOR

Scope: read-only review after the r2 fix wave.

Findings:

1. MAJOR — parent readiness could still be forged using arbitrary repo-local JSON outside the #62 allowed evidence roots. The parent gate parsed `--evidence`, read the file, and checked the snapshot map, but did not require the evidence path to live under `artifacts/ace-manifest-freshness/` or `tests/fixtures/ace-manifest-freshness/`.

2. MINOR — first-time emission to the primary artifact root was unavailable while the subdirectory was absent.

3. EXTERNAL BLOCKER — the repo-local legal scan script remained unavailable. This was not counted as a #62 code defect because the missing gate predates and is owned by the repo-wide legal/security scan work.

Checked:

- #62 validator with fixture evidence
- parent coordination validator
- #62 unittest modules
- dynamic public-scan scope
- forged parent-readiness JSON and legal scan presence probes

Disposition:

- r4 implementation restricts parent evidence paths to the #62 allowed evidence roots and validates symlink-safe resolution. The artifact-root emission issue is fixed in the same r4 patch. The missing legal scan remains an explicit closeout blocker.
