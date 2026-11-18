from app.tools.essential.collections.first.first import first


def test_first():
    list_: list[int] = [1, 2, 3]
    first_item = first(list_)
    assert type(first_item) is int
    assert first_item == 1

def test_first_empty():
    list_: list[int] = []
    first_item = first(list_)
    assert first_item is None
