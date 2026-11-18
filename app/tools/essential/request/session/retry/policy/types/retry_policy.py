from dataclasses import dataclass, field

from pydantic import NonNegativeInt

DEFAULT_RETRY_AMOUNT: NonNegativeInt = 10
DEFAULT_RETRY_TIMEOUT_REQUEST: float = 120.0
DEFAULT_RETRY_TIMEOUT_TOTAL: float = 600.0
DEFAULT_RETRY_METHODS: set[str] = {'GET', 'HEAD', 'OPTIONS'}
DEFAULT_RETRY_STATUSES: set[int] = {413, 429, 500, 502, 503, 504}


@dataclass(frozen=True, slots=True)
class RetryBackoff:
    factor: float = 1
    max: float = 120
    jitter: float = 5


@dataclass(frozen=True, slots=True)
class RetryTimeout:
    attempt: float = DEFAULT_RETRY_TIMEOUT_REQUEST
    total: float = DEFAULT_RETRY_TIMEOUT_TOTAL


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    retries: NonNegativeInt = DEFAULT_RETRY_AMOUNT
    methods: set[str] = field(default_factory=lambda: DEFAULT_RETRY_METHODS.copy())
    statuses: set[int] = field(default_factory=lambda: DEFAULT_RETRY_STATUSES.copy())
    backoff: RetryBackoff = field(default_factory=RetryBackoff)
    timeout: RetryTimeout = field(default_factory=RetryTimeout)
