from sanic import Sanic

from rpg_music.web.spotify.views import spotify_blueprint

app = Sanic("rpg-music")
app.blueprint(spotify_blueprint)
