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


if __name__ == '__main__':
    unittest.main()
