from numpy.lib.function_base import percentile
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.preprocessing import FunctionTransformer

from src.features.scalers import SCALERS_TRANSFORMERS,SCALER_OUTPUT_FORMATER
from src.features.finta_transformer import FINTA_TRANSFORMER
from src.features.unconsistant_data_droper import UNCONSISTANT_FEATURE_DROPER
from src.features.distances import DISTANCES_TRANSFORMERS
import src.config as cfg


def log_step(df):
    print(df.shape)
    return df
LOGGING_STEP = FunctionTransformer(log_step)


"""
    Mix Finta features with scalers and select relevant features according to labels

"""
#Les distances ne peuvent pas en état être ajoutées car elles font exploser
# les dimensions de la matrice de feature qui ne peut plus tenir en rame
# TODO: Ajouter un mécanisme de selection de feature au sein des transformers
FEATURES_PIPELINE = Pipeline([
    ("finta", FINTA_TRANSFORMER),
    ("drop1", UNCONSISTANT_FEATURE_DROPER),
    ("log1", LOGGING_STEP),
    ('scalers', SCALERS_TRANSFORMERS),
    ("scaler_output_formater", SCALER_OUTPUT_FORMATER),
    #("drop2", UNCONSISTANT_FEATURE_DROPER),
    #("log2", LOGGING_STEP),
    #("distances", DISTANCES_TRANSFORMERS),
    #('anova', SelectPercentile(chi2, percentile=0.1))
    ], 
    #memory=".pipeline_cache/"
    )



def build_features(stock):
    pass

if __name__ == "__main__":
    from src.data.stock import Stock
    stock = Stock("aapl")

    X, y = stock.training_data
    X, X_last = X.iloc[:-1], X.iloc[-1]
    y, y_last = y.iloc[:-1], y.iloc[-1]
    X_tr = FEATURES_PIPELINE.fit_transform(X,y)
    pred = FEATURES_PIPELINE.transform(X_last)
    print(X_tr.shape)
    #print(X_tr.columns)
    print(pred)
    print(X_tr.columns)
    s = X_tr.isna().sum()/len(X_tr)
    print(s.where(s!=1).mean())
    #print(len(null_cols)/len(X_tr.shape[1]))
    #print(null_cols)

