from __future__ import annotations

import types
import typing
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import TYPE_CHECKING, Any, ClassVar, Literal, TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing_extensions import Self

from aiogram.filters.base import Filter
from aiogram.types import CallbackQuery

if TYPE_CHECKING:
    from magic_filter import MagicFilter
    from pydantic.fields import FieldInfo

T = TypeVar("T", bound="CallbackData")

MAX_CALLBACK_LENGTH: int = 64


_UNION_TYPES = {typing.Union, types.UnionType}


class CallbackDataException(Exception):
    pass


class CallbackData(BaseModel):
    """
    Base class for callback data wrapper

    This class should be used as super-class of user-defined callbacks.

    The class-keyword :code:`prefix` is required to define prefix
    and also the argument :code:`sep` can be passed to define separator (default is :code:`:`).
    """

    if TYPE_CHECKING:
        __separator__: ClassVar[str]
        """Data separator (default is :code:`:`)"""
        __prefix__: ClassVar[str]
        """Callback prefix"""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if "prefix" not in kwargs:
            msg = (
                f"prefix required, usage example: "
                f"`class {cls.__name__}(CallbackData, prefix='my_callback'): ...`"
            )
            raise ValueError(msg)
        cls.__separator__ = kwargs.pop("sep", ":")
        cls.__prefix__ = kwargs.pop("prefix")
        if cls.__separator__ in cls.__prefix__:
            msg = (
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )
            raise ValueError(msg)
        super().__init_subclass__(**kwargs)

    def _encode_value(self, key: str, value: Any) -> str:
        pass

    def pack(self) -> str:
        """
        Generate callback data string

        :return: valid callback data for Telegram Bot API
        """
        pass

    @classmethod
    def unpack(cls, value: str) -> Self:
        """
        Parse callback data string

        :param value: value from Telegram
        :return: instance of CallbackData
        """
        pass

    @classmethod
    def filter(cls, rule: MagicFilter | None = None) -> CallbackQueryFilter:
        """
        Generates a filter for callback query with rule

        :param rule: magic rule
        :return: instance of filter
        """
        pass


class CallbackQueryFilter(Filter):
    """
    This filter helps to handle callback query.

    Should not be used directly, you should create the instance of this filter
    via callback data instance
    """

    __slots__ = (
        "callback_data",
        "rule",
    )

    def __init__(
        self,
        *,
        callback_data: type[CallbackData],
        rule: MagicFilter | None = None,
    ):
        """
        :param callback_data: Expected type of callback data
        :param rule: Magic rule
        """
        self.callback_data = callback_data
        self.rule = rule

    def __str__(self) -> str:
        return self._signature_to_string(
            callback_data=self.callback_data,
            rule=self.rule,
        )

    async def __call__(self, query: CallbackQuery) -> Literal[False] | dict[str, Any]:
        if not isinstance(query, CallbackQuery) or not query.data:
            return False
        try:
            callback_data = self.callback_data.unpack(query.data)
        except (TypeError, ValueError):
            return False

        if self.rule is None or self.rule.resolve(callback_data):
            return {"callback_data": callback_data}
        return False


def _check_field_is_nullable(field: FieldInfo) -> bool:
    """
    Check if the given field is nullable.

    :param field: The FieldInfo object representing the field to check.
    :return: True if the field is nullable, False otherwise.

    """
    pass
