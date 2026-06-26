# Contribution batch — structured-data / solver / geospatial coverage (2026-06)

Four evidence-backed contributions distilled from a real private ingestion campaign that
applied this playbook to a heterogeneous engineering archive (CSV/position-tracks, KML/KMZ,
GHS/AQWA solver files, plus the usual PDF/Office/CAD). Written **abstraction-by-default** per
[`CONTRIBUTING.md`](../../CONTRIBUTING.md) §4 and the `public-private-routing` skill — method and
aggregate findings only; **no client/corpus identifiers**.

These have been drafted directly as doc changes (additive, append-only). This folder is the
**PR plan / issue text**; the actual content lives in the docs below. Nothing here is committed.

| # | Contribution | Lands in | Status |
|---|---|---|---|
| 1 | Solver text files: extension ≠ dimension (output-listing vs run-script); solver "ASCII" is often UTF-16/binary (probe encoding); bare geometry-point files carry no units/datum (sidecar mandatory) | `docs/10-structured-data-and-model-files.md` | drafted |
| 2 | PDF **rasterizer prerequisite** (`pdftoppm`/Poppler) for image/vision lanes + the "reachable ≠ parseable" failure class + license-register row | `docs/12-tooling-landscape.md` | drafted |
| 3 | Two append-only good practices: **probe source readability cheaply before planning**; **sweep the inventory for the text tier before building heavy lanes** | `docs/05-good-practices.md` | drafted |
| 4 | New case study **structured-data/solver/geospatial coverage sweep** (extends `format-coverage-audit` from Office to CSV/KML/solver; tier model, inventory-sweep method, inverse-value lesson) + `format-coverage-ledger` loss-proxy rows | `docs/case-studies/structured-data-geospatial-coverage-sweep.md`, `skills/format-coverage-ledger/SKILL.md` | drafted |

## The core findings (one-liners)
- **Extension ≠ dimension.** A solver `.TXT` may be a result *output listing* or a *run script*
  (inputs) — opposite value. Read the first lines, don't trust the suffix.
- **Solver "ASCII" is often not ASCII.** Workbench exports come out UTF-16/NUL-laden and trip
  text-tool binary guards; hand-written decks of the same solver are plain ASCII. Probe encoding.
- **Bare geometry-point files have no conventions in-band** — `x y z` with no units/datum/sign.
  Convention sidecar mandatory; mark `partial` until resolved.
- **Rasterizer is a hard PDF prerequisite.** Missing `pdftoppm` makes a whole PDF corpus *look*
  unavailable though storage is fine — "reachable ≠ parseable," a failure class of its own.
- **Inverse-value holds for solver/geo/CAD.** Text lanes give setup/geometry/scope/tracks; the
  computed result tables live in binary `.PF`/PDF/`.xlsx`. Text-readable ≠ answer-bearing.

## To file as issues / land as PRs
Per CONTRIBUTING (one practice per PR; adversarial review; update the Good-Practices *Next ID*).
Suggested `gh` (run from this repo):
```bash
gh issue create -R vamseeachanta/raw-to-knowledge-playbook \
  --title "[doc 10] Solver text: extension≠dimension, UTF-16 exports, bare-point conventions" \
  --body-file contrib/2026-06-structured-data-geospatial/README.md --label documentation
# (repeat per contribution, or open one tracking issue + four PRs)
```
May attach to the existing per-format research briefs (Epic #1 → structured-data / PDF) rather
than new issues — maintainer's call.
