from mshtlib.const import PROJECT_DIR
from pathlib import Path
from shutil import copytree, copy


def create_component():
    copytree(PROJECT_DIR.joinpath("architecture", "component_template", "component"), Path("src").joinpath("components", "component_template"))
    copy(PROJECT_DIR.joinpath("architecture", "component_template", "test_example_component.py"), Path("tests").joinpath("components"))
    with open(Path("src").joinpath("components", "__init__.py"), "a") as file:
        file.write("from src.components.components_template.component import ComponentExample\n")