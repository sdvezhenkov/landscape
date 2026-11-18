from fastapi import status

from app.tools.essential.task.types.task_registry_error_config import TaskRegistryErrorConfig

DEFAULT_ERROR = TaskRegistryErrorConfig(
    http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ws_code=status.WS_1011_INTERNAL_ERROR,
    detail="Internal server error",
)
