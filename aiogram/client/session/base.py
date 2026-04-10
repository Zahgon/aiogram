from __future__ import annotations

import abc
import datetime
import json
import secrets
from collections.abc import AsyncGenerator, Callable
from enum import Enum
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Final, cast

from pydantic import ValidationError
from typing_extensions import Self

from aiogram.client.default import Default
from aiogram.client.telegram import PRODUCTION, TelegramAPIServer
from aiogram.exceptions import (
    ClientDecodeError,
    RestartingTelegram,
    TelegramAPIError,
    TelegramBadRequest,
    TelegramConflictError,
    TelegramEntityTooLarge,
    TelegramForbiddenError,
    TelegramMigrateToChat,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramServerError,
    TelegramUnauthorizedError,
)
from aiogram.methods import Response, TelegramMethod
from aiogram.methods.base import TelegramType
from aiogram.types import InputFile, TelegramObject

from .middlewares.manager import RequestMiddlewareManager

if TYPE_CHECKING:
    from types import TracebackType

    from aiogram.client.bot import Bot

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]

DEFAULT_TIMEOUT: Final[float] = 60.0


class BaseSession(abc.ABC):
    """
    This is base class for all HTTP sessions in aiogram.

    If you want to create your own session, you must inherit from this class.
    """

    def __init__(
        self,
        api: TelegramAPIServer = PRODUCTION,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """

        :param api: Telegram Bot API URL patterns
        :param json_loads: JSON loader
        :param json_dumps: JSON dumper
        :param timeout: Session scope request timeout
        """
        self.api = api
        self.json_loads = json_loads
        self.json_dumps = json_dumps
        self.timeout = timeout

        self.middleware = RequestMiddlewareManager()

    def check_response(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        status_code: int,
        content: str,
    ) -> Response[TelegramType]:
        """
        Check response status
        """
        pass

    @abc.abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """
        Close client session
        """

    @abc.abstractmethod
    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:  # pragma: no cover
        """
        Make request to Telegram Bot API

        :param bot: Bot instance
        :param method: Method instance
        :param timeout: Request timeout
        :return:
        :raise TelegramApiError:
        """

    @abc.abstractmethod
    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        """
        Stream reader
        """
        yield b""

    def prepare_value(
        self,
        value: Any,
        bot: Bot,
        files: dict[str, Any],
        _dumps_json: bool = True,
    ) -> Any:
        """
        Prepare value before send
        """
        pass

    async def __call__(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        middleware = self.middleware.wrap_middlewares(self.make_request, timeout=timeout)
        return cast(TelegramType, await middleware(bot, method))

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
