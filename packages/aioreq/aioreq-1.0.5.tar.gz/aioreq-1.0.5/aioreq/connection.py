import asyncio
import logging
import os
import ssl as _ssl
from contextlib import contextmanager
from typing import Awaitable
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

from dns import asyncresolver  # type: ignore

from aioreq.settings import LOGGER_NAME

res = asyncresolver.Resolver()
res.nameservers = ["1.1.1.1", "8.8.8.8"]

log = logging.getLogger(LOGGER_NAME)

context = _ssl.create_default_context()
context.keylog_filename = os.getenv("SSLKEYLOGFILE")  # type: ignore
context.check_hostname = True
context.verify_mode = True  # type: ignore


async def get_address(host):
    answers = await res.resolve(host)
    return answers.rrset[0].address  # type: ignore


dns_cache: Dict[str, Union[str, Awaitable]] = dict()


@contextmanager
def mock_transport(transport):
    transport.used = True
    yield
    transport.used = False


async def resolve_domain(
    url,
) -> Tuple[str, int]:
    hostname = url.ip or ".".join(url.host)

    port = url.port
    ip = url.ip

    if port is None:
        port = 80 if url.scheme == "http" else 443

    if ip is not None:
        return ip, port

    if hostname in dns_cache:
        memo = dns_cache[hostname]
        if isinstance(memo, str):
            return memo, port
        else:
            return await memo, port

    log.trace(f"trying resolve hostname={hostname}")  # type: ignore
    coro = asyncio.create_task(get_address(hostname))
    dns_cache[hostname] = coro
    ip = await coro
    dns_cache[hostname] = ip
    return ip, port


class Transport:
    def __init__(self):
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.used: bool = False

    async def _send_data(self, raw_data: bytes) -> None:
        assert self.writer
        self.writer.write(raw_data)
        await self.writer.drain()

    async def make_connection(
        self, ip: str, port: int, ssl: bool, server_hostname
    ) -> None:
        log.trace(f"{ip}, {port}")  # type: ignore
        reader, writer = await asyncio.open_connection(
            host=ip,
            port=port,
            ssl=context if ssl else None,
            server_hostname=server_hostname,
        )
        self.reader = reader
        self.writer = writer

    async def send_http_request(self, raw_data: bytes):
        with mock_transport(self):
            await self._send_data(raw_data)
            from aioreq import ResponseParser

            assert self.reader
            status_line = await self.reader.readuntil(b"\r\n")
            status_line = status_line.decode()  # type: ignore
            headers_line = await self.reader.readuntil(b"\r\n\r\n")
            headers_line = headers_line.decode()  # type: ignore
            content_length = ResponseParser.search_content_length(headers_line)
            content = b""

            if content_length is not None:
                content = await self.reader.readexactly(content_length)
            elif ResponseParser.search_transfer_encoding(headers_line):
                while True:
                    chunk = await self.reader.readuntil(b"\r\n")
                    chunk_size = chunk[:-2]
                    if b";" in chunk_size:
                        chunk_size = chunk_size.split(b";")[0].strip()
                    chunk_size = int(chunk_size, 16)  # type: ignore
                    if chunk_size == 0:
                        break
                    data = await self.reader.readexactly(chunk_size)  # type: ignore
                    await self.reader.readexactly(2)  # crlf
                    content += data
            return status_line, headers_line, content

    async def send_http_stream_request(self, raw_data: bytes):
        from aioreq import ResponseParser

        with mock_transport(self):
            await self._send_data(raw_data)
            assert self.reader
            status_line = await self.reader.readuntil(b"\r\n")
            status_line = status_line.decode()  # type: ignore
            headers_line = await self.reader.readuntil(b"\r\n\r\n")
            headers_line = headers_line.decode()  # type: ignore
            content_length = ResponseParser.search_content_length(headers_line)

            yield status_line, headers_line
            if content_length is not None:
                raise TypeError("Stream request should use chunked")
            else:
                while True:
                    chunk = await self.reader.readuntil(b"\r\n")
                    chunk_size = chunk[:-2]

                    chunk_size = int(chunk_size, 16)  # type: ignore
                    if chunk_size == 0:
                        break
                    data = await self.reader.readexactly(chunk_size)  # type: ignore
                    await self.reader.readexactly(2)  # crlf
                    yield data

    def is_closing(self) -> bool:
        """
        Wraps transport is_closing
        """
        if self.writer:
            return self.writer.is_closing()
        raise TypeError("`is_closing` method called on unconnected transport")

    def __repr__(self):
        return f"<Transport {'Closed' if self.is_closing() else 'Open'}>"
