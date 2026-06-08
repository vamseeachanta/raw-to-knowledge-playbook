#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Validate SKILL.md files against the playbook's skill-authoring standard.

One script, three altitudes (the enforcement gradient, docs/08 + AUTHORING-STANDARD.md):
  L2  invoked by a skill / by hand:   uv run skills/validate_skill.py
  L3  pre-commit (`repo: local` hook): same script, blocks the commit on nonzero exit
  L3  CI (GitHub Action):              same script

Tiering follows policy-as-code prior art (Conftest warn/deny): structural rules
that incidents already justified are DENY (fail the build); newer/recommended
conventions are WARN (observed, not blocking) until they prove out — pass
--strict to promote warnings to failures.

Standard targeted: the open Agent Skills spec (agentskills.io, Apache-2.0) for
name/description/license/compatibility/metadata, plus this repo's house rules
(required body sections + incident appendix). See skills/AUTHORING-STANDARD.md.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")          # no leading/trailing/double hyphen
RESERVED = {"anthropic", "claude"}
REQUIRED_SECTIONS = ["Trigger", "Steps", "Verification", "Cleanup", "Incident appendix"]
RECOMMENDED_SECTIONS = ["Preconditions"]
VALID_ENFORCEMENT = {"L1", "L2", "L3"}


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[3:end].strip("\n")
    body = text[end + 4:]
    return fm, body


def section_titles(body: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"(?m)^##\s+(.+)$", body)]


def validate_one(skill_dir: Path):
    """Return (errors, warns) for one skill directory."""
    errors, warns = [], []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"{skill_dir.name}: no SKILL.md"], []
    fm_text, body = split_frontmatter(md.read_text())
    if fm_text is None:
        return [f"{skill_dir.name}: missing or malformed YAML frontmatter"], []
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        return [f"{skill_dir.name}: frontmatter is not valid YAML ({e})"], []

    # --- DENY: name (open-spec hard rules) ---
    name = fm.get("name")
    if not name:
        errors.append(f"{skill_dir.name}: frontmatter missing required `name`")
    else:
        if len(name) > 64:
            errors.append(f"{name}: name exceeds 64 chars")
        if not NAME_RE.match(name):
            errors.append(f"{name}: name must be lowercase a-z/0-9/-, no leading/trailing/double hyphen")
        if name in RESERVED or any(r in name.split("-") for r in RESERVED):
            errors.append(f"{name}: name uses a reserved word ({RESERVED})")
        if name != skill_dir.name:
            errors.append(f"{name}: name must match parent directory '{skill_dir.name}'")

    # --- DENY: description (open-spec hard rules) ---
    desc = (fm.get("description") or "").strip()
    if not desc:
        errors.append(f"{skill_dir.name}: frontmatter missing required `description`")
    else:
        if len(desc) > 1024:
            errors.append(f"{skill_dir.name}: description exceeds 1024 chars")
        if "<" in desc or ">" in desc:
            errors.append(f"{skill_dir.name}: description must not contain XML tags / angle brackets")
        if not re.search(r"\bUse (when|before|to|as|for)\b", desc):
            warns.append(f"{skill_dir.name}: description should state WHEN to use it ('Use when …') for skill selection")

    # --- DENY: required body sections (house rule, incident-justified) ---
    titles = section_titles(body)
    for sec in REQUIRED_SECTIONS:
        if not any(t == sec or t.startswith(sec) for t in titles):
            errors.append(f"{skill_dir.name}: missing required body section '## {sec}'")
    for sec in RECOMMENDED_SECTIONS:
        if not any(t.startswith(sec) for t in titles):
            warns.append(f"{skill_dir.name}: recommended body section '## {sec}' absent")

    # --- WARN: recommended frontmatter ---
    if not fm.get("license"):
        warns.append(f"{skill_dir.name}: no `license` field (open-spec optional, recommended for portability)")
    meta = fm.get("metadata") or {}
    enf = meta.get("enforcement_level")
    if enf not in VALID_ENFORCEMENT:
        warns.append(f"{skill_dir.name}: metadata.enforcement_level should be one of {sorted(VALID_ENFORCEMENT)} (got {enf!r})")

    # --- WARN: evals/evals.json (Anthropic convention; no standard runner yet) ---
    evals = skill_dir / "evals" / "evals.json"
    if not evals.exists():
        warns.append(f"{skill_dir.name}: no evals/evals.json (recommend >=3 scenarios)")
    else:
        try:
            scen = json.loads(evals.read_text())
            items = scen.get("evals", scen) if isinstance(scen, dict) else scen
            if not isinstance(items, list) or len(items) < 3:
                warns.append(f"{skill_dir.name}: evals/evals.json should have >=3 scenarios (has {len(items) if isinstance(items, list) else '?'})")
        except json.JSONDecodeError as e:
            errors.append(f"{skill_dir.name}: evals/evals.json is not valid JSON ({e})")

    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate SKILL.md files against the authoring standard.")
    ap.add_argument("paths", nargs="*", help="skill dirs or SKILL.md files (default: all under skills/)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    if args.paths:
        dirs = [Path(p).parent if Path(p).name == "SKILL.md" else Path(p) for p in args.paths]
    else:
        root = Path(__file__).parent
        dirs = sorted(d for d in root.iterdir() if d.is_dir() and (d / "SKILL.md").exists())

    all_err, all_warn = [], []
    for d in dirs:
        e, w = validate_one(d)
        all_err += e
        all_warn += w

    for w in all_warn:
        print(f"WARN  {w}")
    for e in all_err:
        print(f"DENY  {e}", file=sys.stderr)

    n = len(dirs)
    if all_err:
        print(f"\nFAIL: {len(all_err)} error(s), {len(all_warn)} warning(s) across {n} skill(s)", file=sys.stderr)
        return 1
    if args.strict and all_warn:
        print(f"\nFAIL (--strict): {len(all_warn)} warning(s) across {n} skill(s)", file=sys.stderr)
        return 1
    print(f"\nPASS: {n} skill(s) valid ({len(all_warn)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
