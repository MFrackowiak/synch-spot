from datetime import datetime
from unittest import TestCase

from rpg_music.users.models import UserAuth, AuthProviders
from rpg_music.users.repositories.user_auth.redis import RedisUserAuthRepository
from test.utils import RedisTestCaseMixin, run_sync


class UserRedisRepositoryTestCase(RedisTestCaseMixin, TestCase):
    def test_user_auth_and_retrieved(self):
        auth = UserAuth(AuthProviders.SPOTIFY, "test", datetime(2030, 12, 10))
        repo = RedisUserAuthRepository()
        run_sync(repo.save_user_auth(1, auth))
        retrieved = run_sync(
            repo.get_auth_for_user_and_provider(1, AuthProviders.SPOTIFY)
        )
        self.assertEqual(auth, retrieved)

    def test_user_auth_not_found(self):
        auth = UserAuth(AuthProviders.SPOTIFY, "test", datetime(2030, 12, 10))
        repo = RedisUserAuthRepository()
        run_sync(repo.save_user_auth(1, auth))
        retrieved = run_sync(
            repo.get_auth_for_user_and_provider(1, AuthProviders.GOOGLE)
        )
        self.assertIsNone(retrieved, None)
        retrieved = run_sync(
            repo.get_auth_for_user_and_provider(2, AuthProviders.SPOTIFY)
        )
        self.assertIsNone(retrieved, None)

    def test_save_overwrites(self):
        repo = RedisUserAuthRepository()
        auth_1 = UserAuth(AuthProviders.SPOTIFY, "test", datetime(2030, 12, 10))
        auth_2 = UserAuth(AuthProviders.SPOTIFY, "other", datetime(2028, 12, 10))
        run_sync(repo.save_user_auth(1, auth_1))
        run_sync(repo.save_user_auth(1, auth_2))
        retrieved = run_sync(
            repo.get_auth_for_user_and_provider(1, AuthProviders.SPOTIFY)
        )
        self.assertEqual(auth_2, retrieved)

    def test_retrieve_all_user_auth(self):
        repo = RedisUserAuthRepository()
        auth_1 = UserAuth(AuthProviders.SPOTIFY, "test", datetime(2030, 12, 10))
        auth_2 = UserAuth(AuthProviders.GOOGLE, "other", datetime(2030, 12, 10))
        run_sync(repo.save_user_auth(1, auth_1))
        run_sync(repo.save_user_auth(1, auth_2))

        retrieved = run_sync(repo.get_auth_for_user(1))
        self.assertEqual(retrieved, [auth_1, auth_2])

    def test_retrieve_all_user_auth_none_found(self):
        repo = RedisUserAuthRepository()
        auth_1 = UserAuth(AuthProviders.SPOTIFY, "test", datetime(2030, 12, 10))
        auth_2 = UserAuth(AuthProviders.GOOGLE, "other", datetime(2030, 12, 10))
        run_sync(repo.save_user_auth(1, auth_1))
        run_sync(repo.save_user_auth(1, auth_2))

        retrieved = run_sync(repo.get_auth_for_user(2))
        self.assertEqual(retrieved, [])
