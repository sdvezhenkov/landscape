from app.core.api.types.user import User
from app.tools.essential.cache.cache import cache
from app.tools.essential.env.get_env import get_env
from app.tools.essential.request.response.res_to_model import res_to_model
from app.tools.essential.request.session.retry.retry_session.get_retry_session import get_retry_session


class UserAPI:
    def __init__(self):
        self.url = get_env('LSC_EXAMPLE_API_URL', 'https://jsonplaceholder.typicode.com').rstrip('/')
        self.session = get_retry_session()

    async def aclose(self) -> None:
        await self.session.close()

    @cache.memoize()
    async def get_users(self) -> list[User]:
        async with self.session.get(f'{self.url}/users') as response:
            return await res_to_model(response, list[User])
