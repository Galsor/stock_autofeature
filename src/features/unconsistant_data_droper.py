import pandas as pd
from sklearn.preprocessing import FunctionTransformer
import src.config as cfg

def drop_unconsistant_columns(df:pd.DataFrame) -> pd.DataFrame:
    """
        Check for the first number value (not NaN) and look for NaNs occuring later in the serie.
        If yes, drop the column.
    """
    cols_to_drop = []
    
    for col in df.columns:
        nans = df[col].isna()
        first_valid_idx = df[col].first_valid_index()
        if nans.loc[first_valid_idx:].sum()>0:
            print(f"{col} -> DROPED")
            cols_to_drop.append(col)
    
    cfg.CURRENT_COLS = [col for col in cfg.CURRENT_COLS if col not in cols_to_drop] 
    df.drop(columns=cols_to_drop, inplace=True)
    return df

UNCONSISTANT_FEATURE_DROPER = FunctionTransformer(drop_unconsistant_columns)