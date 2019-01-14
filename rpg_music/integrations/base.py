import ujson
from typing import Optional

from aiohttp import ClientSession


class AsyncAPIClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None

    async def init(self):
        self.session = ClientSession(json_serialize=ujson.dumps)

    async def post(self, *args, **kwargs):
        if not self.session:
            await self.init()
        return await self.session.post(*args, **kwargs)

    async def get(self, *args, **kwargs):
        if not self.session:
            await self.init()
        return await self.session.get(*args, **kwargs)

    async def close_session(self):
        if self.session:
            await self.session.close()
