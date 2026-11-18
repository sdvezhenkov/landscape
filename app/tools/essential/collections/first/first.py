

def first[T](
        list_: list[T],
) -> T | None:
    first_item = list_[0] if list_ else None
    return first_item
