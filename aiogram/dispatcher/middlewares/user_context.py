from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import (
    Chat,
    ChatBoostSourcePremium,
    InaccessibleMessage,
    TelegramObject,
    Update,
    User,
)

EVENT_CONTEXT_KEY = "event_context"

EVENT_FROM_USER_KEY = "event_from_user"
EVENT_CHAT_KEY = "event_chat"
EVENT_THREAD_ID_KEY = "event_thread_id"


@dataclass(frozen=True)
class EventContext:
    chat: Chat | None = None
    user: User | None = None
    thread_id: int | None = None
    business_connection_id: str | None = None

    @property
    def user_id(self) -> int | None:
        pass

    @property
    def chat_id(self) -> int | None:
        pass


class UserContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Update):
            msg = "UserContextMiddleware got an unexpected event type!"
            raise RuntimeError(msg)
        event_context = data[EVENT_CONTEXT_KEY] = self.resolve_event_context(event=event)

        # Backward compatibility
        if event_context.user is not None:
            data[EVENT_FROM_USER_KEY] = event_context.user
        if event_context.chat is not None:
            data[EVENT_CHAT_KEY] = event_context.chat
        if event_context.thread_id is not None:
            data[EVENT_THREAD_ID_KEY] = event_context.thread_id

        return await handler(event, data)

    @classmethod
    def resolve_event_context(cls, event: Update) -> EventContext:
        """
        Resolve chat and user instance from Update object
        """
        pass
