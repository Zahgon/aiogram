import hashlib
import hmac
import json
from collections.abc import Callable
from datetime import datetime
from operator import itemgetter
from typing import Any
from urllib.parse import parse_qsl

from aiogram.types import TelegramObject


class WebAppChat(TelegramObject):
    """
    This object represents a chat.

    Source: https://core.telegram.org/bots/webapps#webappchat
    """

    id: int
    """Unique identifier for this chat. This number may have more than 32 significant bits
    and some programming languages may have difficulty/silent defects in interpreting it.
    But it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this identifier."""
    type: str
    """Type of chat, can be either “group”, “supergroup” or “channel”"""
    title: str
    """Title of the chat"""
    username: str | None = None
    """Username of the chat"""
    photo_url: str | None = None
    """URL of the chat’s photo. The photo can be in .jpeg or .svg formats.
    Only returned for Web Apps launched from the attachment menu."""


class WebAppUser(TelegramObject):
    """
    This object contains the data of the Web App user.

    Source: https://core.telegram.org/bots/webapps#webappuser
    """

    id: int
    """A unique identifier for the user or bot. This number may have more than 32 significant bits
    and some programming languages may have difficulty/silent defects in interpreting it.
    It has at most 52 significant bits, so a 64-bit integer or a double-precision float type
    is safe for storing this identifier."""
    is_bot: bool | None = None
    """True, if this user is a bot. Returns in the receiver field only."""
    first_name: str
    """First name of the user or bot."""
    last_name: str | None = None
    """Last name of the user or bot."""
    username: str | None = None
    """Username of the user or bot."""
    language_code: str | None = None
    """IETF language tag of the user's language. Returns in user field only."""
    is_premium: bool | None = None
    """True, if this user is a Telegram Premium user."""
    added_to_attachment_menu: bool | None = None
    """True, if this user added the bot to the attachment menu."""
    allows_write_to_pm: bool | None = None
    """True, if this user allowed the bot to message them."""
    photo_url: str | None = None
    """URL of the user’s profile photo. The photo can be in .jpeg or .svg formats.
    Only returned for Web Apps launched from the attachment menu."""


class WebAppInitData(TelegramObject):
    """
    This object contains data that is transferred to the Web App when it is opened.
    It is empty if the Web App was launched from a keyboard button.

    Source: https://core.telegram.org/bots/webapps#webappinitdata
    """

    query_id: str | None = None
    """A unique identifier for the Web App session, required for sending messages
    via the answerWebAppQuery method."""
    user: WebAppUser | None = None
    """An object containing data about the current user."""
    receiver: WebAppUser | None = None
    """An object containing data about the chat partner of the current user in the chat where
    the bot was launched via the attachment menu.
    Returned only for Web Apps launched via the attachment menu."""
    chat: WebAppChat | None = None
    """An object containing data about the chat where the bot was launched via the attachment menu.
    Returned for supergroups, channels, and group chats – only for Web Apps launched via the
    attachment menu."""
    chat_type: str | None = None
    """Type of the chat from which the Web App was opened.
    Can be either “sender” for a private chat with the user opening the link,
    “private”, “group”, “supergroup”, or “channel”.
    Returned only for Web Apps launched from direct links."""
    chat_instance: str | None = None
    """Global identifier, uniquely corresponding to the chat from which the Web App was opened.
    Returned only for Web Apps launched from a direct link."""
    start_param: str | None = None
    """The value of the startattach parameter, passed via link.
    Only returned for Web Apps when launched from the attachment menu via link.
    The value of the start_param parameter will also be passed in the GET-parameter
    tgWebAppStartParam, so the Web App can load the correct interface right away."""
    can_send_after: int | None = None
    """Time in seconds, after which a message can be sent via the answerWebAppQuery method."""
    auth_date: datetime
    """Unix time when the form was opened."""
    hash: str
    """A hash of all passed parameters, which the bot server can use to check their validity."""


def check_webapp_signature(token: str, init_data: str) -> bool:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token: bot Token
    :param init_data: data from frontend to be validated
    :return:
    """
    pass


def parse_webapp_init_data(
    init_data: str,
    *,
    loads: Callable[..., Any] = json.loads,
) -> WebAppInitData:
    """
    Parse WebApp init data and return it as WebAppInitData object

    This method doesn't make any security check, so you shall not trust to this data,
    use :code:`safe_parse_webapp_init_data` instead.

    :param init_data: data from frontend to be parsed
    :param loads:
    :return:
    """
    pass


def safe_parse_webapp_init_data(
    token: str,
    init_data: str,
    *,
    loads: Callable[..., Any] = json.loads,
) -> WebAppInitData:
    """
    Validate raw WebApp init data and return it as WebAppInitData object

    Raise :obj:`ValueError` when data is invalid

    :param token: bot token
    :param init_data: data from frontend to be parsed and validated
    :param loads:
    :return:
    """
    pass
