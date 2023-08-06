import hashlib

from .string import s2b
from .typehint import BytesOrStr


def hash(fnc, text: BytesOrStr, return_bytes: bool) -> BytesOrStr:
    return fnc(s2b(text)).digest() if return_bytes else fnc(s2b(text)).hexdigest()


def md5(text: BytesOrStr, return_bytes: bool = False):
    return hash(hashlib.md5, text, return_bytes)


def sha3_224(text: BytesOrStr, return_bytes: bool = False):
    return hash(hashlib.sha3_224, text, return_bytes)


def sha3_256(text: BytesOrStr, return_bytes: bool = False):
    return hash(hashlib.sha3_256, text, return_bytes)


def sha3_384(text: BytesOrStr, return_bytes: bool = False):
    return hash(hashlib.sha3_384, text, return_bytes)


def sha3_512(text: BytesOrStr, return_bytes: bool = False):
    return hash(hashlib.sha3_512, text, return_bytes)
