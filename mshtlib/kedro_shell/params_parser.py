from collections import Counter
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Type, Union

import yaml
from kedro.pipeline import Pipeline, node, pipeline
from kedro.pipeline.node import Node

from mshtlib.kedro_shell.component_builder import ComponentBuilder
from mshtlib.kedro_shell.const.params import (
    ComponentLevelConst as clc,
    InitConst as ic,
    PipelineLevelConst as plc,
    RunConst as rc
)
from mshtlib.kedro_shell.kedro_mls import AbstractRunner, DataCatalog, DataCatalogBuilder, MemoryDataSet, RunnerBuilder
from mshtlib.kedro_shell.params_validation import ParamsValidation


class ParamsCopyMode:
    def __init__(self) -> None:
        self._params = {rc.INPUTS: [], rc.OUTPUTS: []}
        self._check_map: Dict[Type, Callable] = {
            str: self.add_str,
            list: self.add_list,
            dict: self.add_dict,
        }

    def __call__(self, param: Union[None, str, List[str], Dict[str, str]], tag: str) -> None:
        if param:
            fn = self._check_map.get(type(param))
            if fn:
                return fn(param, tag)
            raise TypeError
        return None

    def add_str(self, param: str, tag: str) -> None:
        if tag in self._params:
            self._params[tag].append(param)

    def add_list(self, params: List[str], tag: str) -> None:
        if tag in self._params:
            self._params[tag] += params

    def add_dict(self, params: Dict[str, str], tag: str) -> None:
        if tag in self._params:
            self._params[tag] += list(params.values())

    @property
    def params(self) -> Dict[str, str]:
        result = {}
        params = Counter(self._params[rc.INPUTS] + self._params[rc.OUTPUTS])
        for name, value in params.items():
            if value == 1 and name in self._params[rc.OUTPUTS]:
                continue
            result[name] = "assign"
        return result


class ParamsParser:
    @classmethod
    def run(
            cls,
            params: Union[Path, List[Dict[str, Union[str, Dict]]]],
            component_builder: Optional[ComponentBuilder] = None,
    ) -> List[Dict[str, Union[AbstractRunner, DataCatalog, Pipeline]]]:
        if isinstance(params, Path):
            return cls.run_yaml(path=params, component_builder=component_builder)
        return cls.run_py(params=params, component_builder=component_builder)

    @classmethod
    def run_py(
            cls,
            params: List[Dict[str, Union[str, Dict]]],
            component_builder: Optional[ComponentBuilder] = None,
    ) -> List[Dict[str, Union[AbstractRunner, DataCatalog, Pipeline]]]:
        return cls._process(params=params, component_builder=component_builder)

    @classmethod
    def run_yaml(
            cls, path: Path, component_builder: Optional[ComponentBuilder] = None
    ) -> List[Dict[str, Union[AbstractRunner, DataCatalog, Pipeline]]]:
        params = cls.read_params(path).values()
        return cls._process(params=params, component_builder=component_builder)

    @classmethod
    def _process(
            cls,
            params: Iterable[Dict[str, Union[str, Dict]]],
            component_builder: Optional[ComponentBuilder] = None,
    ) -> List[Dict[str, Union[AbstractRunner, DataCatalog, Pipeline]]]:
        result = []
        ParamsValidation.run(params)
        for context_item in params:
            params_copy_mode = ParamsCopyMode()
            pipe = cls.create_pipeline(
                context_item[plc.PIPELINE],
                params_copy_mode=params_copy_mode,
                component_builder=component_builder,
            )
            data_catalog = cls.create_data_catalog(context_item=context_item, params_copy_mode=params_copy_mode)
            result.append(
                {
                    plc.RUNNER: RunnerBuilder.create(context_item[plc.RUNNER]),
                    plc.DATA_CATALOG: data_catalog,
                    plc.PIPELINE: pipe,
                }
            )
        return result

    @staticmethod
    def read_params(path: Path) -> Dict[str, Union[str, Dict]]:
        with open(path, "r", encoding="utf8") as stream:
            try:
                params = yaml.safe_load(stream)
                return params
            except yaml.YAMLError as exc:
                raise exc

    @classmethod
    def create_pipeline(
            cls,
            context_pipeline: Dict[str, Dict],
            params_copy_mode: ParamsCopyMode,
            component_builder: Optional[ComponentBuilder] = None,
    ) -> Pipeline:
        result = []
        for comp_name, comp_body in context_pipeline.items():
            result.append(
                cls.create_node(
                    comp_name=comp_name,
                    comp_body=comp_body,
                    comp_builder=component_builder,
                )
            )
            cls._add_io_param_to_copy_mode(params_copy_mode=params_copy_mode, comp_run=comp_body[clc.RUN])
        return pipeline(pipe=result)

    @staticmethod
    def create_node(
            comp_name: str,
            comp_body: Dict[str, Dict[str, Union[str, List[str], Dict[str, str]]]],
            comp_builder: ComponentBuilder,
    ) -> Node:
        comp_init = comp_body[clc.INIT]
        comp_run = comp_body[clc.RUN]
        comp = comp_builder.create(
            component_name=comp_init[ic.CLS],
            component_params=comp_body[clc.INIT].get(ic.PARAMS),
        )
        return node(
            func=comp.__call__,
            inputs=comp_run.get(rc.INPUTS),
            outputs=comp_run.get(rc.OUTPUTS),
            name=comp_name,
            tags=comp_run.get(rc.TAGS),
            confirms=comp_run.get(rc.CONFIRMS),
            namespace=comp_run.get(rc.NAMESPACE),
        )

    @classmethod
    def create_data_catalog(
            cls, context_item: Dict[str, Union[str, Dict]], params_copy_mode: ParamsCopyMode
    ) -> DataCatalog:
        data_catalog = context_item.get(plc.DATA_CATALOG)
        data_catalog = DataCatalogBuilder.create(data_catalog) if data_catalog is not None else DataCatalog()
        for param, copy_mode in params_copy_mode.params.items():
            data_catalog.add(data_set_name=param, data_set=MemoryDataSet(copy_mode=copy_mode))
        return data_catalog

    @staticmethod
    def _add_io_param_to_copy_mode(
            params_copy_mode: ParamsCopyMode,
            comp_run: Dict[str, Union[str, List[str], Dict[str, str]]],
    ) -> ParamsCopyMode:
        params_copy_mode(comp_run.get(rc.INPUTS), tag=rc.INPUTS)
        params_copy_mode(comp_run.get(rc.OUTPUTS), tag=rc.OUTPUTS)
        return params_copy_mode
