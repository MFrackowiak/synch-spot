from functools import wraps

from sanic.response import text


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request["session"]:
            return text("Nie")
        return func(request, *args, **kwargs)

    return wrapper
