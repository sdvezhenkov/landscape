import asyncio

from aiohttp import ClientHandlerType, ClientMiddlewareType, ClientRequest, ClientResponse

from app.tools.essential.request.session.retry.delay.get_delay import get_delay
from app.tools.essential.request.session.retry.policy.types.retry_policy import RetryPolicy


def get_retry_middleware(
        policy: RetryPolicy,
) -> ClientMiddlewareType:
    async def retry_middleware(
            req: ClientRequest,
            handler: ClientHandlerType,
    ) -> ClientResponse:
        if req.method in policy.methods:
            policy_retries = policy.retries
        else:
            policy_retries = 0
        for attempt in range(policy_retries+1):
            try:
                async with asyncio.timeout(policy.timeout.attempt):
                    res = await handler(req)
            except TimeoutError:
                if attempt == policy_retries:
                    raise
            else:
                if res.ok or res.status not in policy.statuses:
                    return res
                if attempt == policy_retries:
                    return res
                res.release()
            delay = get_delay(policy.backoff, attempt)
            await asyncio.sleep(delay)
        raise ValueError(
            f'policy.retries must be non-negative but equal to {policy.retries}',
        )

    return retry_middleware
