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
            if user[1] == username:
                return user

        return None

    def get_password(self, username):
        for user in self.users:
            if user[1] == username:
                return user[2]
        return None

    def find_all(self):
        return self.users

    def create_user(self, user):
        hash_password = generate_password_hash(user.password)
        id = len(self.users) + 1

        self.users.append((id, user.username, hash_password))

        return user

    def get_user_id(self, username):
        for user in self.users:
            if user[1] == username:
                return user[0]
            
        return None

    def delete_all(self):
        self.users = []


class FakeSudokuRepository:
    def __init__(self):
        self.sudokus = []
        self.stats = []
        self.create_sudoku(Sudoku("vaikea", 123456789, 3))
        self.create_sudoku(Sudoku("hurja", 123, 3))

    def get_sudoku_id(self, name):
        for sudoku in self.sudokus:
            if sudoku[1] == name:
                return sudoku[0]
        return None

    def save_status(self, user_id, sudoku_id):
        self.stats.append((user_id, sudoku_id))

    def get_sudokus(self, level):
        sudokus = []
        for sudoku in self.sudokus:
            if sudoku[3] == level:
                sudokus.append(sudoku)
        return sudokus if sudokus else None

    def create_sudoku(self, sudoku):
        id = len(self.sudokus) + 1
        self.sudokus.append((id, sudoku.name, sudoku.puzzle, sudoku.level))


class TestSudokuService(unittest.TestCase):
    def setUp(self):
        self.sudoku_service = SudokuService(
            FakeUserRepository(),
            FakeSudokuRepository()
        )

        self.user_kissa = User("kissa", "kala123")
        self.user_koira = User("hauva", "hauhau")
        self.sudoku_testi = Sudoku(
            "testi",
            "123456789123456789123456789123456789123456789123456789123456789123456789123456789", 1)
        self.sudoku_helppo = Sudoku(
            "helppo",
            "111111111222222222333333333444444444555555555666666666777777777888888888999999999", 1
        )

    def login(self, user):
        self.sudoku_service.create_user(user.username, user.password)

    def test_get_sudoku_id_works(self):
        sudoku_id = self.sudoku_service.get_sudoku_id(Sudoku("vaikea", 123456789, 3))
        toinen_id = self.sudoku_service.get_sudoku_id(Sudoku("hurja", 123, 3))
        
        self.assertEqual(sudoku_id, 1)
        self.assertEqual(toinen_id, 2)

    def test_get_sudokus_works(self):
        sudokus = self.sudoku_service.get_sudokus(3)
        self.assertEqual(len(sudokus), 2)
        self.assertEqual(sudokus[0][1], "vaikea")
        self.assertEqual(sudokus[1][2], 123)

    def test_numbers_to_puzzle_works(self):
        puzzle = self.sudoku_service.numbers_to_puzzle(self.sudoku_testi)

        self.assertEqual(len(puzzle), 9)
        self.assertEqual(puzzle[0][0][0], 1)
        self.assertEqual(puzzle[8][8][0], 9)

    def test_get_user_id_works(self):
        self.sudoku_service.create_user(
            self.user_kissa.username,
            self.user_kissa.password
        )

        self.sudoku_service.create_user(
            self.user_koira.username,
            self.user_koira.password
        )

        koira_id = self.sudoku_service.get_user_id(self.user_koira)

        self.assertEqual(koira_id, 2)

    def test_login_works_with_valid_username_and_password(self):
        self.sudoku_service.create_user(
            self.user_kissa.username,
            self.user_kissa.password
        )

        user = self.sudoku_service.login(
            self.user_kissa.username,
            self.user_kissa.password
        )

        self.assertEqual(user[1], self.user_kissa.username)

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
