# Disagreement report - plan #67 r1

## Verdicts

| Provider | Verdict |
|---|---|
| Claude | MAJOR |
| Codex | MAJOR |
| Gemini | UNAVAILABLE |

## Shared / Complementary Findings

- Both active providers found the plan was not ready for `status:plan-review`.
- Claude focused on self-scanner reflexivity, executable-context rule specificity, manifest-source authority, stale Files-to-Change wording, CI command mismatch, and registry scan coverage.
- Codex focused on #62 gate bypass by request-class self-selection, missing seed/sort grammar, missing legal-scan closeout blocking, review-sidecar disposition, and stale plan-existence wording.

## Resolution Direction

- Patch the plan to bind requests to target issue and wave class.
- Define deterministic seed and neutral sort-policy grammar.
- State how classifier/test source avoids public-scan self-blocking.
- Correct manifest-source authority to the coordination ledger.
- Treat missing legal/security scan as a closeout blocker without explicit deferral or approved fallback scan.
- Do not advance #67 to `status:plan-review` until a fresh active-provider re-review has no MAJOR findings.

