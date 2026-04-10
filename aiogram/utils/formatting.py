from __future__ import annotations

import textwrap
from collections.abc import Generator, Iterable, Iterator
from datetime import datetime
from typing import Any, ClassVar

from typing_extensions import Self

from aiogram.enums import MessageEntityType
from aiogram.types import MessageEntity, User
from aiogram.utils.text_decorations import (
    add_surrogates,
    html_decoration,
    markdown_decoration,
    remove_surrogates,
)

NodeType = Any


def sizeof(value: str) -> int:
    pass


class Text(Iterable[NodeType]):
    """
    Simple text element
    """

    type: ClassVar[str | None] = None

    __slots__ = ("_body", "_params")

    def __init__(
        self,
        *body: NodeType,
        **params: Any,
    ) -> None:
        self._body: tuple[NodeType, ...] = body
        self._params: dict[str, Any] = params

    @classmethod
    def from_entities(cls, text: str, entities: list[MessageEntity]) -> Text:
        pass

    def render(
        self,
        *,
        _offset: int = 0,
        _sort: bool = True,
        _collect_entities: bool = True,
    ) -> tuple[str, list[MessageEntity]]:
        """
        Render elements tree as text with entities list

        :return:
        """
        pass

    def _render_entity(self, *, offset: int, length: int) -> MessageEntity:
        pass

    def as_kwargs(
        self,
        *,
        text_key: str = "text",
        entities_key: str = "entities",
        replace_parse_mode: bool = True,
        parse_mode_key: str = "parse_mode",
    ) -> dict[str, Any]:
        """
        Render element tree as keyword arguments for usage in an API call, for example:

        .. code-block:: python

            entities = Text(...)
            await message.answer(**entities.as_kwargs())

        :param text_key:
        :param entities_key:
        :param replace_parse_mode:
        :param parse_mode_key:
        :return:
        """
        pass

    def as_caption_kwargs(self, *, replace_parse_mode: bool = True) -> dict[str, Any]:
        """
        Shortcut for :meth:`as_kwargs` for usage with API calls that take
        ``caption`` as a parameter.

        .. code-block:: python

            entities = Text(...)
            await message.answer_photo(**entities.as_caption_kwargs(), photo=phot)

        :param replace_parse_mode: Will be passed to :meth:`as_kwargs`.
        :return:
        """
        pass

    def as_poll_question_kwargs(self, *, replace_parse_mode: bool = True) -> dict[str, Any]:
        """
        Shortcut for :meth:`as_kwargs` for usage with
        method :class:`aiogram.methods.send_poll.SendPoll`.

        .. code-block:: python

            entities = Text(...)
            await message.answer_poll(**entities.as_poll_question_kwargs(), options=options)

        :param replace_parse_mode: Will be passed to :meth:`as_kwargs`.
        :return:
        """
        pass

    def as_poll_explanation_kwargs(self, *, replace_parse_mode: bool = True) -> dict[str, Any]:
        """
        Shortcut for :meth:`as_kwargs` for usage with
        method :class:`aiogram.methods.send_poll.SendPoll`.

        .. code-block:: python

            question_entities = Text(...)
            explanation_entities = Text(...)
            await message.answer_poll(
                **question_entities.as_poll_question_kwargs(),
                options=options,
                **explanation_entities.as_poll_explanation_kwargs(),
            )

        :param replace_parse_mode: Will be passed to :meth:`as_kwargs`.
        :return:
        """
        pass

    def as_gift_text_kwargs(self, *, replace_parse_mode: bool = True) -> dict[str, Any]:
        """
        Shortcut for :meth:`as_kwargs` for usage with
        method :class:`aiogram.methods.send_gift.SendGift`.

        .. code-block:: python

            entities = Text(...)
            await bot.send_gift(gift_id=gift_id, user_id=user_id, **entities.as_gift_text_kwargs())

        :param replace_parse_mode: Will be passed to :meth:`as_kwargs`.
        :return:
        """
        pass

    def as_html(self) -> str:
        """
        Render elements tree as HTML markup
        """
        pass

    def as_markdown(self) -> str:
        """
        Render elements tree as MarkdownV2 markup
        """
        pass

    def replace(self: Self, *args: Any, **kwargs: Any) -> Self:
        pass

    def as_pretty_string(self, indent: bool = False) -> str:
        pass

    def __add__(self, other: NodeType) -> Text:
        if isinstance(other, Text) and other.type == self.type and self._params == other._params:
            return type(self)(*self, *other, **self._params)
        if type(self) is Text and isinstance(other, str):
            return type(self)(*self, other, **self._params)
        return Text(self, other)

    def __iter__(self) -> Iterator[NodeType]:
        yield from self._body

    def __len__(self) -> int:
        text, _ = self.render(_collect_entities=False)
        return sizeof(text)

    def __getitem__(self, item: slice) -> Text:
        if not isinstance(item, slice):
            msg = "Can only be sliced"
            raise TypeError(msg)
        if (item.start is None or item.start == 0) and item.stop is None:
            return self.replace(*self._body)
        start = 0 if item.start is None else item.start
        stop = len(self) if item.stop is None else item.stop
        if start == stop:
            return self.replace()

        nodes = []
        position = 0

        for node in self._body:
            node_size = len(node)
            current_position = position
            position += node_size
            if position < start:
                continue
            if current_position > stop:
                break
            a = max((0, start - current_position))
            b = min((node_size, stop - current_position))
            new_node = node[a:b]
            if not new_node:
                continue
            nodes.append(new_node)

        return self.replace(*nodes)


