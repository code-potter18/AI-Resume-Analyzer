"""
recommendations.py
-------------------
Generates human-readable recommendations to help a candidate improve
their resume for ATS (Applicant Tracking System) screening, based on
the match score and missing keywords identified by analyzer.py.
"""

from typing import List


def generate_recommendations(
    match_score: float, missing_keywords: List[str], resume_text: str
) -> List[str]:
    """
    Build a list of actionable recommendations for the candidate.

    Args:
        match_score: The resume/JD match percentage (0-100).
        missing_keywords: Keywords present in the JD but absent from the
                           resume.
        resume_text: The raw extracted resume text (used for basic
                      structural checks, e.g. length, sections).

    Returns:
        List[str]: A list of recommendation strings.
    """
    recommendations: List[str] = []

    # --- Score-based recommendations -----------------------------------
    if match_score < 35:
        recommendations.append(
            "Your resume has a low overall match with this job description. "
            "Consider tailoring your resume specifically for this role by "
            "mirroring the language used in the job posting."
        )
    elif match_score < 55:
        recommendations.append(
            "Your resume has a fair match. Adding more role-specific "
            "terminology and quantifiable achievements could improve "
            "your ATS ranking."
        )
    elif match_score < 75:
        recommendations.append(
            "Good match! A few targeted tweaks to incorporate missing "
            "keywords could push your resume into the 'Excellent Match' range."
        )
    else:
        recommendations.append(
            "Excellent match! Your resume aligns very well with this job "
            "description. Focus on polishing formatting and proofreading."
        )

    # --- Missing keyword recommendations --------------------------------
    if missing_keywords:
        top_missing = ", ".join(missing_keywords[:10])
        recommendations.append(
            f"Consider adding these relevant keywords/skills if you "
            f"genuinely possess them: {top_missing}."
        )
        recommendations.append(
            "Incorporate missing keywords naturally within your "
            "experience bullet points rather than just listing them, "
            "as ATS systems and recruiters value contextual usage."
        )
    else:
        recommendations.append(
            "Great news — your resume already contains most of the key "
            "terms from the job description."
        )

    # --- Structural / formatting recommendations -------------------------
    word_count = len(resume_text.split())
    if word_count < 150:
        recommendations.append(
            "Your resume content seems quite short. Consider expanding "
            "on your work experience, projects, and measurable achievements."
        )
    elif word_count > 1200:
        recommendations.append(
            "Your resume is quite lengthy. Consider trimming it to 1-2 "
            "pages, focusing on the most relevant and recent experience."
        )

    lower_text = resume_text.lower()
    if "summary" not in lower_text and "objective" not in lower_text:
        recommendations.append(
            "Add a brief professional summary at the top of your resume "
            "to immediately highlight your fit for the role."
        )

    if not any(char.isdigit() for char in resume_text):
        recommendations.append(
            "Include quantifiable metrics (e.g., '%', numbers, dollar "
            "amounts) to demonstrate measurable impact in your roles."
        )

    if "education" not in lower_text:
        recommendations.append(
            "Consider explicitly including an 'Education' section, as "
            "many ATS systems look for standard section headers."
        )

    recommendations.append(
        "Use standard section headings (Experience, Education, Skills) "
        "and avoid tables/columns/graphics, since complex layouts can "
        "confuse ATS parsers."
    )

    return recommendations


def export_recommendations_as_text(
    match_score: float,
    matching_keywords: List[str],
    missing_keywords: List[str],
    recommendations: List[str],
) -> str:
    """
    Build a plain-text export of the full analysis for download.

    Args:
        match_score: The resume/JD match percentage.
        matching_keywords: Keywords found in both resume and JD.
        missing_keywords: Keywords found in JD but missing from resume.
        recommendations: List of recommendation strings.

    Returns:
        str: A formatted text report ready to be written to a .txt file.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("AI RESUME ANALYZER - ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append(f"\nOverall Match Score: {match_score}%\n")

    lines.append("-" * 60)
    lines.append("MATCHING SKILLS / KEYWORDS")
    lines.append("-" * 60)
    if matching_keywords:
        for kw in matching_keywords:
            lines.append(f"  ✓ {kw}")
    else:
        lines.append("  None found.")

    lines.append("\n" + "-" * 60)
    lines.append("MISSING SKILLS / KEYWORDS")
    lines.append("-" * 60)
    if missing_keywords:
        for kw in missing_keywords:
            lines.append(f"  ✗ {kw}")
    else:
        lines.append("  None — great coverage!")

    lines.append("\n" + "-" * 60)
    lines.append("RECOMMENDATIONS")
    lines.append("-" * 60)
    for i, rec in enumerate(recommendations, start=1):
        lines.append(f"  {i}. {rec}")

    lines.append("\n" + "=" * 60)
    lines.append("Generated by AI Resume Analyzer")
    lines.append("=" * 60)

    return "\n".join(lines)
