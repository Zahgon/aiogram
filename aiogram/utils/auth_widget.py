import hashlib
import hmac
from typing import Any


def check_signature(token: str, hash: str, **kwargs: Any) -> bool:
    """
    Generate hexadecimal representation
    of the HMAC-SHA-256 signature of the data-check-string
    with the SHA256 hash of the bot's token used as a secret key

    :param token:
    :param hash:
    :param kwargs: all params received on auth
    :return:
    """
    pass


def check_integrity(token: str, data: dict[str, Any]) -> bool:
    """
    Verify the authentication and the integrity
    of the data received on user's auth

    :param token: Bot's token
    :param data: all data that came on auth
    :return:
    """
    pass
