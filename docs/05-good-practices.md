# Good Practices Catalog (living document)

Numbered, append-only. Each practice records the **rule**, the **why**
(usually an incident), and **how to apply**. New practices are added via PR
as the work surfaces them — see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Extraction

**GP-01 — Extract deterministically; reserve LLMs for judgment.**
Why: LLM extraction of a 118-page standard yielded ~2% coverage (a summary),
hit copyright guardrails that no prompt overrides, and took hours. A
deterministic PDF library yielded 100% (48k words + 38 table CSVs) in
seconds.
Apply: tools extract; models verify, classify, route, review.

**GP-02 — Provisional by default.**
Why: auto-parsed tables are structurally consistent but value-wrong often
enough to poison a knowledge base.
Apply: every extracted artifact carries `parse_status:
provisional-unverified` until a vision pass promotes it. Record the
extraction level (`extraction_policy`) in frontmatter so consumers know what
they're reading.

**GP-03 — Strip watermarks before extraction.**
Why: rotated watermark overlays merge their glyphs into table cells and pass
every structural check.
Apply: neutralize rotated-placement Form XObjects in-memory pre-extraction;
config-driven; never modify the raw source file.

**GP-04 — Route by content, not folder; filter by value.**
Why: source archives are misfiled grab-bags; image-only/low-text PDFs paginate
into pure noise (one 73-page garbage doc observed).
Apply: classify on extracted text; word-count gate; junk filters for
catalogs/minutes/brochures; record every skip with a reason.

**GP-05 — The hardened ingest contract is all-or-nothing.**
Five rules — content routing, value filter, dedupe-before-write, selective
verbatim + provisional tables, index/log update. Applying a subset creates
duplicates, misfiling, or mislabeled trust states.

## Verification

**GP-06 — Select verification batches by data density.**
Why: alphabetical/file-order selection burned entire batches on blank forms
(0/24 verified); density ranking yields 5–7 verified per 12.
Apply: rank by numeric density; sink row-collapse suspects to the bottom
(don't auto-reject them — vision stays the authority).

**GP-07 — Check the rightmost column.**
Why: multi-header tables align on the left and shift on the right;
"confirm-first-cell-and-extrapolate" subagents over-verified 6 of 12 rows in
one batch.
Apply: every verification confirms at least one rightmost-column value.

**GP-08 — Serialize select→merge per domain.**
Why: the batch selector reads the main branch; selecting before the prior
batch merges re-picks identical rows (two duplicate batches shipped).
Apply: one in-flight verification batch per domain; cross-domain parallelism
is fine (separate queue files).

**GP-09 — Anchor on exact paths, never globs.**
Why: standard editions share table IDs; a glob verifies the wrong edition.

**GP-10 — Prefer the verdict citing a falsifiable defect.**
Why: duplicate batches produced opposite verdicts on one table; the rejection
cited an exact source-value mismatch, the verification was generic approval.
Apply: when reviews disagree, specific evidence wins; require evidence in
verdict notes.

**GP-11 — Rejections carry a defect class and feed a re-parse loop.**
Why: most rejected tables are real data wrongly extracted (transposed,
truncated, collapsed, contaminated) — recoverable once the extractor
improves.
Apply: tag the class in queue notes; after an extractor fix, re-extract
exactly the affected class, mapping by page + in-page order with shape
preservation as the correctness proof.

## Data plumbing

**GP-12 — Union-merge needs append-only; rewrites need dedup-on-write.**
Why: one full-queue rewrite turned union-merge into 46% row duplication.
Apply: self-healing dedup on every write, idempotent, with precedence rules;
never rely on one-time cleanups.

**GP-13 — Row identity must be non-degenerate for every row type.**
Why: blank fields in the identity tuple silently collapse distinct rows.

**GP-14 — Binary-faithful I/O for mixed-line-ending files; diff-size
assertions after every edit.**
Why: text-mode round-trips produced a 352-line phantom diff for a 12-row
edit.
Apply: binary read/write preserving per-row terminators; assert
`git diff --numstat == 2 × rows-changed`; harden for embedded newlines before
the first one appears.

**GP-15 — Status vocabularies are closed sets, separated by column.**
Why: an unregistered status got mangled by the normalizer; a verdict written
into the structural column corrupted a batch.
Apply: register new values before first use; batch prompts hard-specify
allowed values per column.

## Automation

**GP-16 — Resumable state machine + idempotent chunks.**
Apply: chunked work units, JSON state keyed by doc-set, per-chunk commit +
immediate state save, isolated worktrees, force-reset branch creation.

**GP-17 — One PR per tick; humans merge.**
Why: one-PR-per-publisher (13/tick) created chronic merge churn between
shared files; branch chaining diverged refs.
Apply: all work units accumulate on one branch per tick; automation never
merges.

**GP-18 — Don't buy parallelism you don't need.**
Why: concurrency-3 contended on git refs; deterministic extraction is so fast
that serial saturates the pipeline anyway.

**GP-19 — Reconstruct the environment in cron wrappers; parameters live in
the repo.**
Why: cron strips the interactive env (silent dispatch death); in-repo args
mean config changes ship by PR. Remember a running tick uses the script as
of launch.

**GP-20 — Prove a "hang" before killing it.**
Why: block-buffered stdout + timeout SIGKILL leaves an empty log while work
proceeds; a healthy job was falsely flagged.
Apply: unbuffered output + a stack-dump-on-timer before declaring anything
hung.

## Multi-agent discipline

**GP-21 — Orchestrator serializes git; workers only write files.**
Why: 60+ concurrent git procs produced a 19-minute D-state hang; background
git loses traceability.
Apply: atomic per-file commits in the foreground session; partition parallel
workers by disjoint file sets (e.g., per-domain queues).

**GP-22 — Adversarial review before merge, scaled to scope.**
Why: independent reviews found real bugs the author missed (stranded-commit
path, dedup precedence flag-loss).
Apply: every substantive PR gets at least one independent adversarial review;
prompts must force defect-hunting, not charitable reading.

**GP-23 — Verify subagent claims yourself — in both directions.**
Why: subagents over-verify tables (GP-07) and overclaim confidentiality
screening (one asserted "no confidential identifiers" while leaking project
folder names).
Apply: orchestrator spot-checks verifications and greps outputs for known
identifiers before anything ships.

**GP-24 — Capture lessons as durable memory/skills at the moment of
incident.**
Why: every practice in this file exists because it was written down when it
bit; re-derivation is expensive.
Apply: one fact per memory file; promote recurring workflows into versioned,
parameterized skills (see [08-skills-catalog.md](08-skills-catalog.md)).

## Governance

**GP-25 — Raw licensed sources never enter the repo.**
Apply: raw PDFs live in an off-repo archive; the wiki stores derived data +
a source pointer; a deny-list scan runs pre-commit (keys, private paths,
client identifiers).

**GP-26 — Screen for confidential identifiers at write time, verify at
publish time.**
Why: leakage happens through agents' generated text, not just copied files.
Apply: maintain a known-identifier list; grep all outbound content against
it; public/private routing enforced by frontmatter + pre-commit check.

---

*Next ID: GP-27.*
