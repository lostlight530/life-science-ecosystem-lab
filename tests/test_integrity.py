import unittest
from pathlib import Path

from life_science_ecosystem_lab.integrity import build_record_manifest, canonical_json_bytes


class IntegrityTests(unittest.TestCase):
    def test_canonicalization_ignores_key_order(self):
        left = canonical_json_bytes({"b": 2, "a": 1})
        right = canonical_json_bytes({"a": 1, "b": 2})
        self.assertEqual(left, right)

    def test_manifest_is_deterministic(self):
        path = Path(__file__).parent / "fixtures" / "record.json"
        self.assertEqual(build_record_manifest(path), build_record_manifest(path))

    def test_top_level_array_is_rejected(self):
        path = Path(__file__).parent / "fixtures" / "array.json"
        with self.assertRaisesRegex(ValueError, "JSON object"):
            build_record_manifest(path)


if __name__ == "__main__":
    unittest.main()

