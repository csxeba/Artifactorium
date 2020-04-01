import pathlib
import unittest

from artifactorium import test_utils
from artifactorium import Artifactorium


class TestInitializations(test_utils.BaseTest):

    def test_initialization_is_actually_lazy(self):
        Artifactorium(self.master_root.name, "artifactory")
        target = pathlib.Path(self.master_root.name) / "artifactory"
        self.assertFalse(target.exists())

    def test_lazy_root_creation_works_on_retrieval(self):
        a = Artifactorium(self.master_root.name, "artifactory")
        root = a.root  # accessing the property causes the creation of the directory
        self.assertTrue(root.exists())

    def test_setting_overwritable_flag_on_initialization(self):
        a = Artifactorium(self.master_root.name, "artifactory", allow_reset_properties=True)
        self.assertTrue(a._allow_reset_properties)

    def test_setting_string_retrieval_flag_on_initialization(self):
        a = Artifactorium(self.master_root.name, "artifactory", return_paths_as_string=True)
        self.assertTrue(a._return_paths_as_string)


if __name__ == '__main__':
    unittest.main()
