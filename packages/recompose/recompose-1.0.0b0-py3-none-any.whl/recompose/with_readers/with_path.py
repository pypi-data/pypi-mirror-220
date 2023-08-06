from typing import Any

from recompose.exceptions import InvalidSchema
from recompose.with_reader import WithReader


class WithPathReader(WithReader[str]):
    @classmethod
    def key(cls) -> str:
        return "path"

    @classmethod
    def cast(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise InvalidSchema.incorrect_type(
                cls.key(),
                str,
                value,
            )

        return value
