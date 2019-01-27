from dataclasses import asdict
from datetime import datetime
from typing import Optional, List, Union

from rpg_music.common.enums import deep_stringify_enums
from rpg_music.common.redis import RedisBase
from rpg_music.users.models import AuthProviders, UserAuth
from rpg_music.users.repositories.user_auth.base import BaseUserAuthRepository


class RedisUserAuthRepository(RedisBase, BaseUserAuthRepository):
    auth_keys = "user/auth/{id}"

    async def save_user_auth(self, user_id: int, user_auth: UserAuth) -> UserAuth:
        await self.redis.hset(
            self.auth_keys.format(id=user_id),
            user_auth.provider.value,
            self._serialize_user_auth(user_auth),
        )
        return user_auth

    async def get_auth_for_user(self, user_id: int) -> List[UserAuth]:
        all_auth_data = await self.redis.hgetall(self.auth_keys.format(id=user_id))
        return [self._deserialize_user_auth(payload) for payload in all_auth_data.values()]

    async def get_auth_for_user_and_provider(
        self, user_id: int, provider: AuthProviders
    ) -> Optional[AuthProviders]:
        auth_payload = await self.redis.hget(
            self.auth_keys.format(id=user_id), provider.value
        )
        return (
            self._deserialize_user_auth(auth_payload) if auth_payload else None
        )

    def _serialize_user_auth(self, user_auth: UserAuth) -> str:
        user_auth_dict = asdict(user_auth)
        user_auth_dict["provider"] = user_auth_dict["provider"].value
        user_auth_dict["details"] = deep_stringify_enums(user_auth_dict["details"])
        user_auth_dict["expires"] = user_auth_dict["expires"].strftime(
            "%Y-%M-%d %H:%m:%S"
        )
        return self.to_json(user_auth_dict)

    def _deserialize_user_auth(self, payload: Union[str, bytes]) -> UserAuth:
        user_auth_dict = self.from_json(payload)
        user_auth_dict["provider"] = AuthProviders(user_auth_dict["provider"])
        user_auth_dict["expires"] = datetime.strptime(
            user_auth_dict["expires"], "%Y-%M-%d %H:%m:%S"
        )
        return UserAuth(**user_auth_dict)
