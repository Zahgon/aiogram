import inspect
from collections.abc import Generator
from dataclasses import dataclass
from operator import itemgetter
from typing import Any, NamedTuple, Protocol

from aiogram.utils.dataclass import dataclass_kwargs


class ClassAttrsResolver(Protocol):
    def __call__(self, cls: type) -> Generator[tuple[str, Any], None, None]: ...


def inspect_members_resolver(cls: type) -> Generator[tuple[str, Any], None, None]:
    """
    Inspects and resolves attributes of a given class.

    This function uses the `inspect.getmembers` utility to yield all attributes of
    a provided class. The output is a generator that produces tuples containing
    attribute names and their corresponding values. This function is suitable for
    analyzing class attributes dynamically. However, it guarantees alphabetical
    order of attributes.

    :param cls: The class for which the attributes will be resolved.
    :return: A generator yielding tuples containing attribute names and their values.
    """
    pass


def get_reversed_mro_unique_attrs_resolver(cls: type) -> Generator[tuple[str, Any], None, None]:
    """
    Resolve and yield attributes from the reversed method resolution order (MRO) of a given class.

    This function iterates through the reversed MRO of a class and yields attributes
    that have not yet been encountered. It avoids duplicates by keeping track of
    attribute names that have already been processed.

    :param cls: The class for which the attributes will be resolved.
    :return: A generator yielding tuples containing attribute names and their values.
    """
    pass


class _Position(NamedTuple):
    in_mro: int
    in_class: int


@dataclass(**dataclass_kwargs(slots=True))
class _AttributeContainer:
    position: _Position
    value: Any

    def __lt__(self, other: "_AttributeContainer") -> bool:
        return self.position < other.position


def get_sorted_mro_attrs_resolver(cls: type) -> Generator[tuple[str, Any], None, None]:
    """
    Resolve and yield attributes from the method resolution order (MRO) of a given class.

    Iterates through a class's method resolution order (MRO) and collects its attributes
    along with their respective positions in the MRO and the class hierarchy. This generator
    yields a tuple containing the name of each attribute and its associated value.

    :param cls: The class for which the attributes will be resolved.
    :return: A generator yielding tuples containing attribute names and their values.
    """
    pass
