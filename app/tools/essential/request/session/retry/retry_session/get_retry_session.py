from aiohttp import ClientSession, ClientTimeout

from app.tools.essential.request.session.retry.policy.types.retry_policy import RetryPolicy
from app.tools.essential.request.session.retry.retry_middleware.get_retry_middleware import get_retry_middleware


def get_retry_session(
        policy: RetryPolicy | None = None,
) -> ClientSession:
    policy = policy or RetryPolicy()
    retry_middleware = get_retry_middleware(policy)
    session = ClientSession(
        middlewares=(retry_middleware,),
        timeout=ClientTimeout(total=policy.timeout.total),
    )
    return session
