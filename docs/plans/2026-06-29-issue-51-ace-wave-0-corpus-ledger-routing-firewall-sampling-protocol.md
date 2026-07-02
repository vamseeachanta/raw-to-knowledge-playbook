# Plan for #51: ACE Wave 0 Corpus Ledger, Routing Firewall, and Sampling Protocol

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** r27/r28 blocking review evidence recorded; PENDING final no-MAJOR round after the r28 patches; historical r16-r26 artifacts remain public-history evidence only

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
- The split implementation work has moved into [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) still needs a fresh no-MAJOR umbrella-plan review after the split closeouts.
- Gemini review remains unavailable in current noninteractive runs because the installed CLI reports an unsupported-client tier failure; the provider must be restored/migrated or the user must explicitly authorize a one-round degraded quorum after seeing that evidence.
- Pre-existing untracked [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) r1-r15 review artifacts were local residue, not public-history evidence. They were quarantined outside the repo before this r27 closeout so `scripts/legal/legal-sanity-scan.sh --diff-only` can pass and sweep commits cannot accidentally publish them.

### Evidence

**Issue status** (verified 2026-07-02):

```text
#51 OPEN ACE wave 0: corpus ledger, routing firewall, and sampling protocol labels=strengthening,lane:claude,priority:high
```

**Split issue closeout evidence consumed by this umbrella plan** (verified 2026-07-02):

- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) closed with ledger schema and route-store matrix artifacts.
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) closed with public-token fixture and private-field placeholder artifacts.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) closed with bounded sampling firewall artifacts.
- [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) closed with public-surface self-scan artifacts.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) closed with repo-local legal/security scan artifacts.

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
| Local-only quarantined review residue | Pre-existing untracked [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) r1-r15 artifacts moved outside the repo; not cited as plan-review evidence and not eligible for public commit |
| Split issue plans and closeouts | GitHub issues [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69), their plan files, implementation artifacts, and implementation-review artifacts |
| Blocking #51 review artifacts | `scripts/review/results/2026-07-02-plan-51-*-r27.md` and `scripts/review/results/2026-07-02-plan-51-*-r28.md` |
| Future final #51 review artifacts | `scripts/review/results/2026-07-02-plan-51-*-r29.md` or later |

---

## Deliverable

