from collections.abc import Callable, Coroutine
from typing import Any

type AsyncCallable[**P, R] = Callable[P, Coroutine[Any, Any, R]]
type SyncCallable[**P, R] = Callable[P, R]
type AnyCallable[**P, R] = AsyncCallable[P, R] | SyncCallable[P, R]
