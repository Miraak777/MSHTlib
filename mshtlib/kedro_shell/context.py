from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from kedro.io import DataCatalog
from kedro.io.memory_dataset import MemoryDataSet

from mshtlib.kedro_shell.component_builder import ComponentBuilder
from mshtlib.kedro_shell.const.params import PipelineLevelConst as plc
from mshtlib.kedro_shell.params_parser import ParamsParser


class Context:
    def __init__(
        self,
        params: Union[Path, List[Dict[str, Dict]], None],
        component_builder: Optional[ComponentBuilder] = None,
    ) -> None:
        self.params = (
            ParamsParser.run(params=params, component_builder=component_builder) if params is not None else None
        )

    def __call__(self, user_data: Dict[str, Any]) -> Any:
        result = None
        for context_item in self.params:
            catalog = self._get_data_catalog(context_item=context_item, user_data=user_data)
            result = context_item[plc.RUNNER].run(pipeline=context_item[plc.PIPELINE], catalog=catalog)
        return result

    @classmethod
    def run(
        cls,
        params: Union[Path, List[Dict[str, Dict]]],
        user_data: Optional[Dict[str, Any]] = None,
        component_builder: Optional[ComponentBuilder] = None,
    ) -> Any:
        result = None
        for context_item in ParamsParser.run(params=params, component_builder=component_builder):
            result = context_item[plc.RUNNER].run(
                pipeline=context_item[plc.PIPELINE],
                catalog=cls._get_data_catalog(context_item, user_data),
            )
        return result

    @staticmethod
    def _get_data_catalog(context_item: Dict[str, Any], user_data: Optional[Dict[str, Any]] = None) -> DataCatalog:
        data_catalog = context_item[plc.DATA_CATALOG]
        user_data = user_data if user_data is not None else {}
        for key, value in user_data.items():
            data_catalog.add_feed_dict(
                feed_dict={key: MemoryDataSet(data=value, copy_mode="assign")},
                replace=True,
            )
        return data_catalog
