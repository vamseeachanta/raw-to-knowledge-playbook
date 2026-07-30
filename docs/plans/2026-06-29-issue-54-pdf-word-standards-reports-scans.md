# Plan for #54: ACE Wave 3 PDF, Word, Standards, Reports, and Scanned Document Lane

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-07-03
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/54
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-07-03-plan-54-claude-r1.md | scripts/review/results/2026-07-03-plan-54-codex-r1.md | Gemini unavailable/not-run until formal review dispatch

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/01-document-taxonomy.md` defines standards/codes as L4-L5 candidates, reports as L1-L4, forms/templates as L3 rejects, Word reports as explicit XML-table/report-template sources, and scanned documents as L0 or `ocr-interpreted`.
- `docs/03-verification-playbook.md` and `skills/verify-batch/SKILL.md` require table rows to begin as `provisional-unverified` and promote only after independent verification with closed-set verdicts.
- `docs/09-office-formats.md` defines Word reports/specifications as prose plus explicit XML tables, heading/style/template structure, tracked changes, comments, and embedded objects that route to the spreadsheet lane.
- `docs/11-imagery-and-scans.md` states OCR is interpretation, never deterministic raw extraction; scanned tables should expect high rejection/defer rates and may need manual digitization.
- `docs/18-security-and-pii.md` requires every hosted vision/OCR egress decision to fail closed on private/unknown pages and emit an append-only hash-chained egress record before any cloud call.
- `skills/source-extraction-coverage/SKILL.md`, `skills/source-extract-fidelity/SKILL.md`, `skills/format-coverage-ledger/SKILL.md`, `skills/public-private-routing/SKILL.md`, `skills/independent-oracle-validation/SKILL.md`, `skills/page-shape-contract/SKILL.md`, and `skills/verify-batch/SKILL.md` are the method surface this lane will consume and update if new failure modes appear.

### Related issues and live gate state
- [#54](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/54) is open with labels `strengthening`, `lane:claude`, and `priority:high`; no local approval marker exists at `.planning/plan-approved/54.md`.
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the approved parent epic. It does not approve this child implementation.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) remains the unapproved wave-0 umbrella. Its split implementation issues [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) are implemented/closed and may be consumed as closed contracts.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is implemented/closed with user approval marker, validators, passing-command evidence, and implementation closeout evidence. #54 still must validate any durable store, retrieval metadata, lifecycle state, target path, persistent metric, or private measured sidecar against the exact artifact set before writing it.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) is implemented/closed with manifest freshness evidence, and [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) implemented trusted-evidence integration. The current trusted-evidence registry has an empty `trusted_evidence` list, so operational ACE content sampling must fail closed until a trusted #62 evidence pointer exists.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) is implemented/closed with user approval marker, public-output canary, and passing-command evidence. Public docs navigation, `mkdocs.yml`, `llm-wiki`, GitHub-public corpus summaries, measured ACE-derived reports, and external publication still require the #63 canary to pass on the exact artifact set before exposure.
- [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) bounds downstream sampling requests. Under its current contract, downstream operational requests are metadata-only request records; they do not authorize document content-byte reads for measured ingestion.

### Source inventory
- The issue-body inventory states approximately 294k document files / 332.9 GB, with PDFs alone around 253k files / 284.5 GB.
- The issue body also identifies a 43 GB standards library bucket. This plan will not copy raw source paths from the share into public artifacts.
- Expected useful ingestion for the class remains 60-85% at planning level, but the executable #54 metric will be synthetic/metadata-only until trusted #62/#70 evidence and a #67 content-byte extension authorize bounded operational reads.

### Extension/type map

| Extension/type | Content class | Expected useful ingestion into `llm-wiki` if eligible | Detailed content analysis | Success measurement | Ease/difficulty |
|---|---|---:|---|---|---:|
| Born-digital `.pdf` standards/codes | Normative text plus dense engineering tables | 65-85%, public only when license/routing permits | Detect text layer, title/revision, page count, headings, clauses, tables, figures, watermarks, extracted text yield, table count, and standards/license restriction state. | Successful only when route target is closed, text/table yield is recorded, restricted text is not public, and tables remain provisional until verified. | 4/11 |
| Born-digital `.pdf` reports/specifications | Mixed prose, client-sensitive data, tables, figures | 50-80%, often private-sidecar or metadata-only | Detect text layer, section hierarchy, abstract/introduction/conclusion shape, table/figure inventory, confidentiality markers, title-page metadata, and source-derived claim risk. | Successful only when public/private routing precedes target selection and source-derived claims trace to deterministic extract spans. | 4/11 |
| Scanned/image-only `.pdf` | Document image requiring OCR or description | 20-60%, mostly metadata/private unless high value | Detect low/no text layer, page image count, OCR confidence/yield, blur/skew risk, legible text, table-image candidates, and manual-digitization candidates. | OCR output is successful only as `ocr-interpreted`; it is never counted as deterministic raw text. Scanned tables stay provisional/deferred until vision/manual verification. | 6/11 |
| `.docx` Word reports/specs | XML prose, styles, comments, tracked changes, explicit tables | 60-85%, depending confidentiality and embedded objects | Extract paragraphs, heading hierarchy, tables, captions, comments, tracked-change disposition, style/template signals, embedded object inventory, and known losses. | Successful only when table rows start provisional, tracked-change/comment policy is explicit, and embedded objects route to the owning lane. | 4/11 |
| Legacy `.doc`, `.rtf`, `.odt`, document-like text exports | Non-primary office/document formats | Metadata-only/deferred until adapter proof | Inventory extension, size, detected converter/parser availability, title metadata if safe, and route/defer reason. | Excluded from content-ingestion denominator unless an approved adapter and scan-safe fixture prove extraction behavior. | 6/11 |
| Forms/templates | Blank or proforma structures | 0-20%, usually excluded_no_ingest | Detect blank-field/template signals, repeated labels, no filled values, and false-positive table risk. | Successful if rejected/excluded with reason before table verification budget is spent. | 3/11 |
| Brochures/catalogs/minutes/newsletters | Low-value marketing/admin prose | 0-30%, usually excluded_no_ingest or metadata-only | Detect low-value content signals, duplicate/superseded copies, marketing/admin vocabulary, and absence of durable engineering data. | Successful if excluded separately from ingestion failures and not counted in eligible denominator. | 3/11 |
| Standards/reports with embedded or pasted image tables | Mixed document plus image evidence | 20-70%, value depends on verification cost | Detect image-backed tables, captions, page-image anchors, and table/figure handoff to imagery/vision verification. | Image tables are not trusted from OCR; they become verified only after independent table/vision verification or manual digitization. | 6/11 |

### Gaps identified
- No ACE document-lane validator exists at `scripts/validate_ace_wave3_document_lane.py`.
- No #54 scan-safe fixtures exist for born-digital PDF, scanned PDF, DOCX/report, standards restriction, form/template exclusion, low-value brochure exclusion, OCR trust labels, table provisional state, or public/durable gate blocking.
- The current #54 issue body still says "#50 wave 0 ledger/routing contract should be planned first." The current dependency story is: #50 approved parent; #51 unapproved umbrella; #65-#69 closed split contracts; #61/#62/#63/#70/#71/#72 closed or marker-backed as recorded in coordination docs; #70 trusted evidence registry currently empty.
- No current method doc/eval has ACE wave-3-specific cases for OCR trust, hosted vision egress ledgers, DOCX tracked-change/comment disposition, standards/license restriction routing, image-table handoff, or document-family template extraction.

### Evidence

**Issue and marker status** (verified 2026-07-03):
```
#54 OPEN labels=strengthening,lane:claude,priority:high; no .planning/plan-approved/54.md marker
#51 OPEN labels=strengthening,lane:claude,priority:high; no .planning/plan-approved/51.md marker
#52 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high; local marker exists
#53 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high; local marker exists
#61 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high; local marker exists
#62 CLOSED labels=strengthening,status:plan-approved,lane:codex,priority:high; local marker exists
#63 CLOSED labels=strengthening,status:plan-approved,lane:claude,priority:high; local marker exists
#65-#72 CLOSED or marker-backed as recorded in `docs/plans/ace-share-ingestion-wave-coordination.md`
```

**File existence** (verified 2026-07-03):
```
EXISTS docs/01-document-taxonomy.md
EXISTS docs/03-verification-playbook.md
EXISTS docs/09-office-formats.md
EXISTS docs/11-imagery-and-scans.md
EXISTS docs/18-security-and-pii.md
EXISTS skills/source-extraction-coverage/SKILL.md
EXISTS skills/source-extract-fidelity/SKILL.md
EXISTS skills/verify-batch/SKILL.md
EXISTS skills/independent-oracle-validation/evals/evals.json
EXISTS skills/format-coverage-ledger/SKILL.md
EXISTS skills/public-private-routing/SKILL.md
EXISTS skills/page-shape-contract/SKILL.md
EXISTS scripts/ace_bounded_sampling_firewall.py
EXISTS scripts/ace_manifest_evidence_trust.py
EXISTS scripts/validate_ace_public_artifacts.py
EXISTS scripts/legal/legal-sanity-scan.sh
EXISTS artifacts/ace-manifest-freshness/trusted-evidence-registry.json
MISSING scripts/validate_ace_wave3_document_lane.py
MISSING tests/test_validate_ace_wave3_document_lane.py
MISSING tests/fixtures/ace-wave3-document-lane/
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-54-pdf-word-standards-reports-scans.md |
| Planned validator | scripts/validate_ace_wave3_document_lane.py |
| Planned validator tests | tests/test_validate_ace_wave3_document_lane.py |
| Planned committed fixtures | tests/fixtures/ace-wave3-document-lane/ |
| Source extraction coverage skill/evals | skills/source-extraction-coverage/SKILL.md; skills/source-extraction-coverage/evals/evals.json |
| Source extract fidelity skill/evals | skills/source-extract-fidelity/SKILL.md; skills/source-extract-fidelity/evals/evals.json |
| Verify batch skill/evals | skills/verify-batch/SKILL.md; skills/verify-batch/evals/evals.json |
| Independent oracle validation evals | skills/independent-oracle-validation/evals/evals.json |
| Format coverage ledger skill/evals | skills/format-coverage-ledger/SKILL.md; skills/format-coverage-ledger/evals/evals.json |
| Public/private routing skill/evals | skills/public-private-routing/SKILL.md; skills/public-private-routing/evals/evals.json |
| Page shape contract skill/evals | skills/page-shape-contract/SKILL.md; skills/page-shape-contract/evals/evals.json |
| Public measured ACE report | Deferred unless the [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) public-output canary passes on the exact artifact set |
| Private measured ACE sidecar | Deferred unless a [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61)-backed durable-output workflow validates the exact artifact set and private/off-public route |
| Review artifact - Claude r1 | scripts/review/results/2026-07-03-plan-54-claude-r1.md |
| Review artifact - Codex r1 | scripts/review/results/2026-07-03-plan-54-codex-r1.md |
| Review artifact - Gemini r1 | unavailable/not-run until formal review dispatch |

