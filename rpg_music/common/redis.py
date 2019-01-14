from asyncio import get_event_loop

from aioredis import Redis, create_redis


class RedisBase:
    def __init__(self, loop=None):
        self.redis: Redis = None
        self.loop = loop

    async def init(self):
        self.redis = await create_redis(
            "redis://localhost", loop=self.loop or get_event_loop(), encoding="utf-8"
        )
