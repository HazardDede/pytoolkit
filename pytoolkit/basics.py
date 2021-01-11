"""Includes useful general purpose utility stuff."""

import inspect
from typing import Any, Callable, Type, Optional, cast, Union, Set, Iterable

from pytoolkit.converter import listify

ClassGetterMethod = Callable[[type], Any]


class classproperty:  # pylint: disable=invalid-name
    """
    Make class methods look like read-only class properties.
    Writing to that class-property will not do what you expect ;-)

    If `caching` is set to `True` will only invoke the getter method once and cache the result.
    This makes sense if your property is computed once and after that never changed.

    Examples:
        >>> class Foo:
        ...     _instance = 5
        ...     @classproperty
        ...     def foo(cls):
        ...         return cls._instance
        ...
        ...     @classproperty(caching=True)
        ...     def bar(cls):
        ...         return cls._instance

        >>> Foo.foo, Foo.bar
        (5, 5)
        >>> Foo._instance = 15
        >>> Foo.foo, Foo.bar  # Due to caching Foo.bar still returns 5
        (15, 5)

        >>> Foo.foo = 4242  # Setting the classproperty is not allowed
        >>> Foo.foo, Foo.bar, Foo._instance
        (4242, 5, 15)
    """
    def __init__(self, caching: Union[ClassGetterMethod, bool] = False):
        self.getter: Optional[ClassGetterMethod] = cast(ClassGetterMethod, caching) if callable(caching) else None
        self.caching = False if callable(caching) else bool(caching)
        self.cache: Optional[Any] = None

    def __call__(self, getter: ClassGetterMethod) -> 'classproperty':
        self.getter = getter
        return self

    def __get__(self, instance: Optional[Any], owner: Type[Any]):
        if self.getter is None:  # pragma: no cover
            raise RuntimeError("No method is decorated. Please review your usage of classproperty.")

        if self.caching and self.cache:
            return self.cache
        res = self.getter(owner)
        if self.caching:
            self.cache = res
        return res


def field_mro(clazz: Any, field: str) -> Set[str]:
    """
    Goes up the mro (method resolution order) of the given class / instance and returns the union of values for a given
    class field.

    Args:
        clazz (Any): The class to inspect.
        field (str): The field to collect the values.

    Returns:
        Set[str]: Returns a compiled set of values for the given field for each class in the class hierarchy of the
        passed class or instance.

    Example:

        >>> class Root:
        ...     __myfield__ = 'root'
        >>> class A(Root):
        ...     __myfield__ = ['a', 'common']
        >>> class B(Root):
        ...     __myfield__ = ['b', 'common']
        >>> class Final(A, B):
        ...     __myfield__ = 'final'

        >>> field_mro(Final, '__myfield__') == {'root', 'a', 'b', 'common', 'final'}
        True
        >>> field_mro(A, '__myfield__') == {'root', 'a', 'common'}
        True
        >>> field_mro(Final(), '__myfield__') == {'root', 'a', 'b', 'common', 'final'}
        True
    """
    res = set()  # type: Set[str]
    if not hasattr(clazz, '__mro__'):
        # cls might be an instance. mro is only available on classes
        if not hasattr(type(clazz), '__mro__'):  # pragma: no cover
            # No class, no instance ... Return empty set
            return res
        clazz = type(clazz)

    for parent in inspect.getmro(clazz):
        values_ = getattr(parent, field, None)
        if values_ is not None:
            res = res.union(set(cast(Iterable[str], listify(values_))))

    return res
