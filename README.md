# Hermes Config Backup

Git-backed backup of selected Hermes identity/config artifacts.

Included
- SOUL.md
- config.yaml
- memories/
- skills/

Excluded
- secrets (.env, auth.json)
- runtime/session state
- logs and caches

Manual sync
```bash
cd ~/.hermes/external-repos/hermes-config
python3 sync_from_hermes.py
python3 auto_backup.py
```

Rollback
```bash
cd ~/.hermes/external-repos/hermes-config
python3 restore_from_backup.py <commit-ish>
```

Notes
- `auto_backup.py` syncs from `~/.hermes`, commits only if something changed, and pushes to `origin/main`.
- `restore_from_backup.py` restores `SOUL.md`, `config.yaml`, `memories/`, and `skills/` from any git commit while first backing up the current live files under `~/.hermes/backups/restore/`.
