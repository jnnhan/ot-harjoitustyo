from werkzeug.security import generate_password_hash
import unittest
from entities.user import User
from entities.sudoku import Sudoku
from services.user_service import (
    UserService,
    InvalidCredentialsError,
    UsernameExistsError
)
from services.sudoku_service import sudoku_service


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


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService(
            FakeUserRepository()
        )

        self.user_kissa = User("kissa", "kala123")
        self.user_koira = User("hauva", "hauhau")
        self.sudoku_helppo = Sudoku("helppo", "12345", 1)

    def login(self, user):
        self.user_service.create_user(user.username, user.password)

    def test_get_user_id_works(self):
        self.user_service.create_user(
            self.user_kissa.username,
            self.user_kissa.password
        )

        self.user_service.create_user(
            self.user_koira.username,
            self.user_koira.password
        )

        koira_id = self.user_service.get_user_id(self.user_koira)

        self.assertEqual(koira_id, 2)

    def test_get_current_user_works(self):
        self.user_service.create_user(
            self.user_kissa.username,
            self.user_kissa.password
        )

        self.user_service.login(
            self.user_kissa.username,
            self.user_kissa.password
        )

        user = self.user_service.get_current_user()

        self.assertEqual(user[1], self.user_kissa.username)

        self.user_service.logout()

        user = self.user_service.get_current_user()

        self.assertEqual(user, None)

    def test_login_works_with_valid_username_and_password(self):
        self.user_service.create_user(
            self.user_kissa.username,
            self.user_kissa.password
        )

        user = self.user_service.login(
            self.user_kissa.username,
            self.user_kissa.password
        )

        self.assertEqual(user[1], self.user_kissa.username)

    def test_login_fails_with_invalid_password(self):
        self.user_service.create_user(
            self.user_kissa.username,
            self.user_kissa.password
        )

        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.user_service.login(
                self.user_kissa.username,
                "vaarasalasana"
            )
        )

    def test_login_fails_with_invalid_username(self):
        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.user_service.login("kisa", "kala123")
        )

    def test_register_with_invalid_username_and_password(self):
        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.user_service.create_user("ha", "salasana")
        )

        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.user_service.create_user("kissa", "je")
        )

    def test_register_with_existing_username_fails(self):
        username = self.user_kissa.username

        self.user_service.create_user(username, "paraskala")
        self.assertRaises(
            UsernameExistsError,
            lambda: self.user_service.create_user(username, "huonokala")
        )
