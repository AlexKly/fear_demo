import os
import yaml
import pathlib
from typing import Union, Any


def load_config(path: Union[str, pathlib.Path], encoding: str = 'utf-8') -> dict[str, Any]:
    with open(file=path, mode='r', encoding=encoding) as f:
        return yaml.safe_load(stream=f)


def mkdir(path: Union[str, pathlib.Path]) -> None:
    if not os.path.exists(path=path):
        os.makedirs(name=path)
