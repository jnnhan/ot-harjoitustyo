from database_connection import get_database_connection
from entities.user import User


class UserRepository:
    """A class that connects the database and UserService class.
        Handles User objects and the user and stats tables in the database.
        Handles user information and the sudoku statistics of the user.

        Attributes:
            connection: the database connection.
    """

    def __init__(self, connection):
        """Initialize the repository class.

            Args:
                connection: database connection.
        """

        self._connection = connection

    def get_playtime(self, user_id, sudoku_id):
        """Get number of times given sudoku has been solved by user.

        Args:
            user_id: id of currently logged in user.
            sudoku_id: id of given sudoku.

        Returns:
            playtime: amount of times sudoku has been solved
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT playtime FROM stats WHERE user_id=? AND sudoku_id=?",
                       (user_id, sudoku_id))

        playtime = cursor.fetchone()

        return playtime[0] if playtime else None

    def save_status(self, user_id, sudoku_id):
        """Save or update the playtime of given sudoku.
            If no prior playtime exists, new playtime is 1. Otherwise add 1 to prior playtime.

        Args:
            user_id: currently logged in user.
            sudoku_id: id of recently solved sudoku.
        """

        cursor = self._connection.cursor()

        playtime = self.get_playtime(user_id, sudoku_id)

        if playtime is None:
            cursor.execute(
                "INSERT INTO stats (user_id, sudoku_id, playtime) values (?, ?, ?)",
                (user_id, sudoku_id, 1)
            )
        else:
            cursor.execute(
                "UPDATE stats SET playtime=? WHERE user_id=? AND sudoku_id=?",
                ((playtime+1), user_id, sudoku_id)
            )
        self._connection.commit()

    def get_user_playtime(self, user_id):
        """Get number of times sudokus have been solved by the user.

        Args:
            user_id: id of currently logged in user.

        Returns:
            playtime: a number of times sudokus have been solved by the user.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT SUM(playtime) FROM stats WHERE user_id=?", (user_id,)
        )

        playtime = cursor.fetchone()

        return playtime[0]

    def create_user(self, user, hashpassword):
        """Save a new user to database.
            Password is a hash-value for the user password.

            Args:
                user: User object

            Returns:
                user: User object
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) values (?, ?)", (
                user.username, hashpassword)
        )

        self._connection.commit()

        return user

    def get_password(self, username):
        """Get hashed password from database.

            Args:
                username: username the user tries to login with.

            Return:
                password: hashed password connected with the given username.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username=?", (username,)
        )
        password = cursor.fetchone()[0]
        return password

    def delete_all_users(self):
        """Delete all the users from database.
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM users")

        self._connection.commit()

    def find_user(self, username):
        """Check if given username exists in the database.

            Args:
                username: user tries to log in with this username.

            Returns:
                user: User object if username existed, otherwise None.
        """

        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))

        user = cursor.fetchone()

        return User(user["username"], user["password"]) if user else None

    def get_user_id(self, username):
        """Get user id matching given username.
            It's assumed that the user exists.

            Args:
                username: currently logged in user.

            Returns:
                id of current user.
        """

        cursor = self._connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))

        return cursor.fetchone()[0]

    def find_all(self):
        """Find all users from database.

            Returns: 
                A list of User objects if users exist.
        """

        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        return [User(row["username"], row["password"]) for row in rows]


user_repo = UserRepository(get_database_connection())
