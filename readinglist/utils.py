try:
    import simplejson as json
except ImportError:  # pragma: no cover
    import json  # NOQA

import ast
import os
import time
from base64 import b64decode, b64encode
from binascii import hexlify

from colander import null


# removes whitespace, newlines, and tabs from the beginning/end of a string
strip_whitespace = lambda v: v.strip(' \t\n\r') if v is not null else v

msec_time = lambda: int(time.time() * 1000.0)  # floor

# Get a classname from a class.
classname = lambda c: c.__class__.__name__.lower()


def random_bytes_hex(bytes_length):
    """Return a hexstring of bytes_length cryptographic-friendly random bytes.
    """
    return hexlify(os.urandom(bytes_length)).decode('utf-8')


def native_value(value):
    """Convert string value to native python values."""
    if value.lower() in ['on', 'true', 'yes', '1']:
        value = True
    elif value.lower() in ['off', 'false', 'no', '0']:
        value = False
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def decode_token(token):
    """Take a token and return the decoded base64 JSON."""
    return json.loads(b64decode(token))


def encode_token(pagination_rules):
    """Take a list of rules and return a base64-ed JSON."""
    json_rules = json.dumps(pagination_rules)
    return b64encode(json_rules.encode('utf-8')).decode('utf-8')


def Enum(**enums):
    return type('Enum', (), enums)


COMPARISON = Enum(
    LT='<',
    MIN='>=',
    MAX='<=',
    NOT='!=',
    EQ='==',
    GT='>',
)
