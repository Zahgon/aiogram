import inspect
from collections.abc import Iterator
from typing import Any, no_type_check

from aiogram.types import TelegramObject


class State:
    """
    State object
    """

    def __init__(self, state: str | None = None, group_name: str | None = None) -> None:
        self._state = state
        self._group_name = group_name
        self._group: type[StatesGroup] | None = None

    @property
    def group(self) -> "type[StatesGroup]":
        pass

    @property
    def state(self) -> str | None:
        pass

    def set_parent(self, group: "type[StatesGroup]") -> None:
        pass

    def __set_name__(self, owner: "type[StatesGroup]", name: str) -> None:
        if self._state is None:
            self._state = name
        self.set_parent(owner)

    def __str__(self) -> str:
        return f"<State '{self.state or ''}'>"

    __repr__ = __str__

    def __call__(self, event: TelegramObject, raw_state: str | None = None) -> bool:
        if self.state == "*":
            return True
        return raw_state == self.state

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.state == other.state
        if isinstance(other, str):
            return self.state == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.state)


class StatesGroupMeta(type):
    __parent__: type["StatesGroup"] | None
    __childs__: tuple[type["StatesGroup"], ...]
    __states__: tuple[State, ...]
    __state_names__: tuple[str, ...]
    __all_childs__: tuple[type["StatesGroup"], ...]
    __all_states__: tuple[State, ...]
    __all_states_names__: tuple[str, ...]

    @no_type_check
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)

        states = []
        childs = []

        for arg in namespace.values():
            if isinstance(arg, State):
                states.append(arg)
            elif inspect.isclass(arg) and issubclass(arg, StatesGroup):
                child = cls._prepare_child(arg)
                childs.append(child)

        cls.__parent__ = None
        cls.__childs__ = tuple(childs)
        cls.__states__ = tuple(states)
        cls.__state_names__ = tuple(state.state for state in states)

        cls.__all_childs__ = cls._get_all_childs()
        cls.__all_states__ = cls._get_all_states()

        # In order to ensure performance, we calculate this parameter
        # in advance already during the production of the class.
        # Depending on the relationship, it should be recalculated
        cls.__all_states_names__ = cls._get_all_states_names()

        return cls

    @property
    def __full_group_name__(cls) -> str:
        if cls.__parent__:
            return f"{cls.__parent__.__full_group_name__}.{cls.__name__}"
        return cls.__name__

    def _prepare_child(cls, child: type["StatesGroup"]) -> type["StatesGroup"]:
        """Prepare child.

        While adding `cls` for its children, we also need to recalculate
        the parameter `__all_states_names__` for each child
        `StatesGroup`. Since the child class appears before the
        parent, at the time of adding the parent, the child's
        `__all_states_names__` is already recorded without taking into
        account the name of current parent.
        """
        pass

    def _get_all_childs(cls) -> tuple[type["StatesGroup"], ...]:
        pass

    def _get_all_states(cls) -> tuple[State, ...]:
        pass

    def _get_all_states_names(cls) -> tuple[str, ...]:
        pass

    def __contains__(cls, item: Any) -> bool:
        if isinstance(item, str):
            return item in cls.__all_states_names__
        if isinstance(item, State):
            return item in cls.__all_states__
        if isinstance(item, StatesGroupMeta):
            return item in cls.__all_childs__
        return False

    def __str__(self) -> str:
        return f"<StatesGroup '{self.__full_group_name__}'>"

    def __iter__(self) -> Iterator[State]:
        return iter(self.__all_states__)


class StatesGroup(metaclass=StatesGroupMeta):
    @classmethod
    def get_root(cls) -> type["StatesGroup"]:
        pass

    def __call__(self, event: TelegramObject, raw_state: str | None = None) -> bool:
        return raw_state in type(self).__all_states_names__

    def __str__(self) -> str:
        return f"StatesGroup {type(self).__full_group_name__}"


default_state = State()
any_state = State(state="*")
