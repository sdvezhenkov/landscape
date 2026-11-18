from collections.abc import Awaitable, Callable

from app.tools.essential.request.accumulate.types.paginated_base import PaginatedBase


async def accumulate[T, P: PaginatedBase](
        get_page: Callable[[int], Awaitable[P]],
) -> P:
    page = 1
    overall_rows = list[T]()
    while True:
        paginated: P = await get_page(page)
        rows: list[T] = paginated.rows
        if rows:
            overall_rows += rows
        else:
            break
        page += 1
    paginated.rows = overall_rows
    return paginated
