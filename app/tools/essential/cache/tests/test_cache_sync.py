from collections.abc import Callable

from pydantic import BaseModel, Field

from app.tools.essential.cache.cache import TaskCache
from app.tools.essential.cache.cache import cache as single_cache


async def test_cache():
    assert single_cache is not None
    assert type(single_cache) is TaskCache

def test_cache_memoize_sync_calls():
    cache = TaskCache()
    calls = 0

    @cache.memoize()
    def func() -> int:
        nonlocal calls
        calls += 1
        return calls

    func()
    func_calls = func()
    assert func_calls == 1

def test_cache_memoize_sync_type():
    class TestType(BaseModel):
        a: int = 1
        b: dict = Field(default_factory=dict)

    cache = TaskCache()

    @cache.memoize()
    def func() -> TestType:
        return TestType()

    func_result_1 = func()
    func_result_2 = func()
    assert func_result_1 is func_result_2
    assert type(func_result_1) is TestType

def test_cache_memoize_sync_func_type():
    cache = TaskCache()

    @cache.memoize()
    def func() -> Callable[[], None]:
        def func_type():
            ...
        return func_type

    func_result_1 = func()
    func_result_2 = func()
    assert func_result_1 is func_result_2
    assert callable(func_result_1)

def test_cache_memoize_evict_sync_calls():
    cache = TaskCache()
    calls = 0

    @cache.memoize()
    def func() -> int:
        nonlocal calls
        calls += 1
        return calls

    func()
    cache.evict()
    func_calls = func()
    assert func_calls == 2
