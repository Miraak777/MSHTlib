from inspect import getsourcelines
from typing import Any

from .exceptions import PredicateError


class Predicates:
    """Class for handling predicates"""

    def __call__(self, *args, **kwargs) -> bool:
        """
        Run all predicates.
        Raises `PredicateError` if `hard` predicates failed
        and returns bool: `soft` predicates passes
        """
        self.hard(*args, **kwargs)
        try:
            self.soft(*args, **kwargs)
        except PredicateError:
            return False
        return True

    def __repr__(self) -> str:
        hard, soft = ("".join(getsourcelines(method)[0]) for method in (self.hard, self.soft))
        return f"Predicates({hard=}, {soft=})"

    def hard(self, *args, **kwargs) -> None:
        """Required predicates that must stop pipeline if something's wrong"""

    def soft(self, *args, **kwargs) -> None:
        """Predicates that stop only one component of pipeline"""

    class Condition:
        def __init__(self, result: bool, description: str = "Condition predicate failed") -> None:
            """
            Any condition that accepts bool and raises `PredicateError` if it's `False`

            >>> self.condition(isinstance(value, int))
            >>> self.condition(value > 0)
            """
            if not result:
                raise PredicateError(description)

        @staticmethod
        def isinstance(input: Any, expected: Any) -> None:
            if not isinstance(input, expected):
                raise PredicateError(f"Expected {expected}, got {input}")
