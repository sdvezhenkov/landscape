import asyncio
from asyncio import Semaphore
from types import NoneType

from app.tools.essential.task.tests.conftest import ExampleState, ExampleStatus, ExampleType, GateTask
from app.tools.essential.task.types.event import Event
from app.tools.essential.task.types.task_state import TaskStages


async def consumer(
        task: GateTask,
        gate: Semaphore,
) -> None:
    events = list[Event[ExampleState]]()
    async with task.subscribe() as subscriber:
        async for event in subscriber:
            events.append(event)
            if event.state.status.stage is not TaskStages.PENDING:
                gate.release()
    assert not task.subscribers
    assert len(events) == 6
    excpected_state_contents: tuple[dict, ...] = (
        {'stage': TaskStages.PENDING, 'current': 0, 'overall': 0, 'result_type': NoneType},
        {'stage': TaskStages.STARTED, 'current': 0, 'overall': 0, 'result_type': NoneType},
        {'stage': TaskStages.STARTED, 'current': 0, 'overall': 4, 'result_type': NoneType},
        {'stage': TaskStages.STARTED, 'current': 2, 'overall': 4, 'result_type': NoneType},
        {'stage': TaskStages.STARTED, 'current': 3, 'overall': 4, 'result_type': NoneType},
        {'stage': TaskStages.SUCCESS, 'current': 4, 'overall': 4, 'result_type': ExampleType},
    )
    for message, state in zip(events, excpected_state_contents):
        assert message.state.status.stage == state['stage']
        assert message.state.status.current.value == state['current']
        assert message.state.status.overall.value == state['overall']
        assert type(message.state.result) is state['result_type']
    last_message = events[-1]
    last_result = last_message.state.result
    assert last_result is not None
    assert last_result.a == 1
    assert last_result.b == {}

async def test_task_base_run_bg_state_result():
    gate = Semaphore(0)
    task = GateTask(gate)
    task.run_in_background()
    await consumer(task, gate)
    assert type(task.state) is ExampleState
    assert type(task.state.result) is ExampleType
    assert isinstance(task.state.result, ExampleType)
    assert task.state.result.a == 1
    assert task.state.result.b == {}

async def test_task_base_run_bg_state_status():
    gate = Semaphore(0)
    task = GateTask(gate)
    task.run_in_background()
    await consumer(task, gate)
    assert type(task.state) is ExampleState
    assert type(task.state.status) is ExampleStatus
    assert task.state.status.stage == TaskStages.SUCCESS
    assert task.state.status.overall.value == 4
    assert task.state.status.current.value == 4

def test_task_base_run_bg_cancelled_on_shutdown():
    errors = []

    async def main() -> None:
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(
            lambda loop, context: errors.append(context),
        )
        gate = Semaphore(0)
        task = GateTask(gate)
        task.run_in_background()
        while task.state.status.stage is not TaskStages.STARTED:
            await asyncio.sleep(0)

    asyncio.run(main())
    assert len(errors) == 0
