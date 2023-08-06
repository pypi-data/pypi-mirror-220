from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from recompose.exceptions import InvalidSchema
from recompose.types import TransformSchema

T = TypeVar("T")


class SchemaReader(ABC, Generic[T]):
    @classmethod
    def _get(
        cls,
        schema: TransformSchema,
    ) -> Optional[T]:
        value = schema.get(cls.key())

        if value is None:
            return None

        return cls.cast(value)

    @classmethod
    @abstractmethod
    def cast(cls, value: Any) -> T:
        """
        Gets the given value as the given type.
        """

    @classmethod
    def get_optional(
        cls,
        schema: TransformSchema,
    ) -> Optional[T]:
        """
        Gets an optional value.
        """

        return cls._get(schema)

    @classmethod
    def get_required(
        cls,
        schema: TransformSchema,
    ) -> T:
        """
        Gets a required value.
        """

        value = cls.get_optional(schema)

        if value is None:
            raise InvalidSchema.missing(cls.key(), schema)

        return value

    @classmethod
    @abstractmethod
    def key(cls) -> str:
        """
        Property key.
        """
