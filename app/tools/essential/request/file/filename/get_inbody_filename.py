import re
from pathlib import Path
from random import Random

from transliterate import translit

from app.tools.essential.request.file.filename.get_uniq_filecode import get_uniq_filecode


def get_inbody_filename(
        filename: str,
        filecode_len: int = 5,
        sep: str = '-',
        random_: Random | None = None,
) -> str:
    random_: Random = random_ or Random()
    inbody_filename: str = filename
    inbody_filename = translit(Path(inbody_filename).stem, 'ru', reversed=True)
    inbody_filename = inbody_filename.replace('\'', '')
    inbody_filename = re.sub('[^a-zA-Z0-9_ .,()-]', '_', inbody_filename)
    inbody_filename += f'{sep}{get_uniq_filecode(filecode_len, random_)}'
    inbody_filename += Path(filename).suffix
    return inbody_filename
