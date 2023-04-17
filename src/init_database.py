from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS sudokus")
    cursor.execute("DROP TABLE IF EXISTS stats")

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT)"
    )
    cursor.execute(
        "CREATE TABLE sudokus (id SERIAL PRIMARY KEY, name TEXT UNIQUE, \
        puzzle TEXT UNIQUE, level INTEGER)"
    )
    cursor.execute(
        "CREATE TABLE stats (id SERIAL PRIMARY KEY, user_id REFERENCES users, \
        sudoku_id REFERENCES sudokus, status INTEGER)"
    )

    connection.commit()


def init_db():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    init_db()
