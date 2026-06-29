# Plan for #61: ACE Cross-Wave Knowledge-Store, Retrieval, Evaluation, and Lifecycle Contract

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-61-claude.md | scripts/review/results/2026-06-29-plan-61-codex.md | scripts/review/results/2026-06-29-plan-61-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/14-chunking-and-embedding.md` requires structure-aware chunks that preserve trust/provenance and do not slice tables.
- `docs/15-retrieval-evaluation.md` requires golden sets, citation grounding, metric stack, and judge meta-eval.
- `docs/16-corpus-lifecycle.md` uses content hashes, two-level identity, supersede-by-append, and trust reset on source change.

### Related issues
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) owns cross-wave storage/retrieval/eval/lifecycle.
- [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) evaluates knowledge-store data formats.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) is the upstream control-plane dependency.

### Source inventory
- Existing source-of-truth candidates include `assets.json`, `docs/master-index.jsonl`, `_cad-index/`, `.ace-knowledge/index.db`, and `llm-wiki/docs/` under `ACE_SHARE_ROOT`.
- This issue is not a content-ingestion wave; it defines the storage and trust contract for all waves.

### Gaps identified
- No ACE extract-class storage contract exists.
- No ACE lifecycle state machine exists for `candidate`, `provisional`, `verified`, `rejected`, `superseded`, and `stale_requires_rescreen`.
- No ACE retrieval/eval gate exists before bulk ingestion.
- No confidentiality re-screen node exists when source content, route target, or public/private boundary changes.
- No cross-wave `% ingested success` metric contract exists for comparing expected useful ingestion against actual routed, verified, public-safe outcomes.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#61 OPEN ACE cross-wave: knowledge-store, retrieval, evaluation, and lifecycle contract labels=strengthening,lane:claude,priority:high
```

**File existence**:
```
EXISTS docs/14-chunking-and-embedding.md
EXISTS docs/15-retrieval-evaluation.md
EXISTS docs/16-corpus-lifecycle.md
EXISTS ${ACE_SHARE_ROOT}/assets.json
EXISTS ${ACE_SHARE_ROOT}/docs/master-index.jsonl
EXISTS ${ACE_SHARE_ROOT}/.ace-knowledge/index.db
MISSING docs/case-studies/ace-share-knowledge-store-contract.md
MISSING scripts/validate_ace_knowledge_store_contract.py
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-61-ace-cross-wave-knowledge-store-retrieval-evaluation-lifecycle-contract.md |
| Contract doc | docs/case-studies/ace-share-knowledge-store-contract.md |
| Validator | scripts/validate_ace_knowledge_store_contract.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-61-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-61-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-61-gemini.md |

---

## Deliverable

A validated ACE cross-wave contract defining storage forms, required metadata, chunk/retrieval rules, evaluation gates, lifecycle states, `% ingested success`, and batch/branch strategy for all ACE-derived knowledge.

---

## Pseudocode

```text
require #51 control plane
define extract classes:
  landing_page, part_file, dataset, table, media_descriptor,
  geometry_metadata, private_sidecar, exclusion_record
for each extract class:
  assign storage form, route target, source_id, source_sha256, private_lookup_key,
  extraction_estimate, extraction_yield, verification_state
define chunk contract:
  citation_id, content_hash, parse_status, visibility, logical_doc_key, edition
define retrieval/eval contract:
  golden set outside ingest path, continuous checks, CI gate, periodic deep eval
define success metric:
  percent_ingested_success = successful_routed_items / eligible_candidate_items * 100
  hard exclusions report separately as percent_excluded
  successful rows require route target, source token/hash, public safety pass,
  shape/fidelity checks, and allowed lifecycle state
define lifecycle states:
  candidate, provisional, verified, rejected, superseded, stale_requires_rescreen
define invalidation:
  source hash change, route target change, or public/private boundary change resets trust
  and triggers confidentiality re-screen
define batch strategy:
  one PR per tick or stacked branches plus shared-file collision controls
