from typing import Any, cast

from recompose.exceptions import InvalidSchema
from recompose.schema_reader import SchemaReader
from recompose.types import CursorSchema


class CursorSchemaReader(SchemaReader[CursorSchema]):
    @classmethod
    def cast(cls, value: Any) -> CursorSchema:
        if not isinstance(value, dict):
            raise InvalidSchema.incorrect_type(
                cls.key(),
                dict,
                value,
            )

        return cast(CursorSchema, value)

    @classmethod
    def key(cls) -> str:
        return "cursor"
