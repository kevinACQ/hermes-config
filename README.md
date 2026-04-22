# Hermes Config Backup

Git-backed backup of selected Hermes identity/config artifacts.

Included:
- SOUL.md
- config.yaml
- memories/
- skills/

Excluded:
- secrets (.env, auth.json)
- runtime/session state
- logs and caches

To refresh this snapshot locally, run:

```bash
python sync_from_hermes.py
```
