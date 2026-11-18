from app.core.api.post_api import PostAPI
from app.core.tools.task.types.example_state import ExampleStatus
from app.core.tools.text.normalize_text import normalize_text


class PostClient:
    def __init__(self, status: ExampleStatus):
        self.status = status
        self._api = PostAPI()

    async def aclose(self) -> None:
        await self._api.aclose()

    async def get_titles(self, user_id: int) -> list[str]:
        posts = await self._api.get_posts(user_id)
        self.status.overall.set(len(posts))
        titles = list[str]()
        for post in posts:
            titles.append(normalize_text(post.title))
            self.status.current.inc()
        return titles
