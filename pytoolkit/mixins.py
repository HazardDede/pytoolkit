"""Contains useful class mixins."""
import logging
from typing import Any

from fastcore.basics import basic_repr

from pytoolkit import classproperty
from pytoolkit.basics import field_mro


class LogMixin:
    """
    Adds a logger property to the class to provide easy access to a configured logging instance to
    use.

    Example:
        >>> class NeedsLogger(LogMixin):
        ...     def do(self, message):
        ...         self.logger.info(message)
        >>> dut = NeedsLogger()
        >>> dut.do('Instance logging')
        >>> NeedsLogger.logger.info("Class logging")
    """
    @classproperty
    def logger(cls: Any) -> logging.Logger:  # pylint: disable=no-self-argument
        """
        Configures and returns a logger instance for further use.

        Returns:
            (logging.Logger): The logging instance to use for this class / instance.
        """
        component = "{}.{}".format(cls.__module__, cls.__name__)  # pylint: disable=no-member
        return logging.getLogger(component)


class ReprMixin:
    """Adds a `__repr__` and a `__str__` method to the instance. You can control the fields to show
    via the `__REPR_FIELDS__` class field.

    Examples:

        >>> class A(ReprMixin):
        ...     __REPR_FIELDS__ = ['a']
        ...     def __init__(self):
        ...         self.a = 13

        >>> class B(A):
        ...     __REPR_FIELDS__ = 'b'
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.b = 42

        >>> repr(A())
        'A(a=13)'
        >>> repr(B())
        'B(a=13, b=42)'
        >>> repr(B()) == str(B())
        True
    """
    def __repr__(self) -> str:
        repr_fields = sorted(list(field_mro(self.__class__, '__REPR_FIELDS__')))
        res = basic_repr(repr_fields)(self)
        assert isinstance(res, str)
        return res

    def __str__(self) -> str:
        return repr(self)
