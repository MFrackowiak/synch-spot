from abc import abstractmethod, ABC
from typing import List, Optional

from rpg_music.users.models import UserAuth, User, AuthProviders


class BaseUserAuthRepository(ABC):
    @abstractmethod
    async def save_user_auth(self, user_id: int, user_auth: UserAuth) -> UserAuth:
        pass

    @abstractmethod
    async def get_auth_for_user(self, user_id: int) -> List[UserAuth]:
        pass

    @abstractmethod
    async def get_auth_for_user_and_provider(
        self, user_id: int, provider: AuthProviders
    ) -> Optional[UserAuth]:
        pass
