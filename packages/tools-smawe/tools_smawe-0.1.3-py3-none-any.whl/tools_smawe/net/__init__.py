import socket
import re
import logging
import platform

_IS_LESS_THEN_PY39 = float(".".join(platform.python_version_tuple()[:-1])) < 3.9
if _IS_LESS_THEN_PY39:
    import typing
    List = typing.List
    del typing
else:
    List = list


def _get_domain(url: str) -> str:
    try:
        _m = re.search(r"//(.*?)/", url.strip())
        return _m.group(1)
    except AttributeError:
        _m = re.search(r"//(.*)", url.strip())
        if _m:
            return _m.group(1)

    raise ValueError("please enter a valid url")


def get_ip(url: str = None, domain: str = None) -> List[str]:
    """
    get url or domain ip
    :param url: can be url or domain
    :param domain: website domain
    :return: list[str]
    """
    if (url and not domain) or (url and domain):
        url = url.strip()
        if "/" not in url:
            _domain = url
        else:
            _domain = _get_domain(url)
        try:
            (hostname, alias_list, ipaddr_list) = socket.gethostbyname_ex(_domain)
            return ipaddr_list
        except socket.gaierror as e:
            logging.error("please enter valid url")
            logging.error(e)

    if domain:
        domain = domain.strip()
        try:
            (hostname, alias_list, ipaddr_list) = socket.gethostbyname_ex(domain)
            return ipaddr_list
        except socket.gaierror as e:
            logging.error("please enter valid domain")
            logging.error(e)

    raise ValueError("please enter valid parameters")
