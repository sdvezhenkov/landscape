import asyncio
from collections.abc import Callable, Coroutine
from enum import Enum
from typing import Any

from pydantic import BaseModel, PrivateAttr, model_serializer, model_validator

type AsyncCallback = Callable[[], Coroutine[Any, Any, None]]


class ReactiveModel(BaseModel):
    _on_change: AsyncCallback | None = PrivateAttr(default=None)
    _update_scheduled: bool = PrivateAttr(default=False)

    def bind(
            self,
            on_change: AsyncCallback | None,
    ) -> None:
        super().__setattr__('_on_change', on_change)
        for value in self.__dict__.values():
            if isinstance(value, ReactiveModel):
                value.bind(on_change)

    def __setattr__(
            self,
            key,
            value,
    ):
        super().__setattr__(key, value)
        if not self._update_scheduled:
            super().__setattr__('_update_scheduled', True)
            asyncio.create_task(self._update())

    async def _update(self) -> None:
        super().__setattr__('_update_scheduled', False)
        if self._on_change is not None:  # pragma: no branch
            await self._on_change()

    def __deepcopy__(
            self,
            memo: dict[int, Any] | None = None,
    ):
        if memo is None:
            memo = {}
        callback = self._on_change
        if callback is not None:  # pragma: no branch
            memo[id(callback)] = callback
        copied = super().__deepcopy__(memo)
        BaseModel.__setattr__(copied, '_on_change', None)
        BaseModel.__setattr__(copied, '_update_scheduled', False)
        return copied


class Counter(ReactiveModel):
    value: int = 0

    def inc(
            self,
            amount: int = 1,
    ) -> None:
        self.value += amount

    def dec(
            self,
            amount: int = 1,
    ) -> None:
        self.value -= amount  # pragma: no cover

    def set(
            self,
            value: int,
    ) -> None:
        self.value = value

    @model_validator(mode="before")
    @classmethod
    def validate_from_int(
            cls,
            data: Any,
    ) -> Any:
        if isinstance(data, int):  # pragma: no cover
            return {"value": data}
        return data

    @model_serializer()
    def serialize_model(self) -> int:
        return self.value


class TaskStages(Enum):
    PENDING = 'pending'
    STARTED = 'started'
    SUCCESS = 'success'
    FAILURE = 'failure'


TASK_COMPLETION_STAGES = {
    TaskStages.SUCCESS,
    TaskStages.FAILURE,
}
TASK_ACTIVE_STAGES = {
    stage for stage in TaskStages if stage not in TASK_COMPLETION_STAGES
}


class TaskStatus(ReactiveModel):
    stage: TaskStages = TaskStages.PENDING


class TaskState[R](ReactiveModel):
    status: TaskStatus
    result: R | None
