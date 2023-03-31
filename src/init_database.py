from database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()

    sql = "DROP TABLE IF EXISTS users"
    cursor.execute(sql)

    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()

    sql = "CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT)"
    cursor.execute(sql)

    connection.commit()

def init_db():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    init_db()