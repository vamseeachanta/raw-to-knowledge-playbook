# Case study — structured / solver / geospatial coverage sweep

> Worked example behind the [`format-coverage-ledger`](../../skills/format-coverage-ledger/SKILL.md)
> skill and [doc 10](../10-structured-data-and-model-files.md). It **extends**
> the [mixed-office format-coverage audit](format-coverage-audit.md) — which
> scored a live Office archive — into a different population: CSV / position
> tracks, KML/KMZ geospatial, and solver ASCII/binary (GHS, AQWA, and similar
> hydrodynamics / stability packages). Same central claim, restated for this
> population: **a text-readable file is not an answer-bearing one**, and the gap
> is widest exactly where the engineering value is densest.
>
> **Abstraction note (dogfooding [`public-private-routing`](../../skills/public-private-routing/SKILL.md)).**
> The swept corpus is a private client archive. This case study reports only the
> **method and the aggregate / per-format findings** — no document names, no
> project or job codes, no vessel names, no mount paths, no per-document table,
> no corpus identity. The lesson is public; the corpus stays private.

## Setup

Where the sibling audit re-opened every binary to *score* completeness, this
sweep asks a cheaper, earlier question: across a structured/solver/geospatial
population, **which files can a zero-setup text lane read RIGHT NOW**, and which
need tooling we have to stand up first? The answer drives a re-ingest ordering,
not a grade.

The population here is not Office documents but the third population of
[doc 10](../10-structured-data-and-model-files.md): delimited data and position
tracks (CSV/TXT), geospatial overlays (KML/KMZ), and the ASCII/binary
input/output files of analysis solvers (hydrostatics, stability, hydrodynamic
diffraction/radiation, CFD). These *look* easiest — "it's already structured" —
and that is exactly what makes their failure modes silent.

## The tier model (structured / solver / geo population)

Each source is routed into a readiness tier by **what tooling its content
actually requires**, decided by probing bytes, not by trusting the extension:

