from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiogram import Bot
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_CONTEXT_KEY, EventContext
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import (
    DEFAULT_DESTINY,
    BaseEventIsolation,
    BaseStorage,
    StorageKey,
)
from aiogram.fsm.strategy import FSMStrategy, apply_strategy
from aiogram.types import TelegramObject


class FSMContextMiddleware(BaseMiddleware):
    def __init__(
        self,
        storage: BaseStorage,
        events_isolation: BaseEventIsolation,
        strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
    ) -> None:
        self.storage = storage
        self.strategy = strategy
        self.events_isolation = events_isolation

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = cast(Bot, data["bot"])
        context = self.resolve_event_context(bot, data)
        data["fsm_storage"] = self.storage
        if context:
            # Bugfix: https://github.com/aiogram/aiogram/issues/1317
            # State should be loaded after lock is acquired
            async with self.events_isolation.lock(key=context.key):
                data.update({"state": context, "raw_state": await context.get_state()})
                return await handler(event, data)
        return await handler(event, data)

    def resolve_event_context(
        self,
        bot: Bot,
        data: dict[str, Any],
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext | None:
        pass

    def resolve_context(
        self,
        bot: Bot,
        chat_id: int | None,
        user_id: int | None,
        thread_id: int | None = None,
        business_connection_id: str | None = None,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext | None:
        pass

    def get_context(
        self,
        bot: Bot,
        chat_id: int,
        user_id: int,
        thread_id: int | None = None,
        business_connection_id: str | None = None,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext:
        pass

    async def close(self) -> None:
        pass
