import pytest

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError
from app.tools.essential.request.response.res_to_error import res_to_error
from app.tools.essential.request.response.tests.conftest import get_fake_response


@pytest.mark.parametrize(
    'status,message',
    [
        (200,b'test message'),
        (200,b''),
        (201,b'test message'),
    ],
)
async def test_res_to_error(
        status: int,
        message: bytes,
):
    res = get_fake_response(status, message)
    await res_to_error(res)

@pytest.mark.parametrize(
    'status,message',
    [
        (500,b'test message'),
        (500,b''),
        (501,b'test message'),
    ],
)
async def test_res_to_error_error(
        status: int,
        message: bytes,
):
    res = get_fake_response(status, message)
    with pytest.raises(RemoteServiceError) as e:
        await res_to_error(res)
    assert e.value.args[0] == message.decode()
