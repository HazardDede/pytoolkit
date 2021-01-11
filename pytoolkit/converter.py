"""Contains functions to convert between datatypes."""
from typing import Any, Iterable, List, Optional, Union


def listify(item_or_items: Union[Any, Iterable[Any]]) -> Optional[List[Any]]:
    """
    Makes a list out of the given item or items.

    Args:
        item_or_items (Any): A single value or an iterable.

    Returns:
        List[Any]: Returns the given argument as a list.
        If the argument is already a list the identity will be returned unaltered.

    Examples:
        >>> listify(1)
        [1]
        >>> listify('str')
        ['str']
        >>> listify(('i', 'am', 'a', 'tuple'))
        ['i', 'am', 'a', 'tuple']
        >>> print(listify(None))
        None

        >>> # An instance of dict is used as is
        >>> listify({'foo': 'bar'})
        [{'foo': 'bar'}]

        >>> # An instance of lists is unchanged
        >>> l = ['i', 'am', 'a', 'list']
        >>> l_res = listify(l)
        >>> l_res
        ['i', 'am', 'a', 'list']
        >>> l_res is l
        True
    """
    if item_or_items is None:
        return None
    if isinstance(item_or_items, list):
        return item_or_items
    if isinstance(item_or_items, dict):
        return [item_or_items]
    if hasattr(item_or_items, '__iter__') and not isinstance(item_or_items, str):
        return list(item_or_items)
    return [item_or_items]


def try_parse_bool(  # pylint: disable=too-many-return-statements
        value: Any, default: Optional[bool] = None
) -> Optional[bool]:
    """
    Tries to parse the given value as a boolean. If the parsing is unsuccessful the default will
    be returned. A special case is `None`: It will always return the default value.

    Args:
        value (Any): Value to parse.
        default (bool, optional): The value to return in case the conversion is not successful.

    Returns:
        (bool, optional): If the conversion is successful the converted representation of value; otherwise the default.

    Examples:
        >>> try_parse_bool(1)
        True
        >>> try_parse_bool('true')
        True
        >>> try_parse_bool('T')
        True
        >>> try_parse_bool('F')
        False
        >>> try_parse_bool(False)
        False
        >>> print(try_parse_bool('unknown', default=None))
        None
        >>> try_parse_bool(None, default=True)  # Special case
        True
        >>> try_parse_bool(1.0)
        True
        >>> try_parse_bool(0.99)
        True
        >>> try_parse_bool(0.0)
        False
        >>> try_parse_bool(lambda x: False, default=True)  # Will not be invoked
        True
    """
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ['t', 'true', '1', 'wahr', 'ja', 'yes', 'on']:
            return True
        if value.lower() in ['f', 'false', '0', 'falsch', 'nein', 'no', 'off']:
            return False
        return default

    try:
        return bool(value)
    except (ValueError, TypeError):  # pragma: no cover
        return default
