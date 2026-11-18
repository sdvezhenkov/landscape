from app.tools.essential.request.accumulate.types.paginated_base import PaginatedBase


class Paginated[T](PaginatedBase):
    total: int
    rows: list[T]