class HashTag(Text):
    """
    Hashtag element.

    .. warning::

        The value should always start with '#' symbol

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.HASHTAG`
    """

    type = MessageEntityType.HASHTAG

    def __init__(self, *body: NodeType, **params: Any) -> None:
        if len(body) != 1:
            msg = "Hashtag can contain only one element"
            raise ValueError(msg)
        if not isinstance(body[0], str):
            msg = "Hashtag can contain only string"
            raise ValueError(msg)
        if not body[0].startswith("#"):
            body = ("#" + body[0],)
        super().__init__(*body, **params)


class CashTag(Text):
    """
    Cashtag element.

    .. warning::

        The value should always start with '$' symbol

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.CASHTAG`
    """

    type = MessageEntityType.CASHTAG

    def __init__(self, *body: NodeType, **params: Any) -> None:
        if len(body) != 1:
            msg = "Cashtag can contain only one element"
            raise ValueError(msg)
        if not isinstance(body[0], str):
            msg = "Cashtag can contain only string"
            raise ValueError(msg)
        if not body[0].startswith("$"):
            body = ("$" + body[0],)
        super().__init__(*body, **params)


class BotCommand(Text):
    """
    Bot command element.

    .. warning::

        The value should always start with '/' symbol

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.BOT_COMMAND`
    """

    type = MessageEntityType.BOT_COMMAND


class Url(Text):
    """
    Url element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.URL`
    """

    type = MessageEntityType.URL


class Email(Text):
    """
    Email element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.EMAIL`
    """

    type = MessageEntityType.EMAIL


class PhoneNumber(Text):
    """
    Phone number element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.PHONE_NUMBER`
    """

    type = MessageEntityType.PHONE_NUMBER


class Bold(Text):
    """
    Bold element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.BOLD`
    """

    type = MessageEntityType.BOLD


class Italic(Text):
    """
    Italic element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.ITALIC`
    """

    type = MessageEntityType.ITALIC


class Underline(Text):
    """
    Underline element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.UNDERLINE`
    """

    type = MessageEntityType.UNDERLINE


class Strikethrough(Text):
    """
    Strikethrough element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.STRIKETHROUGH`
    """

    type = MessageEntityType.STRIKETHROUGH


class Spoiler(Text):
    """
    Spoiler element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.SPOILER`
    """

    type = MessageEntityType.SPOILER


class Code(Text):
    """
    Code element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.CODE`
    """

    type = MessageEntityType.CODE


class Pre(Text):
    """
    Pre element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.PRE`
    """

    type = MessageEntityType.PRE

    def __init__(self, *body: NodeType, language: str | None = None, **params: Any) -> None:
        super().__init__(*body, language=language, **params)


class TextLink(Text):
    """
    Text link element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.TEXT_LINK`
    """

    type = MessageEntityType.TEXT_LINK

    def __init__(self, *body: NodeType, url: str, **params: Any) -> None:
        super().__init__(*body, url=url, **params)


class TextMention(Text):
    """
    Text mention element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.TEXT_MENTION`
    """

    type = MessageEntityType.TEXT_MENTION

    def __init__(self, *body: NodeType, user: User, **params: Any) -> None:
        super().__init__(*body, user=user, **params)


