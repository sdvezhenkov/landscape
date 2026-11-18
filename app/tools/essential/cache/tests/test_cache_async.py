from collections.abc import Callable, Coroutine
from inspect import iscoroutinefunction
from typing import Any

import pytest
from pydantic import BaseModel, Field

from app.tools.essential.cache.cache import TaskCache


async def test_cache_memoize_async_calls():
    cache = TaskCache()
    calls = 0

    @cache.memoize()
    async def func() -> int:
        nonlocal calls
        calls += 1
        return calls

    await func()
    func_calls = await func()
    assert func_calls == 1

async def test_cache_memoize_evict_async_calls():
    cache = TaskCache()
    calls = 0

    @cache.memoize()
    async def func() -> int:
        nonlocal calls
        calls += 1
        return calls

    await func()
    cache.evict()
    func_calls = await func()
    assert func_calls == 2

async def test_cache_memoize_async_error():
    class TestError1(Exception):
        pass

    class TestError2(Exception):
        pass

    cache = TaskCache()
    calls = 0

    @cache.memoize()
    async def func() -> int:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TestError1()
        if calls == 2:
            raise TestError2()
        return calls

    with pytest.raises(TestError1) as e1:
        await func()
    with pytest.raises(TestError2) as e2:
        await func()

    assert type(e1.value) is TestError1
    assert type(e2.value) is TestError2
    await func()
    func_calls = await func()
    assert func_calls == 3

async def test_cache_memoize_async_type():
    class TestType(BaseModel):
        a: int = 1
        b: dict = Field(default_factory=dict)

    cache = TaskCache()

    @cache.memoize()
    async def func() -> TestType:
        return TestType()

    func_result_1 = await func()
    func_result_2 = await func()
    assert func_result_1 is func_result_2
    assert type(func_result_1) is TestType

async def test_cache_memoize_async_func_type():
    cache = TaskCache()

    @cache.memoize()
    async def func() -> Callable[[], Coroutine[Any, Any, None]]:
        async def func_type():
            ...
        return func_type

    func_result_1 = await func()
    func_result_2 = await func()
    assert func_result_1 is func_result_2
    assert iscoroutinefunction(func_result_1)
