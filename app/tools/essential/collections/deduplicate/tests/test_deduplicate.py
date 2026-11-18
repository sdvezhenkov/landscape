import pytest

from app.tools.essential.collections.deduplicate.deduplicate import deduplicate
from app.tools.essential.collections.deduplicate.tests.cases import *


@pytest.mark.parametrize(
    'case',
    [
        LIST,
        EMPTY_LIST,
    ],
)
def test_deduplicate_list(case: DeduplicateListCase):
    deduplicated_list = deduplicate(case.items)
    assert type(deduplicated_list) is list
    assert deduplicated_list == case.deduplicated

@pytest.mark.parametrize(
    'case',
    [
        TUPLE,
        EMPTY_TUPLE,
    ],
)
def test_deduplicate_list_error(case: DeduplicateTupleCase):
    deduplicated_list = deduplicate(case.items)
    assert type(deduplicated_list) is tuple
    assert deduplicated_list == case.deduplicated
