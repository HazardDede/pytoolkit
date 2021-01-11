"""Contains networking utility functions."""


def is_local(server: str, allow_ipv6: bool = False) -> bool:
    """
    Checks if the given server (name or ip address) is actually a local one.

    Args:
        server (str): The server name or ip to check.
        allow_ipv6 (bool): If True the local ipv6 ip address is checked too.

    Returns:
        bool: Returns `True` if the given server is local; otherwise `False`.

    Examples:

        >>> is_local('www.google.de')
        False
        >>> is_local('LOCALHOST')
        True
        >>> is_local('127.0.0.1')
        True
        >>> is_local('0.0.0.0')
        True
        >>> is_local('::1')
        False
        >>> is_local('::1', allow_ipv6=True)
        True
    """
    server = str(server)
    return (
        server.lower() == 'localhost'
        or server == '127.0.0.1'
        or server == '0.0.0.0'
        or (server == '::1' and allow_ipv6)  # IPv6
    )
