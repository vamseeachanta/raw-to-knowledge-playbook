# CAD Geometry & 2D Drawings: STEP/IGES, Native Parts/Assemblies, DWG/DXF

Beyond documents (docs 01–04), live Office artifacts (doc 09), machine
text (doc 10), and imagery (doc 11), an engineering archive holds a fifth
population: **binary CAD geometry** — boundary-representation (B-rep)
solids, multi-part assemblies, and 2D vector drawings, mostly in
**vendor-proprietary, Windows-only** formats. They look inert ("just open
it in a viewer") and that is the trap: the danger here is **license-lock**
(you can't read the native format without a paid seat) and **silent
geometry loss** (a conversion "succeeds" but drops solids, units, or the
assembly tree).

In the D1/D2/D3 dimension model ([doc 09](09-office-formats.md)):

| Source | D1 content | D2 logic | D3 format |
|---|---|---|---|
| Native part / assembly (vendor binary) | **primary** — geometry + metadata | **the parametric feature tree IS engineering decisions** (like a solver deck) | proprietary binary, version-locked |
| Neutral 3D (STEP / IGES / Parasolid) | **primary** — geometry (+ structure for STEP) | n/a | ISO/neutral; STEP is ASCII, header-declared schema |
| 2D drawing (DWG / DXF) | **primary** — geometry, dimensions, title-block, revisions | n/a | AutoCAD-version binary (DWG) or ASCII (DXF) |

---

## 1. Native formats are license-locked — design the extraction/run split

The single most important fact: **the most valuable models are the least
readable.** In a real estate scan, native SolidWorks/Inventor parts and
assemblies dominated the population, yet **no open-source library could read
them** — every candidate "native reader" claim failed verification; only a
commercial SDK or the originating vendor seat opens them. Neutral formats
(STEP/IGES/Parasolid) read headless and license-free via an OSS CAD kernel.

This is the same principle as solver decks ([doc 10 §License-independence](10-structured-data-and-model-files.md)):

- **Extraction (read geometry, metrics, structure)** must run **license-free
  and headless** — on neutral formats, in CI, on any machine.
- **The unlock (native → neutral export)** is the one **seat-gated** step:
  a one-time vendor-seat batch export of the native estate to STEP. Run once;
  everything downstream is then license-free forever.

Don't confuse "I imported the vendor API" with "this runs in CI." Native
read does not; neutral read does.

## 2. Header-detect format and version — never trust the extension

"It's a CAD file" is a claim, not a property — confirm it from bytes:

- **DWG** carries a 6-byte version code in its first bytes (`AC1014` = R14,
  `AC1032` = 2018); a real archive spanned ~25 years (R11→2018). Conversion
  fidelity and tool choice depend on the version, not the `.dwg` suffix.
- **STEP** declares its schema in the `FILE_SCHEMA` header
  (`CONFIG_CONTROL_DESIGN` = AP203, `AUTOMOTIVE_DESIGN` = AP214,
  `AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF` = AP242). The header also
  names the **originating CAD system and version** — free provenance.
- **Generic extensions lie.** In one scan, every `.nc` file was **NetCDF**
  (hydrodynamics output), not CNC G-code — extension-based classification
  would have reported a non-empty CAM inventory that does not exist. `.dat`
  was solver-input *or* generic data. Resolve ambiguous extensions by content.

## 3. Geometry conversion is lossy — gate on a round-trip invariant oracle

A conversion that "opens in a viewer" can still have dropped solids or
collapsed units. The verifier is a **round-trip invariant comparison**:

- Re-read the converted master and compare **solid-body count, bounding box,
  and volume/mass** against the source within tolerance. A real STEP→STEP
  round-trip was confirmed lossless only this way (Δbbox 0, volume rel-err
  ≤1e-6) — not by a "file written" check.
- **Surface-only formats fail silently.** IGES re-read as **0 solids /
  unoriented surfaces**, yielding a meaningless (negative) volume. It carries
  shape for *exchange* but is not a solid until **sewn** (an explicit
  ShapeFix/sewing step) — prefer STEP, and never compute mass from raw IGES.

## 4. The model is the deck — parse to config, regenerate variants

A parametric CAD model is D2 logic exactly like a solver deck ([doc 10 §2](10-structured-data-and-model-files.md)).
The anti-pattern observed in the wild: a single part whose only real variable
was a count (e.g. a tank's compartment number) saved as **6+ independently
hand-built assemblies**, each with its own redone drawings and mass tables;
and the same sub-assembly re-saved per load-case and per revision. Every
downstream artifact was redone by hand per variant.

The fix mirrors deck→config: capture the engineering parameters in a
**config**, drive a parametric model from it, and **generate** variants
rather than re-modeling them. The hand-built copies become build artifacts.

## 5. The assembly tree is not free — use the structured reader

A basic CAD kernel STEP reader **flattens** assemblies: a sub-assembly whose
file declared **11 products** surfaced as **2 merged solids** through the
simple reader. To recover the **assembly/BOM tree, part names, and colors**
(the thing a BOM or a parts-register needs), use the kernel's **structured
(XCAF-style) reader**, not the flat one. Counting solids ≠ reading the BOM.

## 6. Provenance & assumption ledger — units and material are not in the file

Geometry without convention is a sign-flip waiting to happen ([doc 10 §Conventions are data](10-structured-data-and-model-files.md)).
Every extracted asset carries a **sidecar**: source file + hash, originating
CAD system/version (from the STEP header), schema (AP203/214/242), **units
assumption** (CAD is usually mm but the file rarely says), **material/density
assumption** used for any mass figure, and coordinate frame. Defaults
(assumed-steel, assumed-mm) are an **assumption ledger** — *surfaced, never
silent*. A mass number with an invisible density assumption is a future bug
report.

---

## What "verified" means in this lane

| Sub-lane | Verifier |
|---|---|
| Native part/assembly | Round-trip after the seat-gated STEP export (§3); native read is *not* CI-runnable, so the export itself is the trust boundary |
| Neutral 3D (STEP/Parasolid) | Round-trip invariant oracle: solid-count + bbox + volume/mass within tolerance; XCAF tree vs file `PRODUCT_DEFINITION` count |
| IGES / surface formats | Same oracle **after sewing**; reject volume/mass from un-sewn surfaces |
| 2D drawing (DWG/DXF) | Header version detected; layer/block/entity census vs an independent read; title-block/revision captured |

Same trust model as every other lane: **nothing is trusted because it
opened.** Geometry is a hypothesis the round-trip oracle must confirm.

---

*Worked instance.* The methodology in this lane was distilled from a CAD/CAM
estate-discovery and a license-free extraction pilot (a public engineering
library's `docs/cad-inventory/` set: inventory → ecosystem/automation surface
→ a STEP-AP242-master + glTF/3MF/DXF pipeline validated headless on real
B-rep files). The license-verified OSS tooling for this lane is in
[doc 12 (tooling landscape)](12-tooling-landscape.md); governance of the
extracted paths and any leak vectors is in [doc 07](07-data-governance.md) /
[doc 18](18-security-and-pii.md) / [doc 19](19-trust-boundary-and-private-mode.md).
