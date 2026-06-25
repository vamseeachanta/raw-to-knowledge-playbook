# Good Practices Catalog (living document)

Numbered, append-only. Each practice records the **rule**, the **why**
(usually an incident), and **how to apply**. New practices are added via PR
as the work surfaces them — see [CONTRIBUTING.md](https://github.com/vamseeachanta/raw-to-knowledge-playbook/blob/main/CONTRIBUTING.md).

---

## Extraction

**GP-01 — Extract deterministically; reserve LLMs for judgment.**
Why: LLM extraction of a 118-page standard yielded ~2% coverage (a summary),
hit copyright guardrails that no prompt overrides, and took hours. A
deterministic PDF library yielded 100% (48k words + 38 table CSVs) in
seconds.
Apply: tools extract; models verify, classify, route, review.

**GP-02 — Provisional by default.**
Why: auto-parsed tables are structurally consistent but value-wrong often
enough to poison a knowledge base.
Apply: every extracted artifact carries `parse_status:
provisional-unverified` until a vision pass promotes it. Record the
extraction level (`extraction_policy`) in frontmatter so consumers know what
they're reading.

**GP-03 — Strip watermarks before extraction.**
Why: rotated watermark overlays merge their glyphs into table cells and pass
every structural check.
Apply: neutralize rotated-placement Form XObjects in-memory pre-extraction;
config-driven; never modify the raw source file.

**GP-04 — Route by content, not folder; filter by value.**
Why: source archives are misfiled grab-bags; image-only/low-text PDFs paginate
into pure noise (one 73-page garbage doc observed).
Apply: classify on extracted text; word-count gate; junk filters for
catalogs/minutes/brochures; record every skip with a reason.

**GP-05 — The hardened ingest contract is all-or-nothing.**
Five rules — content routing, value filter, dedupe-before-write, selective
verbatim + provisional tables, index/log update. Applying a subset creates
duplicates, misfiling, or mislabeled trust states.

**GP-49 — Preflight large PDFs: measure, then pick the load strategy.**
Why: a 100MB+/1000-page PDF loaded whole stalls or OOMs the worker
mid-batch. A salvaged internal large-PDF reader build (autopsy:
[case study](case-studies/pdf-large-reader-salvage.md)) proved a cheap
assessment pass — bytes, pages, sampled complexity, defect probe — routes
files correctly before extraction starts; its memory-bounded tests held 50
medium pages under 100 MB peak streaming vs 200 MB list-loaded.
Apply: assess first (runnable: [examples/pdf-preflight/](https://github.com/vamseeachanta/raw-to-knowledge-playbook/tree/main/examples/pdf-preflight/)).
Route < 10 MB & simple → full load; ≥ 100 MB, > 500 pages, or complex →
fixed-size page chunks; everything else → page-at-a-time streaming. Any
critical preflight issue (encryption, failed first/last-page probe) forces
the careful lane. Treat > 10 % U+FFFD replacement characters in sampled text
as an encoding failure — route to the OCR lane (doc 11), never publish the
mojibake.

## Verification

**GP-06 — Select verification batches by data density.**
Why: alphabetical/file-order selection burned entire batches on blank forms
(0/24 verified); density ranking yields 5–7 verified per 12.
Apply: rank by numeric density; sink row-collapse suspects to the bottom
(don't auto-reject them — vision stays the authority).

**GP-07 — Check the rightmost column.**
Why: multi-header tables align on the left and shift on the right;
"confirm-first-cell-and-extrapolate" subagents over-verified 6 of 12 rows in
one batch.
Apply: every verification confirms at least one rightmost-column value.

**GP-08 — Serialize select→merge per domain.**
Why: the batch selector reads the main branch; selecting before the prior
batch merges re-picks identical rows (two duplicate batches shipped).
Apply: one in-flight verification batch per domain; cross-domain parallelism
is fine (separate queue files).

**GP-09 — Anchor on exact paths, never globs.**
Why: standard editions share table IDs; a glob verifies the wrong edition.

**GP-10 — Prefer the verdict citing a falsifiable defect.**
Why: duplicate batches produced opposite verdicts on one table; the rejection
cited an exact source-value mismatch, the verification was generic approval.
Apply: when reviews disagree, specific evidence wins; require evidence in
verdict notes.

**GP-11 — Rejections carry a defect class and feed a re-parse loop.**
Why: most rejected tables are real data wrongly extracted (transposed,
truncated, collapsed, contaminated) — recoverable once the extractor
improves.
Apply: tag the class in queue notes; after an extractor fix, re-extract
exactly the affected class, mapping by page + in-page order with shape
preservation as the correctness proof.

**GP-42 — Verify until PASS; the round count is a floor, not a ceiling.**
Why: a nominally two-round verify took three: round 1 caught the defect
*class*, round 2 caught the **incompleteness of the fix** — by building an
executable reproducer (a monkeypatched parser with synthetic inputs) that
code-reading alone had waved through.
Apply: re-review every fix adversarially until a clean PASS; ask reviewers
to build runnable reproducers for code findings; gate the fix on re-running
the *reviewer's own* reproducer against HEAD. A fix that addresses the cited
example but not the invariant fails the next round — that is the loop
working, not the loop failing. (Skill `adversarial-verify-loop`.)

**GP-47 — Score extracts against an independent engine; verify the
comparator harder than the pipeline.**
Why: the verify loop proves fidelity (extract == what the pipeline read) but
not correctness — both can share a defect. Scoring committed extracts
against a *different* extraction engine (office suite headless conversion,
a different PDF text engine, raw XML text nodes, a second format
implementation) turns "we believe it's faithful" into measured per-lane
precision/recall. The comparator itself is the trap: in the pilot, the
scoring tool's "exact" tier silently rounded numerics — three successive
fixes each satisfied only the probed case (6-sig-fig format → binary-float
identity → bounded-precision decimal context) before a width-matched
context made canonicalization precision-lossless **by construction**. A
flattering comparator bug poisons every downstream number.
Apply: pick oracles from a different codebase than the lane (and say so
honestly when independence is partial — two pure-python readers of one
container format prove less than two unrelated engines). Score on two
tiers: exact (formatting-only normalization, provably lossless at any
precision) and display-tolerant. **Attribute every sub-1.0 number** — each
residual is a diagnostic lead that resolves to a real lane loss (ledger
it), a legitimate engine difference (caveat it), or a comparator bug (fix
the comparator, never the score). Run the adversarial verify loop on the
comparator with *more* rigor than on the pipeline it scores. (Skill
`independent-oracle-validation`.)

**GP-48 — Completeness claims read the raw container, not the object
model.**
Why: a media inventory built to guarantee "nothing silently dropped" was
itself silently dropping 59 of 399 deck images (~15%) — the convenience
API's shape walk missed grouped pictures, placeholder pictures,
alternate-content fallbacks, and an entire **orphaned deleted slide** whose
image bytes still shipped inside the binary, invisible to every API reader.
An adversarial raw-XML census (count occurrences in the container; compare
sha256+size per item) caught it; three review rounds later the inventory
was census-exact.
Apply: when the deliverable *asserts completeness*, enumerate from the
container format directly (the zip members, the XML occurrences, the
relationship targets) — or at minimum census-check the API walk against the
raw container and fail on mismatch. Disclose what the document's own
*renderer* wouldn't show (fallback content, orphaned parts) with explicit
context labels rather than dropping or laundering it. Object models are for
*reading* content; containers are for *counting* it.

## Data plumbing

**GP-12 — Union-merge needs append-only; rewrites need dedup-on-write.**
Why: one full-queue rewrite turned union-merge into 46% row duplication.
Apply: self-healing dedup on every write, idempotent, with precedence rules;
never rely on one-time cleanups.

**GP-13 — Row identity must be non-degenerate for every row type.**
Why: blank fields in the identity tuple silently collapse distinct rows.

**GP-14 — Binary-faithful I/O for mixed-line-ending files; diff-size
assertions after every edit.**
Why: text-mode round-trips produced a 352-line phantom diff for a 12-row
edit.
Apply: binary read/write preserving per-row terminators; assert
`git diff --numstat == 2 × rows-changed`; harden for embedded newlines before
the first one appears.

**GP-15 — Status vocabularies are closed sets, separated by column.**
Why: an unregistered status got mangled by the normalizer; a verdict written
into the structural column corrupted a batch.
Apply: register new values before first use; batch prompts hard-specify
allowed values per column.

**GP-41 — Derived filenames are unique by construction, not by heuristic.**
Why: slugging attachment names collided derived outputs (`Plan.pptx` and
`Plan.pdf` both rendering to `plan.txt` → silent overwrite), and the obvious
patch — append an ordinal on collision — *still* collided a generated name
with a later real stem (`plan-2`); an adversarial reviewer proved the
overwrite with a reproducer.
Apply: generate candidate names in a loop whose **exit condition is the
uniqueness invariant itself** (exit only on an unused name) — deterministic
given the same inputs. Do not guard with fail-if-exists in idempotent
re-run pipelines (every legitimate re-run trips it). Record the final name
in the parent inventory so each input maps to its surviving output.

## Automation

**GP-16 — Resumable state machine + idempotent chunks.**
Apply: chunked work units, JSON state keyed by doc-set, per-chunk commit +
immediate state save, isolated worktrees, force-reset branch creation.

**GP-17 — One PR per tick; humans merge.**
Why: one-PR-per-publisher (13/tick) created chronic merge churn between
shared files; branch chaining diverged refs.
Apply: all work units accumulate on one branch per tick; automation never
merges.

**GP-18 — Don't buy parallelism you don't need.**
Why: concurrency-3 contended on git refs; deterministic extraction is so fast
that serial saturates the pipeline anyway.

**GP-19 — Reconstruct the environment in cron wrappers; parameters live in
the repo.**
Why: cron strips the interactive env (silent dispatch death); in-repo args
mean config changes ship by PR. Remember a running tick uses the script as
of launch.

**GP-20 — Prove a "hang" before killing it.**
Why: block-buffered stdout + timeout SIGKILL leaves an empty log while work
proceeds; a healthy job was falsely flagged.
Apply: unbuffered output + a stack-dump-on-timer before declaring anything
hung.

## Multi-agent discipline

**GP-21 — Orchestrator serializes git; workers only write files.**
Why: 60+ concurrent git procs produced a 19-minute D-state hang; background
git loses traceability.
Apply: atomic per-file commits in the foreground session; partition parallel
workers by disjoint file sets (e.g., per-domain queues).

**GP-22 — Adversarial review before merge, scaled to scope.**
Why: independent reviews found real bugs the author missed (stranded-commit
path, dedup precedence flag-loss).
Apply: every substantive PR gets at least one independent adversarial review;
prompts must force defect-hunting, not charitable reading.

**GP-23 — Verify subagent claims yourself — in both directions.**
Why: subagents over-verify tables (GP-07) and overclaim confidentiality
screening (one asserted "no confidential identifiers" while leaking project
folder names).
Apply: orchestrator spot-checks verifications and greps outputs for known
identifiers before anything ships.

**GP-24 — Capture lessons as durable memory/skills at the moment of
incident.**
Why: every practice in this file exists because it was written down when it
bit; re-derivation is expensive.
Apply: one fact per memory file; promote recurring workflows into versioned,
parameterized skills (see [08-skills-catalog.md](08-skills-catalog.md)).

## Office formats (Excel / Word / PowerPoint)

**GP-27 — Inventory and tier workbooks before converting any.**
Why: a corpus scan surfaced 4,100+ legacy calculation workbooks; converting
in encounter-order wastes budget on low-value/high-complexity files.
Apply: auto-scan every workbook (sheets, dimensions, formula counts,
function histogram, cross-sheet references) → rank by priority (P0–P2) ×
complexity tier (1–6) → budget extraction effort per tier; keep a registry.

**GP-28 — Cached Excel values are not ground truth.**
Why: workbooks saved without recalculation carry stale/missing cached
results, which silently corrupts cached-value-as-oracle testing.
Apply: classify cells `cached_ok` / `cached_missing` / `cached_suspect`;
emit test assertions only for `cached_ok`; verify ported code by
re-execution against those cells.

**GP-29 — Extract the algorithm, not the cells.**
Why: pattern detection on row/column-repeated formula regions yielded
2.5×–44× compression (loops instead of cell-by-cell transliteration) —
and the compression ratio doubles as a conversion-effort estimator.
Apply: detect repetition patterns before code generation; a 500-row formula
column is one loop.

**GP-30 — Integrate extractions before extracting more.**
Why: a pilot extracted 656K+ formulas from 6 workbooks; outputs sat as
unintegrated stubs while thousands more workbooks queued — extraction
outpaces integration by orders of magnitude.
Apply: wire each extraction into live, tested code before widening the
funnel; measure progress by integrated calculations, not extracted
formulas.

**GP-31 — Strip client context, keep methodology, with round-trip
traceability.**
Why: legacy workbooks mix validated engineering logic with
client-confidential data — carrying raw files forward creates legal/IP
risk; losing the source link destroys provenance.
Apply: extract only generic methodology (equations, input ranges, worked
examples → TDD fixtures); deny-list scan before archiving; never copy the
raw workbook; every code artifact records its source-workbook mapping.

**GP-40 — Containers are formats too: inventory, then recurse.**
Why: an email lane that extracts header + body silently drops every
attachment — in the pilot, the one substantive attachment was a slide deck
holding the quantified comparison the thread's prose only referenced; the
hash inventory also exposed, for free, the same logo image recurring under
different filenames across threads.
Apply: split the remedy by guarantee. **Inventory** (deterministic): every
attachment recorded in the parent extract — name + sha256 + size — so
nothing disappears unaccounted, including formats with no extraction lane
(images stay inventory-only: disclosure without interpretation).
**Recurse** (derived): attachments with a format lane go through the *same*
extractor as standalone files (`<parent>__att-<slug>.*`), so an embedded
deck renders identically to a standalone one — one format, one parser, one
verification surface. Attachment bytes touch a temp dir only; the
raw-binary firewall holds for nested content. Forwarded emails recurse
through the email lane itself.

## Structured data & model files (CSV / delimited / solver ASCII)

**GP-32 — Probe dialect and validate field counts at ingestion.**
Why: extra delimiters in a value silently shift every downstream column
while the file still "parses"; an ad-hoc pipe-delimited format corrupted
the first time content contained a `|`; mixed line endings rewrote
themselves through text-mode I/O (B3).
Apply: detect delimiter/quoting/encoding/line-endings per file; assert
per-row field count == header count; generate delimited output only through
a real CSV writer, never string concatenation.

**GP-33 — Validate content parity, not row counts.**
Why: a row-count-only validator accepted a header-only CSV paired with a
non-empty sibling artifact — matching shapes, missing data.
Apply: compare cell contents or deterministic per-row hashes between
artifacts that must agree.

**GP-34 — Conventions are data: capture units, signs, and frames in a
provenance sidecar.**
Why: a dataset with negative lever-arm + positive force columns produced
flipped-sign moments downstream; it was intentional notation, documented
nowhere — indistinguishable from a defect.
Apply: every ingested dataset ships a sidecar recording per-column units,
sign conventions, coordinate frames, and producer quirks.

**GP-35 — Estimate density before committing digitization effort.**
Why: one standard with 166 tables + 95 figures cost ~10× a sibling with 2
figures; document count predicts nothing.
Apply: scan table/figure/column density first; budget and tier by density.

**GP-36 — Solver decks are build artifacts: parse to externalized config,
regenerate, round-trip.**
Why: hand-edited or hardcoded input decks serve one project; an
industry-grade deliverable must be re-targetable by editing reviewable YAML
(materials, thresholds, safety classes, data locations) with zero code
changes.
Apply: deck → parsed YAML config → regenerated deck must round-trip to
identity; the config is the reviewed, git-tracked artifact. Keep the
parse/extract path runnable without the solver license — only execution
needs it.

**GP-37 — Defaults need a ledger; outputs need sanity gates.**
Why: a parser that silently injected default values had to have them
stripped — assumed inputs that aren't surfaced poison downstream trust;
solver outputs consumed without range/coverage checks do the same from the
other end.
Apply: every assumed/defaulted input is provenance-tagged in an assumption
ledger surfaced with results; outputs pass physical-range and coverage
gates before anyone consumes them. (Defaults are fine when recorded,
forbidden when silent.)

## Imagery & scans

**GP-38 — Images are described, never "extracted"; label the
interpretation.**
Why: OCR and vision descriptions are model interpretations, not copies —
mixing them with deterministically-extracted text launders guesses into
trusted-looking content; an image-only document once paginated 73 pages of
noise into the wiki before the word-count gate existed.
Apply: route no-text-layer sources to the description lane; output carries
`extraction_policy: described`/`ocr-interpreted`, falsifiable observations
separated from inference, and verbatim transcription of any legible
in-image text (the only checkable part). Verify with an independent second
description pass.

**GP-39 — Classify Excel as data vs calculation vs canvas by scanned
structure, not filename.**
Why: filenames lie (D4); the three variants route to entirely different
lanes (delimited-data parsing vs formula→code vs describe-only).
Apply: auto-scan formula density, image count, and function mix per
workbook; route accordingly (data → doc 10 lane, calculation → doc 09
lane, image-canvas → doc 11 lane).

## Governance

**GP-25 — Raw licensed sources never enter the repo.**
Apply: raw PDFs live in an off-repo archive; the wiki stores derived data +
a source pointer; a deny-list scan runs pre-commit (keys, private paths,
client identifiers).

**GP-26 — Screen for confidential identifiers at write time, verify at
publish time.**
Why: leakage happens through agents' generated text, not just copied files.
Apply: maintain a known-identifier list; grep all outbound content against
it; public/private routing enforced by frontmatter + pre-commit check.

## Citation & retrieval

**GP-43 — Cite mutable sources with two dates: ingested and last-verified.**
Why: web sources drift silently; a single citation date conflates "when we
learned this" with "when we last checked it still holds." Running a two-date
footnote contract across a multi-hundred-page wiki is what makes stale claims
visibly stale at review time instead of silently trusted.
Apply: every footnote citing a URL carries `(ingested YYYY-MM-DD, last
verified YYYY-MM-DD)`; re-verification refreshes the second date; a
content-hash change instead invalidates the verification and forces
supersession (doc 16's cascade rule applied at the source boundary).

**GP-44 — The answer layer may only assert what resolves to a stored, citable record.**
Why: a client-side model answering over an honest store stitched a fabricated
sign-off date into an otherwise-correct answer; the store never contained the
date. Per-claim citation IDs made the fabrication detectable, and a protocol
now rejects uncited claims at the answer layer.
Apply: require a resolvable record ID per factual claim; treat any claim
without one as "inferred — flag it"; spot-check by tracing claims back to
records.

**GP-45 — Log zero-result queries; repeated misses are your ingestion backlog.**
Why: a persisted failed-queries log (searches returning 0 results) turned out
to be the cheapest gap detector in a production knowledge store — repeat
misses name exactly the knowledge users want and the store lacks.
Apply: persist every zero-result retrieval with timestamp + query; review
weekly; convert repeats into ingest/authoring tasks.

**GP-46 — Retrieval must degrade, not die, when the embedding host is down.**
Why: an embedding-service outage blinded semantic retrieval; reads survived
only because a lexical fallback over the compiled narrative layer existed and
was documented before the outage.
Apply: keep a lexical/keyword leg in the retrieval stack (hybrid, not
dense-only); document the degraded read path; alert on the outage but never
block reads on the embedder.

## CAD geometry & 2D drawings (STEP/IGES/native parts/DWG)

**GP-50 — Header-detect CAD format and version; never trust the extension or a "structured" claim.**
Why: in an estate scan, every `.nc` file was NetCDF (hydrodynamics output),
not CNC G-code — extension classification would have reported a CAM inventory
that did not exist; DWG spanned ~25 years readable only from the 6-byte
version code (`AC1014`=R14 … `AC1032`=2018), and STEP's `FILE_SCHEMA` header
distinguishes AP203/214/242 and names the originating CAD system for free.
Apply: read magic/header bytes (DWG `AC####`, STEP `FILE_SCHEMA`, file magic);
record format + version + originating system as provenance; treat the
extension as a hint and resolve ambiguous ones (`.nc`, `.dat`, `.prt`) by content.

**GP-51 — Exclude editor lock/temp files before counting a native-CAD estate.**
Why: `~$`-prefixed CAD lock files were ~15% (≈8,800 of ≈60,000) of the
apparent part/assembly population; counting them inflates every effort,
billing, and coverage estimate.
Apply: filter lock/temp/autosave patterns (`~$*`, `*.bak`, swap files) before
any census; report real vs raw counts and keep the rule in the inventory script.

**GP-52 — For geometry conversion, gate on a round-trip invariant oracle, not "it opened."**
Why: a STEP→STEP round-trip was proven lossless only by comparing solid-body
count + bounding box + volume (rel-err ≤1e-6); separately, IGES re-read as
unoriented surfaces (0 solids, meaningless negative volume) — a silent loss
that a "file written / viewer opens" check misses entirely.
Apply: after any geometry convert, re-read the output and compare solid count,
bbox, and volume/mass within tolerance; **sew** surface-only formats (IGES)
before trusting any volume/mass; use the kernel's structured (XCAF) reader,
not the flat one, when the BOM tree/part names matter (a flat reader collapsed
an 11-product assembly to 2 solids).

**GP-53 — De-identify a raw-path file manifest before its first commit to a public repo.**
Why: a per-file CAD manifest's path column embedded a personal name plus
client/field linkage and was pushed to a public branch before the leak was
caught; auto-mode could not force-push to purge history (deny rule), so the
blob persisted pending a maintainer squash-merge.
Apply: replace raw paths with hashes and relabel client/vendor folders
*before* the first commit; keep the full raw manifest off-repo (private);
build the de-identification key before authoring any client-mapping doc; if a
leak ships, escalate to a maintainer squash-merge / branch recreation.

## Multi-agent research & verification

**GP-54 — Trust the verifier's per-claim log, not its summary; re-verify decision-critical facts firsthand.**
Why: a fan-out deep-research run degraded twice in one session — its *synthesis*
agent returned a stub object, and the *verify* phase was API-rate-limited into
mass abstentions (claims neither confirmed nor refuted). The real value survived
in the per-claim vote log, and the decision-critical facts (OSS **license**
terms governing whether a package can ship) were resolved only by fetching each
repo's license directly.
Apply: persist per-claim verifier votes separately from the final summary, and
hand-synthesize from the log if the summary is malformed; treat a rate-limited
*abstain* as "unverified", never as a result; and independently confirm the few
facts a decision actually hinges on (licenses, safety limits, numbers you'll
act on) against a primary source — a confident multi-agent summary is still a
claim until its load-bearing facts are checked.

---

*Next ID: GP-55.*
