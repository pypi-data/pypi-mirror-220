from abc import ABC, abstractmethod
from typing import Any, Iterable

from recompose.logging import log
from recompose.transformer import Transformer
from recompose.transformers import find_transformer
from recompose.types import CursorSchema


class Cursor(ABC):
    """
    Cursor.
    """

    def __init__(
        self,
        schema: CursorSchema,
    ) -> None:
        self._schema = schema

    def __str__(self) -> str:
        return self.condition()

    @abstractmethod
    def _transform(self, data: Any) -> Any:
        """
        Transforms and returns the data.
        """

    @classmethod
    @abstractmethod
    def condition(cls) -> str:
        """
        Key.
        """

    def transform(self, data: Any) -> Any:
        """
        Transforms and returns the data.
        """

        log.debug("%s started transforming %s", self, data)
        return self._transform(data)

    @property
    def transformers(self) -> Iterable[Transformer]:
        """
        Yields each transformer.
        """

        if isinstance(self._schema["perform"], list):
            for transform in self._schema["perform"]:
                yield find_transformer(transform)
        else:
            yield find_transformer(self._schema["perform"])
