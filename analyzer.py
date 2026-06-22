"""
analyzer.py
-----------
Core analysis engine for the AI Resume Analyzer.

Responsibilities:
    1. Clean and normalize text (resume + job description).
    2. Compute a match score between resume and job description using
       TF-IDF vectorization + cosine similarity (scikit-learn).
    3. Extract important keywords from the job description and determine
       which of those keywords are present / missing in the resume.
"""

import re
import string
from typing import Dict, List, Set, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A reasonably broad stopword list (kept local to avoid extra NLTK download
# dependencies / network calls at runtime).
STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "could",
    "did", "do", "does", "doing", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here",
    "hers", "herself", "him", "himself", "his", "how", "i", "if", "in",
    "into", "is", "it", "its", "itself", "just", "me", "more", "most",
    "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over",
    "own", "s", "same", "she", "should", "so", "some", "such", "t",
    "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "will",
    "with", "would", "you", "your", "yours", "yourself", "yourselves",
    "etc", "e.g", "eg", "ie", "i.e", "via", "per", "using", "use", "used",
    "including", "include", "includes", "able", "across", "within",
}

# Generic resume / JD filler words that are rarely useful "skills"
GENERIC_NOISE_WORDS: Set[str] = {
    "experience", "work", "working", "knowledge", "ability", "strong",
    "excellent", "good", "skills", "skill", "years", "year", "team",
    "teams", "role", "job", "responsibilities", "responsibility",
    "requirements", "required", "preferred", "candidate", "candidates",
    "company", "position", "looking", "join", "environment", "plus",
    "based", "related", "field", "degree", "bachelor", "master",
    "minimum", "must", "ideal", "ideally", "etc", "new", "various",
}


def clean_text(text: str) -> str:
    """
    Normalize text by lowercasing, removing punctuation/numbers noise,
    and collapsing extra whitespace.

    Args:
        text: Raw input text.

    Returns:
        str: Cleaned text suitable for vectorization or tokenization.
    """
    text = text.lower()
    text = re.sub(r"[\r\n\t]+", " ", text)
    # Keep alphanumerics, '+', '#', '.', '-' (useful for skills like
    # "C++", "C#", "Node.js", "CI/CD")
    text = re.sub(r"[^a-z0-9\+\#\.\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    """
    Split cleaned text into meaningful tokens, removing stopwords,
    very short tokens, and generic noise words.

    Args:
        text: Cleaned text (output of clean_text).

    Returns:
        List[str]: List of meaningful tokens.
    """
    raw_tokens = text.split()
    tokens = []
    for tok in raw_tokens:
        tok = tok.strip(string.punctuation)
        if not tok:
            continue
        if len(tok) <= 2 and tok not in {"c#", "go", "r", "ai"}:
            continue
        if tok in STOPWORDS or tok in GENERIC_NOISE_WORDS:
            continue
        tokens.append(tok)
    return tokens


def extract_keywords(text: str, top_n: int = 30) -> List[Tuple[str, int]]:
    """
    Extract the most frequent meaningful keywords from a block of text.

    Args:
        text: Raw text (e.g. job description).
        top_n: Maximum number of keywords to return.

    Returns:
        List[Tuple[str, int]]: List of (keyword, frequency) sorted by
                                frequency descending.
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)

    freq: Dict[str, int] = {}
    for tok in tokens:
        freq[tok] = freq.get(tok, 0) + 1

    # Also capture simple two-word phrases (bigrams) which often represent
    # real skills, e.g. "machine learning", "project management".
    bigram_freq: Dict[str, int] = {}
    for i in range(len(tokens) - 1):
        bigram = f"{tokens[i]} {tokens[i + 1]}"
        bigram_freq[bigram] = bigram_freq.get(bigram, 0) + 1

    combined = {**freq}
    for bigram, count in bigram_freq.items():
        if count >= 2:  # only keep bigrams that repeat (likely real terms)
            combined[bigram] = count

    sorted_keywords = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n]


def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Calculate the similarity between a resume and a job description using
    TF-IDF vectorization and cosine similarity.

    Args:
        resume_text: Extracted resume text.
        job_description: Job description text pasted by the user.

    Returns:
        float: Match percentage between 0.0 and 100.0.

    Raises:
        ValueError: If either input text is empty after cleaning.
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    if not cleaned_resume or not cleaned_jd:
        raise ValueError(
            "Both resume text and job description must contain readable "
            "content to calculate a match score."
        )

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])

    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    similarity_score = float(similarity_matrix[0][0])

    # Convert to a 0-100 percentage scale
    match_percentage = round(similarity_score * 100, 2)
    return match_percentage


def find_matching_and_missing_keywords(
    resume_text: str, job_description: str, top_n: int = 25
) -> Dict[str, List[str]]:
    """
    Identify keywords from the job description that are present vs.
    missing in the resume.

    Args:
        resume_text: Extracted resume text.
        job_description: Job description text.
        top_n: Number of top JD keywords to consider.

    Returns:
        Dict with two keys:
            "matching": keywords found in both JD and resume.
            "missing":  keywords found in JD but NOT in resume.
    """
    jd_keywords = [kw for kw, _ in extract_keywords(job_description, top_n=top_n)]

    cleaned_resume = clean_text(resume_text)
    resume_tokens_set = set(tokenize(cleaned_resume))
    # Also build a set of resume bigrams for phrase matching
    resume_token_list = tokenize(cleaned_resume)
    resume_bigrams_set = {
        f"{resume_token_list[i]} {resume_token_list[i + 1]}"
        for i in range(len(resume_token_list) - 1)
    }
    resume_full_set = resume_tokens_set | resume_bigrams_set

    matching = []
    missing = []

    for keyword in jd_keywords:
        if keyword in resume_full_set or keyword in cleaned_resume:
            matching.append(keyword)
        else:
            missing.append(keyword)

    return {"matching": matching, "missing": missing}


def get_score_label(score: float) -> str:
    """
    Convert a numeric match score into a human-readable label/category.

    Args:
        score: Match percentage (0-100).

    Returns:
        str: A label such as "Excellent Match", "Good Match", etc.
    """
    if score >= 75:
        return "Excellent Match"
    elif score >= 55:
        return "Good Match"
    elif score >= 35:
        return "Fair Match"
    else:
        return "Weak Match"
