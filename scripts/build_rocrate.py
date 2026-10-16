"""Reproducibly package an attached Workflow Testing RO-Crate for inspection.

Only relative tracked paths declared in the root metadata are packaged.
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    'ro-crate-metadata.json', 'README.md', 'LICENSE', 'CITATION.cff', 'workflow/README.md', 'workflow/main.cwl',
    'workflow/tools/aggregate.cwl', 'workflow/tools/validate.cwl',
    'workflow/tools/knowledge.cwl', 'workflow/tools/verify-knowledge.cwl',
    'test/workflow-job.yml', 'examples/evidence-records.json', 'profiles/topics.json',
]


def build(path: Path) -> None:
    metadata = json.loads((ROOT / FILES[0]).read_text(encoding='utf-8'))
    graph = metadata['@graph']
    root = next(x for x in graph if x['@id'] == './')
    ids = {x['@id'] for x in graph}
    if root['mainEntity']['@id'] not in ids:
        raise ValueError('main workflow missing from metadata')
    sources = [p for p in sorted((ROOT / 'src').rglob('*.py')) if p.is_file()]
    if not sources:
        raise ValueError('missing Python tool sources')
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in FILES + [p.relative_to(ROOT).as_posix() for p in sources]:
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, (ROOT / rel).read_bytes())


if __name__ == '__main__':
    build(Path(sys.argv[1] if len(sys.argv) > 1 else 'build/life-science-evidence.crate.zip'))
