# Life Science Ecosystem Lab

Research Workflow and Data Integrity Pilot

This repository turns proven lifecycle and data-processing patterns into small, testable reference products for Life Science research infrastructure

The pilot begins with two tools:

- **Workflow Integration Profile Validator** checks the immutable identity and registration-readiness metadata of a GitHub-hosted research workflow
- **Research Record Integrity Tool** canonicalizes non-sensitive JSON research records and emits a deterministic SHA-256 manifest

The work commemorates the first workflow generation completed with Jules on 15–16 February 2026, while establishing an independent and deliberately small pilot for future Life Science integration

## Current boundary

This repository currently provides engineering validation, examples, schemas, provenance, and maintenance procedures

It does not claim biological interpretation, clinical validity, sensitive-data authorization, WorkflowHub registration, LifeMonitor enrollment, a published dataset, or a scientific publication

## Quick start

Python 3.11 or newer is sufficient and no runtime dependency is required

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m life_science_ecosystem_lab record-integrity examples/records/input.json --output build/record-manifest.json
PYTHONPATH=src python -m life_science_ecosystem_lab validate-workflow-profile examples/workflow-profile.json
```

On PowerShell, set `$env:PYTHONPATH = "src"` before running the two module commands

## Evidence contract

Every accepted product must have explicit inputs, deterministic output, a versioned schema, test evidence, a bounded write surface, and a recovery identity

See [scope](docs/SCOPE.md) and [provenance policy](docs/PROVENANCE.md)

## Status

`Pilot` — interfaces may evolve before the first stable release

