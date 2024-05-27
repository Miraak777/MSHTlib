from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineLevelConst:
    RUNNER: str = "runner"
    DATA_CATALOG: str = "data_catalog"
    PIPELINE: str = "pipeline"


@dataclass(frozen=True)
class ComponentLevelConst:
    INIT: str = "init"
    RUN: str = "run"


@dataclass(frozen=True)
class InitConst:
    CLS: str = "cls"
    PARAMS: str = "params"


@dataclass(frozen=True)
class RunConst:
    FUNC: str = "func"
    INPUTS: str = "inputs"
    OUTPUTS: str = "outputs"
    NAME: str = "name"
    TAGS: str = "tags"
    CONFIRMS: str = "confirms"
    NAMESPACE: str = "namespace"
