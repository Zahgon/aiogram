from typing import Any

from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n.lazy_proxy import LazyProxy


def get_i18n() -> I18n:
    pass


def gettext(*args: Any, **kwargs: Any) -> str:
    pass


def lazy_gettext(*args: Any, **kwargs: Any) -> LazyProxy:
    pass


ngettext = gettext
lazy_ngettext = lazy_gettext
