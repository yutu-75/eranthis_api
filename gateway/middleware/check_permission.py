import functools

from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from jwt import ExpiredSignatureError

from internal.common.error_code.error_code_msg import AuthError


def check_jwt_identity(*roles):
    def outer_jwt(fn):
        @functools.wraps(fn)
        def inner_jwt(*args, **kwargs):
            if request.endpoint != "auth.login":
                try:
                    verify_jwt_in_request()
                except ExpiredSignatureError as e:
                    raise AuthError.NEED_LOGIN
                role = get_jwt_identity().get('role')
                if role not in roles:
                    raise AuthError.NO_PERMISSION

            return fn(*args, **kwargs)

        return inner_jwt

    return outer_jwt
