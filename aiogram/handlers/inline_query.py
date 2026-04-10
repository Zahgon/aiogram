from abc import ABC

from aiogram.handlers import BaseHandler
from aiogram.types import InlineQuery, User


class InlineQueryHandler(BaseHandler[InlineQuery], ABC):
    """
    Base class for inline query handlers
    """

    @property
    def from_user(self) -> User:
        pass

    @property
    def query(self) -> str:
        pass
