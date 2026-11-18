from collections.abc import AsyncIterator

from app.tools.essential.request.pipe.filestream.types.file_stream import FileStream
from app.tools.essential.request.response.types.file_meta import FileMeta


class ExampleError(Exception):
    pass


TEST_MESSAGE: list[bytes] = [
    b'test', b'message', b'1',
    b'test', b'message', b'2',
]
TEST_NAME = 'test'
TEST_TYPE = None
TEST_SIZE = None

async def get_stream(
        error: Exception | None,
) -> AsyncIterator[bytes]:
    for chunk in TEST_MESSAGE:
        yield chunk
    if error is not None:
        raise error

async def get_source(
        error: Exception | None,
) -> FileStream:
    source = FileStream(
        stream=get_stream(error),
        meta=FileMeta(name=TEST_NAME, type=TEST_TYPE, size=TEST_SIZE),
    )
    return source

async def get_target(
        file: FileStream,
        error: Exception | None,
) -> list[bytes]:
    message: list[bytes] = []
    async for chunk in file.stream:
        message.append(chunk)
    if error is not None:
        raise error
    return message
