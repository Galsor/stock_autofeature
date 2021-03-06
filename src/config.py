import os
import dotenv
import logging

PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw") 
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

DOTENV_PATH = os.path.join(PROJECT_DIR, '.env')
dotenv.load_dotenv(DOTENV_PATH)

# Seuil de rentabilit√© d'une √©volution quotidienne
BREAKEVEN = 0.003

#Features generator parameters
SCALING_WINDOW = 10
SMA_DEFAULT_WINDOW = 3

# CONFIG VARIABLES - This values are filled dynamically by the pipeline
CURRENT_COLS = None # To be filled after each step of the transformation
FINTA_COLS = None # To Be filled when finta_transformer class instance is fitted
SCALERS_NAMES = None # To Be filled when scalers.py is loaded
SCALED_COLS = None
DISTANCES_NAMES = None # To Be filled when distances.py is loaded
DISTANCED_COLS = None
NAN_OFFSET = None
SELECTED_NAMES = None # Filled by Selectors
SELECTED_COLS = None
PASSTHROUGH_NAME = "passthrough"

SORT_STOCK_ASCENDING = False
SHIFT = 1 if SORT_STOCK_ASCENDING else -1


DAILY_COMPACT = {
    "mode":"daily",
    "adjusted":False,
    "outputsize":'compact'
} 

DAILY_FULL = {
    "mode":"daily",
    "adjusted":False,
    "outputsize":'full'
}

INTRADAY_15MIN_FULL ={
    "mode":"intraday",
    "adjusted":False,
    "interval":'15min',
    "outputsize":'full'
}

INTRADAY_1MIN_FULL ={
    "mode":"intraday",
    "adjusted":False,
    "interval":'1min',
    "outputsize":'full'
}


STOCK_SETTINGS = DAILY_COMPACT

#Columns names
DATE = "date"
OPEN = "open"
HIGH = "high"
LOW = "low"
CLOSE = "close"
VOLUME = "volume"
LABELS = "labels"
NEXT_DAY_EVOLUTION = "next_day_evolution"
NEXT_DAY_EVOLUTION_RATIO = "next_day_evolution_ratio"

DOHLCV = [DATE, OPEN, HIGH, LOW, CLOSE, VOLUME]
DOHLC = [DATE, OPEN, HIGH, LOW, CLOSE]
OHLC = [OPEN, HIGH, LOW, CLOSE, VOLUME]
OHLCV = [OPEN, HIGH, LOW, CLOSE]

RENAME_AV_COLUMNS = {
    "1. open": OPEN,
    "2. high": HIGH,
    "3. low": LOW,
    "4. close": CLOSE,
    "5. volume": VOLUME
    }

#Alpha vantage metadata dictionnary keys
META_INFORMATION = '1. Information'
META_SYMBOL = '2. Symbol'
META_LAST_REFRESH = '3. Last Refreshed'
META_OUTPUT_SIZE = '4. Output Size'
META_TIME_ZONE = '5. Time Zone'



LOGGING_CONFIG ={
    "format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    "level": logging.INFO
}