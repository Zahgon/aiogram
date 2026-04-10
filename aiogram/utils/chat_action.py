import asyncio
import logging
import time
from asyncio import Event, Lock
from collections.abc import Awaitable, Callable
from contextlib import suppress
from types import TracebackType
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, TelegramObject

logger = logging.getLogger(__name__)
DEFAULT_INTERVAL = 5.0
DEFAULT_INITIAL_SLEEP = 0.0


class ChatActionSender:
    """
    This utility helps to automatically send chat action until long actions is done
    to take acknowledge bot users the bot is doing something and not crashed.

    Provides simply to use context manager.

    Technically sender start background task with infinity loop which works
    until action will be finished and sends the
    `chat action <https://core.telegram.org/bots/api#sendchataction>`_
    every 5 seconds.
    """

    def __init__(
        self,
        *,
        bot: Bot,
        chat_id: str | int,
        message_thread_id: int | None = None,
        action: str = "typing",
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> None:
        """
        :param bot: instance of the bot
        :param chat_id: target chat id
        :param message_thread_id: unique identifier for the target message thread; supergroups only
        :param action: chat action type
        :param interval: interval between iterations
        :param initial_sleep: sleep before first sending of the action
        """
        self.chat_id = chat_id
        self.message_thread_id = message_thread_id
        self.action = action
        self.interval = interval
        self.initial_sleep = initial_sleep
        self.bot = bot

        self._lock = Lock()
        self._close_event = Event()
        self._closed_event = Event()
        self._task: asyncio.Task[Any] | None = None

    @property
    def running(self) -> bool:
        pass

    async def _wait(self, interval: float) -> None:
        pass

    async def _worker(self) -> None:
        pass

    async def _run(self) -> None:
        pass

    async def _stop(self) -> None:
        pass

    async def __aenter__(self) -> "ChatActionSender":
        await self._run()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Any:
        await self._stop()

    @classmethod
    def typing(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `typing` action"""
        pass

    @classmethod
    def upload_photo(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `upload_photo` action"""
        pass

    @classmethod
    def record_video(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `record_video` action"""
        pass

    @classmethod
    def upload_video(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `upload_video` action"""
        pass

    @classmethod
    def record_voice(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `record_voice` action"""
        pass

    @classmethod
    def upload_voice(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `upload_voice` action"""
        pass

    @classmethod
    def upload_document(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `upload_document` action"""
        pass

    @classmethod
    def choose_sticker(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `choose_sticker` action"""
        pass

    @classmethod
    def find_location(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `find_location` action"""
        pass

    @classmethod
    def record_video_note(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `record_video_note` action"""
        pass

    @classmethod
    def upload_video_note(
        cls,
        chat_id: int | str,
        bot: Bot,
        message_thread_id: int | None = None,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> "ChatActionSender":
        """Create instance of the sender with `upload_video_note` action"""
        pass


class ChatActionMiddleware(BaseMiddleware):
    """
    Helps to automatically use chat action sender for all message handlers
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)
        bot = data["bot"]

        chat_action = get_flag(data, "chat_action") or "typing"
        kwargs = {}
        if isinstance(chat_action, dict):
            if initial_sleep := chat_action.get("initial_sleep"):
                kwargs["initial_sleep"] = initial_sleep
            if interval := chat_action.get("interval"):
                kwargs["interval"] = interval
            if action := chat_action.get("action"):
                kwargs["action"] = action
        elif isinstance(chat_action, bool):
            kwargs["action"] = "typing"
        else:
            kwargs["action"] = chat_action
        kwargs["message_thread_id"] = (
            event.message_thread_id
            if isinstance(event, Message) and event.is_topic_message
            else None
        )
        async with ChatActionSender(bot=bot, chat_id=event.chat.id, **kwargs):
            return await handler(event, data)
