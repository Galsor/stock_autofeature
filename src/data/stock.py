import pandas as pd

import src.config as cfg
from src.data.alpha_vantage import get_data_from_alpha_vantage

class Stock:
    def __init__(self, symbol:str, mode:str="daily", adjusted:bool=False, interval:str='15min', outputsize:str='compact') -> None:
        self._dohlcv, metadata = get_data_from_alpha_vantage(symbol= symbol)
        self._dohlcv.sort_index(ascending=False, inplace=True)
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