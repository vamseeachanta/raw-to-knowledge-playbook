#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["reportlab>=4.0"]
# ///
"""Generate the example's sample PDF: a single ruled engineering table.

The content is ENTIRELY SYNTHETIC and released CC0 — it is NOT copied from any
real standard, so the repo never carries copyrighted source material (doc 07
raw-source firewall). Run once; the produced PDF is committed so the rest of the
example needs only pdfplumber.

    uv run make_sample.py
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

OUT = "sample/allowable_stress.pdf"

# Synthetic data (CC0). Grades resemble line-pipe naming but values are invented.
HEADER = ["Grade", "Yield (MPa)", "Tensile (MPa)", "Allow. Stress (MPa)", "Temp Limit (C)"]
ROWS = [
    ["X52", "359", "455", "215", "120"],
    ["X60", "414", "517", "248", "120"],
    ["X65", "448", "531", "269", "150"],
    ["X70", "483", "565", "290", "150"],
]


def main() -> None:
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                            topMargin=1 * inch, bottomMargin=1 * inch)
    story = [
        Paragraph("Example Spec EX-001 (synthetic, CC0)", styles["Title"]),
        Paragraph("Table 3 — Allowable Stress by Material Grade", styles["Heading2"]),
        Spacer(1, 0.2 * inch),
        Table([HEADER] + ROWS, hAlign="LEFT",
              style=TableStyle([
                  ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                  ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                  ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                  ("FONTSIZE", (0, 0), (-1, -1), 10),
                  ("LEFTPADDING", (0, 0), (-1, -1), 8),
                  ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                  ("TOPPADDING", (0, 0), (-1, -1), 5),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
              ])),
    ]
    doc.build(story)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
