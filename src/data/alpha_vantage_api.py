import os
import pandas as pd
import logging
import dotenv
import time

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

import src.config as cfg

dotenv.load_dotenv(cfg.DOTENV_PATH)
alpha_vantage_api_key = os.environ.get("AV_API_KEY")


ts = TimeSeries(alpha_vantage_api_key, output_format='pandas')
ti = TechIndicators(alpha_vantage_api_key, output_format ='pandas')
#tools.set_credentials_file(username = plotly_username, api_key = plotly_api_key)


def get_data_from_alpha_vantage(symbol, mode="daily", adjusted=False, interval='15min', outputsize='compact'):
    """ Get data from Alpha_vantage API.


    :param symbol:
        the symbol for the equity we want to get its data
    :param mode: str
        Available modes:
        - "daily"
        - "daily" and adjusted
        - "intraday"
        - "last" : last end point of the security
        - "symbol_search" : Get information about values
    :param adjusted: bool
        if true return the adjusted data. Covering up to 20 years of data.
    :param interval: str
        time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min'
        (default '15min')
    !:param outputsize: str
        The size of the call, supported values are
        'compact' and 'full'; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
    :return:
        data: pandas.DataFrame
            Time series with [date, open, high, low, close, volume] columns
        meta_data: dict
            Dictionnay including: '1.information', '2. Symbol', '3. Last refreshed', '4. Output Size', '5. Time Zone'
    """

    ping = 0
    while ping < 3:
        try:
            if mode == "daily" and not adjusted:
                data, meta_data = ts.get_daily(symbol=symbol, outputsize=outputsize)
            elif mode == "intraday" and not adjusted:
                data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
            elif mode == "daily" and adjusted:
                data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize)
            elif mode == "last":
                data, meta_data = ts.get_quote_endpoint(symbol=symbol)
            elif mode == "symbol_search":
                data, metadata = ts.get_symbol_search(symbol)
                if len(data) > 1:
                  #Select the best matching symbol
                  data = data.loc[data.index == data['9. matchScore'].astype(float).idxmax()].to_dict('list')
            break
        except Exception as e:
            logging.error("An issue occured during Alpha Vantage API call (get_data)")
            logging.error(repr(e))
            ping += 1
            time.sleep(1)
    if ping == 3:
        raise ConnectionError("Impossible to connect to Alpha Vantage API.")
    if mode != "symbol_search":
      data = data.rename(columns = cfg.RENAME_AV_COLUMNS)
      data = data.reset_index()
    return data, meta_data