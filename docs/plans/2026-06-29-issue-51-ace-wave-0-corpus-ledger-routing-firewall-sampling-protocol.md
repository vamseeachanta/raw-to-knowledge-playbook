# Plan for #51: ACE Wave 0 Corpus Ledger, Routing Firewall, and Sampling Protocol

> **Status:** draft
> **Complexity:** T2
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-51-claude.md | scripts/review/results/2026-06-29-plan-51-codex.md | scripts/review/results/2026-06-29-plan-51-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/01-document-taxonomy.md` defines content-first routing and L0-L5 extraction levels; the ACE control plane must make those fields explicit before any wave ingests content.
- `docs/07-data-governance.md` and `docs/19-trust-boundary-and-private-mode.md` require raw sources off-repo, private data never crossing public boundaries, and provenance for derived material.
- `skills/README.md` lists the routing, triage, coverage, fidelity, page-shape, and review skills that #51 must bind to each downstream wave.

### Related issues
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the parent epic and requires every child to name method issues and skill groups.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) requires a ledger schema, route states, bounded sampling, exclusion classes, and closeout rules.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) depends on this control plane for storage/lifecycle routing decisions.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) will consume this sampling contract for manifest freshness/drift checks.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will consume this route/token contract for public-output redaction canaries; #51 will define the interface but will not require the #63-owned scanner to exist or pass.

### Source inventory
- `ACE_SHARE_ROOT/INDEX.md` exists and warns that the share contains client data and business records.
- `ACE_SHARE_ROOT/assets.json` is the broad file manifest: 3,077,754 file entries, generated 2026-04-03.
- `ACE_SHARE_ROOT/_cad-index/index-summary.json` is the newer CAD-specific source of truth for CAD counts, generated after the broad manifest.

### Gaps identified
- No repo-local ACE corpus ledger schema exists yet.
- No validated closed route enum exists for `public_llm_wiki`, `private_sidecar`, `metadata_only`, and `excluded_no_ingest`.
- No bounded sampling contract exists to prevent unbounded share crawls through `find`, `du`, `rg`, `fd`, `ls -R`, recursive globbing, `os.walk`, unrestricted `jq`, custom full-manifest loops, or full-file hashing/counting of large manifests.
- No public artifact safety gate exists to enforce source tokenization and private identifier denial before public `docs/` publication.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#51 OPEN ACE wave 0: corpus ledger, routing firewall, and sampling protocol labels=strengthening,lane:claude,priority:high
```

**File existence**:
```
EXISTS docs/01-document-taxonomy.md
EXISTS docs/07-data-governance.md
EXISTS docs/19-trust-boundary-and-private-mode.md
EXISTS skills/public-private-routing/SKILL.md
EXISTS ${ACE_SHARE_ROOT}/INDEX.md
EXISTS ${ACE_SHARE_ROOT}/assets.json
EXISTS ${ACE_SHARE_ROOT}/_cad-index/index-summary.json
MISSING docs/case-studies/ace-share-wave-0-control-plane.md
MISSING scripts/validate_ace_wave0_control_plane.py
```

**Reproduction proofs**:
N/A - governance/planning issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-51-ace-wave-0-corpus-ledger-routing-firewall-sampling-protocol.md |
| Control-plane doc | docs/case-studies/ace-share-wave-0-control-plane.md |
| Validator | scripts/validate_ace_wave0_control_plane.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-51-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-51-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-51-gemini.md |

---

## Deliverable

A documented and CI-validated ACE wave-0 control plane defining the ledger schema, routing firewall, exclusion classes, bounded sampling protocol, and downstream wave issue/skill map.

---

## Pseudocode

