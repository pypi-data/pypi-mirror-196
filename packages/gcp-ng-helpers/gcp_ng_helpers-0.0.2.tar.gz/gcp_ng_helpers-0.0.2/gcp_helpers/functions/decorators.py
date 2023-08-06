from functools import wraps
from flask import Request, make_response


def verify_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req: Request | None = args[0]
        if req is not None and not req.is_json:
            return make_response("Bad request", 400)
        else:
            return func(*args, **kwargs)
    return wrapper
