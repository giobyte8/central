"""When working with mini apps, telegram will provide user and      \
    initialization information as an 'init_data' object.            \

    Such info needs to be validated and used in server, this        \
    service provides all functionality to deal with it

    References:                                                     \
    https://core.telegram.org/bots/webapps#initializing-mini-apps
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""
from __future__ import annotations

import urllib
from central.telegram.errors import (
    TGInitDataAuthError,
    TGInitDataParseError
)
from central.utils import crypto


class TGInitData():

    @staticmethod
    def from_query_string(qs: str) -> TGInitData:
        try:
            parsed_qs = urllib.parse.parse_qs(qs)
            return TGInitData(parsed_qs)
        except Exception as root_cause:
            raise TGInitDataParseError(str(root_cause))

    def __init__(self, init_data: dict) -> None:
        self.init_data = init_data

    def authenticate(self, bot_token: str):
        """Verifies authenticity of init data, which means it verifies \
            it was generated by telegram and unaltered.                \

            Authentication process follows official guidelines as      \
            described at oficial docs, see 'References' in module's    \
            header.

        Args:
            bot_token (str): Telegram bot token. Is required to        \
                generate secret key for hmac verification

        Raises:
            TGInitDataAuthError: If 'hash' is not present in init data
            TGInitDataAuthError: If 'hash' verification fails
        """
        idata_hash = self.get_param('hash')
        if not idata_hash:
            raise TGInitDataAuthError('Hash param not found')

        # Format init data for authenticity verification
        idata_pairs = []
        for key, values in self.init_data.items():
            if key == 'hash':
                continue
            idata_pairs.append(f'{ key }={ values[0] }')
        idata_pairs.sort()
        formatted_idata = '\n'.join(idata_pairs)

        # Verify authenticity
        secret_key_bytes = crypto.hmac_sha256('WebAppData', bot_token)
        auth_code = crypto.hmac_sha256_hex(secret_key_bytes, formatted_idata)
        if not crypto.hmac_verify(auth_code, idata_hash):
            raise TGInitDataAuthError('Hash verification failed')

    def get_param(self, key: str) -> str | None:
        """Retrieves first value for given init param or None if param \
            is not present in init data

        Args:
            key (str): Param name to retrieve value for
        Returns:
            str: Value for param OR None if param wasn't found
        """
        return self.init_data.get(key, [None])[0]


async def validate_init_data(init_data: str, bot_token: str) -> None:
    """Validates authenticity of provided init data by following official \
        guidelines for cryptographic verification.

    Args:
        init_data (str): Raw string of init data provided by telegram
        bot_token (str): Token of bot that generated init data
    """
    idata = TGInitData.from_query_string(init_data)
    idata.authenticate(bot_token)
