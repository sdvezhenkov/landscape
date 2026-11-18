from aiohttp import ClientResponse
from bs4 import BeautifulSoup

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError


async def res_to_html(
        res: ClientResponse,
) -> BeautifulSoup:
    text = await res.text()
    if not res.ok:
        raise RemoteServiceError(
            status=res.status,
            message=text,
        )
    soup = BeautifulSoup(text, 'html.parser')
    return soup
