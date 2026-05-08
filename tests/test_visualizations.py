from src.analytics import (
    calculate_funnel_metrics,
    source_performance,
)

from src.data_loader import load_dataset

from src.visualizations import (
    create_funnel_chart,
    create_source_performance_chart,
)


def test_funnel_chart_creation() -> None:
    """
    Funnel chart should generate successfully.
    """

    dataframe = load_dataset("data/raw/candidates.csv")

    metrics = calculate_funnel_metrics(dataframe)

    figure = create_funnel_chart(metrics)

    assert figure is not None


def test_source_chart_creation() -> None:
    """
    Source performance chart should generate.
    """

    dataframe = load_dataset("data/raw/candidates.csv")

    source_data = source_performance(dataframe)

    figure = create_source_performance_chart(source_data)

    assert figure is not None
