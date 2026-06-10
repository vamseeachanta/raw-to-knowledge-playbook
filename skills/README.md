# Skills: the playbook's workflows as runnable artifacts

[Doc 08](../docs/08-skills-catalog.md) explains *why* a stabilized workflow
becomes a skill and what a good skill file contains. This directory ships those
skills as **adaptable templates** — the transferable rules are concrete; the
corpus-specific paths/commands are `{{PLACEHOLDERS}}` you fill in.

Each `SKILL.md` follows the doc-08 anatomy (Trigger · Preconditions · Steps ·
Verification · Cleanup · Incident appendix) and serializes to the open
**Agent Skills spec** (`name`/`description`/`license`/`compatibility`/`metadata`),
with our extensions (`enforcement_level`, closed-set `params`, `incident_refs`
→ [doc 04](../docs/04-failure-modes.md) failure classes) under `metadata`. The
full contract and the rationale are in
[AUTHORING-STANDARD.md](AUTHORING-STANDARD.md).

## Catalog

| Skill | Doc 08 entry | Enforcement | What it does |
|---|---|---|---|
| [verify-batch](verify-batch/SKILL.md) | The flagship | **L2** | Vision-verify a batch of extracted tables; closed-set verdicts; binary-faithful queue I/O; one PR per batch |
| [source-extraction-coverage](source-extraction-coverage/SKILL.md) | Research skill 3 | **L2** | Doc-type-aware deterministic extraction with an estimate/yield pair that makes shallow extraction loud |
| [page-shape-contract](page-shape-contract/SKILL.md) | Research skill 1 | **L3** | Structural + provenance + trust-label contract for a well-formed page |
| [audit-feedback-loop](audit-feedback-loop/SKILL.md) | Research skill 2 | **L1** | Anchored-text feedback inbox with explicit, never-deleted resolution states |
| [public-private-routing](public-private-routing/SKILL.md) | Research skill 4 | **L3** | Public/private firewall: visibility contract, abstraction-by-default, independent publish-time grep |
| [content-triage-and-exclusion](content-triage-and-exclusion/SKILL.md) | Office-ingestion campaign | **L2** | Ingest-time triage of a raw archive: classify on content (not extension), value-rank, dedup superseded, hard-exclude PII + third-party-confidential |
| [lfs-batch-fetch](lfs-batch-fetch/SKILL.md) | Office-ingestion campaign | **L2** | Fetch off-disk Git-LFS pointer binaries via the LFS Batch API + host token (sha256==oid = free verify); no git-lfs or sudo |
| [format-coverage-ledger](format-coverage-ledger/SKILL.md) | Office-ingestion campaign | **L2** | Right extraction lane per office/email format + a ledger of each format's known inherent losses, so a faithful-but-incomplete extract isn't silently trusted |
| [source-extract-fidelity](source-extract-fidelity/SKILL.md) | Office-ingestion campaign | **L2** | Independent prose-vs-extract review: every page claim traces to the committed extract (a cross-ref is not a quote; a derived number is not "quoted") |
| [stacked-batch-prs](stacked-batch-prs/SKILL.md) | Office-ingestion campaign | **L2** | One PR per batch on stacked branches (avoid shared-file conflicts) + the merge-cascade-strand guard: verify main's tree after each merge |
| [adversarial-verify-loop](adversarial-verify-loop/SKILL.md) | Office-ingestion campaign | **L2** | Independent refute-not-confirm review loop until a clean PASS: reviewer-built reproducers for code findings; fixes gated on re-running the reviewer's reproducer (GP-42) |
| [independent-oracle-validation](independent-oracle-validation/SKILL.md) | Office-ingestion campaign | **L2** | Gold-set scoring of committed extracts against a different extraction engine: two-tier numerics, every sub-1.0 number attributed, comparator verified harder than the pipeline (GP-47) |
| [xlsx-input-code-output-canary](xlsx-input-code-output-canary/SKILL.md) | Spreadsheet canary | **L2** | Classify XLS/XLSX workbooks before extraction and require input contract + code artifact + verified output proof across a ten-file canary |

> The seven **Office-ingestion campaign** skills were distilled from a mixed-office
> raw-archive ingestion (docx/xlsx/msg/pdf/pptx). Their `incident_refs` use
> descriptive slugs for failure modes not yet in the [doc 04](../docs/04-failure-modes.md)
> A/B/C/D/E table (e.g. `merge-cascade-strand`, `prose-overclaim`,
> `lfs-pointer-offdisk`); formalizing those into doc 04 is a follow-up.

## Enforcement gradient (doc 08)

`L1` callable skill · `L2` backed by a checking script · `L3` pre-commit/CI hook
that can't be bypassed. Promote a rule up the gradient when violations recur —
instructions catch intent, hooks catch everything.

## Validate

```bash
uv run skills/validate_skill.py          # check every SKILL.md (warn/deny tiering)
uv run skills/validate_skill.py --strict # treat warnings as failures
```

[`validate_skill.py`](validate_skill.py) is the one-script-three-altitudes
validator (L2 by hand, L3 as a `repo: local` pre-commit hook or CI Action). It
fails closed on the open-spec `name`/`description` rules and the required body
sections; recommended conventions (`license`, `evals/evals.json`, `Preconditions`)
warn. See [AUTHORING-STANDARD.md](AUTHORING-STANDARD.md).

## Adapting a template

1. Replace every `{{PLACEHOLDER}}` (paths, selector command, branch names) with
   your corpus's equivalents.
2. Keep the **rules** verbatim — closed-set values, binary-faithful I/O,
   serialize-per-domain, adversarial spot-check, independent identifier grep.
   Those are the parts paid for in incidents (see each file's incident appendix).
3. Register any new status value in your queue normalizer's known-set *before*
   first use, or rewrites will mangle it.

> `metadata.status: template` marks a file as not-yet-adapted. The formal
> skill-file schema + validator (#14) now ships here — see
> [AUTHORING-STANDARD.md](AUTHORING-STANDARD.md) and `validate_skill.py`.
