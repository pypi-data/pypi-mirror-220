"""
Recompose is a Python package for templated data recomposition.
"""

from importlib.resources import open_text

import recompose.cursor_classes
import recompose.transformer_classes
from recompose.cursors import make_cursor, register_cursor
from recompose.exceptions import (
    InvalidSchema,
    NoCursorForCondition,
    NotATransformerType,
    RecomposeError,
    UnsupportedVersion,
)
from recompose.transformer import Transformer
from recompose.transformers import find_transformer, register_transformer

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()


register_cursor(recompose.cursor_classes.EachValue)
register_cursor(recompose.cursor_classes.ThisValue)

register_transformer(recompose.transformer_classes.ListToObject)
register_transformer(recompose.transformer_classes.Pass)


__all__ = [
    "InvalidSchema",
    "NoCursorForCondition",
    "NotATransformerType",
    "RecomposeError",
    "Transformer",
    "UnsupportedVersion",
    "make_cursor",
    "find_transformer",
]
