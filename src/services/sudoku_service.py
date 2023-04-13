from werkzeug.security import check_password_hash
from entities.user import User
from entities.sudoku import Sudoku
from database_connection import get_database_connection
from repositories.user_repository import UserRepository
from repositories.sudoku_repository import SudokuRepository

class InvalidCredentialsError(Exception):
    pass

class SudokuService:
    def __init__(self):
        self._user = None
        self._sudoku = None
        self._user_repository = UserRepository(get_database_connection())
        self._sudoku_repository = SudokuRepository(get_database_connection())

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
        return set(numbers) == set(range(1,10))

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
            return self._check_numbers(row)

        # construct each column as a simple list
        for i in range(9):
            column = []
            for col in sudoku:
                for number in col[i]:
                    column.append(number)
            return self._check_numbers(column)

        for row in range(3):
            for col in range(3):
                numbers = [sudoku[r][c]
                           for r in range(row * 3, (row + 1) * 3)
                           for c in range(col * 3, (col + 1) * 3)]
                return self._check_square(numbers)

    def read_sudokus(self, file_path, level):
        content = ""

        with open(file_path, "r", encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split("\n")

                if parts[0].startswith("."):
                    self._sudoku_repository.create_sudoku(Sudoku(parts[0][1:], content, level))
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
        user = self._user_repository.create_user(User(username, password))

        return user
