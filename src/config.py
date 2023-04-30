import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

DB_FILE = os.getenv("DB_FILE") or "database.sqlite"
DB_FILE_PATH = os.path.join(dirname, "..", "data", DB_FILE)

EASY_FILE = os.getenv("EASY_FILE") or "easy.txt"
EASY_FILE_PATH = os.path.join(dirname, "..", "data", EASY_FILE)

MEDIUM_FILE = os.getenv("MEDIUM_FILE") or "medium.txt"
MEDIUM_FILE_PATH = os.path.join(dirname, "..", "data", MEDIUM_FILE)

HARD_FILE = os.getenv("HARD_FILE") or "hard.txt"
HARD_FILE_PATH = os.path.join(dirname, "..", "data", HARD_FILE)
