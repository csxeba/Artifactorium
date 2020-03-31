import pickle
import pathlib
from typing import Union
from collections import OrderedDict

from . import path_utils, exception


class Artifactorium:

    """Path manager which stores and builds paths for experiment tracking"""

    __slots__ = "_registry", "_file_flags", "_allow_reset_properties", "_return_paths_as_string", "root"

    def __init__(self,
                 root: Union[str, pathlib.Path],
                 *subdirectories,
                 allow_reset_properties: bool = False,
                 return_paths_as_string: bool = False):

        """
        :param root: str or Path
            Base directoy for logging.
        :param subdirectories: str or Path
            Additional subdirectories, where your actual root will be located.
        :param allow_reset_properties: bool
            Whether to allow resetting a property name. Defaults to False.
        :param return_paths_as_string:
            Whether to return requrested paths as strings or Path objects. Defaults to Path objects (False).
        """

        self._registry: OrderedDict[str, pathlib.Path] = OrderedDict({})
        self._registry["root"] = path_utils.build(root, *subdirectories)
        self._file_flags: OrderedDict[str, bool] = OrderedDict({})
        self._file_flags["root"] = False
        self._allow_reset_properties = allow_reset_properties
        self._return_paths_as_string = return_paths_as_string

    def register_path(self,
                      property_name: str,
                      path: Union[str, pathlib.Path] = None,
                      *subdirectories,
                      is_file: bool = False):

        if property_name == "root":
            raise RuntimeError("The root property cannot be reset, because it contains the Artifactory root.")
        if property_name in self._registry and not self._allow_reset_properties:
            raise exception.PropertyAlreadySetError("Resetting properties is not allowed."
                                                    " Try `allow_reset_paths=True` in the constructor.")
        if path is None:
            path = property_name
        path = path_utils.build(self.root, path, *subdirectories)
        self._registry[property_name] = path
        self._file_flags[property_name] = is_file

    def __getitem__(self, prop: str):
        if prop not in self._registry:
            raise RuntimeError(f"property not in Artifactorium: {prop}")
        path = self._registry[prop]
        if self._file_flags[prop]:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)
        if self._return_paths_as_string:
            path = str(path)
        return path

    def __getattr__(self, prop: str):
        return self.__getitem__(prop)

    def describe(self):
        print(f" [Artifactorium] - Created on {str(path_utils.NOW)}")
        for prop, path in self._registry.items():
            print(f" [Artifactorium] - {prop}: {path}")

    def pickle(self, path: Union[str, pathlib.Path] = None):
        if path is None:
            return pickle.dumps(self._registry)
        with open(str(path), "wb") as handle:
            pickle.dump(self._registry, handle)

    @classmethod
    def unpickle(cls, path: Union[str, pathlib.Path]):
        registry = pickle.load(open(str(path), "rb"))
        obj = cls.from_experiment()
        obj._registry = registry
        return obj
