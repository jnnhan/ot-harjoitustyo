from werkzeug.security import check_password_hash
from entities.user import User
from repositories.user_repository import user_repo as default_user_repository
from repositories.sudoku_repository import sudoku_repo as default_sudoku_repository


class InvalidCredentialsError(Exception):
    pass


class UsernameExistsError(Exception):
    pass


class SudokuService:
    def __init__(
        self,
        user_repository=default_user_repository,
        sudoku_repository=default_sudoku_repository
    ):
        self._user = None
        self._sudoku = None
        self._user_repository = user_repository
        self._sudoku_repository = sudoku_repository

    def get_sudokus(self, level):
        sudokus = self._sudoku_repository.get_sudokus(level)
        return sudokus
    
    def get_sudoku_id(self, sudoku):
        sudoku_id = self._sudoku_repository.get_sudoku_id(sudoku.name)

        return sudoku_id
    
    def get_user_id(self, user):
        user_id = self._user_repository.get_user_id(user.username)

        return user_id
    
    def get_playtime(self, user_id, sudoku_id):
        playtime = self._sudoku_repository.get_playtime(user_id, sudoku_id)

        return playtime

    def save_status(self):
        user_id = self._user_repository.get_user_id(self._user.username)
        sudoku_id = self._sudoku_repository.get_sudoku_id(self._sudoku.name)

        self._sudoku_repository.save_status(user_id, sudoku_id)

        return user_id, sudoku_id

    def numbers_to_puzzle(self, sudoku):
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
        return self._sudoku

    def remove_current_sudoku(self):
        self._sudoku = None

    def _check_numbers(self, numbers):
        if len(numbers) > 9:
            return False
        return set(numbers) == set(range(1, 10))

    def _check_square(self, numbers):
        square = []
        for i in range(9):
            for number in numbers[i]:
                square.append(number)
        return self._check_numbers(square)

    def check_sudoku_win(self, sudoku):
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
        self._user = None

    def login(self, username, password):
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
        return self._user

    def create_user(self, username, password):
        username_exists = self._user_repository.find_user(username)

        if username_exists:
            raise UsernameExistsError(f"Username {username} is taken")

        user = self._user_repository.create_user(User(username, password))

        return user


sudoku_service = SudokuService()