| Tier | Label | Tooling needed | Examples in this population |
|---|---|---|---|
| **A** | **readable now** | nothing beyond a text/CSV reader + encoding probe | text CSV, delimited position tracks, KML (text XML), solver **output listings** in plain ASCII, scope / notes / readme `.txt` |
| **B** | **needs rasterizer** | image/vision lane + **Poppler (`pdftoppm`) HARD PREREQUISITE** (see [doc 12](../12-tooling-landscape.md)) | scanned/image-only PDF result sheets, plotted-figure PDFs |
| **C** | **needs Office reader** | python-docx / openpyxl / pptx readers (the sibling audit's lanes) | `.xlsx` result workbooks, `.docx` reports, `.pptx` decks |
| **D** | **needs solver / CAD tooling or transcode** | solver-native reader, CAD reader, unzip, or encoding transcode | binary solver models / print files, UTF-16 solver exports, CAD geometry (DWG / 3dm / STEP), zipped **KMZ** |
| **E** | **media** | A/V pipeline (out of scope here) | photos, video, audio walkthroughs |

Tier A is the harvestable-today set; Tiers B–E are a tooling backlog. The
sweep's job is to fill Tier A in one pass and route everything else honestly.

## The inventory-sweep method

The corpus already had a **per-source inventory** built by the
[`source-extraction-coverage`](../../skills/format-coverage-ledger/SKILL.md)
campaign (one row per file: corpus-relative path, extension, size, sha256).
Rather than re-traverse slow, networked storage to find the easy wins, the
sweep **greps that existing inventory** for Tier-A text extensions
(`.csv`, `.txt`, `.kml`, and ASCII solver-output suffixes) and enumerates every
zero-setup candidate in a single local pass.

This is the cheap-first move: the inventory is already paid for, it lives on
fast local disk, and grepping it costs nothing — whereas re-walking the network
mounts to rediscover the same files would be the dominant cost. The sweep then
runs a **per-file content probe** only on that short-listed set to confirm the
tier before promoting anything.

## Honest-partial outcomes — files that looked Tier A but degraded

The grep finds *candidates*; the probe demotes the liars. Each of the following
matched a Tier-A extension and degraded on inspection — and each was marked
`partial` / re-tiered, **never silently trusted as a result**:

| Looked like (by extension) | Probe found | Re-tiered to | Why it degraded |
|---|---|---|---|
| solver `.TXT` result listing | a **run-script** / report-definition that *generates* results — the computed numbers live in a binary print file + PDF, not in this file | A → D/B | extension-shared with real output listings; classify by first lines (results banner vs run commands), not suffix |
| solver `.dat` deck | **UTF-16 / binary** export with embedded NUL bytes (a tool-generated export, not a hand-edited ASCII deck) | A → D | "solver ASCII" is often not ASCII; needs an encoding probe + transcode |
| `.kml` named "course" | a **re-plot of a position track**, not a channel centerline / planned route | A (but mislabelled) | the name asserts intent the geometry does not carry; capture what it *is*, not what it's called |
| `.kmz` | a **zipped** KML container | A → D | needs unzip before any text lane can touch it |
| bare-geometry `.txt` point list | clean `x y z` columns with **no header, units, datum, or sign convention** in-band | A, but `partial` | parses perfectly, means nothing alone — needs a convention sidecar (see doc 10) |

The pattern: a Tier-A *extension* is a hypothesis, not a verdict. The probe is
what makes the tier real.

## The lesson — inverse value, restated for solver / geo / CAD

The sibling audit found that completeness ran **inverse to document value** —
text extraction was weakest precisely where the information was densest. This
sweep confirms the same shape in a population that *looks* friendlier to text:

- **Text lanes reliably yield the periphery:** SETUP and model parameters,
  geometry-**point** lists, scope/assumption notes, and recorded position
  tracks. These are genuinely Tier A.
- **The COMPUTED RESULT TABLES are not in the text lane.** Hydrostatics tables,
  hydrodynamic RAOs / added-mass / damping matrices, CFD force histories, and
  stability pass/fail verdicts live in binary print files (`.PF`-class),
  result PDFs, and `.xlsx` workbooks — Tiers B / C / D.

So **text-readable ≠ answer-bearing.** A clean three-column point dump and a
plain-ASCII run header are real, harvestable wins — but they are the inputs and
the scaffolding around the answer, not the answer. The high-value computed
output is exactly the layer the text lane cannot reach, the same inversion the
Office audit measured.

This is why the tier is a **prioritized re-ingest backlog**, not a score: it
tells you that filling Tier A is fast and incomplete, and that the solver /
rasterizer / Office / unzip tooling for Tiers B–D is where the answers are.

## Reproduce / method

1. **Build (or reuse) a per-source inventory** via
   [`source-extraction-coverage`](../../skills/format-coverage-ledger/SKILL.md):
   one row per file — corpus-relative path, extension, size, sha256. Keep it on
   fast local disk.
2. **Sweep for Tier-A candidates in one local pass** — grep the inventory for
   text-tier extensions instead of re-walking slow/networked storage:

   ```
   grep -iE '\.(csv|txt|kml)$' inventory.tsv        # text-tier extension shortlist
   ```

   Add the ASCII solver-output suffixes your solvers emit.
3. **Probe each candidate before promoting it** (the demotion step):
   - read the **first lines** — solver *output listing* (results banner) vs
     *run script* (report-definition commands); route on content, not suffix.
   - run an **encoding probe** — BOM / UTF-16 / NUL detection; a "solver `.dat`"
     that is UTF-16/binary is Tier D, transcode before parse.
   - for `.kmz`, treat as **zipped** → Tier D (unzip first).
   - for bare `x y z` point dumps, require a **convention sidecar** (units,
     datum, sign) before promoting past `partial`.
4. **Record the tier + known loss in the coverage ledger** (mandatory):
   anything that degraded is marked `partial` / re-tiered and queued for its
   richer lane — never shipped as a trusted result.

Cross-links: [doc 10 — structured data & model files](../10-structured-data-and-model-files.md),
the [`format-coverage-ledger`](../../skills/format-coverage-ledger/SKILL.md)
skill, and the sibling [format-coverage audit](format-coverage-audit.md).
