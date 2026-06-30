review_artifact_role: public_history

# Disagreement report — plan #51 (2026-06-29)

## Verdicts

| Provider | Verdict |
|---|---|
| claude | MAJOR |
| codex | MAJOR |
| gemini | UNAVAILABLE (gemini CLI failed, rc=41: Error authenticating: FatalAuthenticationError: Manual authorization is required but the current session is non-interactive. Please run the Gemini CLI in an interactive terminal to log in, provide a GEMINI_API_KEY, or ensure Application Default Credentials are configured.     at initOauthClient (file:///home/vamsee/.npm-global/lib/node_modules/@google/gemini-cli/bundle/chunk-VLV2BYPM.js:269720:13)) |

## Findings unique to each provider

A finding is 'unique to X' if its text appears in X's artifact but not
verbatim in any other provider's artifact.

### claude

- **Cross-issue CI fragility: the hash-sweep report is keyed `path:line` over ~24 files maintained under other issues (plan §"Gaps", line 44; §reconcile, lines 341–342; TDD `test_existing_governance_docs_and_skills_do_not_publish_raw_hashes`, line 495).** The plan mandates that `artifacts/ace-source-hash-policy-sweep.md` classify "every unique `path:line` hit" from `rg ... docs skills`, and the test fails on any unclassified hit. The live sweep returns **90 hits across 24 files**; only a few are #51-owned. 36 hits are in this plan, the rest in sibling plans #50/#52–#63, `docs/{04,05,07,18,19}`, and 8 skill files — all edited under their own issues. Because dedup is explicitly "by canonical `path:line`" (line 342), any line insertion above a hit in any swept file shifts line numbers and invalidates the frozen report's keys, breaking #51's CI. The plan assigns no regeneration owner or staleness policy, so #51's green status is hostage to unrelated edits in files it does not own. This is the central structural risk and the wide blast radius (`Audit/conditional modify docs/plans/2026-06-29-issue-*.md` and "skill files returned by the sweep", lines 456–457) is disproportionate for a "wave 0 control plane" issue.
- **The plan's own prose "Source inventory" lists only 4 of the 7 authoritative fixed paths — self-failing-fixture risk (lines 29–32 vs. lines 78–84 / 128–135; TDD `test_fixed_source_evidence_paths_are_authoritative`, line 504).** The Resource-Intelligence "Source inventory" prose names only `INDEX.md`, `assets.json`, `_cad-index/index-summary.json`, and `llm-wiki` — omitting `docs/master-index.jsonl`, `_cad-index/cad-readability-index.tsv`, and `.ace-knowledge/index.db`. But line 137–138 states "prose source-inventory lists and fenced evidence rows must be generated from or validated against this exact set [of 7]," and the test requires "prose inventory and fenced evidence rows must match the same set." The term "prose source-inventory lists" is never disambiguated as to *which* prose; if it includes this section, the plan's own structure fails its own acceptance test.
- **`rg` reproducibility in CI is unspecified (validator orchestration, lines 113–119; acceptance lines 566, "validating repo fixtures/docs only").** To verify "every hit is classified," the validator must reproduce the 90-hit set, but the plan never says whether it shells out to `rg` (a Rust binary, not a Python stdlib dep — absent in a minimal `uv run` container, though present on GitHub ubuntu runners) or reimplements the alternation in Python `re`. The "CI must pass without ACE_SHARE_ROOT" criterion is asserted, but an unstated dependency on an external `rg` binary undercuts the "repo fixtures/docs only" claim and risks rg-version/Python-regex divergence for the "exact `rg` shape" the scanner must allowlist (line 252, `test_repo_local_hash_sweep_command_is_allowed`).
- **(MINOR/cosmetic) The authoritative sweep string carries a redundant glob (lines 252, 341, 496, 541).** In `rg --glob "*.md" --glob "SKILL.md"`, inclusive globs OR together and `SKILL.md ⊂ *.md`, so the second glob is a no-op. Harmless, but the plan elevates this exact string to a frozen, scanner-allowlisted "exact shape," baking the redundancy into the contract.

### codex

- The retained-review-artifact scan rule is still operationally ambiguous and currently fails if applied literally. Plan line 10 says historical rounds are retained as `scripts/review/results/2026-06-29-plan-51-*-r*.md`; lines 103-105 say to scan every retained `plan-51` artifact plus sidecars; lines 273-284 include every retained plan-51 review artifact in #51 public-surface scanning. But scanning all current `scripts/review/results/2026-06-29-plan-51-*.md` fails on six historical artifacts for denied traversal examples, including `claude-r3.md:34`, `claude-r6.md:18`, `codex-r2.md:26`, and `disagreement-r2.md:37`. Lines 401-404 and 576 later allow older local artifacts to be excluded if transient, but the plan never defines the manifest/status field that decides “retained for traceability” versus “transient local history.” A label-time operator can satisfy or fail the gate depending on interpretation.
- The r16 review summary contradicts the r16 disagreement artifact and the plan’s own verdict-parser contract. Plan lines 628-632 record `Claude r16 | MAJOR` and say “r16 returned MAJOR from both active providers.” But `scripts/review/results/2026-06-29-plan-51-disagreement-r16.md:7` records `claude | UNKNOWN`. The underlying Claude artifact uses `## VERDICT` at `scripts/review/results/2026-06-29-plan-51-claude-r16.md:7`, while the plan’s parser contract at lines 389-394 requires the first `## Verdict` heading or same-line `Verdict:` form. The plan is overstating review evidence that its own parser would not count.
- The public-token fixture marker is not mechanically specified. Plan lines 186-190 and acceptance line 537 require good fixtures to carry “generation request markers” that the validator expands at runtime, rejecting hand-authored concrete `public_source_token` values. The TDD row at line 490 repeats this, but the plan never defines the marker syntax, allowed location, required metadata fields, or how the scanner distinguishes the marker from arbitrary author prose. That leaves a correctness-critical token path to implementer invention.
- The pre-label comment-body digest option can collide with the raw-digest scanner policy. Plan line 577 allows the operator to verify the posted comment against “recorded SHA-256 digest,” while line 538 rejects source-like raw digests in public surfaces and only names Git commit SHA contexts as allowed. If that digest is recorded in the scanned issue-comment body or evidence comment, the plan’s own scanner can reject the status evidence; if it is not public, the plan does not say where it is recorded.

### gemini

- (none)

