import re
from typing import Any

DEFAULT_INDENT = 4

class Serializer:
    def __init__(
        self,
        value: Any,
        indent: int = DEFAULT_INDENT,
    ):
        self._value = value
        self._quote: str | None = None
        self._escaped = False
        self._level = 0
        self._indent = indent

    def dump(self) -> str:
        source = repr(self._value)
        dump = ''
        for char in source:
            dump += self._dump_char(char)
        dump = self._collapse_empty_containers(dump)
        dump = self._add_trailing_commas(dump)
        return dump

    def _dump_char(
        self,
        char: str,
    ) -> str:
        if self._quote is not None:
            if char == self._quote and not self._escaped:
                self._quote = None
            self._escaped = (char == '\\') and not self._escaped
            return char
        if char in "'\"":
            self._quote = char
            return char
        return self._dump_non_string_char(char)

    def _dump_non_string_char(
            self,
            char: str,
    ) -> str:
        match char:
            case '(' | '[' | '{':
                self._level += 1
                return f'{char}\n{' ' * (self._level * self._indent)}'
            case ')' | ']' | '}':
                self._level -= 1
                return f'\n{' ' * (self._level * self._indent) + char}'
            case ',':
                return f',\n{' ' * (self._level * self._indent - 1)}'
            case _:
                return char

    # noinspection RegExpRedundantEscape
    def _collapse_empty_containers(
            self,
            dump: str,
    ) -> str:
        dump = re.sub(
            r'\[\s*\]',
            '[]',
            dump,
        )
        dump = re.sub(
            r'\{\s*\}',
            '{}',
            dump,
        )
        dump = re.sub(
            r'\(\s*\)',
            '()',
            dump,
        )
        return dump

    def _add_trailing_commas(
        self,
        dump: str,
    ) -> str:
        dump = re.sub(
            r'(?m)([^([{,\n])$',
            r'\1,',
            dump,
        )
        dump = dump.removesuffix(',')
        return dump


def serialize(
    value: Any,
) -> str:
    serializer = Serializer(value)
    dump = serializer.dump()
    return dump
