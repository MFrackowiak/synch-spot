from abc import ABC, abstractmethod

from rpg_music.users.models import User


class BaseUserRepository(ABC):
    @abstractmethod
    def save_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        pass
