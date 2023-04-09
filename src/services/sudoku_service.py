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

    def create_sudoku(self, puzzle, level):
        sudoku = self._sudoku_repository.create_sudoku(Sudoku(puzzle, level))

        return sudoku

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