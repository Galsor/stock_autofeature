import pandas as pd
from sklearn.preprocessing import FunctionTransformer

# Pass the processing step without transformation
def passthrough(df:pd.DataFrame) -> pd.DataFrame:
    return df

PASSTHROUGH_TRANSFORMER = FunctionTransformer(passthrough)