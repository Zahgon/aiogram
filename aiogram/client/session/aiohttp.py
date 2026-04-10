from __future__ import annotations

import asyncio
import ssl
from collections.abc import AsyncGenerator, Iterable
from typing import TYPE_CHECKING, Any, cast

import certifi
from aiohttp import BasicAuth, ClientError, ClientSession, FormData, TCPConnector
from aiohttp.hdrs import USER_AGENT
from aiohttp.http import SERVER_SOFTWARE
from typing_extensions import Self

from aiogram.__meta__ import __version__
from aiogram.exceptions import TelegramNetworkError
from aiogram.methods.base import TelegramType

from .base import BaseSession

if TYPE_CHECKING:
    from aiogram.client.bot import Bot
    from aiogram.methods import TelegramMethod
    from aiogram.types import InputFile

_ProxyBasic = str | tuple[str, BasicAuth]
_ProxyChain = Iterable[_ProxyBasic]
_ProxyType = _ProxyChain | _ProxyBasic


def _retrieve_basic(basic: _ProxyBasic) -> dict[str, Any]:
    pass


def _prepare_connector(chain_or_plain: _ProxyType) -> tuple[type[TCPConnector], dict[str, Any]]:
    pass


class AiohttpSession(BaseSession):
    def __init__(self, proxy: _ProxyType | None = None, limit: int = 100, **kwargs: Any) -> None:
        """
        Client session based on aiohttp.

        :param proxy: The proxy to be used for requests. Default is None.
        :param limit: The total number of simultaneous connections. Default is 100.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

        self._session: ClientSession | None = None
        self._connector_type: type[TCPConnector] = TCPConnector
        self._connector_init: dict[str, Any] = {
            "ssl": ssl.create_default_context(cafile=certifi.where()),
            "limit": limit,
            "ttl_dns_cache": 3600,  # Workaround for https://github.com/aiogram/aiogram/issues/1500
        }
        self._should_reset_connector = True  # flag determines connector state
        self._proxy: _ProxyType | None = None

        if proxy is not None:
            try:
                self._setup_proxy_connector(proxy)
            except ImportError as exc:  # pragma: no cover
                msg = (
                    "In order to use aiohttp client for proxy requests, install "
                    "https://pypi.org/project/aiohttp-socks/"
                )
                raise RuntimeError(msg) from exc

    def _setup_proxy_connector(self, proxy: _ProxyType) -> None:
        pass

    @property
    def proxy(self) -> _ProxyType | None:
        pass

    @proxy.setter
    def proxy(self, proxy: _ProxyType) -> None:
        pass

    async def create_session(self) -> ClientSession:
        pass

    async def close(self) -> None:
        pass

    def build_form_data(self, bot: Bot, method: TelegramMethod[TelegramType]) -> FormData:
        pass

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        pass

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        pass

    async def __aenter__(self) -> Self:
        await self.create_session()
        return self
