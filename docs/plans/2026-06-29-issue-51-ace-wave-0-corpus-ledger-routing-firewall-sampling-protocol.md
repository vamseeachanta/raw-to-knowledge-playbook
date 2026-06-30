# Plan for #51: ACE Wave 0 Corpus Ledger, Routing Firewall, and Sampling Protocol

> **Status:** draft
> **Complexity:** T3
> **Date:** 2026-06-29
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** PENDING final no-MAJOR round; historical rounds are retained as `scripts/review/results/2026-06-29-plan-51-*-r*.md`

---

## Resource Intelligence Summary

### Existing repo code/docs
- `docs/01-document-taxonomy.md` defines content-first routing and L0-L5 extraction levels; the ACE control plane must make those fields explicit before any wave ingests content.
- `docs/07-data-governance.md` and `docs/19-trust-boundary-and-private-mode.md` require raw sources off-repo, private data never crossing public boundaries, and provenance for derived material.
- `skills/README.md` lists the routing, triage, coverage, page-shape, and review skills that #51 must bind to each downstream wave.

### Related issues
- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) is the parent epic and requires every child to name method issues and skill groups.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) requires a ledger schema, route states, bounded sampling, exclusion classes, and closeout rules.
- [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) depends on this control plane for storage/lifecycle routing decisions.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) will consume this sampling contract for manifest freshness/drift checks.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will consume this route/token contract for public-output redaction canaries; #51 will define the interface but will not require the #63-owned scanner to exist or pass.

### Source inventory
- `ACE_SHARE_ROOT/INDEX.md` exists and warns that the share contains client data and business records.
- `ACE_SHARE_ROOT/assets.json` is the broad file manifest named by the issue body; #51 will not re-count it. Any exact entry count must come from a bounded/precomputed [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) snapshot sidecar before sampling.
- `ACE_SHARE_ROOT/_cad-index/index-summary.json` is the newer CAD-specific source of truth for CAD counts, generated after the broad manifest.
- `ACE_SHARE_ROOT/llm-wiki` exists as a holding-pen directory, but #51 will treat it as source inventory evidence only; no publication or durable write is authorized by this plan.
- The source-inventory proof below is host-local, metadata-only evidence from the current workstation. It is not a CI/review reproducibility requirement and is not correctness-critical for the validator, which must pass with `ACE_SHARE_ROOT` unset.

### Gaps identified
- No repo-local ACE corpus ledger schema exists yet.
- No validated closed route enum exists for `public_llm_wiki`, `private_sidecar`, `metadata_only`, and `excluded_no_ingest`.
- No bounded sampling contract exists to prevent unbounded share crawls through recursive shell/tool traversal, recursive code traversal, unrestricted manifest queries, custom full-manifest loops, or full-file hashing/counting of large manifests.
- No #51-owned public-surface self-scan exists for the control-plane artifacts themselves. This is distinct from the reusable public-output canary owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63): #51 must scan its own tracked docs, skill edits, review artifacts, and operator-fetched GitHub issue body/comment snapshots before commit/posting using generic repo-local patterns, but it must not implement private-deny-list certification or require the #63 canary.
- Existing policy examples in skill files can contain forbidden confidentiality-marker phrases; #51's scanner must provide narrow policy-example sentinels/allowlists so planned touched skills can self-scan without blanket exemptions while real private corpus leakage still fails.
- The downstream sampling contract needs an explicit per-wave `requires_manifest_snapshot_id` field so manifest-backed waves cannot sample before [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) supplies snapshot evidence.
- No validator CLI contract exists yet for the #51 self-scan. The validator must have separate modes for canonical public-surface scans, adversarial bad-fixture checks, and optional extra `--scan-public-path` inputs for operator-fetched issue body/comment snapshots before posting or status transition.
- Public provenance currently risks overexposing raw source hashes; public surfaces must not publish raw private source identifiers, raw private source hashes, private lookup keys, or private lookup maps. Public methodology docs may discuss these schema field names only in closed parseable contexts defined by the validator.
- Existing governance docs, sibling plans, and public methodology skills include mixed `sha256` references. #51 must classify every unique `path:line` hit surfaced by `rg -n "sha256|source hash|provenance pointer" docs skills --glob "*.md" --glob "SKILL.md"`, modify claims that describe raw source hashes/sha256 pointers as always safe, public-safe, public provenance, or public source references, and record no-change rationale for private-sidecar, LFS/OID, census, schema, validator, or private-ledger contexts. If a hit has both public-safe and private/schema/census language, `modify_public_safe_hash_claim` wins. Any assigned raw source hash, source-like digest value, or source hash table value must be modified/removed even when framed as a private-ledger example; no-change private-ledger examples may keep field names or synthetic placeholders only. After the sweep, raw `source_sha256` values are private-sidecar provenance while public artifacts reference only opaque `public_source_token` values.
- Source hashes have two separate threat models that must not be collapsed: a raw hash is not content, but it can still reveal membership in a private ACE corpus if an observer can compare candidate hashes or recognize repository-visible provenance. #51 will make an ACE-scoped governance decision that public ACE artifacts do not publish raw source hashes or sha256 provenance pointers as source references; broader docs may continue to discuss hashes as content-integrity metadata only when they do not claim public ACE source-reference safety.
- Durable ACE token allocation and the private token-to-source lookup map are not implemented by #51. #51 defines the schema, opaque token grammar, fixture generator, and validation contract; [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) owns durable private-sidecar storage and token lookup-map persistence; [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) owns public-output certification against that shared contract. #51 will record this ownership boundary so implementers do not treat fixture-only token generation as real corpus token allocation.
- The fixed source-evidence path list is not currently a named contract. #51 must define one authoritative `ACE_WAVE0_FIXED_SOURCE_EVIDENCE_PATHS` list and use it for the metadata-evidence positive fixture, so the prose inventory and fenced evidence rows cannot drift.
- The snapshot-gate matrix currently names #52-#60 as ingestion waves; #51 must also define an independent `wave_class`/`ingestion_wave` enumeration so a future child issue cannot escape [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) by omitting `requires_manifest_snapshot_id=true`.
- Historical review artifacts may include quoted bad examples from earlier adversarial findings. #51 must define which artifacts are public status evidence versus local/transient history, and any committed/posted retained artifact that contains source-bearing denied-command examples must be normalized or excluded from status evidence before scan.
- #51 will define logical target-store classes only. Physical private-sidecar storage locations remain owned by [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) before any durable output.
- The draft [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) plan must stay reconciled with #51 so public outputs use only opaque `public_source_token` references while raw source IDs, raw source hashes, private lookup keys, and private lookup maps remain private-only.

### Evidence

**Issue status** (verified 2026-06-29T21:49:42Z):
```
#51 OPEN ACE wave 0: corpus ledger, routing firewall, and sampling protocol labels=strengthening,lane:claude,priority:high
```

**Repo file existence** (verified 2026-06-29T21:49:42Z):
```
EXISTS docs/01-document-taxonomy.md
EXISTS docs/07-data-governance.md
EXISTS docs/19-trust-boundary-and-private-mode.md
EXISTS skills/public-private-routing/SKILL.md
EXISTS skills/content-triage-and-exclusion/SKILL.md
EXISTS skills/format-coverage-ledger/SKILL.md
EXISTS skills/page-shape-contract/SKILL.md
EXISTS skills/adversarial-verify-loop/SKILL.md
MISSING artifacts/ace-share-wave0-control-plane.md
MISSING docs/case-studies/ace-share-wave-0-control-plane.md
MISSING scripts/validate_ace_wave0_control_plane.py
MISSING scripts/validate_ace_public_artifacts.py
```

**Bounded source metadata proof** (point-in-time probe verified 2026-06-29T21:49:42Z; host-local existence/type probe over the fixed source list; no manifest materialization; exact size/mtime values are withheld from public artifacts and must move to a private/non-public evidence sidecar if needed):
```
EXISTS ACE_SHARE_ROOT/INDEX.md type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/assets.json type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/docs/master-index.jsonl type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/_cad-index/index-summary.json type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/_cad-index/cad-readability-index.tsv type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/.ace-knowledge/index.db type=file details=withheld_public
EXISTS ACE_SHARE_ROOT/llm-wiki type=directory details=withheld_public
```
Command form used a fixed source list and existence/type metadata checks against `ACE_SHARE_ROOT/<share-relative-path>` only; no recursive traversal, manifest load, row count, exact size/mtime publication, or full-file hash was run.

**Reproduction proofs**:
N/A - governance/planning issue; no runtime failure is alleged.

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | docs/plans/2026-06-29-issue-51-ace-wave-0-corpus-ledger-routing-firewall-sampling-protocol.md |
| Control-plane artifact | artifacts/ace-share-wave0-control-plane.md |
| Source-hash policy sweep report | artifacts/ace-source-hash-policy-sweep.md |
| Shared public contract | config/ace-public-output-contract.json |
| Generic public-surface deny-list | config/ace-public-surface-deny-list.json |
| Validator | scripts/validate_ace_wave0_control_plane.py |
| Review artifacts - historical rounds | scripts/review/results/2026-06-29-plan-51-*-r*.md |
| Review artifacts - final no-MAJOR round | PENDING; final paths will be recorded only after completed, normalized, non-empty provider artifacts exist |
| Review history and sidecars | Scan every `scripts/review/results/2026-06-29-plan-51-*.md` artifact kept for traceability plus same-directory same-stem sidecars with suffixes `.md.err`, `.err`, `.stderr`, or `.log` when present at commit/comment time; raw source paths in provider output must be tokenized before commit |

