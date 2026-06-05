# Imagery & Scanned Documents: Describing What Can't Be Parsed

The raw archive contains sources with **no text layer at all**: photographs
(site/facility/equipment evidence, survey imagery) and scanned documents
(legacy reports, drawings, faxed standards). These are the inverse of every
other lane: extraction cannot *copy* anything — it must **describe**, and a
description is an interpretation, not source data. That distinction drives
everything below.

## The trust inversion

| Lane | Extraction output | Trust class |
|---|---|---|
| Born-digital PDF / Office / CSV | Copied content (deterministic) | Faithful by construction; values still verified |
| Scanned document | OCR text | **Interpretation** — character-level guesses |
| Photograph | Vision-generated description | **Interpretation** — model's reading of a scene |

So while other lanes mark *parsed structure* provisional, this lane marks
the *entire extraction* as interpretation. Frontmatter must say so
(`extraction_policy: described` / `ocr-interpreted`), and downstream
consumers must never cite a description as if it were the source.

## 1. Photographs (the description lane)

A photo's value is rarely the pixels — it's the **claim the photo
evidences**, anchored in metadata. Ingestion therefore produces a
*description record*, not just a caption:

```yaml
---
source_image: <archive filename>          # raw file stays off-repo
captured: <date/time>                     # EXIF or documented
location: <site/coordinates if known>
capture_context: <who/why, if known>
extraction_policy: described
described_by: <model + date>
---
description: >
  <what is visibly present — objects, conditions, text legible in frame>
observations:
  - <specific, falsifiable statements: "corrosion visible on flange face">
legible_text: ["<any text readable in the image, transcribed verbatim>"]
uncertain: ["<what the describer could not determine>"]
```

Rules (carried over from adjacent verified practice):

- **Describe falsifiably.** "Equipment appears damaged" is unreviewable;
  "paint loss and surface rust across ~30% of the visible beam flange" can
  be checked against the image. The same specific-evidence rule that
  settles conflicting table verdicts (GP-10) applies to descriptions.
- **Separate observation from inference.** What is *in frame* vs what it
  *implies* are different fields; inference goes into analysis pages, not
  the description record.
- **Transcribe legible in-image text verbatim** (nameplates, signage,
  gauges) — it's the only deterministically checkable part of the record.
- **Timelines beat single images.** For condition/evidence use cases, the
  asset is a *dated series* (same subject, repeated capture); a description
  record per frame plus a series index. Review what already exists in the
  archive before capturing or ingesting new imagery — duplication wastes
  both capture and description effort.
- **Tables/figures photographed or pasted as images** (in decks, in field
  reports) route here too — same as PDF figure handling: caption/describe,
  queue for the vision lane, never pretend a pixel table is data.

### Verification

A second, independent vision pass spot-checks descriptions the same way
table batches are spot-checked: adversarial stance, exact-file anchoring,
verdicts with falsifiable specifics. Descriptions that conflict get the
GP-10 treatment.

## 2. Scanned documents (the OCR lane)

A scan is a photograph of a document. The pipeline:

1. **Detect** — the word-count gate (GP-04) catches image-only PDFs;
   route them here instead of letting them paginate noise into the wiki
   (a 73-page garbage ingest taught this).
2. **Decide depth by value** — most scans deserve L0 (metadata stub +
   source pointer). OCR is spent only on documents whose content justifies
   interpretation-grade text.
3. **OCR with explicit trust labeling** — output is L1-equivalent text
   marked `ocr-interpreted`, never `raw-extracted`. Declare an
   `extraction_estimate` before and record `extraction_yield` after (the
   estimate/yield pair is how shallow extraction gets caught).
4. **Tables in scans are the worst case** — OCR'd tables combine every
   class-A defect (digit substitution, row collapse, column drift) with no
   deterministic fallback. They enter the verification queue like any other
   table, but expect rejection rates far above born-digital sources; for
   high-value scanned tables, manual digitization with vision verification
   is usually cheaper than OCR repair.
5. **Engineering drawings** are imagery, not documents: describe the
   drawing (title block verbatim, revision, what it depicts), don't OCR the
   field of the sheet.

## Excel, one more split (cross-reference)

The same describe-vs-extract logic clarifies the Excel population
([doc 09](09-office-formats.md)):

| Variant | Nature | Lane |
|---|---|---|
| **Data Excel** (exports, logs, datasets) | Born-structured content | Parse like delimited data ([doc 10](10-structured-data-and-model-files.md)): dialect/layout probing, convention sidecar |
| **Calculation Excel** (engineering workbooks) | Live logic | Formula graph → code with round-trip traceability (doc 09) |
| **Excel-as-canvas** (pasted screenshots, image-heavy sheets) | Imagery in a spreadsheet skin | This lane: describe, don't parse |

Classify by *scanned structure* (formula density, image count, function
mix), not by filename — names lie (failure D4).
