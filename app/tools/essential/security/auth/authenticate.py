import asyncio
from typing import Any

import anyio
import jwt
from fastapi import HTTPException, WebSocket, WebSocketException
from fastapi.requests import Request

from app.tools.essential.security.auth.types.principal import Principal
from app.tools.essential.security.auth.verifier import verifier


async def authenticate_http(
        request: Request,
) -> Principal:
    authorization = request.headers.get('authorization')
    if authorization is None:
        raise HTTPException(401, 'Authorization required', headers={'WWW-Authenticate': 'Bearer'})
    try:
        token = _get_token_by_header(authorization)
    except ValueError:
        raise HTTPException(401, 'Bearer token required', headers={'WWW-Authenticate': 'Bearer'})
    try:
        principal = await verifier.get_principal(token)
    except anyio.WouldBlock:
        raise HTTPException(503, 'Authentication temporarily unavailable', headers={'Retry-After': '1'})
    except jwt.PyJWTError:
        raise HTTPException(401, 'Invalid access token', headers={'WWW-Authenticate': 'Bearer'})
    return principal

async def authenticate_websocket(
        ws: WebSocket,
) -> Principal:
    authorization = ws.headers.get('authorization')
    if authorization is not None:
        principal = await _authenticate_websocket_by_authorization(ws)
    else:
        principal = await _authenticate_websocket_by_message(ws)
    return principal

async def _authenticate_websocket_by_authorization(
        ws: WebSocket,
) -> Principal:
    authorization = ws.headers.get('authorization')
    if not authorization:
        raise WebSocketException(code=1008, reason='Bearer token required')
    try:
        token = _get_token_by_header(authorization)
    except ValueError:
        raise WebSocketException(code=1008, reason='Bearer token required')
    try:
        principal = await verifier.get_principal(token)
    except anyio.WouldBlock:
        raise WebSocketException(code=1013, reason='Authentication temporarily unavailable')
    except jwt.PyJWTError:
        raise WebSocketException(code=1008, reason='Invalid access token')
    await ws.accept()
    return principal

async def _authenticate_websocket_by_message(
        ws: WebSocket,
) -> Principal:
    await ws.accept()
    try:
        payload = await asyncio.wait_for(ws.receive_json(), timeout=10)
        token = _get_token_by_message(payload)
    except TimeoutError:
        raise WebSocketException(code=1008, reason='Authentication timed out')
    except ValueError:
        raise WebSocketException(code=1008, reason='Invalid authentication message')
    try:
        principal = await verifier.get_principal(token)
    except anyio.WouldBlock:
        raise WebSocketException(code=1013, reason='Authentication temporarily unavailable')
    except jwt.PyJWTError:
        raise WebSocketException(code=1008, reason='Invalid access token')
    return principal

def _get_token_by_header(
        authorization: str,
) -> str:
    scheme, separator, token = authorization.partition(' ')
    scheme = scheme.lower()
    token = token.strip()
    if (
        scheme == 'bearer' and
        separator and
        token
    ):
        return token
    else:
        raise ValueError('Invalid authorization value')

def _get_token_by_message(
        payload: Any,
) -> str:
    if (
        not isinstance(payload, dict) or
        not payload.get('type') == 'auth'
    ):
        raise ValueError('First message must be auth')
    token = payload.get('token')
    if not token or not isinstance(token, str):
        raise ValueError('Invalid auth token')
    return token
