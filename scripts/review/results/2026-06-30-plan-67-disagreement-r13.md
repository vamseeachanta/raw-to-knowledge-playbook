# Disagreement report — plan #67 (2026-06-30)

## Verdicts

| Provider | Verdict |
|---|---|
| claude | **MINOR** |
| codex | MINOR |
| gemini | UNAVAILABLE (gemini CLI failed, rc=1: Warning: Basic terminal detected (TERM=dumb). Visual rendering will be limited. For the best experience, use a terminal emulator with truecolor support. Warning: 256-color support not detected. Using a terminal with at least 256-color support is recommended for a better visual experience. Error authenticating: IneligibleTierError: This client is no longer supported for Gemini Code Assist for indiv) |

## Findings unique to each provider

A finding is 'unique to X' if its text appears in X's artifact but not
verbatim in any other provider's artifact.

### claude

- **Parent-scanner subprocess call is coupled to full parent-coordination state, not just #67 leakage (MINOR).** Plan lines 452–455/542/575 frame the CI step as "invoke the parent scanner … forward each manifest path as `--scan-public-path`" — i.e., a #67-scoped leak scan. But `main()` (`scripts/validate_ace_epic_wave_coordination.py:795–800`) unconditionally also runs `validate_text()` on the coordination ledger **and** `validate_approval_marker(.planning/plan-approved/50.md, PARENT_ISSUE=50, …)`, summing all three error lists before the exit code. So the #67 subprocess returns nonzero whenever the ledger drifts or the **parent (#50)** approval marker is missing/malformed — for reasons wholly unrelated to any #67 artifact leaking. The plan does not acknowledge this false-fail surface. Cleaner: `import validate_public_artifact_paths` directly, or state the coupling explicitly.
- **`guard_no_source_root_access` return-vs-raise contract is ambiguous for a security boundary (MINOR).** Contract shape (line 202) says the helper "**returns or raises** `ACE_SOURCE_ROOT_ACCESS_FORBIDDEN`", but the acceptance test (line 511) and criterion (line 568) assert it "**Returns** `ACE_SOURCE_ROOT_ACCESS_FORBIDDEN`." For a refusal boundary the distinction is load-bearing: a caller that ignores a returned sentinel silently proceeds, whereas a raised exception halts. "Returns or raises" makes `test_validator_refuses_private_reads_when_ace_share_root_is_set` satisfiable by either control flow, so it can't actually pin the guarantee. Pick one contract.
- **Review-artifact discovery has no specified, scanner-safe listing API, and the plan forbids itself an escape hatch (MINOR).** The plan requires the #67 validator to *derive* its public-scan manifest by enumerating prefix-matching files under `scripts/review/results/` (lines 446–447, tests at 538–539), yet `test_validator_source_avoids_unbounded_discovery` only says "no *unbounded* traversal APIs." Two of the parent's denied traversal patterns are unconditional recursive Python/path traversal API denials (lines 152–153), with no manifest-path gate, and the plan explicitly bars adding any scanner exemption (line 317). An implementer who reaches for those recursive APIs to discover artifacts self-blocks with no legal remedy. The plan should name the concrete bounded API it intends (non-recursive `Path.glob`/`iterdir` on the single fixed results dir, which are not in the denied set) rather than leave it to implementation.

### codex

- `docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md:177` says the implementation will create a closed JSON contract “with these top-level fields,” but the table does not include `bound_skill_groups`. The same plan says only the #65 set will populate contract `bound_skill_groups` at line 29, and `test_contract_imports_65_schema_terms` expects bound skill groups to match #65 at line 491. The contract shape and test expectations are out of sync.
- The fixture evidence rows under-list required evidence fields. `Snapshot Evidence Shape` requires `recorded_at` for `shape_only_fixture` at lines 252 and 259, but `metadata-shape-only-evidence-request.json` at line 274 only names `evidence_mode=shape_only_fixture`, `source_issue=62`, and no blocked-state fields. The runtime downstream blocked fixture at line 275 similarly omits `source_issue` and `recorded_at`, although `blocked_pending_62_contract` requires both at line 260.
- The split-registry readiness rule is internally inconsistent. Pseudocode says `#67` “remains implementation_ready=false” at line 354 and again at line 459, but `test_wave0_split_registry_records_67_plan_status` at line 540 says `implementation_ready` must match the current gate state after implementation. Existing #65 precedent has `implementation_ready=true` once implemented in `artifacts/ace-wave0-ledger-schema.json:278`, with validator enforcement in `scripts/validate_ace_wave0_schema_contract.py:258-267`.
- `test_downstream_shape_only_fixture_accepts_complete_62_evidence_shape` at `docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md:504` is still named as a downstream fixture test, but the fixture it describes is a #67 `metadata_only_fixture` at line 274 and cannot authorize downstream sampling. The name preserves an old ambiguity even though the fixture path was renamed.

### gemini

- (none)
