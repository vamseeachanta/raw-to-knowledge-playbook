---
name: page-shape-contract
description: >
  Enforce the structural contract for a knowledge-store page: the layered
  input/output split, required provenance frontmatter, trust labels on every
  value-bearing artifact, and the public/private abstraction gate. Use when
  creating or reviewing any wiki/knowledge page before it is committed.
trigger: "/check-page-shape <page.md>"
enforcement_level: L3   # pre-commit hook can block a malformed page
params:
  page: { type: string }
incident_refs: [B2, fail-closed-citation]
status: template
---

# page-shape-contract

> Template skill (doc 08, doc 07). Governs what a well-formed page looks like so
> that downstream consumers can always tell provenance and trust at a glance.

## Trigger
`/check-page-shape <page.md>`

## Preconditions
- The page declares its `visibility:` (+ optional `client:`) in frontmatter.

## Steps / checks
1. **Provenance frontmatter present:** `code_id`/`publisher`/`revision`,
   `sources:` (sha256 pointer to off-repo raw), `extraction_policy`,
   extraction date. A page with a value but no source pointer fails.
2. **Layered input/output split:** raw-captured parts (inputs) are kept
   distinct from synthesized/derived sections (outputs); a reader can tell
   which is quoted source and which is generated.
3. **Trust label on every value-bearing artifact:** each table/constant carries
   `parse_status` (`verified` | `provisional-unverified` | `deferred` |
   `rejected`); verbatim clause quotes are labeled as deterministic captures.
   No bare numbers without a status.
4. **Non-degenerate identity:** every row/section has a non-blank identity tuple
   (incident B2: a blank field collapsed distinct rows and silently dropped one).
5. **Abstraction gate:** in any shared/public-routed page, client/project names
   are abstracted unless the fact is publicly verifiable (the public/private
   routing skill owns the firewall; this skill checks the page conforms).
6. **Fail-closed citation:** any derived constant cites code id + publisher +
   revision + source page; if the cited page's frontmatter is missing/mismatched
   the page is invalid (the contract refuses rather than ships an unprovable value).

## Verification
- The checker returns a per-rule pass/fail; a pre-commit hook (L3) blocks commit
  on any failure.

## Cleanup
- n/a (read-only check).

## Incident appendix
| Rule | Why |
|---|---|
| Non-degenerate identity | B2: blank identity field silently dropped a distinct row |
| Fail-closed citation | A value with no provable pedigree must refuse, not ship |
