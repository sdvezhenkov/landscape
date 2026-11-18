from pydantic import BaseModel, ConfigDict


class TaskRegistryErrorConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    http_code: int
    ws_code: int
    detail: str
