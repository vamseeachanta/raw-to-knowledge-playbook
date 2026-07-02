# Chunking & Embedding: Holding Trust into Retrieval

The pipeline ends at a *verified store* — but the README promises an
**LLM-queryable knowledge base**. The bridge is chunking + embedding, and it is
where most RAG systems silently lose the fidelity the rest of the pipeline
fought for. The creed still holds: *trust nothing by default* — including the
chunker that slices a table in half and the embedding that can't tell `565`
from `585`.

Research and primary sources for every claim here: **issue #15**.

## The regime split (the finding that changes the default)

How you should chunk depends on the retrieval *task*, and the two tasks invert
the ranking:

| Task | Question | Winner |
|---|---|---|
| **In-corpus** | "*Which* document/standard answers this?" | Contextualized / late chunking *helps* (+22–27% reported) |
| **In-document** | "Find clause 7.3.2's allowable stress *in this standard*" | **Structure-aware wins; late chunking *degrades* it** |

A standards/engineering corpus lives mostly in the **in-document** regime
(precise clause/table lookup). So the default that travels from generic RAG blogs
— "add late chunking, it's a free win" — is the *wrong* default here. Use
structure-aware chunking; reach for late chunking only on the corpus-wide "which
document" hop.

## 1. Structure-aware chunking — never slice a table

**Docling `HybridChunker`** is the documented best fit and is license-clean: the
chunker lives in **`docling-core` (MIT)**, separate from Docling's AGPL-adjacent
reputation. It is one-chunk-per-element with headings/captions attached as
metadata, tokenizer-aware (splits only oversized chunks; merges undersized
siblings that share headings), and `repeat_table_header=True` repeats a table's
header in every piece a long table spans.

Rule: **a chunk boundary must never fall inside a table or split a row from its
header.** A table is the atomic unit; if it's too big for the embedding window,
serialize it row-wise with the header repeated, don't truncate.

## 2. Embedding — and the numeracy gap

Embeddings are **measurably bad at numbers**. Across 13 models, average retrieval
accuracy on numeric-comparison tasks is **~0.54 — barely above the 0.50 random
baseline**, worst on 4-digit integers like `1234`, because numbers are tokenized
as ordinary subwords so magnitude isn't encoded. LLM-based embedders beat encoder
ones by only ~5 points — *not* a fix. For a corpus full of `565,16 mm`,
`12.75 ksi`, `API 5CT`, dense vectors alone **cannot be trusted to discriminate
near values**.

Two mitigations, both cheap:
1. **Pair dense with lexical/sparse.** Hybrid (dense + BM25/sparse) lets an exact
   token — a standard number, a precise value — be retrieved lexically when the
   embedding blurs it. **BGE-M3 (MIT)** does dense + sparse + multi-vector in one
   model for exactly this reason.
2. **Keep the canonical numeric string verbatim** in chunk text *and* metadata, so
   exact-match retrieval can catch what the embedding can't.

License-screened open options (verify model cards before adopting):

| Model | License | Note |
|---|---|---|
| **Qwen3-Embedding** (0.6/4/8B) | Apache-2.0 | 32k ctx, Matryoshka dims, instruction-aware; 8B topped MMTEB multilingual (Jun 2025) |
| **BGE-M3** | MIT | dense+sparse+ColBERT in one — the hybrid answer to the numeracy gap |
| jina-embeddings-v3 | ⚠️ weights CC-BY-NC (verify) | the late-chunking reference model; check the card before commercial use |

No evidence found that any *general* open embedder is domain-adapted for
engineering-standards numerics — that remains an open gap, not a solved problem.

## 3. Carry the trust contract into every chunk

The provenance discipline of doc 07 must survive chunking, or retrieval re-opens
the door the pipeline closed:

- **`citation_id = {doc_id}@{version}#{content_hash}`** — pin the standard's
  *edition* and a content hash, so a chunk's citation breaks loudly when the
  underlying edition changes (the corpus already hit edition-collision bugs where
  editions share table IDs — failure A9/B10).
