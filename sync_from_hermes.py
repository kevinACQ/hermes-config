#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

repo = Path(__file__).resolve().parent
hermes_home = Path.home() / '.hermes'
include = ['SOUL.md', 'config.yaml', 'memories', 'skills', 'scripts']

for name in include:
    src = hermes_home / name
    dst = repo / name
    if not src.exists():
        continue
    if dst.is_dir() or dst.is_symlink():
        shutil.rmtree(dst)
    elif dst.exists():
        dst.unlink()
    if src.is_dir():
        ignore = shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store')
        shutil.copytree(src, dst, ignore=ignore)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

print('Synced Hermes config artifacts into backup repo.')
