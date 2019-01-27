from sanic import Sanic
from sanic_session import Session, AIORedisSessionInterface

from rpg_music.common.redis import RedisPool
from rpg_music.common.sessions import SessionManager
from rpg_music.web.auth.views import auth_blueprint
from rpg_music.web.jinja import jinja
from rpg_music.web.spotify.views import spotify_blueprint

app = Sanic("rpg_music")
app.blueprint(spotify_blueprint)
app.blueprint(auth_blueprint)

session = Session()


@app.listener("before_server_start")
async def server_init(app, loop):
    app.redis = await RedisPool.get_pool()
    session.init_app(app, interface=AIORedisSessionInterface(app.redis))


@app.listener("after_server_stop")
async def close_sessions(app, loop):
    await SessionManager().close_sessions()


jinja.init_app(app)
