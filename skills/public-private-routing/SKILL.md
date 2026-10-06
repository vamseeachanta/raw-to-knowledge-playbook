---
name: public-private-routing
description: >
  Use when routing knowledge by declared visibility, source rights and access permissions.
  Review client, project, personal and location identifiers in the final report.
license: CC-BY-4.0
compatibility: Requires declared visibility and source-rights evidence
metadata:
  version: "1.0"
  enforcement_level: L3            # independent security and source-rights checks
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
- Every page declares `visibility: public|private` (+ optional `client:`).

## Steps
1. **Declare-and-check visibility.** Read `visibility:` from frontmatter. Derived
   data from vendor-licensed/confidential sources MUST route private; only
   genuinely public-domain material routes public. Mismatch → block.
2. **Identifier review.** Permit identifier and location mentions through repositories.
   At final report, review actual names, personal details and paths for the intended
   audience and record disposition. Do not impose an identifier-only commit gate.
3. **Independent security checks.** Preserve credential detection, actual access
   permissions, explicit source-rights restrictions and bounded traversal.
4. **Raw-source firewall.** Assert no raw licensed/confidential source file is
   being committed — only derived parts plus opaque public source tokens or
   public-safe provenance bundle references.
5. **ACE wave-1 JSON/config/code-derived output.** Before any text, config, or
   code-doc candidate routes `public_llm_wiki`, require affirmative public
   clearance and the #63 public-output canary over the exact surface. Without
   clearance, demote to `private_sidecar`, `metadata_only`, or
   `excluded_no_ingest`.

## Verification
- Independent security and source-rights checks must pass; identifier-only findings
  are reviewed at final report without a new automated receipt gate.
- For ACE-derived public outputs, run
  `uv run python scripts/validate_ace_public_artifacts.py --scan-public-path <surface> --issue-comment-body-file <planned-comment.md>`
  over the exact docs, skill, workflow, review artifact, `mkdocs.yml`,
  `llm-wiki`, GitHub-public summary, issue closeout summary, or external
  publication surfaces before they cross the boundary.
- For this repo, run `python scripts/security/public_surface_safety_scan.py --all-tracked-public-surfaces`
  before publishing or closing public-surface work; use `--diff-only` for local
  staged/unstaged closeout checks.

## Cleanup
- n/a (gate).

## Incident appendix
| Rule | Why |
|---|---|
| Final-report identifier review | Verify the actual output and intended audience |
| Explicit source rights | Identifier flow does not grant publication rights |
| Machine-checked visibility | Routing is a contract, not a convention |

Identifier-only findings are reviewed in the final report; they do not block repository flow. Independent secret, access, source-rights, provenance and traversal checks remain active.
