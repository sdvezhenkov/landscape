import json
from collections.abc import AsyncIterator
from typing import cast

from aiohttp import ClientResponse


class FakeResponse:
    def __init__(
            self,
            status: int,
            payload: bytes,
    ):
        self.status = status
        self.content = FakeContent(payload)

    @property
    def ok(self) -> bool:
        return self.status < 400

    async def text(self) -> str:
        return self.content.payload.decode()

    async def json(self) -> str:
        return json.loads(self.content.payload.decode())


class FakeContent:
    def __init__(
            self,
            payload: bytes,
    ):
        self.payload: bytes = payload

    async def iter_chunked(
            self,
            _: int,
    ) -> AsyncIterator[bytes]:
        yield self.payload


class FakeFileResponse(FakeResponse):
    def __init__(
            self,
            status: int,
            payload: bytes,
            content_disposition: FakeContentDisposition | None,
    ):
        super().__init__(status, payload)
        self.content_disposition = content_disposition
        self.content_length: int = len(payload)




class FakeContentDisposition:
    def __init__(
            self,
            filename: str | None,
            filetype: str | None,
    ):
        self.filename = filename
        self.type = filetype


def get_fake_response(
        status: int,
        payload: bytes,
) -> ClientResponse:
    res = FakeResponse(status, payload)
    res = cast(ClientResponse, cast(object, res))
    return res

def get_fake_file_response(
        status: int,
        payload: bytes,
        content_disposition: FakeContentDisposition | None,
) -> ClientResponse:
    res = FakeFileResponse(status, payload, content_disposition)
    res = cast(ClientResponse, cast(object, res))
    return res
