<img width="1917" height="872" alt="mkm" src="https://github.com/user-attachments/assets/7df9c9e0-eef5-4fb6-9e3d-6050d2a1dd7f" />
# 📄 AI Resume Analyzer

An AI-powered web application that compares a resume against a job description, calculates an ATS-style match score, identifies missing skills/keywords, and provides actionable recommendations to improve ATS screening results — all through a clean, interactive Streamlit dashboard.

---

## 🚀 Overview

Job seekers often don't know how well their resume aligns with a specific job posting, or which keywords an Applicant Tracking System (ATS) might be scanning for. **AI Resume Analyzer** solves this by:

- Extracting text from an uploaded resume (PDF or DOCX)
- Comparing it against a pasted job description using **TF-IDF + cosine similarity**
- Surfacing exactly which important keywords are present vs. missing
- Generating tailored, ATS-friendly recommendations
- Visualizing everything in an easy-to-read dashboard
- Allowing the full analysis to be exported as a PDF or text report

---

## ✨ Features

- 📤 **Resume Upload** — Supports PDF (via PyPDF2) and DOCX (via python-docx)
- 📋 **Job Description Input** — Simple paste-and-go text area
- 🎯 **Match Score** — TF-IDF vectorization + cosine similarity (scikit-learn)
- 🔑 **Keyword Analysis** — Matching vs. missing skills displayed in clean tables
- 💡 **ATS Recommendations** — Actionable, specific tips to improve resume alignment
- 📊 **Visual Dashboard** — Metrics cards + bar chart visualization of match score
- 📄 **PDF Report Export** — Download a professional analysis report (bonus feature, via fpdf2)
- 📝 **Text Export** — Download recommendations and keyword analysis as a `.txt` file (bonus feature)
- ⚠️ **Robust Error Handling** — Friendly messages for empty, corrupted, encrypted, or unsupported files
- 🧱 **Modular Codebase** — Cleanly separated into `pdf_parser.py`, `analyzer.py`, `recommendations.py`, and `report_generator.py`

---

## 🛠️ Technologies Used

| Category            | Technology              |
|----------------------|--------------------------|
| Language             | Python 3.9+             |
| Web Framework        | Streamlit                |
| PDF Parsing          | PyPDF2                   |
| DOCX Parsing         | python-docx              |
| NLP / Similarity     | scikit-learn (TF-IDF, cosine similarity) |
| Data Handling        | pandas, numpy            |
| PDF Report Generation| fpdf2                    |

---

## 📁 Project Structure

```
AI-Resume-Analyzer/
├── app.py                      # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py           # PDF/DOCX text extraction
│   ├── analyzer.py             # TF-IDF match scoring & keyword extraction
│   ├── recommendations.py      # ATS recommendation engine
│   └── report_generator.py     # PDF report generation (bonus feature)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── sample_data/                # Sample resume & job description for testing
│   ├── sample_resume.pdf
│   └── sample_job_description.txt
└── screenshots/                # App screenshots for documentation
```

---

## ⚙️ Installation

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Streamlit app locally:

```bash
streamlit run app.py
```

Then open the URL shown in your terminal (typically `http://localhost:8501`) in your browser.

### Steps inside the app:

1. **Upload your resume** (PDF or DOCX) using the file uploader.
2. **Paste the job description** into the text area.
3. Click **🔍 Analyze Resume**.
4. Review your:
   - Match score and category (Excellent / Good / Fair / Weak Match)
   - Matching and missing skill keyword tables
   - ATS improvement recommendations
   - Match score bar chart
5. Optionally, **download a PDF or text report** of your full analysis.

> 💡 Tip: Try it out instantly using the sample files in `sample_data/` (`sample_resume.pdf` and `sample_job_description.txt`).

---

## 📸 Screenshots

> Add your own screenshots to the `screenshots/` folder and reference them below.

| Dashboard Overview | Keyword Comparison |
|---|---|
| ![Dashboard](screenshots/dashboard_overview.png) | ![Keywords](screenshots/keyword_comparison.png) |

| Recommendations | PDF Report Export |
|---|---|
| ![Recommendations](screenshots/recommendations.png) | ![PDF Report](screenshots/pdf_report.png) |

---

## 🔮 Future Enhancements

- [ ] Support for batch analysis of multiple resumes against one job description
- [ ] Integration with spaCy / transformer-based NER for smarter skill extraction
- [ ] Resume formatting/ATS-parsability checker (fonts, tables, columns detection)
- [ ] Job description URL scraping (paste a job posting link instead of raw text)
- [ ] User accounts to save and track analysis history over time
- [ ] Multi-language resume support
- [ ] Side-by-side resume version comparison

---

## 🧩 How the Matching Works

1. **Text Cleaning** — Both resume and job description are lowercased, stripped of irrelevant punctuation, and normalized.
2. **TF-IDF Vectorization** — Each document is converted into a weighted vector representing term importance using `TfidfVectorizer` from scikit-learn.
3. **Cosine Similarity** — The cosine similarity between the resume vector and job description vector produces a score between 0 and 1, scaled to a 0–100% match score.
4. **Keyword Extraction** — The most frequent meaningful terms (single words and recurring two-word phrases) are extracted from the job description and checked against the resume's vocabulary to determine matches and gaps.

---

## ⚠️ Error Handling

The app gracefully handles:
- Empty or corrupted PDF/DOCX files
- Password-protected PDFs
- Scanned PDFs with no extractable text (image-only)
- Unsupported file formats
- Empty job description input
- Unexpected runtime errors during analysis

---

## 📜 License

This project is provided as-is for educational and personal use. Feel free to fork, modify, and build upon it.

---

## 🙌 Acknowledgements

Built with [Streamlit](https://streamlit.io/), [scikit-learn](https://scikit-learn.org/), [PyPDF2](https://pypi.org/project/PyPDF2/), and [fpdf2](https://pypi.org/project/fpdf2/).
