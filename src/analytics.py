from __future__ import annotations

import pandas as pd


def calculate_funnel_metrics(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Calculate cumulative recruitment funnel metrics.
    """

    funnel_order = [
        "Applied",
        "Assessment Cleared",
        "Technical Interview",
        "HR Interview",
        "Hired",
    ]

    stage_rank = {stage: index for index, stage in enumerate(funnel_order)}

    metrics = {}

    for stage in funnel_order:
        current_rank = stage_rank[stage]

        count = dataframe[
            dataframe["application_stage"].map(stage_rank) >= current_rank
        ].shape[0]

        metrics[stage] = count

    return metrics


def calculate_hiring_rate(dataframe: pd.DataFrame) -> float:
    """
    Calculate overall hiring percentage.
    """

    total_candidates = len(dataframe)

    hired_candidates = dataframe["selected"].sum()

    hiring_rate = (hired_candidates / total_candidates) * 100

    return round(hiring_rate, 2)


def source_performance(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze candidate source effectiveness.
    """

    grouped = (
        dataframe.groupby("source")
        .agg(
            avg_final_score=("final_score", "mean"),
            hires=("selected", "sum"),
            avg_assessment=("assessment_score", "mean"),
        )
        .reset_index()
    )

    grouped["avg_final_score"] = grouped["avg_final_score"].round(2)

    grouped["avg_assessment"] = grouped["avg_assessment"].round(2)

    return grouped.sort_values(
        by="avg_final_score",
        ascending=False,
    )


def role_hiring_analysis(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze hiring metrics across roles.
    """

    grouped = (
        dataframe.groupby("role")
        .agg(
            total_candidates=("candidate_id", "count"),
            hires=("selected", "sum"),
            avg_pipeline_days=("days_in_pipeline", "mean"),
        )
        .reset_index()
    )

    grouped["hiring_rate"] = (grouped["hires"] / grouped["total_candidates"]) * 100

    grouped["avg_pipeline_days"] = grouped["avg_pipeline_days"].round(2)

    grouped["hiring_rate"] = grouped["hiring_rate"].round(2)

    return grouped


def top_candidates(
    dataframe: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Return highest-performing candidates.
    """

    columns = [
        "candidate_id",
        "role",
        "source",
        "final_score",
        "assessment_score",
        "interview_score",
        "selected",
    ]

    return (
        dataframe[columns]
        .sort_values(
            by="final_score",
            ascending=False,
        )
        .head(top_n)
    )
