""" This files describes functions and transformer computing distances
 between the current data points and various features 
 such as moving average or smoothed curve"""

import pandas as pd
from typing import Callable
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import FeatureUnion

from src.features.smoothers import lowess_agf, SMA
from src.features.passthrough import PASSTHROUGH_TRANSFORMER
import src.config as cfg


def signed_distance(df:pd.DataFrame, func:Callable, args:tuple=(), kwds:dict={}) -> pd.DataFrame:
    """
        Apply a reference function (i.e lowess smoother or moving average)
        to input dataframe.
        Then compute the euclidian distance between dataframe points and 
        the transformed dataframe.

        Parameters
        ----------

        df: pd.DataFrame
            The input Dataframe
        func: python function
            The function to apply to dataframe to genere reference data
        args: tuple
            Positional arguments to pass to func in addition to the array/series.
        kwds: dictionary
            Additional keyword arguments to pass as keywords arguments to func.


    """
    print(f"--- transform {func.__name__} ---")
    print(df.shape)
    df_ref = func(df, args=args, kwds=kwds)
    print(df_ref.shape)
    return df - df_ref

LOWESS_SIGNED_DISTANCE = FunctionTransformer(signed_distance, kw_args={"func":lowess_agf})
SMA3_SIGNED_DISTANCE = FunctionTransformer(signed_distance, kw_args={"func":SMA, "kwds":{"window":3}})

DISTANCES = [
    (cfg.PASSTHROUGH_NAME, PASSTHROUGH_TRANSFORMER),
    #("lowess_distance", LOWESS_SIGNED_DISTANCE),
    ("sma3_distance", SMA3_SIGNED_DISTANCE),
]

cfg.DISTANCES_NAMES = [s[0] for s in DISTANCES]

DISTANCES_TRANSFORMERS = FeatureUnion(DISTANCES)

def reformat_distance_output(X):

    if not isinstance(X, pd.DataFrame):
        X_f = pd.DataFrame(X)
    else:
        X_f = X
    
    if isinstance(X, pd.Series):
        X_f = X_f.T
    #TODO: reformat function to merge with scaler reformater
    columns = cfg.SCALED_COLS
    for distance in cfg.DISTANCES_NAMES:
        if distance != cfg.PASSTHROUGH_NAME:
            for ind in cfg.SCALED_COLS:
                columns.append(str(ind)+"_"+distance)
    
    X_f.columns = columns
    cfg.DISTANCED_COLS = columns
    return X_f
    
DISTANCES_OUTPUT_FORMATER = FunctionTransformer(reformat_distance_output)