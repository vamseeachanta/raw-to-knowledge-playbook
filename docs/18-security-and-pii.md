# Security & PII: The Data-Egress Firewall

[Doc 07](07-data-governance.md) protects *file copies* and *generated content*
(write-time abstraction + publish-time grep). It does **not** yet govern the leak
the creed makes unavoidable: *"Verify with vision"* means **page images leave the
boundary and go to a hosted VLM.** A confidential page sent to a hosted vision
endpoint is a leak the publish-time grep never sees — it happens *upstream* of any
generated text. This doc is that missing gate.

Research and primary sources for every claim here: **issue #19.**

> The hard rule the research forces: detection tools are imperfect *by their own
> admission*, so **the gate must fail closed (route on-prem) on uncertainty, not
> fail open (send to cloud).**

## 1. Detection can't be the gate (it can only add trip-wires)

Microsoft **Presidio** (MIT, maintained) is the obvious PII component — but its own
docs disclaim completeness: *"there is no guarantee that Presidio will find all
sensitive information."* Independent evaluation found it **missed 159 names** on a
domain-specific benchmark. And a technical archive's high-risk entities are exactly
the long-tail ones where recall is weakest: **author/personnel names, site
coordinates (lat/long), facility identifiers, people in photos** — not the
well-covered emails/phones/SSNs.

Load-bearing consequence: **a detector's "clean" verdict is not a permit to
egress.** The gate is driven by the page's *confidentiality classification* (from
the `visibility:`/`client:` frontmatter doc 07 already maintains); Presidio is a
**second, additive trip-wire**, never the sole gate.

**Fail-closed default:** if `visibility: private`/`client:*`, OR the detector trips,
OR the classification is missing/ambiguous → **route on-prem.** Cloud egress
requires an *affirmative* public/cleared classification. "Unknown" routes the safe
way.

## 2. The hosted-VLM egress decision — read the DPA, not the homepage

Be skeptical of "we don't train on your data" headlines. The operative questions:
**is it retained, for how long, can a court compel retention, who is the
processor.** Verified against provider docs (snapshot 2026-06):

| Provider / mode | Trains? | Retention (verified) | Catch |
|---|---|---|---|
| Anthropic Claude API (Commercial) | No | ZDR: not stored at rest; flagged-abuse up to **2 yr** | ZDR covers **inline Messages only** — Files API, Batch (29d), code-execution (30d) are **NOT ZDR-eligible** |
| OpenAI API (business) | No (since 2023-03-01) | abuse logs **up to 30 d**; ZDR by prior approval | court-order caveat ↓ |
| Google Gemini API (Paid) | No | **Search/Maps grounding = 30 d, cannot be disabled** | grounding retention is non-optional |
| AWS Bedrock | No | "does not store" standard | **AWS is the processor** — different DPA chain |

**The caveat that breaks the marketing:** the *NYT v. OpenAI* preservation order
(2025-05-13) compelled OpenAI to *"preserve and segregate all output log data that
would otherwise be deleted"* — overriding 30-day deletion — for API customers
**without** a ZDR agreement (ZDR-API and Enterprise/Edu exempt). The lesson is
structural, not OpenAI-specific: **a "30-day deletion" promise is defeasible by
litigation hold; only data that is *never stored* (ZDR / on-prem) is robust.** Any
provider can receive a comparable order.

**On-prem (Qwen-VL track, doc 11/12) is mandatory when:**
- the page is `client:*` under NDA/ITAR/export-control, or contains site
  coordinates / named individuals — **no exceptions**;
- you lack a signed **ZDR addendum or BAA** with the provider;
- the vision call must go through Files/Batch/code-execution paths (not ZDR-eligible
  even under a ZDR contract);
- the detector trips or classification is missing (fail-closed).

Cloud VLM is permissible **only** for affirmatively public/cleared pages, or
sensitive pages under a signed ZDR/BAA on **ZDR-eligible inline endpoints**, with the
routing decision logged (§4).

## 3. Redaction before egress — send a derivative, never the raw

- **Reversible (internal only):** Presidio tokenization/encryption so the original
  restores internally with a key — used *only* inside the boundary; the key **never
  crosses the egress line.**
- **Irreversible (anything leaving):** the cloud-bound copy is *destructively*
  redacted — pixels painted out, text deleted (not masked-with-recoverable-token).
  One-way.

