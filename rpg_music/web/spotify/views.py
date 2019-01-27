from urllib.parse import urlencode

from sanic import Blueprint
from sanic.response import redirect, json

import app_config
from rpg_music.integrations.spotify.client import SpotifyAPIClient, SpotifyScope
from rpg_music.users.service import UserService
from rpg_music.web.decorators import login_required

spotify_blueprint = Blueprint("spotify", url_prefix="spotify")
api_client = SpotifyAPIClient(
    app_config.spotify_client_id, app_config.spotify_client_secret
)


@spotify_blueprint.route("/auth", name="auth")
@login_required
async def spotify_auth(request):
    state = "test-1234"
    auth_request = api_client.get_auth_params(
        f"{app_config.http_host}{request.app.url_for('spotify.finish-auth')}",
        [SpotifyScope.MODIFY_PLAYBACK],
        state,
    )
    return redirect(f"{auth_request['url']}?{urlencode(auth_request['params'])}")


@spotify_blueprint.route("/auth/finish", name="finish-auth")
@login_required
async def spotify_finish_auth(request):
    spotify_auth = await api_client.complete_auth(
        redirect_uri=f"{app_config.http_host}{request.app.url_for('spotify.finish-auth')}",
        code=request.raw_args["code"],
    )
    UserService().save_spotify_auth(request["session"]["user_id"], spotify_auth)
    return redirect(request.app.url_for("spotify.devices"))


@spotify_blueprint.route("/devices", name="devices")
@login_required
async def devices(request):
    spotify_auth = await UserService().get_spotify_auth(request["session"]["user_id"])
    devices = await api_client.get_devices_list(spotify_auth.access_token)
    return json(["WIP"])
