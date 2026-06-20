---
name: archive-extraction-integrity
description: >
  Extracts a compressed archive (RAR/ZIP/7z) and then proves the extraction is
  byte-faithful by re-hashing every extracted file against the container's stored
  per-entry checksums — because an open-source decoder can report success while
  silently writing wrong bytes at the correct size (presence and size are NOT
  fidelity). Falls back across decoders (7z, bsdtar, official unrar) for entries
  one engine mis-decodes, and reports the exact set of files that no available
  decoder can reproduce. Use when extracting any archive before its contents enter
  an ingestion pipeline, especially RAR4 archives or when only partial decoders
  (p7zip, libarchive) are installed.
license: CC-BY-4.0
compatibility: >
  Requires the archive plus at least one decoder (7z / bsdtar). CRC verification
  needs the container to store per-entry checksums (RAR, ZIP, 7z do; plain tar does
  not). Byte-perfect recovery of decoder-defeating entries needs the official
  RARLAB `unrar` (download/run is a separate, user-approved step).
metadata:
  version: "1.0"
  enforcement_level: L2            # callable verifier script over the extracted tree
  status: template
  incident_refs: silent-decoder-corruption,presence-not-fidelity,decoder-cascade-desync
  params: "archive:str | dest:str | decoders:str=auto"
---

# archive-extraction-integrity

> Template skill (doc 03, doc 04). An archive is the **first** raw container an
> ingestion run touches; if its files come out corrupt the whole downstream extract
> is built on sand. The trap is that extraction *looks* like it worked: the right
> file count appears, sizes match the listing, no obvious error halts the run — yet
> some files hold garbage of the correct length. This skill makes the container's
> own per-entry checksums the acceptance gate, not the file's mere existence.

> **Field incident this encodes.** A 205 MB cPanel `.rar` (RAR4, non-solid).
> `7z x` raised `Unsupported Method` on ~2008 entries; `bsdtar` decoded those but
> hit `File CRC error` / `Bad RAR file data` / `Invalid location to Huffman tree`
> on others and **aborted the stream**. After a multi-decoder pass every file was
> present at its listed size — but a CRC32 re-hash against the archive proved
> **81 of 2826 files were silently corrupt** (right size, wrong bytes). Only the
> official `unrar` decodes that class. Without the CRC gate the corruption ships
> undetected.

## Trigger
`/archive-extraction-integrity <archive> [--dest DIR] [--decoders auto|7z,bsdtar,unrar]`

## Preconditions
1. The container format stores **per-entry checksums** (RAR/ZIP/7z). Plain `tar`
   does not — for tar, fidelity must come from an external manifest of hashes or
   this skill degrades to size/count checks only (state that explicitly).
2. At least one decoder is installed (`7z`/`7za`, `bsdtar`). Know which: different
   engines have **complementary** blind spots on the same archive.
3. Enough free disk for the *uncompressed* total (read it from the listing, not the
   archive size) plus headroom for a parallel recovery copy.
4. Recovering decoder-defeating entries may require the official RARLAB `unrar`;
   downloading/running an external binary is a **separate user-approved step**, not
   something this skill does silently.

## Steps
1. **List before extracting.** Dump the manifest (`7z l -slt`, `bsdtar -tvf`): note
   entry count, uncompressed total, whether the archive is **solid**, and that it
   is **not** encrypted. *Solid matters:* in a solid archive files share a window,
   so per-file fallback/recovery is impossible — only a single clean full pass
   works. Non-solid is what makes divide-and-conquer recovery viable.
2. **First-pass extract** with the primary decoder into a clean `--dest`. Capture
   stderr — do not trust the exit code alone. Two engines fail differently:
   - `7z` (p7zip) tends to emit `Unsupported Method` and **cascade-desync**: after
     one undecodable block it mislabels many *good* following files too, so its
     failure list is unreliable as a capability list.
   - `bsdtar` (libarchive) tends to **abort the whole stream** at the first
     `File CRC error` / `Bad RAR file data`, zeroing everything after it.
3. **Fallback across decoders for the gaps.** Because the archive is non-solid,
   re-extract the missing/aborted entries with the *other* engine — often in
   isolation (one path at a time, or an explicit `--exclude` loop that drops the
   one entry an engine aborts on, then re-runs) so a single bad entry can't
   desync the rest. Engines are complementary: files one calls `Unsupported` the
   other usually decodes, and vice versa.
4. **CRC gate — the core check.** This is the acceptance test, run over the final
   tree (see `verify_extraction.py`): for **every** non-empty entry, recompute its
   checksum (RAR/ZIP/7z = CRC32, `zlib.crc32`) and compare to the value the
   container stores for that entry. Classify each file as: **OK** (checksum
   matches), **genuinely-empty** (size 0 in the manifest, empty on disk), or
   **CORRUPT/MISSING** (on disk but checksum differs, or absent). *Size-match is
   not a pass* — corrupt files here matched their sizes exactly.
5. **Report the irreducible set.** Emit the exact list of entries no available
   decoder reproduces (CRC still wrong after all fallbacks), grouped by extension/
   size, with the count `good / total`. Name the remedy explicitly: these need a
   fuller decoder (official `unrar`); flag it as a user decision, do not silently
   download-and-run.
6. **Re-verify after any recovery step.** If the official `unrar` (or another tool)
   is then used on the irreducible set, re-run the CRC gate over only those paths —
   acceptance is a clean checksum, never "the tool exited 0."

## Verification
- Every non-empty extracted file's recomputed checksum equals the container's
  stored checksum for that entry (the manifest is fully reconciled — no file passes
  on size/presence alone).
- Every size-0 file on disk corresponds to a size-0 manifest entry (no real entry
  silently truncated to empty).
- The reported `good / total` count is reproducible by re-running the verifier, and
  the CORRUPT/MISSING list is exact (each item cites computed-vs-stored CRC).
- No file is declared recovered without a post-recovery checksum match.

## Cleanup
- Remove temp recovery copies and any per-decoder scratch dirs (e.g. a `/tmp`
  isolation-extract tree). Keep only the final verified extraction and the
  verifier's report.
- Do **not** leave a downloaded external decoder binary on `PATH` unless the user
  asked to install it; treat it as scratch.

## Incident appendix
| Rule | Why |
|---|---|
| CRC-verify every file against the manifest | Decoders report success while writing wrong bytes; presence/size never proves fidelity (81/2826 silently corrupt) |
| Size-match is not a pass | The corrupt files matched their listed sizes exactly — only the checksum caught them |
| Don't trust a decoder's own failure list | p7zip cascade-desyncs and mislabels good files as `Unsupported`; the manifest CRC is the only reliable oracle |
| Capture stderr, not just exit code | bsdtar's whole-stream abort and 7z's per-entry skips both need the error text to locate gaps |
| Exploit non-solid for per-file fallback | Solid archives can't be recovered file-by-file; check `Solid = -` before attempting it |
| Use complementary decoders | 7z and libarchive fail on disjoint entry sets; together they cover more than either alone |
| External decoder download is a user gate | Fetching and running an agent-chosen binary is out-of-band; surface the need, let the user decide |
| Re-verify after recovery | A recovery tool exiting 0 is not acceptance; only a post-fix checksum match is |
