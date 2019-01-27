from dataclasses import dataclass


@dataclass
class UserDevice:
    user_id: int
    device_id: str
    device_name: str
    active: bool
