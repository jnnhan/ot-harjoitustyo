from werkzeug.security import check_password_hash, generate_password_hash
import unittest
from entities.user import User
from entities.sudoku import Sudoku
from services.sudoku_service import (
    SudokuService,
    InvalidCredentialsError,
    UsernameExistsError
)


class FakeUserRepository:
    def __init__(self):
        self.users = []

    def find_user(self, username):
        for user in self.users:
            if user[0] == username:
                return user

        return None

    def get_password(self, username):
        for user in self.users:
            if user[0] == username:
                return user[1]
        return None

    def find_all(self):
        return self.users

    def create_user(self, user):
        hash_password = generate_password_hash(user.password)

        self.users.append((user.username, hash_password))

        return user
    
    def get_user_id(self, username):
        return 1

    def delete_all(self):
        self.users = []


class FakeSudokuRepository:
    def __init__(self):
        self.sudokus = []
        self.stats = []

    def get_sudoku_id(self, name):
        return 3
    
    def save_status(self, user_id, sudoku_id):
        self.stats.append((user_id, sudoku_id))

    def get_sudokus(self, level):
        for sudoku in self.sudokus:
            if sudoku[2] == level:
                return sudoku
        return None

    def create_sudoku(self, sudoku):
        self.sudokus.append((sudoku.name, sudoku.puzzle, sudoku.level))

class TestSudokuService(unittest.TestCase):
    def setUp(self):
        self.sudoku_service = SudokuService(
            FakeUserRepository(),
            FakeSudokuRepository()
        )

        self.user_kissa = User("kissa", "kala123")
        self.sudoku_testi = Sudoku(
            "testi", 
            "123456789123456789123456789123456789123456789123456789123456789123456789123456789", 1)

    def login(self, user):
        self.sudoku_service.create_user(user.username, user.password)

    def test_numbers_to_puzzle_works(self):
        puzzle = self.sudoku_service.numbers_to_puzzle(self.sudoku_testi)

        self.assertEqual(len(puzzle), 9)
        self.assertEqual(puzzle[0][0][0], 1)
        self.assertEqual(puzzle[8][8][0], 9)

    def test_login_works_with_valid_username_and_password(self):
        self.sudoku_service.create_user(
            self.user_kissa.username,
            self.user_kissa.password
        )

        user = self.sudoku_service.login(
            self.user_kissa.username,
            self.user_kissa.password
        )

        self.assertEqual(user[0], self.user_kissa.username)

    def test_login_fails_with_invalid_username(self):
        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.sudoku_service.login("kisa", "kala123")
        )

    def test_register_with_existing_username_fails(self):
        username = self.user_kissa.username

        self.sudoku_service.create_user(username, "paraskala")
        self.assertRaises(
            UsernameExistsError,
            lambda: self.sudoku_service.create_user(username, "huonokala")
        )
