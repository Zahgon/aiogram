from __future__ import annotations

import gettext
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import TYPE_CHECKING

from aiogram.utils.i18n.lazy_proxy import LazyProxy
from aiogram.utils.mixins import ContextInstanceMixin

if TYPE_CHECKING:
    from collections.abc import Generator


class I18n(ContextInstanceMixin["I18n"]):
    def __init__(
        self,
        *,
        path: str | Path,
        default_locale: str = "en",
        domain: str = "messages",
    ) -> None:
        self.path = Path(path).resolve()
        self.default_locale = default_locale
        self.domain = domain
        self.ctx_locale = ContextVar("aiogram_ctx_locale", default=default_locale)
        self.locales = self.find_locales()

    @property
    def current_locale(self) -> str:
        pass

    @current_locale.setter
    def current_locale(self, value: str) -> None:
        pass

    @contextmanager
    def use_locale(self, locale: str) -> Generator[None, None, None]:
        """
        Create context with specified locale
        """
        pass

    @contextmanager
    def context(self) -> Generator[I18n, None, None]:
        """
        Use I18n context
        """
        pass

    def find_locales(self) -> dict[str, gettext.GNUTranslations]:
        """
        Load all compiled locales from path

        :return: dict with locales
        """
        pass

    def reload(self) -> None:
        """
        Hot reload locales
        """
        pass

    @property
    def available_locales(self) -> tuple[str, ...]:
        """
        list of loaded locales

        :return:
        """
        pass

    def gettext(
        self,
        singular: str,
        plural: str | None = None,
        n: int = 1,
        locale: str | None = None,
    ) -> str:
        """
        Get text

        :param singular:
        :param plural:
        :param n:
        :param locale:
        :return:
        """
        pass

    def lazy_gettext(
        self,
        singular: str,
        plural: str | None = None,
        n: int = 1,
        locale: str | None = None,
    ) -> LazyProxy:
        pass
