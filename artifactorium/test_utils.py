import unittest
import tempfile


class BaseTest(unittest.TestCase):

    def setUp(self) -> None:
        self.master_root = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.master_root.cleanup()
