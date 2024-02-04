import pytest
from dotenv import load_dotenv, find_dotenv
from central.utils import config as cfg
from central.utils import crypto


__hmac_key = 'secret_key'
__message = 'random message'

# HMAC externally computed for same key and message
__exp_hmac = '4b513d3012fd18398a8b8162ba8d3d40a38aec902a9076d67ff4d86b08cd5073'


@pytest.fixture(scope='module', autouse=True)
def load_env():
    """Since default '.env' file was already loaded during import of \
        'central.utils.config' module, this fixture uses the         \
        'override=True' flag to load the test environment file.
    """
    envf = find_dotenv('.tests.env')
    load_dotenv(envf, override=True)


def test_hmac_sha256():
    hmac = crypto.hmac_sha256(__hmac_key, __message)

    # Manually convert to hex to verify
    #   Alternatively you can use: binascii.hexlify(hmac)
    hmac_hex = hmac.hex()
    assert hmac_hex == __exp_hmac


def test_hmac_sha256_hex():
    hmac_hex = crypto.hmac_sha256_hex(__hmac_key, __message)
    assert hmac_hex == __exp_hmac


def test_hmac_verify():
    hmac_hex = crypto.hmac_sha256_hex(__hmac_key, __message)

    # Both hmacs should match
    assert crypto.hmac_verify(__exp_hmac, hmac_hex)


def test_checkpw():
    pwd_hash = cfg.notif_feed_subs_pwd()

    assert not crypto.checkpw('test_wrong', pwd_hash)
    assert crypto.checkpw('test', pwd_hash)
