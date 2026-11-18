from json import JSONDecodeError

import pytest
from pydantic import BaseModel, ValidationError

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError
from app.tools.essential.request.response.res_to_model import res_to_model
from app.tools.essential.request.response.tests.conftest import get_fake_response


class Type1(BaseModel):
    a: int = 1
    b: dict


async def test_res_to_model_200():
    res = get_fake_response(200, b'{"a": 1, "b": {}}')
    test_model = await res_to_model(res, Type1)
    assert type(test_model) is Type1
    assert test_model.a == 1
    assert test_model.b == {}

async def test_res_to_model_200_error():
    res = get_fake_response(200, b'{"a": 1, "b": []}')
    with pytest.raises(ValidationError):
        await res_to_model(res, Type1)

async def test_res_to_model_200_half_empty():
    res = get_fake_response(200, b'{"a": 1}')
    with pytest.raises(ValidationError):
        await res_to_model(res, Type1)

async def test_res_to_model_200_empty():
    res = get_fake_response(200, b'')
    with pytest.raises(JSONDecodeError):
        await res_to_model(res, Type1)

async def test_res_to_model_201():
    res = get_fake_response(201, b'{"a": 1, "b": {}}')
    test_model = await res_to_model(res, Type1)
    assert type(test_model) is Type1
    assert test_model.a == 1
    assert test_model.b == {}

async def test_res_to_model_500_error():
    res = get_fake_response(500, b'{"a": 1, "b": {}}')
    with pytest.raises(RemoteServiceError) as e:
        await res_to_model(res, Type1)
    assert e.value.args[0] == b'{"a": 1, "b": {}}'.decode()
