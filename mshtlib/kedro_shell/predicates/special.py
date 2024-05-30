from abc import ABC, abstractmethod
from typing import Any, Optional

from mshtlib.kedro_shell.predicates.exceptions import PredicateError


class SpecialPredicate(ABC):
    """Base predicate class with description in constructor and raise method"""

    def __init__(self, description: str) -> None:
        self.description = f"{self.__class__.__name__} failed" if description is None else description

    @abstractmethod
    def __call__(self, *args, **kwargs) -> None:
        """Predicate body"""

    def raise_(self) -> None:
        """Predicate failed"""
        raise PredicateError(self.description)


class ChanceConditionPredicate(SpecialPredicate):
    """
    Condition predicate that skips the first failure

    >>> self.chance_condition_predicate = ChanceConditionPredicate()
    >>> self.chance_condition_predicate(True)   # run
    >>> self.chance_condition_predicate(False)  # run
    >>> self.chance_condition_predicate(False)  # ___
    """

    def __init__(self, description: Optional[str] = None, state: bool = False) -> None:
        super().__init__(description)
        self.state = state

    def __call__(self, result: bool) -> None:
        if result:
            self.state = True
            return
        if self.state:
            self.state = False
            return
        self.raise_()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(state={repr(self.state)})"


class CounterPredicate(SpecialPredicate):
    """
    Predicate that runs every `total` times.

    >>> CounterPredicate(0)  # run run run run run
    >>> CounterPredicate(1)  # run ___ run ___ run
    >>> CounterPredicate(2)  # run ___ ___ run ___
    """

    def __init__(self, total: int, description: Optional[str] = None, counter: int = 0) -> None:
        super().__init__(description)
        self.total = total
        self.counter = counter

    def __call__(self) -> None:
        if self.counter:
            self.counter -= 1
            self.raise_()
        self.counter = self.total

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(total={repr(self.total)}, counter={repr(self.counter)})"


class StatePredicate(SpecialPredicate):
    """
    Predicate that can be set

    >>> self.state_predicate = StatePredicate()
    >>> self.state_predicate()  # run
    >>> self.state_predicate.state = False  # Change state
    >>> self.state_predicate()  # ___
    """

    def __init__(self, description: Optional[str] = None, state: bool = True) -> None:
        super().__init__(description)
        self.state = state

    def __call__(self) -> None:
        if not self.state:
            self.raise_()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(state={repr(self.state)})"


class ValueChangePredicate(SpecialPredicate):
    """
    Predicate that confirms changing of data

    >>> self.value_change_predicate = ValueChangePredicate(None)
    >>> self.value_change_predicate(1)  # run
    >>> self.value_change_predicate(2)  # run
    >>> self.value_change_predicate(2)  # ___
    >>> self.value_change_predicate(3)  # run
    """

    def __init__(self, first_value: Any, description: Optional[str] = None) -> None:
        super().__init__(description)
        self.value = first_value

    def __call__(self, new_value: Any) -> None:
        if self.value == new_value:
            self.raise_()
        self.value = new_value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"
