from typing import Any

from recompose.exceptions import InvalidSchema
from recompose.schema_reader import SchemaReader


class PathReader(SchemaReader[str]):
    @classmethod
    def cast(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise InvalidSchema.incorrect_type(
                cls.key(),
                str,
                value,
            )

        return value

    @classmethod
    def key(cls) -> str:
        return "path"
