from entities.user import User
from database_connection import get_database_connection

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_user(self, user):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO users (username, password) values (?, ?)", (user.username, user.password))

        self._connection.commit()

        return user

    def delete_all_users(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM users *")

        self._connection.commit()

    def find_user(self, username):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username))

        user = cursor.fetchone()

        return user

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        return [User(row["username"], row["password"]) for row in rows]
    
user_repo = UserRepository(get_database_connection())