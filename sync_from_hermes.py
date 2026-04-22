from pathlib import Path
import shutil

src_root = Path.home() / '.hermes'
repo = Path(__file__).resolve().parent

INCLUDE = ['SOUL.md', 'config.yaml', 'memories', 'skills']
EXCLUDE_NAMES = {'.DS_Store'}
EXCLUDE_SUFFIXES = {'.lock', '.pyc'}
EXCLUDE_DIRS = {'__pycache__'}


def _should_ignore(path: Path) -> bool:
    if path.name in EXCLUDE_NAMES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    return False


def _copy_tree(src: Path, dst: Path) -> None:
    for item in src.rglob('*'):
        rel = item.relative_to(src)
        if _should_ignore(rel):
            continue
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


for name in INCLUDE:
    target = repo / name
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()

for name in INCLUDE:
    src = src_root / name
    dst = repo / name
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        _copy_tree(src, dst)
    else:
        shutil.copy2(src, dst)

print(f'Synced from {src_root} to {repo}')
