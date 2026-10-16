import unittest

from scripts.check_write_boundary import rejected_paths
from scripts.verify_world_line import verify_world_line


class GuardScriptTests(unittest.TestCase):
    def test_rejects_non_data_and_nested_duplicate_roots(self):
        self.assertEqual(rejected_paths(["data/state/a.json"]), [])
        self.assertEqual(rejected_paths(["README.md"]), ["README.md"])
        self.assertEqual(rejected_paths(["data/state/data/state/a.json"]), ["data/state/data/state/a.json"])

    def test_world_line_requires_full_equal_shas(self):
        self.assertTrue(verify_world_line("a" * 40, "a" * 40))
        self.assertFalse(verify_world_line("a" * 40, "b" * 40))
        self.assertFalse(verify_world_line("main", "main"))


if __name__ == "__main__":
    unittest.main()
