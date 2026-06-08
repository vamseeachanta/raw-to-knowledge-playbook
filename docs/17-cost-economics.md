# Pipeline Cost Economics

The playbook's thesis is economic as much as technical: *deterministic tools do
the bulk; LLMs verify.* This doc attaches numbers to that claim so an adopter can
budget a campaign — and the headline reframes the whole pipeline:

> **Deterministic extraction is so cheap it is essentially free at the page
> level. Verification is the only line item that scales with spend. So the cost
> model is really a *verification-budget* model.**

Research and primary sources for every figure: **issue #18.** Every price is
**snapshot-dated 2026-06**; pricing ages fast — re-run the worksheet, don't trust
these dollar figures next quarter.

## 1. Extraction is near-free

Deterministic lanes are CPU-bound and cost **cents per thousand pages**; the
dominant cost is the engineer's wall-clock, not compute. Published throughput,
translated to $/1k pages at a placeholder **$0.05/vCPU-hr** (substitute your own):

| Lane / tool | License | Throughput (primary source) | ~$/1k pages |
|---|---|---|---|
| PyMuPDF native text | AGPL ⚠️ | ~182 pages/s (~0.0055 s/pg) | ~$0.0001 |
| pdfplumber | MIT | ~18 pages/s (~10× slower) | ~$0.0008 |
| Docling (structured) | MIT | median 0.79 s/pg; **p95 16.3 s** | ~$0.011 (median) / ~$0.23 (p95 tail) |
| PaddleOCR CPU (scans) | Apache-2.0 | ~3.74 s/image | ~$0.05 |
| olmOCR (VLM OCR, GPU) | Apache-2.0 | **< $200 / 1M pages** (primary) | **< $0.20** |

Every deterministic lane is **well under $1/1k pages**. Even olmOCR — the priciest
deterministic lane (a VLM on a GPU) — is <$0.20/1k. The cost model's center of
gravity is therefore **not** extraction. The slow tail (Docling p95 16.3 s/pg) is
the only extraction budget risk worth watching.

## 2. Verification — the only line that scales with spend

One VLM call per table: rendered table crop + extracted CSV → "does every cell
match?" Cost = input tokens (image + CSV + prompt) + output (verdict). Current VLM
pricing (input / output per 1M tokens, snapshot 2026-06; **Batch API −50%**):

| Model | Input | Output | ~$/table-verify (2.5k in, 200 out, batch) |
|---|---|---|---|
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | ~$0.00017 |
| GPT-4o-mini | $0.15 | $0.60 | ~$0.00025 |
| Claude Haiku 4.5 | $1.00 | $5.00 | ~$0.00175 |
| Claude Sonnet 4.6 | $3.00 | $15.00 | ~$0.0053 |
| Claude Opus 4.8 | $5.00 | $25.00 | ~$0.009 |

For a **10,000-table corpus**:

| Strategy | Haiku 4.5 (batch) | Opus 4.8 (batch) |
|---|---|---|
| Verify 100% | ~$17.50 | ~$90 |
| Verify 10% sample | ~$1.75 | ~$9 |
| Leave provisional (label only) | $0 | $0 |

