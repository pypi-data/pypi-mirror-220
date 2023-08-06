from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from recompose.exceptions import InvalidSchema
from recompose.types import WithArgs

T = TypeVar("T")


class WithReader(ABC, Generic[T]):
    @classmethod
    def _get(cls, args: Optional[WithArgs]) -> Optional[T]:
        if not args:
            return None

        value = args.get(cls.key())

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
    def get_optional(cls, args: Optional[WithArgs]) -> Optional[T]:
        """
        Gets an optional value.
        """

        return cls._get(args)

    @classmethod
    def get_required(cls, args: Optional[WithArgs]) -> T:
        """
        Gets a required value.
        """

        value = cls.get_optional(args)

        if value is None:
            raise InvalidSchema.missing(cls.key(), args)

        return value

    @classmethod
    @abstractmethod
    def key(cls) -> str:
        """
        Property key.
        """
