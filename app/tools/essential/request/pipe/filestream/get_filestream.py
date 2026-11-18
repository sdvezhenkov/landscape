from collections.abc import AsyncIterator

from aiohttp import ClientSession

from app.tools.essential.request.pipe.filestream.types.file_stream import FileStream
from app.tools.essential.request.response.res_to_chunks import DEFAULT_CHUNK_SIZE, res_to_chunks
from app.tools.essential.request.response.res_to_filemeta import res_to_filemeta


async def get_filestream(
        session: ClientSession,
        url: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> FileStream:
    async def stream() -> AsyncIterator[bytes]:
        async with session.get(url) as res:
            async for chunk in res_to_chunks(res, chunk_size):
                yield chunk

    async with session.head(url) as res:
        meta = await res_to_filemeta(res)

    filestream = FileStream(
        stream=stream(),
        meta=meta,
    )
    return filestream
