---
name: independent-oracle-validation
description: >
  Scores committed extracts against an independent extraction engine (a
  different codebase than the pipeline lane) to produce measured per-lane
  precision/recall, with two-tier numeric scoring and a hard rule that every
  sub-1.0 number is attributed to a named cause. Use when a conversion lane
  needs correctness evidence beyond the fidelity verify loop — turning "we
  believe the extracts are faithful" into per-lane measured numbers.
license: CC-BY-4.0
compatibility: Requires per-lane oracle engines on the host (e.g. office-suite headless conversion, a second PDF text engine, raw container-XML reads, an alternative format library), the committed extracts, and the corpus binaries (or verified cache)
metadata:
  version: "1.0"
  enforcement_level: L2            # callable scoring tool + report the matrix cites
  status: template
  incident_refs: comparator-inflation,prose-overclaim,silent-completeness-gap
  params: "out:str=- | corpus_env:str=CORPUS_ROOT"
---

# independent-oracle-validation

> Template skill (doc 03, doc 05 GP-47). The per-batch verify loop proves
> **fidelity** — the extract matches what the pipeline read. It cannot prove
> **correctness**: the pipeline and its verifier can share a defect. This
> skill adds the missing leg: re-extract the same sources with a *different
> engine* and score the committed extracts against it. In the pilot (11 docs,
> 6 office lanes) the measured numbers were 1.000/1.000 for data and deck
> lanes, with every sub-1.0 residual resolving to a named cause — including
> one previously unledgered real lane loss (render-time list numbering) that
> no amount of self-consistent verification would ever have surfaced.

> **The comparator is the trap.** The pilot's scoring tool needed FOUR
> adversarial review rounds — all on the comparator, none on the pipeline:
> its "exact" tier silently rounded numerics three different ways before
> canonicalization was precision-lossless *by construction*. A flattering
> comparator bug poisons every downstream number, so the scoring tool gets
> the verify loop at higher rigor than the lane it scores.

## Trigger
`/independent-oracle-validation [--out report.md]`

## Preconditions
1. **Oracles are a different codebase than the lane**, per format — e.g.
   office-suite headless conversion vs a python reader; a second PDF text
   engine; raw container-XML text nodes vs an object-model library; an
   alternative implementation of the same format. Where independence is
   partial (two libraries sharing a container parser), the report says so
   explicitly — shared layers prove less.
2. The committed extracts and the source binaries (or a hash-verified cache)
   are available; the corpus root comes from an env var, never a committed
   path.
3. The comparison is reproducible: same inputs → byte-identical report.

## Steps
1. **Re-extract with the oracle** per document, into a temp dir only (the
   raw-binary firewall applies to oracle conversions too).
2. **Normalize formatting, never precision.** Strip currency symbols,
   thousands separators, display percent signs, accounting negatives —
   transformations that are provably formatting-only. Numeric
   canonicalization must be precision-lossless at ANY digit count (decimal
   with width-matched context, not binary float, not bounded-precision
   normalize). Cell-only equivalences (accounting `-` = 0) never apply to
   prose tokens.
3. **Score two tiers** of multiset precision/recall per document: **exact**
   (formatting-normalized) and **display-tolerant** (e.g. 3 significant
   figures), because oracles that export *displayed* values legitimately
   disagree with lanes that store full precision. Report both; never let the
   tolerant tier masquerade as exact.
4. **Strip only your own scaffold** from the lane side (structural markers,
   provenance headers, additive inventories) — positionally, so look-alike
   content inside the document body is preserved. Scaffold is your addition;
   body content the oracle also sees is not.
5. **Attribute every sub-1.0 number.** Diff the bags; each residual class
   resolves to exactly one of: a **real lane loss** → record it in the
   coverage ledger; a **legitimate engine difference** → caveat it in the
   report; a **comparator bug** → fix the comparator and re-run. Never
   adjust a score without naming its cause.
6. **Run the adversarial verify loop on the comparator** (skill
   `adversarial-verify-loop`), instructing reviewers to hunt score-inflating
   normalization collapses with constructed probes. Loop until PASS.
7. **Publish the report** (tool versions pinned, caveats included) and cite
   the measured numbers from the lane-maturity matrix — scoped honestly:
   value/token overlap complements, never replaces, information-capture
   completeness estimates or ordering checks.

## Verification
- Re-running the tool reproduces the committed report byte-for-byte.
- Every sub-1.0 number in report and matrix has a named, probe-verified
  attribution.
- The comparator has its own PASS-terminated adversarial review record.
- Oracle conversions never wrote inside the repo tree.
- Published oracle reports and review evidence pass
  `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces`; use
  `--diff-only` before committing local report changes.

## Cleanup
- Oracle conversion outputs and probe scripts stay in temp/session dirs;
  only the report and the scoring tool are committed.

## Incident appendix
| Rule | Why |
|---|---|
| Oracle from a different codebase | Same-engine re-runs prove reproducibility, not correctness |
| State partial independence honestly | Two readers sharing a container parser prove less than two unrelated engines |
| Precision-lossless exact tier, by construction | Three successive "fixes" each handled only the probed case; bounded-precision contexts still rounded |
| Two tiers, both reported | Display-rounding is a legitimate engine difference; hiding it in "exact" inflates, splitting it attributes |
| Attribute every sub-1.0 number | One residual was a real, previously unledgered lane loss; the rest were engine formatting — only the diff probe tells them apart |
| Verify the comparator harder than the pipeline | A flattering comparator bug poisons every number it produces |
| Scaffold stripped positionally | Prefix-stripping by pattern ate body content that looked like scaffold (quoted-history subject lines) |
