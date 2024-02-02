import hashlib
import hmac
from typing import Union


def hmac_sha256(key: Union[str, bytes], message: str) -> bytes:
    """Computes hmac using sha256 for given message and secret key.

        See:
          1. https://en.wikipedia.org/wiki/HMAC
          2. https://docs.python.org/3/library/hmac.html#module-hmac
    """
    if isinstance(key, str):
        key = key.encode()

    return hmac.digest(
        key,
        message.encode(),
        hashlib.sha256
    )


def hmac_sha256_hex(key: Union[str, bytes], message: str) -> str:
    """Computes hmac using sha256 for given message and secret key. \
        Returns hexadecimal representation of digest.
    """
    if isinstance(key, str):
        key = key.encode()

    auth_code = hmac.new(
        key,
        message.encode(),
        hashlib.sha256
    )
    return auth_code.hexdigest()


def hmac_verify(hmac1: str, hmac2: str) -> bool:
    """Returns True if given HMACs are equals, False otherwise.
    """
    return hmac.compare_digest(hmac1, hmac2)
