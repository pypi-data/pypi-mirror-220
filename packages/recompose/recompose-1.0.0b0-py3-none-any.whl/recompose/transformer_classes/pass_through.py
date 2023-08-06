from typing import Any

from recompose.cursors import make_cursor
from recompose.logging import log
from recompose.transformer import Transformer
from recompose.with_readers import WithCursorSchemaReader, WithPathReader


class Pass(Transformer):
    """
    Passes transformation to child data.
    """

    def _transform(self, data: Any) -> Any:
        cursor_schema = WithCursorSchemaReader.get_required(self.with_args)

        cursor = make_cursor(
            cursor_schema,
            require_version=False,
        )

        path = WithPathReader.get_required(self.with_args)
        child_data = data[path]

        log.debug('%s will transform %s from path "%s"', self, child_data, path)
        transformed = cursor.transform(child_data)

        return {
            **data,
            path: transformed,
        }

    @classmethod
    def name(cls) -> str:
        return "pass"
