"""Public release preflight, deliberately checks paths and high-risk credential shapes.

Not a secret-scanning service or guarantee that a public commit contains no sensitive text.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DISALLOWED = (
    'docs/superpowers/', 'docs/archive/', '.superpowers/', '.env',
    '.github/private/', 'private/', 'internal/', 'secrets/',
)
# Patterns are narrow to avoid rejecting ordinary standards documentation
HIGH_RISK = (
    re.compile(r'gh[pousr]_[A-Za-z0-9_]{24,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{24,}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'(?i)(?:api[_-]?key|secret[_-]?token|access[_-]?token)\s*[:=]\s*[\"\']?(?:sk-|ghp_|github_pat_)[a-z0-9_-]{16,}'),
)


def verify(paths: list[str] | None = None) -> None:
    if paths is None:
        paths = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines()
    problems = []
    for rel in sorted(set(paths)):
        name = rel.replace('\\', '/')
        if name.startswith(DISALLOWED) or '/.env' in name or name.endswith(('.pem', '.key', '.p12')):
            problems.append('DISALLOWED_PUBLIC_PATH: ' + name)
            continue
        p = ROOT / name
        if not p.is_file() or p.stat().st_size > 1_000_000:
            continue
        if b'\x00' in p.read_bytes()[:2048]:
            continue
        try:
            content = p.read_text(encoding='utf-8')
        except UnicodeError:
            continue
        if any(expr.search(content) for expr in HIGH_RISK):
            problems.append('POSSIBLE_SECRET_IN_PUBLIC_FILE: ' + name)
    if problems:
        raise SystemExit('\n'.join(problems))


if __name__ == '__main__':
    verify()
    print('PUBLICATION_BOUNDARY_PREFLIGHT_OK (not a complete secret scan)')
