from dataclasses import dataclass
from textwrap import dedent
from typing import Any

from pydantic import BaseModel, RootModel


@dataclass(frozen=True, slots=True)
class SerializeCase:
    value: Any
    dump: str


class CompositeModel(BaseModel):
    a: int
    b: dict[str, str]
    c: TestModel


class TestModel(BaseModel):
    a: int
    b: list[str]


FLAT_MODEL = SerializeCase(
    value=TestModel(
        a=1,
        b=[],
    ),
    dump=dedent('''
        TestModel(
            a=1,
            b=[],
        )
    ''').strip(),
)
COMPOSITE_MODEL = SerializeCase(
    value=CompositeModel(
        a=1,
        b={
            'd': '2',
            'e': '3',
        },
        c=TestModel(
            a=1,
            b=[
                'd,e',
                'f(d,e)',
            ],
        ),
    ),
    dump=dedent('''
        CompositeModel(
            a=1,
            b={
                'd': '2',
                'e': '3',
            },
            c=TestModel(
                a=1,
                b=[
                    'd,e',
                    'f(d,e)',
                ],
            ),
        )
    ''').strip(),
)


class TestRootModel(RootModel[list[str]]):
    root: list[str]


ROOT_MODEL = SerializeCase(
    value=TestRootModel(
        root=[
            '1',
            '2',
            '3',
        ],
    ),
    dump=dedent('''
        TestRootModel(
            root=[
                '1',
                '2',
                '3',
            ],
        )
    ''').strip(),
)

LIST = SerializeCase(
    value=[
        '1',
        '2',
        '3',
    ],
    dump=dedent('''
        [
            '1',
            '2',
            '3',
        ]
    ''').strip(),
)
