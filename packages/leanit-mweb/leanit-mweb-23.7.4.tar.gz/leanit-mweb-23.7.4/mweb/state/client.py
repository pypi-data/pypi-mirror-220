from __future__ import annotations

import json
import logging
from datetime import timedelta

from jose import jws
from jose.exceptions import JWTError
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response


from mweb.security.jwt import TokenService

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Dict, Union

if TYPE_CHECKING:
    pass

class ClientState(dict):
    secret_key: str = None
    cookie_name: str = None
    ttl: int = None
    _initialized = False

    @classmethod
    def _initialize_class(cls):
        if not cls._initialized:
            from mweb import config
            cls.secret_key = config["mweb"]["secret_key"].encode()
            cls.cookie_name = config["mweb"].get("client_state", {}).get("cookie_name", "c")
            cls.ttl = int(config["mweb"].get("client_state", {}).get("ttl", 60 * 60 * 24 * 7))
            cls._initialized = True

    def __init__(self, **kwargs):
        self._initialize_class()

        super().__init__(**kwargs)

    @classmethod
    def from_request(cls, request: Request):
        cookie_signed = request.cookies.get(cls.cookie_name)
        if not cookie_signed:
            return cls()

        return cls.from_cookie_value(cookie_signed)

    @classmethod
    def from_cookie_value(cls, cookie_value: str) -> ClientState:
        """
        Returns a new ClientState instance from a cookie value.

        @param cookie_value: "eyJhb...zIjoibWV0cmljcy"
        @return:
        """
        cookie_data = cls.unsign(cookie_value)

        state = cls(**cookie_data)
        return state

    @classmethod
    def from_response(cls, response: Response) -> ClientState:
        """
        Returns a new ClientState instance from a Response object.

        @param response:
        @return:
        """
        set_cookie = response.headers.get("Set-Cookie")
        if not set_cookie:
            return cls()
        else:
            return cls.from_set_cookie(set_cookie)

    @classmethod
    def from_set_cookie(cls, set_cookie: str) -> ClientState:
        """
        Returns a new ClientState instance from a Set-Cookie header value.

        @param set_cookie: "c=eyJhb...zIjoibWV0cmljcy; Path=/; SameSite=Strict"
        @return:
        """
        cookie_value = set_cookie.split(";")[0].split("=")[1]
        return cls.from_cookie_value(cookie_value)


    @classmethod
    def sign(cls, value: Union[Dict, str]) -> str:
        signed = TokenService.get_instance().encode_jwt(value, expires_delta=timedelta(seconds=cls.ttl))
        return signed

    @classmethod
    def unsign(cls, value: str) -> Dict:
        """
        :raises: jose.exceptions.JWSError if the signature is invalid
        :param value:
        :return:
        """
        try:
            return TokenService.get_instance().decode_jwt(value)
        except JWTError as e:
            logger.warning(f"Failed to decode JWT: {e}")
            return {}

    def serialize(self) -> Union[Dict, str]:
        return dict(self)

    def update_http_exception(self, exc: HTTPException) -> HTTPException:
        cookie_value_signed = self.get_cookie_value()

        exc.headers["Set-Cookie"] = f"{self.cookie_name}={cookie_value_signed}; Path=/; SameSite=lax"
        return exc

    def update_response(self, response: Response):
        cookie_value_signed = self.get_cookie_value()

        response.set_cookie(self.cookie_name, cookie_value_signed, max_age=self.ttl - 60)
        return response

    def get_cookie_value(self):
        cookie_value_serialized = self.serialize()
        cookie_value_signed = self.sign(cookie_value_serialized)
        return cookie_value_signed

def cookie_string_to_dict(cookie_string: str) -> dict:
    cookies = {}
    for cookie in cookie_string.split('; '):
        name, value = cookie.split('=', 1)
        cookies[name] = value
    return cookies


class ClientStateMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        cookie_line = [i[1] for i in scope["headers"] if i[0] == b"cookie"]
        if cookie_line:
            cookie_line: bytes = cookie_line[0]
            cookie_line_str = cookie_line.decode()
            cookies = cookie_string_to_dict(cookie_line_str)
            if "c" in cookies:
                scope["state"] = ClientState.from_cookie_value(cookies["c"])

        await self.app(scope, receive, send)