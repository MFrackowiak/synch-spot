from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict


class AuthProviders(Enum):
    SPOTIFY = "sptf"


@dataclass
class User:
    username: str
    email: str = ""
    password: str = ""
    id: Optional[int] = field(default=None)


@dataclass
class UserAuth:
    provider: AuthProviders
    access_token: str
    expires: datetime
    refresh_token: Optional[str]
    token_type: str = "Bearer"
    details: Optional[Dict] = None
