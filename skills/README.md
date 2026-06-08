# Skills: the playbook's workflows as runnable artifacts

[Doc 08](../docs/08-skills-catalog.md) explains *why* a stabilized workflow
becomes a skill and what a good skill file contains. This directory ships those
skills as **adaptable templates** — the transferable rules are concrete; the
corpus-specific paths/commands are `{{PLACEHOLDERS}}` you fill in.

Each `SKILL.md` follows the doc-08 anatomy (Trigger · Preconditions · Steps ·
Verification · Cleanup · Incident appendix) and carries frontmatter declaring
its trigger, closed-set params, current `enforcement_level`, and the
`incident_refs` (failure classes from [doc 04](../docs/04-failure-modes.md))
that shaped its rules.

## Catalog

| Skill | Doc 08 entry | Enforcement | What it does |
|---|---|---|---|
| [verify-batch](verify-batch/SKILL.md) | The flagship | **L2** | Vision-verify a batch of extracted tables; closed-set verdicts; binary-faithful queue I/O; one PR per batch |
| [source-extraction-coverage](source-extraction-coverage/SKILL.md) | Research skill 3 | **L2** | Doc-type-aware deterministic extraction with an estimate/yield pair that makes shallow extraction loud |
| [page-shape-contract](page-shape-contract/SKILL.md) | Research skill 1 | **L3** | Structural + provenance + trust-label contract for a well-formed page |
| [audit-feedback-loop](audit-feedback-loop/SKILL.md) | Research skill 2 | **L1** | Anchored-text feedback inbox with explicit, never-deleted resolution states |
| [public-private-routing](public-private-routing/SKILL.md) | Research skill 4 | **L3** | Public/private firewall: visibility contract, abstraction-by-default, independent publish-time grep |

## Enforcement gradient (doc 08)

`L1` callable skill · `L2` backed by a checking script · `L3` pre-commit/CI hook
that can't be bypassed. Promote a rule up the gradient when violations recur —
instructions catch intent, hooks catch everything.

## Adapting a template

1. Replace every `{{PLACEHOLDER}}` (paths, selector command, branch names) with
   your corpus's equivalents.
2. Keep the **rules** verbatim — closed-set values, binary-faithful I/O,
   serialize-per-domain, adversarial spot-check, independent identifier grep.
   Those are the parts paid for in incidents (see each file's incident appendix).
3. Register any new status value in your queue normalizer's known-set *before*
   first use, or rewrites will mangle it.

> `status: template` in the frontmatter marks a file as not-yet-adapted. A formal
> skill-file schema + validator is tracked in the strengthening epic (#14).
