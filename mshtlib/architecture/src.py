from os import mkdir
from pathlib import Path
from shutil import copytree
from mshtlib.const import PROJECT_DIR


def create_src():
    copytree(PROJECT_DIR.joinpath("architecture", "src_template"), "src")
    mkdir(Path("src").joinpath("server", "endpoint_context_params"))
    with Path("src").joinpath("server", "endpoint_context_params").joinpath("template_context_params.yaml").open("w") as file:
        file.write("""
context_item:
  runner: sequential_runner
  pipeline:
    example_component_1:
      init:
        cls: ExampleComponent1
      run:
        inputs: data_name_1
        outputs: data_name_2
    example_component_2:
      init:
        cls: ExampleComponent2
        params: {"example_param": true}
      run:
        inputs: data_name_2
        outputs: data_name_3
        """)
