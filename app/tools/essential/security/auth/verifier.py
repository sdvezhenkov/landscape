from datetime import UTC, datetime
from typing import Any

import anyio
import jwt
from anyio import CapacityLimiter
from jwt import PyJWKClient

from app.tools.essential.env.get_env import get_env
from app.tools.essential.security.auth.types.principal import Principal

DEFAULT_MAX_TOKEN_LENGTH = 8192
DEFAULT_CAPACITY_LIMIT = 8

class OIDCVerifier:
    def __init__(
            self,
            issuer: str,
            audience: str,
            jwks_url: str,
    ):
        self.issuer = issuer.rstrip('/')
        self.audience = audience
        self.jwks = PyJWKClient(jwks_url)
        self.max_token_length = DEFAULT_MAX_TOKEN_LENGTH
        self._limiter = CapacityLimiter(DEFAULT_CAPACITY_LIMIT)

    async def get_principal(
            self,
            token: Any,
    ) -> Principal:
        self._limiter.acquire_nowait()
        try:
            principal = await anyio.to_thread.run_sync(self._get_principal, token)
        finally:
            self._limiter.release()
        return principal

    def is_token_expired(
        self,
        principal: Principal,
    ) -> bool:
        return datetime.now(UTC).timestamp() >= principal.expires_at

    def _get_principal(
            self,
            token: Any,
    ) -> Principal:
        if (
            not isinstance(token, str) or
            not token or
            len(token) > self.max_token_length
        ):
            raise jwt.InvalidTokenError("Invalid token")
        key = self.jwks.get_signing_key_from_jwt(token)
        decoded = jwt.decode_complete(
            jwt=token,
            key=key.key,
            algorithms=["RS256"],
            issuer=self.issuer,
            audience=self.audience,
            options={"require": ["iss", "sub", "aud", "exp", "iat"]},
        )
        header = decoded['header']
        claims = decoded['payload']
        try:
            self._get_typ(header)
            principal = Principal(
                subject=claims["sub"],
                issuer=claims["iss"],
                scopes=self._get_scopes(claims),
                expires_at=int(claims["exp"]),
                client_id=self._get_client_id(claims),
            )
        except (ValueError, TypeError) as exc:
            raise jwt.InvalidTokenError("Invalid token claims") from exc
        return principal

    def _get_typ(
            self,
            header: dict[str, Any],
    ) -> str:
        typ = header.get("typ")
        if typ not in (
            "at+jwt",
            "application/at+jwt",
        ):
            raise jwt.InvalidTokenError("Not an access token")
        else:
            return typ

    def _get_scopes(
            self,
            claims: dict[str, Any],
    ) -> frozenset[str]:
        claims_scope = claims.get("scope", "")
        if isinstance(claims_scope, str):
            scopes = frozenset(claims_scope.split())
            return scopes
        else:
            raise jwt.InvalidTokenError("Invalid scope claim")

    def _get_client_id(
            self,
            claims: dict[str, Any],
    ) -> str | None:
        client_id: str | None = claims.get("azp") or claims.get("client_id")
        if type(client_id) not in (str, None):
            raise jwt.InvalidTokenError("Invalid client_id claim")
        return client_id


verifier = OIDCVerifier(
    issuer=get_env('LSC_OIDC_ISSUER'),
    audience=get_env('LSC_OIDC_AUDIENCE'),
    jwks_url=get_env('LSC_OIDC_JWKS_URL'),
)
