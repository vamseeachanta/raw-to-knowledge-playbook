review_artifact_role: public_history

# Disagreement report — plan #51 (2026-06-29)

## Verdicts

| Provider | Verdict |
|---|---|
| claude | MINOR |
| codex | MAJOR |
| gemini | UNAVAILABLE (gemini CLI failed, rc=41: Error authenticating: FatalAuthenticationError: Manual authorization is required but the current session is non-interactive. Please run the Gemini CLI in an interactive terminal to log in, provide a GEMINI_API_KEY, or ensure Application Default Credentials are configured.     at initOauthClient (file:///home/vamsee/.npm-global/lib/node_modules/@google/gemini-cli/bundle/chunk-VLV2BYPM.js:269720:13)) |

## Findings unique to each provider

A finding is 'unique to X' if its text appears in X's artifact but not
verbatim in any other provider's artifact.

### claude

(no findings unique to this provider)

### codex

- Plan self-blocks on its own public token marker. Plan lines 191-196 define the only valid marker as `public_source_token: <GENERATE_PUBLIC_SOURCE_TOKEN>` and then say the same marker in prose, comments, config files, or public artifacts outside good fixture ledger rows fails validation. The plan itself is a public surface under lines 282-293 and 307-309, and it contains that exact marker at line 192 and again in the TDD table at line 506. As written, the required self-scan rejects the plan.
- Plan self-blocks on denied-command prose. Plan lines 265-275 classify inline denied commands and allow denied command names only in fixed methodology headings or the explicit repo-local `rg` governance scan shape. The plan then places `json.load`, `.read_text()`, `for line in open(...)`, `jq length`, `jq -c`, `cat`, `wc`, `sha256sum`, `os.walk`, `find`, `du`, `rg`, `fd`, and `ls -R` in TDD/acceptance prose at lines 514-515 and 562, including command flags and “ACE manifest/source paths.” Those are not headings and are inside a scan target.
- Review artifact role enforcement is inconsistent with the committed repo state. Plan lines 10, 52, 106, and 418-420 require committed/cited #51 review artifacts to carry `review_artifact_role=status_evidence` or `review_artifact_role=public_history`, while local-transient artifacts are never committed/cited. `git ls-files` shows r16/r17 #51 review artifacts are tracked, and `rg review_artifact_role scripts/review/results/2026-06-29-plan-51-*-r16.md ...r17.md` returns no role entries. The plan does not include an action to normalize, classify, or remove those already-committed artifacts before status transition.
- Live #63 issue text remains contradictory to the #51 token/hash contract and is outside the planned reconciliation scope. The #51 plan says public outputs use only `public_source_token` and raw source IDs/hashes remain private-only at lines 46-54, 220-221, and 343-348, but the live #63 issue body still says “Define public-safe source identifiers: `source_id`, `source_sha256`, `public_source_token`” and its acceptance criteria allow “token/hash/provenance IDs.” The #51 plan only reconciles the #63 plan file at line 474 and pre-label scans only the live #51 issue body at line 591, leaving a public upstream issue contract stale.
- The hash-policy sweep has a coverage mismatch. Plan lines 47, 351-352, and 557 bind the Python scanner to `docs/**/*.md` and `skills/**/SKILL.md`, but the operator preview at lines 261 and 350 uses `rg ... docs skills --glob "*.md"`, which includes top-level public methodology files. `skills/README.md:26` contains a `sha256` hit, and it is not covered by `skills/**/SKILL.md`. The plan can therefore claim every public methodology skill hash hit is classified while missing a public skill catalog hit.

### gemini

- (none)
