from typing import List

from aiohttp import ClientSession

from rpg_music.common.patterns import Singleton


class SessionManager(Singleton):
    def _init(self):
        self.sessions_to_close: List[ClientSession] = []

    def register_session(self, session: ClientSession):
        self.sessions_to_close.append(session)

    async def close_sessions(self):
        for session in self.sessions_to_close:
            await session.close()
