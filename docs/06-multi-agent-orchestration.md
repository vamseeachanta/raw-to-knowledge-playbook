# Multi-Agent Orchestration

This campaign ran across three agent providers concurrently. The division of
labor that emerged was driven by hard constraints (sandboxes, quotas, model
guardrails), not preference — and is likely to generalize.

## Division of labor

| Role | Best fit observed | Why |
|---|---|---|
| **Bulk extraction** | *No agent at all* — deterministic tools dispatched by a thin script | Verbatim reproduction is what tools do and models refuse/garble (GP-01) |
| **Orchestration & verification** | Primary interactive agent (Claude) + its subagents | Vision verification, batch sequencing, queue edits, git serialization need a stateful conductor |
| **Independent code review** | Second provider (Codex) | Independence matters more than capability: a different model with different blind spots found real bugs (stranded commits, dedup precedence loss) |
| **Review fallback / monitoring** | Third provider (Gemini) + an internal monitoring agent | Provider outages happen mid-campaign; a fallback lane keeps the review gate honest. Note: a "third orchestrator" that shares a second provider's quota pool is really the same lane — count quota-independent lanes, not agent brands |

Session-count reality check: ~80 second-provider sessions over 25 days were
almost all *dispatch and review*, not authoring. The "AI pipeline" is mostly
deterministic code with models stationed at judgment points.

## Operational constraints that shaped the design

1. **Nested agents starve.** An agent CLI invoked *inside* another agent's
   sandbox ran at ~5% CPU and produced nothing for hours. Heavy work goes to
   first-class subagents of the orchestrator; nested CLIs only for light,
   independent review.
2. **Sandbox write-roots are launch-cwd-scoped.** A sandboxed agent's
   writable root is where it was launched; sibling repos are read-only.
   `cd` into the target repo before dispatching writes.
3. **Sandbox setup fails transiently under concurrency.** Namespace/uid-map
   errors are retryable, not fatal. Backoff and cap concurrent sandboxed
   agents (≤3 worked).
4. **Buffered stdout from dispatched processes is lossy** — capture to files,
   and kill stalled dispatches by PID (a pattern-based pkill once matched the
   killer itself).

## Parallelism pattern: partition by file ownership

```
            ┌────────────── orchestrator (one session) ──────────────┐
            │  selects batches, validates claims, serializes ALL git │
            └───────┬───────────────┬───────────────┬────────────────┘
                    ▼               ▼               ▼
              worker A          worker B        worker C
            domain-1 queue    domain-2 queue   domain-3 queue
            (writes ONLY      (writes ONLY     (writes ONLY
             its files)        its files)       its files)
```

- Workers never touch git. The orchestrator commits per-file
  (`git commit -- <path>`), foreground, serialized.
- Partitioning unit = whatever guarantees disjoint write sets. Here:
  per-domain verification queues.
- Within a partition, work is *serialized against the merge gate*
  (select → PR → merge → select), because shared state lives on main.

## The review lattice

Three distinct review layers, each catching what the others can't:

| Layer | Catches | Example |
|---|---|---|
| Deterministic checks (CI, structural triage, diff-size assertions) | Shape problems | Ragged CSVs, phantom diffs |
| Vision verification | Value problems | Watermark glyphs, digit substitution, column drift |
| Adversarial cross-provider review | Process problems | Stranded-commit path, dedup precedence bug, identity degeneracy |

Rules of engagement:
- **Adversarial stance is mandatory** — prompts force defect-hunting;
  charitable reading rubber-stamps.
- **Review before the human gate**, never after: a PR is not presented for
  merge until independent review evidence exists.
- **Scale depth to scope**: light change = one reviewer; pipeline-critical
  change = two or three providers.
- **Trust disagreements with evidence** (GP-10): the verdict citing a
  falsifiable specific wins.

## Knowledge persistence across sessions

A multi-week, multi-provider campaign lives or dies on continuity:

- **One fact per memory file**, indexed; incidents recorded the day they
  happen with the *why* and *how-to-apply*.
- **Session handoffs** at every exit: commits with SHAs, repo state, a
  cleanup-audit verdict (CLEAN / EXPECTED / UNEXPECTED residue), open
  questions, and what the session deliberately did *not* do.
- **Recurring workflows promoted to skills** (parameterized, versioned
  prompts+scripts) once they stabilize — see
  [08-skills-catalog.md](08-skills-catalog.md).