---

## Deliverable

A documented and CI-validated ACE wave-0 control plane defining the ledger schema, routing firewall, exclusion classes, bounded sampling protocol, and downstream wave issue/skill map. Implementation will be decomposed into small validator modules rather than one monolithic parser.

### Implementation Decomposition

- `scripts/ace_public_contract.py` will own JSON contract loading, private/public field classifications, and source-hash sweep classification helpers. It may import token grammar metadata from `scripts/ace_public_tokens.py`, but it must not define token-generation helpers, wrappers, or source-derived token functions.
- `scripts/ace_public_surface_scan.py` will own generic public-surface scanning, review-artifact/sidecar scanning, operator-fetched issue body/comment scans, and restricted bad-fixture harness checks.
- `scripts/ace_sampling_firewall.py` will own executable-context detection, bounded sampling grammar, metadata-evidence shape checks, and traversal/materialization denials.
- `scripts/validate_ace_wave0_control_plane.py` will orchestrate those modules, validate the wave map/ledger/route matrix, and expose the CI/CLI entrypoint.
- `tests/test_validate_ace_wave0_control_plane.py` will group tests by module boundary so token/contract, public-surface scanning, sampling firewall, and wave-map matrix failures can be debugged independently.

---

## Pseudocode

```text
authoring-time resource intelligence reads parent #50 and child issues #51-#63;
CI validators consume repo-tracked plans/fixtures only and do not require gh/network
define ACE_WAVE0_FIXED_SOURCE_EVIDENCE_PATHS exactly once:
  INDEX.md
  assets.json
  docs/master-index.jsonl
  _cad-index/index-summary.json
  _cad-index/cad-readability-index.tsv
  .ace-knowledge/index.db
  llm-wiki
  metadata-only evidence fixtures may use only these share-relative paths with
  details=withheld_public; prose source-inventory lists and fenced evidence rows must be
  generated from or validated against this exact set
define ledger required fields:
  source_id, source_sha256, public_source_token, private_lookup_key,
  share_relative_path_private_only, downstream_issue, wave_class, extension_family, content_class, sensitivity,
  route_target, target_store, extraction_level, lifecycle_state, verification_state,
  eval_data, validator_canary_contract_path, requires_manifest_snapshot_id,
  snapshot_id_evidence_rule, token_generation_method, success_metric_applicability,
  public_clearance_evidence, extraction_author, independent_public_reviewer,
  public_route_review_artifact, expected_yield,
  measured_success_numerator, measured_success_denominator,
  success_threshold, validation_command, exclusion_reason, method_issues, skill_group
define closed route enum:
  public_llm_wiki, private_sidecar, metadata_only, excluded_no_ingest
define closed logical target_store enum and route mapping:
  public_llm_wiki -> logical_public_llm_wiki
  private_sidecar -> logical_private_sidecar
  metadata_only -> logical_metadata_ledger
  excluded_no_ingest -> logical_no_store
  physical paths/repos for logical_private_sidecar are deferred to #61 and cannot be invented by #51
define closed verification_state enum:
  not_verified, validator_passed, independent_review_passed, rejected
record lifecycle_state only as a forward reference to the #61-owned lifecycle contract;
  #51 must not define lifecycle enum values or authorize lifecycle transitions
define route firewall:
  public_llm_wiki requires structural_public_review_evidence:
  affirmative public_clearance_evidence, nonsemantic public_source_token,
  verification_state=independent_review_passed,
  public_route_review_artifact, and independent_public_reviewer != extraction_author
  validator enforces structural evidence and author/reviewer non-equality only;
  genuine human/provider independence remains a publication approval gate owned by #63/user approval
  missing, ambiguous, or unverified sensitivity/public eligibility cannot route public_llm_wiki
define fail-closed exclusions:
  client_confidential, personal_pii, third_party_confidential, binary_noise, low_value
define opaque public token grammar:
  public_source_token matches pst_[0-9a-f]{32}
  public tokens must not contain path fragments, extensions, client/project/customer words,
  filenames, email-like strings, or private lookup keys
  token_generation_method must be random_csprng; #51 does not claim static proof that an
  arbitrary already-written token was random rather than a deterministic transform
  generate_public_source_token lives in scripts/ace_public_tokens.py, has no source/path/hash/key
  parameters, and uses secrets.token_hex(16)
  no other #51 module may expose a generate_public_source_token helper, wrapper, or
  source-derived token-generation API; contract/scanner modules may import the grammar or
  call the generator only through scripts/ace_public_tokens.py
  durable token allocation for real ACE rows, cross-wave uniqueness ledgers, and private
  token-to-source lookup-map persistence are not implemented by #51; #51 records the
  contract and fixture-generation rules, #61 owns durable private-sidecar lookup storage,
  and #63 owns public-output certification against the shared contract
  #51-owned good ledger/control-plane fixtures must carry a generation request marker instead
  of committed concrete pst_[0-9a-f]{32} values
  during validation, the wave-0 validator expands those request markers by calling
  generate_public_source_token(), validates grammar/uniqueness/method metadata on the
  generated in-memory rows, and rejects any hand-authored concrete public_source_token
  in good fixtures
  duplicate-token rejection is tested with an injected deterministic duplicate generator or
  monkeypatched token source inside the test harness; production generator remains zero-input
  CSPRNG and is not made deterministic
  deterministic hash/HMAC/encoding/truncation examples live only in bad fixtures and must
  fail the fixture harness; real public-output token certification remains a #63 gate
  generated public_source_token values must be unique across expanded ledger rows; duplicates fail validation
define shared public-output contract artifact:
  config/ace-public-output-contract.json records public_source_token grammar,
  private-only provenance fields, git-SHA exception contexts, content-pattern-restricted
  allowlist policy, and banned public source-reference fields
  config/ace-public-surface-deny-list.json records generic public-surface deny patterns
  both config files are strict JSON loaded with Python stdlib json; no PyYAML or YAML-only
  syntax is required in CI
  #51 creates and validates this config; #63 consumes this config rather than being parsed
  by #51 CI through brittle plan-prose matching
define ACE source-hash governance decision:
  raw source hashes and sha256 provenance pointers are not treated as content excerpts, but
  they can disclose membership in a private ACE corpus when a public observer can compare
  candidate hashes or follow repository-visible provenance
  for ACE public surfaces, source_sha256 and equivalent raw source-hash pointers are
  private-sidecar provenance only; public source references use public_source_token
  existing general governance language may keep hash/content-integrity examples only when
  the text does not claim that raw source hashes are public-safe ACE source references
for every wave issue #52-#63:
  record wave_class, extension family, inventory evidence, method issues, skill group, sampling rule,
  validator/canary contract path string, requires_manifest_snapshot_id, snapshot_id evidence rule,
  % ingested success formula, success_threshold, and validation_command
  downstream rows may reference planned validator/canary paths without requiring file existence;
  #51 implementation validates existence only for #51-owned files it creates
define independent wave_class enum:
  control_plane, ingestion_wave, storage_lifecycle_gate, manifest_freshness_gate, public_canary_gate
  requires_manifest_snapshot_id=true is required for every row with wave_class=ingestion_wave
  and forbidden for gate/control rows unless their own plan explicitly becomes an ingestion wave
  current ingestion_wave issue set must be exactly #52-#60; adding any child issue with an
  ingestion validator/skill binding but wave_class!=ingestion_wave fails validation
define wave-0 success sentinel:
  #51 has no content ingestion; control-plane rows set success_metric_applicability=not_applicable_control_plane,
  expected_yield=0,
  measured_success_numerator=0, measured_success_denominator=0,
  success_threshold=0, and validation_command to the wave-0 validator command
  validators must not divide by zero when success_metric_applicability=not_applicable_control_plane
  and issue is one of #51, #61, #62, or #63; downstream #52-#60 require computed_sample
define manifest gate field split:
  requires_manifest_snapshot_id is a per-issue sampling boolean owned by #51:
  #51/#61/#62/#63 are non-sampling control/gate issues and set it false;
  #52-#60 set it true before sampling
  docs/plans/ace-share-ingestion-wave-coordination.md also carries a Manifest gate text column;
  parent #50 pre-plan-review support keeps scripts/validate_ace_epic_wave_coordination.py
  aligned so control/gate rows can say "not applicable for own sampling; #62 gate applies
  to downstream sampling" while #52-#60 still require #62 snapshot_id evidence;
  #51 implementation consumes and scans that parent coordination support but does not modify it
require manifest-backed downstream waves to set requires_manifest_snapshot_id=true and
  reject sampling unless #62 approval/snapshot evidence is recorded
define closed snapshot gate matrix:
  #51 records requires_manifest_snapshot_id=false because wave 0 is metadata/control-plane only
  #52, #53, #54, #55, #56, #57, #58, #59, #60 require requires_manifest_snapshot_id=true
  #61, #62, #63 are cross-wave gates and record requires_manifest_snapshot_id=false
define sampling command grammar:
  allow only metadata stat probes and bounded helper calls that specify manifest source,
  seed/sort, row_cap, byte_cap, and max_files
  repo-local governance scans such as `rg -n "sha256|source hash|provenance pointer" docs skills --glob "*.md" --glob "SKILL.md"`
  are allowed only when their targets are repo-owned docs/skills/plans and they do not
  mention ACE_SHARE_ROOT, source manifests, source paths, pipes, redirects, or shell
  expansion over source material; they are not sampling commands
  classify executable context as fenced code blocks tagged shell/bash/sh/zsh/python/py,
  inline code beginning with a shell prompt, denied command, `python -c`, `uv run`,
  `subprocess`, `os.walk`, `.rglob`, `.read_text`, `open(`, `json.load`, or a pipe/redirection,
  and list/table cells whose first non-space token is a denied command
  reject executable contexts that combine denied
  traversal/materialization tools with ACE_SHARE_ROOT, assets.json, master-index.jsonl,
  index.db, _cad-index, or other ACE manifest/source tokens
  allow denied command names and private field names only in fixed methodology headings
  and the explicit repo-local governance scan shape above; all other allowed prose must
  avoid executable prefixes, source paths, pipes, redirects, or command flags
  ambiguous context fails closed and must be rewritten as bounded helper prose or fixtures
require ACE_SHARE_ROOT plus share-relative paths in scripts/tests
require public surfaces to use public_source_token only for source references; allow literal
  private field names only in closed schema/policy discussion contexts, and reject raw
  private source-id/hash assigned values, share-relative private path values,
  private lookup key values, and private lookup maps in public/comment/review surfaces
define the public-output canary input contract consumed by #63 without invoking #63's scanner
scan #51 public surfaces before commit/comment:
  artifacts/ace-share-wave0-control-plane.md, artifacts/ace-source-hash-policy-sweep.md,
  config/ace-public-surface-deny-list.json, config/ace-public-output-contract.json,
  .github/workflows/validate.yml, scripts/ace_public_tokens.py,
  scripts/ace_public_contract.py, scripts/ace_public_surface_scan.py,
  scripts/ace_sampling_firewall.py, scripts/validate_ace_wave0_control_plane.py,
  tests/test_validate_ace_wave0_control_plane.py, tests/fixtures/ace-wave0-control-plane/good/,
  touched skills, this plan, the #63 plan, docs/plans/README.md,
  docs/plans/ace-share-ingestion-wave-coordination.md, every retained plan-51 review artifact,
  scripts/validate_ace_epic_wave_coordination.py, tests/test_validate_ace_epic_wave_coordination.py,
  same-stem `.md.err`, `.err`, `.stderr`, and `.log` sidecars present at commit/comment time,
  and operator-fetched issue body/comment snapshot files
define forensic bad-fixture handling:
  tests/fixtures/ace-wave0-control-plane/bad/ is not part of the canonical passing public-surface set;
  it is a restricted adversarial fixture root consumed only by tests expecting validation failure
  every bad fixture must declare expected_failure, synthetic_only=true, and forbidden_pattern_class;
  the fixture harness rejects raw host/share path patterns, synthetic private-like identifiers,
  and any unclassified arbitrary content; real client/project/internal-name detection is #63
  no blanket path exemption is allowed: if a bad fixture is copied into any public-surface scan path,
  the public-surface scanner must fail it
require review artifact evidence:
  final plan-review evidence may cite only completed, normalized, non-empty review artifacts
  that contain a recognized verdict section; in-flight zero-byte stdout/stderr placeholders
  are invalid and must not be used for approval or status transitions
define docs publication boundary:
  docs/plans/ is already a public methodology surface under MkDocs and must be treated as
  published; this plan, the #63 plan, README, coordination docs, and committed/cited
  status-evidence review artifacts must pass #51 generic self-scan before commit/posting
  #51 must not create docs/case-studies/ace-share-wave-0-control-plane.md, docs/index.md
  links, mkdocs nav entries, or any docs/** copy of the control-plane artifact before #63
  approval/canary evidence; publication of the control-plane artifact is a #63-owned future
  transaction
  use content-pattern-restricted scanner self-safety allowlists for fixed policy-example phrases
  in skill files; never use author-controlled arbitrary line sentinels or blanket file/path
  exemptions, and verify marker-wrapped synthetic private-like identifiers still fail
allow metadata-only source evidence fixtures:
  the scanner allows only the exact fenced evidence shape
  `EXISTS ACE_SHARE_ROOT/<fixed-source-path> type=<file|directory> details=withheld_public`
  for the fixed source-list paths named in this plan; the same ACE_SHARE_ROOT path-bearing
  shape fails in executable commands, arbitrary prose, unlisted source paths, private content
  snippets, or any row that publishes exact size, mtime, row count, digest, or content
pair scanner allowlists with negative fixtures:
  any new policy-example phrase in touched skills must be present in the committed allowlist
  and paired with a negative fixture proving arbitrary sentinels and generic leak patterns
  still fail
define public-surface scanner field-name policy:
  literal schema field names such as source_id, source_sha256, private_lookup_key, and
  share_relative_path_private_only are methodology terms and may appear in plans,
  coordination docs, artifacts/ace-share-wave0-control-plane.md,
  artifacts/ace-source-hash-policy-sweep.md, skill instructions, validator constants, tests,
  and the designated policy/schema config files config/ace-public-output-contract.json
  and config/ace-public-surface-deny-list.json
  config files may contain these field names only as string enum/list values describing
  private-only or banned-public fields; JSON/YAML objects that assign real private values,
  maps from private lookup keys to source identifiers, path-bearing values, or raw digests
  still fail
  assignments, JSON/YAML key-value pairs, table rows containing real values, private
  lookup maps, path-bearing values, and source-like raw digests are rejected everywhere;
  git commit SHAs are allowed only in explicit governance contexts such as Reviewed commit,
  reviewed_tree_sha, marker_commit_sha, or review metadata, and never as source_sha256 values
  no author-controlled sentinels, arbitrary line allowlists, or blanket file/path exemptions
reconcile #63 public-output plan contract:
  update docs/plans/2026-06-29-issue-63-ace-public-output-redaction-and-identifier-canary.md
  so config/ace-public-output-contract.json is the authoritative source for source-token
  grammar, private-only fields, git-SHA exceptions, allowlist policy, and banned public
  source-reference fields; any #63 prose lists are explicitly non-authoritative examples
  loaded from or subordinate to the shared config, and contradictory local constants fail
reconcile existing governance docs and public methodology skills:
  run `rg -n "sha256|source hash|provenance pointer" docs skills --glob "*.md" --glob "SKILL.md"`
  dedupe hits by canonical path:line before classification
  classify each hit in artifacts/ace-source-hash-policy-sweep.md as:
    modify_public_safe_hash_claim when it says a raw source hash/sha256 pointer is
    always safe, public-safe, public provenance, public source metadata, repository-visible
    provenance substitute, or a public source reference
    no_change_private_context when it is an LFS/OID example, private-sidecar provenance,
    attachment/manifest census field, schema-field-name discussion, validator metadata,
    or sample private ledger row and does not make a public-safety/source-reference claim
    and does not publish an assigned raw source hash, source-like digest value, or source
    hash table value
  if one hit has both public-safety/source-reference language and private/schema/census
  language, modify_public_safe_hash_claim takes precedence over no_change_private_context
  if one hit contains an assigned raw source hash/source-like digest value, modify/remove
  takes precedence even when the surrounding prose calls the row private-sidecar-only
  update every modify_public_safe_hash_claim so raw source_sha256 values are
  private-sidecar provenance, not public-safe source references; public artifacts use
  public_source_token only
define #51 generic self-scan boundary:
  #51 implements only repo-local generic public-surface self-scan for the artifacts it
  creates/touches, including artifacts/ace-share-wave0-control-plane.md,
  artifacts/ace-source-hash-policy-sweep.md,
  scripts/ace_public_tokens.py, scripts/ace_public_contract.py,
  scripts/ace_public_surface_scan.py, scripts/ace_sampling_firewall.py,
  scripts/validate_ace_wave0_control_plane.py, tests/test_validate_ace_wave0_control_plane.py,
  tests/fixtures/ace-wave0-control-plane/good/, config/ace-public-output-contract.json,
  config/ace-public-surface-deny-list.json, .github/workflows/validate.yml, touched skills,
  the #51 plan, the #63 plan, README/coordination planning surfaces, parent coordination
  validator files, committed/cited review artifacts, same-stem review sidecars present at
  commit/comment time, and operator-fetched issue body/comment snapshots
  it does not load private deny-lists, does not certify real public exposure, and does not
  duplicate the #63 public-output scanner
  real private-identifier denial using maintained client/project/internal-name lists,
  private deny-list loading, non-repo containment checks, and publication/comment
  certification are owned by #63
define validator CLI:
  local/operator commands use `UV_CACHE_DIR=.claude/state/uv-cache uv run ...`;
  bare `uv run ...` is CI-only when CI owns the uv cache
  `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_control_plane.py`
  scans the canonical #51 public surfaces and fixture-backed control-plane contract using
  committed generic and fixture deny patterns; it is explicitly not public-exposure certification
  `--scan-public-path <path>` adds operator-fetched issue body/comment snapshot files or other #51 public surfaces
  for generic self-scan only
  `--scan-fixture-root tests/fixtures/ace-wave0-control-plane/bad` runs the expected-failure
  fixture harness and never marks those files as canonical public surfaces
  the CLI rejects private-deny-list flags in #51 so users cannot mistake it for #63
  publication certification
  CI must pass without ACE_SHARE_ROOT mounted by validating repo fixtures/docs only
define review artifact evidence:
  active review artifact paths must resolve under scripts/review/results, be non-empty,
  and parse the authoritative verdict value immediately under the first `## Verdict`
  heading, or on the same `Verdict:`/`- **Verdict:**` line, as APPROVE, MINOR, or MAJOR;
  implementations must ignore verdict words that appear later in findings, prose,
  retrieval notes, or disagreement tables;
  UNAVAILABLE provider artifacts may be retained as history but do not count as provider
  review evidence for status:plan-review or as review evidence supporting user approval
  final status-transition review artifacts must record the reviewed plan path,
  reviewed_commit_sha, reviewed_tree_sha, and reviewed_plan_blob_sha; all active-provider
  artifacts and the disagreement report must refer to the same reviewed draft identity
  local dirty-working-tree reviews are exploratory only and cannot support status transition
  final status-transition evidence scans only committed/posted review artifacts and
  same-stem sidecars cited in the evidence comment; older local r*-round artifacts are
  either normalized and committed as public history or treated as transient local history
  and excluded from status evidence
define degraded plan-review quorum:
  provider quota/provider outages may degrade T3 to a disclosed two-active-provider quorum
  under the AGENTS cross-review rule
  Gemini noninteractive auth/config failure is not a quota outage and does not automatically
  authorize downgrade; status:plan-review is blocked until Gemini is restored or the user
  explicitly approves a one-round degraded review quorum after seeing the auth-failure
  evidence
  under an allowed degraded quorum, status:plan-review is allowed only when Claude and Codex
  both return fresh no-MAJOR verdicts on the same committed post-patch draft and Gemini is
  recorded as UNAVAILABLE; if either active provider returns MAJOR, the plan remains draft-only
  if Gemini becomes available in the same review round, its fresh verdict is included and
  must also be no-MAJOR before status:plan-review
define review artifact normalization:
  raw provider stdout/stderr is transient local input and is not committed when it contains
  private paths or identifiers; committed review artifacts are normalized public copies with
  only path/identifier token substitutions and source-bearing denied-command example
  tokenization applied
  normalization must record a short note in the artifact or disagreement report and verify
  the authoritative verdict before and after normalization is identical; verdict lines must
  not be hand-edited except for path tokenization outside the verdict value
  review prose may quote a bad-command finding only after executable source-bearing examples
  are replaced with neutral tokens such as <DENIED_TRAVERSAL_EXAMPLE>
require every closeout to update a playbook doc/skill or file a follow-on issue for method gaps
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | artifacts/ace-share-wave0-control-plane.md | Durable ACE ledger/routing/sampling contract kept outside MkDocs publication surfaces until #63 |
| Create | artifacts/ace-source-hash-policy-sweep.md | Public-safe classification report for every `sha256`/source-hash/provenance-pointer hit in docs and public methodology skills, with modify/no-change rationale and dual-purpose-hit precedence |
| Create | scripts/ace_public_tokens.py | Reusable zero-source-input CSPRNG public token generator consumed by the wave-0 validator and downstream canary plans |
| Create | scripts/ace_public_contract.py | JSON contract loader, private/public field classifier, and hash-policy helper module; token generation remains exclusively in `scripts/ace_public_tokens.py` |
| Create | scripts/ace_public_surface_scan.py | Generic public-surface scanner, review-artifact scanner, issue body/comment scan helper, and restricted bad-fixture harness |
| Create | scripts/ace_sampling_firewall.py | Bounded sampling and executable-context firewall helper module |
| Create | scripts/validate_ace_wave0_control_plane.py | CI-checkable orchestrator for required fields, routes, wave bindings, module checks, and sampling constraints |
| Create | config/ace-public-surface-deny-list.json | Generic public-surface deny patterns for #51 self-scan; no private names committed and no private-deny-list certification in #51 |
| Create | config/ace-public-output-contract.json | Shared public token/redaction contract consumed by #51 and #63 instead of prose-matching another draft plan |
| Create | tests/test_validate_ace_wave0_control_plane.py | TDD unit tests for the wave-0 validator and workflow wiring |
| Create | tests/fixtures/ace-wave0-control-plane/good/ | Positive fixture control-plane doc, skill snippets, and bounded sampling examples |
| Create | tests/fixtures/ace-wave0-control-plane/bad/ | Restricted adversarial fixtures for expected-failure tests; not part of the canonical public-surface scan set |
| Reference | scripts/validate_ace_public_artifacts.py | Public-output safety gate owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63); #51 will define the route/token input contract only |
| Modify | .github/workflows/validate.yml | Run the new validator |
| Audit/conditional modify | docs/04-failure-modes.md | Classify `sha256` hits; modify only if a hit claims raw source hashes are public-safe source references |
| Audit/conditional modify | docs/05-good-practices.md | Classify `sha256` hits; modify only if a hit claims raw source hashes are public-safe source references |
| Modify | docs/07-data-governance.md | Reconcile raw source hash guidance so raw `source_sha256` stays private-sidecar provenance and public artifacts use `public_source_token` |
| Audit/conditional modify | docs/18-security-and-pii.md | Classify `sha256` hits; modify only if a hit claims raw source hashes are public-safe source references |
| Modify | docs/19-trust-boundary-and-private-mode.md | Reconcile trust-boundary examples so raw source hashes are not described as public-safe source references |
| Modify | docs/plans/2026-06-29-issue-50-ace-share-raw-to-knowledge-ingestion-waves-epic.md | Reconcile parent epic public provenance language with the #51 token/hash contract |
| Audit/conditional modify | docs/plans/2026-06-29-issue-*.md returned by the sweep | Classify every plan hit in the sweep report; modify only files whose hit claims raw source hashes are public-safe source references |
| Audit/conditional modify | public methodology skill files returned by the sweep, including touched skills | Classify every skill hit in the sweep report; modify only files whose hit claims raw source hashes are public-safe source references |
| Verify/conditional modify | docs/plans/2026-06-29-issue-63-ace-public-output-redaction-and-identifier-canary.md | Verify the draft #63 public-output canary plan treats `config/ace-public-output-contract.json` as authority and local lists as examples only; modify only if drift is found |
| Planning-surface update | docs/plans/ace-share-ingestion-wave-coordination.md | Record #51 review/status fields during plan-review and later closeout so the parent tracker does not remain stale; do not mark #51 implementation-ready before user approval |
| Planning-surface update | docs/plans/README.md | Record #51 plan status/review notes during plan-review and later closeout; do not mark #51 implementation-ready before user approval |
| GitHub issue metadata verification | https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51 | Verify and record that the live issue body is sanitized before `status:plan-review`, with no raw host paths, exact counts, or denied command examples against the private share |
| Deferred | docs/case-studies/ace-share-wave-0-control-plane.md | Do not create any `docs/` copy until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result |
| Deferred | docs/index.md | Do not link the control-plane artifact until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result |
| Deferred | mkdocs.yml | Do not publish the control-plane artifact in site navigation until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) has `status:plan-approved`, the local approval marker exists, the public-output canary is implemented, and the canary has a recorded passing-command result |
| Modify | skills/public-private-routing/SKILL.md | Add ACE route-state expectations |
| Modify | skills/content-triage-and-exclusion/SKILL.md | Add ACE exclusion-class expectations |
| Modify | skills/format-coverage-ledger/SKILL.md | Add ACE ledger expectations |
| Modify | skills/page-shape-contract/SKILL.md | Add ACE page/record shape expectations |
| Modify | skills/adversarial-verify-loop/SKILL.md | Require method-gap disposition in closeout |

