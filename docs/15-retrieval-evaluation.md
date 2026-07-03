# Retrieval Evaluation: The Answer-Side Trust Gate

[Doc 03](03-verification-playbook.md) verifies *extraction* fidelity cell-by-cell.
This doc is its missing twin: verifying *retrieval and answer* fidelity. Without
it, a perfectly-verified store can still return wrong answers and nobody notices.
The creed extends here — *trust nothing by default*, **including the metric and
the judge that produces it.**

Research and primary sources for every claim here: **issue #16**.

## The load-bearing finding: the evaluator needs its own verification layer

Reference-free RAG metrics (RAGAS, ARES) correlate with human judgment *in
aggregate* but fail on individual edge cases, and LLM judges carry measurable,
sometimes hidden, biases. **Correlation is not calibration** — a judge that
correlates strongly with GPT-4 can still score 53% on a unit-test set where a
better-calibrated judge scores 81%. So the recommendation is a *stack*, plus a
**meta-eval gate on the stack itself** (the part most teams skip).

## The judge is biased — design around it

From the MT-Bench study and corroborating work, LLM-as-judge bias is real and
partly invisible:

- **Position bias** — verdicts flip on answer order. Mitigation (the paper's own):
  **call the judge twice with positions swapped; count a win only if it holds both
  ways**, else tie.
- **Verbosity / self-enhancement bias** — judges over-score longer answers and
  their *own* outputs (and, more generally, low-perplexity *familiar* style).
- **Unfaithful rationalization** — judges shift verdicts on injected
  provenance/recency cues (~30% verdict-shift) while their chain-of-thought never
  admits the cue. **A judge's explanation is not a reliability proof.**

Two rules fall out, both decision-critical:
1. **Different-family judge.** Generator and judge must be different model families
   — the self-preference bias is toward the judge's own style.
2. **Never use a judge's CoT justification as proof** that an answer is grounded.

## The metric stack

| Layer | Metric | What it gives | Caveat |
|---|---|---|---|
| Faithfulness | **RAGAS** faithfulness = verified-statements / total-statements (NLI per atomic claim) | The answer-side mirror of extraction verification | Validation used only 2 annotators; penalizes faithful-but-extra statements — trend signal, not verdict |
| Retrieval | **RAGAS** context precision/recall | Did chunking surface the right material? | reference-free; meta-eval the judge |
| Statistical honesty | **ARES** + Prediction-Powered Inference | *Confidence intervals* (not point estimates) → tells you when the corpus is too small/novel to trust | Maintenance uncertain — confirm it runs before depending on PPI |
| Recall coverage | **TREC AutoNuggetizer** nuggets | "Must-cite" clause/value coverage (nuggets = the values a correct answer must cite) | research code; pilot |

## Citation grounding & hallucination detection

Two complementary, primary-source-backed checks — cheaper than full LLM-judge
runs, so they belong in the continuous tier:

- **ALCE (reference-based, NLI):** **citation recall** (is the claim fully
  supported by its cited passages?) + **citation precision** (are cited passages
  actually relevant?). Every answer over a standards corpus *cites*, so each cited
  clause can be auto-checked for entailment. Limit: NLI can't model "partial
  support," depressing precision — read a precision dip as a possible artifact.
- **LettuceDetect (reference-free, MIT):** a ModernBERT token-classifier flagging
  unsupported spans, **79.22% F1 on RAGTruth**, ~30× smaller than prompt-based
  detectors, no API. The cheap, deterministic-ish grounding signal to run on
  *every* answer.

## The golden question set

No primary-source "law" for size; the credible pattern is **silver → gold**:
synthesize candidates, promote via SME review.

- **Cheapest high-quality source = your own verified store.** Generate Q/A directly
  from already-`verified` clauses/tables, so the **answer key *is* the verified
  cell** — ties the eval to provenance for free.
- **Floor ~150 SME-verified questions** (ARES's PPI needs ~150+ for a trustworthy
  interval; GroUSE's meta-eval uses 144).
- **Prevent two leaks:** (1) *pretraining leakage* — prefer corpus-specific values
  (an exact threshold in a specific edition) the model can't answer from memory;
  (2) *index leakage* — keep golden Q/A **out of the ingest path and chunk store**
  (gate ingest to exclude the eval directory).
- **Include unanswerable questions** — does the system correctly *decline*?
  Wrongly-declining and failing-to-decline are first-class failure modes.

## Regression eval in CI (per ingest tick)

A corpus change — new ingest, re-parse, watermark fix — must not silently lower
answer quality:

- Pin the golden set; on each tick re-run retrieval+answer, compute the stack,
  **fail the build on regression beyond threshold** vs the last good run (the
  answer-side analogue of doc 03's diff-size assertion).
- Use **promptfoo (MIT)** or **DeepEval (Apache-2.0)** as the *harness* (CI gate),
  calling RAGAS/LettuceDetect as *metric components* — component-not-framework.
- With ARES confidence intervals, gate on the *interval* dropping, not a noisy
  point estimate — fewer false alarms on small deltas.

## Tiered cadence

| Tier | Cadence | Signals | Cost |
|---|---|---|---|
| Continuous | every answer / tick | LettuceDetect span flags; ALCE NLI citation recall/precision; retrieval hit-rate | low, local |
| CI gate | per tick on golden set | RAGAS faithfulness + context precision/recall, **cross-family + position-swapped judge** | API-metered |
| Periodic deep | release / monthly | ARES PPI intervals; TREC nugget recall; SME spot-audit | human + heavy LLM |

## Tooling verdicts (feed into doc 12)

| Tool | License | Verdict | Why |
|---|---|---|---|
| RAGAS | Apache-2.0 | **ADOPT as component** | Faithfulness + context precision/recall; never trust scores blind — meta-eval the judge |
| LettuceDetect | MIT | **ADOPT** | Cheap continuous span-level grounding, no API |
| promptfoo | MIT | **ADOPT (CI harness)** | Declarative YAML assertions + regression matrix |
| DeepEval | Apache-2.0 | **ADOPT (CI harness)** | pytest-style; runs metrics with self-hosted/open judges |
| ARES | Apache-2.0 | **PILOT** | The PPI confidence-interval feature; confirm it still runs |
| GroUSE (method) | code public, license UNVERIFIED | **ADOPT the method** | 144-unit-test judge meta-eval; pilot the code |
| TREC AutoNuggetizer | research code | **PILOT** | "Must-cite" coverage for standards answers |

## Candidate practices (need a pilot before minting as a GP)

- **Different-family judge** + position-swapped double-judging, counting only
  consistent verdicts.
- **Judge meta-eval gate:** a ~150-case GroUSE-style unit-test set the *judge* must
  pass before its scores are allowed to gate CI.
- **Provenance-anchored golden set** derived from verified cells; eval set kept out
  of the ingest/index path.
- **Tiered cadence** (continuous span-check → CI metric gate → periodic deep eval)
  wired per ingest tick.
- **Span-flag-before-score:** run cheap LettuceDetect first; escalate only flagged
  answers to expensive LLM-judge faithfulness.

## ACE #61 eval exclusion hook

ACE golden and silver eval cases are storage-form `eval_case` records, not ingest
inputs and not retrieval chunks. The #61 contract requires them to stay outside
both the ingest path and the chunk store so regression tests cannot leak answer
keys into retrieval.

ACE reporting uses `eligible_candidate_items`, `successful_routed_items`,
`total_classified_items`, and `hard_excluded_items` from the #61 success-metric
contract. Zero-denominator states are explicit outcomes, not silent pass/fail
shortcuts.

For ACE wave 1, generated JSON and source-tree noise are eval exclusions, not
negative retrieval examples. Golden/silver cases may test that the classifier
excludes them, but the excluded artifacts do not enter the retrieval corpus or
answer-key path. Kept text/config/code-doc rows must expose route target,
candidate class, `extraction_estimate` / `extraction_yield`, and visibility so evaluation can separate
classification failures from extraction failures.

*Snapshot 2026-06. Re-run the doc 12 trust rubric before adopting. Full
primary-source citations and the bias evidence base: issue #16.*
