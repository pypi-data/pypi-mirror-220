from __future__ import annotations

from typing import Any

from recompose.exceptions.recompose import RecomposeError
from recompose.types import CursorSchema


class UnsupportedVersion(RecomposeError):
    """
    Raised when a cursor definition has an unsupported schema version.
    """

    @classmethod
    def no_version(cls, schema: CursorSchema) -> UnsupportedVersion:
        return UnsupportedVersion(
            "Schema does not describe its version (%s)" % schema,
        )

    @classmethod
    def not_integer(cls, found: Any) -> UnsupportedVersion:
        return UnsupportedVersion(
            "Schema version %s (%s) is not an integer"
            % (
                repr(found),
                type(found).__name__,
            )
        )

    @classmethod
    def unsupported(cls, found: int, expected: int) -> UnsupportedVersion:
        return UnsupportedVersion(
            "Found schema version %i but expected no later than %i"
            % (
                found,
                expected,
            )
        )
