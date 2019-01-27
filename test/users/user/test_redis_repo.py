from unittest import TestCase

from rpg_music.users.models import User
from rpg_music.users.repositories.user.redis import RedisUserRepository
from test.utils import run_sync, RedisTestCaseMixin


class UserRedisRepositoryTestCase(RedisTestCaseMixin, TestCase):
    def test_user_saved_with_id(self):
        user = User("testowy", "test@test.co")
        repo = RedisUserRepository()
        user = run_sync(repo.save_user(user))
        self.assertIsNotNone(user.id)

    def test_user_retrieved_by_id(self):
        user = User("testowy", "test@test.co")
        repo = RedisUserRepository()
        user = run_sync(repo.save_user(user))
        retrieved_user = run_sync(repo.get_user_by_id(user.id))
        self.assertEqual(user.id, retrieved_user.id)
        self.assertEqual(user.username, retrieved_user.username)
        self.assertEqual(user.email, retrieved_user.email)

    def test_user_not_found_by_id(self):
        user = User("testowy", "test@test.co")
        repo = RedisUserRepository()
        user = run_sync(repo.save_user(user))
        retrieved_user = run_sync(repo.get_user_by_id(user.id + 1))
        self.assertIsNone(retrieved_user)

    def test_user_retrieved_by_username(self):
        user = User("testowy", "test@test.co")
        repo = RedisUserRepository()
        user = run_sync(repo.save_user(user))
        retrieved_user = run_sync(repo.get_user_by_username(user.username))
        self.assertEqual(user.id, retrieved_user.id)
        self.assertEqual(user.username, retrieved_user.username)
        self.assertEqual(user.email, retrieved_user.email)

    def test_user_not_found_by_username(self):
        user = User("testowy", "test@test.co")
        repo = RedisUserRepository()
        run_sync(repo.save_user(user))
        retrieved_user = run_sync(repo.get_user_by_username("xd"))
        self.assertIsNone(retrieved_user)

    def test_user_retrieved_passes_password_validation(self):
        user = User("testowy", "test@test.co")
        user.set_password("ocietrudnehaslo")
        repo = RedisUserRepository()
        user = run_sync(repo.save_user(user))
        retrieved_user = run_sync(repo.get_user_by_username(user.username))
        self.assertTrue(retrieved_user.check_password("ocietrudnehaslo"))
