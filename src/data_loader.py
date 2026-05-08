from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "candidate_id",
    "source",
    "role",
    "assessment_score",
    "communication_score",
    "resume_score",
    "interview_score",
    "experience_years",
    "final_score",
    "application_stage",
    "selected",
    "days_in_pipeline",
    "dropout_reason",
]


class DatasetValidationError(Exception):
    """
    Raised when dataset validation fails.
    """


def validate_columns(dataframe: pd.DataFrame) -> None:
    """
    Ensure required columns exist.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in dataframe.columns
    ]

    if missing_columns:
        raise DatasetValidationError(f"Missing required columns: {missing_columns}")


def validate_missing_values(dataframe: pd.DataFrame) -> None:
    """
    Ensure critical columns do not contain null values.
    """

    critical_columns = [
        "candidate_id",
        "source",
        "role",
        "assessment_score",
        "application_stage",
    ]

    null_counts = dataframe[critical_columns].isnull().sum()

    problematic_columns = {
        column: count for column, count in null_counts.items() if count > 0
    }

    if problematic_columns:
        raise DatasetValidationError(f"Missing values detected: {problematic_columns}")


def load_dataset(csv_path: str | Path) -> pd.DataFrame:
    """
    Load and validate recruitment dataset.
    """

    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    dataframe = pd.read_csv(path)

    validate_columns(dataframe)
    validate_missing_values(dataframe)

    return dataframe
