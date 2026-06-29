# Plan for #62: ACE Cross-Wave Manifest Freshness and Drift Sentinel

> **Status:** draft
> **Complexity:** T2
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-06-29-plan-62-claude.md | scripts/review/results/2026-06-29-plan-62-codex.md | scripts/review/results/2026-06-29-plan-62-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/16-corpus-lifecycle.md` requires stable content identity and trust reset when source content changes.
- `docs/plans/README.md` now requires `ACE_SHARE_ROOT` plus share-relative paths for proposed implementation scripts.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will define bounded sampling and route contracts consumed by this sentinel.

### Related issues
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) owns cross-wave manifest freshness and drift detection.
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the parent epic.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) is the required route/sampling dependency.
- [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) must record manifest snapshot IDs before pilot sampling.

### Source inventory
- Candidate manifests include `assets.json`, `docs/master-index.jsonl`, `_cad-index/index-summary.json`, `_cad-index/cad-readability-index.tsv`, and `.ace-knowledge/index.db` under `ACE_SHARE_ROOT`.
- This issue will read direct file metadata and bounded manifest headers/summaries only; it will not recursively crawl the share.

### Gaps identified
- No reusable manifest snapshot ID exists for downstream waves.
- No drift severity policy exists for comparing broad manifests, master indexes, CAD indexes, and knowledge-store indexes.
- No validator exists to prevent downstream plans from mixing incompatible manifest counts without reconciliation.

### Evidence

**Issue status** (verified 2026-06-29):
```
#62 OPEN ACE cross-wave: manifest freshness and drift sentinel labels=strengthening,lane:codex,priority:high
```

**File existence**:
```
EXISTS docs/16-corpus-lifecycle.md
EXISTS docs/plans/README.md
MISSING docs/case-studies/ace-manifest-freshness-drift-sentinel.md
MISSING scripts/validate_ace_manifest_freshness.py
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-62-ace-manifest-freshness-and-drift-sentinel.md |
| Sentinel case study | docs/case-studies/ace-manifest-freshness-drift-sentinel.md |
| Validator | scripts/validate_ace_manifest_freshness.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-62-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-62-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-62-gemini.md |

---

## Deliverable

A reusable ACE manifest freshness and drift sentinel that records snapshot IDs, checks bounded freshness evidence, classifies drift severity, and gives downstream waves a stable manifest reference without hardcoded host paths.

---

## Pseudocode

```text
require #51 route/sampling contract
read ACE_SHARE_ROOT from environment
for each configured manifest candidate:
  stat direct path only
  compute sha256, size, mtime, optional generated timestamp, row count, schema marker
  record snapshot_id from path key + sha256 + row count + generated timestamp
compare broad manifest, master index, CAD index, and knowledge-store index:
  classify drift as compatible, warning, blocker, or unavailable
reject commands/config that use hardcoded mount paths or recursive crawls
emit public-safe manifest snapshot report using share-relative keys and hashes only
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-manifest-freshness-drift-sentinel.md | Public-safe manifest freshness/drift contract |
| Create | scripts/validate_ace_manifest_freshness.py | Executable snapshot/drift validator |
| Modify | .github/workflows/validate.yml | Run the manifest validator with synthetic fixtures |
| Modify | docs/16-corpus-lifecycle.md | Cross-link source snapshot identity and trust reset |
| Modify | skills/format-coverage-ledger/SKILL.md | Require manifest snapshot ID in wave ledgers |
| Modify | skills/source-extraction-coverage/evals/evals.json | Add snapshot/drift eval data |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_manifest_snapshot_id_has_required_fields | Snapshot identity | Synthetic manifest files | path key, sha256, size, row count, generated timestamp/status |
| test_ace_share_root_required | Host portability | Validator config | Uses `ACE_SHARE_ROOT` and share-relative paths |
| test_no_recursive_crawl_patterns | Bounded freshness | Validator config/scripts | Rejects recursive crawl/full-manifest commands |
| test_drift_severity_closed_set | Drift classification | Compatible/warning/blocker examples | Closed severity enum only |
| test_incompatible_counts_require_reconciliation | Mixed manifests | Broad and CAD snapshots with mismatch | Blocker unless reconciliation note exists |
| test_public_report_has_no_raw_paths | Public artifact safety | Snapshot report | Source tokens/hashes only; no host paths |

---

## Acceptance Criteria

- [ ] Snapshot IDs exist for configured manifests using share-relative keys, SHA-256, size, row count, timestamp/status, and schema marker where available.
- [ ] Freshness checks use direct file metadata and bounded probes only; no recursive share crawl or full-manifest materialization.
- [ ] Drift is classified as compatible, warning, blocker, or unavailable.
- [ ] Downstream waves can cite manifest snapshot IDs instead of raw host paths.
- [ ] Incompatible manifest counts block downstream sampling unless a reconciliation note is present.
- [ ] Public snapshot reports contain only source tokens/hashes and aggregate counts.
- [ ] `uv run python scripts/validate_ace_manifest_freshness.py` and `uv run skills/validate_skill.py` pass.

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

- **Risk:** Large manifest hashing can be expensive; implementation should cache snapshot results and bound runtime.
- **Risk:** Some source manifests may be unavailable on a machine; validator must distinguish unavailable from stale or incompatible.
- **Open:** [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) must define which downstream waves require fresh snapshot IDs before sampling.

---

## Complexity

**T2** - cross-wave validator and governance doc with bounded file metadata checks, but no content ingestion.
