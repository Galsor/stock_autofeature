from typing import Tuple
import pandas as pd

import src.config as cfg
from src.data.alpha_vantage import get_data_from_alpha_vantage

default_settings = cfg.STOCK_SETTINGS

class Stock:
    def __init__(self, symbol:str) -> None:
        self._dohlcv, metadata = get_data_from_alpha_vantage(symbol= symbol, **default_settings)
        self._dohlcv.sort_index(ascending=cfg.SORT_STOCK_ASCENDING, inplace=True)
        self.symbol = metadata[cfg.META_SYMBOL]
        self.tz = metadata[cfg.META_TIME_ZONE]
    
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
    
    @property
    def labels(self) -> pd.Series:
        return self._next_day_evolution_ratio.apply(lambda x : 0 if x < cfg.BREAKEVEN else x/x) # x/x to return nan if needed

    @property
    def training_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        return self.ohlcv, self.labels
