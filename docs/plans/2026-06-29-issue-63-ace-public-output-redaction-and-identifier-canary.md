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
- `docs/plans/README.md` now requires public artifacts to use `source_id`, `source_sha256`, `public_source_token`, and private-sidecar lookup keys rather than raw paths.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will define the route enum and public/private routing control plane.
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
- No allowlist mechanism exists for intentional aggregate counts and sanitized examples.

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
| Validator | scripts/validate_ace_public_artifacts.py |
| Canary fixtures | tests/fixtures/ace-public-artifact-safety/ |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-63-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-63-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-63-gemini.md |

---

## Deliverable

A public-output redaction contract and executable canary that blocks raw private paths, client-like identifiers, personal identifiers, unsafe row/table/field examples, media EXIF/GPS leakage, title-block/BOM leakage, and copied private snippets before ACE-derived artifacts are published.

---

## Pseudocode

```text
require #51 route enum and public/private routing contract
require #61 durable-output lifecycle contract
define public-safe source fields:
  source_id, source_sha256, public_source_token, private_lookup_key
define forbidden public artifact patterns:
  raw absolute host paths, private share-relative path fragments,
  email addresses, phone numbers, client-like/project-like identifiers,
  EXIF/GPS coordinates, title-block/BOM strings, unsafe table/field names,
  copied private snippets
define allowlist mechanism:
  path-scoped and line-scoped sentinels for sanitized aggregate counts only
scan planned public targets:
  docs, skills, review artifacts, issue-comment body files, future llm-wiki outputs
fail closed unless every finding is removed or explicitly allowed by a narrow sentinel
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-public-output-redaction-contract.md | Public-safe artifact and allowlist contract |
| Create | scripts/validate_ace_public_artifacts.py | Executable scanner/canary |
| Create | tests/fixtures/ace-public-artifact-safety/ | Synthetic positive/negative canary fixtures |
| Modify | .github/workflows/validate.yml | Run public artifact scanner against fixtures and public docs |
| Modify | docs/07-data-governance.md | Cross-link tokenization and public-safe source identifiers |
| Modify | docs/18-security-and-pii.md | Add ACE redaction canary classes |
| Modify | docs/19-trust-boundary-and-private-mode.md | Add public/private publication gate |
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
| test_allows_source_tokens_and_hashes | Safe provenance | `source_id`, SHA-256, public token | Validation passes |
| test_allowlist_is_narrow | Exception hygiene | Whole-file allowlist attempt | Validation fails; line/path-scoped sentinel required |
| test_downstream_wave_publication_requires_canary | Gate binding | Wave closeout/publication checklist | Canary command required before closeout |

---

## Acceptance Criteria

- [ ] Public artifacts use token/hash/provenance IDs rather than raw private paths.
- [ ] Redaction canary blocks raw host paths, private path fragments, client-like identifiers, personal identifiers, emails, phones, EXIF/GPS, title-block/BOM strings, unsafe table/field names, and copied private snippets.
- [ ] Sanitized aggregate counts are allowed only through narrow path-scoped or line-scoped sentinels.
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

- **Risk:** Over-broad deny patterns can block their own tests and docs; implementation must use narrow fixture paths and scoped sentinels.
- **Risk:** Under-broad patterns can create false confidence; the canary must focus on defect classes surfaced by actual ACE wave plans.
- **Open:** [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) must define route targets before downstream waves rely on publication decisions.

---

## Complexity

**T3** - security-sensitive public artifact scanner with canary fixtures, allowlist design, docs, skill updates, and cross-wave closeout binding.
