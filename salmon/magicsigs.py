import re
import base64

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util import number

_WHITESPACE_RE = re.compile(r'\s+')
_KEY_RE = re.compile(
    r"""RSA\.
    (?P<mod>[^\.]+)
    \.
    (?P<exp>[^\.]+)
    (?:\.
    (?P<private_exp>[^\.]+)
    )?""",
    re.VERBOSE)


def encode(s):
    return base64.urlsafe_b64encode(
        unicode(s).encode('utf-8')).encode('utf-8')


def extract_key_details(key):
    match = _KEY_RE.match(key)
    b64_to_num = lambda a: number.bytes_to_long(base64.urlsafe_b64decode(a))
    return (
        b64_to_num(match.group('mod')),
        b64_to_num(match.group('exp')),
        b64_to_num(match.group('private_exp')),
    )


def sign(data, keypair):
    """
    Sign the data. Most of this is taken verbatim from John Panzer's
    reference implementation:

    http://code.google.com/p/salmon-protocol/
    """
    rng = Random.new().read
    h = SHA256.new(data).digest()

    magic_sha256_header = [0x30, 0x31, 0x30, 0xd, 0x6, 0x9, 0x60, 0x86,
                           0x48, 0x1, 0x65, 0x3, 0x4, 0x2, 0x1, 0x5, 0x0,
                           0x4, 0x20]
    encoded = ''.join([chr(c) for c in magic_sha256_header]) + h

    # Round up to next byte
    modulus_size = keypair.size()
    msg_size_bits = modulus_size + 8 - (modulus_size % 8)
    pad_string = chr(0xFF) * (msg_size_bits / 8 - len(encoded) - 3)
    esma_msg = chr(0) + chr(1) + pad_string + chr(0) + encoded

    sig_long = keypair.sign(esma_msg, rng)[0]
    sig_bytes = number.long_to_bytes(sig_long)
    return base64.urlsafe_b64encode(sig_bytes).encode('utf-8')


def magic_envelope(raw_data, data_type, key):
    """Wrap the provided data in a magic envelope."""
    key = re.sub(_WHITESPACE_RE, '', key)
    keypair = RSA.construct((extract_key_details(key)))
    encoded_data = encode(raw_data)
    signed = sign(encoded_data, keypair)
    # todo - xml construction
    return str(dict(data=encoded_data, sig=signed))
