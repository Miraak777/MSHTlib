from typing import Dict, Iterable, List, Union

from mshtlib.kedro_shell.const.params import (
    ComponentLevelConst as clc,
    InitConst as ic,
    PipelineLevelConst as plc,
    RunConst as rc
)
from mshtlib.kedro_shell.predicates import Predicates

NoneType = type(None)


class ContextPredicates(Predicates):
    def hard(self, context_item: dict) -> None:
        self.condition(isinstance(context_item, dict))
        self.condition(2 <= len(context_item) <= 4)
        self.condition(plc.RUNNER in context_item and isinstance(context_item[plc.RUNNER], str))
        self.condition(plc.PIPELINE in context_item and isinstance(context_item[plc.PIPELINE], dict))
        self.condition(len(context_item[plc.PIPELINE]) > 0)


class PipelinePredicates(Predicates):
    def hard(self, pipeline_name: str, pipeline_params: dict) -> None:
        self.condition(isinstance(pipeline_name, str) and isinstance(pipeline_params, dict))
        self.condition(len(pipeline_params) == 2 and clc.INIT in pipeline_params and clc.RUN in pipeline_params)
        self.condition(1 <= len(pipeline_params[clc.INIT]) <= 2)
        self.condition(0 <= len(pipeline_params[clc.RUN]) <= 7)


class PipelineInitPredicates(Predicates):
    def hard(self, init_params: dict) -> None:
        self.condition(isinstance(init_params.get(ic.CLS), str))
        self.condition(isinstance(init_params.get(ic.PARAMS), (dict, NoneType)))
        self.condition(all(isinstance(k, str) for k in init_params))


class PipelineRunPredicates(Predicates):
    def hard(self, run_params: dict) -> None:
        self.condition(isinstance(run_params.get(rc.INPUTS), (str, list, dict, NoneType)))
        self.condition(isinstance(run_params.get(rc.OUTPUTS), (str, list, dict, NoneType)))


class ParamsValidation:
    context_predicates = ContextPredicates()
    pipeline_predicates = PipelinePredicates()
    pipeline_init_predicates = PipelineInitPredicates()
    pipeline_run_predicates = PipelineRunPredicates()

    @classmethod
    def run(cls, context_items: Iterable[Dict[str, Union[str, Union[Dict, List]]]]) -> None:
        """Run all predicates for validating `context_items`"""
        for context_item in context_items:
            cls.context_predicates(context_item)
            for pipeline_name, pipeline_params in context_item[plc.PIPELINE].items():
                cls.pipeline_predicates(pipeline_name, pipeline_params)
                cls.pipeline_init_predicates(pipeline_params[clc.INIT])
                cls.pipeline_run_predicates(pipeline_params[clc.RUN])
