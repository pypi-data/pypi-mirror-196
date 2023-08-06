import asyncio
import logging
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Optional
from typing import Tuple
from typing import Union

from aioreq import codes
from aioreq.errors.base import UnexpectedError
from aioreq.errors.requests import RequestTimeoutError
from aioreq.settings import LOGGER_NAME
from aioreq.urls import parse_url

from .auth import parse_auth_header
from .encodings import get_avaliable_encodings
from .headers import AuthenticationWWW
from .headers import ContentEncoding
from .headers import SetCookie
from .headers import TransferEncoding

if TYPE_CHECKING:
    from .http import Client
    from .http import Request
    from .http import Response

log = logging.getLogger(LOGGER_NAME)

default_middlewares = (
    "RetryMiddleWare",
    "RedirectMiddleWare",
    "CookiesMiddleWare",
    "DecodeMiddleWare",
    "AuthenticationMiddleWare",
)


def load_class(name: str):
    if "." not in name:
        return globals()[name]
    components = name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class MiddleWare(ABC):
    def __init__(self, next_middleware: Optional["MiddleWare"]):
        self.next_middleware = next_middleware

    @abstractmethod
    async def process(self, request: "Request", client: "Client"):
        ...

    @staticmethod
    def build(middlewares_: Union[Tuple[Union[str, type], ...]]):
        result = TimeoutMiddleWare(RequestMiddleWare(next_middleware=None))
        for middleware in reversed(middlewares_):
            if isinstance(middleware, str):
                result = load_class(middleware)(next_middleware=result)
            else:
                result = middleware(next_middleware=result)
        return result


class RequestMiddleWare(MiddleWare):
    async def process(self, request: "Request", client: "Client") -> "Response":
        resp = await client.send_request_directly(request)
        return resp


class RedirectMiddleWare(MiddleWare):
    redirect_count = 3

    def __init__(self, *args, **kwargs):
        redirect = kwargs.get("redirect", None)
        if not redirect:
            redirect = self.redirect_count
        self.redirect = max(redirect + 1, 1)
        self.memory = {}
        super().__init__(*args, **kwargs)

    def contains_location(self, response: "Response") -> bool:
        return "location" in response.headers

    async def handle_301(self, request: "Request", response: "Response") -> bool:
        if not self.contains_location(response):
            return False
        new_location = response.headers["location"]
        old_url = str(request.url)

        if not new_location.startswith("http"):
            new_location = request.url.updated_relative_ref(new_location)

        request.url = new_location
        self.memory[old_url] = str(request.url)
        return True

    async def handle_302(self, request: "Request", response: "Response") -> bool:
        if not self.contains_location(response):
            return False
        new_location = response.headers["location"]
        if not new_location.startswith("http"):
            new_location = request.url.updated_relative_ref(new_location)
        request.url = new_location
        return True

    async def handle_303(self, request: "Request", response: "Response") -> bool:
        if not self.contains_location(response):
            return False
        new_location = response.headers["location"]
        if not new_location.startswith("http"):
            new_location = request.url.updated_relative_ref(new_location)

        request.url = parse_url(new_location)
        request.method = "GET"
        request.content = b""
        request.url = new_location
        return True

    async def handle_304(self, request: "Request", response: "Response") -> bool:
        assert True, "304 status code received by the server"
        return True

    async def handle_305(self, request: "Request", response: "Response") -> bool:
        return False

    async def handle_306(self, request: "Request", response: "Response") -> bool:
        return False

    async def handle_307(self, request: "Request", response: "Response") -> bool:
        return await self.handle_302(request, response)

    async def handle_308(self, request: "Request", response: "Response") -> bool:
        return await self.handle_301(request, response)

    async def process(self, request: "Request", client: "Client") -> "Response":
        redirect = self.redirect
        response = None
        redirects = []
        redirect_uri = ""
        while redirect != 0:
            redirect -= 1

            if (
                str(request.url) in self.memory
            ):  # take from the memory if it's permanent redirected
                request.url = self.memory[str(request.url)]
            assert self.next_middleware
            response = await self.next_middleware.process(request, client)
            if redirect_uri:
                redirects.append(redirect_uri)
                response.redirects = redirects

            if (response.status // 100) == 3:
                handler = getattr(self, f"handle_{response.status}", None)

                if handler is None:
                    raise ValueError(
                        f"Handler for {response.status} status code was not implemented"
                    )
                continue_ = await handler(request, response)

                redirect_uri = str(request.url)
                if redirect < 1 or not continue_:
                    return response
            else:
                return response
        assert response is not None
        return response


class DecodeMiddleWare(MiddleWare):
    def decode(self, response: "Response") -> None:
        for parser, header in (
            (TransferEncoding, "transfer-encoding"),
            (ContentEncoding, "content-encoding"),
        ):
            header_content = response.headers.get(header, None)
            if header_content:
                encodings = parser.parse(header_content)

                for encoding in encodings:
                    response.content = encoding.decompress(response.content)

    async def process(self, request: "Request", client: "Client") -> "Response":
        request.headers.add_header(get_avaliable_encodings())
        assert self.next_middleware
        response = await self.next_middleware.process(request, client)
        self.decode(response)
        return response


class RetryMiddleWare(MiddleWare):
    retry_count = 3

    def __init__(self, *args, **kwargs):
        self.retry_count = max(self.retry_count + 1, 1)
        super().__init__(*args, **kwargs)

    async def process(self, request: "Request", client: "Client") -> "Response":
        retry_count = self.retry_count
        response = None
        while retry_count != -1:
            retry_count -= 1
            try:
                assert self.next_middleware
                response = await self.next_middleware.process(request, client)
                break
            except Exception as e:
                if isinstance(e, UnexpectedError):
                    raise e
                if retry_count == -1:
                    raise e
        assert response
        return response


class AuthenticationMiddleWare(MiddleWare):
    async def process(self, request: "Request", client: "Client") -> "Response":
        assert self.next_middleware
        resp = await self.next_middleware.process(request, client)
        if request.auth:
            if resp.status != codes.UNAUTHORIZED:
                return resp
            if "www-authenticate" not in resp.headers:
                raise ValueError(
                    (
                        f"{codes.UNAUTHORIZED} status code received"
                        f" without `www-authenticate` header"
                    )
                )
            header_obj = AuthenticationWWW.parse(resp.headers["www-authenticate"])
            for authentication_header in parse_auth_header(header_obj, request, resp):
                request.headers["authorization"] = authentication_header
                assert self.next_middleware
                resp = await self.next_middleware.process(request, client)
                if resp.status != codes.UNAUTHORIZED:
                    break
        return resp


class TimeoutMiddleWare(MiddleWare):
    async def process(self, request: "Request", client: "Client") -> "Response":
        try:
            assert self.next_middleware
            return await asyncio.wait_for(
                self.next_middleware.process(request, client),
                timeout=request.timeout or client.timeout,
            )
        except asyncio.TimeoutError:
            raise RequestTimeoutError from None


class CookiesMiddleWare(MiddleWare):
    async def process(self, request: "Request", client: "Client") -> "Response":
        cookies = client.cookies.get_raw_cookies(request.url)
        if cookies:
            request.headers["cookie"] = cookies
        assert self.next_middleware
        resp = await self.next_middleware.process(request, client)

        if "set-cookie" in resp.headers:
            cookies = [
                SetCookie().parse(cookie_value, request.url)
                for cookie_value in resp.headers["set-cookie"]
            ]
            for cookie in cookies:
                if cookie is not None:  # SetCookie returns `None` if cookie is invalid
                    client.cookies.add_cookie(cookie)
        return resp
