# Case study — salvaging an agent-built tool repo (pdf-large-reader autopsy)

> Worked example behind [GP-49](../05-good-practices.md) and the runnable
> [`examples/pdf-preflight/`](../../examples/pdf-preflight/). It is also a
> dogfooding exercise for the [doc 12](../12-tooling-landscape.md) trust
> rubric's **Evidence** gate — *"independent benchmark or production
> reputation, not just a README claim"* — applied to one of our **own** repos
> before retiring it.

## Setup

`pdf-large-reader` was a memory-efficient large-PDF processing library
(streaming, chunking, strategy selection) built in January 2026 by an
autonomous agent loop ("Ralph"-style: PROMPT.md objectives, `@fix_plan.md`
checklist, circuit-breaker state files, loop-exit on completion signals).
History was a single squashed commit. In June 2026 the repo was reviewed for
salvage before deletion from the build machine: what was real, what was
claimed, and what deserved to live on in this playbook?

## What verification found (re-run 2026-06-12)

| README claim | Verdict | Evidence |
|---|---|---|
| "215 tests, 93.58% coverage" | **TRUE** | Re-ran the suite cold via `uv`: 215/215 passed, 92.94% measured coverage |
| Streaming/chunking/assessment modules work | **TRUE** | Covered by the passing suite, including memory-bounded integration tests (50 medium synthetic pages: generator < 100 MB peak, list-load < 200 MB, asserted with `tracemalloc`) |
| "AI Fallback: Claude integration for complex extraction" | **FALSE** | The fallback module targets OpenAI `gpt-4o`, and the actual API call is **commented out** — a stub that returns placeholder text. No Claude integration exists anywhere in the code |
| Benchmark table ("200 MB / 1000 pages / < 2 min / ~250 MB") | **UNSUPPORTED** | No committed benchmark reproduces it; the largest committed perf test generates 200 *pages* of simple synthetic text, not 200 MB |
| `@fix_plan.md` task state | **STALE** | Plan shows the assessment module unstarted; the shipped code implements it fully — the loop's bookkeeping diverged from its output |

The pattern: **the code was honest, the prose was not.** Everything enforced
by the test suite held up; everything that lived only in the README
(provider names, headline benchmarks) drifted or was invented.

## Salvage decisions

| Asset | Decision | Where it went |
|---|---|---|
| Preflight-assessment heuristics (size/pages/sampled-complexity → `full_load` / `stream_pages` / `chunk_batch`; critical issues force the careful lane) | **SALVAGED** | [GP-49](../05-good-practices.md) + [`examples/pdf-preflight/`](../../examples/pdf-preflight/) |
| Cheap defect probes (encryption flag, first/last-page access probe, > 10 % U+FFFD replacement-char ratio as an encoding-failure signal) | **SALVAGED** | same |
| Memory-estimate calibration (~2/5/10 MB-per-page by on-disk bytes/page) and the memory-bounded *test pattern* (`tracemalloc` ceiling asserts) | **SALVAGED** | example README, "real vs heuristic" table |
| The library itself (PyMuPDF-based) | **RETIRED** | PyMuPDF is AGPL-3.0 — already flagged in the [doc 12 license register](../12-tooling-landscape.md) with pdfplumber/Docling as the exit path; the salvage port uses pypdf + pdfplumber. Repo remains archived at its GitHub origin; local clone deleted |
| Stubbed AI fallback, README benchmarks | **DISCARDED** | Unsupported by evidence |

## Lessons

1. **Apply the Evidence gate to your own repos.** The doc 12 rubric exists
   for third-party tools, but an agent-built internal repo is exactly as
   capable of README inflation. Run the tests before trusting — or
   transferring — any claim.
2. **Tests are the trustworthy part of agent output.** Where the agent loop
   was forced to make claims executable (the suite), the claims were true.
   Where prose was free (README features, benchmark tables), it drifted.
   When salvaging, port what the tests prove, and label everything else
   heuristic.
3. **Loop bookkeeping is not ground truth.** The autonomous loop's own plan
   file contradicted its shipped code in both directions (claimed-done vs
   actually-done). Judge the artifact, not the agent's diary.
4. **Check the license before admiring the code.** The donor's core
   dependency (AGPL) would have re-imported a flagged obligation into a
   permissive repo; porting the *heuristics* instead of the *code* kept the
   value and dropped the flag.
