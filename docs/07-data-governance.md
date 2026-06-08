# Data Governance: Provenance, Licensing, Public/Private Routing

Ingesting licensed and confidential material into an LLM-queryable store is
as much a governance problem as a technical one. These are the rules that
kept the campaign clean.

## 1. The raw-source firewall

- **Raw licensed PDFs never enter any repo.** They live in an off-repo,
  read-only archive. The wiki stores *derived* data (text parts, table CSVs,
  captions) plus a `sources:` pointer in frontmatter.
- A **deny-list scan** runs pre-commit: API keys, private mount paths,
  client identifiers, personal data patterns.
- Derived data from vendor-licensed sources lives in a **private** wiki;
  genuinely public-domain material routes to a public sibling. Visibility is
  declared in frontmatter (`visibility:` + optional `client:`) and enforced
  by a pre-commit check — routing is a *machine-checked contract*, not a
  convention.

## 2. Provenance chain (every artifact answers "where did this come from?")

```
source file (off-repo, sha256 recorded)
  → landing page frontmatter (code id, publisher, revision, source pointer,
                              extraction_policy, extraction date)
    → part files (page-number citations)
    → table CSVs (queue row: source page, extraction status, verifier,
                  verification notes)
      → derived constants (sidecar citation: code id + publisher + revision
                           + source wiki; FAILS CLOSED if the cited page's
                           frontmatter is missing or mismatched)
```

The fail-closed citation contract is the keystone: downstream calculations
that consume a wiki value must be able to prove its pedigree at call time,
or they refuse to run.

## 3. Trust labeling

Consumers must always be able to distinguish:

| Label | Meaning | Safe uses |
|---|---|---|
| `verified` | Vision-checked cell-by-cell against the source | Engineering use, derived constants |
| `provisional-unverified` | Auto-extracted, structurally plausible | Search/discovery only; never cite values |
| `deferred` | Known-defective extraction of real data | Re-parse backlog |
| `rejected` | Not a data table / unrecoverable | Audit trail only |
| Verbatim clause captures | Quoted normative text w/ attribution | Trustworthy immediately (deterministic copy) |

A useful asymmetry discovered early: **verbatim clause quotes and honest raw
captures are trustworthy on day one; parsed tables are not.** Ship the
former immediately, gate the latter behind verification.

## 4. Confidentiality screening of *generated* content

The leak vector is not file copying — it's agents *writing about* private
material. Two controls:

1. **Write-time abstraction:** client/project names are abstracted by
   default in any shared store; a name appears only when the fact is
   publicly verifiable.
2. **Publish-time grep:** before any content leaves the private boundary,
   grep it against a maintained list of client names, project codes, and
   internal path/host patterns. Do not delegate this check to the agent that
   produced the content (observed failure: a subagent declared its output
   clean while it contained client folder names).

## 5. Licensing posture for the knowledge store itself

- Split licensing: code under MIT, content under CC-BY-4.0 (for the public
  store).
- For the private store, "private" is a license boundary, not an excuse to
  skip attribution — every page still cites its source, because provenance
  is what makes the data usable in engineering deliverables.

> For how copyrighted and confidential content actually *enters* the repo (the
> derived forms and leak vectors), and the **private-mode operating posture** —
> gates relaxed inside the boundary, two structural invariants kept, the rest
> operator discretion — see [doc 19](19-trust-boundary-and-private-mode.md).
