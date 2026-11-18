from aiohttp import ClientResponse
from pydantic import TypeAdapter

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError


async def res_to_model[T](
        res: ClientResponse,
        model: type[T],
) -> T:
    if not res.ok:
        text = await res.text()
        raise RemoteServiceError(
            status=res.status,
            message=text,
        )
    json = await res.json()
    type_adapter: TypeAdapter[T] = TypeAdapter(model)
    model_object = type_adapter.validate_python(json)
    return model_object
