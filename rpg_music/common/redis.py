import json
from asyncio import get_event_loop
from typing import Dict, Union

from aioredis import Redis, create_redis, create_redis_pool

import app_config


class RedisPool:
    """
    A simple wrapper class that allows you to share a connection
    pool across your application.
    """

    _pool = None

    @classmethod
    async def get_pool(cls, loop=None):
        if not cls._pool:
            cls._pool = await create_redis_pool(
                app_config.redis_url,
                minsize=5,
                maxsize=10,
                loop=loop or get_event_loop(),
            )
        return cls._pool

    @classmethod
    def get_created_pool(cls):
        return cls._pool


class RedisBase:
    def __init__(self, loop=None):
        self.redis: Redis = RedisPool.get_created_pool()
        self.loop = loop

    async def init(self):
        self.redis = await create_redis(
            "redis://localhost", loop=self.loop or get_event_loop(), encoding="utf-8"
        )

    def to_json(self, data: Dict) -> str:
        return json.dumps(data)

    def from_json(self, data: Union[str, bytes]) -> Dict:
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        return json.loads(data)
