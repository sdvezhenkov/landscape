import pytest

from app.tools.essential.task.errors.task_registry import IsBusyError, TaskNotFoundError
from app.tools.essential.task.task_base import TaskBase
from app.tools.essential.task.task_registry import TaskRegistry
from app.tools.essential.task.task_registry import task_registry as single_task_registry
from app.tools.essential.task.tests.conftest import TEST_TASK_REGISTRY_POLICY, EmptyTask, ExampleState, ExampleType
from app.tools.essential.task.types.task_registry_policy import TaskRegistryLimits, TaskRegistryPolicy


def test_task_registry():
    assert single_task_registry is not None
    assert type(single_task_registry) is TaskRegistry

def test_task_registry_get():
    task = EmptyTask()
    task_registry = TaskRegistry()
    task_registry.add(task)
    task_from_registry = task_registry.get(task.id, EmptyTask)
    assert task_from_registry is task

def test_task_registry_is_busy():
    task_registry = TaskRegistry(TEST_TASK_REGISTRY_POLICY)
    limit = task_registry.policy.limit
    for i in range(limit.active):
        task = EmptyTask()
        task_registry.add(task)
    assert task_registry.is_busy() is True

async def test_task_registry_cleanup():
    task_registry = TaskRegistry(TEST_TASK_REGISTRY_POLICY)
    limit = task_registry.policy.limit
    for i in range(limit.storage * 2):
        task = EmptyTask()
        task_registry.add(task)
        if i > limit.active - 2:
            await task.run()
    assert len(task_registry._storage) <= limit.storage

def test_task_registry_get_error_type():
    task = EmptyTask()
    task_registry = TaskRegistry(TEST_TASK_REGISTRY_POLICY)
    task_registry.add(task)
    with pytest.raises(TaskNotFoundError):
        task_registry.get(task.id, TaskBase[ExampleState, ExampleType])

def test_task_registry_get_error_task():
    some_task = EmptyTask()
    task_registry = TaskRegistry(TEST_TASK_REGISTRY_POLICY)
    with pytest.raises(TaskNotFoundError):
        task_registry.get(some_task.id, EmptyTask)

def test_task_registry_add_error_busy():
    task_registry = TaskRegistry(TEST_TASK_REGISTRY_POLICY)
    limit = task_registry.policy.limit
    for i in range(limit.active):
        task = EmptyTask()
        task_registry.add(task)
    with pytest.raises(IsBusyError):
        task = EmptyTask()
        task_registry.add(task)

def test_task_registry_policy_limit_error():
    with pytest.raises(ValueError) as e:
        TaskRegistryPolicy(
            limit=TaskRegistryLimits(
                active=30,
                storage=10,
            ),
        )
    assert e.value.args[0] == 'Active task limit must not exceed storage limit'
