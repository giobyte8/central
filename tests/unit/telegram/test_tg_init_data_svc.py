import pytest
import urllib
from central.telegram import tg_init_data_svc as idata_svc
from central.telegram.tg_init_data_svc import TGInitData
from central.utils import crypto


__TG_BOT_TOKEN = 'secret'


@pytest.fixture(scope='module')
def idata_query_string():
    """Generate synthetic init data following same process as described \
        by telegram docs.

    Returns:
        str: Synthetic query string representing test init data
    """
    idata = {
        'query_id': 'AAHuB9Y0AAAAAO4H1jS66K87',
        'user': 'a_random_user',
        'auth_date': '1706502371',
    }

    # Format as a single string, asc sorted by key and using
    # '\n' to separate key/value pairs
    formatted_qs = '\n'.join(f'{k}={v}' for k, v in sorted(idata.items()))

    # Compute hash
    secret_key = crypto.hmac_sha256('WebAppData', __TG_BOT_TOKEN)
    qs_hash = crypto.hmac_sha256_hex(key=secret_key, message=formatted_qs)

    # Append hash to idata and encode as query string
    idata['hash'] = qs_hash
    return urllib.parse.urlencode(idata)


class TestTGInitData:
    def test_get_param(self, idata_query_string):
        idata = TGInitData.from_query_string(idata_query_string)
        assert idata.get_param('query_id') == 'AAHuB9Y0AAAAAO4H1jS66K87'


@pytest.mark.asyncio
async def test_validate_init_data(idata_query_string):
    await idata_svc.validate_init_data(
        idata_query_string,
        __TG_BOT_TOKEN
    )
    # Non thrown exception means test passed
