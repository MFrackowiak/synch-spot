from abc import ABC, abstractmethod
from typing import List, Optional

from rpg_music.music.models import UserDevice


class BaseDeviceRepository(ABC):
    @abstractmethod
    async def save_user_device(
        self, user_id: int, user_device: UserDevice
    ) -> UserDevice:
        pass

    @abstractmethod
    async def save_user_devices(
        self, user_id: int, user_devices: List[UserDevice]
    ) -> List[UserDevice]:
        pass

    @abstractmethod
    async def get_user_devices(self, user_id: int) -> List[UserDevice]:
        pass

    @abstractmethod
    async def get_user_active_device(self, user_id: int) -> Optional[UserDevice]:
        pass

    @abstractmethod
    async def set_user_active_device(
        self, user_id: int, device_id: str
    ) -> Optional[UserDevice]:
        pass
