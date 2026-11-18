from app.tools.essential.task.errors.task_registry import IsBusyError, TaskNotFoundError, TaskRegistryError
from app.tools.essential.task.types.task_registry_error_config import TaskRegistryErrorConfig

ERROR_CONFIGS: dict[type[TaskRegistryError], TaskRegistryErrorConfig] = {
    TaskNotFoundError: TaskRegistryErrorConfig(
        http_code=404,
        ws_code=1008,
        detail="Task not found",
    ),
    IsBusyError: TaskRegistryErrorConfig(
        http_code=503,
        ws_code=1013,
        detail="Too many active tasks",
    ),
}
