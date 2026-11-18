from app.core.client.post_client import PostClient
from app.core.tools.task.example_task_base import ExampleTaskBase
from app.core.tools.task.types.example_state import ExampleState


class GetPostTitlesTask(ExampleTaskBase[list[str]]):
    def __init__(self, user_id: int):
        super().__init__()
        self._user_id = user_id

    async def _run(self, state: ExampleState[list[str]]) -> list[str]:
        client = PostClient(state.status)
        try:
            return await client.get_titles(self._user_id)
        finally:
            await client.aclose()
