from sanic import Blueprint
from sanic.response import redirect
from sanic.views import HTTPMethodView

from rpg_music.users.service import UserService
from rpg_music.web.jinja import jinja

auth_blueprint = Blueprint("auth", url_prefix="auth")


class LoginView(HTTPMethodView):
    def __init__(self, *args, **kwargs):
        self.services = {}
        super().__init__(*args, **kwargs)

    @property
    def user_service(self) -> UserService:
        if "user" not in self.services:
            self.services["user"] = UserService()
        return self.services["user"]

    @jinja.template("login.html")
    async def get(self, request):
        return {}

    @jinja.template("login.html")
    async def post(self, request):
        user = await self.user_service.authenticate_user(
            request.form.get("username"), request.form.get("password")
        )
        if user:
            request["session"]["user_id"] = user.id
            spotify_auth = await self.user_service.get_spotify_auth(user.id)
            if not spotify_auth:
                return redirect(request.app.url_for("spotify.auth"))
            else:
                return redirect(request.app.url_for("spotify.devices"))
        return {"error": "Authentication failed."}


@auth_blueprint.route("/register", name="register", methods=["POST"])
async def register(request):
    user = await UserService().create_user(
        request.form.get("username"),
        request.form.get("password"),
        request.form.get("email", ""),
    )
    if user:
        request["session"]["user_id"] = user.id
        return redirect(request.app.url_for("spotify.auth"))
    return {"error": "Authentication failed."}


auth_blueprint.add_route(LoginView.as_view(), "/login", "login")
