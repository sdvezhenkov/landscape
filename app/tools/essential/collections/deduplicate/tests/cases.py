from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeduplicateListCase:
    items: list
    deduplicated: list


LIST = DeduplicateListCase(
    items=[3, 2, 1, 1, 2, 3],
    deduplicated=[3, 2, 1],
)
EMPTY_LIST = DeduplicateListCase(
    items=[],
    deduplicated=[],
)


@dataclass(frozen=True, slots=True)
class DeduplicateTupleCase:
    items: tuple
    deduplicated: tuple


TUPLE = DeduplicateTupleCase(
    items=(3, 2, 1, 1, 2, 3),
    deduplicated=(3, 2, 1),
)
EMPTY_TUPLE = DeduplicateTupleCase(
    items=(),
    deduplicated=(),
)
