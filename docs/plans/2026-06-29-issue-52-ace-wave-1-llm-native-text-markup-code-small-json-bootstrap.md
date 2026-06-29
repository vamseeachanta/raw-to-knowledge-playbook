# Plan for #52: ACE Wave 1 LLM-Native Text, Markup, Code, and Small JSON Bootstrap

> **Status:** draft
> **Complexity:** T2
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-06-29-plan-52-claude.md | scripts/review/results/2026-06-29-plan-52-codex.md | scripts/review/results/2026-06-29-plan-52-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/01-document-taxonomy.md` requires content-first classification and extraction-depth choice by type.
- `docs/10-structured-data-and-model-files.md` treats structured files as silently fragile and requires convention/provenance sidecars.
- `skills/content-triage-and-exclusion/SKILL.md`, `skills/source-extraction-coverage/SKILL.md`, and `skills/source-extract-fidelity/SKILL.md` define triage-before-extract, estimate/yield, and fidelity review.

### Related issues
- [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52) targets text/markup/code/small JSON and must avoid generated JSON plus low-value source trees.
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) requires method/skill binding and per-issue review/approval.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) is the required upstream ledger/routing contract.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable stores, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- Prior manifest rollup showed text/markup about 1.48M files / 6.4 GB after classifying engineering `.rst` as simulation, not prose.
- Code/scripts are about 43.8k files / 0.36 GB.
- About 1.43M `.json` files are tiny and likely generated, so `.json` must not imply useful content.
- Expected routed success target: at least 70% for eligible hand-authored text/markup/config candidates in the bounded pilot; generated/noise exclusions are reported separately as `% excluded`.

### Gaps identified
- No deterministic generated/repetitive JSON rule exists in the playbook.
- No ACE text/config pilot report exists.
- No helper self-test exists for text/JSON/source-tree triage.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#52 OPEN ACE wave 1: LLM-native text, markup, code, and small JSON bootstrap labels=strengthening,lane:codex,priority:high
```

**File existence**:
```
EXISTS docs/01-document-taxonomy.md
EXISTS docs/10-structured-data-and-model-files.md
EXISTS skills/content-triage-and-exclusion/SKILL.md
EXISTS skills/source-extraction-coverage/SKILL.md
MISSING docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md
MISSING skills/content-triage-and-exclusion/resources/text_json_triage.py
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-52-ace-wave-1-llm-native-text-markup-code-small-json-bootstrap.md |
| Pilot report | docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md |
| Triage helper | skills/content-triage-and-exclusion/resources/text_json_triage.py |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-52-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-52-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-52-gemini.md |

---

## Deliverable

A bounded ACE wave-1 pilot that classifies text/markup/code/JSON into the closed route targets from [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51), proves generated JSON detection by schema/content, reports `% ingested success`, and updates reusable playbook rules.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
select bounded stratified sample for text, markup, code, json:
  max 25 rows per bucket, deterministic seed/sort, max 250 files or 100 MB touched
for each candidate row:
  hash source and detect content type
  apply fail-closed exclusion before value ranking
  parse shape and score generated/repetitive JSON or low-value source tree
  decide route_target: public_llm_wiki, private_sidecar, metadata_only, excluded_no_ingest
  when kept, record extraction_estimate and extraction_yield
  block public target unless route has affirmative clearance and #61 is approved
write pilot report with counts, public-safe examples, success numerator/denominator, rules, and method gaps
update docs and skills with reusable JSON/config/text filtering rules
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md | Pilot evidence and reusable text/JSON/source-tree rules |
| Create | skills/content-triage-and-exclusion/resources/text_json_triage.py | Deterministic classifier/self-test helper |
| Create | scripts/validate_ace_wave1_text_json.py | Executable validator for sample caps, route enum, success metric, and public artifact safety |
| Modify | skills/content-triage-and-exclusion/SKILL.md | Add generated/repetitive JSON and source-tree triage rules |
| Modify | skills/source-extraction-coverage/SKILL.md | Add text/markup/code/JSON estimate-yield recipes |
| Modify | skills/source-extract-fidelity/SKILL.md | Add text/config/code traceability checks |
| Modify | docs/01-document-taxonomy.md | Clarify LLM-native text/markup/code/config lane |
| Modify | docs/10-structured-data-and-model-files.md | Add small JSON/config metadata handling |
| Modify | .github/workflows/validate.yml | Run `uv run skills/content-triage-and-exclusion/resources/text_json_triage.py self-test` |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_generated_json_detected_by_shape_not_extension | Generated JSON routing is content-based | Manual config JSON and repetitive generated JSON | Config -> metadata-only; generated -> exclude |
| test_exclusions_precede_value_ranking | Security/routing beats usefulness | PII marker in useful doc | Exclude/private route before ranking |
| test_source_tree_not_bulk_ingested | Source trees are not recursively dumped | Dependency/build/generated paths | Metadata-only or exclude |
| test_extract_estimate_and_yield_required | Kept extracts carry coverage fields | Kept text/config row | Estimate and yield present |
| test_route_targets_use_closed_enum | Route vocabulary | Candidate rows | Only `public_llm_wiki`, `private_sidecar`, `metadata_only`, or `excluded_no_ingest` |
| test_public_route_requires_affirmative_clearance | Unknown/private cannot publish | Missing/private visibility | `private_sidecar`, `metadata_only`, or `excluded_no_ingest` |
| test_wave1_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave1_sample_caps_are_enforced | Bounded sampling | Sample manifest | Per-bucket caps, seed/sort, max files, and max bytes present |

---

## Acceptance Criteria

- [ ] Bounded sample classifies every candidate into `public_llm_wiki`, `private_sidecar`, `metadata_only`, or `excluded_no_ingest`.
- [ ] Generated/repetitive JSON is detected by schema/content signals, not `.json` extension alone.
- [ ] Extracted pages or report rows record extraction estimate and yield.
- [ ] `% ingested success` is calculated as successful routed items over eligible candidate items, with generated/noise exclusions reported separately.
- [ ] Public/private routing is checked before any public target path is selected, and no durable output path is selected before [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) approval.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports pass the [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) redaction canary before publication.
- [ ] Reusable JSON/config/text filtering rule lands in docs/skills.
- [ ] `uv run skills/validate_skill.py`, `uv run skills/content-triage-and-exclusion/resources/text_json_triage.py self-test`, and `uv run python scripts/validate_ace_wave1_text_json.py` pass.

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

- **Risk:** This issue depends on #51; implementation must not start before the routing contract exists, and durable publication/storage remains blocked on #61.
- **Risk:** JSON generatedness can be ambiguous; the helper needs sampled false-positive review.
- **Open:** For useful code/scripts, first pilot must decide full private text versus metadata/docstrings only.

---

## Complexity

**T2** - medium docs/skill/resource change with a small harness, but no broad ingestion system.
