from typing import List, Type

from recompose.exceptions import NotATransformerType
from recompose.transformer import Transformer
from recompose.types import AnyTransformSchema

_types: List[Type[Transformer]] = []


def find_transformer(
    schema: AnyTransformSchema,
) -> Transformer:
    """
    Finds and returns the first transformer that fits a definition.
    """

    name = schema.get("transform", "pass") if isinstance(schema, dict) else schema

    for t in _types:
        if name == t.name():
            config = schema if isinstance(schema, dict) else {}
            return t(config)

    raise NotATransformerType(name)


def register_transformer(transformer: Type[Transformer]) -> None:
    """
    Registers a transformer type.
    """

    _types.append(transformer)
