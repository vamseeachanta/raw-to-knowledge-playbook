#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["pdfplumber>=0.11", "pypdf>=4.0"]
# ///
"""Large-PDF preflight — measure, then pick the load strategy (GP-49).

Before any extraction starts, a cheap assessment pass answers three questions:

    1. HOW BIG is this really?      (bytes, pages, bytes/page)
    2. HOW COMPLEX is it?           (sampled images/fonts → 0-100 score)
    3. WHAT WILL BREAK?             (encryption, page-probe failure,
                                     U+FFFD replacement-char ratio)

and routes the file to one of three extraction strategies:

    full_load     small & simple   — open once, read everything
    stream_pages  the default      — generator, one page in memory at a time
    chunk_batch   big or complex   — fixed-size page chunks, freed per chunk

Heuristics salvaged from a retired internal large-PDF reader build
(see docs/case-studies/pdf-large-reader-salvage.md). That build proved them
with memory-bounded tests (streaming held 50 medium pages < 100 MB peak vs
< 200 MB list-loaded) but ran on PyMuPDF (AGPL, license-register flagged);
this port uses only ADOPT-tier permissive tools (pypdf BSD-3, pdfplumber MIT).

Usage:
    uv run preflight.py <file.pdf>          # human-readable report
    uv run preflight.py <file.pdf> --json   # machine-readable, for routing
    uv run preflight.py --check             # self-test on the bundled sample (CI)

Exit codes: 0 = assessed, 1 = unreadable/not a PDF, 2 = assessed with
critical issues (fail-closed signal for shell pipelines).
"""
from __future__ import annotations
import argparse, json, sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

HERE = Path(__file__).parent
SAMPLE = HERE / ".." / "minimal-ingest" / "sample" / "allowable_stress.pdf"

MB = 1024 * 1024
SAMPLE_PAGES = 3          # complexity is sampled, not exhaustive — keep it cheap
FFFD_THRESHOLD = 0.10     # >10% U+FFFD in sampled text = encoding failure


@dataclass
class Issue:
    kind: str       # encryption | corruption | encoding | extraction
    severity: str   # low | medium | high | critical
    message: str


@dataclass
class Preflight:
    file_size: int
    page_count: int
    bytes_per_page: int
    complexity_score: float          # 0-100
    memory_min: int                  # bytes — base + 1 page
    memory_recommended: int          # bytes — base + 5 pages
    memory_peak: int                 # bytes — base + 10 pages, +20% overhead
    strategy: str                    # full_load | stream_pages | chunk_batch
    chunk_size: int                  # pages per unit for the chosen strategy
    issues: list = field(default_factory=list)


def probe_structure(path: Path) -> tuple[PdfReader, list[Issue]]:
    """Cheap structural probe via pypdf: open, count, encryption, first/last page."""
    issues: list[Issue] = []
    reader = PdfReader(path)
    if reader.is_encrypted:
        issues.append(Issue("encryption", "critical",
                            "PDF is encrypted; sampling skipped"))
        return reader, issues
    try:
        n = len(reader.pages)
        if n > 0:
            _ = reader.pages[0]
            if n > 1:
                _ = reader.pages[n - 1]
    except Exception as e:
        issues.append(Issue("corruption", "critical",
                            f"first/last page probe failed: {e}"))
    return reader, issues


def sample_complexity(path: Path, page_count: int) -> tuple[float, float, list[Issue]]:
    """Sample the first few pages with pdfplumber: images, fonts, U+FFFD ratio.

    Returns (avg_images_per_page, avg_fonts_per_page, issues).
    """
    issues: list[Issue] = []
    n = min(SAMPLE_PAGES, page_count)
    if n == 0:
        return 0.0, 0.0, issues
    total_images = total_fonts = 0
    with pdfplumber.open(path) as doc:
        for i in range(n):
            try:
                page = doc.pages[i]
                total_images += len(page.images)
                total_fonts += len({c.get("fontname") for c in page.chars})
                text = page.extract_text() or ""
                if text and text.count("�") / len(text) > FFFD_THRESHOLD:
                    issues.append(Issue(
                        "encoding", "medium",
                        f"page {i + 1}: >{FFFD_THRESHOLD:.0%} U+FFFD replacement "
                        "chars — text layer is mojibake, route to OCR lane"))
            except Exception as e:
                issues.append(Issue("extraction", "high",
                                    f"page {i + 1} unreadable while sampling: {e}"))
    return total_images / n, total_fonts / n, issues


