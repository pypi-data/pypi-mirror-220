import os
import re

from functools import wraps
from typing import Callable

from .typehint import P, PathOrStr, T


ALLOWED_EMAILS = [
    'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'aol.com',
    'hotmail.co.uk',
    'hotmail.fr',
    'msn.com',
    'wanadoo.fr',
    'live.com',
    'hotmail.it',
    'qq.com'
]

domain_pattern = re.compile(
    r'^(?:[a-zA-Z0-9]'  # First character of the domain
    r'(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)'  # Sub domain + hostname
    r'+[A-Za-z0-9][A-Za-z0-9-_]{0,61}'  # First 61 characters of the gTLD
    r'[A-Za-z]$'  # Last character of the gTLD
)


# Check

def _base(check_type):
    def decorator(view_func: Callable[P, T]) -> Callable[P, bool]:
        @wraps(view_func)
        def wrapped_view(*args):
            return all([isinstance(arg, check_type) for arg in args])
        return wrapped_view
    return decorator


@_base(bytes)
def isbytes(*args: object):
    """Determine whether it is bytes."""


def isdomain(domain: str):
    """Check domain."""

    return domain_pattern.match(domain) is not None


def isemail(email: str):
    """Check email format and ping the domain."""

    if re.match(r'.*[+\-*/\\;&|\s​].*', email):
        return False

    domain = email.split('@')[-1].lower()
    return domain in ALLOWED_EMAILS or isdomain(domain)


@_base(dict)
def isdict(*args: object):
    """Determine whether it is dict."""


def isdir(*args: PathOrStr):
    """Determine whether path is dir."""

    return all([os.path.isdir(arg) for arg in args])


def isfile(*args: PathOrStr):
    """Determine whether path is file."""

    return all([os.path.isfile(arg) for arg in args])


@_base(int)
def isint(*args: object):
    """Determine whether it is int."""


@_base(list)
def islist(*args: object):
    """Determine whether it is list."""


@_base(str)
def isstr(*args: object):
    """Determine whether it is str."""