[#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will deliver a wave-0 umbrella contract and dependency map. It will not implement the script modules, fixtures, legal scanner, public-surface scanner, sampling firewall, or durable stores directly.

The implementation work has been separated from this umbrella and will remain owned issue-by-issue:

| Issue | Owner scope | Lane | Status |
|---|---|---|---|
| [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) | Ledger schema, closed route enum, route-to-logical-store matrix, verification state, and structural registry validation | lane:claude | closed; implementation evidence recorded on issue |
| [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) | Fixture-only public-token contract and private-field placeholder grammar | lane:codex | closed; implementation evidence recorded on issue |
| [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) | Bounded sampling firewall and executable-context checks | lane:codex | closed; implementation evidence recorded on issue |
| [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) | Public-surface self-scan over control-plane artifacts and review artifacts; [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) currently uses the generic `--scan-public-path` mode while selector/snapshot generalization is tracked by [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) | lane:claude | closed; implementation evidence recorded on issue |
| [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) | Repo-local legal/security scan wrapper and self-scan-safe deny-list config | lane:claude | closed; implementation evidence recorded on issue |

### Scope Decision

The split branch will remain authoritative. [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will remain the umbrella dependency and review surface; [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will carry their own implementation evidence.

This plan will not request implementation approval for any child slice. A future user approval on [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will authorize only the umbrella coordination artifact unless the approval explicitly names a split child issue and its reviewed plan.

### Dependency Rules

- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) will define the schema fields and route/store vocabulary consumed by the other split issues.
- [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) will own placeholder fields and token grammar that depend on the ledger schema.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) will own bounded sampling controls that depend on the schema and manifest evidence contract.
- [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) will own the public-surface self-scan over control-plane artifacts through generic `--scan-public-path` checks for [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51); generalized selector/snapshot modes are follow-on [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72), not a [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) precondition.
- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will own the repo-local legal/security scan gate.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61), [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62), and [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) remain cross-wave gates and do not become implementation children of [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51).

---

## Pseudocode

```text
read #51, #50, #61, #62, #63, and split issues #65-#69
verify split issues #65-#69 have issue-local closeout comments and remain separate from #51 approval
record split registry in this plan, README, and coordination artifact
keep #51 implementation-ready=false until user approval exists for a reviewed #51 umbrella plan
for downstream wave plans:
  consume #65 route/schema vocabulary, #66 token contract, #67 sampling firewall, #68 generic public-surface scan, #69 legal scan, and #62 manifest evidence
  keep public surfaces under ACE_SHARE_ROOT abstraction
  avoid private corpus content, raw host paths, exact private inventory counts, and client identifiers
do not create #51 implementation scripts or tests from this umbrella plan
```

---

## Files to Change

| Action | Path or issue | Reason |
|---|---|---|
| Modify | `docs/plans/2026-06-29-issue-51-ace-wave-0-corpus-ledger-routing-firewall-sampling-protocol.md` | Refresh the umbrella plan after split issue closeouts |
| Modify | `docs/plans/README.md` | Record that [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains draft while [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) carry closed implementation evidence |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Refresh the wave-0 split registry without marking [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) implementation-ready |
| Edit | [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) issue body | Reconcile the live issue text so it points to the umbrella/split-closeout state instead of re-advertising one bundled implementation |
| Local cleanup | Untracked [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) r1-r15 review artifacts | Preserve unsafe local residue outside the repo and keep `scripts/legal/legal-sanity-scan.sh --diff-only` green |
| Comment | [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) | Record r27 review evidence and next gate |
| Comment | [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) | Record parent-level coordination status without editing the parent issue body |

No implementation files will be created by this [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) umbrella revision.

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_parent_coordination_validator_still_passes` | The existing ACE coordination validator remains green after adding the split registry | `docs/plans/ace-share-ingestion-wave-coordination.md` | Validator passes with canonical #51-#63 registry intact |
| `test_plan_index_records_split_closeouts_without_umbrella_approval` | The plan index records split closeout state without implying [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) readiness | `docs/plans/README.md` | [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains draft and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) remain separate closed implementation units |
| `test_split_issue_closeouts_are_separate_from_51_status` | Split issue closeouts do not grant [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) approval | Live issue snapshots for [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) | [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) has no `status:*` label; split issues have independent closeout evidence |
| `test_public_scan_accepts_split_artifacts` | Split docs and fetched issue/comment bodies remain public-safe under the implemented #68 and #69 gates | Plans, README, coordination doc, review artifacts, temporary fetched issue/comment bodies, and diff-only untracked candidates | `scripts/validate_ace_public_surface_scan.py --scan-public-path`, `scripts/legal/legal-sanity-scan.sh`, and `scripts/legal/legal-sanity-scan.sh --diff-only` pass without raw host paths, private corpus values, personal identifiers, unsafe source-provenance values, or untracked public-surface candidates; selector/snapshot hardening is deferred to [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) |

---

## Acceptance Criteria

- [ ] [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) remain separate implementation units with their own plan, approval, implementation, review, and closeout evidence.
- [ ] [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) no longer claims that one broad implementation will create token, sampling, public-scan, legal-scan, and validator modules in a single approval unit.
- [ ] `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` record the split registry while preserving the canonical #51-#63 child wave ledger for the approved parent epic.
- [ ] Split issue closeouts do not make [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) implementation-ready.
- [ ] Public surfaces use the `ACE_SHARE_ROOT` abstraction and do not publish private source content, raw host paths, exact private inventory counts, client identifiers, or personal identifiers.
- [ ] Verification commands pass before commit/comment: parent coordination validator, relevant unit tests, `scripts/validate_ace_public_surface_scan.py` over edited public artifacts, `scripts/legal/legal-sanity-scan.sh` over edited public artifacts, and `git diff --check`.
- [ ] New review artifacts are scanned and committed or quarantined before `scripts/legal/legal-sanity-scan.sh --diff-only`; the diff-only gate passes before commit/comment so local untracked review residue cannot be swept into a public commit.
- [ ] The live [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) issue body is reconciled to the umbrella/split-closeout state and no longer presents [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) work as a future bundled implementation.
- [ ] No `status:plan-review` transition is attempted for [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) until a fresh adversarial review of the split rewrite returns no active-provider MAJORs and Gemini is restored/migrated or a user-authorized degraded quorum is explicitly recorded.

---

## Pre-Label Evidence Checklist

These checks must be satisfied before [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) can move to `status:plan-review`:

- Live issue snapshots for [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) and [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will be fetched and scanned.
- `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` will match the split scope.
- The final no-MAJOR review round will run against a committed tree and will cite reviewed commit SHA, tree SHA, and plan blob SHA.
- The implemented #68 public-surface scanner generic `--scan-public-path` mode and #69 legal/security scanner will both pass over the edited public artifacts and review artifacts; [#72](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/72) owns broader selector/snapshot generalization.
- The #69 `--diff-only` legal scan will pass after pre-existing untracked [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) r1-r15 review residue is quarantined outside the repo and each new review-artifact round is committed or quarantined.
- Gemini availability will be restored/migrated, or the user will explicitly authorize one degraded-quorum round after the unsupported-client failure is disclosed.
- Implementation will remain stopped after `status:plan-review`; user approval will still be required.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r26 | MAJOR | Required explicit split-vs-bundled scope decision, machine-parseable self-scan anchors, Gemini restoration or waiver, fresh no-MAJOR evidence, and less compound acceptance criteria. |
| Codex r26 | MAJOR | Required tracked review artifact normalization, fallback scanner hardening for local path leaks, fresh no-MAJOR evidence, and explicit split-vs-bundled scope decision. |
| Gemini r26 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| r27 split-closeout refresh | MAJOR/MINOR/UNAVAILABLE | Found untracked r1-r15 residue, missing explicit #69 legal gate, stale #65 legal-scan state, stale #51 ledger/body state, and Gemini unsupported-client unavailability. |
| r28 focused re-review | MAJOR/MINOR/UNAVAILABLE | Found untracked r27 artifacts before they were committed, #68 selector/snapshot overclaim, stale r27 bookkeeping, final-round identity ambiguity, and Gemini failure-class wording. |
| r29 final focused re-review | PENDING | Required before any status transition. |

**Overall result:** This plan remains draft-only. The refreshed plan keeps [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) as an umbrella coordination plan. No implementation or approval label will be applied by this plan revision.

---

## Risks and Open Questions

- **Risk:** The split registry can drift from issue bodies; pre-label review must refetch live issue metadata before any status transition.
- **Risk:** Review fatigue from r1-r28 can hide fresh defects; final review must treat the rewritten plan as a new artifact, not a patched version to rubber-stamp.
- **Risk:** Gemini remains unavailable due an unsupported-client tier failure; the plan cannot enter `status:plan-review` unless Gemini is restored/migrated or the user explicitly authorizes a degraded-quorum round.
- **Open:** The next concrete planning target after [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) review should be the cross-wave lifecycle gate [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61), because durable downstream outputs depend on it.

---

## Complexity

**T3** - security-sensitive cross-wave planning and dependency governance, now split into issue-sized implementation plans.
