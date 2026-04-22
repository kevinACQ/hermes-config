#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

repo = Path(__file__).resolve().parent
sync_script = repo / 'sync_from_hermes.py'


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, cwd=repo, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout.strip()


run(['python3', str(sync_script)])
run(['git', 'add', '.'])
status = run(['git', 'status', '--porcelain'])
if not status:
    print('No changes to back up.')
    raise SystemExit(0)

ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
run(['git', 'commit', '-m', f'chore: Hermes auto backup {ts}'])
run(['git', 'push', 'origin', 'main'])
print('Backup committed and pushed.')
