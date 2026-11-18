import pytest

from app.tools.essential.request.accumulate.accumulate import accumulate
from app.tools.essential.request.accumulate.tests.types.paginated import Paginated

ROWS = [1, 2, 3]

@pytest.mark.parametrize(
    'total',
    list[int](range(3)),
)
async def test_accumulate(
        total: int,
):
    async def get_page(
            page_number: int,
    ) -> Paginated[int]:
        assert 1 <= page_number <= total + 1
        rows: list[int] = ROWS if page_number <= total else []
        page = Paginated[int](
            total=total,
            rows=rows,
        )
        return page

    accumulated = await accumulate(
        lambda page: get_page(page),
    )

    assert type(accumulated) is Paginated[int]
    assert accumulated.total == total
    assert accumulated.rows == ROWS * total
