---
name: audit-feedback-loop
description: >
  Maintains an anchored-text feedback inbox for a knowledge store where every
  item attaches to an exact text anchor, carries an explicit resolution state,
  and is never silently deleted. Use when collecting, triaging, or resolving
  review feedback on extracted or generated pages.
license: CC-BY-4.0
compatibility: Requires a feedback store keyed by stable text anchors; no external dependency
metadata:
  version: "1.0"
  enforcement_level: L1            # callable skill; graduates to L2 when a state validator is added
  status: template
  incident_refs: feedback-silent-delete
  params: "action:enum(add,list,resolve)"
---

# audit-feedback-loop

> Template skill (doc 08). Feedback that is deleted on resolution loses the
> audit trail that makes a knowledge store defensible. Every item is anchored
> and state-tracked instead.

## Trigger
`/audit-feedback <add|list|resolve> [args]`

## Closed-set resolution states
`open` → `acknowledged` → `resolved` | `wontfix` | `superseded`
(Never `deleted`. A resolved item is *closed with a reason*, kept for audit.)

## Steps
- **add:** attach feedback to an **exact text anchor** (page + quoted span or
  stable id), not "somewhere on this page." Record author + timestamp + initial
  state `open`.
- **list:** show items filtered by state/anchor; surface stale `open`/`acknowledged`
  items past an age threshold.
- **resolve:** move an item to a terminal state **with a reason and a link to the
  change** (PR/commit) that addressed it. The item stays in the record.

## Verification
- Every item has an anchor that still resolves to existing text (a validator can
  flag orphaned anchors after edits).
- No item is ever removed; state transitions are append-only.

## Cleanup
- n/a — non-deletion is the point.

## Incident appendix
| Rule | Why |
|---|---|
| Anchored to exact text | Vague feedback can't be verified as addressed |
| Never silently delete | Resolved-with-reason preserves the audit trail |
