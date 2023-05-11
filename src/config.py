import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

DB_FILE = os.getenv("DB_FILE") or "database.sqlite"
DB_FILE_PATH = os.path.join(dirname, "..", "data", DB_FILE)