---

## Parent #50 Pre-Plan-Review Support

The parent coordination validator support remains outside #51 implementation scope. Before #51 can be promoted to `status:plan-review`, the planning branch will keep `scripts/validate_ace_epic_wave_coordination.py` and `tests/test_validate_ace_epic_wave_coordination.py` green under approved parent [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) so the portfolio tracker can parse the final review artifacts, zero-denominator control rows, manifest gates, and route/token coordination fields. #51 implementation will not modify those files as part of the wave-0 validator deliverable.

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| test_ace_ledger_schema_requires_all_control_fields | Ledger schema covers #51 fields | Control-plane ledger table | Source token/hash fields, private lookup key, downstream issue, `wave_class`, eval data, route, target store, extraction level, lifecycle, verification state, success applicability, public clearance evidence, independent reviewer/review artifact fields, expected yield, measured success fields, threshold, and validation command present |
| test_ace_route_enum_is_closed | Route targets are closed-set | Route table | Exactly four route targets |
| test_target_store_mapping_is_closed | Logical stores are testable without inventing physical paths | Route/store matrix | Each route maps to exactly one logical target store; physical private sidecar paths are rejected in #51 |
| test_verification_state_enum_is_closed | Verification state cannot be hand-wavy prose | Verification table | Exactly `not_verified`, `validator_passed`, `independent_review_passed`, and `rejected` are allowed |
| test_ace_route_and_lifecycle_are_separate | Route targets do not mix with #61-owned lifecycle states | Route/lifecycle tables | #51 rejects lifecycle enum definitions and route aliases such as `private_only` or `excluded` |
| test_public_route_requires_structural_review_evidence | Public routing fails closed structurally | Ledger rows with missing or ambiguous sensitivity/public eligibility | `public_llm_wiki` is rejected unless public clearance evidence, `verification_state=independent_review_passed`, non-empty public-route review artifact, and reviewer != extraction author are present; this is only structural bookkeeping and does not prove human/provider independence |
| test_public_source_token_is_opaque | Public token grammar and negative examples cannot leak source identity | Token fixtures | Runtime-generated tokens must match `pst_[0-9a-f]{32}`, be unique, and carry `token_generation_method=random_csprng`; deterministic hash/HMAC/encoding/truncation examples are present only as bad fixtures and fail the fixture harness |
| test_public_token_generator_has_no_source_inputs | #51 fixtures do not hand-author concrete public tokens | `scripts/ace_public_tokens.py` generator signature, other #51 modules, and good fixtures | Token generator takes no source path/name/hash/key parameters, uses `secrets.token_hex(16)`, emits `pst_[0-9a-f]{32}`, no other #51 module defines or wraps token-generation helpers, and the validator rejects any committed concrete `public_source_token` value in good fixtures instead of expanding a generation request marker at validation time; durable token allocation and private lookup-map persistence are documented as #61-owned, not #51 fixture behavior; duplicate-token failure is exercised with an injected duplicate generator in tests |
| test_public_surfaces_reject_raw_source_hashes | Public provenance cannot reveal corpus membership | Public-surface fixtures | Allows schema field-name discussion in methodology prose, but rejects assigned raw `source_id`/`source_sha256` values, private lookup key values, private lookup maps, path-bearing values, and SHA-like digests in public surfaces |
| test_private_lookup_map_is_private_only | Public surfaces cannot contain private lookup maps | Control-plane/public-surface fixtures | Rejects `private_lookup_key` mappings in public docs, review artifacts, skills, or issue-comment body files |
| test_shared_public_output_contract_is_consumed | Downstream canary contract cannot drift from #51 | `config/ace-public-output-contract.json` and #63 plan text | Shared config contains token grammar, private-only fields, git-SHA governance exceptions, and allowlist policy; #63 references the shared config instead of redefining or contradicting it |
| test_public_config_field_names_are_closed_schema_context | Config self-scan does not block its own schema contract | `config/ace-public-output-contract.json`, `config/ace-public-surface-deny-list.json`, and negative config fixtures | Allows private field names only as string enum/list values in designated config files; rejects assigned private values, private lookup maps, path-bearing values, and raw digest values |
| test_existing_governance_docs_and_skills_do_not_publish_raw_hashes | Existing docs/plans/skills cannot contradict #51 token policy | Unique `path:line` hits from `rg -n "sha256|source hash|provenance pointer" docs skills --glob "*.md" --glob "SKILL.md"` plus `artifacts/ace-source-hash-policy-sweep.md` | Every hit is classified as `modify_public_safe_hash_claim` or `no_change_private_context`; modified claims no longer say raw hash pointers are always/public safe; dual-purpose hits with public-safety/source-reference language are modified; any assigned raw source hash/source-like digest value is modified or removed; no-change hits have an allowed private/LFS/census/schema/validator rationale without published digest values |
| test_repo_local_hash_sweep_command_is_allowed | Hash-governance scan is not mistaken for ACE source sampling | Plan and sampling-firewall fixtures | Allows the exact repo-local `rg` docs/skills hash-policy sweep shape; rejects `rg`, `find`, `jq`, `cat`, `wc`, or hash commands when combined with ACE_SHARE_ROOT or source manifest tokens |
| test_ace_sampling_protocol_blocks_unbounded_crawls | Sampling rules do not allow unbounded crawls | Sampling section and bad fixtures | Fails on unbounded `find`, `du`, `rg`, `fd`, `ls -R`, recursive glob, `os.walk`, unrestricted `jq`, custom full-manifest loop, or full-file hashing/counting of large manifests |
| test_ace_sampling_protocol_rejects_materialization_code | Python/shell fixture denial | Bad fixtures | Rejects `json.load`, `.read_text()`, `for line in open(...)`, `jq`, `jq length`, `jq -c`, `cat`, recursive `grep`, `wc`, `sha256sum`, recursive glob, `rglob`, and validator self-scan bypasses when pointed at ACE manifest/source paths |
| test_sampling_deny_tokens_are_scoped_to_executable_contexts | The plan can name denied commands without self-blocking | Prose policy section and bad executable fixtures | Allows denied command names only in fixed methodology headings without executable prefixes/source paths; rejects shell/python fenced blocks, inline code, list/table command starts, pipes, redirects, command flags, and ambiguous contexts when paired with ACE source/manifest tokens |
| test_metadata_only_evidence_block_is_allowed_but_not_generalized | The plan's own source evidence block can self-scan safely | Positive fixture with fenced `EXISTS ACE_SHARE_ROOT/<fixed-source-path> type=<file|directory> details=withheld_public` rows plus negative fixtures | Allows only fixed source-list existence/type rows; rejects unlisted ACE paths, rows publishing size/mtime/count/digest, executable/path-bearing commands, and private content snippets |
| test_ace_sampling_protocol_requires_caps | Sampling rules are bounded | Sampling section | Manifest source, seed/sort, per-bucket caps, max files, and max bytes are present |
| test_manifest_backed_waves_require_snapshot_id | #62 freshness gate is represented in #51 sampling contract | Wave map | #51/#61/#62/#63 are false, #52-#60 require `requires_manifest_snapshot_id=true`, and sampling is rejected without #62 snapshot evidence |
| test_manifest_snapshot_gate_matrix_covers_all_ingestion_waves | Future ingestion waves cannot escape #62 gate silently | Child issue map with independent `wave_class` enum | The `requires_manifest_snapshot_id=true` set exactly equals every row with `wave_class=ingestion_wave`; current ingestion_wave rows are #52-#60; any child with ingestion-wave executable bindings but missing `wave_class=ingestion_wave` or `requires_manifest_snapshot_id=true` fails |
| test_fixed_source_evidence_paths_are_authoritative | Metadata evidence rows cannot drift from prose inventory | `ACE_WAVE0_FIXED_SOURCE_EVIDENCE_PATHS` and metadata evidence fixture | Exactly the seven named share-relative evidence paths are allowed; prose inventory and fenced evidence rows must match the same set |
| test_ace_share_root_required | Host portability | Script/test examples | Uses `ACE_SHARE_ROOT` plus share-relative paths |
| test_control_plane_artifact_is_not_under_docs_before_publication_gate | MkDocs cannot publish the artifact before #63 | File paths and repo tree | The #51 control-plane artifact is under `artifacts/`; any `docs/**/ace-share-wave-0-control-plane.md` path fails until #63 approval evidence exists |
| test_bad_fixtures_are_forensic_inputs_not_public_surfaces | Negative fixtures do not self-block the public-surface scan | `tests/fixtures/ace-wave0-control-plane/bad/` with fixture metadata | Bad fixtures are rejected by the expected-failure harness, require `expected_failure`, `synthetic_only=true`, and `forbidden_pattern_class`, and are not included in the canonical passing public-surface scan set |
| test_public_surface_self_scan_blocks_raw_identifiers | #51 public-surface safety | Control-plane artifact, hash-policy sweep artifact, token generator, decomposed modules, validator, deny-list config, public-output contract config, workflow, good fixtures, plan, #63 plan, README, coordination doc, parent coordination validator/tests, touched skills, review artifacts, sidecars, and operator-fetched issue body/comment snapshots | Blocks raw paths, generic private-like identifier patterns, personal identifiers, proprietary snippets, raw source hash values, and private lookup maps before commit/comment/status transition; real client/project/internal-name deny-list coverage remains a #63 gate |
| test_public_surface_scanner_self_safety_for_policy_examples | Scanner avoids self-blocking policy text without bypasses | Touched skill files, committed allowlist entries, and bad leak fixtures | Allows only fixed policy-example phrase patterns in skills when a matching allowlist entry and negative fixture are present; rejects arbitrary sentinel use, rejects synthetic private-like identifiers even if marker-wrapped, and scans all planned touched skills without blanket exemptions |
| test_public_surface_scans_review_history_and_sidecars | Provider review artifacts are not an unscanned publication surface | Historical `plan-51-*.md` artifacts plus `.md.err`, `.err`, `.stderr`, and `.log` fixtures next to a review artifact | All retained review history and same-stem sidecars present at commit/comment time are scanned and leaks fail before commit/comment |
| test_review_artifacts_are_non_empty_and_verdict_bearing | Empty in-flight review placeholders cannot support plan-review | Review artifact fixtures | Rejects zero-byte artifacts, artifacts whose first verdict heading/line does not start with `APPROVE`/`MINOR`/`MAJOR`, verdict words that appear only later in prose, and `UNAVAILABLE` artifacts as provider-review evidence before status evidence or review evidence supporting user approval is accepted |
| test_status_review_artifacts_bind_to_reviewed_draft | Status-transition evidence cannot cite stale reviews | Final review artifacts and disagreement report | Requires reviewed plan path, reviewed_commit_sha, reviewed_tree_sha, reviewed_plan_blob_sha, and identical reviewed draft identity across all active-provider artifacts before `status:plan-review` evidence is accepted |
| test_degraded_quorum_requires_allowed_reason_or_user_waiver | T3 review cannot silently become T2 for local auth failure | Quorum metadata in disagreement report/evidence comment | Provider quota/outage may degrade with disclosure; Gemini auth/config failure blocks `status:plan-review` unless Gemini is restored or the user explicitly approves a one-round degraded quorum; active-provider MAJOR always blocks |
| test_issue_51_rejects_private_deny_list_flags | #51 cannot be mistaken for the #63 publication scanner | CLI fixtures | `--require-private-deny-list`, `--private-deny-list`, and `ACE_PRIVATE_DENY_LIST` use fail with a message that private-deny-list certification is owned by #63 |
| test_review_artifact_normalization_preserves_verdict | Public review artifacts can be redacted without changing verdict evidence | Raw/local and normalized review artifact fixtures | Only path/identifier substitutions and source-bearing denied-command example tokenization are allowed; authoritative verdict before and after normalization must match; verdict value is never hand-edited |
| test_validator_cli_default_scans_canonical_surfaces | Repo-local uv command is meaningful | Validator CLI | `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_control_plane.py` scans canonical #51 public surfaces and fixture contract |
| test_validator_cli_scans_issue_body_and_comment_snapshots | GitHub issue body/comment text can be checked before posting or status transition | Operator-fetched issue body/comment snapshot with `--scan-public-path <path>` | Extra scan path is checked with #51 generic patterns, and generic leaks fail without claiming #63 publication certification |
| test_validator_runs_without_live_ace_share_root | CI does not require the share mount | CI-like environment with ACE_SHARE_ROOT unset | Validator and unit tests use repo fixtures/docs only and do not dereference live share paths |
| test_wave0_success_fields_use_closed_zero_sentinel | Wave 0 does not invent ingestion success | #51 control-plane rows | `expected_yield`, numerator, denominator, and threshold are zero with the wave-0 validator command; downstream rows still require real formulas |
| test_zero_denominator_is_non_computing_sentinel | The success formula is not divided by zero | Control/gate issue rows | #51/#61/#62/#63 allow denominator zero only with `success_metric_applicability=not_applicable_control_plane`; #52-#60 reject zero denominator |
| test_manifest_gate_boolean_matches_coordination_text | Existing coordination validator cannot contradict #51 matrix | Coordination rows and validator fixtures | #51/#61/#62/#63 are non-sampling rows with no own snapshot_id requirement; #52-#60 require #62 snapshot evidence |
| test_every_downstream_wave_has_issue_skill_and_validator | #52-#63 each have bindings | Wave map | No missing issue, skill group, eval data, validator/canary contract path string, requires_manifest_snapshot_id, snapshot_id evidence rule, threshold, or validation command; downstream path existence is not required by #51 |
| test_public_canary_is_referenced_not_required | #51/#63 dependency boundary | Control-plane contract | #51 records the #63 scanner interface but does not require `scripts/validate_ace_public_artifacts.py` to exist or pass |
| test_wave0_workflow_runs_validator_and_tests | CI wiring exists | `.github/workflows/validate.yml` | Workflow invokes `scripts/validate_ace_wave0_control_plane.py` and `tests.test_validate_ace_wave0_control_plane` |
| test_skill_updates_include_ace_sections | Planned skill edits are substantive | Modified skill files | Required ACE route, exclusion, ledger, page-shape, and method-gap closeout sections/terms are present |
| test_closeout_requires_method_gap_disposition | Method gaps cannot disappear | Closeout rule | Requires doc/skill update or follow-on issue |