- **`parse_status` as a first-class, indexed, filterable metadata field** on every
  chunk (`provisional` | `verified` | `rejected`). Retrieval can then *prefer or
  hard-restrict to* `verified` cells — the chunk-level expression of "trust
  nothing by default." A provisional value must never be returned as if citable.
- Keeping **BM25 alongside dense** (mitigation 1) conveniently lets `citation_id`
  and standard-number tokens be retrieved lexically.

## 4. How to represent a table as a chunk

Measured, not stylistic. On an LLM-comprehension test across 11 formats,
**Markdown key-value** (each cell labeled with its column) scored **60.7%** vs a
plain **Markdown table 51.9%** and **CSV 44.3%** — but KV cost **2.7× the tokens**.
And **TableRAG beat naive text-chunked RAG by ≥10 points** on table-heavy
retrieval, because flattening a table into prose causes *structural-information
loss* and *loss of global view* (you can't aggregate across rows you've shattered).

Guidance: **don't flatten tables into prose.** Keep them structured; where token
budget allows and a table is decision-critical, the column-labeled KV
serialization measurably aids comprehension at a token cost — spend it on
high-value tables, not all of them.

## 5. Contextual Retrieval — real but conditional

Anthropic's Contextual Retrieval (prepend a 50–100-token LLM-generated context
blurb per chunk before embedding) reports large retrieval-failure reductions
(35–67%, the bigger number with a reranker). It is a **cross-corpus**
disambiguation aid (regime split, above) and it costs an LLM pass per chunk at
ingest. Pilot it on the "which document" hop; measure before paying the
per-chunk generation cost across the whole corpus.

## Tooling verdicts (feed into doc 12 Lane 7)

| Tool / pattern | License | Verdict | Why |
|---|---|---|---|
| Docling `HybridChunker` (`docling-core`) | MIT | **ADOPT** | Structure-aware, never-slice-a-table, header repetition |
| Late chunking (Jina) | Apache-2.0 (code) | **PILOT, in-corpus only** | Helps "which document"; *degrades* in-document clause lookup |
| Qwen3-Embedding | Apache-2.0 | **ADOPT (self-host)** | Strong MMTEB, permissive, long context |
| BGE-M3 | MIT | **ADOPT** | One-model hybrid (dense+sparse) — the numeracy-gap answer |
| jina-embeddings-v3 | ⚠️ weights license | **EVALUATE** | Verify CC-BY-NC weights terms first |
| Markdown-KV table serialization | pattern | **EVALUATE** | +9pts comprehension over markdown table, at 2.7× tokens — spend selectively |
| TableRAG-style structured retrieval | pattern | **PILOT** | ≥10pts over naive flattening on table queries |
| Contextual Retrieval (Anthropic) | technique | **PILOT** | Real but conditional; costs a per-chunk LLM pass |

## Candidate practices (need a pilot before minting as a GP)

- **Regime-aware chunking:** structure-aware (HybridChunker) for in-document
  clause/table lookup; reserve late/contextual chunking for the corpus-wide hop.
- **Hybrid dense+sparse by default** for any numeric/standards content, with the
  canonical numeric string kept verbatim in chunk text and metadata.
- **`parse_status` as filterable chunk metadata**, so retrieval can restrict to
  `verified` — the trust gate extended into the vector store.
- **Edition-pinned `citation_id`** = `doc@version#hash`, failing loudly on edition
  drift.
- **Don't flatten tables;** column-labeled KV serialization for decision-critical
  ones, budget permitting.

## ACE #61 chunk metadata hook

ACE wave work must bind retrieval chunks to the #61 knowledge-store contract
before any bulk indexing. Each chunk carries `citation_id`,
`logical_document_key`, edition/revision fields, `is_current`, an `as_of`
timestamp, `visibility`, lifecycle and parse status, a hash reference,
`structure_type`, `route_target`, and `logical_target_store`.

Tables stay structurally intact through chunking. A table chunk records that the
table was preserved; it must not be flattened into prose to make embedding
easier. Golden and silver eval cases are not retrieval chunks and remain outside
the ingest path and chunk store.

*Snapshot 2026-06. Models and benchmarks age fast — re-run the doc 12 trust
rubric before adopting. Full primary-source citations: issue #15.*
