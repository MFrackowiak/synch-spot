from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

from passlib.handlers.pbkdf2 import pbkdf2_sha256

import app_config


class AuthProviders(Enum):
    SPOTIFY = "sptf"
    FACEBOOK = "fcb"
    GOOGLE = "google"


@dataclass
class User:
    username: str
    email: str = ""
    password: str = ""
    id: Optional[int] = field(default=None)

    def set_password(self, raw_password: str):
        self.password = pbkdf2_sha256.hash(
            raw_password, salt=app_config.salt.encode("ascii")
        )

    def check_password(self, password: str) -> bool:
        return (
            pbkdf2_sha256.hash(password, salt=app_config.salt.encode("ascii"))
            == self.password
        )


@dataclass
class UserAuth:
    provider: AuthProviders
    access_token: str
    expires: datetime
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    details: Optional[Dict] = None
