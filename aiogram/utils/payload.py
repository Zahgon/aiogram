"""
Payload preparing

We have added some utils to make work with payload easier.

Basic encode example:

    .. code-block:: python

        from aiogram.utils.payload import encode_payload

        encoded = encode_payload("foo")

        # result: "Zm9v"

Basic decode it back example:

    .. code-block:: python

        from aiogram.utils.payload import decode_payload

        encoded = "Zm9v"
        decoded = decode_payload(encoded)
        # result: "foo"

Encoding and decoding with your own methods:

    1. Create your own cryptor

        .. code-block:: python

            from Cryptodome.Cipher import AES
            from Cryptodome.Util.Padding import pad, unpad

            class Cryptor:
                def __init__(self, key: str):
                    self.key = key.encode("utf-8")
                    self.mode = AES.MODE_ECB  # never use ECB in strong systems obviously
                    self.size = 32

                @property
                def cipher(self):
                    return AES.new(self.key, self.mode)

                def encrypt(self, data: bytes) -> bytes:
                    return self.cipher.encrypt(pad(data, self.size))

                def decrypt(self, data: bytes) -> bytes:
                    decrypted_data = self.cipher.decrypt(data)
                    return unpad(decrypted_data, self.size)

    2. Pass cryptor callable methods to aiogram payload tools

        .. code-block:: python

            cryptor = Cryptor("abcdefghijklmnop")
            encoded = encode_payload("foo", encoder=cryptor.encrypt)
            decoded = decode_payload(encoded_payload, decoder=cryptor.decrypt)

            # result: decoded == "foo"

"""

from __future__ import annotations

from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def encode_payload(
    payload: str,
    encoder: Callable[[bytes], bytes] | None = None,
) -> str:
    """Encode payload with encoder.

    Result also will be encoded with URL-safe base64url.
    """
    pass


def decode_payload(
    payload: str,
    decoder: Callable[[bytes], bytes] | None = None,
) -> str:
    """Decode URL-safe base64url payload with decoder."""
    pass


def _encode_b64(payload: bytes) -> str:
    """Encode with URL-safe base64url."""
    pass


def _decode_b64(payload: str) -> bytes:
    """Decode with URL-safe base64url."""
    pass
