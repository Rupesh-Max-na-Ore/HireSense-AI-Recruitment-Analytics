from __future__ import annotations

import streamlit as st

from src.analytics import (
    calculate_funnel_metrics,
    calculate_hiring_rate,
    role_hiring_analysis,
    source_performance,
    top_candidates,
)

from src.data_loader import load_dataset

from src.visualizations import (
    create_correlation_heatmap,
    create_funnel_chart,
    create_role_hiring_chart,
    create_source_performance_chart,
)

st.set_page_config(
    page_title="HireSense AI",
    layout="wide",
)

st.title("HireSense AI")
st.subheader("Recruitment Funnel Analytics Dashboard")

# =========================
# Load Dataset
# =========================


@st.cache_data
def get_dataset():
    """
    Load recruitment dataset with caching.
    """

    return load_dataset("data/raw/candidates.csv")


dataframe = get_dataset()

# =========================
# Sidebar Filters
# =========================

st.sidebar.header("Dashboard Filters")

selected_role = st.sidebar.selectbox(
    "Select Role",
    ["All"] + sorted(dataframe["role"].unique().tolist()),
)

if selected_role != "All":
    dataframe = dataframe[dataframe["role"] == selected_role]

# =========================
# KPI Calculations
# =========================

funnel_metrics = calculate_funnel_metrics(dataframe)

hiring_rate = calculate_hiring_rate(dataframe)

source_data = source_performance(dataframe)

role_data = role_hiring_analysis(dataframe)

top_candidates_df = top_candidates(dataframe)

# =========================
# KPI Cards
# =========================

total_candidates = len(dataframe)

total_hires = dataframe["selected"].sum()

average_score = round(
    dataframe["final_score"].mean(),
    2,
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Candidates",
    total_candidates,
)

col2.metric(
    "Total Hires",
    int(total_hires),
)

col3.metric(
    "Hiring Rate",
    f"{hiring_rate}%",
)

col4.metric(
    "Average Final Score",
    average_score,
)

st.divider()

# =========================
# Funnel Visualization
# =========================

st.header("Hiring Funnel Analysis")

funnel_chart = create_funnel_chart(funnel_metrics)

st.plotly_chart(
    funnel_chart,
    use_container_width=True,
)

# =========================
# Source Analysis
# =========================

st.header("Candidate Source Performance")

source_chart = create_source_performance_chart(source_data)

st.plotly_chart(
    source_chart,
    use_container_width=True,
)

st.dataframe(
    source_data,
    use_container_width=True,
)

# =========================
# Role Analysis
# =========================

st.header("Role-wise Hiring Metrics")

role_chart = create_role_hiring_chart(role_data)

st.plotly_chart(
    role_chart,
    use_container_width=True,
)

st.dataframe(
    role_data,
    use_container_width=True,
)

# =========================
# Correlation Analysis
# =========================

st.header("Candidate Correlation Analysis")

heatmap = create_correlation_heatmap(dataframe)

st.plotly_chart(
    heatmap,
    use_container_width=True,
)

# =========================
# Top Candidates
# =========================

st.header("Top Ranked Candidates")

st.dataframe(
    top_candidates_df,
    use_container_width=True,
)

# =========================
# Business Insights
# =========================

st.header("Key Business Insights")

top_source = source_data.iloc[0]["source"]

top_source_score = source_data.iloc[0]["avg_final_score"]

st.markdown(f"""
- **{top_source}** produces the strongest candidate quality
  with an average final score of **{top_source_score}**.

- Technical interview stages show the largest candidate filtering effect.

- Referral and Hackathon candidates outperform traditional sourcing channels.

- Hiring conversion remains highly selective,
  indicating a competitive recruitment pipeline.

- Strong positive correlations exist between
  assessment scores, interview scores, and final outcomes.
""")
