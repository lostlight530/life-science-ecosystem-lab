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
    codemeta=json.loads((ROOT/'codemeta.json').read_text(encoding='utf-8'))
    assert codemeta.get('@type')=='SoftwareSourceCode', 'CodeMeta type mismatch'
    assert codemeta.get('softwareVersion')==version, 'CodeMeta version mismatch'
    assert len(codemeta.get('hasPart', []))==3, 'CodeMeta three independently callable assets mismatch'
    assert not (ROOT/'lifemonitor.yaml').exists(), 'global LifeMonitor defaults should not be overridden'
    assert status['bio_tool']=='bio_tool/cli.py', 'bioinformatics tool identity mismatch'
    assert (ROOT/'.lifemonitor.yaml').is_file(), 'LifeMonitor configuration missing'
    bio=json.loads((ROOT/'metadata/bioschemas-bio-tool.jsonld').read_text(encoding='utf-8'))
    assert bio['@type']=='SoftwareApplication' and bio['version']==version, 'Bio Tool descriptor mismatch'
    assert bio['license'].endswith('/MIT'), 'Bio Tool license mismatch'
    draft=json.loads((ROOT/'metadata/biotools-protein-audit.draft.json').read_text(encoding='utf-8'))
    assert draft['name']=='Life Science Protein File Audit', 'bio.tools draft identity mismatch'
    assert draft['version']==version, 'bio.tools draft version mismatch'
    assert {op['uri'] for func in draft['function'] for op in func['operation']} == {
        'http://edamontology.org/operation_2403', 'http://edamontology.org/operation_2406'
    }, 'bio.tools EDAM operations mismatch'
    assert 'biotoolsID' not in draft and 'doi' not in draft, 'bio.tools external IDs cannot be fabricated'
    assert (ROOT/'bio_tool/cli.py').is_file(), 'Bio Tool command missing'
    assert (ROOT/'LICENSE').is_file()
if __name__=='__main__':
    verify();print('LIFE_SCIENCE_METADATA_PREFLIGHT_OK (not external standard certification)')
