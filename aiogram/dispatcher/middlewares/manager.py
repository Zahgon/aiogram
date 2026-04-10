import functools
from collections.abc import Callable, Sequence
from typing import Any, overload

from aiogram.dispatcher.event.bases import (
    MiddlewareEventType,
    MiddlewareType,
    NextMiddlewareType,
)
from aiogram.dispatcher.event.handler import CallbackType
from aiogram.types import TelegramObject


class MiddlewareManager(Sequence[MiddlewareType[TelegramObject]]):
    def __init__(self) -> None:
        self._middlewares: list[MiddlewareType[TelegramObject]] = []

    def register(
        self,
        middleware: MiddlewareType[TelegramObject],
    ) -> MiddlewareType[TelegramObject]:
        pass

    def unregister(self, middleware: MiddlewareType[TelegramObject]) -> None:
        pass

    def __call__(
        self,
        middleware: MiddlewareType[TelegramObject] | None = None,
    ) -> (
        Callable[[MiddlewareType[TelegramObject]], MiddlewareType[TelegramObject]]
        | MiddlewareType[TelegramObject]
    ):
        if middleware is None:
            return self.register
        return self.register(middleware)

    @overload
    def __getitem__(self, item: int) -> MiddlewareType[TelegramObject]:
        pass

    @overload
    def __getitem__(self, item: slice) -> Sequence[MiddlewareType[TelegramObject]]:
        pass

    def __getitem__(
        self,
        item: int | slice,
    ) -> MiddlewareType[TelegramObject] | Sequence[MiddlewareType[TelegramObject]]:
        return self._middlewares[item]

    def __len__(self) -> int:
        return len(self._middlewares)

    @staticmethod
    def wrap_middlewares(
        middlewares: Sequence[MiddlewareType[MiddlewareEventType]],
        handler: CallbackType,
    ) -> NextMiddlewareType[MiddlewareEventType]:
        @functools.wraps(handler)
        pass
