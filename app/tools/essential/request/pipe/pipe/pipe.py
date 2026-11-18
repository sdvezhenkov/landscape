from asyncio import Queue, Task, create_task, gather
from collections.abc import AsyncIterator, Awaitable, Callable, Coroutine
from typing import Any, cast

from app.tools.essential.request.pipe.filestream.types.file_stream import FileStream
from app.tools.essential.request.pipe.pipe.errors.source_pipe_error import SourcePipeError
from app.tools.essential.request.pipe.pipe.errors.target_pipe_error import TargetPipeError

PIPE_EOF = object()

async def pipe[T](
        source: Callable[[], Awaitable[FileStream]],
        target: Callable[[FileStream], Coroutine[Any, Any, T]],
        queue_maxsize: int = 8,
) -> T:
    file = await source()
    queue = Queue[bytes | object](maxsize=queue_maxsize)

    async def source_to_queue() -> None:
        try:
            async for chunk in file.stream:
                await queue.put(chunk)
            await queue.put(PIPE_EOF)
        except Exception as e:
            raise SourcePipeError from e

    async def read_from_queue() -> AsyncIterator[bytes]:
        while True:
            item = await queue.get()
            if item is PIPE_EOF:
                return
            chunk = cast(bytes, item)
            yield chunk

    async def target_from_queue() -> T:
        try:
            piped_file = FileStream(
                stream=read_from_queue(),
                meta=file.meta,
            )
            return await target(piped_file)
        except Exception as error:
            raise TargetPipeError from error

    source_to_queue_task: Task[None] = create_task(source_to_queue())
    target_from_queue_task: Task[T] = create_task(target_from_queue())

    try:
        _, target_result = await gather(
            source_to_queue_task,
            target_from_queue_task,
        )
        return target_result
    except (SourcePipeError, TargetPipeError):
        source_to_queue_task.cancel()
        target_from_queue_task.cancel()
        source_result, target_result = await gather(
            source_to_queue_task,
            target_from_queue_task,
            return_exceptions=True,
        )
        if isinstance(source_result, Exception):
            raise source_result
        else:
            raise target_result
