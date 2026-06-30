# Plan for #63: ACE Cross-Wave Public-Output Redaction and Identifier Canary

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-63-claude.md | scripts/review/results/2026-06-29-plan-63-codex.md | scripts/review/results/2026-06-29-plan-63-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/07-data-governance.md`, `docs/18-security-and-pii.md`, and `docs/19-trust-boundary-and-private-mode.md` require raw/private material to stay out of public artifacts.
- `docs/plans/README.md` now requires public artifacts to use opaque `public_source_token` references rather than raw paths, raw source IDs, raw source hashes, private lookup keys, or private lookup maps.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will define the route enum, public/private routing control plane, token grammar, and fixture-generation boundary that this issue consumes.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) will define durable output and lifecycle gates.

### Related issues
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) owns the public-output redaction canary.
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the parent epic.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) and [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) are required upstream gates.
- [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) must run this canary before publication or closeout.

### Source inventory
- Inputs are public repo artifacts and synthetic canary fixtures only.
- This issue will not read private ACE source content; fixtures must be synthetic and client-neutral.

### Gaps identified
- No reusable public-output scanner exists for ACE-derived plans, docs, skills, issue comments, and future `llm-wiki` outputs.
- No explicit canary fixture set exists for path leaks, client-like identifiers, personal identifiers, EXIF/GPS leakage, title blocks, BOM names, table/field names, or copied private snippets.
- No content-pattern-restricted allowlist mechanism exists for intentional aggregate counts and sanitized examples.
- No implemented #63 scanner or shared `config/ace-public-output-contract.json` exists yet.
- No repo-wide ACE source-hash policy sweep exists to classify public methodology references that could treat raw source hashes as public-safe source references.

### Evidence

**Issue status** (verified 2026-06-29):
```
#63 OPEN ACE cross-wave: public-output redaction and identifier canary labels=strengthening,lane:claude,priority:high
```

**File existence**:
```
EXISTS docs/07-data-governance.md
EXISTS docs/18-security-and-pii.md
EXISTS docs/19-trust-boundary-and-private-mode.md
MISSING docs/case-studies/ace-public-output-redaction-contract.md
MISSING artifacts/ace-source-hash-policy-sweep.md
MISSING config/ace-public-output-contract.json
MISSING config/ace-public-surface-deny-list.json
MISSING scripts/ace_public_contract.py
MISSING scripts/validate_ace_public_artifacts.py
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-63-ace-public-output-redaction-and-identifier-canary.md |
| Redaction contract | docs/case-studies/ace-public-output-redaction-contract.md |
| Source-hash policy sweep report | artifacts/ace-source-hash-policy-sweep.md |
| Shared public contract | config/ace-public-output-contract.json |
| Public-surface deny-list | config/ace-public-surface-deny-list.json |
| Contract loader | scripts/ace_public_contract.py |
| Validator | scripts/validate_ace_public_artifacts.py |
| Canary fixtures | tests/fixtures/ace-public-artifact-safety/ |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-63-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-63-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-63-gemini.md |

---

## Deliverable

A public-output redaction contract, shared JSON config, source-hash policy sweep, and executable canary that blocks raw private paths, client-like identifiers, personal identifiers, unsafe row/table/field examples, media EXIF/GPS leakage, title-block/BOM leakage, raw source-hash public-reference claims, and copied private snippets before ACE-derived artifacts are published.

---

## Pseudocode

