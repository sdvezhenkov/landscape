from app.core.client.user_client import UserClient
from app.core.tools.task.example_task_base import ExampleTaskBase
from app.core.tools.task.types.example_state import ExampleState


class GetUserNamesTask(ExampleTaskBase[list[str]]):
    async def _run(self, state: ExampleState[list[str]]) -> list[str]:
        client = UserClient(state.status)
        try:
            return await client.get_names()
        finally:
            await client.aclose()
