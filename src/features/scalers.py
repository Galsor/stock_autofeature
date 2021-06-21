import pandas as pd
import logging
from pandas.core.series import Series
from sklearn.preprocessing import StandardScaler, MinMaxScaler, FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion

from src.features.passthrough import PASSTHROUGH_TRANSFORMER
import src.config as cfg


def moving_standard_scaler(df: pd.DataFrame, window:int=10) -> pd.DataFrame :
    """ 
        Custom method applying standard scaler based on rolling average and standard deviation.

        Parameters
        ----------
        df: pd.DataFrame
            stock data with volumes and dates as index
        window: int
            Amount of days used in rolling windows
    """

    return (df - df.rolling(window).mean()) / df.rolling(window).std()

class MovingStandardScaler(TransformerMixin, BaseEstimator):
    """Standardize features by removing the mean and scaling to unit variance
    
    The standard score of a sample `x` is calculated as:
        z = (x - u) / s
    
    where `u` is the mean of the training samples or zero if `with_mean=False`,
    and `s` is the standard deviation of the training samples or one if
    `with_std=False`.

    This class is design to be used in scikit-learn pipeline

    """

    def __init__(self, window, with_mean=True, with_std=True):
        self.window = window
        self.with_mean = with_mean
        self.with_std = with_std


    def fit(self, X, y=None, sample_weight=None):
        """Compute the mean and std to be used for later scaling.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to compute the mean and standard deviation
            used for later scaling along the features axis.
        y : None
            Ignored.
        sample_weight : array-like of shape (n_samples,), default=None
            Individual weights for each sample.
            .. versionadded:: 0.24
               parameter *sample_weight* support to StandardScaler.
        Returns
        -------
        self : object
            Fitted scaler.
        """
        if isinstance(X, pd.DataFrame):
            self.buffer_ = X.iloc[-self.window:]
        else:                    
            try:
                self.buffer_ = X[-self.window]
            except KeyError:
                raise KeyError("X must be an array-like type and preferably pd.DataFrame")

        return self
    
    def transform(self, X, copy=None):
        """Perform standardization by centering and scaling
        Parameters
        ----------
        X : {array-like, sparse matrix of shape (n_samples, n_features)
            The data used to scale along the features axis.
        copy : bool, default=None
            Copy the input X or not.
        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Transformed array.
        """
        if not isinstance(X, pd.DataFrame) and not isinstance(X, pd.Series):
            X = pd.DataFrame(X)

        n = len(X) if not isinstance(X, pd.Series) else 1

        if n < self.window:
            missing_values_count = self.window +1 - n
            previous_values = self.buffer_.iloc[-missing_values_count:]
            X_tr = previous_values.append(X)
        else :
            X_tr = X.copy()
        
        self.buffer_ = X.iloc[-self.window :]
        
        means = X_tr.rolling(self.window).mean()
        stds = X_tr.rolling(self.window).std()
        if self.with_mean:
            X_tr -= means
        if self.with_std:
            X_tr /= stds
        return X_tr.iloc[-n:] 


def moving_min_max_scaler(df: pd.DataFrame, window:int=10) -> pd.DataFrame :
    """
        Custom method applying MinMaxScaler based on rolling minimum and maximum values.
    
        Parameters
        ----------
        df: pd.DataFrame
            stock data with volumes and dates as index
        window: int
            Amount of days used in rolling windows
    """
    mins = df.rolling(window).min()
    maxs = df.rolling(window).max()
    return (df - mins)/(maxs - mins)