class CustomEmoji(Text):
    """
    Custom emoji element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.CUSTOM_EMOJI`
    """

    type = MessageEntityType.CUSTOM_EMOJI

    def __init__(self, *body: NodeType, custom_emoji_id: str, **params: Any) -> None:
        super().__init__(*body, custom_emoji_id=custom_emoji_id, **params)


class BlockQuote(Text):
    """
    Block quote element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.BLOCKQUOTE`
    """

    type = MessageEntityType.BLOCKQUOTE


class ExpandableBlockQuote(Text):
    """
    Expandable block quote element.

    Will be wrapped into :obj:`aiogram.types.message_entity.MessageEntity`
    with type :obj:`aiogram.enums.message_entity_type.MessageEntityType.EXPANDABLE_BLOCKQUOTE`
    """

    type = MessageEntityType.EXPANDABLE_BLOCKQUOTE


class DateTime(Text):
    type = MessageEntityType.DATE_TIME

    def __init__(
        self,
        *body: NodeType,
        unix_time: int | datetime,
        date_time_format: str | None = None,
        **params: Any,
    ) -> None:
        if isinstance(unix_time, datetime):
            unix_time = int(unix_time.timestamp())
        super().__init__(
            *body,
            unix_time=unix_time,
            date_time_format=date_time_format,
            **params,
        )


NODE_TYPES: dict[str | None, type[Text]] = {
    Text.type: Text,
    HashTag.type: HashTag,
    CashTag.type: CashTag,
    BotCommand.type: BotCommand,
    Url.type: Url,
    Email.type: Email,
    PhoneNumber.type: PhoneNumber,
    Bold.type: Bold,
    Italic.type: Italic,
    Underline.type: Underline,
    Strikethrough.type: Strikethrough,
    Spoiler.type: Spoiler,
    Code.type: Code,
    Pre.type: Pre,
    TextLink.type: TextLink,
    TextMention.type: TextMention,
    CustomEmoji.type: CustomEmoji,
    BlockQuote.type: BlockQuote,
    ExpandableBlockQuote.type: ExpandableBlockQuote,
    DateTime.type: DateTime,
}


def _apply_entity(entity: MessageEntity, *nodes: NodeType) -> NodeType:
    """
    Apply single entity to text

    :param entity:
    :param text:
    :return:
    """
    pass


def _unparse_entities(
    text: bytes,
    entities: list[MessageEntity],
    offset: int | None = None,
    length: int | None = None,
) -> Generator[NodeType, None, None]:
    pass


def as_line(*items: NodeType, end: str = "\n", sep: str = "") -> Text:
    """
    Wrap multiple nodes into line with :code:`\\\\n` at the end of line.

    :param items: Text or Any
    :param end: ending of the line, by default is :code:`\\\\n`
    :param sep: separator between items, by default is empty string
    :return: Text
    """
    pass


def as_list(*items: NodeType, sep: str = "\n") -> Text:
    """
    Wrap each element to separated lines

    :param items:
    :param sep:
    :return:
    """
    pass


def as_marked_list(*items: NodeType, marker: str = "- ") -> Text:
    """
    Wrap elements as marked list

    :param items:
    :param marker: line marker, by default is '- '
    :return: Text
    """
    pass


def as_numbered_list(*items: NodeType, start: int = 1, fmt: str = "{}. ") -> Text:
    """
    Wrap elements as numbered list

    :param items:
    :param start: initial number, by default 1
    :param fmt: number format, by default '{}. '
    :return: Text
    """
    pass


def as_section(title: NodeType, *body: NodeType) -> Text:
    """
    Wrap elements as simple section, section has title and body

    :param title:
    :param body:
    :return: Text
    """
    pass


def as_marked_section(
    title: NodeType,
    *body: NodeType,
    marker: str = "- ",
) -> Text:
    """
    Wrap elements as section with marked list

    :param title:
    :param body:
    :param marker:
    :return:
    """
    pass


def as_numbered_section(
    title: NodeType,
    *body: NodeType,
    start: int = 1,
    fmt: str = "{}. ",
) -> Text:
    """
    Wrap elements as section with numbered list

    :param title:
    :param body:
    :param start:
    :param fmt:
    :return:
    """
    pass


def as_key_value(key: NodeType, value: NodeType) -> Text:
    """
    Wrap elements pair as key-value line. (:code:`<b>{key}:</b> {value}`)

    :param key:
    :param value:
    :return: Text
    """
    pass
