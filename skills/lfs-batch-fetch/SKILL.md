---
name: lfs-batch-fetch
description: >
  Fetches the real bytes behind off-disk Git LFS pointer files via the LFS Batch
  API when git-lfs and sudo are unavailable, using a host token, and verifies the
  download because the content sha256 IS the pointer oid. Use when a source binary
  in a Git repo is a stored LFS pointer (a tiny version-oid-size stub) and you must
  read the actual file to extract from it, without installing git-lfs.
license: CC-BY-4.0
compatibility: Requires curl + a `gh`-class auth token for the host, jq for JSON, and a temp dir outside any repo; no git-lfs install or sudo needed
metadata:
  version: "1.0"
  enforcement_level: L2            # callable + the sha256==oid check is a hard gate
  status: template
  incident_refs: lfs-pointer-offdisk,raw-binary-firewall
  params: "pointer:str | dest:str"
---

# lfs-batch-fetch

> Template skill (doc 02, doc 12). When a corpus lives in a Git repo with large
> binaries stored in **Git LFS**, a fresh checkout (or a sparse/partial clone)
> gives you only **pointer files** — the actual bytes are off-disk on the LFS
> server. If `git lfs` isn't installed and you can't `sudo`, you are not stuck:
> the LFS Batch API is plain HTTPS + JSON, and the protocol's own oid is a free
> integrity check.

## Trigger
`/lfs-batch-fetch <pointer-file> [--dest <temp-dir>]`

## Preconditions
1. The file is a **real LFS pointer**: a few-line text stub of the form
   ```
   version https://git-lfs.github.com/spec/v1
   oid sha256:<64-hex>
   size <bytes>
   ```
   (If it is the actual binary, you do not need this skill.)
2. You have a host auth token (`gh auth token` for GitHub) with read access to
   the repo, and the repo's HTTPS clone URL.
3. A **temp dir outside any tracked repo** is chosen as `--dest` — the raw binary
   must never land inside a repo working tree (raw-binary firewall).

## Steps
1. **Parse the pointer.** Extract `oid` (the `sha256:` hex) and `size` (integer
   bytes) from the stub. These two fields are the whole request payload.
2. **Call the Batch API.** POST to `<clone-url-without-.git>.git/info/lfs/objects/batch`
   (e.g. `https://github.com/owner/repo.git/info/lfs/objects/batch`) with:
   - `Authorization: Bearer $(gh auth token)`
   - `Accept: application/vnd.git-lfs+json`
   - `Content-Type: application/vnd.git-lfs+json`
   - body: `{"operation":"download","transfers":["basic"],"objects":[{"oid":"<oid>","size":<size>}]}`
3. **Read the signed URL.** The response `objects[0].actions.download.href` is a
   short-lived signed object-store (e.g. S3) URL. Honor any returned `header`
   map on the download request; do **not** reuse the bearer token against the
   signed URL.
4. **Download to the temp dir.** `curl -L -o <dest>/<oid>.bin "<href>"`. Stream
   to disk; never into the repo.
5. **Verify — the oid is the hash.** Compute `sha256sum` of the downloaded file.
   It MUST equal the pointer's `oid`. The LFS protocol defines the oid *as* the
   content sha256, so this is a free, mandatory integrity gate — a mismatch means
   a truncated/wrong/tampered download. STOP on mismatch.
6. **Hand off, then forget the binary.** Pass the verified temp-file path to the
   extractor (e.g. `source-extract-fidelity`). The extractor emits text/CSV +
   the **sha256 pointer**; the raw binary stays in the temp dir and is deleted on
   cleanup.

## Verification
- `sha256sum <downloaded>` == the pointer's `oid` (hard gate; non-negotiable).
- The downloaded byte count == the pointer's `size`.
- No raw binary path is inside any repo working tree (`git check-ignore` /
  path-prefix assertion against every repo root).

## Cleanup
- Delete the temp binary after extraction. Only derived text/CSV + a `sources:`
  sha256 pointer persist. The signed URL expires on its own.

## Incident appendix
| Rule | Why |
|---|---|
| sha256(download) == pointer oid | The protocol oid is the content hash — free, mandatory verification; catches truncated/tampered fetches |
| Temp dir outside any repo | Raw-binary firewall: licensed/confidential bytes never enter a tracked tree, only derived parts + a pointer |
| Don't reuse bearer on the signed URL | The object-store URL is pre-signed; resending auth can 400/leak the token to a third-party host |
| Honor returned `header` map | Some hosts require object-store-specific headers; omitting them fails the download |
