---
name: adversarial-verify-loop
description: >
  Runs an independent adversarial verification loop on a produced change
  (extraction code, corpus batch, or page set) until a clean PASS — the producer
  never self-certifies, the reviewer is prompted to refute and to build runnable
  reproducers for code findings, and every fix is gated on re-running the
  reviewer's own reproducer. Use when a change must earn justified confidence
  before merge, especially pipeline-code changes where a plausible fix can be
  narrower than the defect class.
license: CC-BY-4.0
compatibility: Requires an independent reviewer agent (different model/session from the producer), a reproducible run command for the change under review, and a PR label flow (needs-verify -> verified)
metadata:
  version: "1.0"
  enforcement_level: L2            # callable review loop; L3 hardening = a merge gate on the verified label
  status: template
  incident_refs: prose-overclaim,derived-name-collision,attachment-drop,merge-cascade-strand
  params: "target:str | min_rounds:int=2"
---

# adversarial-verify-loop

> Template skill (doc 03, doc 04, GP-42). The confidence mechanism behind a
> mixed-office ingestion campaign: every batch and every pipeline change was
> cleared by an **independent reviewer told to refute it**, not confirm it.
> The loop's value showed up precisely when it "failed": closing one gap took
> three rounds — round 1 caught a defect *class* (derived-filename collision),
> round 2 caught the **incompleteness of the producer's fix** by building a
> monkeypatched reproducer with synthetic inputs, round 3 re-ran that same
> reproducer against the new fix and passed. Code-reading alone had waved the
> intermediate fix through.

> **What this gates:** the change PR (`needs-verify` → `verified` label flow).
> It composes with `source-extract-fidelity` (the prose-vs-extract rules for
> page content) — this skill is the *outer loop*: independence, reproducers,
> and the until-PASS termination rule.

## Trigger
`/adversarial-verify-loop <target> [--min-rounds 2]`

## Preconditions
1. The reviewer is **independent of the producer** — a different agent/model/
   session, with no stake in the change passing, prompted to *find a reason it
   is wrong*.
2. The change is **reproducibly runnable**: the reviewer can execute the same
   extraction/build command the producer ran (record the exact command,
   including env vars and runner — e.g. PEP-723 scripts MUST be run with
   `uv run`, not bare `python`; a wrong runner produces false FAILs).
3. A label flow exists on the PR: it opens `needs-verify` and may only flip to
   `verified` on a clean PASS.

## Steps
1. **Scope the round.** Give the reviewer the exact diff (commit range), the
   run command, and the invariants to attack (determinism, no-silent-drop,
   raw-binary firewall, claim-traceability — whatever the change asserts).
2. **Demand refutation, not confirmation.** The prompt asks the reviewer to
   break the change: hunt edge cases the producer didn't test, construct
   inputs that violate the asserted invariant, and check the prose/docs for
   claims beyond the evidence.
3. **Reproducers for code findings.** A code finding is credible when it comes
   with a **runnable reproducer** (synthetic inputs, monkeypatched parsers,
   crafted file sets) — not just an argued scenario. Findings carry severity
   (blocker/major/minor) and a falsifiable location (file:line).
4. **Reproduce the producer's run.** The reviewer re-runs the pipeline command
   and confirms committed artifacts are **byte-identical** to a fresh run
   (determinism + honesty of what was committed).
5. **Fix narrowly-or-fully, then re-loop.** The producer fixes findings; the
   next round re-checks **by re-running the reviewer's own reproducer against
   HEAD**, plus fresh eyes on the fix commit for new defects. A fix that
   handles the cited example but not the invariant fails here — by design.
6. **Terminate on PASS, not on round count.** `min_rounds` is a floor. The
   loop ends only when a round returns zero findings. Then flip the label to
   `verified` and post the round table (verdict per round + what each caught)
   on the PR as the verification record.
7. **Close child-wave method gaps explicitly.** For ACE ingestion waves under
   issue #50, every reusable method gap found during review must be resolved as
   one of `doc-update`, `skill-eval-update`, or `follow-on-issue` before
   closeout. Update the wave's coordination row if the disposition changes.

## Verification
- The PR carries a posted round table: every round's verdict and findings,
  ending in a PASS round with zero findings.
- Every code finding in any round has a runnable reproducer, and the final
  round re-ran each one against HEAD.
- The reviewer's re-run of the pipeline command produced byte-identical
  committed artifacts.
- The label history shows `needs-verify` → `verified` only after the PASS
  round (no self-certification by the producer).
- ACE wave closeout records each method gap as `doc-update`,
  `skill-eval-update`, or `follow-on-issue`; no reusable gap remains only in
  session notes.
- Review artifacts and publication-facing summaries pass
  `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces`; use
  `--diff-only` before committing reviewer outputs.

## Cleanup
- Review transcripts/reproducers live outside the repo (temp/session dirs);
  move them out before committing — they stage otherwise.
- After merge, verify the default branch's **tree** actually contains the
  change (the merge-cascade-strand guard from `stacked-batch-prs`).

## Incident appendix
| Rule | Why |
|---|---|
| Independent reviewer, prompted to refute | The producer can't see its own overclaim; charitable review rubber-stamps |
| Reproducers, not arguments | A monkeypatched reproducer caught an incomplete fix that code-reading waved through |
| Re-run the reviewer's reproducer on HEAD | The producer's "fixed" is a claim; the reproducer is the test |
| PASS terminates, not a round count | The fix for round 1's finding introduced round 2's; only a zero-finding round proves convergence |
| Record the exact runner | A reviewer running a PEP-723 script with bare `python` produced a false FAIL (missing deps) |
| Post the round table on the PR | The verification record is part of the deliverable — confidence must be auditable later |
| Close method gaps into durable artifacts | ACE child waves must improve the playbook or file a follow-on issue instead of burying reusable lessons in a transcript |