class MovingMinMaxScaler(TransformerMixin, BaseEstimator):
    """Transform features by scaling each feature to a given range.
    
    This estimator scales and translates each feature individually such
    that it is in the given range on the training set, e.g. between
    zero and one.

    The transformation is given by::
        X_std = (X - X.rolling(window).min(axis=0)) / (X.rolling(window).max(axis=0) - X.rolling(window).min(axis=0))
    
    This class is design to be used in scikit-learn pipeline
    """

    def __init__(self, window) -> None:
        self.window = window

    def fit(self, X, y=None):
        """Save the end of training dataset as buffer for further completion of partial window during transform.
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data used to compute the per-feature minimum and maximum
            used for later scaling along the features axis.
        y : None
            Ignored.
        Returns
        -------
        self : object
            Fitted scaler.
        """
        if isinstance(X, pd.DataFrame):
            self.buffer_ = X.iloc[-self.window:]
        else:
            try:
                self.buffer_ = X[-self.window :]
            except KeyError:
                raise KeyError("X must be an array-like type and preferably pd.DataFrame")

        return self

    def transform(self, X) -> pd.DataFrame:
        """Scale features of X according to the local min and max values.
        If X contains less values than window size, X is completed with previous values saved in buffer.
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data that will be transformed.
        Returns
        -------
        Xt : ndarray of shape (n_samples, n_features)
            Transformed data.
        """
        if not isinstance(X, pd.DataFrame) and not isinstance(X, pd.Series):
            X = pd.DataFrame(X)
        
        n = len(X) if not isinstance(X, pd.Series) else 1

        if n < self.window:
            missing_values_count = self.window - n
            previous_values = self.buffer_.iloc[-missing_values_count:]
            X_tr = previous_values.append(X)
        else :
            X_tr = X.copy()
                
        self.buffer_ = X.iloc[-self.window:]

        mins = X_tr.rolling(self.window).min()
        maxs = X_tr.rolling(self.window).max()
        X_tr -= mins
        X_tr /= maxs - mins
        return X_tr.iloc[-n:] 


def moving_low_high_scaler(ohlc:pd.DataFrame, window:int=10) -> pd.DataFrame:
    """
        Custom method standardizing prices with the lowest and the highest price of the window.
    
        Parameters
        ----------
        ohlc: pd.DataFrame
            stock prices data without volumes and with dates as index
        window: int
            Amount of days used in rolling windows
    """
    mins = ohlc[cfg.LOW].rolling(window).min()
    maxs = ohlc[cfg.HIGH].rolling(window).max()
    return ohlc.apply(lambda x: (x - mins)/(maxs - mins))

SCALERS = [
    (cfg.PASSTHROUGH_NAME, PASSTHROUGH_TRANSFORMER),
    ("standard_scaler", StandardScaler()),
    ("minmax_scaler", MinMaxScaler()),
    ("moving_standard_scaler",MovingStandardScaler(window=cfg.SCALING_WINDOW)),
    ("moving_minmax_scaler", MovingMinMaxScaler(window=cfg.SCALING_WINDOW)),
]

cfg.SCALERS_NAMES = [s[0] for s in SCALERS]

SCALERS_TRANSFORMERS = FeatureUnion(SCALERS)

def reformat_scaling_output(X):

    # Convert numpy or Series in DataFrame
    if isinstance(X, pd.Series):
        X = pd.DataFrame(X)
        X = X.T
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    
    print(X.columns)

    # Rename columns
    scaled_columns = []
    for scaler in cfg.SCALERS_NAMES:
        if scaler != cfg.PASSTHROUGH_NAME:
            for ind in cfg.CURRENT_COLS:
                scaled_columns.append(str(ind+"_"+scaler))
    
    cfg.CURRENT_COLS += scaled_columns 
    X.columns = cfg.CURRENT_COLS
    cfg.SCALED_COLS = cfg.CURRENT_COLS
    return X

SCALER_OUTPUT_FORMATER = FunctionTransformer(reformat_scaling_output)

if __name__ == "__main__":
    from src.data.stock import Stock
    from src.visualization.ohlcv import candlestick
    stock = Stock("aapl")
    #print(moving_low_high_scaler(stock.ohlc))
    #candlestick(stock.ohlc)
    
    X, last = stock.ohlc.iloc[:-1], stock.ohlc.iloc[-1]
    print(X)
    """st_sc = MovingStandardScaler(window=10).fit(X)
    X_std = st_sc.transform(X)
    print(X_std)

    mm_sc = MovingMinMaxScaler(window=10).fit(X)
    X_mm = mm_sc.transform(X)
    print(X_mm)
    print("_"*80)
    print(st_sc.buffer_)
    print(mm_sc.buffer_)
    print("_"*80)
    print(last)
    print(st_sc.transform(last))
    print(mm_sc.transform(last))"""
    print(SCALERS_TRANSFORMERS.fit_transform(X))

    print(SCALERS_TRANSFORMERS.transformer_list[:][0])



