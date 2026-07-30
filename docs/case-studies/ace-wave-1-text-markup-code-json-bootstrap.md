# ACE Wave 1 Text, Markup, Code, and Small JSON Bootstrap

This page is a synthetic-fixture methodology report for issue #52. It does not
contain ACE source inventory, private row counts, raw file names, source
snippets, measured corpus results, or publication output.

## Scope

Wave 1 covers LLM-native text, markup, code-adjacent documentation, and small
JSON/config metadata. The bootstrap lane routes every candidate to one of the
closed targets imported from the wave-0 schema:

| Route target | Wave-1 use |
|---|---|
| `public_llm_wiki` | Allowed only after affirmative public clearance and public-output canary evidence |
| `private_sidecar` | Hand-authored text or markup that is useful but not public-cleared |
| `metadata_only` | Small config JSON and code documentation where metadata is the useful knowledge |
| `excluded_no_ingest` | Generated JSON, lockfiles, minified/source-tree noise, and hard exclusions |

## Synthetic Fixture Matrix

| Fixture | Expected class | Expected route | Rationale |
|---|---|---|---|
| `manual-config.json` | `small_config_json` | `metadata_only` | Hand-authored config metadata is useful but not prose ingest |
| `generated-repetitive-json.json` | `generated_repetitive_json` | `excluded_no_ingest` | Repeated object templates plus generated timestamp signal cache-like output |
| `generated-path-key-cardinality-json.json` | `generated_repetitive_json` | `excluded_no_ingest` | High cardinality of generated path-like keys is cache/index output, not hand-authored config |
| `generated-lockfile-like.json` | `generated_lockfile_like_json` | `excluded_no_ingest` | Package-lock shape is dependency state, not knowledge content |
| `hand-authored-markdown.md` | `hand_authored_markup` | `private_sidecar` | Useful prose remains private unless separately public-cleared |
| `hand-authored-rst.rst` | `hand_authored_markup` | `private_sidecar` | Markup structure is retained with `extraction_estimate` / `extraction_yield` fields |
| `source-tree-docstring.py` | `code_documentation` | `metadata_only` | Module docstring is extracted as metadata; source tree is not bulk-ingested |
| `source-tree-vendored-minified.js` | `source_tree_noise` | `excluded_no_ingest` | Minified or vendored code is noise for this lane |

## Metric

`% ingested success` uses
`successful_routed_items / eligible_candidate_items * 100`. Hard exclusions are
reported separately as `% excluded`; generated/noise exclusions are not treated
as extraction failures.

## Gates

Operational manifest-backed sampling stays fail-closed unless a trusted #62
evidence pointer is present through the #70 registry and the #67 bounded
sampling caps pass. Public route selection requires the #63 public-output canary
over the exact public surface. Durable stores, retrieval metadata, lifecycle
state, and persistent metrics require #61 evidence.