---

## Deliverable

This issue will produce a sensitivity-first document-lane pilot plan and, after user approval only, a test-first implementation that classifies bounded document candidates, records expected vs actual extraction coverage, separates deterministic text from interpreted OCR, gates standards/reports through public/private routing before extraction, keeps all table outputs provisional until verification, logs any vision/OCR egress decision before a hosted call, and updates method docs/skills when the pilot exposes reusable failure modes.

The approved implementation will use synthetic scan-safe fixtures by default. Under the current [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) contract, downstream operational requests are metadata-only request records; they do not authorize reading private document content bytes for measured ingestion. Therefore this issue's executable success metrics will be measured on synthetic fixtures unless a later approved issue extends the sampling firewall to content-byte pilots and a trusted [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence pointer accepted by [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) exists. Any measured ACE-derived private sidecar, target path, lifecycle field, durable metric, or persistent store write must go through a #61-backed durable-output workflow on the exact artifact set. Any public output must pass the #63 canary on the exact artifact set before exposure.

Public artifacts may expose only aggregate/synthetic evidence, opaque `public_source_token` values, or a `private_provenance_bundle_ref`. Raw provenance fields, source digests, share-relative paths, and private lookup material are private-sidecar-only and must not appear in plans, comments, public reports, docs navigation, or `llm-wiki` surfaces.

