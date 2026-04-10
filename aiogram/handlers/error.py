from abc import ABC

from aiogram.handlers.base import BaseHandler


class ErrorHandler(BaseHandler[Exception], ABC):
    """
    Base class for errors handlers
    """

    @property
    def exception_name(self) -> str:
        pass

    @property
    def exception_message(self) -> str:
        pass