validate contract tables and closed sets
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-share-knowledge-store-contract.md | Cross-wave storage/retrieval/eval/lifecycle contract |
| Create | scripts/validate_ace_knowledge_store_contract.py | Contract validator |
| Modify | .github/workflows/validate.yml | Run validator |
| Modify | docs/14-chunking-and-embedding.md | Add ACE chunk contract hooks |
| Modify | docs/15-retrieval-evaluation.md | Add ACE retrieval/eval gates |
| Modify | docs/16-corpus-lifecycle.md | Add ACE lifecycle states and invalidation |
| Modify | docs/07-data-governance.md | Cross-link storage routes to provenance/routing |
| Modify | docs/19-trust-boundary-and-private-mode.md | Cross-link private-mode store behavior |
| Modify | skills/page-shape-contract/evals/evals.json | Metadata/shape evals |
| Modify | skills/source-extraction-coverage/evals/evals.json | Estimate/yield evals |
| Modify | skills/source-extract-fidelity/evals/evals.json | Fidelity evals |
| Modify | skills/verify-batch/evals/evals.json | Verification-state evals |
| Modify | skills/independent-oracle-validation/evals/evals.json | Oracle evals |
| Modify | skills/public-private-routing/evals/evals.json | Routing evals |
| Modify | skills/stacked-batch-prs/evals/evals.json | Batch/branch collision evals |
| Create | scripts/validate_ace_ingested_success_metric.py | Cross-wave validator for numerator/denominator/threshold/reporting contract |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_extract_classes_have_required_contract_fields | Every class has required metadata | Storage contract table | Estimate/yield/verification/hash/path/route present |
| test_chunk_contract_carries_trust_and_citation | Retrieval metadata preserves provenance | Chunk contract | citation_id/content_hash/parse_status/visibility/logical_doc_key/edition |
| test_eval_gate_exists_before_bulk_ingestion | Retrieval/eval precedes scale-up | Eval section | Golden set, continuous checks, CI gate, periodic deep eval |
| test_ingested_success_metric_contract_is_complete | `% ingested success` comparable across waves | Metric section | Numerator, denominator, exclusions, threshold, and validation command defined |
| test_lifecycle_state_machine_is_closed | Lifecycle states closed-set | Lifecycle table | six allowed states only |
| test_route_and_lifecycle_enums_do_not_overlap | Route/lifecycle separation | Contract tables | Route targets from #51 and lifecycle states from #61 are distinct |
| test_source_change_resets_verification | Freshness resets trust | Invalidation rule | Source hash change routes lifecycle to stale_requires_rescreen |
| test_boundary_change_requires_confidentiality_rescreen | Public/private safety | Invalidation rule | Route or visibility change requires confidentiality re-screen before publication |
| test_batch_strategy_prevents_shared_file_collisions | Branch strategy explicit | Batch section | PR/tick or stacked strategy with verification |

---

## Acceptance Criteria

- [ ] Storage contract covers landing pages, part files, datasets, extracted tables, media descriptors, geometry metadata, private sidecars, and exclusion records.
- [ ] Every extract class records extraction estimate, extraction yield, verification state, source ID, source SHA-256, private lookup key, and route target.
- [ ] Retrieval/evaluation criteria exist before bulk ingestion expands beyond pilot size.
- [ ] `% ingested success` is defined consistently across waves as successful routed items over eligible candidate items, with hard exclusions reported separately.
- [ ] Lifecycle states include `candidate`, `provisional`, `verified`, `rejected`, `superseded`, and `stale_requires_rescreen`, and do not duplicate route targets.
- [ ] Source hash, route target, visibility, or public/private boundary changes require confidentiality re-screen before publication.
- [ ] Chunk metadata carries trust, visibility, edition, citation, and content hash.
- [ ] Batch/branch strategy prevents shared-file collisions and supports progressive waves.
- [ ] `uv run python scripts/validate_ace_knowledge_store_contract.py`, `uv run python scripts/validate_ace_ingested_success_metric.py`, and `uv run skills/validate_skill.py` pass.

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

- **Risk:** This should not implement before #51 is accepted.
- **Risk:** Storage choices from #12 may change the final persistence format.
- **Risk:** Golden Q/A must stay outside ingest path and chunk store to avoid eval leakage.
- **Open:** The exact private-sidecar backing store remains pending; until it is named, child waves may classify and sample but must not write durable private outputs.

---

## Complexity

**T3** - systemic cross-wave contract touching storage, retrieval, evaluation, lifecycle, governance, skills, and CI validation.
