from dataclasses import dataclass, field
from random import Random


@dataclass(frozen=True, slots=True)
class GetInbodyFilenameCase:
    filename: str
    inbody_filename_pattern: str
    sep: str = '-'
    codelen: int = 5
    random: Random = field(default_factory=lambda: Random(1))


FILENAME = GetInbodyFilenameCase(
    filename='TestName.pdf',
    inbody_filename_pattern=r'TestName-[a-zA-Z]{5}\.pdf',
)
FILENAME_SPEC_SYMBOLS = GetInbodyFilenameCase(
    filename='Тест$ ?Нейм_.pdf',
    inbody_filename_pattern=r'Test_ _Nejm_-[a-zA-Z]{5}\.pdf',
)
FILENAME_EMPTY_TITLE = GetInbodyFilenameCase(
    filename='.pdf',
    inbody_filename_pattern=r'\.pdf-[a-zA-Z]{5}',
)
FILENAME_EMPTY = GetInbodyFilenameCase(
    filename='',
    inbody_filename_pattern=r'-[a-zA-Z]{5}',
)
