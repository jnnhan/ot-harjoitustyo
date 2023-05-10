import unittest
from entities.user import User
from entities.sudoku import Sudoku
from repositories.user_repository import user_repo
from repositories.sudoku_repository import sudoku_repo


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        user_repo.delete_all_users()
        sudoku_repo.delete_all_sudokus()
        self.user_avokado = User("avokado", "luumu666")
        self.user_kananmuna = User("kananmuna", "monni123")
        self.user_toinen_avokado = User("avokado", "kala765")
        self.testi_sudoku = Sudoku("testailua", "123456", 1)

    def test_save_status_works(self):
        user_repo.create_user(self.user_avokado)
        sudoku_repo.create_sudoku(self.testi_sudoku)

        user_id = user_repo.get_user_id(self.user_avokado.username)
        sudoku_id = sudoku_repo.get_sudoku_id(self.testi_sudoku.name)

        user_repo.save_status(user_id, sudoku_id)
        playtime = user_repo.get_user_playtime(user_id)

        self.assertEqual(playtime, 1)

        user_repo.save_status(user_id, sudoku_id)
        playtime = user_repo.get_user_playtime(user_id)

        self.assertEqual(playtime, 2)

    def test_create_user(self):
        user_repo.create_user(self.user_avokado)
        users = user_repo.find_all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, self.user_avokado.username)

    def test_passwords_not_saved_as_strings(self):
        user_repo.create_user(self.user_kananmuna)

        password = user_repo.get_password(self.user_kananmuna.username)
        self.assertNotEqual(password, self.user_kananmuna.password)

    def test_find_all_finds_all_users(self):
        user_repo.create_user(self.user_avokado)
        user_repo.create_user(self.user_kananmuna)
        users = user_repo.find_all()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, self.user_avokado.username)
        self.assertEqual(users[1].username, self.user_kananmuna.username)

    def test_find_by_username_works(self):
        user_repo.create_user(self.user_kananmuna)
        user = user_repo.find_user(self.user_kananmuna.username)

        self.assertEqual(user.username, self.user_kananmuna.username)

    def test_get_user_id_works(self):
        user_repo.create_user(self.user_avokado)

        user_id = user_repo.get_user_id(self.user_avokado.username)

        self.assertEqual(user_id, 1)
