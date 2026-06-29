# Plan for #55: ACE Wave 4 Presentations and Email Archive Ingestion Lane

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/55
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-06-29-plan-55-claude.md | scripts/review/results/2026-06-29-plan-55-codex.md | scripts/review/results/2026-06-29-plan-55-gemini.md

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/09-office-formats.md` treats PowerPoint as primarily D3 reporting concepts, with slide text/notes as D1 and pasted-image tables routed to vision/image lanes.
- `docs/case-studies/format-coverage-audit.md` and `docs/20-measured-outcomes.md` record that diagram decks and attachment-heavy email are under-captured by text-only extraction.
- `skills/format-coverage-ledger/SKILL.md`, `skills/source-extract-fidelity/SKILL.md`, and `skills/public-private-routing/SKILL.md` require loss ledgers, fidelity checks, and private/public routing.

### Related issues
- [#55](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/55) covers decks and email archives.
- [#8](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/8), [#12](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/12), and [#33](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/33) are method anchors.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) must define route targets before this lane can run.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) must be approved before this lane writes durable deck/email pages, target paths, retrieval metadata, or public/private published outputs.

### Source inventory
- Presentations: about 65k files / 23 GB.
- Email: about 41.4k files / 67.3 GB.
- Expected useful ingestion: 55-80% for curated decks and 45-75% for email after privacy triage/dedupe/thread reconstruction; pilot thresholds are 55% routed success for eligible deck candidates and 45% for eligible email candidates.

### Gaps identified
- No ACE deck/email pilot exists.
- No deck/email closed-set classifier evals exist for this wave.
- No attachment recursion contract exists for ACE email archives.

### Evidence

**Issue status** (verified 2026-06-29T10:40:35Z):
```
#55 OPEN ACE wave 4: presentations and email archive ingestion lane labels=strengthening,lane:claude,priority:medium
```

**File existence**:
```
EXISTS docs/09-office-formats.md
EXISTS docs/case-studies/format-coverage-audit.md
EXISTS docs/20-measured-outcomes.md
EXISTS skills/format-coverage-ledger/evals/evals.json
MISSING docs/case-studies/ace-wave-4-decks-email-pilot.md
```

**Reproduction proofs**:
N/A - planning/governance issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-55-presentations-email-archive-ingestion-lane.md |
| Pilot report | docs/case-studies/ace-wave-4-decks-email-pilot.md |
| Review artifact - Claude | scripts/review/results/2026-06-29-plan-55-claude.md |
| Review artifact - Codex | scripts/review/results/2026-06-29-plan-55-codex.md |
| Review artifact - Gemini | scripts/review/results/2026-06-29-plan-55-gemini.md |

---

## Deliverable

A selective deck/email ingestion lane that classifies decks and email archives, extracts reusable reporting concepts and recoverable decisions, inventories attachments/loss modes, verifies a small pilot against originals, reports `% ingested success`, and routes sensitive material to `private_sidecar` or `excluded_no_ingest`.

---

## Pseudocode

```text
require #51 ledger/routing contract
require #61 before durable output, retrieval metadata, target paths, or publication writes
select bounded sample:
  max 20 rows per deck/email bucket, deterministic seed/sort, max 180 files or 250 MB touched
  reporting_concept_decks, project_client_decks, templates, image_heavy_decks,
  excluded_decks, decision_threads, attachment_index_threads,
  private_sidecar_threads, duplicate_threads, excluded_noise_threads
for each item:
  classify by content, not extension or folder
  apply exclusion before value ranking
  hash off-repo source and route fail-closed
  if deck:
    extract slide text, speaker notes, native tables
    classify reporting_concept, project_client, template, image_heavy, exclude
    route pasted tables/charts/images to vision/image lane
  if email:
    extract headers, body, thread order, encoding
    inventory attachments by name, sha256, size, derived route
    recurse supported attachments through existing lanes
    dedupe forwarded/superseded threads
