from typing import overload


@overload
def deduplicate[T](
        items: list[T],
) -> list[T]:
    ...

@overload
def deduplicate[T](
        items: tuple[T, ...],
) -> tuple[T, ...]:
    ...

def deduplicate[T](
        items: list[T] | tuple[T, ...],
) -> list[T] | tuple[T, ...]:
    deduplicated = dict.fromkeys(items)
    if isinstance(items, list):
        return list(deduplicated)
    else:
        return tuple(deduplicated)
