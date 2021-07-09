import logging
from typing import Tuple
import pandas as pd
import json
from pathlib import Path

from scipy.sparse import data

import src.config as cfg
from src.data.alpha_vantage_api import get_data_from_alpha_vantage

default_settings = cfg.STOCK_SETTINGS

class Stock:

    def __init__(self, symbol:str, save=False) -> None:
        self.symbol = symbol
        self._dohlcv, metadata = self.load_existing_dataset()
        
        if self._dohlcv is None:
            self._dohlcv, metadata = get_data_from_alpha_vantage(symbol= symbol, **default_settings)
            self._dohlcv.sort_index(ascending=cfg.SORT_STOCK_ASCENDING, inplace=True)
        
        if save:
            self.save(self._dohlcv, metadata)
    
    @property
    def ohlc(self) -> pd.DataFrame:
        """ Open, Low, High, Close with dates as index"""
        return self.dohlcv[cfg.DOHLC].set_index(cfg.DATE)
    
    @property
    def ohlcv(self) -> pd.DataFrame:
        """ Open, Low, High, Close and volumes with dates as index"""
        return self.dohlcv.set_index(cfg.DATE)
    
    @property
    def dohlcv(self) -> pd.DataFrame:
        """ Dates, Open, Low, High, Close and Volumes with integer indexes"""
        return self._dohlcv
    
    @property
    def _daily_evolution(self) -> pd.Series:
        return self._dohlcv[cfg.CLOSE] - self._dohlcv[cfg.OPEN]

    @property
    def _next_day_evolution(self) -> pd.Series:
        return self._daily_evolution.shift(cfg.SHIFT)
    
    @property
    def _next_day_evolution_ratio(self) -> pd.Series:
        return self._next_day_evolution/self._dohlcv.shift(cfg.SHIFT)[cfg.OPEN]
    
    # ----------- Data accessors -----------

    @property
    def labels(self) -> pd.DataFrame:
        s_label = self._next_day_evolution_ratio.apply(lambda x : 0 if x < cfg.BREAKEVEN else x/x) # x/x to return nan if needed
        return pd.DataFrame(s_label)

    @property
    def training_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.ohlcv.iloc[:-1], self.labels[:-1]
    
    @property
    def features(self) -> pd.DataFrame:
        return self.load_existing_features()

    @property
    def last_data(self) -> pd.DataFrame:
        return self.ohlcv.iloc[-1]

    # ----------- File paths -----------

    @property
    def data_filepath(self) -> Path:
        return Path(cfg.RAW_DATA_DIR) / f"{self.symbol}.csv"
    
    @property
    def features_filepath(self) -> Path:
        return Path(cfg.PROCESSED_DATA_DIR) / f"{self.symbol}_all_features.csv"
    
    @property
    def metadata_filepath(self) -> Path:
        return Path(cfg.RAW_DATA_DIR) / f"{self.symbol}_metadata.json"

    # ----------- File load & save utils -----------

    def load_existing_dataset(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if self.data_filepath.exists() and self.metadata_filepath.exists():
            data = pd.read_csv(self.data_filepath)
            with open(self.metadata_filepath, 'r') as fp:
                metadata = json.load(fp)
            return data
        elif self.data_filepath.exists():
            return pd.read_csv(self.data_filepath), None
        else:
            return None, None

    def load_existing_features(self) -> pd.DataFrame:
        try :
            return pd.read_csv(self.features_filepath)
        except FileNotFoundError:
            logging.warning("No features file found.\
                Processed raw data with `make features` to enable this attribute.")
            return None

    def save(self, data, metadata) -> str:
        """Save Raw DOHLCV data"""
        data.to_csv(self.data_filepath, index=False)
        with open(self.metadata_filepath, 'w') as fp:
            json.dump(metadata, fp)
        return self.data_filepath

if __name__ == '__main__':
    Stock("aapl", save=True)
