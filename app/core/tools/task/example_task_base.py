from app.core.tools.task.types.example_state import ExampleState
from app.tools.essential.task.task_base import TaskBase


class ExampleTaskBase[R](TaskBase[ExampleState[R], R]):
    def _create_state(self) -> ExampleState[R]:
        return ExampleState[R]()
