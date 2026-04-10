from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from aiogram.dispatcher.middlewares.manager import MiddlewareManager
from aiogram.exceptions import UnsupportedKeywordArgument
from aiogram.filters.base import Filter

from .bases import UNHANDLED, MiddlewareType, SkipHandler
from .handler import CallbackType, FilterObject, HandlerObject

if TYPE_CHECKING:
    from aiogram.dispatcher.router import Router
    from aiogram.types import TelegramObject


class TelegramEventObserver:
    """
    Event observer for Telegram events

    Here you can register handler with filter.
    This observer will stop event propagation when first handler is pass.
    """

    def __init__(self, router: Router, event_name: str) -> None:
        self.router: Router = router
        self.event_name: str = event_name

        self.handlers: list[HandlerObject] = []

        self.middleware = MiddlewareManager()
        self.outer_middleware = MiddlewareManager()

        # Re-used filters check method from already implemented handler object
        # with dummy callback which never will be used
        self._handler = HandlerObject(callback=lambda: True, filters=[])

    def filter(self, *filters: CallbackType) -> None:
        """
        Register filter for all handlers of this event observer

        :param filters: positional filters
        """
        pass

    def _resolve_middlewares(self) -> list[MiddlewareType[TelegramObject]]:
        pass

    def register(
        self,
        callback: CallbackType,
        *filters: CallbackType,
        flags: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> CallbackType:
        """
        Register event handler
        """
        pass

    def wrap_outer_middleware(
        self,
        callback: Any,
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        pass

    def check_root_filters(self, event: TelegramObject, **kwargs: Any) -> Any:
        pass

    async def trigger(self, event: TelegramObject, **kwargs: Any) -> Any:
        """
        Propagate event to handlers and stops propagation on first match.
        Handler will be called when all its filters are pass.
        """
        pass

    def __call__(
        self,
        *filters: CallbackType,
        flags: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Callable[[CallbackType], CallbackType]:
        """
        Decorator for registering event handlers
        """

        def wrapper(callback: CallbackType) -> CallbackType:
            pass

        return wrapper