### Document Class and Route Mapping

The implementation will keep document classification separate from route target and lifecycle state. A document class cannot authorize public output by itself.

| Document evidence | `document_class` | Route implication | Notes |
|---|---|---|---|
| Born-digital PDF with standards/code evidence | `standard_pdf` | Usually `private_sidecar` or `metadata_only`; `public_llm_wiki` only after license/routing proof | Tables start provisional and require verification before trust. |
| Born-digital PDF with report/spec evidence | `report_pdf` | Route from sensitivity/routing policy | Client-sensitive reports default away from public output unless public clearance exists. |
| Low/no text layer PDF | `scanned_pdf` | Usually `metadata_only` or `private_sidecar` | OCR text is `ocr-interpreted`; image tables require vision/manual verification. |
| Word XML report/spec | `word_report` | Route from sensitivity/routing policy | Tables are explicit XML but still provisional; comments/tracked changes need explicit disposition. |
| Blank form/template | `form_template` | Usually `excluded_no_ingest` | This is a successful exclusion, not an ingestion failure. |
| Marketing/admin low-value document | `low_value_document` | Usually `excluded_no_ingest` or `metadata_only` | Keep out of the eligible ingestion denominator unless a durable content signal is present. |
| Unsupported legacy/converter-bound document | `unsupported_document` | `metadata_only` or `excluded_no_ingest` until adapter proof | `.doc`, `.rtf`, `.odt`, and similar variants need adapter tests before content success. |

