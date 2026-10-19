"""Fail-closed tests for reviewed Knowledge Workflow execution profiles."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from evidence.workflow_profiles import load_profile_registry, resolve_profile, validate_profile_registry


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence" / "profiles" / "workflow-profiles.json"


class WorkflowProfileTests(unittest.TestCase):
    def test_reviewed_native_and_protein_profiles_resolve_with_digests(self):
        registry, registry_digest = load_profile_registry(REGISTRY)
        self.assertEqual(set(registry["profiles"]), {"native", "protein_structure"})
        native = resolve_profile(ROOT, registry, registry_digest, "native")
        protein = resolve_profile(ROOT, registry, registry_digest, "protein_structure")
        self.assertEqual(native["authority"], "PRODUCTION")
        self.assertTrue(native["persistence_allowed"])
        self.assertEqual(protein["authority"], "ISOLATED_RESEARCH")
        self.assertFalse(protein["persistence_allowed"])
        for receipt in (native, protein):
            self.assertRegex(receipt["registry_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(receipt["sources_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(receipt["topics_sha256"], r"^[0-9a-f]{64}$")

    def test_unknown_profile_and_unsafe_paths_fail_closed(self):
        registry, registry_digest = load_profile_registry(REGISTRY)
        with self.assertRaises(ValueError):
            resolve_profile(ROOT, registry, registry_digest, "lipid_unreviewed")
        unsafe = copy.deepcopy(registry)
        unsafe["profiles"]["protein_structure"]["sources"] = "../outside.json"
        with self.assertRaises(ValueError):
            resolve_profile(ROOT, unsafe, registry_digest, "protein_structure")

    def test_registry_rejects_extra_authority_and_persistence_escalation(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        registry["profiles"]["protein_structure"]["persistence_allowed"] = True
        with self.assertRaises(ValueError):
            validate_profile_registry(registry)


if __name__ == "__main__":
    unittest.main()
