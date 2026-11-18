from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    subject: str
    issuer: str
    scopes: frozenset[str]
    expires_at: int
    client_id: str | None
