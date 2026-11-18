from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.tools.essential.env.get_env import get_env

authority = f'{get_env('LSC_DB_USERNAME')}:{get_env('LSC_DB_PASSWORD')}'
host = get_env('LSC_DB_HOST')
database = get_env('LSC_DB_NAME')
port = 5432
sql_url = f'postgresql+asyncpg://{authority}@{host}:{port}/{database}'
engine = create_async_engine(sql_url)
session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda conn: SQLModel.metadata.create_all(conn))

async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session

@asynccontextmanager
async def get_session_context() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session

SessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]
