"""Fail closed on declared workflow and testing crate structure and packaged paths.

This is a structural preflight, not a certificate of full JSON-LD / profile conformance.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def verify() -> None:
    value = json.loads((ROOT / 'ro-crate-metadata.json').read_text(encoding='utf-8'))
    graph = {i['@id']: i for i in value['@graph']}
    main = graph['./']['mainEntity']['@id']
    assert main == '.github/workflows/life-science-knowledge.yml'
    assert {'File', 'SoftwareSourceCode', 'ComputationalWorkflow'}.issubset(set(graph[main]['@type']))
    assert graph[main]['programmingLanguage']['@id'] in graph
    assert graph['./']['license']['@id'] in graph
    assert graph['#suite']['@type'] == 'TestSuite'
    assert any(x['@id'] == '#gh-test' for x in graph['#suite']['instance'])
    assert graph['#gh-test']['name'] == 'GitHub Actions integration validation'
    assert graph['#gh-test']['runsOn']['@id'] == 'https://w3id.org/ro/terms/test#GithubService'
    assert graph['#gh-test']['url'] == 'https://api.github.com'
    assert graph['#gh-test']['resource'] == 'repos/lostlight530/life-science-ecosystem-lab/actions/workflows/validate.yml'
    github_service = graph['https://w3id.org/ro/terms/test#GithubService']
    assert github_service['@type'] == 'TestService'
    assert github_service['name'] == 'Github Actions'
    assert github_service['url']['@id'] == 'https://github.com'
    for p in graph['./']['hasPart']:
        if not (ROOT / p['@id']).exists():
            raise ValueError('missing declared crate member: ' + p['@id'])
    for param in graph[main]['input'] + graph[main]['output']:
        assert graph[param['@id']]['@type'] == 'FormalParameter'


if __name__ == '__main__':
    verify()
    print('RO-Crate structural preflight OK (not full profile conformance)')
