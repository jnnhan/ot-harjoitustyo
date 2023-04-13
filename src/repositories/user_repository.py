from entities.user import User
from werkzeug.security import generate_password_hash


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_user(self, user):
        hash_value = generate_password_hash(user.password)
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO users (username, password) values (?, ?)", (user.username, hash_value))

        self._connection.commit()

        return user
    
    def get_password(self, username):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username=?", (username,)
        )
        pas = cursor.fetchone()[0]
        return pas

    def delete_all_users(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM users")

        self._connection.commit()

    def find_user(self, username):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))

        user = cursor.fetchone()
        if user:
            return User(user["username"], user["password"])
        else:
            return None

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        return [User(row["username"], row["password"]) for row in rows]