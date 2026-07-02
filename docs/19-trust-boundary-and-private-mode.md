# Trust Boundary: What Enters the Repo, and the Private-Mode Posture

[Doc 07](07-data-governance.md) gives the governance *rules* and [doc 18](18-security-and-pii.md)
guards *egress* (page images leaving for a hosted VLM). This doc answers the
question underneath both: **how does copyrighted and confidential information
actually get *into* a committed repo — and how strict should you be about it?**

The honest framing first: the corpus is mostly **copyrighted** standards and
**confidential** project material, and the README promises usefulness "*without
committing copyrighted source material or trusting raw model output.*" Both halves
of that promise are about a **boundary**, not about never touching the content. The
content *must* enter the repo in derived form — that is the reuse value. This doc
maps what enters, and states the operating posture that decides how tightly to
police it.

> **Scope.** This is an engineering-controls analysis of the pipeline, **not legal
> advice.** The facts-vs-expression and fair-use questions it surfaces are the
> organization's to settle with counsel. The playbook flags counsel only for *tool*
> licenses (doc 12); *source-content* copyright is left to the operator — see the
> private-mode posture below.

## The two structural invariants (always hold, even in private mode)

Everything else in this doc is adjustable. These two are not — they are cheap,
structural, and they prevent the one irreversible mistake:

1. **The raw source file never enters any repo.** It lives in an off-repo,
   read-only archive; the repo stores only *derived* data plus opaque source
   tokens or provenance bundle references. Raw source digest values stay
   private-sidecar only. This keeps the repo from *being* the redistributable copy.
2. **Private-classified data never crosses into a public/shared repo.** The
   `visibility:` frontmatter field is the single point that, if wrong, turns an
   internal knowledge base into publication. It is machine-checked at commit
   (doc 07 §1; the `public-private-routing` skill).

If you keep only two checks, keep these.

## The private-mode operating posture

Most adopters run this over a **private** corpus for **internal** use — the same
model countless businesses use for an internal knowledge base over licensed
standards and confidential files: ingest under provenance and access control, use
internally, do **not** republish, and leave the licensing/fair-use judgment to the
organization rather than the tooling.

In that mode, "private" is a **license/trust boundary, not a legal clearance**
(doc 07 §5). Inside the boundary the gates are **deliberately relaxed**: derived
tables, figures, clauses, and passages are kept for reuse with attribution, and you
do not pay for exhaustive PII redaction, verbatim-length caps, or facts-vs-expression
adjudication on every artifact. What you keep is **provenance** (every value cites
its source) — because that is what makes the knowledge *usable* in deliverables, and
it is worth keeping regardless of how open the gates are.

| Control | Private internal mode | Public / shared-boundary mode |
|---|---|---|
| Raw source file off-repo (private-sidecar digest only) | **Required** | **Required** |
| Private never crosses to public | **Required** | **Required** |
| Provenance / citation on every value | **Required** | **Required** |
| Verbatim-length caps, cumulative-coverage limits | **Discretion** | Tighten (fair-use exposure) |
| PII detector recall tuning, redaction depth | **Discretion** | Tighten (egress + publication) |
| Facts-vs-expression review of tables/clauses | **Discretion** | Counsel before publishing |
| Independent publish-time grep against deny-list | Recommended | **Required** |

The columns are a dial, not a cliff. A page that might ever be published, demoed,
or shared with a third party moves to the right-hand column **before** it crosses
the boundary — which is why the `visibility:` field and the egress gate (doc 18)
are where the discretion actually gets spent.

## How content enters — the derived forms

Content reaches the repo only as *derived* representations; copyright and
confidentiality each ride different ones:

| Derived form committed | Copyright lens | Confidentiality lens | Routing |
|---|---|---|---|
| **Raw source file** | the whole work | the whole source | **never committed** — private-sidecar digest reference only |
| Verbatim clause quote | copyrighted **expression**, attributed | source text | private unless source is public-domain |
| Text "parts" / page excerpts | **full** verbatim body text | full source body | private |
| Table CSV of values | numeric **facts** (lean uncopyrightable) | PII/values can hide in cells | per source class |
| Summaries / derived constants | **transformative** | abstracted by default | shareable when corroborated |
| Chunks + embeddings | verbatim text in the vector store | same text, now a retrieval surface | follows source `visibility:` |
| **Generated agent prose** | paraphrase (risk: verbatim-in-disguise) | **#1 leak vector** — agents *writing about* private material (doc 07 §4) | abstraction-by-default |
| Opaque provenance bundle reference | none | none | public-safe when it carries no raw digest |

