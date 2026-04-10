from functools import lru_cache


class TokenValidationError(Exception):
    pass


@lru_cache
def validate_token(token: str) -> bool:
    """
    Validate Telegram token

    :param token:
    :return:
    """
    pass


@lru_cache
def extract_bot_id(token: str) -> int:
    """
    Extract bot ID from Telegram token

    :param token:
    :return:
    """
    pass
