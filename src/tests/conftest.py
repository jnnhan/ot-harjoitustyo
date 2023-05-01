from init_database import init_db
from read_sudokus import read_sudokus


def pytest_configure():
    init_db()
    read_sudokus()
