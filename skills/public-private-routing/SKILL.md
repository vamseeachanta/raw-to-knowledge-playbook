---
name: public-private-routing
description: >
  Enforces the firewall between a public knowledge store and per-client private
  stores by checking declared visibility, abstracting client/project identifiers
  by default, and running an independent publish-time grep against a maintained
  identifier list. Use before committing or publishing any page, and as a pre-commit/CI gate.
license: CC-BY-4.0
compatibility: Requires a maintained identifier deny-list and pages declaring visibility/client frontmatter; wires into pre-commit + CI
metadata:
  version: "1.0"
  enforcement_level: L3            # pre-commit + CI deny-list scan
  status: template
  incident_refs: B-screening,subagent-overclaim
  params: "target:str"
---

# public-private-routing

> Template skill (doc 08, doc 07 §1/§4). The leak vector is not file copying —
> it is agents *writing about* private material. This skill is the machine-checked
> contract that catches it.

## Trigger
`/route-visibility <path-or-diff>`

## Preconditions
- A maintained **identifier list** exists: client names, project codes, internal
  path/host patterns, API-key shapes, personal-data patterns.
- Every page declares `visibility: public|private` (+ optional `client:`).

## Steps
1. **Declare-and-check visibility.** Read `visibility:` from frontmatter. Derived
   data from vendor-licensed/confidential sources MUST route private; only
   genuinely public-domain material routes public. Mismatch → block.
2. **Abstraction by default.** In any public-routed (or shared) page, client and
   project names are abstracted unless the fact is *publicly verifiable*. A
   concrete name in a public page without public corroboration → block.
3. **Publish-time grep.** Before content crosses the boundary, grep the actual
   content against the identifier list. **Do NOT delegate this to the agent that
   produced the content** — run it independently (a subagent once declared its
   own output clean while it contained client folder names).
4. **Raw-source firewall.** Assert no raw licensed/confidential source file is
   being committed — only derived parts + `sources:` sha256 pointer.

## Verification
- Pre-commit hook + CI deny-list scan must pass (L3); a hit blocks the commit/merge.
- The grep is run by the gate, not self-reported by the producing agent.

## Cleanup
- n/a (gate).

## Incident appendix
| Rule | Why |
|---|---|
| Independent publish-time grep | Producing agent overclaimed "no confidential identifiers" |
| Abstraction by default | Names leak via generated prose, not file copies |
| Machine-checked visibility | Routing is a contract, not a convention |
