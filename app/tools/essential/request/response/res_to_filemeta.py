
from aiohttp import ClientResponse

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError
from app.tools.essential.request.response.types.file_meta import FileMeta


async def res_to_filemeta(
        res: ClientResponse,
) -> FileMeta:
    if not res.ok:
        text = await res.text()
        raise RemoteServiceError(
            status=res.status,
            message=text,
        )
    filemeta = FileMeta(
        name=get_filename(res),
        type=get_filetype(res),
        size=get_filesize(res),
    )
    return filemeta

def get_filename(
        res: ClientResponse,
) -> str | None:
    content_disposition = res.content_disposition
    if content_disposition is not None:
        filename = content_disposition.filename
    else:
        filename = None
    return filename

def get_filetype(
        res: ClientResponse,
) -> str | None:
    content_disposition = res.content_disposition
    if content_disposition is not None:
        filetype = content_disposition.type
    else:
        filetype = None
    return filetype

def get_filesize(
        res: ClientResponse,
) -> int | None:
    filesize = res.content_length
    return filesize
