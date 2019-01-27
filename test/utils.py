import asyncio
from unittest import mock
from unittest.mock import patch, Mock

from redis import Redis

from rpg_music.common.redis import RedisPool


def run_sync(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def AsyncMock(*args, **kwargs):
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


class RedisTestCaseMixin:
    def setUp(self):
        super().setUp()
        self.config_patch = patch(
            "rpg_music.common.redis.app_config",
            Mock(redis_url="redis://localhost:6379/1"),
        )
        self.config_patch.start()
        run_sync(RedisPool.get_pool())

    def tearDown(self):
        super().tearDown()
        self.config_patch.stop()
        Redis(db=1).flushdb()
