from pathlib import Path

import pandas as pd


def load_catalog(file_source) -> pd.DataFrame:
    """Load a supplier catalog from an uploaded file or local path."""
    return pd.read_csv(file_source)


def load_demo_catalog() -> pd.DataFrame:
    """Load the fictional demo catalog."""
    path = Path("data/sample_supplier_catalog.csv")
    return load_catalog(path)