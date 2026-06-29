# Plan for #57: ACE Wave 6 CAD, Drawings, Neutral Geometry, and Native Seat-Export Lane

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/57
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:codex
> **Review artifacts:** scripts/review/results/2026-06-29-plan-57-claude.md | scripts/review/results/2026-06-29-plan-57-codex.md | scripts/review/results/2026-06-29-plan-57-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/21-cad-and-brep-geometry.md` states native CAD is license-locked, extensions lie, and geometry conversion needs invariant verification.
- `docs/12-tooling-landscape.md` records CAD tooling caveats: no OSS native SolidWorks/Inventor reader, neutral formats are the license-free extraction path.
- `docs/18-security-and-pii.md` and `docs/19-trust-boundary-and-private-mode.md` require fail-closed routing where title blocks, BOMs, paths, or model metadata expose private identifiers.

### Related issues
- [#57](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/57) owns the CAD wave.
- [#1](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/1) and [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12) are method anchors.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) provides the route/ledger dependency.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable geometry stores, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- `ACE_SHARE_ROOT/_cad-index/index-summary.json`: 464,170 indexed CAD files.
- Readability: 242,967 seat-only; 216,702 DWG-convertible 2D; 4,235 immediately OSS-readable/mesh/2D/3D.
- Existing ACE artifacts include `_cad-index/`, `_glb-library/`, and `_step-export/`.
- Expected routed success target: at least 95% of bounded index rows receive a valid route/trust classification; geometry promotion is measured only for rows with invariant verification.

### Gaps identified
- No ACE CAD lane pilot exists in this repo.
- No CAD-specific route/trust-state eval exists for metadata-only, drawing extraction, neutral geometry, and seat-export queue.
- No freshness check exists for `_cad-index` that avoids recrawling the share.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#57 OPEN ACE wave 6: CAD, drawings, neutral geometry, and native seat-export lane labels=strengthening,lane:codex,priority:high
```