**The catch that limits this:** redacting the page may defeat the verification's
purpose — black out the cell you wanted vision to check and you've verified nothing.
So redaction-before-egress applies to *surrounding* PII (title-block author, stamp,
embedded personnel photo) while preserving the technical region under test. **When
the sensitive content *is* the region under test → on-prem, don't redact-and-send.**

## 4. Audit — proving the negative

Compliance often requires proving a negative: *"this confidential page was never
sent externally."* You cannot prove that from cloud logs you don't control — you
prove it from **your own egress-gate ledger**, written at the choke point every page
passes through:

- Every vision call emits an append-only, **hash-chained** record:
  `sha256(page_image)`, source provenance pointer, classification, **route decision
  (`on-prem` | `cloud:<provider>`)**, detector verdict + version, redaction (Y/N +
  method), timestamp, gate-policy version.
- The **negative assertion is then queryable:** "for every page whose `sha256` is in
  the confidential set, the ledger shows `route=on-prem` and zero `cloud:*` rows."
  The ledger is the evidence; provider DPAs describe *intent*, the ledger describes
  what your pipeline actually *did*. It mirrors doc 07's fail-closed citation
  contract.

## 5. Photo-specific — strip metadata and faces/plates first

Evidence imagery (doc 11) carries PII in two layers:

- **Metadata is deterministic — strip it always, first.** `exiftool -all=`
  (or `-gps:all=`) removes EXIF/GPS reliably; a phone photo's GPS is accurate to
  ~5 m — it can pinpoint a restricted site. A cheap, exact step that fits the creed
  ("extract deterministically"); run on *every* image before any VLM call regardless
  of route.
- **Pixels need (imperfect) detection.** **EgoBlur** (Meta, Apache-2.0) blurs
  faces/plates; Presidio Image Redactor (MIT) handles text PII baked into pixels via
  OCR. Because pixel detection misses, the fail-closed rule holds: **if an image
  contains people/vehicles and you cannot affirmatively clear it, route the
  description pass on-prem rather than trusting the blur.**

## Tooling verdicts (feed into doc 12)

| Tool | License | Verdict | Why |
|---|---|---|---|
| Presidio (text + image redactor) | MIT | **ADOPT as trip-wire, not gate** | vendor disclaims completeness; tune for recall (F-β, β=2) |
| ExifTool | Artistic/GPL (dual) | **ADOPT (subprocess)** | deterministic EXIF/GPS strip; copyleft fine for CLI invocation |
| EgoBlur (face/plate) | Apache-2.0 | **ADOPT (candidate)** | photo pre-redaction; no published recall → blur is best-effort, pair with fail-closed routing |
| Cloud VLM (Anthropic/OpenAI/Google) | service | **Conditional** | public/cleared pages, or sensitive under signed ZDR/BAA on ZDR-eligible inline endpoints |
| AWS Bedrock VLM | service | **Conditional** | different processor chain; verify your own DPA |

## Candidate practices (need a pilot before minting as a GP)

1. **Fail-closed egress gate:** one choke point for all vision calls; default route
   = on-prem; cloud requires affirmative public/cleared classification OR signed
   ZDR/BAA on a ZDR-eligible endpoint.
2. **Detector-as-trip-wire, never-as-gate:** Presidio can only *add* reasons to route
   on-prem; it can never *grant* cloud egress.
3. **Negative-assertion egress ledger:** append-only, hash-chained per-page record —
   the auditable proof confidential pages stayed internal.
4. **Deterministic metadata strip on every image** (ExifTool `-all=`) before any VLM
   call, regardless of route.
5. **Photo pixel pre-redaction** (EgoBlur + Presidio image OCR) for cloud-bound
   imagery, with fail-closed routing because blur recall is unpublished.
6. **Pin sensitive vision to ZDR-eligible inline endpoints** (avoid Files/Batch/
   code-execution paths that exit the ZDR envelope even under a ZDR contract).
7. **Re-verify each provider DPA at adoption time;** record verified retention terms
   + date in externalized gate-policy YAML.

*Snapshot 2026-06. Provider retention terms churn — re-verify against the DPA at
adoption. Full primary-source citations (vendor docs, the court order, license
files): issue #19.*
