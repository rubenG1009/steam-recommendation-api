import pandas as pd
import os

CLEAN_PATH = "data/steam_clean.csv"

_df_cache = None

def load_data() -> pd.DataFrame:
    global _df_cache
    if _df_cache is not None:
        return _df_cache
    if not os.path.exists(CLEAN_PATH):
        raise FileNotFoundError(
            f"Clean dataset not found at '{CLEAN_PATH}'. "
            "Please run 'python etl.py' first to process the raw data."
        )
    _df_cache = pd.read_csv(CLEAN_PATH)
    return _df_cache
