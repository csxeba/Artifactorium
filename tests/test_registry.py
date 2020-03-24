import pathlib
import unittest

from artifactorium import test_utils
from artifactorium import Artifactorium


class MyTestCase(test_utils.BaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.artifactorium = Artifactorium(self.master_root.name, "testing")

    def _run_check(self, artifactorium: Artifactorium):
        root = pathlib.Path(self.master_root.name).absolute()
        target_dir1 = root / "testing" / "test_dir1"
        target_dir2 = root / "testing" / "test_dir2"

        self.assertEqual(artifactorium._registry["test_dir1"], target_dir1)  # check path is stored correctly
        self.assertEqual(artifactorium._registry["test_dir2"], target_dir2)

        # check lazy non-creation (direct _registry access should not create dirs)
        self.assertFalse(target_dir1.exists())
        self.assertFalse(target_dir2.exists())

        dir1 = artifactorium.test_dir1
        dir2 = artifactorium.test_dir2

        self.assertTrue(target_dir1.exists())  # check accessing actually creates directories
        self.assertTrue(target_dir2.exists())

        self.assertEqual(dir1, target_dir1)  # check whether path building was correct
        self.assertEqual(dir2, target_dir2)

    def test_registering_during_initialization(self):
        a = Artifactorium(self.master_root.name, "testing",
                          test_dir1="test_dir1",
                          test_dir2="test_dir2")
        self._run_check(artifactorium=a)

    def test_registering_with_the_register_function(self):
        self.artifactorium.register_path("test_dir1", "test_dir1")
        self.artifactorium.register_path("test_dir2", "test_dir2")
        self._run_check(self.artifactorium)

    def test_registering_with_keyword_assignment(self):
        self.artifactorium["test_dir1"] = "test_dir1"
        self.artifactorium["test_dir2"] = "test_dir2"
        self._run_check(self.artifactorium)

    def test_registering_with_property_assignment(self):
        self.artifactorium.test_dir1 = "test_dir1"
        self.artifactorium.test_dir2 = "test_dir2"
        self._run_check(self.artifactorium)

    def test_registering_with_the_simple_register_form(self):
        self.artifactorium.register_path("test_dir1")
        self.artifactorium.register_path("test_dir2")
        self._run_check(self.artifactorium)


if __name__ == '__main__':
    unittest.main()
