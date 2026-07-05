"""
Scoring filter - assigns a numeric score to each job based on weighted keywords.
This is rule-based scoring, NOT machine learning or AI - just weighted keyword
matching, kept simple and transparent so it's easy to explain and tune.
"""

from config import POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS, MIN_SCORE_TO_POST


def score_job(job):
    """Returns an integer score. Higher = more relevant to fresher DA/DS roles."""
    haystack = f"{job['title']} {job['tags']} {job['description']}".lower()

    score = 0
    for keyword, weight in POSITIVE_KEYWORDS.items():
        if keyword in haystack:
            score += weight
    for keyword, weight in NEGATIVE_KEYWORDS.items():
        if keyword in haystack:
            score += weight  # weight is already negative

    return score


def passes_score_threshold(job):
    return job.get("score", score_job(job)) >= MIN_SCORE_TO_POST


def classify_experience_level(job):
    """Rough label for display purposes, based on the same keyword signals."""
    score = job.get("score", score_job(job))
    haystack = f"{job['title']} {job['description']}".lower()

    if any(k in haystack for k in ["senior", "principal", "staff ", "lead ", "manager", "director"]):
        return "Senior/Lead"
    if any(k in haystack for k in ["internship", "intern ", "graduate", "entry level", "junior", "fresher"]):
        return "Entry-level/Internship"
    if score >= MIN_SCORE_TO_POST:
        return "Likely fresher-friendly"
    return "Unclear"
