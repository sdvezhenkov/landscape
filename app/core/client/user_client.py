from app.core.api.user_api import UserAPI
from app.core.tools.task.types.example_state import ExampleStatus
from app.core.tools.text.normalize_text import normalize_text


class UserClient:
    def __init__(self, status: ExampleStatus):
        self.status = status
        self._api = UserAPI()

    async def aclose(self) -> None:
        await self._api.aclose()

    async def get_names(self) -> list[str]:
        users = await self._api.get_users()
        self.status.overall.set(len(users))
        names = list[str]()
        for user in users:
            names.append(normalize_text(user.name))
            self.status.current.inc()
        return names
