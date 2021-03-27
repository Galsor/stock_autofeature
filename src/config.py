import os
import dotenv

PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

DOTENV_PATH = os.path.join(PROJECT_DIR, '.env')
dotenv.load_dotenv(DOTENV_PATH)