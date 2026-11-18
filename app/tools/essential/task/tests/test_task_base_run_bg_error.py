from asyncio import Semaphore
from types import NoneType

from app.tools.essential.task.tests.conftest import ErrorGateTask, ExampleState, ExampleStatus
from app.tools.essential.task.types.event import Event
from app.tools.essential.task.types.task_state import TaskStages


async def consumer(
        task: ErrorGateTask,
        gate: Semaphore,
) -> None:
    events = list[Event[ExampleState]]()
    async with task.subscribe() as subscriber:
        async for event in subscriber:
            events.append(event)
            if event.state.status.stage is not TaskStages.PENDING:
                gate.release()
    assert not task.subscribers
    assert len(events) == 4
    excpected_state_contents: tuple[dict, ...] = (
        {'stage': TaskStages.PENDING, 'current': 0, 'overall': 0, 'result_type': NoneType},
        {'stage': TaskStages.STARTED, 'current': 0, 'overall': 0, 'result_type': NoneType},
        {'stage': TaskStages.STARTED, 'current': 0, 'overall': 4, 'result_type': NoneType},
        {'stage': TaskStages.FAILURE, 'current': 1, 'overall': 4, 'result_type': NoneType},
    )
    for message, state in zip(events, excpected_state_contents):
        assert message.state.status.stage == state['stage']
        assert message.state.status.current.value == state['current']
        assert message.state.status.overall.value == state['overall']
        assert type(message.state.result) is state['result_type']

async def test_task_base_run_bg_state_result():
    gate = Semaphore(0)
    task = ErrorGateTask(gate)
    task.run_in_background()
    await consumer(task, gate)
    assert type(task.state) is ExampleState
    assert task.state.result is None

async def test_task_base_run_bg_state_status():
    gate = Semaphore(0)
    task = ErrorGateTask(gate)
    task.run_in_background()
    await consumer(task, gate)
    assert type(task.state) is ExampleState
    assert type(task.state.status) is ExampleStatus
    assert task.state.status.stage == TaskStages.FAILURE
    assert task.state.status.overall.value <= 4
    assert task.state.status.current.value <= 4
