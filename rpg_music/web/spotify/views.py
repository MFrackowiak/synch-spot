from urllib.parse import urlencode

from sanic import Blueprint
from sanic.response import redirect, json

import app_config
from rpg_music.integrations.spotify.client import SpotifyAPIClient, SpotifyScope

spotify_blueprint = Blueprint("spotify", url_prefix="spotify")
api_client = SpotifyAPIClient(
    app_config.spotify_client_id, app_config.spotify_client_secret
)


@spotify_blueprint.route("/auth", name="auth")
async def spotify_auth(request):
    state = "test-1234"
    auth_request = api_client.get_auth_params(
        f"{app_config.http_host}{request.app.url_for('spotify.finish-auth')}",
        [SpotifyScope.MODIFY_PLAYBACK],
        state,
    )
    return redirect(f"{auth_request['url']}?{urlencode(auth_request['params'])}")


@spotify_blueprint.route("/auth/finish", name="finish-auth")
async def spotify_finish_auth(request):
    spotify_auth = await api_client.complete_auth(
        redirect_uri=f"{app_config.http_host}{request.app.url_for('spotify.finish-auth')}",
        code=request.raw_args["code"],
    )
    return json({"status": "fuck_yeah"})


@spotify_blueprint.listener("after_server_stop")
async def close_session(app, loop):
    await api_client.close_session()
