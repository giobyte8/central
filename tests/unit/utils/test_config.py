import pytest
import os
from dotenv import load_dotenv, find_dotenv
from central.utils import config as cfg


@pytest.fixture(scope='module', autouse=True)
def load_env():
    """Since default '.env' file was already loaded during import of \
        'central.utils.config' module, this fixture uses the         \
        'override=True' flag to load the test environment file.
    """
    envf = find_dotenv('.tests.env')
    load_dotenv(envf, override=True)


def test_env_loaded():
    assert '80' == cfg.redis_port()
    assert 'testhost.com' == cfg.redis_host()


def test_load_special_chars():
    expected_hash = '$2b$12$plEXp7n6DR/B1dU.B.F8FOkIeYZbbvRZAj77EEg7bJM0oOmbOSRqO'

    rhash = os.environ['RANDOM_HASH']
    rhash_quoted = os.environ['RANDOM_HASH_QUOTED']

    assert expected_hash == rhash
    assert expected_hash == rhash_quoted


def test_interpolated_values():
    unconfirmed_notif_subs = 'ct.tg.unconfirmed_notif_subs'
    assert unconfirmed_notif_subs == cfg.rd_tg_unconfirmed_notif_subs()

