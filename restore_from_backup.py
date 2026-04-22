#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

repo = Path(__file__).resolve().parent
hermes_home = Path.home() / '.hermes'
backup_root = hermes_home / 'backups' / 'restore'
include = ['SOUL.md', 'config.yaml', 'memories', 'skills']


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, cwd=repo, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout.strip()


if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 restore_from_backup.py <commit-ish>')

commitish = sys.argv[1]
run(['git', 'fetch', 'origin'])
run(['git', 'rev-parse', '--verify', commitish])

ts = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_dir = backup_root / ts
backup_dir.mkdir(parents=True, exist_ok=True)

for name in include:
    live = hermes_home / name
    bak = backup_dir / name
    if live.exists():
        if live.is_dir():
            shutil.copytree(live, bak)
        else:
            bak.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(live, bak)

for name in include:
    live = hermes_home / name
    if live.is_dir():
        shutil.rmtree(live)
    elif live.exists():
        live.unlink()

for name in include:
    src = repo / name
    subprocess.run(['git', 'checkout', commitish, '--', name], cwd=repo, check=True)
    if src.is_dir():
        shutil.copytree(src, hermes_home / name)
    else:
        shutil.copy2(src, hermes_home / name)

# Return backup repo working tree to HEAD so restore does not leave it dirty.
subprocess.run(['git', 'restore', '--source=HEAD', '--', *include], cwd=repo, check=True)

print(f'Restored {commitish} into {hermes_home}')
print(f'Live files backed up to {backup_dir}')