---

## Pseudocode

```text
require explicit user approval before implementation
load #65 route/store vocabulary and #67 bounded sampling contract
load #62/#70 trusted evidence registry state
if operational ACE sampling requested:
  require trusted #62 evidence pointer accepted by #70
  require #67 metadata-only request shape, fixed seed/sort, per-bucket/file/byte caps
  fail closed while trusted evidence registry is empty
else:
  use synthetic scan-safe fixtures only

for each candidate document record:
  classify by structure and content evidence, not filename or folder alone
  assign document_class separately from route_target and lifecycle state
  assign closed route_target before any target path or output surface is selected
  declare extraction_estimate before extraction
  if born-digital pdf:
    run deterministic text/page/table probe
    record extraction_yield, page/text/table counts, known losses, watermark risk, and table candidates
  if scanned/image-only pdf:
    route to OCR/description recipe
    decide on-prem vs hosted vision/OCR egress before rendering/sending page images
    if classification is private or unknown, or detector trips, route on-prem and log the egress decision
    record `ocr-interpreted` trust label, OCR confidence/yield, and scan-quality risks
    never claim OCR as deterministic raw text or deterministic source-citable text
  if word report/spec:
    parse paragraphs/headings/tables/styles/comments/tracked-change disposition from structured XML
    route embedded objects to their owning lane
  if standards/restricted source:
    run license/visibility gate before text extraction
    route restricted standards metadata-only or private-sidecar unless public clearance exists
  if form/template or low-value document:
    exclude with reason and keep out of the eligible denominator
  enqueue table candidates as provisional only
  verify any trusted table candidate through independent table/vision/manual proof before promotion, enforcing exact table identity and closed status vocabularies
  keep operational requests metadata-only until a later approved issue extends #67 for content-byte pilots
  keep durable stores, retrieval metadata, lifecycle fields, target paths, private sidecars, and persistent metrics outside #54 classifier rows unless the exact artifact set passes the #61 workflow
  keep docs nav, mkdocs, llm-wiki, public case reports, and external publication outside #54 unless the exact artifact set passes the #63 canary
  compute success only for eligible candidate items, with hard exclusions reported separately
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | scripts/validate_ace_wave3_document_lane.py | Executable validator for document classes, OCR trust labels, vision egress ledger, table provisional state, route/durable/public gates, exact `public_scan_paths()`, and success metric fields |
| Create | tests/test_validate_ace_wave3_document_lane.py | Red/green tests for all #54 gate and document-lane behavior |
| Create | tests/fixtures/ace-wave3-document-lane/ | Scan-safe synthetic fixture records and tiny generated-at-test document samples only; no private corpus bytes |
| Modify | skills/source-extraction-coverage/evals/evals.json | Add estimate/yield/private-provenance/trust cases for born-digital PDF, scanned PDF, and DOCX-like records |
| Modify | skills/source-extract-fidelity/evals/evals.json | Add source-claim traceability cases for document-derived prose and OCR interpretation boundaries |
| Modify | skills/format-coverage-ledger/evals/evals.json | Add PDF/DOCX/scanned known-loss cases, including comments/tracked changes and image-table handoff |
| Modify | skills/verify-batch/evals/evals.json | Add table provisional/verified/deferred/rejected status cases for document tables |
| Modify | skills/independent-oracle-validation/evals/evals.json | Add second-pass verification cases for table/claim/OCR disputes |
| Modify | skills/public-private-routing/evals/evals.json | Add standards/report/public-output fail-closed cases |
| Modify | skills/page-shape-contract/evals/evals.json | Add document page-shape/trust-label/provenance cases |
| Modify | docs/01-document-taxonomy.md | Patch document-lane guidance from pilot evidence |
| Modify | docs/03-verification-playbook.md | Patch table/OCR verification guidance from pilot evidence |
| Modify | docs/09-office-formats.md | Patch DOCX tracked-change/comment/table guidance if pilot evidence demands it |
| Modify | docs/11-imagery-and-scans.md | Patch OCR/scanned-document guidance from pilot evidence |
| Modify | docs/18-security-and-pii.md | Patch egress-ledger/routing guidance if standards/reports expose a new sensitivity failure mode |
| Modify | docs/plans/README.md | Update #54 status after review; correct any discovered queue drift |
| Modify | docs/plans/ace-share-ingestion-wave-coordination.md | Update #54 row after review with current gates and review artifact paths |
| Modify | .github/workflows/validate.yml | Run the #54 validator/tests once implemented |

Public `docs/case-studies/` output is intentionally not in the implementation file set. Any such output must pass the [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) public-output canary on the exact artifact set before exposure. Private measured ACE sidecars are also intentionally absent from #54 classifier rows unless a [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61)-backed durable-output workflow validates the exact artifact set.

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_document_classification_closed_values | Document class enum stays closed | Synthetic candidate records | Only `standard_pdf`, `report_pdf`, `scanned_pdf`, `word_report`, `form_template`, `low_value_document`, `unsupported_document` |
| test_route_enum_separate_from_document_class | Route target is not document class | Excluded form/template record | `document_class=form_template`, `route_target=excluded_no_ingest` |
| test_born_digital_pdf_requires_text_layer_probe | Born-digital path is evidence-based | PDF-like fixture with text layer metadata | Deterministic extraction route allowed only with text-layer evidence |
| test_restricted_standard_routes_before_text_extraction | Standards license/visibility gate precedes extraction | Restricted-standard fixture with no public clearance | Text extraction/public route blocked; metadata-only or private route allowed |
| test_scanned_pdf_requires_ocr_interpreted_trust | OCR is interpretation | Scanned PDF fixture marked raw-extracted | Validation fails; `ocr-interpreted` passes |
| test_ocr_output_never_counts_as_raw_text | OCR cannot masquerade as deterministic extraction | OCR fixture with raw-text trust label | Validation fails |
| test_scanned_doc_whole_artifact_interpreted_not_source_citable | Scanned extraction is not deterministic source text | OCR fixture with deterministic/verbatim citation claim | Validation fails until independent verification supports the claim |
| test_vision_egress_ledger_fail_closed | Hosted vision/OCR egress is gated and auditable | Private/unknown page image request, cloud route, or missing egress fields | Routes `on-prem`; any `cloud:*` row requires affirmative clearance/ZDR-eligible endpoint and hash-chained ledger fields |
| test_docx_tables_start_provisional | Word tables are explicit but untrusted | DOCX-like table fixture | Table rows start `provisional-unverified` |
| test_pdf_tables_start_provisional | PDF tables are not trusted on parse | Born-digital PDF table fixture | Table rows start `provisional-unverified` |
| test_verified_table_requires_independent_proof | Table promotion is gated | Table marked verified without proof | Validation fails |
| test_table_closed_status_sets_and_columns | Table status vocabularies are not mixed | Table row with bad parse/structural status or swapped columns | Validation fails |
| test_table_watermark_in_cell_rejects_for_reextract | Watermark contamination is not verified-with-note | Table row with in-cell watermark evidence | Row is rejected/deferred for re-extraction, not verified |
| test_table_rightmost_column_shift_defers | Rightmost-column drift is caught | Table proof where first cell matches but rightmost column is shifted | Row is deferred with defect class |
| test_table_exact_csv_path_required | Table verification anchors exact artifact identity | Verification record using doc id/glob instead of exact CSV path | Validation fails |
| test_no_csv_figure_identity_preserved | Figures are not converted into fake tables | Figure/no-csv row | `structural_status=no-csv`; no table promotion |
| test_tracked_changes_and_comments_have_disposition | Word decisions are not silently lost | DOCX-like fixture with comments/tracked changes | Disposition is required: captured, discarded-with-reason, or routed-private |
| test_embedded_objects_route_to_owner_lane | Word/PDF embedded objects are not silently parsed here | Embedded workbook/object fixture | Object is routed/deferred to owning lane |
| test_docx_review_history_and_embedded_objects_not_silent_loss | Word report completeness is explicit | DOCX-like fixture with review history and embedded object | Review history has disposition; embedded object routes to owning lane |
| test_standards_restricted_text_not_public | Standards restriction blocks public output | Restricted standard fixture with public route | Validation fails unless public clearance evidence exists |
| test_client_report_defaults_private_or_metadata | Sensitive reports fail closed | Report fixture without public clearance | Public route blocked |
| test_forms_templates_are_successful_exclusions | Blank templates are not ingestion failures | Form/template fixture | `excluded_no_ingest` with reason; excluded from denominator |
| test_low_value_documents_excluded_separately | Brochures/admin noise do not skew success metric | Low-value fixture | Exclusion recorded separately from failures |
| test_known_losses_are_ledgered | Lossy document layers are explicit | DOCX/PDF/scanned fixture with comments/images/OCR | Known-loss ledger fields are present |
| test_extraction_estimate_yield_required | Shallow extraction is visible | Candidate missing estimate or yield | Validation fails |
| test_success_metric_defined_for_eligible_items | `% ingested success` is measurable | Synthetic pilot ledger | Numerator, denominator, threshold, command, exclusions present |
| test_missing_trusted_62_evidence_fails_closed | Empty #70 registry blocks operational sampling | Downstream request without trusted pointer | Sampling denied; synthetic-only path remains allowed |
| test_fixture_62_evidence_cannot_authorize_sampling | Fixture evidence cannot authorize operational run | #62 fixture pointer | Request denied |
| test_67_boundary_caps_import_contract_values | Boundary caps are imported from #67 | Request at 200 rows, 25 files, 1048576 bytes and one-over variants | Boundary accepted when other gates pass; one-over variants fail |
| test_sampling_uses_snapshot_seed_caps_and_denies_unbounded_traversal | Sampling obeys the firewall contract | Sampling request missing snapshot/seed/sort/caps or using unbounded traversal | Validation fails |
| test_67_content_byte_sampling_deferred | Current #67 boundary is metadata-only | Operational request asks to read content bytes | Validation fails with future-extension blocker |
| test_61_durable_fields_blocked | Durable outputs remain gated | Record with store path/retrieval/lifecycle/persistent metrics without exact #61 durable-output validation | Validation fails |
| test_63_public_output_blocked | Public surfaces remain gated | Docs nav, mkdocs, llm-wiki, public report path without exact #63 canary pass | Validation fails |
| test_public_surfaces_reject_private_provenance_fields | Public artifacts cannot leak private source fields | Public report/comment fixture with raw source digest or private lookup material | Validation fails; `public_source_token` or `private_provenance_bundle_ref` passes |
| test_wave3_public_scan_paths_cover_exact_surfaces | Validator scans the exact public surfaces | #54 validator `public_scan_paths()` output | Plan, README, coordination, validator, tests, fixtures, skills/docs, review artifacts, workflow, and issue-comment draft are covered |
| test_raw_document_bytes_not_committed | Private/source bytes stay out of repo | Tracked fixture tree containing document binaries | Validator fails |
| test_scan_safe_negative_fixtures | Negative examples do not self-block scanners | Runtime-assembled hostile strings | Tests assert denials while source files pass public/legal scans |

---

## Acceptance Criteria

- [ ] Document records are classified as `standard_pdf`, `report_pdf`, `scanned_pdf`, `word_report`, `form_template`, `low_value_document`, or `unsupported_document` before extraction or target selection.
- [ ] `document_class`, `route_target`, and lifecycle/trust state are separate fields; the validator rejects enum intermixing.
- [ ] Bounded sample design separates born-digital PDFs, scanned PDFs, Word reports/specs, standards, forms/templates, and low-value brochures.
- [ ] Every extracted document records extraction estimate, extraction yield, opaque public token, private-sidecar provenance policy, trust label, and route target; raw provenance fields and source digests remain private-only.
- [ ] Restricted standards run a license/visibility gate before text extraction and route metadata-only or private-sidecar unless public clearance exists.
- [ ] OCR output is labeled `ocr-interpreted`; it is never deterministic raw text, never counted as raw-extracted success, and never source-citable until independently verified.
- [ ] Hosted vision/OCR egress is fail-closed and recorded in an append-only hash-chained ledger with page-image digest, classification, route decision, detector version/verdict, redaction flag, timestamp, and policy version.
- [ ] PDF and DOCX table rows enter `provisional-unverified` and only become trusted after independent proof; verification enforces closed status sets, exact table identity, watermark rejection, rightmost-column checks, and no-csv figure identity.
- [ ] Word comments and tracked changes are either captured, routed private, or discarded with reason; they are never silently lost.
- [ ] Standards and client-sensitive reports fail closed for public output unless public clearance and #63 canary evidence exist for the exact artifact set.
- [ ] Forms/templates and low-value brochures are excluded with reason and reported separately from ingestion failures.
- [ ] `% ingested success` is calculated as `successful_routed_items / eligible_candidate_items * 100`, with hard exclusions and unsupported classes reported separately.
- [ ] Operational ACE sampling is blocked unless a [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67) bounded request supplies a trusted [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) evidence pointer accepted by [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70).
- [ ] Current operational sampling remains metadata-only under [#67](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/67); content-byte pilot sampling requires a future approved firewall-extension issue.
- [ ] Durable stores, retrieval metadata, lifecycle state, persistent metrics, target paths, and private measured sidecars stay outside #54 classifier rows unless a [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61)-backed durable-output workflow validates the exact artifact set.
- [ ] Public docs navigation, `mkdocs.yml`, `llm-wiki`, measured ACE-derived public summaries, GitHub-public corpus reports, and external publication stay outside #54 unless the [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) canary passes on the exact artifact set.
- [ ] The #54 validator defines `public_scan_paths()` for the exact #54 public surface set and passes those paths to both `validate_ace_public_surface_scan.py` and `validate_ace_public_artifacts.py`.
- [ ] New reusable method gaps produce a governing doc patch, skill-eval update, or follow-on issue before closeout.
- [ ] Plan-review evidence is committed, pushed, and linked in a scanned issue comment before applying `status:plan-review`.
- [ ] The issue-comment body is written to a repo-local temporary review artifact, scanned by `validate_ace_public_surface_scan.py` and `scripts/legal/legal-sanity-scan.sh`, posted via `gh issue comment --body-file`, then removed before final commit/closeout.
- [ ] No `status:plan-approved` label is applied and no `.planning/plan-approved/54.md` marker is created by the planning agent.
- [ ] `PYTHONDONTWRITEBYTECODE=1 uv run python scripts/validate_ace_wave3_document_lane.py`, `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest tests.test_validate_ace_wave3_document_lane`, and `PYTHONDONTWRITEBYTECODE=1 uv run skills/validate_skill.py` pass after implementation.

---

## Planned Review and Validation Commands

These commands will be run before posting [#54](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/54) plan-review evidence. The review-artifact scan list must match the final materialized artifact set; missing provider artifacts are not referenced. If Gemini is unavailable, the review summary and coordination row will record `Gemini: unavailable: <reason>` instead of naming a missing file.

```bash
PLAN_54_COMMENT_BODY=artifacts/ace-wave3-document-lane/plan-review-evidence/issue-54-plan-review-comment.md
PYTHONDONTWRITEBYTECODE=1 uv run python scripts/validate_ace_epic_wave_coordination.py
PYTHONDONTWRITEBYTECODE=1 uv run python scripts/validate_ace_public_surface_scan.py \
  --scan-public-path docs/plans/2026-06-29-issue-54-pdf-word-standards-reports-scans.md \
  --scan-public-path docs/plans/README.md \
  --scan-public-path docs/plans/ace-share-ingestion-wave-coordination.md \
  --scan-public-path scripts/review/results/2026-07-03-plan-54-claude-r1.md \
  --scan-public-path scripts/review/results/2026-07-03-plan-54-codex-r1.md \
  --scan-public-path "$PLAN_54_COMMENT_BODY"
