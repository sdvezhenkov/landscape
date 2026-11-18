import asyncio
from collections.abc import AsyncIterator
from time import time
from typing import Annotated

from fastapi import Depends, HTTPException, WebSocketException
from fastapi.requests import HTTPConnection, Request
from fastapi.security import SecurityScopes
from fastapi.websockets import WebSocket

from app.tools.essential.docs.oauth2 import oauth2
from app.tools.essential.security.auth.authenticate import authenticate_http, authenticate_websocket
from app.tools.essential.security.auth.types.principal import Principal


async def require_token_lifetime(
        connection: HTTPConnection,
        _auth: Annotated[None, Depends(require_auth)],
) -> AsyncIterator[None]:
    if not isinstance(connection, WebSocket):
        yield
        return

    principal = principal_of(connection)
    remaining = principal.expires_at - time()
    if remaining <= 0:
        raise WebSocketException(code=1008, reason='Access token expired')

    deadline = asyncio.timeout(remaining)
    try:
        async with deadline:
            yield
    except TimeoutError:
        if not deadline.expired():
            raise
        raise WebSocketException(code=1008, reason='Access token expired')

async def require_auth(
        connection: HTTPConnection,
) -> None:
    if isinstance(connection, WebSocket):
        principal = await authenticate_websocket(connection)
    elif isinstance(connection, Request):
        principal = await authenticate_http(connection)
    else:
        raise TypeError("Unsupported connection type")
    connection.state.principal = principal

async def require_scopes(
    connection: HTTPConnection,
    security_scopes: SecurityScopes,
    _token: Annotated[str | None, Depends(oauth2)],
) -> None:
    principal = principal_of(connection)
    if not set(security_scopes.scopes).issubset(principal.scopes):
        if isinstance(connection, WebSocket):
            raise WebSocketException(
                code=1008,
                reason="Insufficient scope",
            )
        else:
            raise HTTPException(
                status_code=403,
                detail="Insufficient scope",
            )

def principal_of(
        connection: HTTPConnection,
) -> Principal:
    principal: Principal | None = getattr(connection.state, 'principal', None)
    if principal is None:
        raise RuntimeError('Authentication dependency missing: use protected root router')
    return principal
