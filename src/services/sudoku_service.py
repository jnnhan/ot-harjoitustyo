from werkzeug.security import check_password_hash
import copy
from entities.user import User
from entities.sudoku import Sudoku
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

    def start_sudoku(self, sudoku):
        self.puzzle = copy.deepcopy(sudoku)
        self.original = copy.deepcopy(sudoku)
        self.game_over = False

    def get_sudokus(self, level):
        sudokus = self._sudoku_repository.get_sudokus(level)
        return sudokus

    def numbers_to_puzzle(self, sudoku):
        numbers = [int(n) for n in sudoku]

        puzzle = [[[] for _ in range(9)] for _ in range(9)]

        k = 0
        for i in range(9):
            for j in range(9):
                puzzle[i][j].append(numbers[k])
                k += 1

        return puzzle

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
        # construct each row in sudoku as a simple list
        for i in range(9):
            row = []
            for j in range(9):
                for number in sudoku[i][j]:
                    row.append(number)
            if not self._check_numbers(row):
                return False

        # construct each column as a simple list
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
        self.game_over = True
        return True

    def read_sudokus(self, file_path, level):
        content = ""

        with open(file_path, "r", encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split("\n")

                if parts[0].startswith("."):
                    self._sudoku_repository.create_sudoku(
                        Sudoku(parts[0][1:], content, level))
                    content = ""
                else:
                    content += parts[0]

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

    def create_user(self, username, password):
        username_exists = self._user_repository.find_user(username)

        if username_exists:
            raise UsernameExistsError(f"Username {username} is taken")

        user = self._user_repository.create_user(User(username, password))

        return user
