"""Contract preflight for LS workflow/tool publication metadata (not external certification)."""
from __future__ import annotations
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def verify() -> None:
    project=(ROOT/'pyproject.toml').read_text(encoding='utf-8')
    cff=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
    release=re.search(r'(?m)^version\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"$',project)
    assert release, 'missing pyproject semver'
    version=release.group(1)
    assert f'version: {version}' in cff, 'CFF version mismatch'
    assert 'orcid.org/0009-0001-3617-0832' in cff, 'CFF ORCID missing'
    for name,expected_type in [('bioschemas-workflow.jsonld','ComputationalWorkflow'),('bioschemas-tool.jsonld','SoftwareApplication')]:
        doc=json.loads((ROOT/'metadata'/name).read_text(encoding='utf-8'))
        assert doc['@type']==expected_type, name
        assert doc['version']==version, f'{name} version mismatch'
        assert doc['license'].endswith('/MIT'), name
        assert doc['dct:conformsTo'].startswith('https://bioschemas.org/profiles/'), name
    status=json.loads((ROOT/'metadata/standards-status.json').read_text(encoding='utf-8'))
    assert status['software_version']==version, 'status version mismatch'
    assert status['workflow']=='.github/workflows/life-science-knowledge.yml'
    assert status['tool']=='evidence/cli.py'
    assert not (ROOT/'lifemonitor.yaml').exists(), 'global LifeMonitor defaults should not be overridden'
    assert (ROOT/'LICENSE').is_file()
if __name__=='__main__':
    verify();print('LIFE_SCIENCE_METADATA_PREFLIGHT_OK (not external standard certification)')
