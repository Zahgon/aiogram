from __future__ import annotations

import asyncio
import contextvars
import signal
import sys
import warnings
from asyncio import CancelledError, Event, Future, Lock
from collections.abc import AsyncGenerator, Awaitable
from contextlib import suppress
from typing import TYPE_CHECKING, Any

from aiogram import loggers
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.middleware import FSMContextMiddleware
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import DisabledEventIsolation, MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.methods import GetUpdates, TelegramMethod
from aiogram.types import Update, User
from aiogram.types.base import UNSET, UNSET_TYPE
from aiogram.types.update import UpdateTypeLookupError
from aiogram.utils.backoff import Backoff, BackoffConfig

from .event.bases import UNHANDLED, SkipHandler
from .event.telegram import TelegramEventObserver
from .middlewares.error import ErrorsMiddleware
from .middlewares.user_context import UserContextMiddleware
from .router import Router

if TYPE_CHECKING:
    from aiogram.client.bot import Bot
    from aiogram.methods.base import TelegramType

DEFAULT_BACKOFF_CONFIG = BackoffConfig(min_delay=1.0, max_delay=5.0, factor=1.3, jitter=0.1)


class Dispatcher(Router):
    """
    Root router
    """

    def __init__(
        self,
        *,  # * - Preventing to pass instance of Bot to the FSM storage
        storage: BaseStorage | None = None,
        fsm_strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
        events_isolation: BaseEventIsolation | None = None,
        disable_fsm: bool = False,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Root router

        :param storage: Storage for FSM
        :param fsm_strategy: FSM strategy
        :param events_isolation: Events isolation
        :param disable_fsm: Disable FSM, note that if you disable FSM
            then you should not use storage and events isolation
        :param kwargs: Other arguments, will be passed as keyword arguments to handlers
        """
        super().__init__(name=name)

        if storage and not isinstance(storage, BaseStorage):
            msg = f"FSM storage should be instance of 'BaseStorage' not {type(storage).__name__}"
            raise TypeError(msg)

        # Telegram API provides originally only one event type - Update
        # For making easily interactions with events here is registered handler which helps
        # to separate Update to different event types like Message, CallbackQuery etc.
        self.update = self.observers["update"] = TelegramEventObserver(
            router=self,
            event_name="update",
        )
        self.update.register(self._listen_update)

        # Error handlers should work is out of all other functions
        # and should be registered before all others middlewares
        self.update.outer_middleware(ErrorsMiddleware(self))

        # User context middleware makes small optimization for all other builtin
        # middlewares via caching the user and chat instances in the event context
        self.update.outer_middleware(UserContextMiddleware())

        # FSM middleware should always be registered after User context middleware
        # because here is used context from previous step
        self.fsm = FSMContextMiddleware(
            storage=storage or MemoryStorage(),
            strategy=fsm_strategy,
            events_isolation=events_isolation or DisabledEventIsolation(),
        )
        if not disable_fsm:
            # Note that when FSM middleware is disabled, the event isolation is also disabled
            # Because the isolation mechanism is a part of the FSM
            self.update.outer_middleware(self.fsm)
        self.shutdown.register(self.fsm.close)

        self.workflow_data: dict[str, Any] = kwargs
        self._running_lock = Lock()
        self._stop_signal: Event | None = None
        self._stopped_signal: Event | None = None
        self._handle_update_tasks: set[asyncio.Task[Any]] = set()

    def __getitem__(self, item: str) -> Any:
        return self.workflow_data[item]

    def __setitem__(self, key: str, value: Any) -> None:
        self.workflow_data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.workflow_data[key]

    def get(self, key: str, /, default: Any | None = None) -> Any | None:
        return self.workflow_data.get(key, default)

    @property
    def storage(self) -> BaseStorage:
        pass

    @property
    def parent_router(self) -> Router | None:
        """
        Dispatcher has no parent router and can't be included to any other routers or dispatchers

        :return:
        """
        pass

    @parent_router.setter
    def parent_router(self, value: Router) -> None:
        """
        Dispatcher is root Router then configuring parent router is not allowed

        :param value:
        :return:
        """
        pass

    async def feed_update(self, bot: Bot, update: Update, **kwargs: Any) -> Any:
        """
        Main entry point for incoming updates
        Response of this method can be used as Webhook response

        :param bot:
        :param update:
        """
        pass

    async def feed_raw_update(self, bot: Bot, update: dict[str, Any], **kwargs: Any) -> Any:
        """
        Main entry point for incoming updates with automatic Dict->Update serializer

        :param bot:
        :param update:
        :param kwargs:
        """
        pass

    @classmethod
    async def _listen_updates(
        cls,
        bot: Bot,
        polling_timeout: int = 30,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | None = None,
    ) -> AsyncGenerator[Update, None]:
        """
        Endless updates reader with correctly handling any server-side or connection errors.

        So you may not worry that the polling will stop working.
        """
        pass

    async def _listen_update(self, update: Update, **kwargs: Any) -> Any:
        """
        Main updates listener

        Workflow:
        - Detect content type and propagate to observers in current router
        - If no one filter is pass - propagate update to child routers as Update

        :param update:
        :param kwargs:
        :return:
        """
        pass

    @classmethod
    async def silent_call_request(cls, bot: Bot, result: TelegramMethod[Any]) -> None:
        """
        Simulate answer into WebHook

        :param bot:
        :param result:
        :return:
        """
        pass

    async def _process_update(
        self,
        bot: Bot,
        update: Update,
        call_answer: bool = True,
        **kwargs: Any,
    ) -> bool:
        """
        Propagate update to event listeners

        :param bot: instance of Bot
        :param update: instance of Update
        :param call_answer: need to execute response as Telegram method (like answer into webhook)
        :param kwargs: contextual data for middlewares, filters and handlers
        :return: status
        """
        pass

    async def _process_with_semaphore(
        self,
        handle_update: Awaitable[bool],
        semaphore: asyncio.Semaphore,
    ) -> bool:
        """
        Process update with semaphore to limit concurrent tasks

        :param handle_update: Coroutine that processes the update
        :param semaphore: Semaphore to limit concurrent tasks
        :return: bool indicating the result of the update processing
        """
        pass

    async def _polling(
        self,
        bot: Bot,
        polling_timeout: int = 30,
        handle_as_tasks: bool = True,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | None = None,
        tasks_concurrency_limit: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Internal polling process

        :param bot:
        :param polling_timeout: Long-polling wait time
        :param handle_as_tasks: Run task for each event and no wait result
        :param backoff_config: backoff-retry config
        :param allowed_updates: List of the update types you want your bot to receive
        :param tasks_concurrency_limit: Maximum number of concurrent updates to process
            (None = no limit), used only if handle_as_tasks is True
        :param kwargs:
        :return:
        """
        pass

    async def _feed_webhook_update(self, bot: Bot, update: Update, **kwargs: Any) -> Any:
        """
        The same with `Dispatcher.process_update()` but returns real response instead of bool
        """
        pass

    async def feed_webhook_update(
        self,
        bot: Bot,
        update: Update | dict[str, Any],
        _timeout: float = 55,
        **kwargs: Any,
    ) -> TelegramMethod[TelegramType] | None:
        pass

    async def stop_polling(self) -> None:
        """
        Execute this method if you want to stop polling programmatically

        :return:
        """
        pass

    def _signal_stop_polling(self, sig: signal.Signals) -> None:
        pass

    async def start_polling(
        self,
        *bots: Bot,
        polling_timeout: int = 10,
        handle_as_tasks: bool = True,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | UNSET_TYPE | None = UNSET,
        handle_signals: bool = True,
        close_bot_session: bool = True,
        tasks_concurrency_limit: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Polling runner

        :param bots: Bot instances (one or more)
        :param polling_timeout: Long-polling wait time
        :param handle_as_tasks: Run task for each event and no wait result
        :param backoff_config: backoff-retry config
        :param allowed_updates: List of the update types you want your bot to receive
               By default, all used update types are enabled (resolved from handlers)
        :param handle_signals: handle signals (SIGINT/SIGTERM)
        :param close_bot_session: close bot sessions on shutdown
        :param tasks_concurrency_limit: Maximum number of concurrent updates to process
            (None = no limit), used only if handle_as_tasks is True
        :param kwargs: contextual data
        :return:
        """
        pass

    def run_polling(
        self,
        *bots: Bot,
        polling_timeout: int = 10,
        handle_as_tasks: bool = True,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | UNSET_TYPE | None = UNSET,
        handle_signals: bool = True,
        close_bot_session: bool = True,
        tasks_concurrency_limit: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Run many bots with polling

        :param bots: Bot instances (one or more)
        :param polling_timeout: Long-polling wait time
        :param handle_as_tasks: Run task for each event and no wait result
        :param backoff_config: backoff-retry config
        :param allowed_updates: List of the update types you want your bot to receive
        :param handle_signals: handle signals (SIGINT/SIGTERM)
        :param close_bot_session: close bot sessions on shutdown
        :param tasks_concurrency_limit: Maximum number of concurrent updates to process
            (None = no limit), used only if handle_as_tasks is True
        :param kwargs: contextual data
        :return:
        """
        pass
