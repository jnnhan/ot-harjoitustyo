from werkzeug.security import check_password_hash, generate_password_hash
from entities.user import User
from services.sudoku_service import sudoku_service
from repositories.user_repository import user_repo as default_user_repository


class InvalidCredentialsError(Exception):
    """A class for the error raised by invalid credentials."""


class UsernameExistsError(Exception):
    """Class for the error raised by existing username."""


class UserService:
    """A class for application logic that connects the user via UI
        to user repository.

        Attributes:
            user: currently logged in user
            user_repository: UserRepository object for accessing the db
    """

    def __init__(
        self,
        user_repository=default_user_repository
    ):
        """Initialize the service class.

        Args:
            user_repository: UserRepository object for accessing the db. 
            Defaults to default_user_repository.
        """
        self._user = None
        self._user_repository = user_repository

    def get_user_playtime(self, user):
        """Get a number of times sudokus have been played by user.

        Args:
            user: User object

        Returns:
            playtime: number of times sudokus have been solved by the user.
            If playtime is None return 0.
        """

        user_id = self.get_user_id(user)
        playtime = self._user_repository.get_user_playtime(user_id)

        return 0 if playtime is None else playtime

    def get_user_id(self, user):
        """Returns an id for a specific user.

        Args:
            user: User object

        Returns:
            user_id: the id for current user
        """

        user_id = self._user_repository.get_user_id(user.username)

        return user_id

    def logout(self):
        """Log user out and empty the variable of current user.
        """

        self._user = None

    def get_playtime(self, user_id, sudoku_id):
        """Get number of times a specific sudoku has been solved by the user.

        Args:
            user_id: id for current user
            sudoku_id: id for solved sudoku

        Returns:
            playtime: number of times the sudoku has been solved by current user.
        """

        playtime = self._user_repository.get_playtime(user_id, sudoku_id)

        return playtime

    def save_status(self):
        """Save playtime to the database after sudoku has been solved."""
        user_id = self._user_repository.get_user_id(self._user.username)
        sudoku = sudoku_service.get_current_sudoku()

        sudoku_id = sudoku_service.get_sudoku_id(sudoku)

        self._user_repository.save_status(user_id, sudoku_id)

    def get_current_user(self):
        """Get currently logged in user.

        Returns:
            user: User object
        """

        return self._user if self._user else None

    def login(self, username, password):
        """Log user in if correct username and password have been given.
            User types the password and it has to match the corresponding hash password
            in the database.

        Args:
            username: user's attempted username
            password: user's attempted password

        Returns:
            user: User object if both the username and password were correct.

        Raises:
            InvalidCredentialsError: if username or password is incorrect.
        """

        user = self._user_repository.find_user(username)

        if not user:
            raise InvalidCredentialsError("Wrong username")

        hash_password = self._user_repository.get_password(username)
        if check_password_hash(hash_password, password):
            self._user = user
        else:
            raise InvalidCredentialsError("Wrong password")

        return user

    def create_user(self, username, password):
        """Create a new user by adding a username and its password to the database.
        Check if username already exists.

        Args:
            username: a username given by the user.
            password: a password given by the user.

        Returns:
            user: User object

        Raises:
            UsernameExistsError: if username already exists.
            InvalidCredentialsError: if username or password is too short.
        """

        username_exists = self._user_repository.find_user(username)

        if username_exists:
            raise UsernameExistsError(f"Username {username} is taken.")

        if len(username) < 3:
            raise InvalidCredentialsError(
                "Username must be at least\n 3 characters long.")
        if len(password) < 4:
            raise InvalidCredentialsError(
                "Password must be at least\n 4 characters long.")

        hash_value = generate_password_hash(password)

        user = self._user_repository.create_user(
            User(username, password), hash_value)

        return user


user_service = UserService()
