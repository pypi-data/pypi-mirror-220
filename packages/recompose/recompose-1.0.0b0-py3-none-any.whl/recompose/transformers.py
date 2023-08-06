from typing import List, Type

from recompose.exceptions import NotATransformerType
from recompose.transformer import Transformer
from recompose.types import TransformSchema

_types: List[Type[Transformer]] = []


def find_transformer(schema: TransformSchema) -> Transformer:
    """
    Finds and returns the first transformer that fits a definition.
    """

    for t in _types:
        if schema.get("transform", "pass") == t.name():
            return t(schema.get("with"))

    raise NotATransformerType(schema.get("transform", "<none>"))


def register_transformer(transformer: Type[Transformer]) -> None:
    """
    Registers a transformer type.
    """

    _types.append(transformer)
