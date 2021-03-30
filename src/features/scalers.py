import pandas as pd
import numpy as np
import logging
from math import ceil
from scipy import linalg

def moving_standard_scaler(ohlcv: pd.DataFrame, period:int=10) -> pd.DataFrame :
    """ 
        Custom method applying standard scaler based on rolling average and standard deviation.

        Parameters
        ----------
        ohlcv: pd.DataFrame
            stock data with volumes and dates as index
        period: int
            Amount of days used in rolling windows
    """

    return (ohlcv - ohlcv.rolling(period).mean()) / ohlcv.rolling(period).std()


def moving_min_max_scaler(ohlcv: pd.DataFrame, period:int=10) -> pd.DataFrame :
    """
        Custom method applying MinMaxScaler based on rolling minimum and maximum values.
    
        Parameters
        ----------
        ohlcv: pd.DataFrame
            stock data with volumes and dates as index
        period: int
            Amount of days used in rolling windows
    """
    mins = ohlcv.rolling(period).min()
    maxs = ohlcv.rolling(period).max()
    return (ohlcv - mins)/(maxs - mins)



if __name__ == "__main__":
    from src.data.stock import Stock
    stock = Stock("aapl")
    print(moving_standard_scaler(stock.ohlcv))