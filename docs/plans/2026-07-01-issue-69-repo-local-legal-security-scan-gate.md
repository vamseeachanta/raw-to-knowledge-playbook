# Plan for #69: ACE Wave 0 Repo-Local Legal and Security Scan Gate

> **Status:** plan-review
> **Complexity:** T3
> **Date:** 2026-07-01
> **Issue:** https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69
> **Client:** N/A
> **Project:** N/A
> **Lane:** lane:claude
> **Review artifacts:** scripts/review/results/2026-07-01-plan-69-claude-r4.md | scripts/review/results/2026-07-01-plan-69-codex-r4.md | scripts/review/results/2026-07-01-plan-69-gemini-r4.md

---

## Resource Intelligence Summary

### Existing repo code/docs

- `docs/plans/README.md` will remain the portfolio gate surface. This planning update records [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) as `plan-review` and not implementation-ready.
- `docs/plans/ace-share-ingestion-wave-coordination.md` will remain the parseable ACE coordination ledger. This planning update records [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) as `plan-review`, pending user approval of the dependency correction.
- `artifacts/ace-wave0-ledger-schema.json` and `scripts/validate_ace_wave0_schema_contract.py` still encode the old [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) dependency on [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68). Implementation will propose a dependency correction because the legal/security hard gate now blocks completed work, while [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) remains a broader public-surface scanner plan.
- `scripts/validate_ace_epic_wave_coordination.py` already contains the only repo-local public-artifact scan patterns: generic private-root shapes, local home/runtime paths, emails, client/customer/project identifier assignment shapes, confidentiality markers, personal identifier shapes, private source field assignments, source-like digest assignments, and unbounded traversal commands.
- `.github/workflows/validate.yml` runs repo-local validators and unit tests without live GitHub authentication. The legal/security scan will join this stock CI surface.
- `docs/07-data-governance.md`, `docs/18-security-and-pii.md`, and `docs/19-trust-boundary-and-private-mode.md` establish the raw-source firewall, private/public boundary, fail-closed security posture, and independent publish-time grep requirement.
- The bound skill group will be `public-private-routing`, `content-triage-and-exclusion`, `verify-batch`, `independent-oracle-validation`, and `adversarial-verify-loop`. Implementation will update these skills with the reusable repo-local legal scan command or file a follow-on issue for any method gap that cannot be closed safely inside this slice.

### Related issues

