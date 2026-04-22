from pathlib import Path
import shutil

src_root = Path.home() / '.hermes'
repo = Path(__file__).resolve().parent

for name in ['SOUL.md', 'config.yaml', 'memories', 'skills']:
    target = repo / name
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()

shutil.copy2(src_root / 'SOUL.md', repo / 'SOUL.md')
shutil.copy2(src_root / 'config.yaml', repo / 'config.yaml')
shutil.copytree(src_root / 'memories', repo / 'memories')
shutil.copytree(src_root / 'skills', repo / 'skills')
print(f'Synced from {src_root} to {repo}')
