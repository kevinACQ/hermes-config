---
name: claude-code-project-hub
description: Create and maintain Kevin's Hermes-accessible Claude Code project hub by symlinking local ~/projects repos into ~/.hermes/workspace/claude-code-projects, with auto-refresh, tests, cron, and config backup.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude-code, hermes, project-discovery, symlinks, cron, backup]
    related_skills: [hermes-agent, claude-code]
---

# Claude Code Project Hub

Use this when Kevin wants Hermes to access, refresh, repair, or extend the shared local hub of Claude Code projects.

## Goal

Give Hermes one stable folder for discovering Kevin's local Claude Code projects without copying files or depending on GitHub sync.

Canonical hub:

```bash
~/.hermes/workspace/claude-code-projects
```

Real repos usually live in:

```bash
~/projects
```

## Current Installed Setup

- Refresh script: `~/.hermes/scripts/refresh_claude_code_projects.py`
- Tests: `~/.hermes/scripts/tests/test_refresh_claude_code_projects.py`
- Hub docs: `~/.hermes/workspace/claude-code-projects/PROJECTS.md`
- Cron job: `Refresh Claude Code project hub`, hourly, local-only delivery
- Backup repo: `~/.hermes/external-repos/hermes-config`
- Backup repo includes `scripts/` so the refresh script survives rollback/rebuild.

## Workflow

1. Inspect current hub state:

```bash
for p in ~/.hermes/workspace/claude-code-projects/*; do
  [ -e "$p" ] && printf '%s -> %s\n' "$p" "$(readlink "$p" 2>/dev/null || printf file)"
done
```

2. Run tests before changing the refresh script:

```bash
python3 ~/.hermes/scripts/tests/test_refresh_claude_code_projects.py
```

If `pytest` is unavailable, use stdlib `unittest` as this setup does.

3. Refresh the hub:

```bash
python3 ~/.hermes/scripts/refresh_claude_code_projects.py
```

Expected output shape:

```text
Refreshed Claude Code project hub: N projects, X links added/updated, Y stale links removed.
```

4. Verify `PROJECTS.md`:

```bash
sed -n '1,120p' ~/.hermes/workspace/claude-code-projects/PROJECTS.md
```

5. Verify cron exists:

Use the `cronjob` tool with `action='list'` and look for `Refresh Claude Code project hub`.

6. Back up durable changes:

```bash
cd ~/.hermes/external-repos/hermes-config
python3 sync_from_hermes.py
python3 auto_backup.py
```

## Implementation Pattern

The refresh script should:

- Scan only `~/projects` for direct child directories containing `.git`.
- Create symlinks in the hub named after each repo.
- Regenerate `PROJECTS.md` with branch and origin info.
- Remove stale symlinks only.
- Never delete real files or real directories in the hub.
- Preserve `HERMES.md` and `PROJECTS.md`.

## Important Pitfalls Learned

- Do not rely on `pytest`; Kevin's macOS Python may not have it. Use stdlib `unittest` for this small script.
- Python on the machine may be older, so avoid `str | None`; use `Optional[str]` for compatibility.
- macOS temp paths may resolve through `/private/var`; compare resolved paths on both sides in tests.
- Cron script paths must be relative to `~/.hermes/scripts/`, e.g. `refresh_claude_code_projects.py`, not absolute paths.
- When backing up, ensure `sync_from_hermes.py` includes `scripts`; otherwise the refresh script is not protected by GitHub backup.

## Verification Checklist

Before saying done:

- [ ] Tests pass: `python3 ~/.hermes/scripts/tests/test_refresh_claude_code_projects.py`
- [ ] Refresh command succeeds.
- [ ] `PROJECTS.md` lists expected repos.
- [ ] Cron job is scheduled and enabled.
- [ ] `hermes-config` backup is committed and pushed if durable files changed.
