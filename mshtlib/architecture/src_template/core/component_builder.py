import inspect
import sys
from typing import Any, Dict, Optional

# pylint: disable=W0401
# pylint: disable=unused-wildcard-import
from mshtlib.kedro_shell.component_builder import Component, ComponentBuilder

from src.components.__init__ import *


def get_component_cls_map():
    result = {}
    for name, obj in inspect.getmembers(sys.modules[__name__], predicate=inspect.isclass):
        if name != Component.__name__ and issubclass(obj, Component):
            result[name] = obj
    return result


class ServiceComponentBuilder(ComponentBuilder):
    subclass_map = get_component_cls_map()

    @classmethod
    def is_component(cls, component_name: str) -> bool:
        return component_name in cls.subclass_map

    @classmethod
    def create(cls, component_name: str, component_params: Dict[str, Any] = None) -> Optional[Component]:
        if not cls.is_component(component_name):
            return None
        component_cls = cls.subclass_map[component_name]
        if component_params is not None:
            return component_cls(**component_params)
        return component_cls()
