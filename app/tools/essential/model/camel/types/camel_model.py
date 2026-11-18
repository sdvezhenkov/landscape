from typing import ClassVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(alias_generator=to_camel)
