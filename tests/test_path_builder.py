import pathlib
import unittest

from artifactorium import path_utils


class TestBuilder(unittest.TestCase):

    def test_builder_builds_correct_paths(self):
        paths = ["root", "subdir1", "subdir2"]
        output = path_utils.build(paths[0], *paths[1:])
        target = pathlib.Path(paths[0]) / paths[1] / paths[2]
        self.assertEqual(output, target.absolute())


if __name__ == '__main__':
    unittest.main()
