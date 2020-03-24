import datetime
import pathlib
from typing import Union


NOW = datetime.datetime.now().strftime("xp_%Y%m%d.%H%M%S")


def build(path: Union[str, pathlib.Path], *subdirectories):
    path = pathlib.Path(path).absolute()
    for subpath in subdirectories:
        if subpath == "NOW":
            subpath = NOW
        if subpath is None:
            continue
        path = path / subpath
    return path
