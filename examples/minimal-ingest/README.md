# Minimal ingest example — the playbook on one table

The whole methodology, end to end, on a single synthetic table:

```
EXTRACT (deterministic)  →  PROVISIONAL  →  VERIFY (vision)  →  PROMOTE
   pdfplumber               trust nothing    cell-by-cell        verified
```

No corpus, no cron, no multi-agent fan-out — just the load-bearing idea
([README](../../README.md)): *extract deterministically, verify, trust nothing
by default.* It runs offline with one permissive dependency.

## Run it

Requires [`uv`](https://docs.astral.sh/uv/) (deps are declared inline via
PEP 723; `uv` fetches them into an isolated env — nothing to pre-install):

```bash
uv run ingest.py                 # happy path  → VERIFIED, promoted
uv run ingest.py --inject-defect # simulate an OCR digit-substitution → DEFERRED
uv run ingest.py --check         # run + assert outputs match expected/ fixtures (CI)
```

Happy-path output:

```
EXTRACT  : 5 rows via pdfplumber (deterministic)
PROVISIONAL: out/provisional.csv  (sha256 source pinned: 712dd9673d21…)
VERIFY   : VERIFIED  (all cells match source)
PROMOTE  : out/verified.csv + page.md(verified)
```

Defect-path output — the gate **catches** a single perturbed cell and refuses to
promote, citing a *specific, falsifiable* mismatch (doc 03):

```
VERIFY   : DEFERRED  [A7-ocr-digit-substitution]  cell (row 4, col 2): page shows '565', CSV has '585'
PROMOTE  : held provisional; defect queued for re-extract
```

## What's real vs stubbed (read this — it's the honest part)

| Step | This example | Production (the rest of the repo) |
|---|---|---|
| Extract | **real** — pdfplumber (MIT, doc 12 ADOPT) | same family of deterministic extractors |
| Provisional gate | **real** — every extraction starts `provisional-unverified` | same status lifecycle (doc 03/07) |
| Verdict decision tree | **real** — closed-set verdicts, defect classes (doc 04) | same |
| **Vision comparator** | **STUBBED** — diffs the CSV against a committed `ground_truth.csv` standing in for "what the rendered page says" | a **VLM** compares a rendered page PNG ↔ CSV cell-by-cell |
| Queue / PR / cron | a single JSON row | per-domain queue, one PR per batch, 6-hourly cron |

To go live, replace `vision_compare()` in `ingest.py` with a real VLM call on a
rendered page image. **The gate around it does not change** — that separation is
the point: deterministic extraction and the provisional→verified contract are
fixed; only the comparator's intelligence is swapped in.

## Files

| Path | Role |
|---|---|
| `make_sample.py` | Generates `sample/allowable_stress.pdf` from **synthetic CC0** data (run once; PDF is committed). Never commit real copyrighted standards — doc 07 raw-source firewall. |
| `sample/allowable_stress.pdf` | The tiny born-digital source (one ruled table). |
| `ingest.py` | The four-step loop in ~120 lines. |
| `ground_truth/allowable_stress.csv` | Stand-in for the VLM's reading of the page — what `vision_compare()` checks against. |
| `expected/`, `expected_defect/` | Committed fixtures the `--check` mode asserts against. |
| `out/` | Generated artifacts (gitignored): `provisional.csv`, `queue_row.json`, `page.md`, `verified.csv`. |

## Why this shape

- **One permissive dependency.** pdfplumber is MIT and ADOPT-tier (doc 12); the
  example never pulls in an AGPL extractor or a framework runtime.
- **Synthetic source.** The PDF content is invented and CC0, so the repo carries
  zero licensed material while still exercising real table extraction.
- **Deterministic and offline.** Stubbing the VLM with a ground-truth diff keeps
  the example reproducible in CI — and makes the real-vs-mocked boundary explicit
  instead of hand-waved.
