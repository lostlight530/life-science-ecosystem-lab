"""Real published software artifacts, not empirical scientific validation."""
import copy
import csv
import hashlib
import io
import json
import shlex
import tempfile
import unittest
from pathlib import Path

from ls_framework.engine import assess

ROOT = Path(__file__).resolve().parents[1] / "fixtures/external-transfer"


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def domain_checks(csv_text, command_text):
    # Independent stdlib oracles. These inspect software examples, not specimens.
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    paired = sum(bool(r.get("fastq_2")) for r in rows)
    names = {r["sample"] for r in rows}
    # Duplicate sample names are valid for separate sequencing lanes.
    table_ok = (len(rows) == 7 and len(names) == 6 and paired == 3
                and all(r["fastq_1"].endswith(".fastq.gz") and
                        r["strandedness"] == "forward" for r in rows))
    # Parse only the final command, never execute shell or inference.
    command = command_text[command_text.index("python3 run_pretrained_openfold.py"):]
    args = shlex.split(command.replace("\\\n", " "))
    flags = dict(zip(args[4::2], args[5::2]))
    script_ok = (args[:4] == ["python3", "run_pretrained_openfold.py", "$FASTA_DIR", "$MMCIF_DIR"]
                 and flags.get("--config_preset") == "model_1_ptm"
                 and flags.get("--data_random_seed") == "42"
                 and flags.get("--model_device") == "cuda:0")
    return table_ok, script_ok


class ExternalTransferTests(unittest.TestCase):
    def test_pinned_bytes_and_independent_oracles(self):
        rows = json.loads((ROOT / "sources.json").read_text())["sources"]
        for row in rows:
            self.assertEqual(git_blob((ROOT / row["local"]).read_bytes()), row["blob_sha"])
        csv_text = (ROOT / rows[0]["local"]).read_text()
        command_text = (ROOT / rows[1]["local"]).read_text()
        self.assertEqual(domain_checks(csv_text, command_text), (True, True))
        self.assertEqual(domain_checks(csv_text.replace("forward", "bad", 1), command_text), (False, True))
        self.assertEqual(domain_checks(csv_text, command_text.replace("model_1_ptm", "other")), (True, False))

    def test_contract_transfer_detection_and_abstention(self):
        rows = json.loads((ROOT / "sources.json").read_text())["sources"][:2]
        assets = []
        for row, domain in zip(rows, ("transcriptomics", "structural_biology")):
            assets.append({"id": domain, "domain": domain, "kind": "published-software-example",
                "sha256": hashlib.sha256((ROOT / row["local"]).read_bytes()).hexdigest(),
                "source": {"id": row["repository"] + "/" + row["path"], "version": row["commit"]},
                "path": row["local"]})
        bundle = {"kind": "LS_RSE_INTEROP_BUNDLE", "schema_version": "0.1.0",
                  "scope": "LIFE_SCIENCES", "assets": assets, "steps": [], "claims": []}
        combined = assess(bundle, ROOT)
        self.assertEqual(combined["status"], "FAIL")
        self.assertIn("MISSING_LINEAGE_STEPS", {x["code"] for x in combined["errors"]})
        for asset in assets:
            single = dict(bundle, assets=[asset])
            report = assess(single, ROOT)
            self.assertEqual(report["status"], "PASS", report)
            self.assertEqual(report["metrics"]["local_bytes_verified"], 1)
            self.assertEqual(report["metrics"]["declared_cross_domain_steps"], 0)
        bundle = dict(bundle, assets=[assets[0]])
        cases = []
        wrong = copy.deepcopy(bundle)
        wrong["assets"][0]["sha256"] = "0" * 64
        cases.append((wrong, "FAIL"))
        missing = copy.deepcopy(bundle)
        del missing["assets"][0]["path"]
        cases.append((missing, "INDETERMINATE"))
        claim = copy.deepcopy(bundle)
        claim["claims"] = [{"id": "c", "statement": "unreviewed scientific claim",
                            "evidence": ["transcriptomics"], "authority": "PROPOSAL_ONLY"}]
        cases.append((claim, "INDETERMINATE"))
        for value, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(assess(value, ROOT)["status"], expected)
                self.assertEqual(assess(value, ROOT), assess(value, ROOT))
        # Rehash altered bytes: identity assessment alone cannot replace domain checks.
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp)
            for asset in assets:
                (scratch / asset["path"]).write_bytes((ROOT / asset["path"]).read_bytes())
            p = scratch / assets[0]["path"]
            p.write_bytes(p.read_bytes().replace(b"forward", b"bad", 1))
            self.assertEqual(assess(bundle, scratch)["status"], "FAIL")
            changed = copy.deepcopy(bundle)
            changed["assets"][0]["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
            self.assertEqual(assess(changed, scratch)["status"], "PASS")
            self.assertFalse(domain_checks(p.read_text(), (scratch / assets[1]["path"]).read_text())[0])
