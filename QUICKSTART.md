# Quickstart — your first ingest in ~15 minutes

This playbook is 13 dense docs. Before reading them, *run* the core idea once so
the rest has something to hang on. Everything below is backed by the runnable
[`examples/minimal-ingest/`](examples/minimal-ingest/) — no claim here is
aspirational.

## The one idea

> **Extract deterministically. Verify with vision. Trust nothing by default.**

A tool (not an LLM) copies the bulk content. Everything auto-extracted is
`provisional` until a vision pass checks it cell-by-cell and *promotes* it to
`verified`. That's the whole spine; the docs are details hung on it.

## Do it (≈5 min hands-on)

You need [`uv`](https://docs.astral.sh/uv/). Then:

```bash
git clone https://github.com/vamseeachanta/raw-to-knowledge-playbook
cd raw-to-knowledge-playbook/examples/minimal-ingest

uv run ingest.py                 # 1. extract → provisional → VERIFY → promote
uv run ingest.py --inject-defect # 2. watch the gate REFUSE a corrupted cell
```

Run 1 promotes a clean table to `verified`. Run 2 perturbs one number and the
verifier defers it with a *specific, falsifiable* reason — `page shows '565',
CSV has '585'` — instead of rubber-stamping. That refusal is the methodology.

Open `examples/minimal-ingest/out/page.md` to see the promoted artifact, and
`out/queue_row.json` to see the closed-set verdict that gates it.

## What you just saw, mapped to the docs

| You saw | It's really | Read next |
|---|---|---|
| `pdfplumber` pulling the table | Deterministic extraction beats LLM extraction (LLM gave ~2% coverage) | [doc 02](docs/02-pipeline-architecture.md) |
| `provisional-unverified` on every cell | Trust labeling; never cite a provisional value | [doc 07](docs/07-data-governance.md) |
| The VERIFY decision tree | The vision loop: verified / deferred / rejected | [doc 03](docs/03-verification-playbook.md) |
| `A7-ocr-digit-substitution` | One of 16 catalogued failure modes | [doc 04](docs/04-failure-modes.md) |
| A stubbed comparator | In production a VLM reads the rendered page | [doc 03](docs/03-verification-playbook.md) |

## Then scale up

The example is one table run by hand. The real campaign adds, in order:

1. **More raw types** — Office files, CSV/solver decks, imagery each get a lane
   ([doc 01 taxonomy](docs/01-document-taxonomy.md), [doc 13 flowcharts](docs/13-lane-flowcharts.md)).
2. **Batching + automation** — a per-domain queue, one PR per batch, a resumable
   cron ([doc 02](docs/02-pipeline-architecture.md)).
3. **Multiple agents** — bulk dispatch, vision verification, and adversarial code
   review split across providers ([doc 06](docs/06-multi-agent-orchestration.md)).
4. **Reusable skills** — once a workflow stabilizes it becomes a skill; templates
   live in [`skills/`](skills/) ([doc 08](docs/08-skills-catalog.md)).
5. **License + tooling discipline** — every tool screened before adoption
   ([doc 12](docs/12-tooling-landscape.md)).

New questions are tracked as research issues — the
[per-format program (epic #1)](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/1)
and the [strengthening program (epic #22)](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/22).
