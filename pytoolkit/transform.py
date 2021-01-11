"""Contains transformation functions."""
import re
from typing import Any, Callable, Dict, Optional

from typeguard import typechecked

TransformDictFun = Callable[[Any], Any]


def bps_mbps(val: float) -> float:
    """
    Converts bits per second (bps) into megabits per second (mbps).

    Args:
        val (float): The value in bits per second to convert.

    Returns:
        Returns val in megabits per second.

    Examples:

        >>> bps_mbps(1000000)
        1.0
        >>> bps_mbps(1129000)
        1.13
    """
    return round(float(val) / 1000000, 2)


def camel_to_snake(camel_str: str) -> str:
    """
    Converts camelCase to snake_case.
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case

    Args:
        camel_str (str): The camelCase string to convert to snake_case.

    Returns:
        Returns the snake_case representation of the passed camelCase string.

    >>> camel_to_snake('CamelCase')
    'camel_case'
    >>> camel_to_snake('CamelCamelCase')
    'camel_camel_case'
    >>> camel_to_snake('Camel2Camel2Case')
    'camel2_camel2_case'
    >>> camel_to_snake('getHTTPResponseCode')
    'get_http_response_code'
    >>> camel_to_snake('get2HTTPResponseCode')
    'get2_http_response_code'
    >>> camel_to_snake('HTTPResponseCode')
    'http_response_code'
    >>> camel_to_snake('HTTPResponseCodeXYZ')
    'http_response_code_xyz'

    """
    _str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str(camel_str))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', _str).lower()


@typechecked
def transform_dict(
        dct: Dict[Any, Any],
        key_fun: Optional[TransformDictFun] = None,
        val_fun: Optional[TransformDictFun] = None
) -> Dict[Any, Any]:
    """
    Transforms keys and/or values of the given dictionary by applying the given functions.

    Args:
        dct: The dictionary to transform.
        key_fun: The function to apply to all dictionary keys. If not passed the keys will be unaltered.
        val_fun: The function to apply to all dictionary values. If not passed the values will be unaltered.

    Return:
        Returns a new dictionary by applying the key and/or value function to the given dictionary.
        If both transformation functions are not supplied the passed dictionary will be returned unaltered.

    Examples:
        >>> dct = {"CamelCase": "gnaaa", "foo_oool": 42}
        >>> (transform_dict(dct, key_fun=camel_to_snake) ==
        ...     {"camel_case": "gnaaa", "foo_oool": 42})
        True

        >>> transform_dict(dct, val_fun=str) == {"CamelCase": "gnaaa", "foo_oool": "42"}
        True

        >>> (transform_dict(dct, key_fun=camel_to_snake, val_fun=str) ==
        ...     {"camel_case": "gnaaa", "foo_oool": "42"})
        True

        >>> res = transform_dict(dct, None, None)
        >>> print(res)
        {'CamelCase': 'gnaaa', 'foo_oool': 42}
        >>> res is dct
        True
    """
    if not key_fun and not val_fun:
        return dct

    def apply(kov: Any, fun: Optional[Callable[[Any], Any]]) -> Any:
        return kov if not fun else fun(kov)

    return {apply(k, key_fun): apply(v, val_fun) for k, v in dct.items()}
