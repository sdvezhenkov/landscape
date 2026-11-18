from random import Random
from string import ascii_letters


def get_uniq_filecode(
        len_: int = 5,
        random_: Random | None = None,
) -> str:
    random_: Random = random_ or Random()
    file_code = ''.join(random_.choice(ascii_letters) for _ in range(len_))
    return file_code
