import asyncio
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect


def receive_result(client: TestClient, state_url: str) -> dict:
    with client.websocket_connect(state_url) as websocket:
        while True:
            state = websocket.receive_json()
            if state['status']['stage'] in ('success', 'failure'):
                break
        with pytest.raises(WebSocketDisconnect) as closed:
            websocket.receive_json()
        assert closed.value.code == 1000
    return state


@pytest.mark.parametrize(
    ('route', 'body', 'expected', 'expected_request'),
    [
        ('user_names', None, ['Alice Example', 'Bob Example'], ('/users', None)),
        ('post_titles', {'user_id': 1}, ['First post', 'Second post'], ('/posts', '1')),
    ],
)
async def test_example_task(application: FastAPI, example_api, route, body, expected, expected_request):
    def run_scenario() -> None:
        with TestClient(application) as client:
            response = client.post(f'/{route}/', json=body)
            assert response.status_code == 200
            state_url = f'/{route}/state/{response.json()}'
            state = receive_result(client, state_url)
            assert state['status'] == {'stage': 'success', 'current': 2, 'overall': 2}
            assert state['result'] == expected
            assert client.get(state_url).json() == state
            assert receive_result(client, state_url) == state

    await asyncio.to_thread(run_scenario)
    assert example_api == [expected_request]


async def test_invalid_source_response(application: FastAPI, example_api):
    def run_scenario() -> None:
        with TestClient(application) as client:
            response = client.post('/post_titles/', json={'user_id': 999})
            assert response.status_code == 200
            state_url = f'/post_titles/state/{response.json()}'
            state = receive_result(client, state_url)
            assert state['status']['stage'] == 'failure'
            assert state['result'] is None
            assert client.get(state_url).json() == state
            assert receive_result(client, state_url) == state

    await asyncio.to_thread(run_scenario)
    assert example_api == [('/posts', '999')]


async def test_missing_task(application: FastAPI):
    def run_scenario() -> None:
        with TestClient(application) as client:
            state_url = f'/user_names/state/{uuid4()}'
            response = client.get(state_url)
            assert response.status_code == 404
            with (
                pytest.raises(WebSocketDisconnect) as closed,
                client.websocket_connect(state_url) as websocket,
            ):
                websocket.receive_json()
            assert closed.value.code == 1008

    await asyncio.to_thread(run_scenario)
