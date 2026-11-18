import socket
from collections.abc import AsyncIterator, Iterator
from time import time

import pytest
from aiohttp import web
from fastapi import FastAPI, WebSocket
from fastapi.requests import HTTPConnection


@pytest.fixture
async def example_api(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[list[tuple[str, str | None]]]:
    requests: list[tuple[str, str | None]] = []

    async def users(request: web.Request) -> web.Response:
        requests.append((request.path, None))
        return web.json_response([
            {'id': 1, 'name': ' Alice   Example '},
            {'id': 2, 'name': 'Bob\tExample'},
        ])

    async def posts(request: web.Request) -> web.Response:
        user_id = request.query['userId']
        requests.append((request.path, user_id))
        if user_id == '999':
            return web.json_response([{'id': 1}])
        return web.json_response([
            {'id': 1, 'userId': int(user_id), 'title': ' First   post '},
            {'id': 2, 'userId': int(user_id), 'title': 'Second\npost'},
        ])

    app = web.Application()
    app.router.add_get('/users', users)
    app.router.add_get('/posts', posts)
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            port = listener.getsockname()[1]
            site = web.SockSite(runner, listener)
            await site.start()
            monkeypatch.setenv('LSC_EXAMPLE_API_URL', f'http://127.0.0.1:{port}')
            yield requests
    finally:
        await runner.cleanup()


@pytest.fixture
def application(monkeypatch: pytest.MonkeyPatch) -> Iterator[FastAPI]:
    settings = {
        'LSC_PROJECT_NAME': 'landscape',
        'LSC_DB_USERNAME': 'example',
        'LSC_DB_PASSWORD': 'example',
        'LSC_DB_HOST': 'localhost',
        'LSC_DB_NAME': 'example',
        'LSC_OIDC_ISSUER': 'https://identity.example/realms/example',
        'LSC_OIDC_AUDIENCE': 'landscape',
        'LSC_OIDC_JWKS_URL': 'https://identity.example/realms/example/certs',
        'LSC_OAUTH_CLIENT_ID': 'landscape-swagger',
    }
    for key, value in settings.items():
        monkeypatch.setenv(key, value)

    import main
    from app.tools.essential.docs.oauth2 import SCOPES
    from app.tools.essential.security.auth.dependencies import require_auth
    from app.tools.essential.security.auth.types.principal import Principal

    async def initialize_database() -> None:
        pass

    async def authenticate(connection: HTTPConnection) -> None:
        if isinstance(connection, WebSocket):
            await connection.accept()
        connection.state.principal = Principal(
            subject='example-client',
            issuer=settings['LSC_OIDC_ISSUER'],
            scopes=frozenset(SCOPES),
            expires_at=int(time()) + 60,
            client_id='example-client',
        )

    monkeypatch.setattr(main, 'create_db_and_tables', initialize_database)
    main.app.dependency_overrides[require_auth] = authenticate
    try:
        yield main.app
    finally:
        main.app.dependency_overrides.clear()
