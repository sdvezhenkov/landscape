from typing import Annotated

from fastapi import APIRouter, Body, Security, WebSocket
from pydantic import PositiveInt

from app.core.task.get_post_titles_task import GetPostTitlesTask
from app.core.tools.task.types.example_state import ExampleState
from app.tools.essential.security.auth.dependencies import require_scopes
from app.tools.essential.task.task_registry import task_registry
from app.tools.router.types.task_id.post_titles_id import PostTitlesID

router = APIRouter(tags=['post titles'])
post_titles_router = router


@router.post('/', dependencies=[Security(require_scopes, scopes=['landscape:post_titles:run'])])
async def run_get_post_titles(user_id: Annotated[PositiveInt, Body(embed=True)]) -> PostTitlesID:
    task = GetPostTitlesTask(user_id)
    task_id = task_registry.add(task)
    task.run_in_background()
    return task_id


@router.get('/state/{task_id}', dependencies=[Security(require_scopes, scopes=['landscape:post_titles:show'])])
async def show_get_post_titles_state(task_id: PostTitlesID) -> ExampleState[list[str]]:
    task = task_registry.get(task_id, GetPostTitlesTask)
    return task.state


@router.websocket('/state/{task_id}', dependencies=[Security(require_scopes, scopes=['landscape:post_titles:show'])])
async def show_get_post_titles_state_ws(websocket: WebSocket, task_id: PostTitlesID) -> None:
    task = task_registry.get(task_id, GetPostTitlesTask)
    async with task.subscribe() as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.state.model_dump_json())
    await websocket.close()
