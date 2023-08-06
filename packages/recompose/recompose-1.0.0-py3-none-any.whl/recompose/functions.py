from typing import Any

from recompose.cursors import make_cursor
from recompose.types import CursorSchema


def transform(schema: CursorSchema, data: Any) -> Any:
    """
    Transforms and returns `data` according to `schema`.
    """

    cursor = make_cursor(schema)
    return cursor.transform(data)
