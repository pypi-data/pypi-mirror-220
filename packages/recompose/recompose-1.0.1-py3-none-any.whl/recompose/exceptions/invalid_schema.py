from __future__ import annotations

from typing import Any, Dict, Optional, Type

from recompose.exceptions.recompose import RecomposeError


class InvalidSchema(RecomposeError):
    """
    Raised when a schema is invalid.
    """

    @classmethod
    def incorrect_type(
        cls,
        key: str,
        expected: Type[Any],
        found: Any,
    ) -> InvalidSchema:
        return InvalidSchema(
            'Expected "%s" to be %s but found %s (%s)'
            % (
                key,
                expected.__name__,
                repr(found),
                found.__class__.__name__,
            )
        )

    @classmethod
    def missing(cls, key: str, schema: Optional[Dict[str, Any]]) -> InvalidSchema:
        return InvalidSchema(
            '"%s" is not present in schema (%s)'
            % (
                key,
                schema or "<none>",
            ),
        )
