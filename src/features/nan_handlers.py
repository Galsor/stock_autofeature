from typing import Tuple
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
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

    df.drop(columns=cols_to_drop, inplace=True)
    cfg.CURRENT_COLS = list(df.columns)
    return df

class UnconsistantColumnDroper(TransformerMixin, BaseEstimator):
    def __init__(self, col_config_slot=cfg.CURRENT_COLS):
        self.col_slot = col_config_slot
    
    def fit(self, X:pd.DataFrame, y=None)->pd.DataFrame:
        return self
    
    def transform(self, X:pd.DataFrame, y=None)-> pd.DataFrame:
        X = drop_unconsistant_columns(X)
        print(X)
        if self.col_slot is None:
            self.col_slot = list(X.columns)
        return X[self.col_slot]

def offset_nan(X:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print("--- Offset NaNs ---")
    first_valid_indexes = []
    for col in X.columns:
        nans = X[col].isna()
        first_valid_indexes.append(X[col].first_valid_index())
    cfg.NAN_OFFSET = max(first_valid_indexes)
    X = X.iloc[cfg.NAN_OFFSET:].reset_index(drop=True)
    return X

OFFSET_NAN_DROPER = FunctionTransformer(offset_nan)