import pytest

from app.tools.essential.serialization.serialize import serialize
from app.tools.essential.serialization.tests.cases import COMPOSITE_MODEL, FLAT_MODEL, LIST, ROOT_MODEL, SerializeCase


@pytest.mark.parametrize(
    'case',
    [
        FLAT_MODEL,
        COMPOSITE_MODEL,
        ROOT_MODEL,
        LIST,
    ],
)
def test_dump_model(
        case: SerializeCase,
):
    dump = serialize(case.value)
    assert dump == case.dump