def complexity_score(file_size: int, page_count: int, avg_images: float,
                     avg_fonts: float, encrypted: bool, pdf_version: str) -> float:
    """0-100; higher = heavier pages, more layout machinery, more risk."""
    score = 0.0
    bpp = file_size / page_count if page_count else 0
    score += 30 if bpp > 500 * 1024 else 20 if bpp > 200 * 1024 else 10 if bpp > 100 * 1024 else 0
    score += 20 if page_count > 1000 else 15 if page_count > 500 else 10 if page_count > 100 else 5 if page_count > 50 else 0
    score += 15 if avg_images > 5 else 10 if avg_images > 2 else 5 if avg_images > 0 else 0
    score += 15 if avg_fonts > 10 else 10 if avg_fonts > 5 else 5 if avg_fonts > 2 else 0
    if encrypted:
        score += 10
    if any(v in pdf_version for v in ("1.7", "2.0")):
        score += 10
    elif any(v in pdf_version for v in ("1.5", "1.6")):
        score += 5
    return min(score, 100.0)


def memory_estimate(file_size: int, page_count: int) -> tuple[int, int, int]:
    """(min, recommended, peak) bytes. Per-page cost scales with bytes/page."""
    bpp = file_size / page_count if page_count else 0
    per_page = 10 * MB if bpp > 200 * 1024 else 2 * MB if bpp < 50 * 1024 else 5 * MB
    return (file_size + per_page,
            file_size + per_page * 5,
            int((file_size + per_page * 10) * 1.2))


def select_strategy(file_size: int, page_count: int, score: float,
                    issues: list[Issue]) -> tuple[str, int]:
    """Returns (strategy, chunk_size). Critical issues force the careful lane."""
    if any(i.severity == "critical" for i in issues):
        return "stream_pages", 1
    if file_size < 10 * MB and score < 50:
        return "full_load", page_count or 1
    if file_size >= 100 * MB or score > 70 or page_count > 500:
        return "chunk_batch", 5 if score > 70 else 10
    return "stream_pages", 1


def assess(path: Path) -> Preflight:
    file_size = path.stat().st_size
    reader, issues = probe_structure(path)
    encrypted = reader.is_encrypted
    page_count = 0 if encrypted else len(reader.pages)
    pdf_version = reader.pdf_header or ""

    avg_images = avg_fonts = 0.0
    if not encrypted and not any(i.severity == "critical" for i in issues):
        avg_images, avg_fonts, sample_issues = sample_complexity(path, page_count)
        issues += sample_issues

    score = complexity_score(file_size, page_count, avg_images, avg_fonts,
                             encrypted, pdf_version)
    mem_min, mem_rec, mem_peak = memory_estimate(file_size, page_count)
    strategy, chunk = select_strategy(file_size, page_count, score, issues)
    return Preflight(file_size, page_count,
                     int(file_size / page_count) if page_count else 0,
                     score, mem_min, mem_rec, mem_peak, strategy, chunk,
                     [asdict(i) for i in issues])


def report(p: Preflight) -> str:
    lines = [
        f"size       : {p.file_size / MB:.2f} MB  ({p.page_count} pages, "
        f"{p.bytes_per_page / 1024:.0f} KB/page)",
        f"complexity : {p.complexity_score:.0f}/100",
        f"memory     : min {p.memory_min / MB:.0f} MB | recommended "
        f"{p.memory_recommended / MB:.0f} MB | peak {p.memory_peak / MB:.0f} MB",
        f"STRATEGY   : {p.strategy}  (chunk_size={p.chunk_size})",
    ]
    for i in p.issues:
        lines.append(f"issue      : [{i['severity'].upper()}] {i['kind']}: {i['message']}")
    if not p.issues:
        lines.append("issues     : none detected")
    return "\n".join(lines)


def self_check() -> int:
    """CI: assess the bundled minimal-ingest sample; assert the obvious facts."""
    p = assess(SAMPLE.resolve())
    assert p.page_count == 1, f"sample is 1 page, got {p.page_count}"
    assert p.strategy == "full_load", f"tiny simple PDF must full_load, got {p.strategy}"
    assert not p.issues, f"sample must preflight clean, got {p.issues}"
    assert p.memory_min < p.memory_recommended < p.memory_peak
    print("CHECK    : OK — sample assessed clean, strategy=full_load")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", nargs="?", type=Path, help="PDF file to assess")
    ap.add_argument("--json", action="store_true", help="emit JSON for routing")
    ap.add_argument("--check", action="store_true", help="self-test on bundled sample")
    args = ap.parse_args()

    if args.check:
        return self_check()
    if not args.pdf:
        ap.error("pdf path required (or --check)")
    if not args.pdf.exists():
        print(f"ERROR: no such file: {args.pdf}", file=sys.stderr)
        return 1
    try:
        p = assess(args.pdf)
    except Exception as e:
        print(f"ERROR: cannot assess (not a PDF?): {e}", file=sys.stderr)
        return 1
    print(json.dumps(asdict(p), indent=2) if args.json else report(p))
    return 2 if any(i["severity"] == "critical" for i in p.issues) else 0


if __name__ == "__main__":
    sys.exit(main())
