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
HIGH = "high",
LOW = "low"
CLOSE = "close"
VOL = "volume"
LABELS = "labels"
NEXT_DAY_EVOLUTION = "next_day_evolution"
NEXT_DAY_EVOLUTION_RATIO = "next_day_evolution_ratio"

OHLCV_COLUMNS_NAME = [DATE, OPEN, HIGH, LOW, CLOSE, VOL]