- [#50](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/50) will remain the approved parent epic.
- [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) will remain the wave-0 umbrella that delegates implementation slices to [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-[#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69).
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) implementation is pushed, but closeout is blocked because the required legal/security command is missing.
- [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will remain the owner of maintained real client/project/customer deny-lists, publication certification, and private runtime config.
- [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) provides the implemented schema and private source term vocabulary that [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will reuse instead of duplicating source-field policy.
- [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) will remain the owner of the broader reusable public-surface scanner. [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will not wait for [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68); it will implement the narrower repo-local legal/security gate and a self-scan-safe config contract now, then leave richer review-artifact/comment/sidecar scanning to [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)/[#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63).

### Decision checkpoint

- The live [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) issue body currently says it is blocked by the public-surface scanner slice defining deny-list self-scan without a blanket exemption. This plan will be approval-ready only if the user approves the following dependency correction: [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will replace that blocker with a narrower field-scoped config self-scan contract backed by the implemented [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema, while [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) remains the future owner of the broader public-surface scanner.
- If the user does not approve that correction, this plan must remain `draft`/blocked and [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) must wait for [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) instead of moving to implementation.

### Source inventory

- [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will not read the ACE share, private raw corpus files, or maintained private runtime deny-lists.
- `.legal-deny-list.yaml` will contain strict JSON text despite the `.yaml` extension. This is the JSON-compatible YAML subset requested by the issue; it will be loaded with Python stdlib `json.loads` and will reject normal YAML comments, anchors, aliases, block scalars, and unquoted keys.
- The committed deny-list will contain only synthetic/generic rule shapes and neutral rule identifiers. It will not contain real client names, customer names, project names, private hostnames, private machine roots, raw source identifiers, example private values, or arbitrary literal inventory fields.
- Negative test cases will be assembled at runtime or inside temporary files. No committed fixture will need a whole-file or whole-directory exemption to contain prohibited values.
- The scanner will expose three candidate modes:
  - `--diff-only` for local closeout and pre-commit checks. It will use Git state as its source of truth: staged candidate blobs, unstaged tracked candidate worktree edits, and untracked public-surface candidate paths.
  - `--scan-public-path <path>` for explicit closeout sets such as [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) artifacts and review files already committed before [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) exists.
  - `--all-tracked-public-surfaces` for clean-checkout CI. It will enumerate tracked public-surface candidates with `git ls-files -z`, so push/PR CI cannot pass merely because the checkout has no staged, unstaged, or untracked diff.
- All scanner modes will route every diagnostic through one redaction wrapper before printing. This includes findings, unclassified-candidate errors, path traversal or symlink rejection, invalid config, regex compile failures, and unexpected exceptions.

### Public-surface candidate contract

The path classifier will be closed. Unknown public-adjacent text paths will fail as unclassified candidates until they are added to the matrix or explicitly excluded with a reason.

| Class | Include | Exclude |
|---|---|---|
| Docs/plans | `docs/**/*.md`, `docs/**/*.json`, `docs/**/*.jsonl`, `docs/**/*.yaml`, `docs/**/*.yml`, `docs/**/*.toml` | Rendered/binary media under docs |
| Skills | `skills/**/*.md`, `skills/**/*.json`, `skills/**/*.yaml`, `skills/**/*.yml`, `skills/**/*.py` | Skill cache/build artifacts |
| Skill resources | `skills/**/resources/**/*.py`, `skills/**/resources/**/*.md`, `skills/**/resources/**/*.json`, `skills/**/resources/**/*.yaml`, `skills/**/resources/**/*.yml`, `skills/**/resources/**/*.txt`, `skills/**/resources/**/*.csv`, `skills/**/resources/**/*.tsv` | Binary/generated resources unless explicitly passed |
| Scripts | `scripts/**/*.py`, `scripts/**/*.sh`, `scripts/**/*.md`, `scripts/**/*.json`, `scripts/**/*.yaml`, `scripts/**/*.yml` | `__pycache__`, `*.pyc` |
| Tests/fixtures | `tests/**/*.py`, `tests/**/*.md`, `tests/**/*.json`, `tests/**/*.jsonl`, `tests/**/*.yaml`, `tests/**/*.yml`, `tests/**/*.txt`, `tests/**/*.csv`, `tests/**/*.tsv` | Binary fixture files unless explicitly passed |
| Artifacts/config | `artifacts/**/*.md`, `artifacts/**/*.json`, `artifacts/**/*.jsonl`, `artifacts/**/*.yaml`, `artifacts/**/*.yml`, `artifacts/**/*.txt`, `artifacts/**/*.csv`, `artifacts/**/*.tsv`, `config/**/*.json`, `config/**/*.yaml`, `config/**/*.yml`, `.legal-deny-list.yaml` | Raw corpus binaries and generated caches |
| Workflow/planning | `.github/workflows/**/*.yaml`, `.github/workflows/**/*.yml`, `.planning/**/*.md`, `.planning/**/*.json` | CI cache directories |
| Review evidence | `scripts/review/results/**/*.md` when tracked or passed explicitly | Untracked review files will fail closed under `--diff-only` |
| Examples | `examples/**/*.py`, `examples/**/*.md`, `examples/**/*.json`, `examples/**/*.yaml`, `examples/**/*.yml`, `examples/**/*.txt`, `examples/**/*.csv`, `examples/**/*.tsv`, `examples/**/.gitignore` | Example binaries such as PDFs unless explicitly passed |
| Agent/runtime tracked policy | `.claude/**/*.md`, `.claude/**/*.json`, `.claude/**/*.yaml`, `.claude/**/*.yml` when tracked | `.claude/state/**`, caches, logs, auth/session files |
| Top-level policy | `*.md`, `*.json`, `*.yaml`, `*.yml`, `*.toml`, `.gitignore`, `.gitattributes` | Git internals and local runtime state |

The implementation will include a live classifier test over `git ls-files -z`. Every tracked text/public-adjacent path must be either included by the matrix or excluded by a closed exclusion reason. The test will cover examples, skill resources, and tracked `.claude/**` files explicitly because those are present in this repository.

### Existing-deny-fixture migration and forensic allow contexts

`--all-tracked-public-surfaces` must not be wired into CI until the implementation proves the current tracked repository exits 0. Existing committed deny examples and canary metadata will be handled before enabling CI:

1. Prefer migration to runtime-generated/temp-file negative examples.
2. If committed forensic examples must remain, allow them only through a closed allow-context object with:
   - `context_id` from a closed set.
   - path globs restricted to test, fixture, or named skill-resource files.
   - explicit `rule_ids`.
   - a required same-line sentinel token.
   - `max_lines_per_file`.
   - a short justification string.
3. Malformed, unknown, over-budget, or path-mismatched allow contexts will fail closed.
4. No allow context may exempt an entire file or directory.
5. The real repo command `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces` must exit 0 before `.github/workflows/validate.yml` is changed to run it.

### Pattern-field validation contract

`rules[].patterns[]` will be validated by a meta-policy instead of by normal content scanning:

- Positive policy regex examples will include structural classes for home-path-like values, private-root-like values, email-like values, client/customer/project assignment shapes, host/domain-like values, and digest-like values. These examples will be assembled in tests from neutral fragments when needed to avoid self-blocking.
- Negative examples will include literal email-like values, literal slash-home paths, literal slash-mnt paths, literal host/domain names, literal client/project/customer assignments, and literal 32+ hex digest values.
- A pattern will be accepted only if it compiles, uses structural regex syntax, and does not contain a literal value matching the scanner's own sensitive-value detectors after regex escapes are normalized.
- Pattern validation failures will be emitted through the same universal redaction wrapper as scan findings.

### [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) closeout path source

The [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) closeout scan will derive its paths from the implemented [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) helper rather than a hand-maintained list:

```text
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=.claude/state/uv-cache uv run python - <<'PY' | xargs -0 bash scripts/legal/legal-sanity-scan.sh
from scripts.ace_manifest_freshness_contract import public_scan_paths
import sys

for path in public_scan_paths():
    sys.stdout.buffer.write(b"--scan-public-path\0")
    sys.stdout.buffer.write(str(path).encode("utf-8") + b"\0")
PY
```

Implementation tests will assert that this derived path set includes every tracked [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) plan, approval marker, config, script, test, fixture, case-study, lifecycle doc, workflow, and `scripts/review/results/*plan-62*.md` / `*implementation-62*.md` artifact.

### Gaps identified

- The repo has no `scripts/legal/legal-sanity-scan.sh` wrapper and no `.legal-deny-list.yaml`.
- Completed [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) work cannot satisfy the inherited legal/security scan hard gate until [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) lands.
- The previous [#51](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51) plan reviews found that the legal deny-list patterns were under-specified and that a JSON-in-`.yaml` parser contract could confuse maintainers unless the file self-identifies and tests reject conventional YAML features.
- The existing [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) draft defines a future richer public-surface scanner, but it is still blocked-draft. [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) needs a smaller executable gate now.
- Current validators scan explicit public paths but do not inspect staged blobs. The legal/security command must prevent a clean working tree from hiding a staged leak or an unstaged tracked leak.
- Untracked candidate files are not representable as staged blobs or tracked worktree edits. The command must fail closed when it sees untracked public-surface candidates under the `--diff-only` path set.
- Push/PR CI cannot rely on `--diff-only` because a clean `actions/checkout` has no staged/unstaged/untracked state. CI must run `--all-tracked-public-surfaces` or an explicit tracked path set.
- [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) closeout needs a way to scan already-tracked [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) artifacts and review files. `--scan-public-path` will provide that path without pretending `--diff-only` covers historical artifacts.
- The repository already contains committed negative fixtures and canary metadata that may match new legal/security rules. [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) must either migrate those examples or encode precise forensic allow contexts before enabling all-tracked CI.

### Evidence

**Issue status** (verified 2026-07-01):

```text
$ gh issue view 69 --json number,title,state,labels,url
#69 OPEN ACE wave 0 split: repo-local legal and security scan gate
labels=strengthening,lane:claude,priority:high
url=https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69
```

**Related issue status** (verified 2026-07-01):

```text
#62 OPEN labels include status:plan-approved
#63 OPEN labels do not include a status gate
#65 OPEN labels include status:plan-approved
#68 OPEN labels do not include a status gate
```

**File existence** (verified 2026-07-01):

```text
EXISTS docs/plans/README.md
EXISTS docs/plans/ace-share-ingestion-wave-coordination.md
EXISTS artifacts/ace-wave0-ledger-schema.json
EXISTS scripts/validate_ace_epic_wave_coordination.py
EXISTS scripts/validate_ace_wave0_schema_contract.py
EXISTS .github/workflows/validate.yml
MISSING .legal-deny-list.yaml
MISSING scripts/legal/legal-sanity-scan.sh
MISSING scripts/legal/legal_sanity_scan.py
MISSING tests/test_legal_sanity_scan.py
```

**Reproduction proofs** (verified 2026-07-01):

```text
$ if [ -x scripts/legal/legal-sanity-scan.sh ]; then scripts/legal/legal-sanity-scan.sh --diff-only; else echo 'MISSING scripts/legal/legal-sanity-scan.sh'; exit 2; fi
MISSING scripts/legal/legal-sanity-scan.sh
exit-code: 2
```

**Branch sync** (verified 2026-07-01):

```text
HEAD=46811b38e1df61c079013318e6e9f5d9b31c1821
origin/docs/ace-ingestion-wave-plans=46811b38e1df61c079013318e6e9f5d9b31c1821
```

---

## Artifact Map

| Artifact | Path |
|---|---|
| This plan | `docs/plans/2026-07-01-issue-69-repo-local-legal-security-scan-gate.md` |
| Strict JSON-subset deny-list config | `.legal-deny-list.yaml` |
| Bash wrapper | `scripts/legal/legal-sanity-scan.sh` |
| Scanner implementation | `scripts/legal/legal_sanity_scan.py` |
| Unit tests | `tests/test_legal_sanity_scan.py` |
| Plan index | `docs/plans/README.md` |
| Coordination ledger | `docs/plans/ace-share-ingestion-wave-coordination.md` |
| Wave-0 schema registry | `artifacts/ace-wave0-ledger-schema.json` |
| Schema registry validator | `scripts/validate_ace_wave0_schema_contract.py` |
| Schema registry tests | `tests/test_validate_ace_wave0_schema_contract.py` |
| Workflow | `.github/workflows/validate.yml` |
| Bound skill docs | `skills/public-private-routing/SKILL.md`, `skills/content-triage-and-exclusion/SKILL.md`, `skills/verify-batch/SKILL.md`, `skills/independent-oracle-validation/SKILL.md`, `skills/adversarial-verify-loop/SKILL.md` |
| Review artifact - Claude r1 | `scripts/review/results/2026-07-01-plan-69-claude-r1.md` |
| Review artifact - Codex r1 | `scripts/review/results/2026-07-01-plan-69-codex-r1.md` |
| Review artifact - Gemini r1 | `scripts/review/results/2026-07-01-plan-69-gemini-r1.md` |

---

## Deliverable

After approval and implementation, [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) will provide an executable repo-local legal/security scan command that can block generic confidentiality, identifier, secret, private-root, and raw-provenance leak shapes in changed public-surface text without storing real private deny-list values in this repository.

---

## Pseudocode

```text
legal-sanity-scan.sh:
  resolve repo root with git rev-parse
  exec python scripts/legal/legal_sanity_scan.py with forwarded args

legal_sanity_scan.py:
  load .legal-deny-list.yaml as strict JSON text with json.loads
  validate config schema:
    format is json-subset-yaml
    owner_issue is 69
    private_runtime_config_owner_issue is 63
    top-level keys are a closed set
    rule object keys are a closed set
    every rule has id, severity, description, patterns
    severity is block or warn
    pattern strings compile with re
    no rule stores real_values, private_roots, literal_identifier_inventory,
    client_names, project_names, customer_names, examples, literal_values,
    private_hostnames, or unknown inventory-like keys
    pattern strings are field-scoped policy regexes:
      allow regex metasyntax inside rules[].patterns[]
      reject literal private-looking values inside pattern strings
      scan all other string fields normally
    allow-context objects are closed, path-restricted, rule-scoped,
    line-budgeted, same-line-sentinel based, and never file-wide
    no parser accepts YAML-only constructs

  resolve repo root from git
  build closed candidate classifier from config:
    include only the public-surface path classes named in this plan
    exclude binary/cache paths by closed suffix and directory rules
    reject unknown public-adjacent text paths as unclassified

  if --diff-only:
    collect staged candidates:
      git diff -z --cached --name-only --diff-filter=ACMR
      keep public-surface text candidate paths only
      read staged blob content from the index

    collect unstaged tracked candidates:
      git diff -z --name-only --diff-filter=ACMR
      keep public-surface text candidate paths only
      read worktree content

    collect untracked candidates:
      git ls-files -z --others --exclude-standard
      keep public-surface candidate paths only
      if any exist, emit DENY with candidate ids and redacted paths, then exit nonzero

  if --scan-public-path is present:
    resolve each supplied path inside the repo
    reject absolute paths outside the repo, symlink escapes, and path traversal
    expand directories with bounded local traversal over the supplied root only
    keep public-surface text candidate paths only
    read tracked/worktree content

  if --all-tracked-public-surfaces:
    collect tracked candidates with git ls-files -z
    keep every closed-matrix public-surface text candidate
    read worktree content in the clean checkout

  require at least one candidate mode unless --help is used
  dedupe candidates by repo-relative path plus source kind

  scan every candidate:
    normalize bytes to text with replacement
    scan the repo-relative path string before content
    redact sensitive-looking path segments before printing
    scan each line with compiled rules
    report candidate id, source kind, redacted repo path, line number, rule id,
    severity, and neutral description
    never print the matched sensitive-looking substring or an unredacted sensitive path
    treat block-severity matches as failing

  emit diagnostics only through safe_emit():
    redact candidate paths, config paths, supplied CLI paths, regex text,
    matched text, exception messages, and traceback-derived paths
    use neutral candidate ids for untracked/unclassified/path-error cases
    print uncaught exceptions as redacted tool/config failures unless --debug is explicitly used

  validate self-scan:
    scanner config, scanner code, wrapper, tests, plan/README/coordination docs,
    workflow, and bound skill docs must be able to pass the scan
    prohibited-value negative fixtures are built at runtime or in temp files
    .legal-deny-list.yaml is scanned through field-scoped config validation:
      rules[].patterns[] are validated as policy regex fields, not blanket-exempted
      all non-pattern string fields are scanned as normal public text

  exit 0 when no block-severity findings and no untracked candidates
  exit 1 on block-severity findings or untracked candidate public-surface files
  exit 2 on tool/config misuse

implementation integration:
  update schema split registry so #69 depends on the implemented #65 schema
  add issue_skill_groups to the #69 split row with exactly:
    public-private-routing
    content-triage-and-exclusion
    verify-batch
    independent-oracle-validation
    adversarial-verify-loop
  keep #68 as a future richer public-surface scanner dependency, not a blocker
  run all-tracked scan on the current repo before CI wiring:
    migrate existing committed deny examples to runtime generation where possible
    add only precise forensic allow contexts where migration is not appropriate
    require bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces to pass
  add legal scan to CI before validator unit tests using --all-tracked-public-surfaces only after that pass
  define the #62 closeout scan command from scripts.ace_manifest_freshness_contract.public_scan_paths()
  update the issue-69 skill group with the command and fail-closed expectations
```

---

## Files to Change

| Action | Path | Reason |
|---|---|---|
| Create | `.legal-deny-list.yaml` | Strict JSON-subset YAML config for generic block/warn rules without real private identifiers |
| Create | `scripts/legal/legal-sanity-scan.sh` | Repo-local hard-gate command required by workspace closeout |
| Create | `scripts/legal/legal_sanity_scan.py` | Git-aware staged/unstaged/untracked scanner implementation using Python stdlib only |
| Create | `tests/test_legal_sanity_scan.py` | TDD coverage for config parsing, rule matching, Git candidate selection, untracked fail-closed behavior, and self-scan safety |
| Modify | `.github/workflows/validate.yml` | Run `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces` in stock CI |
| Modify | `docs/plans/README.md` | Record [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) plan status and plan path |
| Modify | `docs/plans/ace-share-ingestion-wave-coordination.md` | Record [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) plan status and the dependency correction posture |
| Modify | `artifacts/ace-wave0-ledger-schema.json` | Record [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) plan path/status and update the split dependency from [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68)-blocked to [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-schema-backed generic gate |
| Modify | `scripts/validate_ace_wave0_schema_contract.py` | Validate the corrected [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) dependency, plan-path/status contract, and issue-69 skill group fields |
| Modify | `tests/test_validate_ace_wave0_schema_contract.py` | Lock the dependency correction, issue-69 skill group, and rejection of stale [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) plan-required schema state after implementation |
| Modify | `skills/public-private-routing/SKILL.md` | Add the repo-local legal scan command as the independent grep gate for this repository |
| Modify | `skills/content-triage-and-exclusion/SKILL.md` | Add the legal scan as the pre-extraction/pre-commit exclusion backstop for public-surface artifacts |
| Modify | `skills/verify-batch/SKILL.md` | Add the scan to batch closeout hygiene so verification reports do not rely on producer self-certification |
| Modify | `skills/independent-oracle-validation/SKILL.md` | Add the scan to oracle report publication hygiene |
| Modify | `skills/adversarial-verify-loop/SKILL.md` | Add the scan to review artifact/comment closeout expectations |

---

## TDD Test List

| Test name | What it verifies | Expected input | Expected output |
|---|---|---|---|
| `test_config_loads_as_strict_json_subset_yaml` | `.legal-deny-list.yaml` is valid JSON text despite its suffix | Repo config | `json.loads` succeeds and required metadata/rules exist |
| `test_config_rejects_yaml_only_constructs` | Maintainers cannot accidentally use normal YAML features | Temporary config with YAML-only syntax | Parser exits with config error |
| `test_config_rejects_unknown_top_level_and_rule_keys` | Config schema is closed | Temporary config with unknown keys | Parser exits with config error |
| `test_config_rejects_real_identifier_inventory_fields` | Repo config cannot carry real private deny-list values | Temporary config containing forbidden inventory keys such as `client_names`, `examples`, and `literal_values` | Parser exits with config error |
| `test_pattern_fields_allow_policy_regexes_but_reject_literal_private_values` | Pattern strings are field-scoped policy, not a blanket config exemption | Temporary config with structural regexes for home-path-like, private-root-like, email-like, client/project assignment, host/domain-like, and digest-like classes, then literal private-looking values | Structural policy regexes pass; literal private-looking values fail |
| `test_forensic_allow_contexts_are_closed_and_path_scoped` | Existing deny fixtures can be retained only through precise contexts | Temporary config with valid and invalid allow contexts | Valid path/rule/line/sentinel context passes; unknown, file-wide, over-budget, or path-mismatched contexts fail |
| `test_block_rules_compile` | All regex patterns are explicit and runnable | Repo config | Every pattern compiles |
| `test_candidate_path_matrix_includes_public_surfaces` | Closed classifier covers repo public surfaces | Representative docs, skills, skill resources, scripts, tests, artifacts, config, workflow, planning, examples, tracked `.claude/**`, top-level policy, and review paths | Public text candidates are included |
| `test_all_tracked_text_paths_are_classified_or_excluded_with_reason` | The matrix cannot omit live tracked text paths | `git ls-files -z` over the repository | Every tracked text/public-adjacent path is included or excluded by a closed reason |
| `test_candidate_path_matrix_rejects_unclassified_public_text` | Unknown public-adjacent paths cannot be silently skipped | Temporary tracked public-like text path outside the matrix | Scanner exits nonzero with unclassified candidate |
| `test_blocks_generic_private_root_shapes` | Synthetic private-root-like paths fail without storing real roots | Runtime-generated temp content | Scanner reports block finding with redacted summary |
| `test_blocks_confidentiality_markers` | Confidentiality marker phrases fail | Runtime-generated temp content | Scanner reports block finding |
| `test_blocks_client_project_identifier_assignments` | Client/customer/project identifier assignments fail as shapes | Runtime-generated temp content | Scanner reports block finding |
| `test_blocks_secret_assignments` | Secret/token/password assignment shapes fail | Runtime-generated temp content | Scanner reports block finding |
| `test_blocks_raw_source_provenance_assignments` | Raw source/provenance field assignment shapes fail | Runtime-generated temp content using #65 field terms | Scanner reports block finding |
| `test_blocks_personal_identifier_shapes` | Email, phone-like, and personal-id-like shapes fail | Runtime-generated temp content | Scanner reports block finding |
| `test_blocks_unbounded_traversal_commands` | Dangerous recursive/share traversal commands fail | Runtime-generated temp content | Scanner reports block finding |
| `test_does_not_echo_sensitive_match_text_or_path` | Output redacts the matched value and sensitive path segments | Runtime-generated temp content and path | Finding includes candidate id, rule id, line, and redacted path only |
| `test_all_error_paths_use_safe_emit_redaction` | Non-finding errors cannot leak raw paths or values | Invalid config, regex compile failure, symlink escape, path traversal, unclassified candidate, and forced internal exception | Every diagnostic is redacted and no traceback is printed without debug mode |
| `test_scans_staged_blob_content` | Staged content is scanned from the index | Temporary git repo with staged candidate leak | Command exits nonzero before worktree changes can hide it |
| `test_scans_unstaged_tracked_edits` | Unstaged tracked edits are scanned from the worktree | Temporary git repo with tracked candidate edit | Command exits nonzero |
| `test_fails_closed_on_untracked_public_surface_candidates` | Untracked public-surface files cannot be silently missed | Temporary git repo with untracked text candidate | Command exits nonzero and prints candidate id plus redacted path |
| `test_git_path_collection_uses_nul_delimiters` | Newlines and shell metacharacters in filenames cannot corrupt output parsing | Temporary git repo with newline-bearing candidate path | Command handles path as one candidate and redacts output |
| `test_ignores_non_candidate_paths_without_traversal` | `--diff-only` stays bounded to changed public-surface candidates | Temporary git repo with ignored/cache files | Command does not scan ignored/cache paths |
| `test_scan_public_path_scans_existing_tracked_artifacts` | Explicit path mode can scan already-tracked artifacts | Temporary git repo with committed public file passed by `--scan-public-path` | Command scans and fails on leak |
| `test_all_tracked_public_surfaces_catches_clean_checkout_leak` | CI mode catches committed leaks without staged/unstaged state | Temporary clean checkout with committed public leak | Command exits nonzero under `--all-tracked-public-surfaces` |
| `test_real_repo_all_tracked_public_surfaces_passes_before_ci_wiring` | CI will not self-block on existing committed fixtures | Current repository after fixture migration/forensic allow contexts | `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces` exits zero before workflow is changed |
| `test_62_closeout_path_source_scans_existing_artifacts` | [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) closeout can scan tracked [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) surfaces without drift | Paths derived from `scripts.ace_manifest_freshness_contract.public_scan_paths()` and tracked `*plan-62*.md` / `*implementation-62*.md` artifacts | Derived command visits every expected path and exits zero after implementation |
| `test_self_scan_artifacts_pass` | The scanner can scan its own config/code/tests/docs without blanket exemption | Repo artifacts from this issue | Command exits zero after implementation |
| `test_legal_scan_is_in_ci` | Stock CI runs a mode that works on clean checkouts | `.github/workflows/validate.yml` | Workflow contains `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces` |
| `test_wave0_schema_records_69_dependency_correction` | Registry no longer blocks the legal gate on blocked-draft #68 | Schema artifact and validator | [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) row names #65 schema backing and false implementation readiness until approval |
| `test_wave0_schema_records_69_issue_skill_group` | The authoritative [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) skill set is not confused with [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) global skill groups | Schema artifact and validator | [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) split row has `issue_skill_groups` with exactly `public-private-routing`, `content-triage-and-exclusion`, `verify-batch`, `independent-oracle-validation`, and `adversarial-verify-loop` |
| `test_bound_skills_document_69_scan_gate` | Required issue-69 skill group is updated | Five issue-69 skill docs | Each names the command or a filed follow-on issue |

---

## Acceptance Criteria

- [ ] Issue plan will exist under `docs/plans/` and will pass adversarial plan review before implementation.
- [ ] User approval of this plan will explicitly authorize replacing the live [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) blocker with the narrower [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-schema-backed legal/security gate described here.
- [ ] `bash scripts/legal/legal-sanity-scan.sh --diff-only` will exist and exit nonzero on block-severity matches.
- [ ] `bash scripts/legal/legal-sanity-scan.sh --scan-public-path <path>` will scan explicit already-tracked closeout artifacts such as the [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) public artifact set.
- [ ] `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces` will scan clean-checkout CI state and fail on committed public-surface leaks even when no staged, unstaged, or untracked files exist.
- [ ] Existing committed deny fixtures/canary metadata will be migrated to runtime-generated tests or covered by precise forensic allow contexts before all-tracked CI is enabled.
- [ ] The real repository command `bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces` will exit zero before `.github/workflows/validate.yml` is changed to call it.
- [ ] `.legal-deny-list.yaml` will use the JSON-compatible YAML subset contract and will be loaded through Python stdlib `json.loads`.
- [ ] The parser will reject normal YAML-only constructs, unknown config keys, private identifier inventories, real private-root inventories, and arbitrary literal/example inventory fields in the repo-local config.
- [ ] `rules[].patterns[]` will be treated as a field-scoped policy-regex context, not a blanket config exemption; all non-pattern config strings will be scanned normally and literal private-looking values inside pattern fields will fail.
- [ ] Forensic allow contexts will be closed, path-restricted, rule-scoped, line-budgeted, same-line-sentinel based, and never whole-file or whole-directory exemptions.
- [ ] The scanner will implement a closed public-surface candidate path matrix for docs, plans, skills, skill resources, scripts, tests, fixtures, examples, tracked `.claude/**`, artifacts, config, workflow, planning, review evidence, and top-level policy files.
- [ ] A live `git ls-files -z` classifier test will prove every tracked text/public-adjacent path is included or explicitly excluded with a closed reason.
- [ ] The wrapper will scan staged candidate blobs, unstaged tracked candidate edits, and fail closed on untracked candidate public-surface files.
- [ ] Git path collection will use NUL-delimited output for staged, unstaged, tracked, and untracked candidate discovery.
- [ ] Initial deny-list rules will cover synthetic/generic private-root shapes, confidentiality markers, client/project/customer identifier assignment shapes, secret assignment shapes, raw source-provenance assignment shapes, personal identifier shapes, and unbounded traversal command shapes.
- [ ] Scanner findings and all non-finding diagnostics will redact matched sensitive-looking substrings and sensitive path segments, and will report only candidate id, source kind, redacted path, line, severity, rule id, neutral description, or redacted tool/config error.
- [ ] Negative test content will be generated at runtime or in temporary files; committed fixtures will not require a blanket exemption.
- [ ] Real client/project/customer names and private machine roots will remain out of this repository and will stay owned by [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63)/private runtime config.
- [ ] The [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) schema registry and validator will record that [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) is a [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-schema-backed legal/security gate, while [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68) remains the future broader public-surface scanner owner.
- [ ] The [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) issue-local skill group will be recorded in the schema split row as `issue_skill_groups`, distinctly from [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)'s schema-bound skill group, with the exact closed value set from this plan.
- [ ] The [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) closeout command will derive its path source from `scripts.ace_manifest_freshness_contract.public_scan_paths()` and tests will prove all tracked [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) review/artifact paths are visited.
- [ ] `.github/workflows/validate.yml` will run the legal/security scan in stock CI without requiring live GitHub authentication.
- [ ] Issue-local bound skill docs will be updated or a follow-on playbook issue will be filed for any reusable method gap.

---

## Adversarial Review Summary

| Provider | Verdict | Key findings |
|---|---|---|
| Claude | APPROVE | r1-r3 MAJOR findings were resolved; r4 verified the path matrix, live classifier test, all-tracked CI gate, and real-repo pre-CI pass requirement. |
| Codex | MINOR | r4 found only stale review metadata and required this final update before applying `status:plan-review`. |
| Gemini | UNAVAILABLE | r4 CLI attempt failed with `IneligibleTierError`; earlier r1/r2 MAJOR findings were addressed in the current plan text. |

**Overall result:** no-MAJOR active-provider quorum. The plan is ready for `status:plan-review`; implementation remains blocked until user approval applies `status:plan-approved` and creates the required local approval marker. User approval must explicitly accept the dependency correction that lets [#69](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69) proceed as a narrower [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-schema-backed gate instead of waiting for [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68).

---

## Risks and Open Questions

- **Risk:** The dependency correction could conflict with the previously implemented [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65) split registry. Implementation will patch the schema artifact, validator, tests, README, and coordination ledger together so there is one explicit source of truth.
- **Risk:** Strict JSON inside a `.yaml` filename could surprise maintainers. The config will self-identify as JSON-subset YAML, parser errors will name the contract, and tests will reject conventional YAML constructs.
- **Risk:** Approving the plan changes the live issue's original dependency posture. The approval request and GitHub evidence comment will state that approval explicitly accepts the narrower [#65](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/65)-backed self-scan contract in place of waiting on [#68](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68).
- **Risk:** Diff-only scanning is insufficient in CI and for already-tracked closeout artifacts. The implementation will add `--all-tracked-public-surfaces` for clean-checkout CI and repeated `--scan-public-path` for explicit historical artifact sets.
- **Risk:** All-tracked CI could self-block on existing committed deny fixtures and canary metadata. Implementation will run the all-tracked scan before CI wiring, migrate negative fixtures where possible, and allow irreducible forensic examples only through path/rule/line/sentinel-scoped contexts.
- **Risk:** A closed candidate matrix can drift from tracked repo reality. A live `git ls-files -z` classifier test will require every tracked text/public-adjacent path to be included or excluded with reason.
- **Risk:** Over-broad patterns could block the scanner's own config, code, tests, or plan. The implementation will keep bad examples in runtime-generated/temp content and will require the scanner to self-scan its issue artifacts before closeout.
- **Risk:** The generic deny-list will not prove absence of real client/customer/project names. This is intentional; [#63](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/63) will own maintained private runtime deny-list certification.
- **Risk:** Staged/worktree split handling can miss state if implemented through worktree reads only. Tests will require staged blob reads from the Git index and separate worktree reads for unstaged tracked edits.
- **Risk:** Untracked public-surface candidates can be noisy. The command will fail closed and print candidate ids plus redacted paths, so operators must stage, ignore, or remove those files before legal/security closeout.
- **Risk:** Sensitive filenames can leak through diagnostics. Git candidate collection will use NUL-delimited output, scanner diagnostics will redact path segments, and tests will cover newline-bearing/sensitive paths.
- **Risk:** The [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) legal closeout path list can drift as review artifacts are added. The closeout command will derive from `public_scan_paths()` and tests will compare that source against tracked [#62](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62) artifacts.

---

## Complexity

**T3** - this is a security-sensitive gate that affects repo-wide closeout, Git staged/unstaged/untracked state, CI, schema/coordination registry dependencies, and multiple bound playbook skills.
