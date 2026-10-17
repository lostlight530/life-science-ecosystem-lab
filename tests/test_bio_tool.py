"""Contract, data-quality and boundary tests for independently callable Bio Tool."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from bio_tool.cli import main
from bio_tool.protein import analyze_fasta, analyze_pdb

ROOT = Path(__file__).resolve().parents[1]


def ca(chain: str, res: str, n: int, alt: str = " ") -> str:
    return f"ATOM   {n:4d}   CA{alt}{res:3s} {chain}{n:4d}    {float(n):8.3f}{1.:8.3f}{2.:8.3f}{1.:6.2f}{20.:6.2f}           C\n"


class BioToolTests(unittest.TestCase):
    def test_real_sequence_processing_and_digest_determinism(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.fasta"
            path.write_bytes(b">sample two words\r\nACDE\r\nFGXX\r\n>second\r\nMKLL\r\n")
            a = analyze_fasta(path)
            self.assertEqual(a, analyze_fasta(path))
            self.assertEqual(a["source_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(a["record_count"], 2)
            self.assertEqual(a["residue_count"], 12)
            self.assertEqual(a["records"][0]["counts"]["X"], 2)
            self.assertEqual(a["status"], "WARN_UNCERTAIN_RESIDUES")
            self.assertEqual(a["records"][0]["uncertain_positions"], [7, 8])
            output = Path(temp) / "report.json"
            self.assertEqual(main(["protein-fasta", "--input", str(path), "--output", str(output)]), 0)
            self.assertEqual(json.loads(output.read_text()), a)

    def test_invalid_fasta_rejected_without_output(self):
        for value in ("ACD", ">a\n", ">a\nACD*\n", ">a\nACD\n>a\nPEP\n",
                      ">a\nAC2\n", ">a\nACD\n>b\n"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "bad.fa"
                path.write_text(value)
                target = Path(temp) / "failed.json"
                self.assertEqual(main(["protein-fasta", "--input", str(path), "--output", str(target)]), 2)
                self.assertFalse(target.exists())

    def test_pdb_first_model_ca_counts_and_unknown_residue(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "coordinates.pdb"
            path.write_text("MODEL        1\n" + ca("A", "ALA", 1) + ca("A", "CYS", 2) +
                            ca("B", "MSE", 1) + "ENDMDL\nMODEL        2\n" + ca("A","ALA",3) + "ENDMDL\n")
            report = analyze_pdb(path)
            self.assertEqual(report["observed_ca_count"], 3)
            self.assertEqual(report["chain_count"], 2)
            self.assertEqual(report["chains"][0]["observed_ca_residues"], 2)
            self.assertEqual(report["chains"][1]["nonstandard_residues"], 1)
            self.assertIn("NONSTANDARD_RESIDUE", report["warnings"])
            self.assertEqual(report["model_scope"], "first model only")

    def test_pdb_bad_ca_and_binary_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.pdb"
            path.write_bytes(b"ATOM   1   CA\n")
            with self.assertRaisesRegex(ValueError, "malformed"):
                analyze_pdb(path)
            path.write_bytes(b"\x00binary")
            with self.assertRaisesRegex(ValueError, "binary"):
                analyze_pdb(path)

    def test_standalone_tool_does_not_require_workflow_or_evidence_runtime(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.fa"
            path.write_text(">protein\nACDEFGHIK\n")
            out = Path(temp) / "record.json"
            self.assertEqual(main(["protein-fasta", "--input", str(path), "--output", str(out)]), 0)
            self.assertEqual(json.loads(out.read_text())["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
