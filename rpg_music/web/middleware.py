from rpg_music.web.app import app


@app.middleware("request")
async def auth_middleware(request):
    pass
