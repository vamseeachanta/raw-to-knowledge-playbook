# Plan for #54: ACE Wave 3 PDF, Word, Standards, Reports, and Scanned Document Lane

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/54
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-54-claude.md | scripts/review/results/2026-06-29-plan-54-codex.md | scripts/review/results/2026-06-29-plan-54-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/01-document-taxonomy.md` says standards target L4-L5, reports L1-L4, forms/templates reject at L3, and scanned docs are L0 or `ocr-interpreted`.
- `docs/03-verification-playbook.md` and `skills/verify-batch/SKILL.md` require table rows to start `provisional-unverified` and become trusted only after verification.
- `docs/09-office-formats.md` and `docs/11-imagery-and-scans.md` cover DOCX tables, tracked-change decisions, and OCR-as-interpretation.

### Related issues
- [#54](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/54) covers documents: 294k files / 332.9 GB.
- [#2](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/2), [#3](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/3), [#7](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/7), [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12), and [#33](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/33) are method anchors.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) must provide the route/ledger contract.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable document pages, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- PDFs alone: about 253k files / 284.5 GB.
- `ACE_SHARE_ROOT/O&G-Standards/` is a 43 GB standards library.
- Expected useful ingestion: 60-85%, depending on OCR and routing restrictions; pilot threshold is at least 60% routed success for eligible document candidates.

### Gaps identified
- No ACE document-lane pilot exists.
- No ACE test fixtures enforce OCR trust labels or document sample bucket coverage.
- No current flow records how restricted standards text routes public/private.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#54 OPEN ACE wave 3: PDF, Word, standards, reports, and scanned document lane labels=strengthening,lane:claude,priority:high
```

**File existence**:
```
EXISTS docs/01-document-taxonomy.md
EXISTS docs/03-verification-playbook.md
EXISTS docs/09-office-formats.md
EXISTS docs/11-imagery-and-scans.md
EXISTS skills/verify-batch/evals/evals.json
MISSING docs/case-studies/ace-wave-3-document-lane-pilot.md
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-54-pdf-word-standards-reports-scans.md |
| Pilot report | docs/case-studies/ace-wave-3-document-lane-pilot.md |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-54-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-54-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-54-gemini.md |

---

## Deliverable

A sensitivity-first wave-3 pilot that classifies a bounded ACE document sample, routes each source, extracts by document type, records estimate/yield/source hash/trust state, and verifies table candidates without leaking raw or restricted content.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
select bounded sample:
  12 standards pdfs, 12 born-digital report pdfs, 10 docx reports/specs,
  10 scanned/image-only pdfs, 6 forms/templates, 6 low-value brochures
for each candidate row:
  probe content, hash off-repo source, route fail-closed
  if excluded: record reason and stop
  declare extraction_estimate before extraction
  extract with pdf, docx, or scanned/OCR recipe
  record extraction_yield, source_id/source_sha256/public_source_token, lifecycle state
  if tables found:
    enqueue provisional rows and run structural triage
verify top data-dense table batch
run source-extract-fidelity and public-private-routing gates
publish public-safe aggregate pilot report only after route and public-artifact safety gates pass
compute routed success numerator/denominator for eligible candidate rows
update docs/skills or file follow-on issue
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-wave-3-document-lane-pilot.md | Abstracted pilot report after approval |
| Create | scripts/validate_ace_wave3_document_lane.py | Executable validator for sample buckets, route enum, trust labels, success metric, and public artifact safety |
| Modify | skills/source-extraction-coverage/evals/evals.json | Test estimate/yield/hash/trust requirements |
| Modify | skills/format-coverage-ledger/evals/evals.json | Test PDF/DOCX/scanned known-loss ledger behavior |
| Modify | skills/verify-batch/evals/evals.json | Test provisional table state and closed verification statuses |
| Modify | skills/public-private-routing/evals/evals.json | Test fail-closed document routing |
| Modify | skills/page-shape-contract/evals/evals.json | Test provenance/trust page shape |
| Modify | docs/01-document-taxonomy.md | Patch document-lane guidance from pilot evidence |
| Modify | docs/03-verification-playbook.md | Patch verification guidance from pilot evidence |
| Modify | docs/09-office-formats.md | Patch DOCX-specific guidance from pilot evidence |
| Modify | docs/11-imagery-and-scans.md | Patch OCR/scanned guidance from pilot evidence |
| Modify | docs/18-security-and-pii.md | Patch egress/routing guidance if vision verification gap appears |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_wave3_sample_has_required_buckets | Sample coverage | 56-row candidate manifest | Required buckets present |
| test_wave3_estimate_yield_hash_trust_required | Mandatory extraction metadata | Landing page missing a field | Validation fails |
| test_wave3_ocr_never_raw_extracted | OCR label discipline | Scanned PDF marked raw-extracted | Fails; `ocr-interpreted` passes |
| test_wave3_tables_start_provisional | Tables not trusted on parse | Extracted table without verification | Remains provisional |
| test_wave3_fail_closed_routing | Private/unknown cannot publish | Missing/private visibility | Public output blocked |
| test_wave3_known_losses_are_ledgered | Lossy layers explicit | DOCX/images/scanned table | Losses recorded |
| test_wave3_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave3_public_artifact_has_no_raw_paths | Public safety | Pilot report | Uses source tokens/hashes, not raw source paths or private identifiers |

---

## Acceptance Criteria

- [ ] Wave 0 ledger/routing dependency is satisfied before implementation starts.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved before durable document pages, target paths, retrieval metadata, or publication writes.
- [ ] Bounded sample separates born-digital PDFs, scanned PDFs, Word reports/specs, standards, forms/templates, and low-value brochures.
- [ ] Every extracted document records extraction estimate, extraction yield, source ID, source SHA-256, public source token, and lifecycle state.
- [ ] Tables enter provisional state and only become trusted after verification.
- [ ] OCR output is labeled `ocr-interpreted`, never deterministic raw text.
- [ ] Public/private routing blocks client identifiers, personal records, and restricted standards text from public `llm-wiki`.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports require [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) `status:plan-approved`, local approval marker, implemented redaction canary, and recorded passing-command result before docs, comments, `llm-wiki`, or external publication.
- [ ] `% ingested success` is calculated as successful routed items over eligible candidate items, with excluded/no-ingest rows reported separately.
- [ ] New method gaps produce a governing doc/skill patch or a follow-on issue before closeout.
- [ ] `uv run python scripts/validate_ace_wave3_document_lane.py` and `uv run skills/validate_skill.py` pass.

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

- **Risk:** Hosted vision verification can leak sensitive pages unless egress routing is fail-closed.
- **Risk:** Scanned tables may have high reject/deferred rates; manual digitization may be cheaper than OCR repair.
- **Open:** Exact private sidecar and public `llm-wiki` output paths must come from #51/#61.

---

## Complexity

**T3** - multi-format ingestion, routing, OCR interpretation, table verification, and possible governing doc/skill updates.
