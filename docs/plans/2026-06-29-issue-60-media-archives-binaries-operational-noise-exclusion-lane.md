# Plan for #60: ACE Wave 9 Media, Archives, Binaries, and Operational-Noise Exclusion Lane

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-60-claude.md | scripts/review/results/2026-06-29-plan-60-codex.md | scripts/review/results/2026-06-29-plan-60-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/01-document-taxonomy.md` requires content-first routing and pre-ingest filtering of low-value/admin material.
- `docs/04-failure-modes.md` captures relevant failure classes: misfiled grab-bag, PII leak, third-party confidential, raw-binary firewall, silent completeness gap.
- `skills/archive-extraction-integrity/SKILL.md`, `skills/content-triage-and-exclusion/SKILL.md`, and `skills/format-coverage-ledger/SKILL.md` require list-before-extract, exclusions first, and explicit loss ledgers.

### Related issues
- [#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) covers media, archives, binaries, backups, and operational noise.
- [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) is the storage method anchor.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) supplies route/ledger dependency.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable media/archive records, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- Video: about 5.3k files / 1.11 TB.
- Audio: about 7.2k files / 23.1 GB.
- Archives/containers: about 14k files / 208.6 GB.
- Binaries/build artifacts: about 11k files / 23.3 GB.
- Operational noise: about 27.8k files / 14.3 GB.
- Expected routed success target: at least 90% correct route/exclusion decisions in the bounded pilot; content ingestion is intentionally narrow and reported separately.

### Gaps identified
- No media/archive/noise lane policy exists.
- No high-signal exclusion policy exists for ACE backups, build artifacts, binaries, and shortcuts.
- No media coverage ledger records transcript/OCR/description as partial capture.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#60 OPEN ACE wave 9: media, archives, binaries, and operational-noise exclusion lane labels=strengthening,lane:claude,priority:medium
```