---

## Acceptance Criteria

- [ ] Ledger schema covers all fields named in #51 plus `downstream_issue`, `wave_class`, skill, `eval_data`, `validator_canary_contract_path`, `requires_manifest_snapshot_id`, `snapshot_id_evidence_rule`, `token_generation_method`, `success_metric_applicability`, public clearance evidence, `extraction_author`, `independent_public_reviewer`, `public_route_review_artifact`, `target_store`, `verification_state`, measured success numerator/denominator, success threshold, and validation command.
- [ ] Ledger distinguishes public `llm-wiki`, private sidecar, metadata-only, and excluded/no-ingest routing.
- [ ] The closed route-to-store matrix maps `public_llm_wiki` to `logical_public_llm_wiki`, `private_sidecar` to `logical_private_sidecar`, `metadata_only` to `logical_metadata_ledger`, and `excluded_no_ingest` to `logical_no_store`; #51 rejects physical private sidecar paths because [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) owns physical storage.
- [ ] The closed `verification_state` enum is `not_verified`, `validator_passed`, `independent_review_passed`, and `rejected`.
- [ ] `public_llm_wiki` is allowed only with structural public-review bookkeeping: affirmative public clearance evidence, opaque public token, `verification_state=independent_review_passed`, a non-empty public route review artifact, and `independent_public_reviewer != extraction_author`. The validator enforces structural evidence and author/reviewer non-equality only; it does not prove human/provider independence. Genuine independent-review confidence remains a publication approval gate owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) and user approval. Missing, ambiguous, self-reviewed, or unverified sensitivity/public eligibility routes fail closed to `metadata_only`, `private_sidecar`, or `excluded_no_ingest`.
- [ ] Public source token generation for #51 fixtures is validator-owned and enforceable: good fixtures carry generation request markers rather than committed concrete `pst_[0-9a-f]{32}` values; `scripts/ace_public_tokens.py::generate_public_source_token()` takes no source/path/name/hash/key inputs, uses `secrets.token_hex(16)`, and the validator expands those markers at runtime, verifies grammar/uniqueness/`token_generation_method=random_csprng`, and rejects hand-authored concrete public tokens in good fixtures. Duplicate-token rejection is exercised with an injected deterministic duplicate generator in tests, without making the production generator deterministic. `scripts/ace_public_contract.py`, `scripts/ace_public_surface_scan.py`, `scripts/ace_sampling_firewall.py`, and `scripts/validate_ace_wave0_control_plane.py` must not define token-generation helpers/wrappers or source-derived token APIs. #51 does not claim static cryptographic proof that arbitrary already-written public tokens were random rather than deterministic transforms; real public-output certification remains owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63).
- [ ] Public surfaces may mention literal private schema field names as methodology terms. Public surfaces reject assigned raw `source_id` values, raw `source_sha256` values, `share_relative_path_private_only` values, `private_lookup_key` values, private lookup maps, path-bearing values, and source-like raw digests; raw source hashes remain private-sidecar provenance only. Git commit SHAs are allowed only in explicit governance contexts such as `Reviewed commit`, `reviewed_tree_sha`, `marker_commit_sha`, or review metadata.
- [ ] `config/ace-public-output-contract.json` and `config/ace-public-surface-deny-list.json` are closed policy/schema contexts: they may contain private field names only as string enum/list values for private-only or banned-public fields, and they reject assigned private values, private lookup maps, path-bearing values, and raw digest values.
- [ ] `config/ace-public-output-contract.json` defines the shared public-token/redaction contract: `public_source_token` grammar, private-only provenance fields, git-SHA governance exceptions, content-pattern-restricted allowlists, and banned public source-reference fields. The draft [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) plan references this config instead of redefining or contradicting it.
- [ ] Every unique `path:line` hit from `rg -n "sha256|source hash|provenance pointer" docs skills --glob "*.md" --glob "SKILL.md"` is recorded in `artifacts/ace-source-hash-policy-sweep.md` with one of two outcomes: `modify_public_safe_hash_claim` for claims that raw source hashes/sha256 pointers are always safe, public-safe, public provenance, public source metadata, repository-visible provenance substitutes, public source references, or any assigned raw source hash/source-like digest value; or `no_change_private_context` for LFS/OID examples, private-sidecar provenance, attachment/manifest census fields, schema-field-name discussion, validator metadata, and sample private ledger rows that do not make a public-safety/source-reference claim and do not publish digest values. Dual-purpose hits are deterministic: public-safety/source-reference language and assigned digest values take precedence and must be modified. Every `modify_public_safe_hash_claim` hit is edited so raw `source_sha256` values are private-sidecar provenance and are not described as public-safe source references.
- [ ] Route targets are separate from #61-owned lifecycle states; #51 validates only the `lifecycle_state` field boundary and does not define lifecycle enum values.
- [ ] Every downstream ACE wave has a bounded sampling protocol and no unbounded share crawl, full-manifest materialization, or full-file hashing/counting of large manifests.
- [ ] The closed `wave_class` matrix records [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) as `control_plane`, [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) as `storage_lifecycle_gate`, [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) as `manifest_freshness_gate`, and [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) as `public_canary_gate`, all with `requires_manifest_snapshot_id=false`; requires [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) to be `wave_class=ingestion_wave` and carry `requires_manifest_snapshot_id=true`; and rejects any ingestion-wave executable binding that omits `wave_class=ingestion_wave` or falsifies the snapshot field.
- [ ] Sampling is rejected for [#52](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/52)-[#60](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/60) unless [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) approval plus snapshot evidence is recorded.
- [ ] Sampling firewall deny fixtures cover `json.load`, `.read_text()`, `for line in open(...)`, raw `jq` invocations against ACE manifest/source paths including `jq length` and `jq -c`, `cat`, recursive `grep`, `wc`, `sha256sum`, recursive glob/rglob, `os.walk`, `find`, `du`, `rg`, `fd`, `ls -R`, and validator self-scan safety. Denied-command prose is allowed only under fixed methodology headings without executable prefixes, source paths, pipes, redirects, command flags, or ambiguous command-like context; executable/path-bearing examples fail.
- [ ] Proposed scripts/tests use `ACE_SHARE_ROOT` plus share-relative paths.
- [ ] The #51 control-plane artifact is created at `artifacts/ace-share-wave0-control-plane.md`, not under `docs/`; `docs/case-studies/ace-share-wave-0-control-plane.md` and any other `docs/**` copy are rejected until [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) approval, local marker, implemented canary, and passing canary command exist.
- [ ] #51-owned public-surface self-scan blocks raw source paths, generic private-like identifier patterns, personal identifiers, proprietary snippets, raw source hash values, private lookup maps, and provider stderr/log sidecar leaks in the control-plane artifact, `artifacts/ace-source-hash-policy-sweep.md`, `scripts/ace_public_tokens.py`, `scripts/ace_public_contract.py`, `scripts/ace_public_surface_scan.py`, `scripts/ace_sampling_firewall.py`, `scripts/validate_ace_wave0_control_plane.py`, `tests/test_validate_ace_wave0_control_plane.py`, `tests/fixtures/ace-wave0-control-plane/good/`, `config/ace-public-output-contract.json`, `.github/workflows/validate.yml`, deny-list config, touched skills, plan, #63 plan, `docs/plans/README.md`, `docs/plans/ace-share-ingestion-wave-coordination.md`, `scripts/validate_ace_epic_wave_coordination.py`, `tests/test_validate_ace_epic_wave_coordination.py`, every retained `plan-51-*.md` review artifact, same-stem sidecars present at commit/comment time, and operator-fetched issue body/comment snapshots before commit/posting/status transition. Provider review output that includes raw source paths must be normalized before commit. Real private identifier denial using maintained client/project/internal-name lists remains owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63).
- [ ] `tests/fixtures/ace-wave0-control-plane/bad/` is handled only as a restricted forensic expected-failure fixture root. Each bad fixture declares `expected_failure`, `synthetic_only=true`, and `forbidden_pattern_class`; bad fixtures are rejected if they contain raw host/share path patterns, synthetic private-like identifiers outside the fixture contract, or unclassified arbitrary content; copying a bad fixture into the canonical public-surface scan set fails. Real client/project/internal-name detection remains owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63).
- [ ] The public-surface scanner includes a positive fixture for the plan's fenced metadata evidence shape: `EXISTS ACE_SHARE_ROOT/<fixed-source-path> type=<file|directory> details=withheld_public` passes only for the fixed source-list paths named in this plan, while unlisted ACE paths, rows publishing size/mtime/count/digest, executable/path-bearing commands, and private content snippets fail.
- [ ] The public-surface scanner includes a positive fixture for the authoritative `ACE_WAVE0_FIXED_SOURCE_EVIDENCE_PATHS` list and rejects any metadata evidence row outside exactly that seven-path set.
- [ ] Review artifacts cited for `status:plan-review` or as review evidence supporting user approval are completed, normalized, non-empty, and contain an authoritative `APPROVE`, `MINOR`, or `MAJOR` verdict parsed from the start of the first `## Verdict` section value or same-line `Verdict:`/`- **Verdict:**` field; zero-byte in-flight placeholders, verdict-less transcripts, verdict words that appear only later in prose, and `UNAVAILABLE` provider stubs are rejected as provider-review evidence. `UNAVAILABLE` artifacts may be retained only as historical provider-availability records. Status-transition review evidence must record matching reviewed plan path, reviewed_commit_sha, reviewed_tree_sha, and reviewed_plan_blob_sha across active-provider artifacts and the disagreement report.
- [ ] #51 implements only generic repo-local self-scan. It does not load private deny-lists, does not provide real public-exposure certification, rejects private-deny-list CLI flags, and points users to [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) for private-identifier denial and publication/comment certification.
- [ ] Committed review artifacts are normalized public copies when provider output contains private paths/identifiers. Normalization is limited to path/identifier token substitutions, records a note in the artifact or disagreement report, and proves the authoritative verdict before and after normalization is identical; verdict values are not hand-edited.
- [ ] Public-surface scanner self-safety is proven by scanning all planned touched skills with content-pattern-restricted policy-example allowlists and requiring each allowed policy phrase to have a matching negative fixture proving arbitrary sentinels, marker-wrapped synthetic private-like identifiers, and generic private-leak patterns still fail; no blanket file/path exemptions are allowed.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_control_plane.py` performs the canonical #51 local CI/fixture self-scan; `--scan-public-path <path>` adds operator-fetched issue body/comment snapshots for generic #51 self-scan without certifying real public exposure; `--scan-fixture-root tests/fixtures/ace-wave0-control-plane/bad` runs expected-failure fixture checks without treating bad fixtures as passing public surfaces.
- [ ] #51 defines the public-output canary input contract consumed by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63), but it does not require `scripts/validate_ace_public_artifacts.py` to exist or pass.
- [ ] Any `docs/` placement, `docs/index.md`, or `mkdocs.yml` publication of the #51 control-plane artifact requires [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) `status:plan-approved`, local approval marker, implemented redaction canary, and recorded passing-command result.
- [ ] `% ingested success` numerator, denominator, threshold, and validation command are required for every downstream wave; #51/#61/#62/#63 control/gate rows use `success_metric_applicability=not_applicable_control_plane` as a non-computing zero-denominator sentinel, while #52-#60 require `computed_sample` and nonzero denominator.
- [ ] Exclusion classes are fail-closed for PII, client-confidential, third-party-confidential, binary noise, and low-value material.
- [ ] Unit tests live in `tests/test_validate_ace_wave0_control_plane.py` with fixtures under `tests/fixtures/ace-wave0-control-plane/`.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_wave0_control_plane.py` passes.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_wave0_control_plane` passes.
- [ ] `.github/workflows/validate.yml` invokes both the wave-0 validator and the wave-0 unit test module.
- [ ] The validator and unit tests pass with `ACE_SHARE_ROOT` unset in CI by validating repo fixtures/docs only.
- [ ] `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py` passes after skill updates.

---

## Pre-Label Evidence Checklist

These are operator status-transition checks, not CI acceptance criteria. They must be recorded in the label-time evidence comment before #51 can move to `status:plan-review`.

- The live [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) issue body is sanitized so public issue text no longer contains raw host paths, exact inventory counts/sizes/dates, or denied-command examples against the private share.
- Before plan-review, the parent coordination validator is the fallback public-surface scanner because `scripts/validate_ace_wave0_control_plane.py` will not exist until approved #51 implementation. The parent fallback must apply both generic private-leak patterns and denied traversal/materialization command patterns to every extra `--scan-public-path`. The label-time operator will run `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py --scan-public-path <path>` against the #51 plan, #63 plan, README, coordination doc, status-evidence review artifacts, same-stem `.md.err`/`.err`/`.stderr`/`.log` sidecars present at comment/label time, sanitized live issue body snapshot, and plan-review comment body file before posting or labeling. Historical local r*-round artifacts that are not committed, posted, or cited as status evidence are not part of the status-transition evidence set.
- Plan-review comments are posted only from the same scanned body file, using `gh issue comment 51 --body-file <tmp-comment-body-file>`. The operator then refetches the created public comment body, verifies the body matches the scanned file bytes or recorded SHA-256 digest, reruns the parent fallback scan against the fetched body, and only then applies `status:plan-review`.
- After #51 is approved and implemented, implementation closeout comments and #51-owned public surfaces are checked with the #51 validator's `--scan-public-path` mode. Stronger private-deny-list/publication certification remains deferred to [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63).
- Parent [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) coordination support remains green: `UV_CACHE_DIR=.claude/state/uv-cache uv run python scripts/validate_ace_epic_wave_coordination.py`, `UV_CACHE_DIR=.claude/state/uv-cache uv run python -m unittest tests.test_validate_ace_epic_wave_coordination`, `UV_CACHE_DIR=.claude/state/uv-cache uv run skills/validate_skill.py`, and `git diff --check` pass before labeling.
- Plan-review quorum is explicitly recorded against a committed reviewed draft identity: plan path, reviewed_commit_sha, reviewed_tree_sha, and reviewed_plan_blob_sha. Provider quota/outage may degrade T3 to a disclosed two-active-provider quorum; Gemini noninteractive auth/config failure does not automatically qualify and blocks `status:plan-review` unless Gemini is restored or the user explicitly approves a one-round degraded quorum after seeing the auth-failure evidence. Under any allowed degraded quorum, Claude and Codex must both be fresh no-MAJOR for the same committed post-patch draft, or #51 stays draft-only.
- `docs/plans/ace-share-ingestion-wave-coordination.md` and `docs/plans/README.md` record the final #51 review/status evidence when #51 enters plan-review and again at implementation closeout, while keeping #51 non-implementation-ready until the user supplies `status:plan-approved` plus `.planning/plan-approved/51.md`.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude r3 | MAJOR | Required clearer downstream validator path semantics, independent public-check enforcement, skill-edit/scanner ordering, success sentinel, and sampling-token scoping. |
| Codex r3 | MAJOR | Required private deny-list CLI consistency, deny-list config scanning, closed field-name grammar, closed sidecar globbing, and route-to-store mapping. |
| Gemini r3 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r4 | MAJOR | Required honest structural-vs-true independence scoping and parseable field-name allow contexts; noted Gemini unavailable and manifest-gate wording drift. |
| Codex r4 | MAJOR | Required self-scan-safe field-name/sampling contexts, review-history scanning/tokenization, manifest-gate validator update, and zero-denominator sentinel. |
| Gemini r4 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r5 | MAJOR | Required keeping the control-plane artifact outside `docs/`, defining private deny-list containment detection, and separating operator-only gates from CI. |
| Codex r5 | MAJOR | Required repo-local `uv` cache commands, non-empty verdict-bearing review artifacts, commit-time private deny-list certification, and ledger schema consistency. |
| Gemini r5 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r6 | MAJOR | Required self-scan-safe field-name contexts and unique ordered allow-window anchors. |
| Codex r6 | MAJOR | Required scanning README/coordination docs, token generation provenance, and non-empty verdict-bearing review evidence. |
| Gemini r6 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r7 | MAJOR | Found anchor-window self-contradictions and scanned sibling-doc token conflicts. |
| Codex r7 | MAJOR | Required token generator provenance, manifest-gate fields in the canonical schema, and reconciliation of review-artifact evidence. |
| Gemini r7 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r8 | MAJOR | Required non-volatile review-artifact evidence, terminal verdict parsing, Gemini unavailability disclosure, private deny-list marker evidence, and exact token grammar. |
| Codex r8 | MAJOR | Required #63 plan reconciliation, control-plane artifact field-name context, review-artifact evidence cleanup, and explicit planning-surface vs implementation boundary. |
| Gemini r8 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r9 | MAJOR | Required anchored verdict parsing, explicit parent #50 validator-hardening boundary, metadata evidence positive fixture, and #63 token grammar assertion. |
| Codex r9 | MAJOR | Required scanner coverage for generated scripts/tests/fixtures, parent success-sentinel reconciliation, #63 exception-model reconciliation, and a concrete token generator home. |
| Gemini r9 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r10 | MAJOR | Required executable-context scanner grammar, shared #63 contract extraction, review-artifact normalization policy, and removal of exact private-share metadata disclosure. |
| Codex r10 | MAJOR | Required complete scan target coverage, git-SHA governance exceptions, two-stage public-scan marker sequencing, and token uniqueness. |
| Gemini r10 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r11 | MAJOR | Required resolving #51/#63 scanner boundary overlap, marker self-scan/lint sequencing, and moving operator-only attestations out of objective acceptance criteria. |
| Codex r11 | MAJOR | Required enforcing generation inside controlled token path, reconciling raw-hash policy with governance docs, pre-commit private-list scan sequencing, stricter verdict parsing, and narrower #63 local contract prose. |
| Gemini r11 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r12 | MAJOR | Required mechanically enforceable token generation evidence, broader `sha256` policy reconciliation across docs/plans, and moving parent #50 validator support out of #51 implementation scope. |
| Codex r12 | MAJOR | Required bad-fixture/public-surface scan separation, mechanically enforceable token generation or narrower claim, live #51 issue-body sanitization, and stricter #63 shared-config authority. |
| Gemini r12 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r13 | MAJOR | Required removing stale #51-parent-validator implementation wording and making the `sha256` hit filter mechanically explicit. |
| Codex r13 | MAJOR | Required using the parent coordination scanner for pre-label issue-body checks, resolving parent-validator scope contradiction, completing the `sha256` sweep rule, and narrowing private-identifier claims. |
| Gemini r13 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r14 | MAJOR | Required correcting the docs/publication boundary, decomposing the validator scope, stabilizing the hash-policy sweep, and removing temporal/unit-test claims. |
| Codex r14 | MAJOR | Required avoiding real private-identifier claims in bad fixtures, defining JSON config parser strategy, deduping the hash sweep, and marking live issue-body sanitization as verification-only. |
| Gemini r14 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r15 | MAJOR | Required an explicit governance decision/threat model for raw source hashes versus membership inference, a deterministic dual-purpose hash-hit precedence rule, and a degraded-quorum policy. |
| Codex r15 | MAJOR | Required adding decomposed Python modules to self-scan targets, resolving pre-implementation plan-scan sequencing, extending hash-policy sweep to public skills, and clarifying token helper ownership. |
| Gemini r15 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |
| Claude r16 | MAJOR | Required explicit repo-local governance-scan allowance, authoritative fixed source-evidence path list, independently derived ingestion-wave snapshot matrix, and separation of operator quorum gates from mechanical acceptance. |
| Codex r16 | MAJOR | Required handling historical review artifacts that contain quoted denied-command examples, adding config files as closed schema/policy contexts, and adding same-stem sidecars to the pre-label checklist. |
| Gemini r16 | UNAVAILABLE | Noninteractive Gemini auth failed with rc=41. |

**Overall result:** r16 returned MAJOR from both active providers. This plan remains draft-only and must not move to `status:plan-review`. This draft has since been patched for r16 findings: explicit repo-local governance-scan allowance, authoritative fixed source-evidence path list, `wave_class`-based ingestion-wave snapshot matrix, duplicate-token test seam, config-file closed schema/policy contexts, historical review-artifact retention/normalization rules, same-stem sidecar checklist coverage, and separation of operator quorum gates from mechanical acceptance. A fresh post-patch review round must return no-MAJOR before any status transition.

---

## Risks and Open Questions

- **Risk:** ACE inventory can drift; implementation must use exact manifests, bounded freshness probes, and `ACE_SHARE_ROOT` rather than hardcoded host paths.
- **Risk:** `visibility` remains hand-set; implementation must fail closed unless public clearance evidence, structural reviewer identity, and review artifact all exist. True independence is not proven by local validation; publication still requires [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) and user approval.
- **Risk:** #51's generic self-scan is not a real private-identifier/publication certification. This is intentional to avoid duplicating #63; any public-output certification remains blocked until #63 is approved and implemented.
- **Risk:** Gemini has been unavailable in noninteractive review runs; final review evidence must disclose any degraded provider quorum and cannot count `UNAVAILABLE` artifacts as provider approval. Provider quota/outage may degrade T3 to a disclosed two-active-provider quorum; Gemini auth/config failure blocks `status:plan-review` unless Gemini is restored or the user explicitly approves a one-round degraded quorum after seeing the auth-failure evidence. Under any allowed degraded quorum, Claude and Codex must both be fresh no-MAJOR for the same committed post-patch draft.
- **Risk:** The source-hash policy sweep is currently a large exact-hit classification pass. Implementation must produce a deterministic report for every hit, preserve dual-purpose precedence, and treat any unclassified hit as a failure rather than relying on reviewer memory.
- **Open:** The physical private sidecar backing store remains owned by [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61); #51 defines only logical target-store classes.

---

## Complexity

**T3** - security-sensitive publication firewall plus multi-file governance, validator, workflow, fixture, and skill changes; no content ingestion is authorized.
