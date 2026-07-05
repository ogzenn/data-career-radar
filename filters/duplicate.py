"""Duplicate filter - collapses jobs that appear on multiple sources."""


def dedupe_across_sources(jobs):
    """Same job can appear on 2+ boards (e.g. Arbeitnow re-lists Greenhouse jobs).
    Collapse by normalized title+company so we don't post the same role twice
    within a single run. Cross-run duplicates are handled separately by the database."""
    unique = {}
    for job in jobs:
        key = (job["title"].strip().lower(), job["company"].strip().lower())
        if key not in unique:
            unique[key] = job
    return list(unique.values())
