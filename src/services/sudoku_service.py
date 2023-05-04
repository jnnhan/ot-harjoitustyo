from werkzeug.security import check_password_hash
from entities.user import User
from repositories.user_repository import user_repo as default_user_repository
from repositories.sudoku_repository import sudoku_repo as default_sudoku_repository


class InvalidCredentialsError(Exception):
    pass


class UsernameExistsError(Exception):
    pass


class SudokuService:
    """A Class for application logic that connects user via UI to
    user and sudoku repositories.

    Attributes:
        user: currently logged in user
        sudoku: current or recently played sudoku
        user_repository: UserRepository object
        sudoku_repository: SudokuRepository object
    """

    def __init__(
        self,
        user_repository=default_user_repository,
        sudoku_repository=default_sudoku_repository
    ):
        """Initialize the service class.

        Args:
            user_repository: UserRepository object for accessing the db
            sudoku_repository: SudokuRepository object for accessing the db
        """

        self._user = None
        self._sudoku = None
        self._user_repository = user_repository
        self._sudoku_repository = sudoku_repository

    def get_sudokus(self, level):
        """Get all the sudokus by given level.

        Args: 
            level (int): level for sudokus

        Returns:
            sudokus: a list of Sudoku objects
        """

        sudokus = self._sudoku_repository.get_sudokus(level)
        return sudokus
    
    def get_user_playtime(self, user):
        """Get a number of times sudokus have been played by user.

        Args:
            user: User object

        Returns:
            playtime: number of times sudokus have been solved by the user.
        """

        user_id = self.get_user_id(user)
        playtime = self._sudoku_repository.get_user_playtime(user_id)

        return playtime

    def get_sudoku_id(self, sudoku):
        """Returns an id for a specific sudoku given by the user.

        Args:
            sudoku: Sudoku object

        Returns:
            sudoku_id: The id for specified sudoku
        """

        sudoku_id = self._sudoku_repository.get_sudoku_id(sudoku.name)

        return sudoku_id

    def get_user_id(self, user):
        """Returns an id for a specific user.

        Args:
            user: User object

        Returns:
            user_id: the id for current user
        """

        user_id = self._user_repository.get_user_id(user.username)

        return user_id

    def get_playtime(self, user_id, sudoku_id):
        """Get number of times a specific sudoku has been solved.

        Args:
            user_id: id for current user
            sudoku_id: id for solved sudoku

        Returns:
            playtime: amount the sudoku has been solved
        """

        playtime = self._sudoku_repository.get_playtime(user_id, sudoku_id)

        return playtime

    def save_status(self):
        """Save playtime to the database after sudoku has been solved.
        """
        user_id = self._user_repository.get_user_id(self._user.username)
        sudoku_id = self._sudoku_repository.get_sudoku_id(self._sudoku.name)

        self._sudoku_repository.save_status(user_id, sudoku_id)

    def numbers_to_puzzle(self, sudoku):
        """Convert sudoku to matrix so it can be solved.
            Save the sudoku object as the current sudoku (self._sudoku).
        Args:
            sudoku: Sudoku object

        Returns:
            puzzle: 9x9 matrix
        """

        numbers = [int(n) for n in sudoku.puzzle]

        puzzle = [[[] for _ in range(9)] for _ in range(9)]

        k = 0
        for i in range(9):
            for j in range(9):
                puzzle[i][j].append(numbers[k])
                k += 1

        self._sudoku = sudoku
        return puzzle

    def get_current_sudoku(self):
        """Get current sudoku.

        Returns:
            sudoku: A sudoku object
        """

        return self._sudoku

    def remove_current_sudoku(self):
        """Remove current sudoku. This is done after sudoku is solved and it's status saved.
        """

        self._sudoku = None

    def _check_numbers(self, numbers):
        """Check if a set of 9 numbers has each number 1,2,...,9 and only once.

        Args:
            numbers: a list of numbers (either a row, column or a square).

        Returns:
            True, if the list has all the numbers, otherwise False.
        """

        if len(numbers) > 9:
            return False
        return set(numbers) == set(range(1, 10))

    def _check_square(self, numbers):
        """Check if square in sudoku contains each of the numbers 1,2,...,9 only once.
            Argument is a list of lists, so convert it to a list of numbers.

            Args:
                numbers: a list of 9 lists. Each inner list contains a number.

            Returns:
                True, if the list has all the numbers, otherwise False.
        """

        square = []
        for i in range(9):
            for number in numbers[i]:
                square.append(number)
        return self._check_numbers(square)

    def check_sudoku_win(self, sudoku):
        """Construct and check each row, column and square in the sudoku. Each of these
            must have each of the numbers 1,2,...,9 only once.

            Args:
                sudoku: a full sudoku matrix.

            Returns:
                True, if all the rows, columns and squares are correct, otherwise False.
        """

        for i in range(9):
            row = []
            for j in range(9):
                for number in sudoku[i][j]:
                    row.append(number)
            if not self._check_numbers(row):
                return False

        for i in range(9):
            column = []
            for col in sudoku:
                for number in col[i]:
                    column.append(number)
            if not self._check_numbers(column):
                return False

        for row in range(3):
            for col in range(3):
                numbers = [sudoku[r][c]
                           for r in range(row * 3, (row + 1) * 3)
                           for c in range(col * 3, (col + 1) * 3)]
                if not self._check_square(numbers):
                    return False
        return True

    def logout(self):
        """Log user out and empty the variable of current user.
        """

        self._user = None

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

    def get_current_user(self):
        """Get currently logged in user.

        Returns:
            user: User object
        """

        return self._user

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

        user = self._user_repository.create_user(User(username, password))

        return user


sudoku_service = SudokuService()
