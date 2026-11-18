import asyncio
import json

import pytest

from app.tools.essential.task.tests.conftest import ErrorGateTask, ExampleError, GateTask


async def test_task_base_serialization_initial_state():
    task = GateTask()
    async with task.subscribe() as subscriber:
        event = await anext(subscriber)
        payload = json.loads(event.state.model_dump_json())
    assert payload == {
        'status': {'stage': 'pending', 'current': 0, 'overall': 0},
        'result': None,
    }
    assert not task.subscribers

async def test_task_base_serialization_failed_state():
    task = ErrorGateTask()
    with pytest.raises(ExampleError):
        await task.run()
    async with asyncio.timeout(1):
        async with task.subscribe() as subscriber:
            events = [event async for event in subscriber]
    assert len(events) == 1
    assert json.loads(events[0].state.model_dump_json()) == {
        'status': {'stage': 'failure', 'current': 1, 'overall': 4},
        'result': None,
    }
    assert not task.subscribers

async def test_task_base_serialization_success_state():
    task = GateTask()
    await task.run()
    async with asyncio.timeout(1):
        async with task.subscribe() as subscriber:
            events = [event async for event in subscriber]
    assert len(events) == 1
    assert json.loads(events[0].state.model_dump_json()) == {
        'status': {'stage': 'success', 'current': 4, 'overall': 4},
        'result': {'a': 1, 'b': {}},
    }
    assert not task.subscribers

async def test_task_base_serialization_preserves_previous_event():
    task = GateTask()
    async with asyncio.timeout(1):
        async with task.subscribe() as subscriber:
            initial_event = await anext(subscriber)
            await task.run()
            events = [event async for event in subscriber]
    assert json.loads(initial_event.state.model_dump_json()) == {
        'status': {'stage': 'pending', 'current': 0, 'overall': 0},
        'result': None,
    }
    assert events
    assert json.loads(events[-1].state.model_dump_json()) == {
        'status': {'stage': 'success', 'current': 4, 'overall': 4},
        'result': {'a': 1, 'b': {}},
    }
    assert not task.subscribers
