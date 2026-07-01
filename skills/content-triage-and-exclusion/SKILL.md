---
name: content-triage-and-exclusion
description: >
  Triages a raw company archive into an ingest set by classifying on content (not
  extension), value-ranking candidates, deduping superseded versions, and hard
  EXCLUDING PII and third-party-confidential material before any extraction. Use
  when starting an ingestion campaign whose source is a messy company repo or
  shared drive full of code, build/venv, agent, and marketing noise.
license: CC-BY-4.0
compatibility: Requires read access to the raw archive and a written exclusion policy (PII classes, third-party-confidential markers); emits an ingest manifest, not copied files
metadata:
  version: "1.0"
  enforcement_level: L2            # callable triage + an exclusion gate that blocks
  status: template
  incident_refs: misfiled-grabbag,pii-leak,third-party-confidential,superseded-dupe
  params: "archive:str | manifest:str"
---

# content-triage-and-exclusion

> Template skill (doc 01, doc 07, doc 18). A raw company archive is a misfiled
> grab-bag: a directory named for one thing holds another, and most of it is
> noise — source code, `venv`/build artifacts, agent scratch, marketing decks.
> Extension and folder name lie. Triage decides **what is even worth ingesting**,
> and — just as important — **what must never be ingested** (PII, third-party
> confidential material). Get this wrong and you either drown the corpus in noise
> or leak something you had no right to publish.

## Trigger
`/content-triage <archive> [--manifest <out.csv>]`

## Preconditions
1. A written **exclusion policy** exists naming the hard-stop classes:
   personal/financial PII (W-9s, payment/bank threads, SSNs, home addresses) and
   third-party-confidential material (a vendor deliverable marked "do NOT send";
   another party's conference/proprietary deck).
2. Triage is **read-only** over the archive; nothing is copied yet — the output is
   a manifest of decisions, not files.

## Steps
1. **Classify on content, not extension/path.** Sample each file's actual content
   to decide what it is. A `.docx` in a folder named "marketing" may be an
   engineering memo; a vendor's deck may sit under your own project dir. Noise
   classes to drop wholesale: source code, dependency/`venv`/build dirs, lockfiles,
   agent/tool scratch, generic marketing collateral.
2. **Apply exclusions FIRST (fail-closed).** Before value-ranking, route any file
   matching the exclusion policy to an `EXCLUDED` bucket with a reason:
   - **PII** → exclude (W-9, payment/bank/wire threads, personal identifiers).
   - **Third-party-confidential** -> exclude (explicit redistribution-forbidden
     markers, another party's proprietary deliverable/deck). When in doubt that
     *we have the right to ingest it*, exclude — confidentiality is fail-closed.
   An excluded file is recorded (path + reason) but never extracted or copied.
3. **Value-rank the remainder.** Score surviving candidates by knowledge value
   (unique engineering content, decisions, data) vs. redundancy/triviality.
   Low-value passes (cover sheets, empty templates, duplicated boilerplate) sink.
4. **Dedup superseded versions.** Group near-duplicates (rev A/B/final/FINAL2,
   email re-forwards) and keep the **authoritative latest**; mark the rest
   `superseded` so the corpus carries one canonical copy, not a version pile.
5. **Emit the manifest.** Write one row per file: classification, value rank,
   keep | superseded | EXCLUDED(+reason). This manifest is the auditable input to
   the extraction lane — extraction only ever reads `keep` rows.

## Verification
- Every EXCLUDED file has a recorded reason and appears in **no** downstream
  extract or commit (grep the corpus for excluded identifiers to confirm).
- No two `keep` rows are content-duplicate versions of the same artifact.
- Extension/path was never the sole basis for a keep/drop decision (spot-check a
  sample of misfiled files).
- Public-surface manifests, reports, and review artifacts pass
  `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces`; local
  closeout uses `--diff-only` before commit.

## Cleanup
- The manifest persists; the raw archive is untouched (read-only). No excluded or
  raw content is copied anywhere.

## Incident appendix
| Rule | Why |
|---|---|
| Classify on content not extension | Archives are misfiled grab-bags; a NEMA dir once held wave-kinematics papers |
| Exclusions applied first, fail-closed | PII (W-9/payment) and third-party-confidential ("do NOT send" vendor deliverable, another party's deck) must never enter the corpus |
| Dedup superseded versions | One canonical copy beats a rev-A/B/FINAL2 pile; supersession is recorded, not guessed |
| Manifest, not copies | Triage is an auditable decision record; extraction reads only `keep` rows |
