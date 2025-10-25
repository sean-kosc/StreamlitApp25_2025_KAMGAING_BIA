import pandas as pd
from pathlib import Path

LOCAL_PATH = Path(__file__).parent.parent / "data" / "velib-emplacement-des-stations.csv"

def load_data(source_path: Path = LOCAL_PATH) -> pd.DataFrame:
    """
    Loads Vélib data from local CSV (separator ';')
    """
    try:
        return pd.read_csv(source_path, sep=";", encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(source_path, sep=";", encoding="utf-8")
