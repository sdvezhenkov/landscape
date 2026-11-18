from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FileMeta:
    name: str | None
    type: str | None
    size: int | None

    @property
    def payload_kwargs(self) -> dict[str, str]:
        payload = dict[str, str]()
        if self.name:
            payload['filename'] = self.name
        if self.type:
            payload['content_type'] = self.type
        return payload
