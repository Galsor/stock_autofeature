import pandas as pd
from src.data.alpha_vantage import get_data_from_alpha_vantage

def test_get_data_from_alpha_vantage():
    df, meta = get_data_from_alpha_vantage("AAPL")
    assert isinstance(df, pd.DataFrame) and len(df) > 0

