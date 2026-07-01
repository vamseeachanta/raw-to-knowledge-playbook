# Disagreement report — plan #67 (2026-06-30)

## Verdicts

| Provider | Verdict |
|---|---|
| claude | **MAJOR** |
| codex | MAJOR |
| gemini | UNAVAILABLE (gemini CLI failed, rc=1: Warning: Basic terminal detected (TERM=dumb). Visual rendering will be limited. For the best experience, use a terminal emulator with truecolor support. Warning: 256-color support not detected. Using a terminal with at least 256-color support is recommended for a better visual experience. Error authenticating: IneligibleTierError: This client is no longer supported for Gemini Code Assist for indiv) |

## Findings unique to each provider

A finding is 'unique to X' if its text appears in X's artifact but not
verbatim in any other provider's artifact.

### claude

- **MAJOR — the authoritative #62 evidence-artifact schema is undefined, but the operational gate and its mismatch tests require parsing it; this is the unresolved core of the r4 "guessed #62 interface" MAJOR, merely relocated.** Lines 193-200 state the operational gate "will load and validate the authoritative #62 evidence artifact" and match `checker_ref`/`passing_command_ref`/`exit_code`/`snapshot_id`/`snapshot_artifact_ref` against it, and line 193 explicitly disclaims: "#67 will not hardcode a checker filename." Yet #62 is draft (`.planning/plan-approved/62.md` absent, `scripts/validate_ace_manifest_freshness.py` not implemented at HEAD, no evidence-artifact format defined anywhere). For `test_downstream_sampling_rejects_mismatched_62_evidence` (line 351, "controlled temp fixture with command, exit-code, snapshot-id, or artifact mismatch") and `test_downstream_sampling_rejects_self_attested_62_evidence` (line 350) to be implementable, #67's code must encode an assumed field structure of the authoritative artifact. That means #67 either (a) is unimplementable-as-specified for the operational path, or (b) silently defines the #62 evidence-artifact read contract it claims #62 owns. The plan removed the hardcoded filename that r4 flagged but never replaced it with a specified interface — it defers to an artifact that does not exist. No cross-issue sync mechanism is named to keep #67's assumed shape aligned with whatever #62 eventually emits.
- **MINOR — the firewall is only tested with `ACE_SHARE_ROOT` unset; there is no test that it refuses private reads when the root IS set.** Lines 45/402 and `test_control_plane_fixture_does_not_require_live_62` (line 353) prove pass-with-root-unset. For a security-sensitive sampling *firewall*, the more important assertion — that no private content is read when `ACE_SHARE_ROOT` is populated — is never exercised. The negative security property (the reason the firewall exists) is untested; only the availability property is.
- **MINOR — #67 modifies the parent's test file (`tests/test_validate_ace_epic_wave_coordination.py`, line 330) while explicitly avoiding modifying the parent script (line 329).** Asserting "the parent helper is non-authoritative for #67 source enumeration" belongs in #67's own test module, not grafted into the parent's test file. This re-introduces exactly the parent-helper blast-radius coupling that r3 flagged: a child issue editing the parent's tests couples their lifecycles and risks breaking the parent suite on unrelated parent changes.
- **MINOR — duplicated/diverging detection logic between the new classifier and the parent scanner, with no sync mechanism.** Line 23 concedes the parent validator "already carries public-surface denial primitives for … unbounded traversal patterns," and line 320 creates `scripts/ace_bounded_sampling_firewall.py` as a second "executable-context classifier." The plan asserts #67 is "narrower" (line 23) and reuses the parent scanner for public-surface scanning (line 405), but if the parent later adds a denied token/verb, the #67 classifier's independent enum (`command_verb_classes`, `denied_executable_classes`) will silently drift. No shared-source-of-truth is cited for the two detectors' denied-token vocabularies.
- **Checks run that found nothing wrong** (silence-is-failure compliance): (a) `bound_skill_groups` drift from r4 is **fixed** — plan line 29 and Artifact Map line 112 now bind exactly `{format-coverage-ledger, public-private-routing, content-triage-and-exclusion, page-shape-contract, adversarial-verify-loop}`, matching schema lines 160-166. (b) Caps authority from r4 is **fixed** — line 151 cites the coordination ledger, which does specify 200/25/1048576 (verified lines 18-20). (c) Environment-coupled #62-absence test from r4 is **fixed** — replaced by controlled temp fixture (lines 282, 348). (d) Malformed-marker and self-attestation gaps from r4 Codex are **fixed** (tests lines 349-350; validation line 192). (e) Fixture inventory from r4 is **fixed** — both fixtures now listed MISSING (lines 87-88). (f) Six manifest keys match the coordination ledger exactly. (g) All mapping-table wave classes exist in the #65 `canonical_wave_registry`; #64 is genuinely absent from both registries. (h) Plan + retained review artifacts empirically pass the parent public scanner (RC=0).

### codex

- Plan §Public-surface path list omits a changed public artifact. The Artifact Map lists `artifacts/ace-wave0-ledger-schema.json` as “Schema split registry update” at `docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md:109`, and Files to Change says to modify it at line 328. But the planned public-scan path list at lines 305-309 omits `artifacts/ace-wave0-ledger-schema.json`, and `test_public_scan_paths_cover_67_artifacts` at line 375 omits it too. This contradicts Acceptance Criteria lines 405 and 424, which require the complete #67 public path list to cover every #67 artifact.
- Plan §Files to Change promises to “Record the #67 plan path/status in the split registry” at `docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md:328`, but the TDD list has no assertion for that update. Current `artifacts/ace-wave0-ledger-schema.json:293-301` has the #67 row with `plan_path: ""` and `status_snapshot: "plan-required"`, and `scripts/validate_ace_wave0_schema_contract.py:258-265` skips plan-path/marker validation for every non-`implementation_ready` row. As written, an implementation can leave the #67 schema registry stale and still pass the listed validators.

### gemini

- (none)

