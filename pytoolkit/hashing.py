"""Contains hashing related functions."""

from typing import Any

from pytoolkit.check import is_iterable_but_no_str


def is_hashable(candidate: Any) -> bool:
    """
    Determines whether the `candidate` can be hashed or not.

    Args:
        candidate (Any): The candidate to test if it is hashable.

    Returns:
        bool: `True` if `candidate` is hashable; otherwise `False`.

    Examples:
        >>> is_hashable("i am")
        True
        >>> is_hashable({"I am": "not"})
        False
    """
    try:
        hash(candidate)
    except TypeError:
        return False
    return True


def make_hashable(obj: Any) -> Any:
    """
    Converts a non-hashable instance into a hashable representation. Will take care of nested
    objects (like in iterables, dictionaries) as well. Will not detect a recursion
    and the function will fail in that case.

    Args:
        obj (Any): The object to convert to a hashable object.

    Returns:
        Any: Returns a hashable representation of the passed argument.

    Examples:
        >>> make_hashable("unchanged")
        'unchanged'
        >>> make_hashable((1, 2, 3))
        frozenset({1, 2, 3})
        >>> make_hashable({1: {2: [3, 4, 5]}})
        frozenset({(1, frozenset({(2, frozenset({3, 4, 5}))}))})
    """
    if isinstance(obj, dict):
        return frozenset({
            make_hashable(k): make_hashable(v)
            for k, v in obj.items()
        }.items())
    if is_iterable_but_no_str(obj):
        return frozenset([make_hashable(item) for item in obj])

    return obj if is_hashable(obj) else str(obj)
