from werkzeug.security import check_password_hash, generate_password_hash
import unittest
from entities.user import User
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
    
    def delete_all(self):
        self.users = []


class FakeSudokuRepository:
    def __init__(self):
        self.sudokus = []


class TestSudokuService(unittest.TestCase):
    def setUp(self):
        self.sudoku_service = SudokuService(
            FakeUserRepository(),
            FakeSudokuRepository()
        )

        self.user_kissa = User("kissa", "kala123")

    def login(self, user):
        self.sudoku_service.create_user(user.username, user.password)

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