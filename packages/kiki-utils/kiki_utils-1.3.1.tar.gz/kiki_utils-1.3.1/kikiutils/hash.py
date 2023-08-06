import hashlib

from .string import s2b


def hash(fnc, text: bytes | str, return_bytes: bool) -> bytes | str:
    return fnc(s2b(text)).digest() if return_bytes else fnc(s2b(text)).hexdigest()


def md5(text: bytes | str, return_bytes: bool = False):
    return hash(hashlib.md5, text, return_bytes)


def sha3_224(text: bytes | str, return_bytes: bool = False):
    return hash(hashlib.sha3_224, text, return_bytes)


def sha3_256(text: bytes | str, return_bytes: bool = False):
    return hash(hashlib.sha3_256, text, return_bytes)


def sha3_384(text: bytes | str, return_bytes: bool = False):
    return hash(hashlib.sha3_384, text, return_bytes)


def sha3_512(text: bytes | str, return_bytes: bool = False):
    return hash(hashlib.sha3_512, text, return_bytes)
