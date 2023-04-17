import unittest
from entities.user import User
from repositories.user_repository import user_repo


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        user_repo.delete_all_users()
        self.user_avokado = User("avokado", "luumu666")
        self.user_kananmuna = User("kananmuna", "monni123")

    def test_create_user(self):
        user_repo.create_user(self.user_avokado)
        users = user_repo.find_all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, self.user_avokado.username)

    def test_passwords_not_saved_as_strings(self):
        user_repo.create_user(self.user_kananmuna)

        password = user_repo.check_password(self.user_kananmuna.username)
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
