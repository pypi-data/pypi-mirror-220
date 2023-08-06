from socket import gethostbyname
from urllib.parse import urlparse

from .check import isdomain
from .decorators import try_and_get_data


# Network utils

@try_and_get_data
def get_domain_ip(domain: str):
    return gethostbyname(domain)


def get_host(url: str):
    """Get the host of the input url."""

    if host := urlparse(url).hostname:
        return host

    return (isdomain(url) and url) or None


def domains_is_ip(domains: list[str], ip: str):
    return all([get_domain_ip(domain) == ip for domain in domains])
