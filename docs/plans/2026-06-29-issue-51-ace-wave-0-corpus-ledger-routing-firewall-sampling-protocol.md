# Plan for #51: ACE Wave 0 Corpus Ledger, Routing Firewall, and Sampling Protocol

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** PENDING final no-MAJOR round; historical r16-r26 artifacts remain public-history evidence only

---

## Resource Intelligence Summary

### Existing repo code/docs

- `docs/01-document-taxonomy.md` defines content-first routing and extraction levels that ACE wave plans will consume.
- `docs/07-data-governance.md` and `docs/19-trust-boundary-and-private-mode.md` require raw/private material to stay out of public methodology artifacts.
- `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` carry the current ACE portfolio gates.
- `skills/README.md` lists the routing, triage, coverage, page-shape, and review skills that downstream wave plans will bind.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic. It authorizes coordination and planning, not child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will remain the wave-0 umbrella and interface plan.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) will own durable storage, lifecycle, retrieval, and success metric gates.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) will own manifest freshness and snapshot evidence before downstream sampling.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will own public-output redaction, maintained private deny-lists, publication certification, shared public-output config, and source-hash policy sweep.

### Source inventory

- The plan will use only metadata-index evidence from the fixed logical source list below.
- The plan will not ingest content, count the whole share, materialize broad manifests, publish exact sizes/dates/counts, or copy private corpus values.
- The root abstraction is `ACE_SHARE_ROOT`; public surfaces must not record the host-local root.

```ace-metadata-index-evidence
EXISTS ACE_SHARE_ROOT/INDEX.md type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/assets.json type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/docs/master-index.jsonl type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/_cad-index/index-summary.json type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/_cad-index/cad-readability-index.tsv type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/.ace-knowledge/index.db type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/llm-wiki type=directory details=withheld_public
```

### Gaps identified

- The r26 version of this plan bundled too much implementation scope into one review target.
- The active split will move implementation slices into [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- Each split issue will need its own plan, adversarial review, and user approval before implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) still needs a fresh no-MAJOR plan review after the split rewrite.
- Gemini review remains unavailable in current noninteractive runs until auth is restored or the user explicitly authorizes a one-round degraded quorum after seeing that evidence.

### Evidence

**Issue status** (verified 2026-06-30):

```text
#51 OPEN ACE wave 0: corpus ledger, routing firewall, and sampling protocol labels=strengthening,lane:claude,priority:high
```

**Split issues created from #51 r26 scope** (verified 2026-06-30):

- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) ACE wave 0 split: ledger schema and route-store matrix
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) ACE wave 0 split: public-token fixtures and private-field placeholders
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) ACE wave 0 split: bounded sampling firewall
- [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) ACE wave 0 split: public-surface self-scan for control-plane artifacts
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) ACE wave 0 split: repo-local legal and security scan gate

**Reproduction proofs**:
N/A - governance/planning issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-06-29-issue-51-ace-wave-0-corpus-ledger-routing-firewall-sampling-protocol.md` |
| Plan index | `docs/plans/README.md` |
| ACE coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Historical #51 review artifacts | `scripts/review/results/2026-06-29-plan-51-*-r16.md` through r25, plus `scripts/review/results/2026-06-30-plan-51-*-r26.md` |
| Split issue bodies | GitHub issues [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) |
| Future split plans | `docs/plans/YYYY-MM-DD-issue-65-*.md` through `docs/plans/YYYY-MM-DD-issue-69-*.md` |

---

## Deliverable

[#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will deliver a wave-0 umbrella contract and dependency map. It will not implement the script modules, fixtures, legal scanner, public-surface scanner, sampling firewall, or durable stores directly.

The implementation work will be reviewed issue-by-issue:

| Issue | Owner scope | Lane | Status |
|---|---|---|---|
| [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) | Ledger schema, closed route enum, route-to-logical-store matrix, verification state, and structural registry validation | lane:claude | draft issue; plan required |
| [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) | Fixture-only public-token contract and private-field placeholder grammar | lane:codex | draft issue; plan required |
| [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) | Bounded sampling firewall and executable-context checks | lane:codex | draft issue; plan required |
| [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) | Generic #51 public-surface self-scan for control-plane artifacts, review artifacts, sidecars, and issue/comment snapshots | lane:claude | draft issue; plan required |
| [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) | Repo-local legal/security scan wrapper and self-scan-safe deny-list config | lane:claude | draft issue; plan required |

### Scope Decision

The split branch will be taken. [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will remain the umbrella dependency and review surface; [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will carry implementation-sized plans.

This plan will not request implementation approval for any child slice. A future user approval on [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will authorize only the umbrella coordination artifact unless the approval explicitly names a split child issue and its reviewed plan.

### Dependency Rules

- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) should be planned first because it defines the schema fields and route/store vocabulary consumed by the other split issues.
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) should follow [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) because placeholder fields and token grammar depend on the ledger schema.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) should follow [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) because manifest snapshot fields and wave classes are part of the schema.
- [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) should follow [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) and [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) because it will scan public-safe placeholder and token contexts.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) should follow or pair with [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) because deny-list config self-safety must not become a blanket exemption.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61), [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62), and [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) remain cross-wave gates and do not become implementation children of [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51).

---

## Pseudocode

```text
read #51, #50, #61, #62, #63, and split issues #65-#69
verify no split issue carries status:plan-review or status:plan-approved before review
record split registry in this plan, README, and coordination artifact
keep #51 implementation-ready=false until user approval exists for a reviewed #51 umbrella plan
for each split issue:
  require a standalone issue plan
  require adversarial plan review
  require user approval before implementation
  require TDD and code/artifact review before closeout
