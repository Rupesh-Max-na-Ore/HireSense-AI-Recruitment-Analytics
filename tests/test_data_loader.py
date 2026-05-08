from pathlib import Path

from src.data_loader import load_dataset


def test_dataset_loads_successfully() -> None:
    """
    Ensure dataset loads correctly.
    """

    dataset_path = Path("data/raw/candidates.csv")

    dataframe = load_dataset(dataset_path)

    assert dataframe.shape[0] > 0
    assert dataframe.shape[1] == 13
