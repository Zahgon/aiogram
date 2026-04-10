from collections.abc import Sequence
from ipaddress import IPv4Address, IPv4Network

DEFAULT_TELEGRAM_NETWORKS = [
    IPv4Network("149.154.160.0/20"),
    IPv4Network("91.108.4.0/22"),
]


class IPFilter:
    def __init__(self, ips: Sequence[str | IPv4Network | IPv4Address] | None = None):
        self._allowed_ips: set[IPv4Address] = set()

        if ips:
            self.allow(*ips)

    def allow(self, *ips: str | IPv4Network | IPv4Address) -> None:
        pass

    def allow_ip(self, ip: str | IPv4Network | IPv4Address) -> None:
        pass

    @classmethod
    def default(cls) -> "IPFilter":
        pass

    def check(self, ip: str | IPv4Address) -> bool:
        pass

    def __contains__(self, item: str | IPv4Address) -> bool:
        return self.check(item)
