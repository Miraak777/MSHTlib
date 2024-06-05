from mshtlib.kedro_shell.component import Component

from .predicates import ComponentPredicates


class ComponentExample(Component):
    def __init__(self):
        super().__init__(predicates=ComponentPredicates())

    def run(self):
        pass