```text
require #51 route enum and public/private routing contract
require #61 durable-output lifecycle contract
create shared public contract at config/ace-public-output-contract.json:
  public_source_token grammar, private-only provenance fields,
  git-SHA governance exceptions, content-pattern-restricted allowlist policy,
  banned public source-reference fields, and source-hash private-sidecar policy
create config/ace-public-surface-deny-list.json:
  generic public-surface deny patterns and canary-owned pattern classes;
  no real client/project/customer names are committed
load shared public contract from config/ace-public-output-contract.json:
  public-safe source references, token grammar, private-only provenance fields,
  git-SHA governance exceptions, allowlist policy, and banned public fields
parse the shared contract with Python stdlib json; no YAML-only syntax or PyYAML dependency
  is required in CI
do not redefine token grammar or private-only provenance fields in #63-local constants;
  the shared config is authoritative
derive forbidden public artifact pattern classes from the shared config plus #63-owned
  non-source privacy scanners; the list below is illustrative and subordinate to config:
  raw absolute host paths, private share-relative path fragments,
  raw source_id values, raw source_sha256 values, private lookup key values,
  private lookup maps,
  email addresses, phone numbers, client-like/project-like identifiers,
  EXIF/GPS coordinates, title-block/BOM strings, unsafe table/field names,
  copied private snippets
derive allowlist mechanism from the shared config:
  content-pattern-restricted allowlists for sanitized aggregate counts and fixed examples only;
  no author-controlled arbitrary line/path sentinels and no blanket file/path exemptions
run repo-wide ACE source-hash policy sweep over repo-tracked docs/plans/skills markdown:
  record stable hit keys in artifacts/ace-source-hash-policy-sweep.md
  classify each hit as modify_public_safe_hash_claim or no_change_private_context
  modify public-safety/source-reference claims so raw source hashes are private-sidecar
  provenance only and public artifacts use public_source_token references
scan planned public targets:
  docs, skills, review artifacts, issue-comment body files, future llm-wiki outputs
fail closed unless every finding is removed or explicitly allowed by a narrow committed pattern
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-public-output-redaction-contract.md | Public-safe artifact and content-pattern-restricted allowlist contract |
| Create | artifacts/ace-source-hash-policy-sweep.md | Public-safe classification report for `sha256`/source-hash/provenance-pointer hits in docs, plans, and public methodology skills |
| Create | config/ace-public-output-contract.json | Shared public token/redaction/source-hash policy contract consumed by #63 canary and downstream waves |
| Create | config/ace-public-surface-deny-list.json | Generic public-surface deny patterns for #63 publication/comment certification |
| Create | scripts/ace_public_contract.py | JSON contract loader, private/public field classifier, and source-hash sweep classification helper; token generation remains in the #51-owned token module |
| Create | scripts/validate_ace_public_artifacts.py | Executable scanner/canary |
| Create | tests/fixtures/ace-public-artifact-safety/ | Synthetic positive/negative canary fixtures |
| Modify | .github/workflows/validate.yml | Run public artifact scanner against fixtures and public docs |
| Modify | docs/07-data-governance.md | Cross-link tokenization and public-safe source identifiers |
| Modify | docs/18-security-and-pii.md | Add ACE redaction canary classes |
| Modify | docs/19-trust-boundary-and-private-mode.md | Add public/private publication gate |
| Audit/conditional modify | docs/04-failure-modes.md | Classify source-hash hits; modify only public-safe source-reference claims |
| Audit/conditional modify | docs/05-good-practices.md | Classify source-hash hits; modify only public-safe source-reference claims |
| Audit/conditional modify | docs/plans/2026-06-29-issue-*.md returned by the sweep | Classify plan hits; modify only files whose hit claims raw source hashes are public-safe source references or publishes source-like digest values |
| Audit/conditional modify | public methodology skill markdown returned by the sweep, including top-level skill catalog files | Classify skill/catalog hits; modify only public-safe source-reference claims or assigned source-like digest values |
| Modify | skills/public-private-routing/SKILL.md | Require canary before public outputs |
| Modify | skills/public-private-routing/evals/evals.json | Add public-output canary eval data |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_blocks_raw_host_paths | Path leakage | Artifact with raw absolute path | Validation fails |
| test_blocks_private_identifier_patterns | Identifier leakage | Synthetic client/project/email/phone strings | Validation fails |
| test_blocks_exif_gps_and_media_metadata | Image/media leakage | Synthetic EXIF/GPS metadata fixture | Validation fails |
| test_blocks_title_block_bom_and_field_names | Engineering metadata leakage | Synthetic CAD/DB/table examples | Validation fails |
| test_allows_opaque_public_source_tokens | Safe public provenance | `public_source_token` values accepted by `config/ace-public-output-contract.json` | Validation passes |
| test_blocks_raw_source_ids_hashes_and_private_lookup_maps | Private provenance leakage | Raw `source_id`, `source_sha256`, `private_lookup_key`, lookup map, or share-relative path value | Validation fails |
| test_loads_shared_public_output_contract | Cross-wave contract reuse | `config/ace-public-output-contract.json` | Validator uses the shared token grammar, private-only fields, git-SHA governance exceptions, and allowlist policy |
| test_public_config_field_names_are_closed_schema_context | Config self-scan does not block its own schema contract | `config/ace-public-output-contract.json`, `config/ace-public-surface-deny-list.json`, and negative config fixtures | Allows private field names only as string enum/list values in designated config files; rejects assigned private values, private lookup maps, path-bearing values, and raw digest values |
| test_existing_governance_docs_and_skills_do_not_publish_raw_hashes | Existing docs/plans/skills cannot contradict public-token policy | Stable-hit-key results from the Python stdlib source-hash scanner over `docs/**/*.md`, `skills/**/*.md`, and top-level skill catalog markdown plus `artifacts/ace-source-hash-policy-sweep.md` | Every stable hit key is classified; modified claims no longer say raw hash pointers are always/public safe; assigned raw source-hash values are removed or rewritten; no-change hits have an allowed private/LFS/census/schema/validator rationale without published digest values |
| test_repo_local_hash_sweep_command_is_allowed | Hash-governance scan is not mistaken for ACE source sampling | Plan and scanner fixtures | Allows repo-local docs/skills hash-policy preview commands only when they do not touch `ACE_SHARE_ROOT`; rejects source-material traversal/count/hash commands |
| test_allowlist_is_narrow | Exception hygiene | Whole-file allowlist, arbitrary line/path sentinel, or author-controlled bypass attempt | Validation fails; only committed content-pattern-restricted examples are allowed |
| test_downstream_wave_publication_requires_canary | Gate binding | Wave closeout/publication checklist | Canary command required before closeout |

---

## Acceptance Criteria

- [ ] Public artifacts use only the public-safe source reference fields and token grammar from `config/ace-public-output-contract.json`.
- [ ] The canary loads `config/ace-public-output-contract.json` rather than redefining the token/private-field contract in #63-local prose or constants.
- [ ] Raw `source_id`, raw `source_sha256`, `private_lookup_key`, private lookup maps, and `share_relative_path_private_only` values are private-only because they are declared by `config/ace-public-output-contract.json`; #63 fails validation when public surfaces contain those fields as values or lookup maps.
- [ ] `config/ace-public-output-contract.json` and `config/ace-public-surface-deny-list.json` are closed policy/schema contexts: they may contain private field names only as string enum/list values for private-only or banned-public fields, and they reject assigned private values, private lookup maps, path-bearing values, and raw digest values.
- [ ] Every stable hit key from the Python stdlib source-hash scanner over repo-tracked `docs/**/*.md` and `skills/**/*.md`, including top-level skill catalog markdown, is recorded in `artifacts/ace-source-hash-policy-sweep.md` with a modify/no-change rationale. Dual-purpose hits with public-safety/source-reference language are modified; assigned raw source-hash/source-like digest values are removed or rewritten; raw source hashes become private-sidecar provenance, not public source references.
- [ ] Redaction canary blocks raw host paths, private path fragments, client-like identifiers, personal identifiers, emails, phones, EXIF/GPS, title-block/BOM strings, unsafe table/field names, and copied private snippets.
- [ ] Sanitized aggregate counts are allowed only through narrow committed content-pattern-restricted allowlists loaded from or mechanically subordinate to `config/ace-public-output-contract.json`; arbitrary author-controlled line/path sentinels and blanket file/path exemptions fail.
- [ ] Downstream wave plans reference `uv run python scripts/validate_ace_public_artifacts.py` before docs/mkdocs publication and issue closeout.
- [ ] The canary uses synthetic fixtures only and does not require reading private ACE source content.
- [ ] `uv run python scripts/validate_ace_public_artifacts.py` and `uv run skills/validate_skill.py` pass.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude | PENDING | Not yet reviewed |
| Codex | PENDING | Not yet reviewed |
| Gemini | PENDING | Not yet reviewed |

**Overall result:** PENDING - draft only; not ready for `status:plan-review`.

---

## Risks and Open Questions

- **Risk:** Over-broad deny patterns can block their own tests and docs; implementation must use narrow committed content-pattern fixtures and must not rely on author-controlled line/path sentinels or blanket file/path exemptions.
- **Risk:** Under-broad patterns can create false confidence; the canary must focus on defect classes surfaced by actual ACE wave plans.
- **Risk:** The source-hash policy sweep can grow large; implementation must produce deterministic stable hit keys and fail on unclassified hits rather than relying on reviewer memory.
- **Open:** [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) must define route targets before downstream waves rely on publication decisions.

---

## Complexity

**T3** - security-sensitive public artifact scanner with canary fixtures, content-pattern-restricted allowlist design, docs, skill updates, and cross-wave closeout binding.
