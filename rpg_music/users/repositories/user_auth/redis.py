from typing import Optional, List

from rpg_music.common.redis import RedisBase
from rpg_music.users.models import User, AuthProviders, UserAuth
from rpg_music.users.repositories.user_auth.base import BaseUserAuthRepository


class RedisUserAuthRepository(RedisBase, BaseUserAuthRepository):
    auth_keys = "user/auth/{id}"

    def save_user_auth(self, user_id: int, user_auth: UserAuth) -> UserAuth:
        self.redis.hset(self.auth_keys.format(id=user_id), user_auth.provider.value)

    def get_auth_for_user(self, user_id: int) -> List[UserAuth]:
        pass

    def get_auth_for_user_and_provider(
        self, user_id: int, provider: AuthProviders
    ) -> Optional[AuthProviders]:
        pass
