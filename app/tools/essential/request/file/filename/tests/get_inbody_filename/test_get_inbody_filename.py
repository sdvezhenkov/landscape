import re

import pytest

from app.tools.essential.request.file.filename.get_inbody_filename import get_inbody_filename
from app.tools.essential.request.file.filename.tests.get_inbody_filename.cases import *


@pytest.mark.parametrize(
    'case',
    [
        FILENAME,
        FILENAME_SPEC_SYMBOLS,
        FILENAME_EMPTY_TITLE,
        FILENAME_EMPTY,
    ],
)
def test_get_inbody_filename(case: GetInbodyFilenameCase):
    inbody_filename = get_inbody_filename(
        case.filename,
        case.codelen,
        case.sep,
        case.random,
    )
    assert re.fullmatch(
        case.inbody_filename_pattern,
        inbody_filename,
    )
