"""
app.py
------
Main Streamlit application entry point for the AI Resume Analyzer.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd

from utils.pdf_parser import extract_resume_text, ResumeParsingError
from utils.analyzer import (
    calculate_match_score,
    find_matching_and_missing_keywords,
    get_score_label,
)
from utils.recommendations import (
    generate_recommendations,
    export_recommendations_as_text,
)
from utils.report_generator import generate_pdf_report


# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------------------------------
# Minimal custom styling for a clean, professional look
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #6b7280;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }
    .stMetric {
        background-color: #f8f9fb;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📄 AI Resume Analyzer")
    st.write(
        "Upload your resume and paste a job description to see how well "
        "they match, identify missing skills, and get ATS-friendly "
        "recommendations."
    )
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown(
        """
        1. Upload a **PDF or DOCX** resume
        2. Paste the **job description**
        3. Click **Analyze**
        4. Review your **match score**, **keyword gaps**, and
           **recommendations**
        """
    )
    st.markdown("---")
    st.caption("Built with Python, Streamlit & scikit-learn")


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Compare your resume against any job description '
    'and get an instant ATS match score with actionable feedback.</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Input section
# --------------------------------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-header">1. Upload Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX resume",
        type=["pdf", "docx"],
        help="Your resume should contain selectable text (not a scanned image).",
    )

with col2:
    st.markdown('<div class="section-header">2. Paste Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste the full job description here",
        height=220,
        placeholder="e.g. We are looking for a Data Scientist with experience in Python, "
        "machine learning, SQL, and cloud platforms such as AWS...",
    )

analyze_clicked = st.button("🔍 Analyze Resume", type="primary", use_container_width=False)


# --------------------------------------------------------------------------
# Analysis & Results
# --------------------------------------------------------------------------
if analyze_clicked:
    # --- Validation ---------------------------------------------------
    if uploaded_file is None:
        st.error("⚠️ Please upload a resume file (PDF or DOCX) before analyzing.")
        st.stop()

    if not job_description or not job_description.strip():
        st.error("⚠️ Please paste a job description before analyzing.")
        st.stop()

    # --- Resume text extraction -----------------------------------------
    try:
        with st.spinner("Extracting text from resume..."):
            resume_text = extract_resume_text(uploaded_file)
    except ResumeParsingError as e:
        st.error(f"❌ Could not process resume: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ An unexpected error occurred while reading the file: {e}")
        st.stop()

    # --- Match score calculation -----------------------------------------
    try:
        with st.spinner("Calculating match score..."):
            match_score = calculate_match_score(resume_text, job_description)
            keyword_results = find_matching_and_missing_keywords(resume_text, job_description)
            matching_keywords = keyword_results["matching"]
            missing_keywords = keyword_results["missing"]
            score_label = get_score_label(match_score)
            recommendations = generate_recommendations(match_score, missing_keywords, resume_text)
    except ValueError as e:
        st.error(f"❌ {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ An unexpected error occurred during analysis: {e}")
        st.stop()

    st.success("✅ Analysis complete!")
    st.markdown("---")

    # ----------------------------------------------------------------
    # Dashboard: Metrics row
    # ----------------------------------------------------------------
    st.markdown('<div class="section-header">📊 Results Dashboard</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Match Score", f"{match_score}%", score_label)
    m2.metric("Matching Keywords", len(matching_keywords))
    m3.metric("Missing Keywords", len(missing_keywords))
    total_kw = len(matching_keywords) + len(missing_keywords)
    coverage = round((len(matching_keywords) / total_kw) * 100, 1) if total_kw else 0
    m4.metric("Keyword Coverage", f"{coverage}%")

    # ----------------------------------------------------------------
    # Chart: Match score gauge-style bar chart
    # ----------------------------------------------------------------
    st.markdown("#### Match Score Breakdown")
    chart_data = pd.DataFrame(
        {
            "Category": ["Match", "Gap"],
            "Percentage": [match_score, round(100 - match_score, 2)],
        }
    )
    st.bar_chart(chart_data.set_index("Category"))

    # ----------------------------------------------------------------
    # Tables: Matching vs Missing keywords
    # ----------------------------------------------------------------
    t1, t2 = st.columns(2, gap="large")

    with t1:
        st.markdown("#### ✅ Matching Skills")
        if matching_keywords:
            st.dataframe(
                pd.DataFrame({"Keyword": matching_keywords}),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No matching keywords found.")

    with t2:
        st.markdown("#### ❌ Missing Skills")
        if missing_keywords:
            st.dataframe(
                pd.DataFrame({"Keyword": missing_keywords}),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No missing keywords — great coverage!")

    # ----------------------------------------------------------------
    # Recommendations
    # ----------------------------------------------------------------
    st.markdown("#### 💡 Recommendations to Improve ATS Score")
    for i, rec in enumerate(recommendations, start=1):
        st.markdown(f"**{i}.** {rec}")

    st.markdown("---")

    # ----------------------------------------------------------------
    # Downloads: PDF report + text export
    # ----------------------------------------------------------------
    st.markdown('<div class="section-header">⬇️ Export Your Results</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)

    with d1:
        try:
            pdf_bytes = generate_pdf_report(
                match_score, score_label, matching_keywords, missing_keywords, recommendations
            )
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.warning(f"Could not generate PDF report: {e}")

    with d2:
        text_report = export_recommendations_as_text(
            match_score, matching_keywords, missing_keywords, recommendations
        )
        st.download_button(
            label="📝 Download Text Report",
            data=text_report,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # ----------------------------------------------------------------
    # Raw extracted text (optional, expandable)
    # ----------------------------------------------------------------
    with st.expander("🔎 View Extracted Resume Text"):
        st.text(resume_text)

else:
    st.info("👆 Upload a resume and paste a job description, then click **Analyze Resume** to get started.")
