from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_funnel_chart(
    funnel_metrics: dict,
) -> go.Figure:
    """
    Create recruitment funnel visualization.
    """

    stages = list(funnel_metrics.keys())

    counts = list(funnel_metrics.values())

    figure = go.Figure(
        go.Funnel(
            y=stages,
            x=counts,
            textinfo="value+percent initial",
        )
    )

    figure.update_layout(
        title="Recruitment Funnel Analysis",
        height=500,
    )

    return figure


def create_source_performance_chart(
    source_dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Visualize hiring source performance.
    """

    figure = px.bar(
        source_dataframe,
        x="source",
        y="avg_final_score",
        color="hires",
        title="Candidate Source Performance",
        text_auto=".2f",
    )

    figure.update_layout(
        xaxis_title="Candidate Source",
        yaxis_title="Average Final Score",
    )

    return figure


def create_role_hiring_chart(
    role_dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Visualize hiring rate across roles.
    """

    figure = px.bar(
        role_dataframe,
        x="role",
        y="hiring_rate",
        color="avg_pipeline_days",
        title="Role-wise Hiring Analysis",
        text_auto=".2f",
    )

    figure.update_layout(
        xaxis_title="Role",
        yaxis_title="Hiring Rate (%)",
    )

    return figure


def create_correlation_heatmap(
    dataframe: pd.DataFrame,
) -> go.Figure:
    """
    Visualize numerical feature correlations.
    """

    numerical_columns = [
        "assessment_score",
        "communication_score",
        "resume_score",
        "interview_score",
        "experience_years",
        "final_score",
        "days_in_pipeline",
    ]

    correlation_matrix = dataframe[numerical_columns].corr()

    figure = px.imshow(
        correlation_matrix,
        text_auto=True,
        aspect="auto",
        title="Candidate Metrics Correlation Heatmap",
    )

    return figure
