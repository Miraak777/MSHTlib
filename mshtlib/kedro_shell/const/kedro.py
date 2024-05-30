from dataclasses import dataclass


@dataclass(frozen=True)
class DataCatalogBuilderConst:
    MEMORY_DATA_SET: str = "memory_data_set"


@dataclass(frozen=True)
class RunnerBuilderConst:
    SEQUENTIAL_RUNNER: str = "sequential_runner"
    PARALLEL_RUNNER: str = "parallel_runner"
    THREAD_RUNNER: str = "thread_runner"
