# Implementation Review: Issue 61 Contract/Runtime

## Verdict

APPROVE after fixes.

## Initial Findings

- MAJOR: #65 route/store import was too shallow. Fixed by invoking the #65 schema validator from `scripts/validate_ace_knowledge_store_contract.py`.
- MAJOR: lifecycle event validation did not enforce exact transition reasons or rescreen evidence. Fixed with transition reason checks and storage drift reset validation.
- MAJOR: private provenance allowed-field policy was not closed. Fixed by requiring only `private_provenance_bundle_ref`, opaque refs, and no committed lookup material.
- MAJOR: retrieval chunk validation was presence-only. Fixed by validating route/store pairs, visibility, parse status, hash-reference shape, table preservation, and CLI chunk/eval record inputs.
- MAJOR: success metric validation accepted unknown wave classes and polluted control records. Fixed by importing #65 wave classes, enforcing zero control counts, and validating exclusion metric fields.

## Re-Review

No remaining findings.

Final reviewer verdict: APPROVE.
