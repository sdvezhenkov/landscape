from pydantic import BaseModel


class PaginatedBase(BaseModel):
    rows: list
