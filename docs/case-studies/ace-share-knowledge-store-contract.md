# ACE Share Knowledge-Store Contract

Issue 61 defines the public-safe method contract for ACE-derived knowledge storage. It does not publish corpus content, source-root paths, source identifiers, exact private counts, or lookup material.

The contract separates logical storage forms from physical backends. Downstream waves may bind to forms such as `landing_page`, `part_file`, `dataset_table`, `media_descriptor`, `geometry_metadata`, `private_sidecar_record`, `exclusion_record`, `retrieval_chunk`, and `eval_case`, but the storage engine remains out of scope.

Each stored artifact must carry identity, routing, lifecycle, verification, provenance, evaluation, and success metadata. Route targets and logical stores come from issue 65. Manifest evidence comes from issue 62 through opaque snapshot status records. Public-output certification remains owned by issue 63.

Lifecycle state is closed: `candidate`, `provisional`, `verified`, `rejected`, `superseded`, and `stale_requires_rescreen`. Source replacement, manifest drift, visibility changes, route changes, parser changes, and policy changes reset affected artifacts to `stale_requires_rescreen`. A confidentiality re-screen is required before an artifact can return to `provisional`, and independent verification is required before it can return to `verified`.

Retrieval chunks must preserve citation, logical document key, edition, revision, current/as-of flags, visibility, lifecycle state, parse status, hash reference, structure type, route target, and logical target store. Table chunks must preserve table structure. Golden and silver evaluation cases stay outside ingest paths and chunk stores.

`% ingested success` is measured as `successful_routed_items / eligible_candidate_items * 100`. Hard exclusions are reported separately as `% excluded`. Control-plane issues use the `not_applicable_control_plane` status and emit no percentage.

This page is a methodology artifact only. It must remain scan-clean and must not be added to public navigation, wiki publication, or public ACE corpus summaries until the issue 63 canary exists and passes.
