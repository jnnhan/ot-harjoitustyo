from collections import defaultdict
import unittest
from entities.user import User
from entities.sudoku import Sudoku
from services.user_service import (
    UserService,
    InvalidCredentialsError,
    UsernameExistsError
)


class FakeUserRepository:
    def __init__(self, users=None):
        self.users = users or []
        self.stats = defaultdict(list)

    def find_user(self, username):
        for user in self.users:
            if user[1] == username:
                return User(user[1], user[2])

        return None

    def save_status(self, user_id, sudoku_id):
        for stat in self.stats[str(user_id)]:
            if stat[0] == sudoku_id:
                stat[1] += 1
                return
        self.stats[str(user_id)].append([sudoku_id, 1])

    def get_playtime(self, user_id, sudoku_id):
        playtime = 0

        for stat in self.stats[str(user_id)]:
            if stat[0] == sudoku_id:
                return stat[1]
        return playtime

    def get_user_playtime(self, user_id):
        playtime = 0

        for stat in self.stats[str(user_id)]:
            playtime += stat[1]
        return playtime

    def get_password(self, username):
        for user in self.users:
            if user[1] == username:
                return user[2]
        return None

    def find_all(self):
        return self.users

    def create_user(self, user, hash_password):
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


class FakeSudokuService:
    def __init__(self):
        self.sudoku = None
        self.sudokus = []

    def get_current_sudoku(self):
        return self.sudoku

    def set_current_sudoku(self, sudoku):
        self.sudoku = sudoku
        if self.sudoku not in self.sudokus:
            self.sudokus.append(self.sudoku)

    def get_sudoku_id(self, sudoku):
        return self.sudokus.index(sudoku)


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.fake_sudoku_service = FakeSudokuService()
        self.user_service = UserService(
            FakeUserRepository(),
            self.fake_sudoku_service
        )

        self.user_kissa = User("kissa", "kala123")
        self.user_koira = User("hauva", "hauhau")
        self.sudoku_helppo = Sudoku("helppo", "12345", 1)
        self.sudoku_vaikea = Sudoku("vaikea", "000100", 3)

    def create_user_and_login(self, user):
        self.user_service.create_user(
            user.username,
            user.password
        )

        self.user_service.login(
            user.username,
            user.password
        )

    def test_get_playtime_works(self):
        self.create_user_and_login(self.user_kissa)

        self.fake_sudoku_service.set_current_sudoku(self.sudoku_helppo)
        self.user_service.save_status()
        user_id = self.user_service.get_user_id(self.user_kissa)
        sudoku_id = self.fake_sudoku_service.get_sudoku_id(self.sudoku_helppo)

        playtime = self.user_service.get_playtime(user_id, sudoku_id)

        self.assertEqual(playtime, 1)

        self.fake_sudoku_service.set_current_sudoku(self.sudoku_vaikea)
        self.user_service.save_status()

        playtime = self.user_service.get_playtime(user_id, sudoku_id)

        self.assertEqual(playtime, 1)

    def test_get_user_playtime_works(self):
        self.create_user_and_login(self.user_kissa)

        self.fake_sudoku_service.set_current_sudoku(self.sudoku_helppo)
        self.user_service.save_status()
        playtime = self.user_service.get_user_playtime(self.user_kissa)

        self.assertEqual(playtime, 1)

        self.fake_sudoku_service.set_current_sudoku(self.sudoku_vaikea)
        self.user_service.save_status()
        playtime = self.user_service.get_user_playtime(self.user_kissa)

        self.assertEqual(playtime, 2)

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
        self.create_user_and_login(self.user_kissa)

        user = self.user_service.get_current_user()

        self.assertEqual(user.username, self.user_kissa.username)

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

        self.assertEqual(user.username, self.user_kissa.username)

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
