from random import Random

from app.tools.essential.request.session.retry.policy.types.retry_policy import RetryBackoff


def get_delay(
        backoff: RetryBackoff,
        attempt: int,
        random_: Random | None = None,
) -> float:
    random_: Random = random_ or Random()
    backoff_current: float = backoff.factor * (2 ** attempt)
    delay = min(backoff_current, backoff.max)
    delay += random_.uniform(0, backoff.jitter)
    return delay
