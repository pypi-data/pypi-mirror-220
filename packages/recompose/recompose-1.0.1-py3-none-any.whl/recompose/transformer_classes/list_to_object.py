from typing import Any

from recompose.transformer import Transformer


class ListToObject(Transformer):
    """
    Transforms a list into a single object.
    """

    def _transform(self, data: Any) -> Any:
        return data[0]

    @classmethod
    def name(cls) -> str:
        return "list-to-object"
