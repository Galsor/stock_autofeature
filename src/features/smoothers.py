import numpy as np
import pandas as pd
from math import ceil
from scipy import linalg
import logging  

def lowess(df:pd.DataFrame) -> pd.DataFrame:
    """
        Lowess smooth method.
        This methods implements Alexandre Gramfort's method detailed in the embedded to apply a smoothing filter for the `period` amount of values prior the given point.
        This methods can be used to integrate 'prior information' in the values of the given date.

        Parameter
        ---------
        df: pd.DataFrame
            Data
        
        Returns
        --------
            pd.DataFrame
            The smoothed results
    """
    def lowess_agf(y:pd.Series, period:int=10, iter:int=3) -> np.array:
        """ Lowess method implemented by Alexandre Gramfort and adapted to smooth only based on past values.
        
        Lowess smoother: Robust locally weighted regression.
        The lowess function fits a nonparametric regression curve to a scatterplot.
        The arrays x and y contain an equal number of elements; each pair
        (x[i], y[i]) defines a data point in the scatterplot. 
        The function returns the estimated (smooth) values of y.
        The smoothing span is given by `f` which results from `period`. A larger value for `period` will result in a
        smoother curve. The number of robustifying iterations is given by `iter`. The
        function will run faster with a smaller number of iterations.

        Returns
        -------
            array-like, pd.Series
            The smoothed serie

        """
        if  type(y[0])

        x = np.arange(len(y))
        f = 1./(len(y)/period)
        n = len(x)
        r = int(ceil(f * n))
        h = [np.sort(np.abs(x - x[i]))[r] for i in range(n)]
        w = np.clip(np.abs((x[:, None] - x[None, :]) / h), 0.0, 1.0)
        w = (1 - w ** 3) ** 3
        # triangle the weight matrix to remove the weight of futures points.
        w = np.triu(w)
        yest = np.zeros(n)
        delta = np.ones(n)
        for iteration in range(iter):
            for i in range(n):
                weights = delta * w[:, i]
                b = np.array([np.sum(weights * y), np.sum(weights * y * x)])
                A = np.array([[np.sum(weights), np.sum(weights * x)],
                            [np.sum(weights * x), np.sum(weights * x * x)]])
                try :
                    beta = linalg.solve(A, b)
                    yest[i] = beta[0] + beta[1] * x[i]
                except np.linalg.LinAlgError as e:
                    logging.debug("LinAlgError for value :", i, " during iteration :", iteration)
                    yest[i] = y[i]
                
            residuals = y - yest
            s = np.median(np.abs(residuals))
            delta = np.clip(residuals / (6.0 * s), -1, 1)
            delta = (1 - delta ** 2) ** 2

        return yest

    smoothed_df = df.apply(lowess_agf)
    return smoothed_df

if __name__ == "__main__":
    from src.data.stock import Stock
    s = Stock("aapl")
    print(s.ohlcv)
    print(lowess(s.ohlcv))