from app.tools.essential.task.errors.task_registry import IsBusyError, TaskNotFoundError
from app.tools.essential.task.task_base import TaskBase
from app.tools.essential.task.types.task_id import TaskID
from app.tools.essential.task.types.task_registry_policy import TaskRegistryPolicy
from app.tools.essential.task.types.task_state import TASK_ACTIVE_STAGES, TASK_COMPLETION_STAGES


class TaskRegistry:
    def __init__(
            self,
            policy: TaskRegistryPolicy | None = None,
    ):
        self._storage = dict[TaskID, TaskBase]()
        self.policy = policy or TaskRegistryPolicy()

    def add(
            self,
            task: TaskBase,
    ) -> TaskID:
        if self.is_busy():
            raise IsBusyError()
        self._cleanup()
        task_id = task.id
        self._storage[task_id] = task
        return task_id

    def _cleanup(self) -> None:
        if len(self._storage) >= self.policy.limit.storage:
            for task_id, task in self._storage.items():  # pragma: no branch
                if task.state.status.stage in TASK_COMPLETION_STAGES:
                    del self._storage[task_id]
                    return

    def is_busy(self) -> bool:
        active_tasks = 0
        for task in self._storage.values():
            if task.state.status.stage in TASK_ACTIVE_STAGES:
                active_tasks += 1
        is_busy = active_tasks >= self.policy.limit.active
        return is_busy

    def get[T: TaskBase](
            self,
            task_id: TaskID,
            task_type: type[T],
    ) -> T:
        task = self._storage.get(task_id)
        if task is None:
            raise TaskNotFoundError()
        if type(task) is not task_type:
            raise TaskNotFoundError()
        return task


task_registry = TaskRegistry()
