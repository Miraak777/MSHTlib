from typing import Any, Dict, Optional

from kedro.io import AbstractDataSet, DataCatalog, MemoryDataSet
from kedro.runner import AbstractRunner, ParallelRunner, SequentialRunner, ThreadRunner

from mshtlib.kedro_shell.const.kedro import DataCatalogBuilderConst as dcc, RunnerBuilderConst as rc


class DataCatalogBuilder:
    data_set_map = {
        dcc.MEMORY_DATA_SET: MemoryDataSet,
    }

    def __call__(self, data_catalog_map: str) -> Optional[AbstractDataSet]:
        return self.data_set_map.get(data_catalog_map)

    @classmethod
    def create(cls, data_catalog_params: Optional[Dict[str, Any]] = None) -> Optional[DataCatalog]:
        data_sets = {}
        for dataset_custom_name, dataset_settings in data_catalog_params.items():
            for dataset_name, dataset_params in dataset_settings.items():
                if dataset_name in cls.data_set_map:
                    data_sets[dataset_custom_name] = cls.data_set_map[dataset_name](**dataset_params)
                else:
                    raise KeyError(f"Dataset '{dataset_name}({dataset_params})' not found in catalog dataset map")
        return DataCatalog(data_sets)


class RunnerBuilder:
    runner_map = {
        rc.SEQUENTIAL_RUNNER: SequentialRunner,
        rc.PARALLEL_RUNNER: ParallelRunner,
        rc.THREAD_RUNNER: ThreadRunner,
    }

    def __call__(self, runner_name: str, runner_params: Optional[Dict[str, Any]] = None) -> Optional[AbstractRunner]:
        return self.runner_map.get(runner_name, runner_params)

    @classmethod
    def create(cls, runner_name: str, runner_params: Optional[Dict[str, Any]] = None) -> Optional[AbstractRunner]:
        runner_cls = cls.runner_map.get(runner_name)
        if runner_cls:
            if runner_params:
                return runner_cls(**runner_params)
            return runner_cls()
        return None
