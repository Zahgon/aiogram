from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import TelegramMethod
from aiogram.types import InputFile


def _get_fake_bot(default: DefaultBotProperties | None = None) -> Bot:
    pass


@dataclass
class DeserializedTelegramObject:
    """
    Represents a dumped Telegram object.

    :param data: The dumped data of the Telegram object.
    :type data: Any
    :param files: The dictionary containing the file names as keys
        and the corresponding `InputFile` objects as values.
    :type files: dict[str, InputFile]
    """

    data: Any
    files: dict[str, InputFile]


def deserialize_telegram_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    pass


def deserialize_telegram_object_to_python(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> Any:
    """
    Deserialize telegram object to JSON compatible Python object excluding files.

    :param obj: The telegram object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized telegram object.
    """
    pass
