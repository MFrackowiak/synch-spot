from datetime import datetime, timedelta
from typing import Optional

from rpg_music.integrations.spotify.client import SpotifyAuth
from rpg_music.users.models import UserAuth, AuthProviders, User
from rpg_music.users.repositories.user.base import BaseUserRepository
from rpg_music.users.repositories.user.redis import RedisUserRepository
from rpg_music.users.repositories.user_auth.base import BaseUserAuthRepository
from rpg_music.users.repositories.user_auth.redis import RedisUserAuthRepository


class UserService:
    def __init__(
        self,
        user_repository: BaseUserRepository = None,
        user_auth_repository: BaseUserAuthRepository = None,
    ):
        self.user_repository = user_repository or RedisUserRepository()
        self.user_auth_repository = user_auth_repository or RedisUserAuthRepository()

    async def save_spotify_auth(
        self, user_id: int, spotify_auth: SpotifyAuth
    ) -> UserAuth:
        user_auth = UserAuth(
            provider=AuthProviders.SPOTIFY,
            access_token=spotify_auth.access_token,
            expires=datetime.now() + timedelta(seconds=spotify_auth.expires_in),
            refresh_token=spotify_auth.refresh_token,
            token_type=spotify_auth.token_type,
            details={"scopes": spotify_auth.scope},
        )
        return await self.user_auth_repository.save_user_auth(user_id, user_auth)

    async def get_spotify_auth(self, user_id: int) -> Optional[UserAuth]:
        return await self.user_auth_repository.get_auth_for_user_and_provider(
            user_id, AuthProviders.SPOTIFY
        )

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None

    async def create_user(self, username: str, password: str, email: str):
        user = User(username=username, email=email)
        user.set_password(password)
        user = await self.user_repository.save_user(user)
        return user
