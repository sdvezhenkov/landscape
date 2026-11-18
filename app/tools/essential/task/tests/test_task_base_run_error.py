import pytest

from app.tools.essential.task.tests.conftest import (
    ErrorGateTask,
    ExampleError,
    ExampleState,
    ExampleStatus,
    WithoutRunTask,
    WithoutStateTask,
)
from app.tools.essential.task.types.task_state import TaskStages


async def test_task_base_run_without_state_error():
    with pytest.raises(NotImplementedError):
        WithoutStateTask()

async def test_task_base_run_without_run_error():
    task = WithoutRunTask()
    with pytest.raises(NotImplementedError):
        await task.run()

async def test_task_base_run_error():
    task = ErrorGateTask()
    with pytest.raises(ExampleError):
        await task.run()

async def test_task_base_run_error_state_result():
    task = ErrorGateTask()
    with pytest.raises(ExampleError):
        await task.run()
    assert type(task.state) is ExampleState
    assert task.state.result is None

async def test_task_base_run_error_state_status():
    task = ErrorGateTask()
    with pytest.raises(ExampleError):
        await task.run()
    assert type(task.state) is ExampleState
    assert type(task.state.status) is ExampleStatus
    assert task.state.status.stage == TaskStages.FAILURE
    assert task.state.status.overall.value <= 4
    assert task.state.status.current.value <= 4