when drafting split plans:
  keep public surfaces under ACE_SHARE_ROOT abstraction
  avoid private corpus content, raw host paths, exact private inventory counts, and client identifiers
  use the issue-owned playbook method and skill bindings
do not create #51 implementation scripts or tests from this umbrella plan
```

---

## Files to Change

| Action | Path or issue | Reason |
|---|---|---|
| Modify | `docs/plans/2026-06-29-issue-51-ace-wave-0-corpus-ledger-routing-firewall-sampling-protocol.md` | Replace bundled r26 implementation scope with a split-issue umbrella plan |
| Modify | `docs/plans/README.md` | Record that [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) split scope into [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Add a wave-0 split registry without marking the split issues implementation-ready |
| Comment | [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) | Record the split and the next planning sequence |
| Comment | [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) | Record parent-level coordination status without editing the parent issue body |

No implementation files will be created by this [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) umbrella revision.

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_parent_coordination_validator_still_passes` | The existing ACE coordination validator remains green after adding the split registry | `docs/plans/ace-share-ingestion-wave-coordination.md` | Validator passes with canonical #51-#63 registry intact |
| `test_plan_index_records_split_without_approval` | The plan index records split state without implying readiness | `docs/plans/README.md` | [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains draft and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) remain plan-required |
| `test_split_issues_have_no_status_gate_labels` | Split issues are not accidentally advanced | Live issue snapshots for [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) | No `status:plan-review` or `status:plan-approved` labels |
| `test_public_scan_accepts_split_artifacts` | Split docs and issue/comment bodies remain public-safe | Plans, README, coordination doc, and fetched issue/comment bodies | No raw host paths, private corpus values, personal identifiers, or unsafe source-provenance values |

---

## Acceptance Criteria

- [ ] [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) exist and carry only planning-safe labels (`strengthening`, one `lane:*`, and priority), not `status:plan-review` or `status:plan-approved`.
- [ ] [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) no longer claims that one broad implementation will create token, sampling, public-scan, legal-scan, and validator modules in a single approval unit.
- [ ] `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` record the split registry while preserving the canonical #51-#63 child wave ledger for the approved parent epic.
- [ ] Every split issue body requires a standalone plan, adversarial review, user approval, and TDD implementation before closeout.
- [ ] No split issue is implementation-ready until its own GitHub issue has `status:plan-approved` and a matching local approval marker.
- [ ] Public surfaces use the `ACE_SHARE_ROOT` abstraction and do not publish private source content, raw host paths, exact private inventory counts, client identifiers, or personal identifiers.
- [ ] Verification commands pass before commit/comment: parent coordination validator, unit tests for that validator, skill validation, public fallback scan, and `git diff --check`.
- [ ] No `status:plan-review` transition is attempted for [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) until a fresh adversarial review of the split rewrite returns no active-provider MAJORs and Gemini is restored or a user-authorized degraded quorum is explicitly recorded.

---

## Pre-Label Evidence Checklist

These checks must be satisfied before [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) can move to `status:plan-review`:

- Live issue snapshots for [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will be fetched and scanned.
- `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` will match the split scope.
- Fresh review artifacts will be created for the split rewrite and will cite the same reviewed commit, tree, and plan blob identity.
- Gemini availability will be restored, or the user will explicitly authorize one degraded-quorum round after the auth failure is disclosed.
- Implementation will remain stopped after `status:plan-review`; user approval will still be required.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r26 | MAJOR | Required explicit split-vs-bundled scope decision, machine-parseable self-scan anchors, Gemini restoration or waiver, fresh no-MAJOR evidence, and less compound acceptance criteria. |
| Codex r26 | MAJOR | Required tracked review artifact normalization, fallback scanner hardening for local path leaks, fresh no-MAJOR evidence, and explicit split-vs-bundled scope decision. |
| Gemini r26 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| r27 split rewrite | PENDING | Fresh review will be required before plan-review. |

**Overall result:** This plan remains draft-only. The r27 rewrite will take the split path and will keep [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) as an umbrella coordination plan. No implementation or approval label will be applied by this plan revision.

---

## Risks and Open Questions

- **Risk:** The split registry can drift from issue bodies; closeout must refetch live issue metadata before any status transition.
- **Risk:** Review fatigue from r1-r26 can hide fresh defects; r27 review must treat the rewritten plan as a new artifact, not a patched version to rubber-stamp.
- **Risk:** Gemini remains unavailable; the plan cannot enter `status:plan-review` unless Gemini is restored or the user explicitly authorizes a degraded-quorum round.
- **Open:** The next concrete planning target should be [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65), because the other split issues depend on its schema vocabulary.

---

## Complexity

**T3** - security-sensitive cross-wave planning and dependency governance, now split into issue-sized implementation plans.
