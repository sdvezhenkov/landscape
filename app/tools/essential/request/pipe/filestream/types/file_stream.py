from collections.abc import AsyncIterator
from dataclasses import dataclass

from app.tools.essential.request.response.types.file_meta import FileMeta


@dataclass(frozen=True, slots=True)
class FileStream:
    stream: AsyncIterator[bytes]
    meta: FileMeta
