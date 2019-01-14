import json
from dataclasses import asdict
from typing import Optional

from rpg_music.common.redis import RedisBase
from rpg_music.users.models import User
from rpg_music.users.repositories.user.base import BaseUserRepository


class RedisUserRepository(RedisBase, BaseUserRepository):
    user_id_key = "user/id"
    user_storage = "user/storage/{id}"
    user_name_hash = "user/name_map"

    async def save_user(self, user: User) -> User:
        if not user.id:
            user.id = await self.redis.incr(self.user_id_key)
        await self.redis.set(
            self.user_storage.format(id=user.id), json.dumps(asdict(user))
        )
        await self.redis.hset(self.user_name_hash, user.username, user.id)
        # todo integrity post modification!
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user_raw_data = await self.redis.get(self.user_storage.format(id=user_id))
        if not user_raw_data:
            return None
        return User(**json.loads(user_raw_data))

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user_id = self.redis.hget(self.user_name_hash, username)
        if not user_id:
            return None
        return await self.get_user_by_id(user_id)
