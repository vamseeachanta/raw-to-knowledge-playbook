# Corpus Lifecycle: Incremental Re-Ingestion & Freshness

A corpus is not a build artifact you produce once — it is a **living dataset
under a slow stream of edits**: new standard editions, watermark-free
re-releases, corrections to verified tables. This doc makes freshness a
first-class concern. The creed extends with one extra clause: **re-ingestion
resets trust rather than inheriting it.**

Research and primary sources for every claim here: **issue #17**.

> Thesis: *make supersession an append, never a delete; make invalidation a
> function of a hash-keyed dependency graph; and bound re-verification by what
> actually changed, not by the calendar.*

## 1. Change detection — content-hash docstore, two-level identity

The settled mechanism: a **content-hash docstore** maps a stable `doc_id` to the
hash of its content; re-ingestion compares hashes to decide skip vs reprocess
(LlamaIndex `IngestionPipeline`'s `DocstoreStrategy` is the borrowable pattern —
the pattern, not the framework). The docstore must be **persisted across runs**
or every run looks new.

What a bare hash *cannot* distinguish is the hard case, which needs different
downstream policy:

| Event | Identity signal | Policy |
|---|---|---|
| **New edition** (API RP 2A 21st→22nd) | same logical key, *new* edition | new logical doc in a supersession chain; prior edition stays queryable |
| **Same edition re-released** (watermark stripped, re-OCR'd) | same logical key + edition, new hash | same logical doc, new revision; **reset trust to provisional** |

So use a **two-level identity**: a *logical document key* (`API-RP-2A-WSD:22` =
standard number + edition) separate from the *physical content hash*. Edition is
parsed from metadata/title — and because edition parsing is itself a fallible
extraction step (the corpus's own "year false-positive → need a standard-#
registry" lesson), **edition identity must be vision/human-confirmed, not
regex-trusted.**

## 2. Supersession — keep the citation trail (append, never mutate)

The right prior art is **bitemporal modeling** (valid time + transaction time),
not a soft-delete flag:

| Design | Citation trail | "What did we believe when" | Verdict |
|---|---|---|---|
| Soft-delete (`is_deleted`) | partial | no — overwrites lose history | insufficient |
| Tombstone | no (after vacuum) | no | only for true *retraction* (licensing takedown) |
| **Version-chain / bitemporal** | **yes** | **yes** (as-of queries) | **recommended** |

A verified page/table is **never mutated in place.** A correction or supersession
**appends** a new version row carrying `supersedes: <prior_version_id>`, an
effective interval, and a fresh `parse_status` reset to `provisional-unverified`
on any content change. The old citation still resolves — it now also reports
"superseded by vN." This is the doc-07 provisional-by-default model extended along
a time axis. Transaction time is append-only — the audit spine; valid time is
mutable — supports retroactive correction.

## 3. Cascade invalidation — re-run the downstream closure, always including verify

A dependency-graph + hashing problem. The derived-artifact DAG per source:

```
source file (hash) → extracted text/tables → chunks → embeddings
                                           ↘ vision-verifications
                                           ↘ ported Excel/solver code
```

Key each derived artifact on a **hash of its direct inputs** (DVC `dvc.lock`
style); on a source change, re-run strictly the **transitive downstream closure**
of the changed node (dbt `state:modified+`, Pachyderm datum-incrementality are the
reference models — study, don't adopt the warehouse/k8s-shaped tools). The
invalidation contract:

| Change | Re-run | Keep |
|---|---|---|
| New edition | full pipeline on new edition | old edition's artifacts (audit) |
| Re-release, extracted text **identical** | nothing | everything |
| Re-release, text **changed** | re-chunk changed regions → re-embed changed chunks → **reset verifications to provisional** | unchanged chunks/embeddings |
| Verified table corrected | that table's verification + any code derived from it | unrelated tables |

The creed forces one edge most pipelines omit: **a content change must invalidate
the *verification*, not just the embedding.** Re-embedding is cheap and automatic;
a stale `verified` flag on changed content is a fidelity lie. **Always include the
verification node in the invalidation closure — fail closed on trust.**

## 4. Cost of freshness — bound the blast radius

The blast radius of an edit is set by **chunking stability**. With
**content-defined chunking** (FastCDC-style, boundaries set by a rolling hash over
content, not fixed offsets), a small correction perturbs only chunks *near* the
edit; with fixed-size offsets, a one-line insertion shifts every subsequent
boundary and forces a **full document re-embed**. Prefer content-stable boundaries
specifically to bound re-embedding cost.

But re-embedding is *not* the expensive part of this pipeline — **vision
re-verification is** (human/LLM-in-the-loop). So freshness cost is really a
re-verification-cost question, and the answer is **event-driven**:

- **Re-verify only when a page/table's source content hash changes.** A pure
  re-release with identical extracted text needs **zero** re-verification.
- **Full rebuild only when** (a) the **embedding model changes** (all vectors must
  regenerate — you cannot mix embedding spaces) or (b) measured ANN recall
  degrades. Otherwise always incremental.

> The quantitative "10–15% reprocessing" / "$500→$45" figures circulating online
> rest on a single preprint and blogs — directionally adopt, but run a repo-local
> micro-benchmark before publishing numbers. (Marked UNVERIFIED in #17.)

## 5. Edition-aware retrieval — one index, metadata filter

Return the **current edition by default, keep superseded editions queryable for
audit** — via **metadata-filtered retrieval on one index**, never a "latest" vs
"archive" index split (a split desyncs and breaks citation resolution). Each chunk
carries `logical_doc_key`, `edition`, `is_current`, `valid_from/until`,
`supersedes`. Default query applies `is_current = true` (or a recency prior); an
explicit as-of/audit mode drops the filter.

A simple **recency prior reliably picks the latest document** (reported accuracy
1.00 on freshness tasks). Its *limit* is load-bearing: heuristics **cannot** reason
about how a requirement *evolved* across editions — "explain what changed between
the 21st and 22nd edition" is a diffing/analysis task, **not** a metadata-filter
problem, and must not be promised as one.

## Tooling verdicts (feed into doc 12)

| Tool / pattern | License | Verdict | Why |
|---|---|---|---|
| LlamaIndex `IngestionPipeline` docstore | MIT | **ADOPT the pattern** | content-hash skip/reprocess/delete — the incremental-ingest spine |
| DVC (stage-hash invalidation) | Apache-2.0 | **ADOPT as reference / optional** | `dvc.lock` hashing + run-cache |
| dbt `state:modified+` | Apache-2.0 | **STUDY the pattern** | DAG-downstream selection; tool is warehouse-shaped |
| Pachyderm (datum + provenance) | Apache-2.0 | **STUDY, don't adopt** | heavyweight (k8s); momentum slowing post-acquisition |
| Bitemporal / SCD-Type-2 model | pattern | **ADOPT the model** | valid+transaction time in your own metadata, no DB dependency |
| FastCDC / content-defined chunking | algorithm | **ADOPT the principle** | content-stable boundaries bound re-embed blast radius |

## Candidate practices (need a pilot before minting as a GP)

- **Two-level identity:** logical key (standard# + edition, vision-confirmed) vs
  physical content hash — distinguishes supersession from revision.
- **Supersede-by-append:** new version row + `supersedes` pointer + reset
  `parse_status=provisional`; never UPDATE/DELETE a verified artifact in place.
- **Hash-keyed cascade invalidation:** re-run the transitive downstream closure of
  any changed node, **always including the verification node**.
- **Content-stable chunk boundaries** (FastCDC-style) to keep re-embedding
  proportional to the edit.
- **Event-driven re-verification:** re-verify only on source-hash change; identical
  re-release ⇒ zero re-verification.
- **Single-index edition-aware retrieval:** `is_current` default + as-of override;
  never a latest/archive split.

*Snapshot 2026-06. Full primary-source citations and the UNVERIFIED-figure
caveats: issue #17.*
