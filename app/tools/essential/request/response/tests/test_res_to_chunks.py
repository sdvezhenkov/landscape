from inspect import isasyncgen

import pytest

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError
from app.tools.essential.request.response.res_to_chunks import res_to_chunks
from app.tools.essential.request.response.tests.conftest import get_fake_response


@pytest.mark.parametrize(
    'status,message',
    [
        (200,b'test message'),
        (200,b''),
        (201,b'test message'),
    ],
)
async def test_res_to_chunks(
        status: int,
        message: bytes,
):
    res = get_fake_response(status, message)
    chunks = res_to_chunks(res)
    assert isasyncgen(chunks)
    assert (await anext(chunks)) == message
    with pytest.raises(StopAsyncIteration):
        await anext(chunks)

@pytest.mark.parametrize(
    'status,message',
    [
        (500,b'test message'),
        (500,b''),
        (501,b'test message'),
    ],
)
async def test_res_to_chunks_error(
        status: int,
        message: bytes,
):
    test_message = b'test message'
    res = get_fake_response(500, test_message)
    chunks = res_to_chunks(res)
    assert isasyncgen(chunks)
    with pytest.raises(RemoteServiceError) as e:
        await anext(chunks)
    assert e.value.args[0] == test_message.decode()