```text
load parent #50 and child issues #51-#61
define ledger required fields:
  source_id, source_sha256, public_source_token, private_lookup_key,
  share_relative_path_private_only, extension_family, content_class, sensitivity,
  route_target, extraction_level, lifecycle_state, expected_yield,
  measured_success_numerator, measured_success_denominator,
  exclusion_reason, method_issues, skill_group
define closed route enum:
  public_llm_wiki, private_sidecar, metadata_only, excluded_no_ingest
define lifecycle enum consumed from #61:
  candidate, provisional, verified, rejected, superseded, stale_requires_rescreen
define fail-closed exclusions:
  client_confidential, personal_pii, third_party_confidential, binary_noise, low_value
for every wave issue #52-#61:
  record extension family, inventory evidence, method issues, skill group, sampling rule,
  executable validator/canary file, and % ingested success formula
reject sampling commands that perform unbounded recursive traversal,
  full-manifest materialization, or full-file hashing/counting of large manifests
require ACE_SHARE_ROOT plus share-relative paths in scripts/tests
require public artifacts to use source_id/source_sha256/public_source_token, never raw paths
define the public-output canary input contract consumed by #63 without invoking #63's scanner
require every closeout to update a playbook doc/skill or file a follow-on issue for method gaps
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-share-wave-0-control-plane.md | Durable ACE ledger/routing/sampling contract |
| Create | scripts/validate_ace_wave0_control_plane.py | CI-checkable validator for required fields, routes, wave bindings, and sampling constraints |
| Reference | scripts/validate_ace_public_artifacts.py | Public-output safety gate owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63); #51 will define the route/token input contract only |
| Modify | .github/workflows/validate.yml | Run the new validator |
| Deferred | docs/index.md | Do not link the case study until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result |
| Deferred | mkdocs.yml | Do not publish the case study in site navigation until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result |
| Modify | skills/public-private-routing/SKILL.md | Add ACE route-state expectations |
| Modify | skills/content-triage-and-exclusion/SKILL.md | Add ACE exclusion-class expectations |
| Modify | skills/format-coverage-ledger/SKILL.md | Add ACE ledger expectations |
| Modify | skills/page-shape-contract/SKILL.md | Add ACE page/record shape expectations |
| Modify | skills/adversarial-verify-loop/SKILL.md | Require method-gap disposition in closeout |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_ace_ledger_schema_requires_all_control_fields | Ledger schema covers #51 fields | Case-study ledger table | Source token/hash fields, private lookup key, route, lifecycle, expected yield, measured success fields present |
| test_ace_route_enum_is_closed | Route targets are closed-set | Route table | Exactly four route targets |
| test_ace_route_and_lifecycle_are_separate | Route targets do not mix with lifecycle states | Route/lifecycle tables | No `private_only` or `excluded` lifecycle used as a route alias |
| test_ace_sampling_protocol_blocks_unbounded_crawls | Sampling rules do not allow unbounded crawls | Sampling section | Fails on unbounded `find`, `du`, `rg`, `fd`, `ls -R`, recursive glob, `os.walk`, unrestricted `jq`, custom full-manifest loop, or full-file hashing/counting of large manifests |
| test_ace_sampling_protocol_requires_caps | Sampling rules are bounded | Sampling section | Manifest source, seed/sort, per-bucket caps, max files, and max bytes are present |
| test_ace_share_root_required | Host portability | Script/test examples | Uses `ACE_SHARE_ROOT` plus share-relative paths |
| test_public_artifact_safety_gate_blocks_raw_identifiers | Public publication safety | Case-study and docs targets | Blocks raw paths, private identifiers, personal identifiers, and proprietary snippets |
| test_every_downstream_wave_has_issue_skill_and_validator | #52-#61 each have bindings | Wave map | No missing issue, skill group, eval data, or executable validator/canary |
| test_public_canary_is_referenced_not_required | #51/#63 dependency boundary | Control-plane contract | #51 records the #63 scanner interface but does not require `scripts/validate_ace_public_artifacts.py` to exist or pass |
| test_closeout_requires_method_gap_disposition | Method gaps cannot disappear | Closeout rule | Requires doc/skill update or follow-on issue |

---

## Acceptance Criteria

- [ ] Ledger schema covers all fields named in #51 plus downstream issue, skill, eval data, executable validator/canary, and measured success binding.
- [ ] Ledger distinguishes public `llm-wiki`, private sidecar, metadata-only, and excluded/no-ingest routing.
- [ ] Route targets are separate from lifecycle states; `private_only` and `exclude` aliases are rejected in favor of the closed enums.
- [ ] Every downstream ACE wave has a bounded sampling protocol and no unbounded share crawl, full-manifest materialization, or full-file hashing/counting of large manifests.
- [ ] Proposed scripts/tests use `ACE_SHARE_ROOT` plus share-relative paths.
- [ ] Public artifact safety gate blocks raw source paths, private identifiers, personal identifiers, and proprietary snippets before docs publication.
- [ ] #51 defines the public-output canary input contract consumed by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63), but it does not require `scripts/validate_ace_public_artifacts.py` to exist or pass.
- [ ] Any `docs/index.md` or `mkdocs.yml` publication of the #51 case study requires [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) `status:plan-approved`, local approval marker, implemented redaction canary, and recorded passing-command result.
- [ ] `% ingested success` numerator, denominator, threshold, and validation command are required for every downstream wave.
- [ ] Exclusion classes are fail-closed for PII, client-confidential, third-party-confidential, binary noise, and low-value material.
- [ ] `uv run python scripts/validate_ace_wave0_control_plane.py` passes.
- [ ] `uv run skills/validate_skill.py` passes after skill updates.

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

- **Risk:** ACE inventory can drift; implementation must use exact manifests, bounded freshness probes, and `ACE_SHARE_ROOT` rather than hardcoded host paths.
- **Risk:** `visibility` remains hand-set; the plan should require independent cross-check, not just schema presence.
- **Open:** The private sidecar store must be named before downstream waves rely on it.

---

## Complexity

**T2** - multi-file governance/doc plus validator work, but no content ingestion and no production pipeline change.
