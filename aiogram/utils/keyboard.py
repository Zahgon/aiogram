from __future__ import annotations

from abc import ABC
from copy import deepcopy
from itertools import chain
from itertools import cycle as repeat_all
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    CallbackGame,
    CopyTextButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    LoginUrl,
    ReplyKeyboardMarkup,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

ButtonType = TypeVar("ButtonType", InlineKeyboardButton, KeyboardButton)
T = TypeVar("T")


class KeyboardBuilder(ABC, Generic[ButtonType]):
    """
    Generic keyboard builder that helps to adjust your markup with defined shape of lines.

    Works both of InlineKeyboardMarkup and ReplyKeyboardMarkup.
    """

    max_width: int = 0
    min_width: int = 0
    max_buttons: int = 0

    def __init__(
        self,
        button_type: type[ButtonType],
        markup: list[list[ButtonType]] | None = None,
    ) -> None:
        if not issubclass(button_type, (InlineKeyboardButton, KeyboardButton)):
            msg = f"Button type {button_type} are not allowed here"
            raise ValueError(msg)
        self._button_type: type[ButtonType] = button_type
        if markup:
            self._validate_markup(markup)
        else:
            markup = []
        self._markup: list[list[ButtonType]] = markup

    @property
    def buttons(self) -> Generator[ButtonType, None, None]:
        """
        Get flatten set of all buttons

        :return:
        """
        pass

    def _validate_button(self, button: ButtonType) -> bool:
        """
        Check that button item has correct type

        :param button:
        :return:
        """
        pass

    def _validate_buttons(self, *buttons: ButtonType) -> bool:
        """
        Check that all passed button has correct type

        :param buttons:
        :return:
        """
        pass

    def _validate_row(self, row: list[ButtonType]) -> bool:
        """
        Check that row of buttons are correct
        Row can be only list of allowed button types and has length 0 <= n <= 8

        :param row:
        :return:
        """
        pass

    def _validate_markup(self, markup: list[list[ButtonType]]) -> bool:
        """
        Check that passed markup has correct data structure
        Markup is list of lists of buttons

        :param markup:
        :return:
        """
        pass

    def _validate_size(self, size: Any) -> int:
        """
        Validate that passed size is legit

        :param size:
        :return:
        """
        pass

    def export(self) -> list[list[ButtonType]]:
        """
        Export configured markup as list of lists of buttons

        .. code-block:: python

            >>> builder = KeyboardBuilder(button_type=InlineKeyboardButton)
            >>> ... # Add buttons to builder
            >>> markup = InlineKeyboardMarkup(inline_keyboard=builder.export())

        :return:
        """
        return deepcopy(self._markup)

    def add(self, *buttons: ButtonType) -> KeyboardBuilder[ButtonType]:
        """
        Add one or many buttons to markup.

        :param buttons:
        :return:
        """
        pass

    def row(self, *buttons: ButtonType, width: int | None = None) -> KeyboardBuilder[ButtonType]:
        """
        Add row to markup

        When too much buttons is passed it will be separated to many rows

        :param buttons:
        :param width:
        :return:
        """
        pass

    def adjust(self, *sizes: int, repeat: bool = False) -> KeyboardBuilder[ButtonType]:
        """
        Adjust previously added buttons to specific row sizes.

        By default, when the sum of passed sizes is lower than buttons count the last
        one size will be used for tail of the markup.
        If repeat=True is passed - all sizes will be cycled when available more buttons
        count than all sizes

        :param sizes:
        :param repeat:
        :return:
        """
        pass

    def _button(self, **kwargs: Any) -> KeyboardBuilder[ButtonType]:
        """
        Add button to markup

        :param kwargs:
        :return:
        """
        pass

    def as_markup(self, **kwargs: Any) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
        pass

    def attach(self, builder: KeyboardBuilder[ButtonType]) -> KeyboardBuilder[ButtonType]:
        pass


def repeat_last(items: Iterable[T]) -> Generator[T, None, None]:
    pass


class InlineKeyboardBuilder(KeyboardBuilder[InlineKeyboardButton]):
    """
    Inline keyboard builder inherits all methods from generic builder
    """

    max_width: int = 8
    min_width: int = 1
    max_buttons: int = 100

    def button(
        self,
        *,
        text: str,
        icon_custom_emoji_id: str | None = None,
        style: str | None = None,
        url: str | None = None,
        callback_data: str | CallbackData | None = None,
        web_app: WebAppInfo | None = None,
        login_url: LoginUrl | None = None,
        switch_inline_query: str | None = None,
        switch_inline_query_current_chat: str | None = None,
        switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = None,
        copy_text: CopyTextButton | None = None,
        callback_game: CallbackGame | None = None,
        pay: bool | None = None,
        **kwargs: Any,
    ) -> InlineKeyboardBuilder:
        pass

    def as_markup(self, **kwargs: Any) -> InlineKeyboardMarkup:
        """Construct an InlineKeyboardMarkup"""
        pass

    def __init__(self, markup: list[list[InlineKeyboardButton]] | None = None) -> None:
        super().__init__(button_type=InlineKeyboardButton, markup=markup)

    def copy(self: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
        """
        Make full copy of current builder with markup

        :return:
        """
        return InlineKeyboardBuilder(markup=self.export())

    @classmethod
    def from_markup(
        cls: type[InlineKeyboardBuilder],
        markup: InlineKeyboardMarkup,
    ) -> InlineKeyboardBuilder:
        """
        Create builder from existing markup

        :param markup:
        :return:
        """
        pass


class ReplyKeyboardBuilder(KeyboardBuilder[KeyboardButton]):
    """
    Reply keyboard builder inherits all methods from generic builder
    """

    max_width: int = 10
    min_width: int = 1
    max_buttons: int = 300

    def button(
        self,
        *,
        text: str,
        icon_custom_emoji_id: str | None = None,
        style: str | None = None,
        request_users: KeyboardButtonRequestUsers | None = None,
        request_chat: KeyboardButtonRequestChat | None = None,
        request_contact: bool | None = None,
        request_location: bool | None = None,
        request_poll: KeyboardButtonPollType | None = None,
        web_app: WebAppInfo | None = None,
        **kwargs: Any,
    ) -> ReplyKeyboardBuilder:
        pass

    def as_markup(self, **kwargs: Any) -> ReplyKeyboardMarkup:
        """Construct a ReplyKeyboardMarkup"""
        pass

    def __init__(self, markup: list[list[KeyboardButton]] | None = None) -> None:
        super().__init__(button_type=KeyboardButton, markup=markup)

    def copy(self: ReplyKeyboardBuilder) -> ReplyKeyboardBuilder:
        """
        Make full copy of current builder with markup

        :return:
        """
        return ReplyKeyboardBuilder(markup=self.export())

    @classmethod
    def from_markup(cls, markup: ReplyKeyboardMarkup) -> ReplyKeyboardBuilder:
        """
        Create builder from existing markup

        :param markup:
        :return:
        """
        pass
