from typing import Any, Dict, Optional
from .component import Component


class ComponentBuilder:
    @staticmethod
    def _import_error(component_name: str, component_params: Optional[Dict[str, Any]] = None) -> None:
        if component_params:
            component_info = []
            for key, value in component_params.items():
                component_info.append(f"{key}={value}, ")
            component_info = "".join(component_info[:-2])
            raise ImportError(
                f"Component '{component_name}' with params '({component_info})' not found at subclass_map"
            )
        raise ImportError(f"Component '{component_name}' not found at subclass_map")

    @classmethod
    def create(cls, component_name: str, component_params: Dict[str, Any] = None) -> Optional[Component]:
        pass
