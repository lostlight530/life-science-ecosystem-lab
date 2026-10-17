"""Bounded, offline regression tests for protein prediction field-case contracts."""
import importlib.util
import json
import unittest
from pathlib import Path
from evidence.agent_handoff import validate_agent_handoff
from evidence.profiles import load_source_registry, load_topic_registry

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evidence" / "profiles" / "research" / "protein_structure"
spec = importlib.util.spec_from_file_location("protein_demo_audit", ROOT / ".github" / "scripts" / "protein_structure_sample_audit.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ProteinFieldTests(unittest.TestCase):
    def test_pinned_inputs_not_bulk_weights(self):
        manifest = json.loads((PROFILE / "sample-manifest.json").read_text())
        self.assertEqual(len(manifest["samples"]), 7)
        for s in manifest["samples"]:
            self.assertRegex(s["commit"], r"^[0-9a-f]{40}$")
            self.assertRegex(s["blob_sha"], r"^[0-9a-f]{40}$")
            self.assertLessEqual(s["bytes"], mod.MAX_BYTES)
            self.assertNotIn("weights", s["path"].lower())
        self.assertEqual({s["format"] for s in manifest["samples"]}, {"PDB", "FASTA", "JSON"})

    def test_agent_proposal_known_scoped_native_topics(self):
        t = load_topic_registry(PROFILE / "topics.json")
        s = load_source_registry(PROFILE / "sources.json")
        handoff = json.loads((ROOT / ".github" / "agent-handoff" / "protein-structure-2026-10-17.json").read_text())
        self.assertEqual(validate_agent_handoff(handoff, known_topics={x["id"] for x in t.topics}).errors, ())
        self.assertEqual(handoff["authority"], "PROPOSAL_ONLY")
        self.assertEqual(len(s.sources), 6)
        for item in s.sources:
            self.assertRegex(item["ref"], r"^[0-9a-f]{40}$")
        current = load_topic_registry(ROOT / "evidence" / "profiles" / "topics.json")
        self.assertTrue({x["id"] for x in current.topics}.isdisjoint({x["id"] for x in t.topics}))

    def test_bounded_parsers(self):
        self.assertEqual(mod.parse_sample(b">example\nMSTNPKPQR\n", "FASTA")["sequence_length"], 9)
        with self.assertRaises(ValueError):
            mod.parse_sample(b"invalid", "PDB")
        self.assertEqual(mod.parse_sample(b'{"sequences":[{"protein":{"id":"A","sequence":"MAGG"}}]}', "JSON")["sequence_lengths"], [4])

    def test_readonly_separation(self):
        text = (ROOT / ".github" / "workflows" / "protein-structure-agent-demo.yml").read_text()
        self.assertIn("contents: read", text)
        self.assertNotIn("contents: write", text)
        self.assertNotIn("git push", text)
        self.assertIn("build/protein/simulated", text)
        self.assertIn("ls-evidence validate-handoff", text)
        self.assertIn("NO_MEANINGFUL_DELTA", (ROOT / ".github" / "scripts" / "protein_structure_demo_summary.py").read_text())


if __name__ == "__main__":
    unittest.main()
