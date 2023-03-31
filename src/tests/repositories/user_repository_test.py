import unittest
from entities.user import User
from repositories.user_repository import user_repo

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        user_repo.delete_all_users()
        self.user_avokado = User("avokado", "luumu666")

    def test_create_user(self):
        user_repo.create_user(self.user_avokado)
        users = user_repo.find_all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, self.user_avokado.username)
