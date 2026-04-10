import base64
from operator import itemgetter
from urllib.parse import parse_qsl

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .web_app import WebAppInitData, parse_webapp_init_data

PRODUCTION_PUBLIC_KEY = bytes.fromhex(
    "e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d",
)
TEST_PUBLIC_KEY = bytes.fromhex("40055058a4ee38156a06562e52eece92a771bcd8346a8c4615cb7376eddf72ec")


def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    pass


def safe_check_webapp_init_data_from_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> WebAppInitData:
    """
    Validate raw WebApp init data using only bot id and return it as WebAppInitData object

    :param bot_id: bot id
    :param init_data: data from frontend to be parsed and validated
    :param public_key_bytes: public key
    :return: WebAppInitData object
    """
    pass
