# ACE Manifest Freshness Drift Sentinel

The ACE wave portfolio uses manifest snapshots as public-safe evidence that a
downstream sampling run used a known source inventory state. Issue #62 defines
the reusable contract; issue #70 will import it into the operational sampling
firewall.

The public record keeps only opaque snapshot identifiers, manifest source keys,
status enums, validator command evidence, and pairwise drift verdicts. Exact
source statistics, raw digest material, private row counts, lookup material, and
host paths remain outside committed artifacts.

## Closed Manifest Set

The contract recognizes exactly these manifest source keys:

| Key | Role |
|---|---|
| `INDEX.md` | Root inventory index |
| `assets.json` | Asset manifest |
| `docs/master-index.jsonl` | Master record index |
| `_cad-index/index-summary.json` | CAD summary index |
| `_cad-index/cad-readability-index.tsv` | CAD readability index |
| `.ace-knowledge/index.db` | Knowledge-store index |

The validator treats any other pair as not comparable until a later reviewed
contract revision adds it.

## Authorization Rule

A #70 request may point to a #62 evidence artifact with `source_issue=62`,
`record_id`, and `evidence_artifact_ref`. It must not copy validator command
evidence, snapshot maps, pair verdicts, or reconciliation refs into the request
payload and call that fresh. The validator loads the referenced artifact and
checks the closed schema.

`sampling_allowed` requires every drift-eligible pair to be compatible and every
compatible pair to be backed by under-cap or sidecar evidence. `warning` and
`blocker` require reconciliation refs and still block authorization. `unavailable`
blocks authorization because evidence is absent.

## Synthetic Example

`tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json` is a
small public-safe fixture. Its snapshot identifiers use the `ams_` prefix plus
opaque hexadecimal suffixes and do not encode source identity.
