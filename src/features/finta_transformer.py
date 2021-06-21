import inspect
import pandas as pd
import logging

from finta import TA

from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin

import src.config as cfg

FINTA_METHODS = inspect.getmembers(TA, predicate=inspect.isfunction)

def compute_finta_metrics(ohlcv: pd.DataFrame) -> pd.DataFrame:
    """
        Generates Financial Technical Analysis features.
        More information on the methods implemented in Finta librairy documentation: 
        https://github.com/peerchemist/finta

    Parameters
    ----------
    ohlcv: pd.DataFrame
        Open, high, low, close stock prices with volumes and with dates as indexes.

    Example:
    --------
    ```Python
        from src.data.stock import Stock
        stock = Stock("aapl")
        features = add_finta_metrics(stock.ohlcv)
    ```

    """
    if isinstance(ohlcv, pd.Series):
        ohlcv = pd.DataFrame(ohlcv).T

    inds = [ohlcv]
    error_count = 0
    for name, method in FINTA_METHODS:
        try:
            ind_df = method(ohlcv)
            if name.lower() not in ind_df.columns :
                ind_df = ind_df.add_prefix(f"{name}_")
            elif len(ind_df.columns)>1:
                #Change only columns name if different than indicator name
                ind_df.columns = [col if col.lower()==name.lower() else f"{name}_{col}" for col in ind_df.columns]
            inds.append(ind_df)
        except Exception as e:
            logging.debug(f"Fail during processing of {name} method")
            logging.debug(e)
            error_count += 1
    logging.info(f"{error_count} errors occured during finta features generation ({round(error_count/len(FINTA_METHODS)*100,2)}% of methods).")
    
    finta_ind = pd.concat(inds, axis=1, ignore_index=False)
    cfg.FINTA_COLS = cfg.CURRENT_COLS = list(finta_ind.columns)
    return finta_ind

#DEPRECATED - Prefer using FintaTransformer Class
#FINTA_TRANSFORMER = FunctionTransformer(compute_finta_metrics)


class FintaTransformer(TransformerMixin, BaseEstimator):
    """
        Transform stock prices by appling them a wide range of financial technical analysis indicators
        This class is design to be used in scikit-learn pipeline

    """
    def __init__(self) -> None:
        super().__init__()
        self.buffer_size = 99 # Amount of past values needed to compute all indicators
        self._buffer = []

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
            self._buffer = X.iloc[-self.buffer_size:]
        else:
            try:
                self._buffer = X[-self.buffer_size :]
            except KeyError:
                raise KeyError("X must be an array-like type and preferably pd.DataFrame")
        return self

    def transform(self, X) -> pd.DataFrame:
        """Scale features of X according to the local min and max values.
        If X contains less values than buffer_size size, X is completed with previous values saved in buffer.
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

        if n < self.buffer_size:
            missing_values_count = self.buffer_size - n
            previous_values = self._buffer.iloc[-missing_values_count:]
            X_tr = previous_values.append(X)
        else :
            X_tr = X.copy()
                
        self._buffer = X.iloc[-self.buffer_size:]

        X_tr = compute_finta_metrics(X_tr)
        return X_tr.iloc[-n:] 

FINTA_TRANSFORMER = FintaTransformer()

if __name__ == "__main__":
    from src.data.stock import Stock
    stock = Stock("aapl")
    print(compute_finta_metrics(stock.ohlcv))
