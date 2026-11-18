from random import Random

from app.tools.essential.request.session.retry.delay.get_delay import get_delay
from app.tools.essential.request.session.retry.policy.types.retry_policy import RetryBackoff


def test_get_delay_factor():
    backoff = RetryBackoff(
        factor=2,
        max=100,
        jitter=0,
    )
    delay = get_delay(backoff, attempt=3)
    assert delay == 16

def test_get_delay_max():
    backoff = RetryBackoff(
        factor=2,
        max=15,
        jitter=0,
    )
    delay = get_delay(backoff, attempt=3)
    assert delay == 15

def test_get_delay_jitter():
    backoff = RetryBackoff(
        factor=2,
        max=100,
        jitter=5,
    )
    random_ = Random(1)
    delay = get_delay(backoff, attempt=3, random_=random_)
    assert 16 <= delay <= 21
