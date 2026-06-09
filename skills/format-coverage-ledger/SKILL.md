---
name: format-coverage-ledger
description: >
  Runs the right deterministic extraction lane per office/email format and records
  each format's KNOWN losses UNDER A TEXT/CSV LANE in a coverage ledger so a
  faithful extract never masquerades as complete. Use when extracting
  docx/xlsx/msg/pdf/pptx sources whose richest content (formulas, charts, diagrams,
  attachments, images, speaker notes) does not survive a text/CSV dump.
license: CC-BY-4.0
compatibility: Requires per-format deterministic extractors (python-docx/openpyxl/MSG reader/pdf text/pptx reader), a corpus-root env var, and per-batch manifests
metadata:
  version: "1.0"
  enforcement_level: L2            # callable extraction + a ledger the page must carry
  status: template
  incident_refs: silent-completeness-gap,formula-loss,diagram-loss,attachment-drop
  params: "path:str | format:enum(auto,docx,xlsx,msg,pdf,pptx)=auto"
---

# format-coverage-ledger

> Template skill (doc 09, doc 02, complements `source-extraction-coverage`). Each
> office/email format hides its most valuable content in a layer that a naive
> text dump silently discards. A faithful extract is **not** a complete one. This
> skill pairs a deterministic per-format lane with an explicit **coverage ledger**
> that names what was *not* captured, so the gap is recorded against the page
> instead of being discovered later as a surprise.

## Trigger
`/format-coverage-ledger <path> [--format auto|docx|xlsx|msg|pdf|pptx]`

## Preconditions
1. The corpus root is referenced via an **env var** (e.g. `$FDAS_CORPUS`), so no
   host mount path is ever committed; the extractor reads `$ROOT/<relpath>`.
2. Format is detected by content/structure, not filename (names lie).
3. Each batch carries a **manifest**; one reusable extractor, per-batch manifests.

## Steps
1. **Route to the deterministic lane** (one extractor, format-dispatched):
   - **docx → txt** (python-docx): paragraphs + tables.
   - **xlsx → csv per sheet** (openpyxl), `data_only=True` so cells hold the
     **computed values** — note this means **formulas are not captured**.
   - **msg → txt thread** (MSG reader): the message thread text.
   - **pdf → txt**: deterministic text layer.
   - **pptx → txt**: slide text + tables.
2. **Record the coverage ledger (mandatory).** In the page (a `completeness`
   field or a coverage/status section — the campaign used a body status section),
   state per this format what was captured AND what was **not**, from the
   text/CSV-lane known-loss table:

   | Format | Captured (text/CSV lane) | KNOWN loss of this lane (record it) |
   |---|---|---|
   | xlsx | computed cell values (`data_only`) | **formulas, named ranges, charts/plots** |
   | pptx | slide-shape text + tables | **diagrams, plots, drawn figures, speaker notes** (often the engineering content) |
   | msg | message thread text | **attachments** (dropped) |
   | docx | text + tables | **embedded images/figures** |
   | pdf | text layer | **images/figures/scanned regions** |

   (These are losses of *this lane*, not of the libraries — openpyxl can read
   formulas, extract-msg can read attachments, etc.; a richer lane recovers them.)

3. **Provenance on every value.** Each extracted value carries
   `corpus-relative-path + sha256` (the source pointer). Raw binary never
   committed — derived text/CSV + pointer only.
4. **Flag the gap as backlog, not done.** A page whose lost layer is where the
   value lives (e.g. an xlsx that is a calculation tool → formulas lost; a pptx
   that is engineering plots → diagrams lost) is marked
   `completeness: partial` and queued for a richer lane (formula-graph extraction,
   image/diagram capture, attachment harvesting), not silently shipped as
   complete.

## Verification
- Every extracted page declares a coverage ledger naming the lane's known loss;
  a reviewer rejects a page that omits it (a frontmatter-field validator is the
  L2 hardening to add — the FDAS campaign enforced this by review, not yet a check).
- No host mount path appears in any committed file (the corpus root is an env
  var); grep the diff to confirm.
- Every value has a `corpus-relative-path + sha256` pointer; raw binary absent.

## Cleanup
- Raw binary stays in the temp/off-repo location; only derived parts + pointers
  persist. Manifests are not committed as corpus content.

## Incident appendix
| Rule | Why |
|---|---|
| Coverage ledger is mandatory | A faithful text extract silently hid that xlsx formulas / pptx diagrams / msg attachments were never captured |
| xlsx data_only loses formulas | Computed values ≠ the calculation; the formula layer is usually why the file exists |
| pptx loses diagrams/plots | The engineering content is often the drawn figure, not the slide text |
| Corpus root via env var | No host mount path is ever committed; the corpus is relocatable and private |
| Partial ≠ done | A page whose lost layer holds the value goes to the richer-lane backlog, not the trusted set |
