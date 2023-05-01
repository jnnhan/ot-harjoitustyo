from werkzeug.security import generate_password_hash
from database_connection import get_database_connection
from entities.user import User


class UserRepository:
    """A class that connects the database and SudokuService class.
        Handles User objects and the user table in the database.
        
        Attributes:
            connection: the database connection.
    """

    def __init__(self, connection):
        """Initialize the repository class.
        
            Args:
                connection: database connection.
        """

        self._connection = connection

    def create_user(self, user):
        """Save a new user to database.
            Hash password using werkzeug password hashing.
            
            Args:
                user: User object
                
            Returns:
                user: User object
        """

        hash_value = generate_password_hash(user.password)
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) values (?, ?)", (
                user.username, hash_value)
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
            It's assumed that the user ecists.
            
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
