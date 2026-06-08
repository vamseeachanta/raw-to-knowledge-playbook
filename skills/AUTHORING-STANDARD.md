# Skill-Authoring Standard

The standard the `skills/` artifacts are validated against. It extends
[doc 08](../docs/08-skills-catalog.md) (the *why* and the "anatomy of a good
skill file") with a **machine-checkable contract** so the catalog can't drift as
it grows. Research and primary sources: **issue #14**.

Design stance, consistent with the repo: **serialize to an open standard, adopt a
validator as a component — never migrate to a framework runtime.**

## Target format: the open Agent Skills spec

Skills serialize as `SKILL.md` with YAML frontmatter, per the open
**Agent Skills specification** (agentskills.io, Apache-2.0 code / CC-BY-4.0 docs;
Anthropic-originated). Two surfaces exist and **diverge** — adopt with eyes open:

- **Anthropic product docs** define a deliberately *minimal* runtime contract:
  only `name` and `description` are required.
- **The open spec** documents the same two **plus** optional `license`,
  `compatibility`, `metadata`, `allowed-tools`.

So `license`/`metadata` are **spec-conformant but not runtime-read** — treat them
as portable metadata, not behavior. The validator distinguishes the two:
**name/description rules fail closed (DENY); open-spec optional fields warn.**

### Frontmatter contract

| Field | Tier | Rule (source: open spec + Anthropic docs) |
|---|---|---|
| `name` | **DENY** | ≤64 chars; `[a-z0-9-]`, no leading/trailing/**double** hyphen; reserved `anthropic`/`claude` forbidden; **must equal the parent directory name** |
| `description` | **DENY** | 1–1024 chars; no XML/angle brackets; third person; states **what it does AND when to use it** (`Use when …`) — the single highest-leverage field for skill selection |
| `license` | WARN | open-spec; metadata only |
| `compatibility` | WARN | open-spec; ≤500 chars; runtime/env requirements |
| `metadata.version` | WARN | string |
| `metadata.enforcement_level` | WARN | **our** field: `L1` \| `L2` \| `L3` (drives validator strictness) |
| `metadata.status` | WARN | `template` until adapted to a corpus |
| `metadata.incident_refs` | WARN | comma list of doc-04 failure classes the rules trace to |
| `metadata.params` | WARN | compact closed-set param spec; `enum(...)` for every closed set |

> **`allowed-tools` is experimental** and support varies by implementation — do
> not build enforcement on it yet.

### Required body sections (house rule, lintable)

DENY: `## Trigger`, `## Steps`, `## Verification`, `## Cleanup`,
`## Incident appendix`. WARN: `## Preconditions`, `## Examples`. Recommended
sibling: `evals/evals.json` with **≥3 scenarios** (Anthropic skill-creator
convention — note there is *no standard runner yet*, so these are human/agent-
gradeable acceptance scenarios).

> **Naming-clash warning.** Anthropic's progressive-**disclosure** levels
> (L1 metadata always loaded ~100 tok → L2 body when triggered, keep <5k tok /
> <500 lines → L3 resources on demand) are a **different axis** from this repo's
> **enforcement** gradient (L1 instruction → L2 checking script → L3 CI/hook).
> Don't conflate "disclosure Level 2 = body text" with "enforcement L2 = script."

## Closed-set params

Anthropic frontmatter has no param schema, so validating "did the agent pass an
allowed `--bucket`?" is **our** responsibility. Express each closed-set flag with
**JSON Schema `enum`** — the canonical closed-set primitive — either inline in
`metadata.params` or as a sibling `params.schema.json`. This formalizes the
catalog's "closed-set values" rule (the one a batch once violated by writing a
verdict into the wrong column — incident B6).

## The enforcement gradient, formalized

Our L1→L2→L3 is the dominant pattern in two adjacent fields (independent
corroboration): SRE runbook-to-automation (manual → scripted → event-driven) and
policy-as-code. From policy-as-code we steal a **sub-tiering of L3** (Conftest's
`warn` vs `deny`): a **new** rule lands as `warn` (observed, non-blocking) and is
promoted to `deny` only once it proves out — a graceful on-ramp instead of a noisy
hard gate on day one. Promotion trigger (per doc 08): **violations recur.**

**The mechanism is one script at three altitudes:**
[`validate_skill.py`](validate_skill.py) —
- **L2:** `uv run skills/validate_skill.py` (skill-invoked / by hand)
- **L3 pre-commit:** the same script as a `repo: local` hook (blocks commit on
  nonzero exit)
- **L3 CI:** the same script as a GitHub Action

`--strict` promotes warnings to failures. One component, three altitudes — no
framework adopted.

```yaml
# .pre-commit-config.yaml (sketch — L3)
repos:
  - repo: local
    hooks:
      - id: validate-skills
        name: validate SKILL.md files
        entry: uv run skills/validate_skill.py
        language: system
        files: ^skills/.*/SKILL\.md$
        pass_filenames: false
```

## Open risks (from #14)

- **Spec drift / dual governance:** open-spec and product docs already diverge;
  the validator never blocks on open-spec-only fields, only on name/description.
- **`name == dir` is open-spec, UNVERIFIED as a product-runtime hard rule** — we
  enforce it as a safe convention.
- **No standard evals runner exists** — `evals/evals.json` is a documented
  convention; the scorer is on the adopter.

## Candidate practices (need a pilot before minting as a GP)

1. **Open Agent Skills spec as the on-disk format** (`name==dir`, body <500
   lines/<5k tokens, references one level deep).
2. **House frontmatter contract** layering `metadata.enforcement_level` +
   `metadata.params` onto the open spec.
3. **One validator, three altitudes**; closed-set params via JSON Schema `enum`;
   wire warn-only first, count false positives before flipping any rule to `deny`.
4. **Require `evals/evals.json` (≥3 scenarios)** per shipped skill.
5. **Document the disclosure-vs-enforcement naming clash** explicitly (done above).

*Snapshot 2026-06. The open spec is young and dual-governed — re-check
agentskills.io and the Anthropic docs before depending on any optional field.
Full primary-source citations: issue #14.*
