review_artifact_role: public_history

# Disagreement report - plan #51 (2026-06-29)

## Verdicts

| Provider | Verdict |
|---|---|
| claude | MAJOR |
| codex | MAJOR |
| gemini | UNAVAILABLE (gemini CLI failed, rc=41: Error authenticating: FatalAuthenticationError: Manual authorization is required but the current session is non-interactive. Please run the Gemini CLI in an interactive terminal to log in, provide a GEMINI_API_KEY, or ensure Application Default Credentials are configured.     at initOauthClient (<LOCAL_FILE_URI>)) |

## Findings unique to each provider

A finding is 'unique to X' if its text appears in X's artifact but not
verbatim in any other provider's artifact.

### claude

(no findings unique to this provider)

### codex

- `docs/plans/2026-06-29-issue-51-ace-wave-0-corpus-ledger-routing-firewall-sampling-protocol.md` lines 100, 102, and 530 require retained `plan-51` review artifacts to be scanned before labeling. Current retained artifacts fail that fallback scan: `scripts/review/results/2026-06-29-plan-51-claude-r3.md:34`, `claude-r6.md:18`, `claude-r6.md:34`, `codex-r2.md:26`, `disagreement-r2.md:37`, and `disagreement-r3.md:39` are rejected for quoted denied traversal examples. Plan lines 379-385 only define normalization for private paths/identifiers, not for historical review prose containing denied-command examples, so the pre-label scan gate is currently unsatisfiable while retaining those artifacts.
- The JSON config self-scan policy is internally inconsistent. Plan lines 181-185 and acceptance line 495 require `config/ace-public-output-contract.json` to contain private-only provenance fields and banned public source-reference fields; lines 325-333 and acceptance line 504 include that config and the deny-list config in the public-surface scan. But lines 290-296 allow literal private schema field names only in plans, coordination docs, artifacts, skill instructions, validator constants, and tests, then reject JSON/YAML key-value contexts. The config files are not named as closed policy/schema contexts, so a compliant config containing `source_sha256` or `private_lookup_key` can self-block unless an unplanned exemption is added.
- The pre-label checklist omits same-stem review sidecars. Plan lines 102, 255, 335, and acceptance line 504 require `.md.err`, `.err`, `.stderr`, and `.log` sidecars to be scanned when present, but checklist line 530 only names retained review artifacts. I found no current sidecars, so this is not presently blocking, but the checklist can allow an unscanned sidecar if one is produced during the final review round.

### gemini

- (none)
