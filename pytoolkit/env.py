"""Contains utilities to alter the current environment such as environment variables."""

import contextlib
import os
from typing import Iterator


@contextlib.contextmanager
def modify_environ(*remove: str, **update: str) -> Iterator[None]:
    """
    Temporarily updates the `os.environ` dictionary in-place and resets it to the original state
    when finished.

    The `os.environ` dictionary is updated in-place so that the modification is sure to work in
    most situations.

    Args:
        remove (str): Environment variables to remove from the environment scope.
        update (str): Dictionary of environment variables and values to add if it does not exist or update it's value.

    Examples:
        >>> import os
        >>> os.environ['THIS_IS_SOME_DOCTEST'] = "42"
        >>> print(os.environ['THIS_IS_SOME_DOCTEST'])
        42

        >>> with modify_environ("THIS_IS_SOME_DOCTEST", Test='abc'):
        ...     print(os.environ.get('Test'))
        ...     print(os.environ.get('THIS_IS_SOME_DOCTEST'))
        abc
        None

        >>> print(os.environ.get('Test'))
        None
        >>> print(os.environ.get("THIS_IS_SOME_DOCTEST"))
        42
    """
    env = os.environ
    update = update or {}
    remove = remove or ()

    # List of environment variables being updated or removed.
    stomped = (set(update.keys()) | set(remove)) & set(env.keys())
    # Environment variables and values to restore on exit.
    update_after = {k: env[k] for k in stomped}
    # Environment variables and values to remove on exit.
    remove_after = frozenset(k for k in update if k not in env)

    try:
        env.update(update)
        [env.pop(k, None) for k in remove]  # pylint: disable=expression-not-assigned
        yield
    finally:
        env.update(update_after)
        [env.pop(k) for k in remove_after]  # pylint: disable=expression-not-assigned
