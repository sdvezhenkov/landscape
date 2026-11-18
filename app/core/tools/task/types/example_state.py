from pydantic import Field

from app.tools.essential.task.types.task_state import Counter, TaskState, TaskStatus


class ExampleStatus(TaskStatus):
    current: Counter = Field(default_factory=Counter)
    overall: Counter = Field(default_factory=Counter)


class ExampleState[R](TaskState[R]):
    status: ExampleStatus = Field(default_factory=ExampleStatus)
    result: R | None = None
