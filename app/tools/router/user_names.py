from fastapi import APIRouter, Security, WebSocket

from app.core.task.get_user_names_task import GetUserNamesTask
from app.core.tools.task.types.example_state import ExampleState
from app.tools.essential.security.auth.dependencies import require_scopes
from app.tools.essential.task.task_registry import task_registry
from app.tools.router.types.task_id.user_names_id import UserNamesID

router = APIRouter(tags=['user names'])
user_names_router = router


@router.post('/', dependencies=[Security(require_scopes, scopes=['landscape:user_names:run'])])
async def run_get_user_names() -> UserNamesID:
    task = GetUserNamesTask()
    task_id = task_registry.add(task)
    task.run_in_background()
    return task_id


@router.get('/state/{task_id}', dependencies=[Security(require_scopes, scopes=['landscape:user_names:show'])])
async def show_get_user_names_state(task_id: UserNamesID) -> ExampleState[list[str]]:
    task = task_registry.get(task_id, GetUserNamesTask)
    return task.state


@router.websocket('/state/{task_id}', dependencies=[Security(require_scopes, scopes=['landscape:user_names:show'])])
async def show_get_user_names_state_ws(websocket: WebSocket, task_id: UserNamesID) -> None:
    task = task_registry.get(task_id, GetUserNamesTask)
    async with task.subscribe() as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.state.model_dump_json())
    await websocket.close()