record coverage ledger and run fidelity/routing gates
compute routed success numerator/denominator for eligible candidate rows
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | docs/case-studies/ace-wave-4-decks-email-pilot.md | Abstracted deck/email pilot report |
| Create | scripts/validate_ace_wave4_decks_email.py | Executable validator for classifier enums, attachment routing, sample caps, success metric, and public artifact safety |
| Modify | skills/content-triage-and-exclusion/evals/evals.json | Deck/email exclusion, dedupe, and value classification tests |
| Modify | skills/format-coverage-ledger/evals/evals.json | PPTX/Keynote/MSG/PST known-loss tests |
| Modify | skills/source-extract-fidelity/evals/evals.json | Deck/email claim-traceability tests |
| Modify | skills/public-private-routing/evals/evals.json | Sensitive summary routing tests |
| Modify | docs/09-office-formats.md | Patch deck/email lane guidance |
| Modify | docs/12-tooling-landscape.md | Add/adjust deck/email tooling verdicts |
| Modify | docs/13-lane-flowcharts.md | Add deck/email routing flow |
| Modify | docs/18-security-and-pii.md | Add egress/PII guidance if pilot reveals gaps |
| Modify | docs/19-trust-boundary-and-private-mode.md | Add private-mode implications for email/decks |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_wave4_deck_classifier_closed_set | Deck class enum | Deck feature manifest | reporting_concept/project_client/template/image_heavy/exclude |
| test_wave4_email_classifier_closed_set | Email class enum | Thread feature manifest | decision_context/attachment_index/private_sidecar/duplicate/exclude |
| test_wave4_msg_loss_modes_recorded | Email losses explicit | MSG/PST with attachments and quoted history | Loss ledger populated |
| test_wave4_attachment_inventory_recurse | Attachments routed | Email with PDF/DOCX/image | Parent records attachment hash/size and routes child |
| test_wave4_sensitive_summary_blocked_public | Summaries cannot leak | Private thread with identifiers | Public output blocked |
| test_wave4_deck_fidelity_against_original | Extract matches deck | PPTX with notes/table/image chart | Notes captured, native table provisional, image chart routed |
| test_wave4_duplicate_thread_collapses | Duplicate handling | Forwarded copies | One canonical thread plus superseded records |
| test_wave4_success_metric_defined | `% ingested success` measurable | Pilot report | Numerator, denominator, threshold, and command present |
| test_wave4_sample_caps_are_enforced | Bounded sampling | Sample manifest | Per-bucket caps, seed/sort, max files, and max bytes present |

---

## Acceptance Criteria

- [ ] Decks are classified into reporting concept, project/client deck, template, image-heavy deck, or exclude.
- [ ] Email archives are classified into decision/context, attachment index, private-sidecar, duplicate, or exclude.
- [ ] PST/MSG extraction records attachments, inline images, headers, thread order, and encoding loss modes.
- [ ] Sensitive email/deck content is routed to `private_sidecar` or `excluded_no_ingest` before any derived summary is published.
- [ ] [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved before durable deck/email pages, target paths, retrieval metadata, or publication writes.
- [ ] Manifest-backed sampling records a [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot/drift result before sample selection.
- [ ] Public-facing docs/reports pass the [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) redaction canary before publication.
- [ ] `% ingested success` is calculated separately for eligible deck and email candidates, with exclusions reported separately.
- [ ] Pilot fidelity check compares extracted deck/email samples against originals.
- [ ] Coverage ledger records deck diagrams/charts/speaker notes and email attachment/header/thread loss modes.
- [ ] Reusable rules discovered during the wave update docs/skills or become follow-on issues before closeout.
- [ ] `uv run python scripts/validate_ace_wave4_decks_email.py` and `uv run skills/validate_skill.py` pass.

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

- **Risk:** Email archives are high-risk for PII, financial records, client names, and privileged/private context.
- **Risk:** PST/MSG parsing can drop attachments, inline images, encodings, and thread order.
- **Risk:** Keynote conversion may require platform-specific tooling.
- **Open:** #51 must define route targets and #61 must define where private-sidecar extracts, exclusion manifests, and public aggregate summaries are stored.

---

## Complexity

**T3** - multi-format archive lane with privacy triage, attachment recursion, deck-image loss modes, fidelity review, and docs/skills updates.
