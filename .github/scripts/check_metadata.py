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
    workflowhub=status['workflowhub_registration']
    assert workflowhub['workflow_id']==2347 and workflowhub['version']==2, 'WorkflowHub external record mismatch'
    assert workflowhub['workflow_type']=='Common Workflow Language', 'WorkflowHub workflow type mismatch'
    assert workflowhub['doi']=='10.48546/workflowhub.workflow.2347.2', 'WorkflowHub DOI mismatch'
    assert workflowhub['status']=='PUBLICLY_VERIFIED', 'WorkflowHub status mismatch'
    lifemonitor=status['lifemonitor_registration']
    assert lifemonitor['workflow_uuid']=='cc202b33-cd3e-48cc-8004-8e8db87bd200', 'LifeMonitor workflow UUID mismatch'
    assert lifemonitor['origin']=='local file uploaded' and lifemonitor['visibility']=='private', 'LifeMonitor record boundary mismatch'
    assert lifemonitor['evidence_basis']=='MAINTAINER_OBSERVED_AUTHENTICATED_DASHBOARD', 'LifeMonitor evidence basis mismatch'
    assert lifemonitor['suite'] == {
        'uuid': '05f4e427-ebcc-4650-ab97-2348c0788a32',
        'name': 'GitHub Actions automated workflow tests',
        'passing': 1,
        'some_passing': 0,
        'failing': 0,
        'unavailable': 0,
    }, 'LifeMonitor suite status mismatch'
    assert lifemonitor['test_instance']['uuid']=='18d116e5-3806-4103-950a-8b65ab75d7f4', 'LifeMonitor test instance mismatch'
    assert lifemonitor['test_instance']['resource'].endswith('/actions/workflows/validate.yml'), 'LifeMonitor test resource mismatch'
    codemeta=json.loads((ROOT/'codemeta.json').read_text(encoding='utf-8'))
    assert codemeta.get('@type')=='SoftwareSourceCode', 'CodeMeta type mismatch'
    assert codemeta.get('softwareVersion')==version, 'CodeMeta version mismatch'
    parts=codemeta.get('hasPart', [])
    assert len(parts)==4, 'CodeMeta repository component inventory mismatch'
    framework=[part for part in parts if str(part.get('@id', '')).endswith('/framework')]
    assert framework and framework[0].get('version')=='0.1.0', 'Framework CodeMeta identity mismatch'
    assert framework[0].get('developmentStatus')=='experimental', 'Framework maturity boundary mismatch'
    assert '10.5281/zenodo.23447089' in cff, 'released software DOI missing from CFF'
    life_config_path = ROOT/'lifemonitor.yaml'
    assert life_config_path.is_file(), 'LifeMonitor requires the official root-level lifemonitor.yaml'
    assert not (ROOT/'.lifemonitor.yaml').exists(), 'nonstandard .lifemonitor.yaml must not coexist with the official configuration'
    life_config = life_config_path.read_text(encoding='utf-8')
    assert re.search(r'(?m)^name:\s*\S', life_config), 'LifeMonitor repository name missing'
    assert re.search(r'(?m)^issues:[ \t]*\n[ \t]+check:[ \t]*true[ \t]*(?:#.*)?$', life_config), 'LifeMonitor issue checks must be enabled for this repository'
    assert not re.search(r'(?m)^(?:push|public)\s*:', life_config), 'LifeMonitor push and visibility settings must remain governed by account-wide settings'
    assert status['bio_tool']=='bio_tool/cli.py', 'bioinformatics tool identity mismatch'
    bio=json.loads((ROOT/'metadata/bioschemas-bio-tool.jsonld').read_text(encoding='utf-8'))
    assert bio['@type']=='SoftwareApplication' and bio['version']==version, 'Bio Tool descriptor mismatch'
    assert bio['license'].endswith('/MIT'), 'Bio Tool license mismatch'
    draft=json.loads((ROOT/'metadata/biotools-protein-audit.draft.json').read_text(encoding='utf-8'))
    assert draft['name']=='Life Science Protein File Audit', 'bio.tools draft identity mismatch'
    assert draft['version']==version, 'bio.tools draft version mismatch'
    assert {op['uri'] for func in draft['function'] for op in func['operation']} == {
        'http://edamontology.org/operation_2403', 'http://edamontology.org/operation_2406'
    }, 'bio.tools EDAM operations mismatch'
    assert draft['biotoolsID']=='life-science-protein-file-audit', 'bio.tools registered ID mismatch'
    assert draft['biotoolsCURIE']=='biotools:life-science-protein-file-audit', 'bio.tools registered CURIE mismatch'
    assert 'doi' not in draft, 'bio.tools descriptor must not invent a DOI'
    assert status['biotools_registration'] == {
        'biotools_id': 'life-science-protein-file-audit',
        'biotools_curie': 'biotools:life-science-protein-file-audit',
        'record_url': 'https://bio.tools/life-science-protein-file-audit',
        'status': 'EXTERNALLY_OBSERVED',
        'evidence_basis': 'MAINTAINER_OBSERVED_REGISTRY_RECORD',
        'api_verification': 'NOT_INDEPENDENTLY_VERIFIED',
        'curation_status': 'NOT_INDEPENDENTLY_VERIFIED',
    }, 'bio.tools external record boundary mismatch'
    openebench=status['openebench_record']
    assert openebench['tool_id']=='life-science-protein-file-audit', 'OpenEBench tool identity mismatch'
    assert openebench['status']=='MAINTAINER_OBSERVED_ACTIVE_RECORD', 'OpenEBench observation status mismatch'
    assert openebench['upstream_validated']==0, 'OpenEBench validated field must remain source-accurate'
    assert openebench['upstream_confidence_label']=='ultimate', 'OpenEBench source confidence label mismatch'
    assert any('not an OpenEBench scientific benchmark' in item for item in openebench['limitations']), 'OpenEBench benchmark boundary missing'
    assert status['zenodo_release']['doi']=='10.5281/zenodo.23447089', 'Zenodo DOI mismatch'
    assert status['github_release']['source_commit']=='c09d4f3d0a8ebe28970dd511c7ab1e96f2ee0ea6', 'GitHub release source mismatch'
    assert status['framework']=='framework/src/ls_framework/cli.py', 'Framework identity mismatch'
    assert (ROOT/'bio_tool/cli.py').is_file(), 'Bio Tool command missing'
    assert (ROOT/'LICENSE').is_file()
if __name__=='__main__':
    verify();print('LIFE_SCIENCE_METADATA_PREFLIGHT_OK (not external standard certification)')
