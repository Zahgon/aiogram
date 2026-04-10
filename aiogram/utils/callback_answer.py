from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, loggers
from aiogram.dispatcher.flags import get_flag
from aiogram.exceptions import CallbackAnswerException
from aiogram.methods import AnswerCallbackQuery
from aiogram.types import CallbackQuery, TelegramObject


class CallbackAnswer:
    def __init__(
        self,
        answered: bool,
        disabled: bool = False,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
    ) -> None:
        """
        Callback answer configuration

        :param answered: this request is already answered by middleware
        :param disabled: answer will not be performed
        :param text: answer with text
        :param show_alert: show alert
        :param url: game url
        :param cache_time: cache answer for some time
        """
        self._answered = answered
        self._disabled = disabled
        self._text = text
        self._show_alert = show_alert
        self._url = url
        self._cache_time = cache_time

    def disable(self) -> None:
        """
        Deactivate answering for this handler
        """
        pass

    @property
    def disabled(self) -> bool:
        """Indicates that automatic answer is disabled in this handler"""
        pass

    @disabled.setter
    def disabled(self, value: bool) -> None:
        pass

    @property
    def answered(self) -> bool:
        """
        Indicates that request is already answered by middleware
        """
        pass

    @property
    def text(self) -> str | None:
        """
        Response text
        :return:
        """
        pass

    @text.setter
    def text(self, value: str | None) -> None:
        pass

    @property
    def show_alert(self) -> bool | None:
        """
        Whether to display an alert
        """
        pass

    @show_alert.setter
    def show_alert(self, value: bool | None) -> None:
        pass

    @property
    def url(self) -> str | None:
        """
        Game url
        """
        pass

    @url.setter
    def url(self, value: str | None) -> None:
        pass

    @property
    def cache_time(self) -> int | None:
        """
        Response cache time
        """
        pass

    @cache_time.setter
    def cache_time(self, value: int | None) -> None:
        pass

    def __str__(self) -> str:
        args = ", ".join(
            f"{k}={v!r}"
            for k, v in {
                "answered": self.answered,
                "disabled": self.disabled,
                "text": self.text,
                "show_alert": self.show_alert,
                "url": self.url,
                "cache_time": self.cache_time,
            }.items()
            if v is not None
        )
        return f"{type(self).__name__}({args})"


class CallbackAnswerMiddleware(BaseMiddleware):
    def __init__(
        self,
        pre: bool = False,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
    ) -> None:
        """
        Inner middleware for callback query handlers, can be useful in bots with a lot of callback
        handlers to automatically take answer to all requests

        :param pre: send answer before execute handler
        :param text: answer with text
        :param show_alert: show alert
        :param url: game url
        :param cache_time: cache answer for some time
        """
        self.pre = pre
        self.text = text
        self.show_alert = show_alert
        self.url = url
        self.cache_time = cache_time

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, CallbackQuery):
            return await handler(event, data)

        callback_answer = data["callback_answer"] = self.construct_callback_answer(
            properties=get_flag(data, "callback_answer"),
        )

        if not callback_answer.disabled and callback_answer.answered:
            await self.answer(event, callback_answer)
        try:
            return await handler(event, data)
        finally:
            if not callback_answer.disabled and not callback_answer.answered:
                await self.answer(event, callback_answer)

    def construct_callback_answer(
        self,
        properties: dict[str, Any] | bool | None,
    ) -> CallbackAnswer:
        pass

    def answer(self, event: CallbackQuery, callback_answer: CallbackAnswer) -> AnswerCallbackQuery:
        pass
