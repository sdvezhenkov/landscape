import asyncio
import functools
import weakref
from inspect import iscoroutinefunction

from app.tools.essential.cache.types.callable import AnyCallable, AsyncCallable, SyncCallable
from app.tools.essential.cache.types.decorator import AnyDecorator, AsyncDecorator, SyncDecorator


class TaskCache:
    def __init__(self):
        self.cached_functions = weakref.WeakSet()

    def memoize[**P, R](self) -> AnyDecorator[P, R]:
        def dynamic_decorator(
                func: AnyCallable[P, R],
        ) -> AnyCallable[P, R]:
            if iscoroutinefunction(func):
                decorator: AsyncDecorator[P, R] = self.memoize_async()
                wrapper: AsyncCallable[P, R] = decorator(func)
            else:
                decorator: SyncDecorator[P, R] = self.memoize_sync()
                wrapper: SyncCallable[P, R] = decorator(func)
            return wrapper
        return dynamic_decorator

    def memoize_async[**P, R](self) -> AsyncDecorator[P, R]:
        def decorator(
                func: AsyncCallable[P, R],
        ) -> AsyncCallable[P, R]:
            @functools.cache
            def cached_func(
                    *args: P.args,
                    **kwargs: P.kwargs,
            ) -> asyncio.Task[R]:
                result = asyncio.create_task(func(*args, **kwargs))
                return result

            @functools.wraps(func)
            async def wrapper(
                    *args: P.args,
                    **kwargs: P.kwargs,
            ) -> R:
                try:
                    result = await cached_func(*args, **kwargs)
                    return result
                except Exception:
                    cached_func.cache_clear()
                    raise

            wrapper.cache_clear = cached_func.cache_clear
            self.cached_functions.add(wrapper)
            return wrapper
        return decorator

    def memoize_sync[**P, R](self) -> SyncDecorator[P, R]:
        def decorator(
                func: SyncCallable[P, R],
        ) -> SyncCallable[P, R]:
            @functools.cache
            def cached_func(
                    *args: P.args,
                    **kwargs: P.kwargs,
            ) -> R:
                result = func(*args, **kwargs)
                return result

            @functools.wraps(func)
            def wrapper(
                    *args: P.args,
                    **kwargs: P.kwargs,
            ) -> R:
                result: R = cached_func(*args, **kwargs)
                return result

            wrapper.cache_clear = cached_func.cache_clear
            self.cached_functions.add(wrapper)
            return wrapper
        return decorator

    def evict(self) -> None:
        for cached_function in tuple(self.cached_functions):
            cached_function.cache_clear()

cache = TaskCache()
