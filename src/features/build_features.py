import logging

from dotenv.main import find_dotenv, load_dotenv
from src.data.stock import Stock
import click
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from src.features.scalers import SCALERS_TRANSFORMERS,SCALER_OUTPUT_FORMATER
from src.features.finta_transformer import FINTA_TRANSFORMER
from src.features.nan_handlers import OFFSET_NAN_DROPER, UnconsistantColumnDroper
from src.features.distances import DISTANCES_OUTPUT_FORMATER, DISTANCES_TRANSFORMERS
import src.config as cfg


def log_step(o):
    if isinstance(o, pd.DataFrame):
        print("--- Shape of dataset: ",  o.shape)
    elif isinstance(o, tuple):
        print("--- Shape of dataset: ",  o[0].shape)
        if o[1] is not None:
            print("--- Shape of labels: ",  o[1].shape)
    return o
LOGGING_STEP = FunctionTransformer(log_step)


"""
    Mix Finta features with scalers

"""
#Les distances ne peuvent pas en état être ajoutées car elles font exploser
# les dimensions de la matrice de feature qui ne peut plus tenir en rame
FEATURES_PIPELINE = Pipeline([
    ("finta", FINTA_TRANSFORMER),
    ("clean_finta", UnconsistantColumnDroper(col_config_slot=cfg.FINTA_COLS)),
    ('scalers', SCALERS_TRANSFORMERS),
    ("scaler_output_formater", SCALER_OUTPUT_FORMATER),
    ("clean_scaled", UnconsistantColumnDroper(col_config_slot=cfg.SCALED_COLS)),
    #("distances", DISTANCES_TRANSFORMERS),
    #("distance_output_formater", DISTANCES_OUTPUT_FORMATER),
    #("clean_distances", UnconsistantColumnDroper(cfg.DISTANCED_COLS)),
    ("nan offset", OFFSET_NAN_DROPER),
    ], 
    verbose=True,
    )

@click.command()
@click.argument('symbol', type=click.String)
def build_features(symbol:str, save=True):
    stock = Stock(symbol)
    X, y = stock.training_data
    X_tr = FEATURES_PIPELINE.fit_transform(X,y)
    if save:
        X_tr.to_csv(index=False)
    return X_tr


if __name__ == "__main__":
    logging.basicConfig(**cfg.LOGGING_CONFIG)
    load_dotenv(find_dotenv())

    build_features()


    

