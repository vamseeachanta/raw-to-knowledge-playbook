# ACE Public-Output Redaction Contract

Issue 63 defines the publication canary for ACE-derived public artifacts. The canary imports the issue 66 public-token fixture contract, the issue 68 public-surface scanner, and the issue 69 legal/security scan instead of redefining those rule engines.

Public source references use `public_source_token` only. Raw private provenance fields, raw source digest terms, private lookup material, host paths, personal identifiers, private-like identifiers, media metadata, title-block/BOM strings, copied private snippets, and unsafe issue-comment bodies are blocked before publication.

Git commit identifiers are allowed only as governance evidence fields such as `reviewed_commit_sha`, `commit_sha`, or `git_commit_sha`. They are not source provenance and must not be presented as public source references.

The committed deny-list supplement is schema-like and public-safe. Runtime private deny-list inputs, if used later, must stay outside tracked repo state and enter only through an operator-provided local path or environment variable.

This document is a methodology artifact. Adding ACE-derived content to docs navigation, `mkdocs.yml`, `llm-wiki`, GitHub-public summaries, or external publication requires a passing issue 63 canary command over the exact public output surfaces.