**File existence**:
```
EXISTS docs/04-failure-modes.md
EXISTS docs/07-data-governance.md
EXISTS docs/18-security-and-pii.md
EXISTS skills/archive-extraction-integrity/SKILL.md
EXISTS skills/archive-extraction-integrity/evals/evals.json
MISSING docs/case-studies/ace-wave-9-media-archives-binaries-noise.md
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-60-media-archives-binaries-operational-noise-exclusion-lane.md |
| Pilot report | docs/case-studies/ace-wave-9-media-archives-binaries-noise.md |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-60-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-60-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-60-gemini.md |

---

## Deliverable

A reviewed playbook lane that defaults media, archives, binaries, backups, and operational noise to exclude, while defining the narrow conditions under which selected media is transcribed/OCRed or selected archives are integrity-checked and recursively triaged.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
build wave_9_manifest with bounded caps:
  max 20 rows per bucket, deterministic seed/sort, max 160 files or 500 MB touched
for each bounded manifest row:
  identify actual format from magic/header/container census, not extension/path
  apply hard exclusions first: PII, third-party-confidential, secrets, temp/build/backup noise
  if excluded: record reason and do not extract/copy
  else if archive:
    list manifest only with counts, uncompressed size, encrypted/solid status
    require bounded extraction plan before expansion, including zip-slip and decompression-ratio checks
    extract selected subset off-repo/temp only
    verify CRC/size/hash and record irreducible failures
    route verified children back through triage
  else if audio/video:
    record metadata and value score
    transcribe/OCR/describe only when route and value permit
    ledger transcript/coverage loss as partial
  else if binary/build/noise:
    exclude unless issue-scoped justification exists
run routing and deny-list scan before any derived artifact is promoted
compute routed success numerator/denominator for eligible candidate rows
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-wave-9-media-archives-binaries-noise.md | Pilot/exclusion policy report |
| Create | scripts/validate_ace_wave9_media_archive_noise.py | Executable validator for manifest caps, archive safety, success metric, and public artifact safety |
| Modify | docs/01-document-taxonomy.md | Add archive/media/binary/noise target levels |
| Modify | docs/13-lane-flowcharts.md | Add wave 9 lane branch |
| Modify | docs/04-failure-modes.md | Add/cross-link unsafe archive expansion, backup resurrection, binary leakage, bulk transcription waste |
| Modify | docs/07-data-governance.md | Bind archive/media handling to raw-source firewall |
| Modify | docs/12-tooling-landscape.md | Add license-reviewed archive/media probing tools |
| Modify | docs/18-security-and-pii.md | Clarify media transcription/VLM egress |
| Modify | docs/19-trust-boundary-and-private-mode.md | Clarify private-mode media/archive posture |
| Modify | skills/archive-extraction-integrity/evals/evals.json | Archive integrity evals |
| Modify | skills/content-triage-and-exclusion/evals/evals.json | Noise/exclusion evals |
| Modify | skills/format-coverage-ledger/evals/evals.json | Media partial-coverage evals |
| Modify | skills/public-private-routing/evals/evals.json | Private media route evals |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_excludes_bulk_media_without_value_signal | Media not bulk-transcribed | low-value mp4/wav rows | Excluded or L0 metadata-only |
| test_archive_requires_bounded_integrity_plan | List-first archive rule | zip/rar row with no bound | blocked, manifest-only |
| test_archive_records_crc_failures | Integrity matters | archive CRC mismatch | corrupt/missing list |
| test_archive_blocks_zip_slip | Archive path safety | archive member with `../` or absolute path | Extraction blocked |
| test_archive_blocks_decompression_bomb | Archive expansion safety | archive with excessive ratio/uncompressed size | Extraction blocked |
| test_drops_binary_build_temp_noise | Noise excluded | dll/exe/node_modules/venv/bak | excluded with reason |
| test_private_media_cloud_transcription_blocked | Egress gate | private media source | on-prem or block |
| test_media_coverage_ledger_marks_partial | Transcript not full capture | video transcript only | lost layers named |
| test_wave9_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave9_sample_caps_are_enforced | Bounded sampling | Sample manifest | Per-bucket caps, seed/sort, max files, and max bytes present |
| test_skills_validate_after_updates | Skills valid | updated skills | `uv run skills/validate_skill.py` passes |

---

## Acceptance Criteria

- [ ] Archives are list-first and not expanded unless a bounded, integrity-checked plan exists.
- [ ] Bounded sample declares per-bucket caps, deterministic seed/sort, maximum files, and maximum bytes touched.
- [ ] Archive outputs record CRC/size/hash verification and irreducible failures.
- [ ] Archive extraction blocks zip-slip/path traversal and decompression-ratio/bomb cases before expansion.
- [ ] Media selection is value-gated; no default bulk transcription/OCR.
- [ ] Binaries, build artifacts, temp files, shortcuts, and backups default to exclude.
- [ ] Private/public routing applies before any derived transcript, metadata record, or extracted archive child is promoted.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved before durable media/archive records, target paths, retrieval metadata, or publication writes.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports require [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) `status:plan-approved`, local approval marker, implemented redaction canary, and recorded passing-command result before docs, comments, `llm-wiki`, or external publication.
- [ ] `% ingested success` is calculated for route/exclusion decisions, with narrow content ingestion reported separately.
- [ ] Skill evals cover the new policy, and `uv run python scripts/validate_ace_wave9_media_archive_noise.py` plus `uv run skills/validate_skill.py` pass.

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

- **Risk:** Backup archives may contain secrets, PII, stale private data, and duplicate superseded content.
- **Risk:** Hosted transcription/VLM is an egress path, so private/ambiguous media needs on-prem routing or no extraction.
- **Open:** Tool choices for media/archive probing need license verification before adoption.

---

## Complexity

**T3** - multiple source classes, security/PII egress, archive integrity, routing governance, docs, skills, and evals.
