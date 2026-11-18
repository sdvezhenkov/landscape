from collections.abc import Callable

from app.tools.essential.cache.types.callable import AnyCallable, AsyncCallable, SyncCallable

type AsyncDecorator[**P, R] = Callable[[AsyncCallable[P, R]], AsyncCallable[P, R]]
type SyncDecorator[**P, R] = Callable[[SyncCallable[P, R]], SyncCallable[P, R]]
type AnyDecorator[**P, R] = Callable[[AnyCallable[P, R]], AnyCallable[P, R]]
