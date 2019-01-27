from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict

from aiohttp import BasicAuth

from rpg_music.integrations.base import AsyncAPIClient


class SpotifyScope(Enum):
    MODIFY_PLAYBACK = "user-modify-playback-state"


@dataclass
class SpotifyAuth:
    access_token: str
    expires_in: int
    refresh_token: str
    scope: List[SpotifyScope]
    token_type: str


class SpotifyClientError(Exception):
    pass


@dataclass
class SpotifyDevice:
    device_id: str
    name: str
    active: bool


class SpotifyAPIClient(AsyncAPIClient):
    BASE = "https://accounts.spotify.com"
    API = "https://api.spotify.com/v1"

    def __init__(self, client_id: str, client_secret: str):
        super().__init__()
        self._client_id: str = client_id
        self._client_secret: str = client_secret

    def get_auth_params(
        self, redirect_uri: str, scopes: List[SpotifyScope], state: Optional[str] = None
    ) -> Dict[str, str]:
        params = {
            "redirect_uri": redirect_uri,
            "scope": ",".join(scope.value for scope in scopes),
            "response_type": "code",
            "client_id": self._client_id,
        }

        if state is not None:
            params["state"] = state

        return {"url": f"{self.BASE}/authorize", "params": params}

    async def complete_auth(self, redirect_uri: str, code: str) -> SpotifyAuth:
        response = await self.post(
            f"{self.BASE}/api/token",
            data={
                "redirect_uri": redirect_uri,
                "code": code,
                "grant_type": "authorization_code",
            },
            auth=BasicAuth(self._client_id, self._client_secret),
        )
        response_content = await response.json()

        if response.status != 200:
            print(response_content)
            raise SpotifyClientError()

        return SpotifyAuth(
            scope=[
                SpotifyScope(scope)
                for scope in response_content.pop("scope", "").split(",")
            ],
            **response_content,
        )

    async def refresh_token(self, refresh_token: str):
        response = await self.post(
            f"{self.BASE}/api/token",
            data={"refresh_token": refresh_token, "grant_type": "refresh_token"},
            auth=BasicAuth(self._client_id, self._client_secret),
        )

        if response.status_code != 200:
            raise SpotifyClientError()

        response_content = response.json()
        return SpotifyAuth(
            scope=[
                SpotifyScope(scope)
                for scope in response_content.pop("scope", "").split(",")
            ],
            **response_content,
            refresh_token=refresh_token,
        )

    async def get_devices_list(self, user_token: str) -> List[SpotifyDevice]:
        response = await self.session.get(
            f"{self.API}/me/player/devices",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        return [
            SpotifyDevice(
                device_id=device["id"], active=device["is_active"], name=device["name"]
            )
            for device in response.json()["devices"]
        ]

    async def get_track_info(self, track_id: str) -> Dict:
        pass

    async def play_track(self, user_token: str, track_id: str):
        pass

    async def queue_track(self, user_token: str, *tracks):
        pass
