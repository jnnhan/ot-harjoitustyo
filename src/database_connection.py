from config import DB_FILE_PATH
import sqlite3

connection = sqlite3.connect(DB_FILE_PATH)
connection.row_factory = sqlite3.Row

def get_database_connection():
    return connection