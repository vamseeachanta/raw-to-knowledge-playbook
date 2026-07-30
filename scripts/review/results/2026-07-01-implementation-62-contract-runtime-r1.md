# Issue 62 Implementation Review r1 — Contract Runtime

Verdict: MAJOR

Scope: read-only review of the initial #62 implementation artifacts before the r2 patch wave.

Findings:

1. MAJOR — `reconciliation_refs` validation used the drift-verdict map instead of the root operational record. `scripts/ace_manifest_freshness_operational.py` called the reconciliation check with pair verdicts, while the callee expected root-level `reconciliation_refs`. Impact: compatible records could carry unnecessary refs and warning records with valid refs still failed.

2. MAJOR — drift pair validation checked only pair IDs and known manifest keys, not the exact `pair_id -> left_source/right_source` binding required by the plan and contract. Impact: a contract could silently remap a pair to different sources while passing validation.

3. MAJOR — the initial CLI validated pre-existing evidence but did not provide the planned runtime evidence-emission path from a share root. Impact: #70 would receive a schema and fixture but no #62-produced operational evidence artifact shape.

Checked:

- `scripts/validate_ace_manifest_freshness.py --evidence tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json`
- `python -m unittest tests.test_validate_ace_manifest_freshness`
- `scripts/validate_ace_epic_wave_coordination.py`
- `scripts/validate_ace_wave0_schema_contract.py`

Disposition:

- r2 implementation added exact pair binding validation, fixed reconciliation-ref wiring, and added runtime evidence builder/emitter coverage.
