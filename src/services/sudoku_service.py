from entities.user import User
from entities.sudoku import Sudoku
from database_connection import get_database_connection
from repositories.user_repository import UserRepository
from repositories.sudoku_repository import SudokuRepository
from werkzeug.security import check_password_hash
from sudokus import *

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

    def read_sudokus(self, file_path, level):
        content = ""

        file = open(file_path, "r")
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
        hash_password = self._user_repository.check_password(username)

        if not user:
            raise InvalidCredentialsError("Wrong username")
        else:
            if check_password_hash(hash_password, password):
                self._user = user
            else:
                raise InvalidCredentialsError("Wrong password")

        return user

    def create_user(self, username, password):
        user = self._user_repository.create_user(User(username, password))

        return user