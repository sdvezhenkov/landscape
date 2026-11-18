from typing import cast, overload

from fastapi import Request, WebSocket
from fastapi.responses import JSONResponse, Response

from app.tools.essential.logger.logger import logger
from app.tools.essential.task.constants.default_error import DEFAULT_ERROR
from app.tools.essential.task.constants.error_configs import ERROR_CONFIGS
from app.tools.essential.task.errors.task_registry import TaskRegistryError


@overload
async def task_registry_exception_handler(
    connection: Request,
    exc: Exception,
) -> Response:
    ...

@overload
async def task_registry_exception_handler(
    connection: WebSocket,
    exc: Exception,
) -> None:
    ...

async def task_registry_exception_handler(
    connection: Request | WebSocket,
    exc: Exception,
) -> Response | None:
    error = cast(TaskRegistryError, exc)
    error_type = type(error)
    error_config = ERROR_CONFIGS.get(error_type, DEFAULT_ERROR)
    if error is DEFAULT_ERROR:
        logger.error(
            "Unhandled task registry exception",
            exc_info=(type(exc), exc, exc.__traceback__),
        )
    if isinstance(connection, Request):
        return JSONResponse(
            status_code=error_config.http_code,
            content={"detail": error_config.detail},
        )
    else:
        await connection.close(
            code=error_config.ws_code,
            reason=error_config.detail,
        )
        return None
