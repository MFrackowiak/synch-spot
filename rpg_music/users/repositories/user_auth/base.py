from abc import abstractmethod, ABC
from typing import List, Optional

from rpg_music.users.models import UserAuth, User, AuthProviders


class BaseUserAuthRepository(ABC):
    @abstractmethod
    def save_user_auth(self, user_id: int, user_auth: UserAuth) -> UserAuth:
        pass

    @abstractmethod
    def get_auth_for_user(self, user_id: int) -> List[UserAuth]:
        pass

    @abstractmethod
    def get_auth_for_user_and_provider(
        self, user: User, provider: AuthProviders
    ) -> Optional[AuthProviders]:
        pass
