#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Verify an extracted tree against an archive's stored per-entry checksums.

The acceptance gate for `archive-extraction-integrity`: presence and size never
prove fidelity — an open-source decoder can write wrong bytes at the right size.
Only re-hashing each extracted file against the container's stored CRC catches
that silent corruption.

Supported containers: RAR / ZIP / 7z (all store a CRC32 per entry). It shells out
to `7z l -slt` for the manifest (path / size / CRC), so it works for any format
7-Zip can *list* even when it cannot fully *decode* it — which is the whole point:
the listing CRC is the oracle the (possibly broken) extraction is judged against.

Usage:
    uv run verify_extraction.py <archive> <extracted_root>
        # <extracted_root> is the dir the archive was extracted INTO, i.e. the
        # parent of the archive's top-level entry paths.

Exit 0 only when every non-empty entry's CRC matches and no entry is missing.
Prints a good/total summary and the exact CORRUPT/MISSING list (computed vs stored).
"""
from __future__ import annotations
import subprocess, sys, zlib, os
from pathlib import Path


def parse_manifest(archive: str):
    """Yield (path, size:int, crc:str|"") per file entry via `7z l -slt`."""
    out = subprocess.run(["7z", "l", "-slt", archive],
                         capture_output=True, text=True).stdout
    cur: dict[str, str] = {}
    base = os.path.basename(archive)
    for line in out.splitlines():
        if line.strip() == "":
            if "Path" in cur:
                yield cur
                cur = {}
            continue
        if " = " in line:
            k, v = line.split(" = ", 1)
            cur[k.strip()] = v
    if "Path" in cur:
        yield cur


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    archive, root = sys.argv[1], sys.argv[2]
    rootp = Path(root)

    ok = empty_ok = corrupt = missing = 0
    bad: list[tuple[str, str]] = []
    checked = 0
    for e in parse_manifest(archive):
        path = e.get("Path")
        if not path:
            continue
        # The archive's own header block carries 'Physical Size'/'Type'; real
        # file entries do not. Skip it however the archive path was spelled.
        if "Physical Size" in e or "Type" in e:
            continue
        if "D" in e.get("Attributes", ""):           # directory
            continue
        size = int(e.get("Size", "0") or 0)
        crc = (e.get("CRC", "") or "").upper()
        checked += 1
        disk = rootp / path
        if not disk.exists():
            missing += 1
            bad.append(("MISSING", path))
            continue
        data = disk.read_bytes()
        if size == 0:
            if len(data) == 0:
                empty_ok += 1
            else:
                corrupt += 1
                bad.append(("SIZE0-but-has-data", path))
            continue
        if not crc:
            # listing exposes no CRC for this entry — can't prove fidelity
            bad.append(("NO-STORED-CRC", path))
            continue
        d = "%08X" % (zlib.crc32(data) & 0xFFFFFFFF)
        if d == crc:
            ok += 1
        else:
            corrupt += 1
            bad.append((f"CRC computed={d} stored={crc}", path))

    print(f"entries checked     : {checked}")
    print(f"CRC-verified OK     : {ok}")
    print(f"genuinely-empty OK  : {empty_ok}")
    print(f"CORRUPT             : {corrupt}")
    print(f"MISSING             : {missing}")
    print(f"=> GOOD total       : {ok + empty_ok} / {checked}")
    if bad:
        print("\n--- files failing the CRC gate ---")
        for reason, path in bad:
            print(f"  {reason}\t{path}")
    return 0 if (corrupt == 0 and missing == 0 and not bad) else 1


if __name__ == "__main__":
    raise SystemExit(main())
