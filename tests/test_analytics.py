from src.analytics import (
    calculate_funnel_metrics,
    calculate_hiring_rate,
)
from src.data_loader import load_dataset


def test_hiring_rate_range() -> None:
    """
    Hiring rate should remain valid percentage.
    """

    dataframe = load_dataset("data/raw/candidates.csv")

    hiring_rate = calculate_hiring_rate(dataframe)

    assert 0 <= hiring_rate <= 100


def test_funnel_metrics_exist() -> None:
    """
    Ensure all funnel stages exist.
    """

    dataframe = load_dataset("data/raw/candidates.csv")

    metrics = calculate_funnel_metrics(dataframe)

    expected_stages = [
        "Applied",
        "Assessment Cleared",
        "Technical Interview",
        "HR Interview",
        "Hired",
    ]

    for stage in expected_stages:
        assert stage in metrics
