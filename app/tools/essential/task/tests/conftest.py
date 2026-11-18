from asyncio import Semaphore
from collections.abc import Callable, Coroutine
from typing import Any

from pydantic import BaseModel, Field

from app.tools.essential.task.task_base import TaskBase
from app.tools.essential.task.types.task_registry_policy import TaskRegistryLimits, TaskRegistryPolicy
from app.tools.essential.task.types.task_state import Counter, TaskState, TaskStatus

TEST_OVERALL = 4

type ExampleRunSuit = Callable[[ExampleState, Semaphore], Coroutine[Any, Any, ExampleType]]

class ExampleStatus(TaskStatus):
    current: Counter = Field(default_factory=Counter)
    overall: Counter = Field(default_factory=Counter)


class ExampleType(BaseModel):
    a: int = 1
    b: dict = Field(default_factory=dict)


class ExampleState(TaskState[ExampleType]):
    status: ExampleStatus = Field(default_factory=ExampleStatus)
    result: ExampleType | None = None


class GateTask(TaskBase[ExampleState, ExampleType]):
    def __init__(
            self,
            gate: Semaphore | None = None,
    ):
        super().__init__()
        self.gate = gate or Semaphore(TEST_OVERALL)

    def _create_state(self) -> ExampleState:
        state: ExampleState = ExampleState()
        return state

    async def _run(
            self,
            state: ExampleState,
    ) -> ExampleType:
        await self.gate.acquire()
        state.status.overall.set(TEST_OVERALL)
        await self.gate.acquire()
        state.status.current.inc()
        state.status.current.inc()
        await self.gate.acquire()
        state.status.current.inc()
        await self.gate.acquire()
        state.status.current.inc()
        return ExampleType()


class EmptyTask(TaskBase[ExampleState, ExampleType]):
    def _create_state(self) -> ExampleState:
        state: ExampleState = ExampleState()
        return state

    async def _run(
            self,
            state: ExampleState,
    ) -> ExampleType:
        return ExampleType()


class WithoutStateTask(TaskBase[ExampleState, ExampleType]):
    pass


class WithoutRunTask(TaskBase[ExampleState, ExampleType]):
    def _create_state(self) -> ExampleState:
        state: ExampleState = ExampleState()
        return state


class ExampleError(Exception):
    pass


class ErrorGateTask(TaskBase[ExampleState, ExampleType]):
    def __init__(
            self,
            gate: Semaphore | None = None,
    ):
        super().__init__()
        self.gate = gate or Semaphore(TEST_OVERALL)

    def _create_state(self) -> ExampleState:
        state: ExampleState = ExampleState()
        return state

    async def _run(
            self,
            state: ExampleState,
    ) -> ExampleType:
        await self.gate.acquire()
        state.status.overall.set(TEST_OVERALL)
        await self.gate.acquire()
        state.status.current.inc()
        raise ExampleError()


TEST_TASK_REGISTRY_POLICY = TaskRegistryPolicy(
    limit=TaskRegistryLimits(
        active=2,
        storage=6,
    ),
)
