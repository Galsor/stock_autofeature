import os
import dotenv

PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

DOTENV_PATH = os.path.join(PROJECT_DIR, '.env')
dotenv.load_dotenv(DOTENV_PATH)

# Seuil de rentabilité d'une évolution quotidienne
BREAKEVEN = 0.003


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