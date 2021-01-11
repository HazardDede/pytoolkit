"""Contains various checking functions."""

from typing import Any


def is_iterable_but_no_str(candidate: Any) -> bool:
    """
    Checks if the given `candidate` is an `iterable` but not a `str` instance

    Args:
        candidate (Any): The candidate to test.

    Returns:
        bool: Returns `True` if the given `candidate` is an `iterable` but no `str`; otherwise `False`.

    Example:
        >>> is_iterable_but_no_str(['a'])
        True
        >>> is_iterable_but_no_str('a')
        False
        >>> is_iterable_but_no_str(None)
        False
    """
    return hasattr(candidate, '__iter__') and not isinstance(candidate, (str, bytes))


def is_real_float(candidate: Any) -> bool:
    """
    Checks if the given `candidate` is a real `float`. An `integer` will return `False`.

    Args:
        candidate (Any): The candidate to test.

    Returns:
        bool: Returns `True` if the `candidate` is a real float; otherwise `False.`

    Examples:
        >>> is_real_float(1.1)
        True
        >>> is_real_float(1.0)
        False
        >>> is_real_float(object())
        False
        >>> is_real_float(1)
        False
        >>> is_real_float("str")
        False
    """
    try:
        return not float(candidate).is_integer()
    except (TypeError, ValueError):
        return False
