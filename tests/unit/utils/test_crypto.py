from central.utils import crypto


__hmac_key = 'secret_key'
__message = 'random message'

# HMAC externally computed for same key and message
__exp_hmac = '4b513d3012fd18398a8b8162ba8d3d40a38aec902a9076d67ff4d86b08cd5073'


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
