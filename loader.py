import pandas as pd
from sample_data import get_dataframe

_cache = None

def load_data() -> pd.DataFrame:
    global _cache
    if _cache is None:
        _cache = get_dataframe()
    return _cache
