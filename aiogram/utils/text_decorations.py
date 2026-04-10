from __future__ import annotations

import html
import re
from abc import ABC, abstractmethod
from datetime import date, datetime, time
from typing import TYPE_CHECKING, cast

from aiogram.enums import MessageEntityType
from aiogram.utils.link import create_tg_link

if TYPE_CHECKING:
    from collections.abc import Generator
    from re import Pattern

    from aiogram.types import MessageEntity

__all__ = (
    "HtmlDecoration",
    "MarkdownDecoration",
    "TextDecoration",
    "add_surrogates",
    "html_decoration",
    "markdown_decoration",
    "remove_surrogates",
)


def add_surrogates(text: str) -> bytes:
    pass


def remove_surrogates(text: bytes) -> str:
    pass


class TextDecoration(ABC):
    def apply_entity(self, entity: MessageEntity, text: str) -> str:
        """
        Apply single entity to text

        :param entity:
        :param text:
        :return:
        """
        pass

    def unparse(self, text: str, entities: list[MessageEntity] | None = None) -> str:
        """
        Unparse message entities

        :param text: raw text
        :param entities: Array of MessageEntities
        :return:
        """
        pass

    def _unparse_entities(
        self,
        text: bytes,
        entities: list[MessageEntity],
        offset: int | None = None,
        length: int | None = None,
    ) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def link(self, value: str, link: str) -> str:
        pass

    @abstractmethod
    def bold(self, value: str) -> str:
        pass

    @abstractmethod
    def italic(self, value: str) -> str:
        pass

    @abstractmethod
    def code(self, value: str) -> str:
        pass

    @abstractmethod
    def pre(self, value: str) -> str:
        pass

    @abstractmethod
    def pre_language(self, value: str, language: str) -> str:
        pass

    @abstractmethod
    def underline(self, value: str) -> str:
        pass

    @abstractmethod
    def strikethrough(self, value: str) -> str:
        pass

    @abstractmethod
    def spoiler(self, value: str) -> str:
        pass

    @abstractmethod
    def quote(self, value: str) -> str:
        pass

    @abstractmethod
    def custom_emoji(self, value: str, custom_emoji_id: str) -> str:
        pass

    @abstractmethod
    def blockquote(self, value: str) -> str:
        pass

    @abstractmethod
    def expandable_blockquote(self, value: str) -> str:
        pass

    @abstractmethod
    def date_time(
        self,
        value: str,
        unix_time: int | datetime,
        date_time_format: str | None = None,
    ) -> str:
        pass


class HtmlDecoration(TextDecoration):
    BOLD_TAG = "b"
    ITALIC_TAG = "i"
    UNDERLINE_TAG = "u"
    STRIKETHROUGH_TAG = "s"
    CODE_TAG = "code"
    PRE_TAG = "pre"
    LINK_TAG = "a"
    SPOILER_TAG = "tg-spoiler"
    EMOJI_TAG = "tg-emoji"
    DATE_TIME_TAG = "tg-time"
    BLOCKQUOTE_TAG = "blockquote"

    def _tag(
        self,
        tag: str,
        content: str,
        *,
        attrs: dict[str, str] | None = None,
        flags: list[str] | None = None,
    ) -> str:
        pass

    def link(self, value: str, link: str) -> str:
        pass

    def bold(self, value: str) -> str:
        pass

    def italic(self, value: str) -> str:
        pass

    def code(self, value: str) -> str:
        pass

    def pre(self, value: str) -> str:
        pass

    def pre_language(self, value: str, language: str) -> str:
        pass

    def underline(self, value: str) -> str:
        pass

    def strikethrough(self, value: str) -> str:
        pass

    def spoiler(self, value: str) -> str:
        pass

    def quote(self, value: str) -> str:
        pass

    def custom_emoji(self, value: str, custom_emoji_id: str) -> str:
        pass

    def blockquote(self, value: str) -> str:
        pass

    def expandable_blockquote(self, value: str) -> str:
        pass

    def date_time(
        self,
        value: str,
        unix_time: int | datetime,
        date_time_format: str | None = None,
    ) -> str:
        pass


class MarkdownDecoration(TextDecoration):
    MARKDOWN_QUOTE_PATTERN: Pattern[str] = re.compile(r"([_*\[\]()~`>#+\-=|{}.!\\])")

    def link(self, value: str, link: str) -> str:
        pass

    def bold(self, value: str) -> str:
        pass

    def italic(self, value: str) -> str:
        pass

    def code(self, value: str) -> str:
        pass

    def pre(self, value: str) -> str:
        pass

    def pre_language(self, value: str, language: str) -> str:
        pass

    def underline(self, value: str) -> str:
        pass

    def strikethrough(self, value: str) -> str:
        pass

    def spoiler(self, value: str) -> str:
        pass

    def quote(self, value: str) -> str:
        pass

    def custom_emoji(self, value: str, custom_emoji_id: str) -> str:
        pass

    def blockquote(self, value: str) -> str:
        pass

    def expandable_blockquote(self, value: str) -> str:
        pass

    def date_time(
        self,
        value: str,
        unix_time: int | datetime,
        date_time_format: str | None = None,
    ) -> str:
        pass


html_decoration = HtmlDecoration()
markdown_decoration = MarkdownDecoration()
