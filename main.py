from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import app_router
from app.tools.essential.database.session import create_db_and_tables
from app.tools.essential.docs.router import get_docs_router
from app.tools.essential.env.get_env import get_env
from app.tools.essential.task.errors.task_registry import TaskRegistryError
from app.tools.essential.task.task_registry_exception_handler import task_registry_exception_handler


# noinspection unused-parameter
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    await create_db_and_tables()
    yield

app: FastAPI = FastAPI(
    title=get_env('LSC_PROJECT_NAME'),
    version='1.0.0',
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_exception_handler(
    TaskRegistryError,
    task_registry_exception_handler,
)

app.include_router(get_docs_router(app), include_in_schema=False)
app.include_router(app_router)
