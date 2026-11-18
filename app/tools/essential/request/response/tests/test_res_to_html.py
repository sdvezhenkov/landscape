import pytest

from app.tools.essential.request.response.errors.remote_service_error import RemoteServiceError
from app.tools.essential.request.response.res_to_html import res_to_html
from app.tools.essential.request.response.tests.conftest import get_fake_response

TEST_ID_TEXT = 'test message'
TEST_MESSAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div id='test-id'>{TEST_ID_TEXT}</div>
</body>
</html>
'''.encode()

@pytest.mark.parametrize(
    'status,message',
    [
        (200,TEST_MESSAGE),
        (201,TEST_MESSAGE),
    ],
)
async def test_res_to_html_200(
        status: int,
        message: bytes,
):
    res = get_fake_response(status, message)
    html = await res_to_html(res)
    test_id_element = html.find(id='test-id')
    assert test_id_element is not None
    assert test_id_element.text == TEST_ID_TEXT

@pytest.mark.parametrize(
    'status,message',
    [
        (200,b''),
        (500,TEST_MESSAGE),
        (501,TEST_MESSAGE),
    ],
)
async def test_res_to_html_error(
        status: int,
        message: bytes,
):
    res = get_fake_response(500, TEST_MESSAGE)
    with pytest.raises(RemoteServiceError) as e:
        await res_to_html(res)
    assert e.value.args[0] == TEST_MESSAGE.decode()
