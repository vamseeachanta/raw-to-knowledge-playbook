# Plan for #56: ACE Wave 5 Images, Scans, Photos, Plots, and Evidence-Series Lane

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/56
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-56-claude.md | scripts/review/results/2026-06-29-plan-56-codex.md | scripts/review/results/2026-06-29-plan-56-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/11-imagery-and-scans.md` treats images as described records, not extracted text; scans are `ocr-interpreted`.
- `docs/18-security-and-pii.md` requires EXIF/GPS stripping and fail-closed routing for faces, plates, coordinates, and named individuals.
- `docs/12-tooling-landscape.md` discusses image/OCR/vision tool choices and license containment.

### Related issues
- [#56](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/56) covers images/scans/photos/plots.
- [#3](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/3), [#4](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/4), and [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) are method anchors.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) supplies the route/ledger dependency.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable image records, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- Images/scans: about 299.6k files / 416 GB.
- Common extensions include `.jpg`, `.png`, `.tif`, `.bmp`, `.gif`, and `.wmf`.
- Expected useful ingestion is 25-60%; many images should be metadata-only or excluded, and the pilot threshold is at least 25% routed success for eligible image candidates.

### Gaps identified
- No ACE imagery pilot exists.
- No ACE evidence-series grouping contract exists.
- No eval currently binds EXIF/PII egress to image description records.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#56 OPEN ACE wave 5: images, scans, photos, plots, and evidence-series lane labels=strengthening,lane:claude,priority:medium
```

**File existence**:
```
EXISTS docs/11-imagery-and-scans.md
EXISTS docs/12-tooling-landscape.md
EXISTS docs/18-security-and-pii.md
EXISTS skills/independent-oracle-validation/SKILL.md
MISSING docs/case-studies/ace-wave-5-images-scans-photos-plots.md
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-56-ace-wave-5-images-scans-photos-plots-evidence-series.md |
| Pilot report | docs/case-studies/ace-wave-5-images-scans-photos-plots.md |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-56-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-56-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-56-gemini.md |

---

## Deliverable

A tested imagery lane defining bounded sampling, content classification, exclusion, description/OCR records, evidence-series grouping, PII-safe routing, and independent verification.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
load bounded image candidates from wave-0 manifest
stratify by extension, size, path family, hash/phash, and source class:
  max 20 rows per bucket, deterministic seed/sort, max 200 files or 500 MB touched
for each candidate row:
  classify by content, not suffix
  apply exclusion first
  route private/unknown imagery to private_sidecar/on-prem or excluded_no_ingest
  strip EXIF before any vision path
  if scanned_doc: emit L0 or ocr_interpreted record with estimate/yield
  if photo/plot: emit observations, legible_text, uncertainty, inference_separate
  if repeated subject: group into evidence series with deterministic signals
  append route decision and verification state
run independent spot-check for OCR/description defects
compute routed success numerator/denominator for eligible candidate rows
update docs, skills, and evals
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-wave-5-images-scans-photos-plots.md | Pilot evidence and image lane rules |
| Create | scripts/validate_ace_wave5_images.py | Executable validator for EXIF/PII gates, sample caps, success metric, and public artifact safety |
| Modify | docs/11-imagery-and-scans.md | Add ACE-scale image/scan/photo/plot lane rules |
| Modify | docs/12-tooling-landscape.md | Carry tool choices and license containment |
| Modify | docs/18-security-and-pii.md | Add image egress/EXIF/faces/plates gates if gaps surface |
| Modify | docs/13-lane-flowcharts.md | Add image/scans/photos routing flow |
| Modify | skills/content-triage-and-exclusion/evals/evals.json | Image classification/exclusion evals |
| Modify | skills/source-extraction-coverage/evals/evals.json | OCR/description estimate-yield evals |
| Modify | skills/source-extract-fidelity/evals/evals.json | Description overclaim evals |
| Modify | skills/independent-oracle-validation/evals/evals.json | Second-pass image validation evals |
| Modify | skills/public-private-routing/evals/evals.json | Private imagery egress evals |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_classifies_image_sample_by_content_not_extension | Content classifier | mixed jpg/png/tif/wmf/gif | photo/plot/scan/drawing/noise/exclude |
| test_routes_private_image_on_prem | Private/PII routing | faces/plates/GPS/client marker | on-prem/private or blocked |
| test_exif_gps_stripped_before_any_vision_path | Metadata egress | Image with EXIF/GPS | EXIF removed before OCR/VLM path |
| test_scan_ocr_record_carries_estimate_yield | OCR trust | scanned page | `ocr-interpreted` plus estimate/yield |
| test_photo_description_separates_observation_inference | Description discipline | equipment photo | observations separate from inference |
| test_legible_text_is_verbatim_field | Text in image separated | nameplate/signage/gauge | legible_text field populated |
| test_pixel_table_not_verified_data | Pasted table/plot not trusted | plot image | described/queued, not verified data |
| test_second_pass_catches_description_defect | Independent check | mismatched description | Defect flagged |
| test_wave5_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave5_sample_caps_are_enforced | Bounded sampling | Sample manifest | Per-bucket caps, seed/sort, max files, and max bytes present |

---

## Acceptance Criteria

- [ ] Bounded sample classifies images as scanned docs, plots/charts, equipment/site photos, screenshots, decorative/noise, or exclude.
- [ ] Description records separate falsifiable observations, inferred interpretation, legible text, uncertainty, capture metadata, and source hash.
- [ ] OCR/caption outputs carry interpreted trust labels and verification state.
- [ ] Private/client/personal imagery routes to `private_sidecar`/on-prem or `excluded_no_ingest` before derived publication.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved before durable image records, target paths, retrieval metadata, or publication writes.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports require [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) `status:plan-approved`, local approval marker, implemented redaction canary, and recorded passing-command result before docs, comments, `llm-wiki`, or external publication.
- [ ] `% ingested success` is calculated as successful routed items over eligible candidate items, with excluded/no-ingest rows reported separately.
- [ ] Evidence-series grouping uses deterministic metadata/hash signals and records uncertainty.
- [ ] Raw images/scans are never committed; only derived records plus public source tokens/hashes are allowed in public artifacts.
- [ ] `uv run python scripts/validate_ace_wave5_images.py` and `uv run skills/validate_skill.py` pass.

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

- **Risk:** Pixel PII detection is imperfect; fail-closed routing may push most useful images to on-prem.
- **Risk:** Hosted VLM retention/ZDR terms must be verified at adoption time.
- **Open:** Final sample size and storage target depend on #51 and #61.
- **Open:** WMF/legacy drawings may need a follow-on issue.

---

## Complexity

**T3** - large private corpus, multiple image subtypes, security/egress risk, interpreted outputs, and independent verification.
