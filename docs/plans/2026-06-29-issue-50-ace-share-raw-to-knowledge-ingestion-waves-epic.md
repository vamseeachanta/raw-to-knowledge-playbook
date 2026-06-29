# Plan for #50: ACE Share Raw-to-Knowledge Ingestion Waves Epic

> **Status:** plan-review
> **Complexity:** T2
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-50-claude.md | scripts/review/results/2026-06-29-plan-50-codex.md | scripts/review/results/2026-06-29-plan-50-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/01-document-taxonomy.md` will provide the content-class and extraction-level vocabulary for child waves.
- `docs/07-data-governance.md`, `docs/18-security-and-pii.md`, and `docs/19-trust-boundary-and-private-mode.md` will define the raw-source, private-sidecar, and publication boundaries for every child plan.
- `docs/20-measured-outcomes.md` will provide the measured office/PDF baseline that child waves will compare against when setting expected useful ingestion ranges.
- `docs/21-cad-and-brep-geometry.md` will provide the CAD-specific method baseline for [#57](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/57).
- `skills/README.md` and `skills/*/evals/evals.json` will provide reusable skill groups and eval data; executable TDD coverage will still require validators or canary tests because `skills/validate_skill.py` only validates skill/eval structure.

### Related issues
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the parent epic for all ACE-share ingestion waves.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will define the control-plane ledger, routing firewall, and sampling protocol that downstream waves consume.
- [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) will each implement one progressive format family.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) will define the cross-wave knowledge-store, retrieval, evaluation, and lifecycle contract.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) will define manifest snapshot/freshness/drift gates.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will define public-output redaction and identifier canaries.

### Source inventory
- The epic will treat `INDEX.md`, `assets.json`, `docs/master-index.jsonl`, `_cad-index/`, and `.ace-knowledge/index.db` under `ACE_SHARE_ROOT` as input sources whose private contents must not be copied into public repo artifacts.
- The epic will use only bounded manifest reads and targeted metadata checks through `ACE_SHARE_ROOT`. It will not authorize recursive share crawls.

### Gaps identified
- The child issue set will need a single coordination artifact that records each wave's plan status, formal review status, user-approval state, method issue binding, skill group, and dependency blockers.
- Downstream plans will need a consistent rule for promoting method gaps into playbook docs, skill eval data plus executable validators/canaries, or follow-on issues.
- The issue tree will need a branch/publication rule so planning artifacts are not accidentally mixed into unrelated feature branches.
- The issue tree will need a public-output safety gate covering path tokenization, private identifier denial, and publication readiness before any case study enters the public site.

### Evidence

**Issue status** (verified 2026-06-29):
```
#50 OPEN EPIC: ACE share raw-to-knowledge ingestion waves for llm-wiki labels=epic,strengthening,lane:claude,priority:high
```

**File existence**:
```
EXISTS docs/01-document-taxonomy.md
EXISTS docs/07-data-governance.md
EXISTS docs/18-security-and-pii.md
EXISTS docs/19-trust-boundary-and-private-mode.md
EXISTS docs/20-measured-outcomes.md
EXISTS docs/21-cad-and-brep-geometry.md
EXISTS skills/README.md
MISSING docs/plans/ace-share-ingestion-wave-coordination.md
MISSING scripts/validate_ace_epic_wave_coordination.py
```

**Reproduction proofs**:
N/A - parent epic/planning issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-50-ace-share-raw-to-knowledge-ingestion-waves-epic.md |
| Coordination table | docs/plans/ace-share-ingestion-wave-coordination.md |
| Coordination validator | scripts/validate_ace_epic_wave_coordination.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-50-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-50-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-50-gemini.md |

---

## Deliverable

A repo-local CI-validated epic coordination artifact that will track the ACE child wave plans, dependencies, approval gates, skill-group bindings, method issue bindings, review evidence, and follow-on method-gap disposition rules without authorizing child implementation. CI validation will check recorded snapshots and local approval markers only; live GitHub label checks will remain an explicit pre-label/changeover step captured in issue comments because stock CI will not have interactive `gh` auth.

---

## Pseudocode

```text
load epic #50 and child issues #51-#63
for each child issue:
  record plan path, local status, latest recorded live-status snapshot,
  snapshot timestamp, lane label, complexity
  record prerequisite issues and blocked-by dependencies
  record raw-to-knowledge method issue anchors
  record skill groups, eval data, and executable validator/canary files
  record expected useful ingestion range, measured success formula,
  measured-vs-expected status, and difficulty rank
  record whether formal Claude/Codex/Gemini plan-review artifacts exist
  record whether .planning/plan-approved/<issue>.md exists with approved-by/date/plan/sha/review fields
  record child-gate evidence as command, timestamp, exit code, artifact path,
  and reviewed commit; do not run child validators from the coordination validator
assert implementation_ready=false unless:
  latest recorded live-status snapshot shows status:plan-approved
  matching child approval marker exists
  missing .planning/plan-approved/ is treated as all children unapproved
  parent coordination table shows no unresolved prerequisite blocker
  #61 has status:plan-approved, approval marker, implemented validators,
    and recorded passing validation evidence before any durable store,
    public/private target path, retrieval metadata, or publication write
  #62 has status:plan-approved, approval marker, implemented freshness validator,
    recorded passing validation evidence, and cited snapshot_id before any
    downstream wave samples a manifest-backed source family
  #63 has status:plan-approved, approval marker, implemented public-output canary,
    and recorded passing validation evidence before any docs nav, mkdocs,
    llm-wiki, or other public publication
require every method gap to land as:
  playbook doc update, skill/eval update, or follow-on GitHub issue
require public artifact safety gate before publication exposure:
  no raw absolute source paths, no private identifiers, source_id/source_sha256 tokens only
require branch publication rule:
  dedicated planning branch or explicit stacked-branch note; no accidental mix with unrelated feature branches
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/plans/ace-share-ingestion-wave-coordination.md | Durable coordination table for child issues [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51)-[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) |
| Create | scripts/validate_ace_epic_wave_coordination.py | CI-checkable validation for repo-local snapshots, dependencies, issue links, skill groups, executable test bindings, method issue bindings, review/approval gates, and branch/publication rule |
| Modify | .github/workflows/validate.yml | Run the coordination validator |
| Deferred | docs/index.md | Do not link the coordination table until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result |
| Deferred | mkdocs.yml | Do not publish the coordination table in site navigation until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result |
| Modify | skills/adversarial-verify-loop/SKILL.md | Require child-wave method-gap disposition during closeout |
| Modify | skills/format-coverage-ledger/SKILL.md | Add epic-level wave status and expected-yield fields |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_epic_coordination_lists_all_children | Child issue coverage | Coordination table | [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51)-[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) all present |
| test_each_child_has_method_issue_binding | Raw-to-knowledge method traceability | Coordination table rows | Every child row lists at least one method issue anchor |
| test_each_child_has_skill_group_and_executable_test_binding | Skill-group/test traceability | Coordination table rows | Every child row lists skill groups plus validator/canary/eval files |
| test_review_artifact_status_recorded_per_child | Review traceability | Coordination table rows | Every child row records Claude/Codex/Gemini review artifact paths or explicit provider unavailability |
| test_status_gate_records_unapproved_children | Approval gate | Child row without `.planning/plan-approved/<issue>.md` or with missing marker directory | `implementation_ready=false` is recorded without crashing |
| test_dependencies_include_wave0_and_lifecycle_contract | Dependency correctness | Child dependency rows | Downstream waves depend on [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51), and durable output/retrieval/publication work also depends on [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) approval plus validators |
| test_method_gap_disposition_is_closed_set | Closeout governance | Method-gap rule | Gap disposition is doc update, skill/eval update, or follow-on issue |
| test_public_artifact_safety_gate_required | Public repo safety | Coordination table publication rows | Requires deny-list/path-tokenization gate before docs nav/mkdocs/llm-wiki publication |
| test_branch_publication_rule_present | Branch hygiene | Coordination rules | Requires dedicated planning branch or explicit stacked-branch publication note |
| test_ingested_success_metric_is_defined | Measurement contract | Child rows | Expected range is present for draft rows; measured numerator, denominator, threshold, and command are required only for approved/implemented rows |
| test_manifest_snapshot_gate_bound_per_row | Freshness gate | Manifest-backed child rows | Each row that samples manifest-backed source families depends on [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) approval, marker, implemented validator, recorded passing-command result, and snapshot_id |
| test_public_redaction_canary_gate_bound_per_row | Publication safety gate | Public-output child rows | Each row that publishes docs, mkdocs, llm-wiki, or comments depends on [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) approval, marker, implemented canary, and recorded passing-command result |
| test_bounded_share_reads_are_declared | ACE source safety | Source inventory section and validator config | `ACE_SHARE_ROOT`, named manifest source, seed/sort rule, row caps, max files/bytes, and denied traversal patterns are present |
| test_unbounded_manifest_traversal_is_denied | ACE source safety | Bad command/config fixtures | Recursive share walk, full-manifest materialization, full-file hashing/counting of large manifests, unrestricted `jq`, `os.walk`, `ls -R`, `find`, `du`, `rg`, and `fd` patterns fail validation |

---

## Acceptance Criteria

- [ ] Coordination artifact lists [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51)-[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) with plan file, lane, complexity, status, dependency, method issue, skill group, expected useful ingestion range, measured success formula, and difficulty rank where applicable.
- [ ] No child issue is represented as implementation-ready unless the coordination table records a fresh live-status snapshot showing `status:plan-approved`, `.planning/plan-approved/<issue>.md` exists, and missing `.planning/plan-approved/` is handled as all children unapproved.
- [ ] Every child row names the raw-to-knowledge method issue(s), skill group(s), eval data, and executable validator/canary files that implementation will use and update.
- [ ] Every child row records whether formal plan review artifacts exist for Claude, Codex, and Gemini, or records explicit provider unavailability.
- [ ] Method gaps found during child waves must update a playbook doc/skill/eval or create a follow-on GitHub issue before child closeout.
- [ ] Public artifact safety gate blocks raw source paths, private identifiers, personal identifiers, and proprietary snippets before any docs nav, `mkdocs.yml`, `llm-wiki`, or external publication exposure.
- [ ] Branch/publication rule prevents these plan artifacts from landing accidentally on unrelated feature branches.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is represented as `status:plan-approved` snapshot plus approval marker plus implemented validator plus recorded passing-command result before any child wave writes durable stores, target paths, retrieval metadata, or published summaries.
- [ ] [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) is represented per manifest-backed row as `status:plan-approved` snapshot plus approval marker plus implemented validator plus recorded passing-command result plus cited `snapshot_id` before any downstream child wave samples manifest-backed source families.
- [ ] [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is represented per publication row as `status:plan-approved` snapshot plus approval marker plus implemented canary plus recorded passing-command result before any child wave publishes public artifacts.
- [ ] Coordination validation denies recursive ACE share walks, full-manifest materialization, and full-file hashing/counting of large manifests unless a later approved issue explicitly authorizes them or a bounded precomputed sidecar is cited.
- [ ] `uv run python scripts/validate_ace_epic_wave_coordination.py` passes.
- [ ] `uv run skills/validate_skill.py` passes after skill updates.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | MAJOR | CI cannot enforce live GitHub status; TDD under-covers per-wave #62/#63 dependency binding; wording overstates "block" enforcement. |
| Codex r1 | MAJOR | Gate dependency cycle across #51/#63; #62/#63 represented as listed gates rather than implemented/approved gates; publication and bounded-read tests under-specified. |
| Gemini r1 | UNAVAILABLE | `gemini -p` failed with auth exit 41; no non-interactive Gemini credentials were available in this session. |
| Claude r2 | MINOR | R1 blockers resolved; residual acceptance/TDD consistency and recorded-evidence wording required. |
| Codex r2 | MAJOR | #62 still allowed unbounded full-manifest hash/count; downstream publication plans still lacked the full #63 approval-marker-canary-command gate. |
| Claude r3 | MINOR | R2 MAJOR objectives resolved; residual #50/#51 deferred wording and #62 cap/no-sidecar behavior required tightening. |
| Codex r3 | APPROVE | No findings in focused diff review of `614e33f..2be9f80`. |
| Claude r4 | MINOR | No MAJOR; stale #50 risk wording and optional deferral-row hardening remained. |
| Codex r4 | MINOR | No MAJOR; #50/#51 deferral rows and #50 risk prose needed literal four-part #63 gate wording. |

**Overall result:** NO MAJOR - ready for `status:plan-review` after evidence comment and live GitHub label update. R4 MINOR wording findings were patched in this plan revision; implementation remains blocked pending user approval.

---

## Risks and Open Questions

- **Risk:** The coordination artifact can drift from live GitHub labels; this plan will keep CI limited to repo-local snapshot fields and require a fresh `gh issue view` evidence comment before any label transition.
- **Risk:** Planning artifacts currently live on `docs/ace-ingestion-wave-plans`, a dedicated planning branch stacked on `docs/cad-brep-geometry-lane`; publication exposure should wait until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result.
- **Open:** [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) must name the private sidecar location before child waves rely on it for output routing.
- **Open:** [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must define retrieval/evaluation gates before bulk ingestion expands beyond pilot size.

---

## Complexity

**T2** - coordination/governance plan and validator across a multi-issue tree, but no content ingestion and no production pipeline change.