PYTHONDONTWRITEBYTECODE=1 uv run python scripts/validate_ace_public_artifacts.py \
  --scan-public-path docs/plans/2026-06-29-issue-54-pdf-word-standards-reports-scans.md \
  --scan-public-path docs/plans/README.md \
  --scan-public-path docs/plans/ace-share-ingestion-wave-coordination.md \
  --scan-public-path scripts/review/results/2026-07-03-plan-54-claude-r1.md \
  --scan-public-path scripts/review/results/2026-07-03-plan-54-codex-r1.md \
  --scan-public-path "$PLAN_54_COMMENT_BODY"
bash scripts/legal/legal-sanity-scan.sh \
  --scan-public-path docs/plans/2026-06-29-issue-54-pdf-word-standards-reports-scans.md \
  --scan-public-path docs/plans/README.md \
  --scan-public-path docs/plans/ace-share-ingestion-wave-coordination.md \
  --scan-public-path scripts/review/results/2026-07-03-plan-54-claude-r1.md \
  --scan-public-path scripts/review/results/2026-07-03-plan-54-codex-r1.md \
  --scan-public-path "$PLAN_54_COMMENT_BODY"
bash scripts/legal/legal-sanity-scan.sh --diff-only
git diff --check --cached
git diff --check
```

If review produces a later no-MAJOR round, the scan path list will be updated to the final round artifacts before commit and label movement.

### Plan-review transition criteria

#54 is T3. The formal plan-review gate requires a same-round provider review set with at least two usable provider results and no usable provider returning MAJOR. Preparatory Codex subagent artifacts are useful evidence but do not count as provider-review quorum. Gemini may be recorded as `UNAVAILABLE` only with an exact CLI/auth/quota reason and does not count toward the usable-provider floor.

For the `status:plan-review` transition, the operator will:

1. update this plan's header, review artifact list, Adversarial Review Summary, and Overall result to `plan-review` / no-MAJOR provider review evidence;
2. update `docs/plans/README.md` and `docs/plans/ace-share-ingestion-wave-coordination.md` so #54 records `plan-review` with `implementation ready=false`;
3. commit and push the plan, index/coordination rows, and review artifacts before any label transition;
4. create temporary repo-relative Markdown body files under `artifacts/ace-wave3-document-lane/plan-review-evidence/`, scan them with the parent public scanner, #63 public-output canary, and #69 legal scan, post the scanned comment, refetch the posted body into the same repo-relative scratch directory, scan the refetch, then remove those scratch files before final clean-state verification;
5. record the posted comment URL and only then add `status:plan-review`;
6. stop before `status:plan-approved`; user approval remains required.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r1 | PENDING | Formal provider review not yet completed. |
| Codex r1 | PENDING | Formal provider review not yet completed. |
| Gemini r1 | NOT-RUN | Gemini availability will be checked during formal review dispatch. |

**Overall result:** PENDING - draft only; not ready for `status:plan-review`.

---

## Risks and Open Questions

- **Risk:** The [#70](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70) trusted evidence registry is empty, so operational sampling claims must fail closed.
- **Risk:** Hosted vision/OCR verification can leak sensitive pages unless the public/private route is fail-closed before any egress.
- **Risk:** Standards may be license-restricted even when technically extractable; public `llm-wiki` routing must require explicit public clearance.
- **Risk:** Scanned tables may have high reject/deferred rates; manual digitization may be cheaper than OCR repair for high-value tables.
- **Risk:** Word comments/tracked changes can contain decision history or sensitive review notes; silent discard and public capture are both unsafe.
- **Open:** Exact private sidecar and public `llm-wiki` output paths remain outside #54 unless the exact artifact set passes #61/#63 workflows.
- **Open:** Legacy `.doc`/`.rtf`/`.odt` handling may need a follow-on adapter issue rather than being included in the first implementation.

---

## Complexity

**T3** - multi-format document ingestion, routing, OCR interpretation, table verification, standards/license restriction handling, Word report semantics, public/private firewall, durable-output dependency, and cross-skill/doc updates.
