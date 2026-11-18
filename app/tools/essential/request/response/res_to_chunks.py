from collections.abc import AsyncIterator

from aiohttp import ClientResponse

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError

DEFAULT_CHUNK_SIZE = 1024 * 1024

async def res_to_chunks(
        res: ClientResponse,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> AsyncIterator[bytes]:
    if not res.ok:
        text = await res.text()
        raise RemoteServiceError(
            status=res.status,
            message=text,
        )
    async for chunk in res.content.iter_chunked(chunk_size):
        yield chunk