**File existence**:
```
EXISTS docs/21-cad-and-brep-geometry.md
EXISTS docs/12-tooling-landscape.md
EXISTS ${ACE_SHARE_ROOT}/_cad-index/index-summary.json
EXISTS ${ACE_SHARE_ROOT}/_cad-index/cad-readability-index.tsv
MISSING docs/case-studies/ace-wave-6-cad-drawings-geometry.md
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-57-ace-wave-6-cad-drawings-neutral-geometry-seat-export.md |
| Pilot report | docs/case-studies/ace-wave-6-cad-drawings-geometry.md |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-57-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-57-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-57-gemini.md |

---

## Deliverable

A tested CAD playbook lane that turns the ACE CAD index into routed metadata, drawing extraction, neutral-geometry extraction, and native seat-export queues with explicit trust states and invariant verification.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
load ACE_SHARE_ROOT/_cad-index/index-summary.json and cad-readability-index.tsv
assert no direct share recrawl
build bounded batch manifest:
  max 25 rows per readability bucket, max 150 rows per pilot PR, deterministic seed/sort
for each bounded CAD row:
  classify by header/content/readability, not suffix
  apply exclusion and private routing
  if metadata_only: emit public-safe metadata stub with source_id/source_sha256 only
  if dwg/dxf: detect header version and extract title blocks/layers/entities
  if neutral_geometry: read with structured reader and compute invariants
  if native_seat_only: enqueue licensed seat export; make no geometry claim
for converted geometry:
  verify solid count, bbox, volume/mass, tree count within tolerance
  reject/defer IGES/surface outputs until sewn
  record units, material, coordinate assumptions
run independent oracle validation and update CAD docs/skills/evals
compute routed success numerator/denominator for bounded index rows
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-wave-6-cad-drawings-geometry.md | CAD pilot and trust-state evidence |
| Modify | docs/21-cad-and-brep-geometry.md | Add ACE index/readability/trust-state rules |
| Modify | docs/index.md | Update site count/link if doc 21 is published |
| Modify | mkdocs.yml | Publish doc 21 or document why it remains repo-only |
| Modify | docs/12-tooling-landscape.md | Carry CAD tool containment and adoption caveats |
| Modify | docs/01-document-taxonomy.md | Align CAD lane with taxonomy/trust states |
| Modify | docs/18-security-and-pii.md | Clarify title-block/BOM/path leakage routing |
| Modify | docs/19-trust-boundary-and-private-mode.md | Clarify private-mode CAD derived artifacts |
| Modify | skills/content-triage-and-exclusion/evals/evals.json | CAD exclusion/routing evals |
| Modify | skills/format-coverage-ledger/evals/evals.json | CAD known-loss evals |
| Modify | skills/source-extraction-coverage/evals/evals.json | CAD estimate/yield evals |
| Modify | skills/source-extract-fidelity/evals/evals.json | CAD claim traceability evals |
| Modify | skills/independent-oracle-validation/evals/evals.json | Geometry invariant/oracle evals |
| Create | scripts/validate_ace_wave6_cad.py | Executable validator for index source, batch caps, route/trust states, success metric, and public artifact safety |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_cad_starts_from_index_not_recrawl | `_cad-index` is source | Command/code references | Uses `ACE_SHARE_ROOT/_cad-index` and no direct share recrawl |
| test_cad_batch_caps_are_enforced | Pilot batch safety | Batch manifest | Max rows per bucket and max rows per PR enforced |
| test_cad_header_detection_beats_extension | Header/content routing | DWG/STEP/ambiguous examples | Header classification wins |
| test_cad_trust_states_are_distinct | Separate states | Mixed CAD rows | metadata/drawing/neutral/seat-export states |
| test_native_seat_only_not_readable | Native formats not claimed readable | SW/Inventor rows | Seat-export queue only |
| test_neutral_geometry_invariants_required | Geometry verification | STEP/IGES sample | Invariant report required |
| test_assembly_tree_uses_structured_reader | BOM/tree claims | Assembly row | Product/tree evidence required |
| test_cad_public_routing_blocks_identifiers | Private identifiers blocked | Title block/path/BOM names | Public output blocked or abstracted |
| test_oracle_residuals_are_attributed | Oracle mismatch explanation | Distinct-engine comparison | Residual cause recorded |
| test_wave6_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |

---

## Acceptance Criteria

- [ ] Wave starts from `ACE_SHARE_ROOT/_cad-index` rather than re-crawling the share.
- [ ] Pilot processing is bounded to explicit batch manifests with per-bucket and per-PR row caps.
- [ ] CAD files route by content/header/readability, not extension alone.
- [ ] Metadata-only, drawing extraction, neutral geometry extraction, and seat-export queues are distinct trust states.
- [ ] Geometry conversion claims require round-trip invariant evidence.
- [ ] Native seat-only files are not treated as readable until exported through a licensed-seat workflow.
- [ ] Units, material/density, coordinate frame, source hash, CAD system/version, and schema assumptions are recorded.
- [ ] Raw CAD binaries are never committed; public outputs use source IDs/hashes and abstract private identifiers.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved before durable geometry stores, target paths, retrieval metadata, or publication writes.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports pass the [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) redaction canary before publication.
- [ ] `% ingested success` is calculated for bounded index-row routing, with geometry promotion reported only for rows passing invariant verification.
- [ ] `uv run python scripts/validate_ace_wave6_cad.py` and `uv run skills/validate_skill.py` pass.

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

- **Risk:** `_cad-index` may be stale; plan needs a cheap freshness check without recrawling.
- **Risk:** Licensed-seat export owner/tooling is not defined in the issue.
- **Risk:** IGES/surface files may appear usable while failing mass/solid invariants.
- **Open:** Storage target and schema depend on #12/#61 decisions.

---

## Complexity

**T3** - large CAD corpus, mixed proprietary/neutral formats, licensed-seat boundary, geometry-loss risk, private identifiers, and oracle-based verification.
