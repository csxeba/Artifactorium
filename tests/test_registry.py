import pathlib
import unittest

from artifactorium import test_utils
from artifactorium import Artifactorium


class TestLazyEvaluation(test_utils.BaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.artifactorium = Artifactorium(self.master_root.name, "testing")

    def _run_check(self, artifactorium: Artifactorium, **targets):
        root = pathlib.Path(self.master_root.name).absolute()
        targets = {prop: root / "testing" / path for prop, path in targets.items()}

        for propname, target in targets.items():
            self.assertEqual(artifactorium._registry[propname], target)  # check path is stored correctly

        for target in targets.values():
            self.assertFalse(target.exists())

        for propname, target in targets.items():
            self.assertEqual(artifactorium[propname], target)

    def test_registering_with_the_register_function(self):
        self.artifactorium.register_path("test_dir1", "test_dir1")
        self.artifactorium.register_path("test_dir2", "test_dir2")
        self._run_check(self.artifactorium, test_dir1="test_dir1", test_dir2="test_dir2")
        self.assertTrue(self.artifactorium.test_dir1.exists())
        self.assertTrue(self.artifactorium.test_dir2.exists())

    def test_registering_with_the_simple_register_form(self):
        self.artifactorium.register_path("test_dir1")
        self.artifactorium.register_path("test_dir2")
        self._run_check(self.artifactorium, test_dir1="test_dir1", test_dir2="test_dir2")
        self.assertTrue(self.artifactorium.test_dir1.exists())
        self.assertTrue(self.artifactorium.test_dir2.exists())

    def test_registering_files(self):
        self.artifactorium.register_path("test_file1", "test_file1.txt", is_file=True)
        self.artifactorium.register_path("test_file2", "test_file2.txt", is_file=True)
        self._run_check(self.artifactorium,
                        test_file1="test_file1.txt",
                        test_file2="test_file2.txt")
        self.assertFalse(self.artifactorium.test_file1.exists())
        self.assertFalse(self.artifactorium.test_file2.exists())
        self.assertTrue(self.artifactorium.test_file1.parent.exists())
        self.assertTrue(self.artifactorium.test_file2.parent.exists())


if __name__ == '__main__':
    unittest.main()
