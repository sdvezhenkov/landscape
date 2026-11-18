from dataclasses import dataclass

from app.tools.essential.task.types.task_id import TaskID
from app.tools.essential.task.types.task_state import TaskState


@dataclass(frozen=True, slots=True)
class Event[TS: TaskState]:
    task_id: TaskID
    state: TS
