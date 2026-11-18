import pytest

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError
from app.tools.essential.request.response.res_to_filemeta import res_to_filemeta
from app.tools.essential.request.response.tests.conftest import FakeContentDisposition, get_fake_file_response

TEST_MESSAGE = b'test message'

async def test_res_to_filemeta_200():
    content_disposition = FakeContentDisposition('test.txt', 'attachment')
    res = get_fake_file_response(200, TEST_MESSAGE, content_disposition)
    filemeta = await res_to_filemeta(res)
    assert filemeta.payload_kwargs == {
        'filename': 'test.txt',
        'content_type': 'attachment',
    }
    assert filemeta.size == len(TEST_MESSAGE)

async def test_res_to_filemeta_200_half_empty():
    content_disposition = FakeContentDisposition('test.txt', '')
    res = get_fake_file_response(200, TEST_MESSAGE, content_disposition)
    filemeta = await res_to_filemeta(res)
    assert filemeta.payload_kwargs == {
        'filename': 'test.txt',
    }
    assert filemeta.size == len(TEST_MESSAGE)

async def test_res_to_filemeta_200_empty():
    content_disposition = FakeContentDisposition('', '')
    res = get_fake_file_response(200, TEST_MESSAGE, content_disposition)
    filemeta = await res_to_filemeta(res)
    assert filemeta.payload_kwargs == {}
    assert filemeta.size == len(TEST_MESSAGE)

async def test_res_to_filemeta_200_none():
    content_disposition = FakeContentDisposition(None, None)
    res = get_fake_file_response(200, TEST_MESSAGE, content_disposition)
    filemeta = await res_to_filemeta(res)
    assert filemeta.payload_kwargs == {}
    assert filemeta.size == len(TEST_MESSAGE)

async def test_res_to_filemeta_200_content_disposition_none():
    content_disposition = None
    res = get_fake_file_response(200, TEST_MESSAGE, content_disposition)
    filemeta = await res_to_filemeta(res)
    assert filemeta.payload_kwargs == {}
    assert filemeta.size == len(TEST_MESSAGE)

async def test_res_to_filemeta_201():
    content_disposition = FakeContentDisposition('test.txt', 'attachment')
    res = get_fake_file_response(201, TEST_MESSAGE, content_disposition)
    filemeta = await res_to_filemeta(res)
    assert filemeta.payload_kwargs == {
        'filename': 'test.txt',
        'content_type': 'attachment',
    }
    assert filemeta.size == len(TEST_MESSAGE)

async def test_res_to_filemeta_500_error():
    content_disposition = FakeContentDisposition('test.txt', 'attachment')
    res = get_fake_file_response(500, TEST_MESSAGE, content_disposition)
    with pytest.raises(RemoteServiceError) as e:
        await res_to_filemeta(res)
    assert e.value.args[0] == TEST_MESSAGE.decode()
