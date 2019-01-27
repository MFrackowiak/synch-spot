from dataclasses import asdict
from typing import Optional, List

from rpg_music.common.redis import RedisBase
from rpg_music.music.models import UserDevice
from rpg_music.music.repositories.base import BaseDeviceRepository


class RedisDeviceRepository(RedisBase, BaseDeviceRepository):
    user_device_key = "user/devices/{id}"

    async def save_user_device(
        self, user_id: int, user_device: UserDevice
    ) -> UserDevice:
        await self.redis.rpush(
            self.user_device_key.format(id=user_id), self.to_json(asdict(user_device))
        )
        return user_device

    async def save_user_devices(
        self, user_id: int, user_devices: List[UserDevice]
    ) -> List[UserDevice]:
        await self.redis.delete(self.user_device_key.format(id=user_id))
        await self.redis.rpush(
            self.user_device_key.format(id=user_id),
            *map(self.to_json, map(asdict, user_devices))
        )
        return user_devices

    async def get_user_devices(self, user_id: int) -> List[UserDevice]:
        devices = await self.redis.lrange(
            self.user_device_key.format(id=user_id), 0, -1
        )
        return [UserDevice(**self.from_json(payload)) for payload in devices]

    async def get_user_active_device(self, user_id: int) -> Optional[UserDevice]:
        devices = await self.get_user_devices(user_id)
        return next((device for device in devices if device.active), None)

    async def set_user_active_device(
        self, user_id: int, device_id: str
    ) -> Optional[UserDevice]:
        devices = await self.get_user_devices(user_id)
        active_device = None
        for device in devices:
            if device.device_id == device_id:
                device.active = True
                active_device = device
            else:
                device.active = False
        await self.save_user_devices(user_id, devices)
        return active_device
