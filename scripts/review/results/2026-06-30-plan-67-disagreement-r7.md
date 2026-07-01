# Disagreement report - plan #67 (2026-06-30)

## Verdicts

| Provider | Verdict |
|---|---|
| Claude | MAJOR |
| Codex | MAJOR |
| Gemini | UNAVAILABLE |

## Claude Findings
- The snapshot-evidence discriminator was vacuous because `metadata_fixture_scope` was a singleton and did not actually narrow when metadata fixtures may carry `snapshot_evidence`.
- The #62 snapshot gate re-derived the target issue set instead of consuming #65 `requires_manifest_snapshot_id`.
- The adversarial-review gate had no quorum rule while Gemini had returned no usable signal.
- CI public-scan wiring for #67 artifacts was under-specified.
- The skill-validation command style was inconsistent with surrounding acceptance commands.

## Codex Findings
- Markdown executable-context tests missed non-whitelisted Markdown cases that could still contain runnable denied examples.
- Private root-read refusal needed guards for metadata access as well as file content reads.
- The metadata-only control-plane fixture wording conflicted with the closed request-class mapping.

## Resolution Direction
- Gate snapshot evidence on `evidence_mode`, not a singleton fixture-scope value.
- Import #65 `requires_manifest_snapshot_id` as the single source of truth for downstream snapshot gating.
- Define a degraded-provider quorum rule requiring two usable no-MAJOR providers.
- Pin CI to run the parent public scanner with explicit #67 path arguments, in addition to the #67 validator and tests.
- Add non-whitelisted Markdown denial fixtures and source-root metadata-access guards.
- Rename the metadata-only fixture test to avoid a control-plane/metadata hybrid.

## Sanitization Note
The raw disagreement report included scanner-triggering command and manifest examples from provider output. This retained artifact preserves review substance without those literals.
