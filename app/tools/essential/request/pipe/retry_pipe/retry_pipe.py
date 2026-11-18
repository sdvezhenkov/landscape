import asyncio
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

from app.tools.essential.request.pipe.filestream.types.file_stream import FileStream
from app.tools.essential.request.pipe.pipe.pipe import pipe
from app.tools.essential.request.session.retry.delay.get_delay import get_delay
from app.tools.essential.request.session.retry.policy.types.retry_policy import RetryPolicy


async def retry_pipe[T](
        source: Callable[[], Awaitable[FileStream]],
        target: Callable[[FileStream], Coroutine[Any, Any, T]],
        queue_maxsize: int = 8,
        retry_policy: RetryPolicy | None = None,
) -> T:
    policy = retry_policy or RetryPolicy()
    async with asyncio.timeout(policy.timeout.total):
        for attempt in range(policy.retries+1):
            # noinspection broad-exception
            try:
                result: T = await pipe(
                    source=source,
                    target=target,
                    queue_maxsize=queue_maxsize,
                )
                return result
            except Exception:
                if attempt == policy.retries:
                    raise
                delay = get_delay(policy.backoff, attempt)
                await asyncio.sleep(delay)
        raise ValueError(
            f'policy.retries must be non-negative but equal to {policy.retries}',
        )
