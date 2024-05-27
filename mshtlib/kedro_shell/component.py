from abc import ABC, abstractmethod
from typing import Any, Optional

from mshtlib.kedro_shell.predicates import Predicates


class Component(ABC):
    def __init__(self, predicates: Optional[Predicates] = None) -> None:
        self.predicates = predicates if predicates is not None else Predicates()

    def __call__(self, *args, **kwargs) -> Any:
        self.predicates(*args, **kwargs)
        return self.run(*args, **kwargs)

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        pass
