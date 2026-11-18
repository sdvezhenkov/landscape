from aiohttp import ClientResponse

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError


async def res_to_error(
        res: ClientResponse,
) -> None:
    if not res.ok:
        text = await res.text()
        raise RemoteServiceError(
            status=res.status,
            message=text,
        )
