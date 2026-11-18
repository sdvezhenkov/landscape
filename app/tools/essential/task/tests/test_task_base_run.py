from app.tools.essential.task.tests.conftest import EmptyTask, ExampleState, ExampleStatus, ExampleType, GateTask
from app.tools.essential.task.types.task_state import TaskStages


async def test_task_base_run_result():
    task = EmptyTask()
    task_result = await task.run()
    assert type(task_result) is ExampleType
    assert task_result.a == 1
    assert task_result.b == {}

async def test_task_base_run_state_result():
    task = EmptyTask()
    await task.run()
    assert type(task.state) is ExampleState
    assert type(task.state.result) is ExampleType
    assert isinstance(task.state.result, ExampleType)
    assert task.state.result.a == 1
    assert task.state.result.b == {}

async def test_task_base_run_state_status():
    task = GateTask()
    await task.run()
    assert type(task.state) is ExampleState
    assert type(task.state.status) is ExampleStatus
    assert task.state.status.stage == TaskStages.SUCCESS
    assert task.state.status.overall.value == 4
    assert task.state.status.current.value == 4
