import re
from random import Random

from app.tools.essential.request.file.filename.get_inbody_filename import get_uniq_filecode


def test_get_uniq_filecode():
    passed_len = 5
    random_ = Random(1)
    filecode = get_uniq_filecode(passed_len, random_)
    assert len(filecode) == passed_len
    assert re.match('[a-zA-Z]', filecode)
