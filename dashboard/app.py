"""
Data Career Radar - Analytics Dashboard (Streamlit)

Deploy this for free on Streamlit Community Cloud (share.streamlit.io):
1. Connect your GitHub repo
2. Set main file path to: dashboard/app.py
3. Deploy

Streamlit Cloud auto-redeploys whenever GitHub Actions commits jobs.db back
to the repo, so the dashboard reflects each new run within a few minutes.

NOTE: This cannot run on GitHub Actions itself - Actions only runs scripts
on a schedule and shuts down, it can't host a live webpage. That's why this
needs Streamlit Community Cloud (or similar) as a separate, free host.
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_recent_jobs, get_stats, get_connection

st.set_page_config(page_title="Data Career Radar", page_icon="📊", layout="wide")

st.title("📊 Data Career Radar")
st.caption("Live tracking of Data Analyst / Data Science friendly job postings")

try:
    stats = get_stats()
    jobs = get_recent_jobs(limit=500)
except Exception as e:
    st.error(f"Could not load database: {e}")
    st.stop()

if not jobs:
    st.info("No jobs collected yet. The bot runs every 30 minutes via GitHub Actions.")
    st.stop()

df = pd.DataFrame(jobs)

# ---------- TOP METRICS ----------

col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs Tracked", stats["total"])
col2.metric("Sources Active", len(stats["by_source"]))
col3.metric("Entry-level/Internship Jobs",
            df[df["experience_level"] == "Entry-level/Internship"].shape[0])

st.divider()

# ---------- CHARTS ----------

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Jobs by Source")
    source_df = pd.DataFrame(stats["by_source"]).set_index("source")
    st.bar_chart(source_df)

with chart_col2:
    st.subheader("Jobs by Experience Level")
    exp_df = pd.DataFrame(stats["by_experience"]).set_index("experience_level")
    st.bar_chart(exp_df)

st.divider()

# ---------- SEARCH / FILTER ----------

st.subheader("🔍 Search Jobs")

search_term = st.text_input("Search by title, company, or skill")
min_score = st.slider("Minimum score", min_value=-10, max_value=15, value=0)

filtered = df.copy()
if search_term:
    mask = (
        filtered["title"].str.contains(search_term, case=False, na=False)
        | filtered["company"].str.contains(search_term, case=False, na=False)
        | filtered["tags"].str.contains(search_term, case=False, na=False)
    )
    filtered = filtered[mask]
filtered = filtered[filtered["score"] >= min_score]

st.write(f"Showing {len(filtered)} of {len(df)} jobs")

st.dataframe(
    filtered[["title", "company", "location", "source", "experience_level", "score", "url"]]
    .sort_values("score", ascending=False),
    column_config={"url": st.column_config.LinkColumn("Apply Link")},
    use_container_width=True,
    hide_index=True,
)