## Inflow / leak vectors — where it reaches the *wrong* boundary

These are the channels by which content tips beyond intent (into a public repo, or
over-reproducing a work). In private internal mode most are accepted risk; they
matter most for anything heading toward the public column above. Each maps to the
control that catches it and the residual risk that remains your discretion.

| Vector | How it reaches a commit | Control | Residual risk (your discretion) |
|---|---|---|---|
| Raw file committed directly | someone adds the PDF/workbook itself | raw-source firewall + deny-list path scan (doc 07 §1) | renamed/relocated file; a derived "part" that is effectively the whole work |
| Mis-set `visibility:` routes private→public | frontmatter wrong but internally consistent; router faithfully permits | machine-checked visibility contract (doc 07 §1) | the check enforces *consistency*, not *correctness* — the load-bearing hand-set field |
| Agent prose names a client/project, or over-quotes | LLM narrative embeds a real identifier or long verbatim passage | write-time abstraction + **independent** publish-time grep (doc 07 §4) | deny-list completeness; cumulative verbatim has **no quantitative cap** |
| Subagent self-certifies "clean" | producing agent vouches for its own output; orchestrator trusts it | the gate greps **itself**, never the producer (doc 03; doc 07 §4) | procedural — nothing structural forces the independent grep |
| Client data interleaved in an extracted Excel calc (D5) | populated input cells ride along with ported formulas | extract generic methodology only; scan before archive (doc 04 D5; GP-31) | confidential **numeric values** are invisible to an identifier grep |
| PII in a table value / EXIF-GPS in a photo | a cell holds an author/coordinate; an image keeps GPS | Presidio trip-wire (doc 18 §1); `exiftool -all=` first (doc 18 §5) | detector recall is vendor-disclaimed; metadata strip must actually be run |
| Re-ingested edition re-introduces withheld content | a new/clean re-release is re-extracted | supersede-by-append + trust reset (doc 16) | lifecycle resets *trust*, **not** confidentiality/redaction — re-screen is a documented gap |
| Embeddings as a reconstruction surface | chunks keep verbatim source text by design (doc 14) | `parse_status`/`visibility` carried into chunks | protects *trust*, not *redistribution* if the index leaves the boundary |

## Hardening options (only if you tighten toward the public column)

None of these are required in private internal mode — they are the dials to turn
when an artifact approaches a shared/public boundary:

- **Keep the identifier deny-list genuinely complete** — a *process* to review and
  extend it, not just "maintained"; it is the silent single point of failure for
  every grep-based control.
- **A cumulative-verbatim signal** per source — there is no documented threshold for
  "how much of one standard is too much"; add one before publishing clause text.
- **A confidentiality re-screen node** in the corpus-lifecycle cascade (doc 16) so
  re-ingested editions are re-redacted, not just re-trusted.
- **Value-level review** for ported calc fixtures (D5) — identifier grep is blind to
  proprietary numeric inputs.
- **A cross-check on the `visibility:` tag** (frontmatter-vs-source-class, or
  independent review) — the one field whose error is irreversible.
- **Treat any cloud egress of sensitive pages as residual exposure** regardless of
  DPA (doc 18 §2: retention is defeasible by litigation hold).

## The bottom line

In private internal mode the gates are intentionally open inside the boundary;
keep the **two structural invariants** (raw file off-repo, private never goes
public) and **provenance**, and leave the rest to operator discretion — escalating
to the public column only for content that will actually be shared. That is the
standard internal-knowledge-base model; the playbook supplies the engineering half
(firewall + boundary + provenance), and the legal half stays with the organization.

## ACE #61 private boundary hook

The #61 knowledge-store contract is a methodology and control-plane artifact. It
does not publish ACE content, link a wiki route, or certify public egress by
itself. Public navigation and wiki exposure remain blocked until the #63 canary
certifies the relevant surface.

raw source digest values stay private-sidecar only. Public surfaces use opaque
tokens, provenance bundle references, or non-digest hash references when a public
artifact needs to cite private provenance shape.

Inside the private boundary, #61 permits opaque provenance bundle references and
closed lifecycle states so agents can work progressively without committing raw
source detail. Anything promoted toward a shared boundary must pass the
independent scan and publication gate first.