**Verifying an entire 10k-table corpus cell-by-cell costs tens of dollars, not
thousands.** That reframes "trust nothing, verify with vision" from "arbitrarily
expensive" to "a rounding error against the human time already spent." The genuinely
expensive thing is *human* re-verification of disagreements — so the ROI lever is
**cheap-model first-pass triage + escalation** (doc 06's review lattice), not
paying frontier prices for every table.

> **Measure image tokens per provider before budgeting.** Image-token counts per
> table crop (~1,000–1,600, provider-specific) are the single biggest source of
> error in verify cost — use each provider's own token counter, never a hardcoded
> constant. (Marked UNVERIFIED in #18.)

## 3. Deterministic-vs-LLM crossover

The corpus's load-bearing fact: **LLM-as-primary extraction gave ~2% coverage**
where deterministic got the bulk. Quantified on a 1M-page corpus: the deterministic
lane costs **<$15 total compute**; LLM-as-primary (page → VLM → text) runs
**$500–$2,000 per 1M pages** — **30×–130× more expensive *and* worse coverage**.

LLM/VLM extraction earns its cost **only where deterministic coverage is ~0**:
(a) scanned/image-only pages with no text layer (the OCR/VLM lane, <$0.20/1k);
(b) born-degenerate layouts (rotated, watermark-contaminated, transposed); (c)
last-mile correction of a specific flagged table. **Never as the default lane** —
the creed, now with the ~30–130× multiplier attached.

## 4. Multi-provider arbitrage

Doc 06 routes bulk to one provider, verification to another. The cost basis:

- **Bulk dispatch is deterministic code, not an LLM** — there's no per-token "bulk
  LLM" cost to arbitrage. The arbitrage is in verification + orchestration.
- **Cheapest-capable routing:** 100% first-pass triage on Flash-Lite/GPT-4o-mini
  (~10–30× cheaper input), escalate only disagreements to a frontier model. Worked
  10k-table split ≈ **$11–12 total** vs ~$90 all-Opus.
- **Independence ≠ cost:** the second provider is chosen for blind-spot independence
  (doc 06); the happy accident is that the cheap-triage and independent-review
  models can be different vendors, so independence and cost align.
- **Subscription vs API:** much of this campaign ran on interactive-agent
  *subscriptions* where marginal token cost is the seat, not metered API — so a
  solo/small-team adopter's real marginal cost may be **$0 up to quota.** The
  worksheet's dollars are the **API-metered** basis; subscription users substitute
  "quota consumed" for "$".

## 5. Value-of-information — what's worth the verify spend

Because per-table verify is cents, the question is rarely "can we afford it" — it's
"where does a wrong cell cause real harm":

| Content class | Verify spend | Why |
|---|---|---|
| Load-bearing engineering tables (allowables, dimensions, material props) | **Verify cell-by-cell**, escalate to human | wrong digit → wrong design decision |
| Frequently-retrieved tables | **Verify** | error blast-radius scales with reads |
| Verbatim clauses / honest raw captures | **Ship as-is** | not parsed → no fidelity risk; provenance is the product |
| Structural noise (blank proformas, figure-as-table) | **Reject, don't verify** | don't pay to verify junk |
| Long-tail, rarely-read tables | **Ship provisional + confidence label** | VoI < verify cost; the label is the honest hedge |

The decision rule is **not** budget — it's `stakes × read-frequency`: verify when
`P(error) × cost-of-acting-on-error × read-frequency` exceeds the ~$0.01 verify
cost. For most corpora: **verify the load-bearing minority, ship the long tail
provisional.**

## Reusable cost-model worksheet

```
INPUTS (fill per campaign, date them):
  N_pages, N_tables          totals
  p_scanned                  fraction needing OCR/VLM lane
  vCPU_rate                  $/vCPU-hour (e.g. $0.05)
  verify_model               {flash-lite|4o-mini|haiku45|sonnet46|opus48}
  in_price,out_price         $/1M tok for verify_model (TABLE §2)
  img_tok                    image tokens/table crop (~1000-1600) [MEASURE, don't assume]
  ctx_tok,out_tok            csv+prompt (~1000), verdict (~200)
  batch                      1 if Batch API (×0.5)
  verify_frac                fraction of tables to verify (VoI-driven, §5)

EXTRACTION COMPUTE:
  det_secs_per_page          from §1 (0.0055 PyMuPDF … 0.79 Docling median … 16.3 p95)
  C_extract = N_pages × det_secs_per_page/3600 × vCPU_rate
  C_ocr     = p_scanned × N_pages × (0.20/1000)         # olmOCR primary <$0.20/1k

VERIFICATION:
  c_per_verify = ((img_tok+ctx_tok)/1e6×in_price + out_tok/1e6×out_price) × (batch?0.5:1)
  C_verify     = N_tables × verify_frac × c_per_verify

TOTAL_API_$ = C_extract + C_ocr + C_verify
  (subscription users: replace $ with quota-consumed; marginal $ may be 0 under seat)

SANITY CHECKS:
  - C_extract < $15 per 1M pages for native/Docling-median lanes
  - C_verify should DOMINATE total; if not, you're over-paying for extraction (wrong lane)
  - verify_frac=1.0 on Opus + large N_tables → switch first-pass to a cheap model + escalate
```

## Candidate practices (need a pilot before minting as a GP)

1. **Budget as a verification-budget model**, not an extraction model.
2. **Default verification to the Batch API** (−50%; verification is never
   latency-sensitive in a campaign).
3. **Two-tier verify routing:** cheap-capable model for 100% triage, escalate only
   disagreements (~8× cheaper than all-frontier on a worked 10k-table corpus).
4. **Measure image tokens per provider** before budgeting — the dominant error term.
5. **VoI gate:** verify load-bearing/high-read tables, ship the long tail
   provisional-with-label, reject structural noise.
6. **LLM/VLM extraction only where deterministic coverage ≈ 0.**
7. **Publish a dated worksheet, not dated numbers** (doc 12's snapshot convention);
   present both an API-metered and a subscription/quota column.

*Snapshot 2026-06. Prices from #18's primary sources (provider pricing pages,
Docling/olmOCR/PaddleOCR benchmarks). Re-run before trusting any dollar figure.*
