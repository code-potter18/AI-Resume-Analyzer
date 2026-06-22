"""
report_generator.py
--------------------
Generates a downloadable PDF analysis report summarizing the resume's
match score, matching/missing keywords, and recommendations.

Uses fpdf2, a lightweight pure-Python PDF generation library.
"""

from datetime import datetime
from typing import List

from fpdf import FPDF


class ReportPDF(FPDF):
    """Custom PDF class with a simple branded header/footer."""

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "AI Resume Analyzer - Analysis Report", ln=True, align="C")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, datetime.now().strftime("Generated on %B %d, %Y at %H:%M"), ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def _sanitize(text: str) -> str:
    """Replace characters unsupported by FPDF's default font encoding."""
    return (
        text.encode("latin-1", "replace").decode("latin-1")
        if text else ""
    )


def generate_pdf_report(
    match_score: float,
    score_label: str,
    matching_keywords: List[str],
    missing_keywords: List[str],
    recommendations: List[str],
) -> bytes:
    """
    Build a PDF report and return it as raw bytes, suitable for use
    with Streamlit's st.download_button.

    Args:
        match_score: Resume/JD match percentage.
        score_label: Human-readable label (e.g. "Good Match").
        matching_keywords: Keywords found in both resume and JD.
        missing_keywords: Keywords missing from the resume.
        recommendations: List of recommendation strings.

    Returns:
        bytes: The generated PDF file content.
    """
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- Score section ---------------------------------------------------
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, f"Overall Match Score: {match_score}% ({score_label})", ln=True)
    pdf.ln(2)

    # --- Matching keywords -------------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 120, 20)
    pdf.cell(0, 8, "Matching Skills / Keywords", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    if matching_keywords:
        pdf.multi_cell(0, 6, _sanitize(", ".join(matching_keywords)))
    else:
        pdf.cell(0, 6, "None found.", ln=True)
    pdf.ln(3)

    # --- Missing keywords ----------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(180, 40, 40)
    pdf.cell(0, 8, "Missing Skills / Keywords", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    if missing_keywords:
        pdf.multi_cell(0, 6, _sanitize(", ".join(missing_keywords)))
    else:
        pdf.cell(0, 6, "None - great coverage!", ln=True)
    pdf.ln(3)

    # --- Recommendations --------------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 20, 120)
    pdf.cell(0, 8, "Recommendations", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    for i, rec in enumerate(recommendations, start=1):
        pdf.multi_cell(0, 6, _sanitize(f"{i}. {rec}"))
        pdf.ln(1)

    # fpdf2 returns a bytearray; Streamlit's download_button needs bytes
    return bytes(pdf.output(dest="S"))
