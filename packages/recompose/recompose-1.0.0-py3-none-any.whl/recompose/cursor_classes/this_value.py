from typing import Any

from recompose.cursor import Cursor


class ThisValue(Cursor):
    """
    A cursor that expects and yields a single value.
    """

    def _transform(self, data: Any) -> Any:
        for transformer in self.transformers:
            data = transformer.transform(data)

        return data

    @classmethod
    def condition(cls) -> str:
        return "this-value"
