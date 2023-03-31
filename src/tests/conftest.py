from init_database import init_db


def pytest_configure():
    init_db()
