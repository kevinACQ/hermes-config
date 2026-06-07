# Claude Code Skills → Hermes Mirror Recipe

## Context

This reference captures a durable migration pattern discovered while making Kevin's Claude Code skill library available to Hermes.

Goal: Hermes should use the same skills from Claude Code exactly as designed, without copying files or creating drift.

## Known Paths from the Session

- Claude Code skill source: `/Users/kevin/.claude/skills`
- Hermes local skills: `/Users/kevin/.hermes/skills`
- Recommended mirror: `/Users/kevin/.hermes/external-repos/claude-code-skills`
- Hermes config file: `/Users/kevin/.hermes/config.yaml`
- Config key: `skills.external_dirs`

Existing shared knowledge-base symlinks may exist separately:

```text
/Users/kevin/.claude/knowledgebase -> /Users/kevin/projects/cog-config/knowledge-base
/Users/kevin/.hermes/knowledgebase -> /Users/kevin/projects/cog-config/knowledge-base
```

Do not treat those as evidence that skills are already shared.

## Practical Selection Policy

For Claude Code libraries, link:

1. Immediate child directories of `~/.claude/skills` that contain `SKILL.md`.
2. Immediate child directories of `~/.claude/skills/gstack` that contain `SKILL.md`, when gstack is part of the user's active workflow.
3. Optional curated nested packs, such as `~/.claude/skills/gstack/openclaw/skills/*`, only when they are clearly user-facing.

Skip by default:

- `.git`, `.github`, `.venv`, `venv`, `node_modules`, `site-packages`, caches
- hidden generated multi-agent variants like `.cursor`, `.opencode`, `.agents`, `.factory`, `.kiro`, `.hermes`, unless explicitly requested
- archived folders unless the user asks for archived skills too
- duplicate skill names that would collide with Hermes or another selected source skill

## Collision Examples from This Session

Existing Hermes conflicts:

- `codex`
- `humanizer`

Claude/gstack duplicate-name examples:

- `autoplan`
- `context-restore`
- `context-save`
- `design-consultation`
- `guard`
- `investigate`
- `make-pdf`
- `office-hours`
- `open-gstack-browser`
- `plan-ceo-review`

Policy used: expose the top-level/user-facing source or existing Hermes skill, skip generated/internal duplicates, and record all skips in the manifest.

## Minimal Implementation Shape

Create symlinks rather than copies:

```python
from pathlib import Path

src = Path.home() / '.claude' / 'skills'
dst = Path.home() / '.hermes' / 'external-repos' / 'claude-code-skills'
dst.mkdir(parents=True, exist_ok=True)

for skill_dir in src.iterdir():
    if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
        link = dst / skill_dir.name
        if not link.exists():
            link.symlink_to(skill_dir, target_is_directory=True)
```

The production version should add duplicate detection, excluded-dir filtering, and manifest writing before updating config.

## Config Update Shape

Preserve existing config and append the mirror path:

```yaml
skills:
  external_dirs:
    - /Users/kevin/.hermes/external-repos/claude-code-skills
```

Do not overwrite unrelated `skills:` keys such as `disabled`, `template_vars`, or shell preprocessing settings.

## Verification Commands

After updating config, verify from a fresh session or via explicit tools:

```bash
hermes skills list | grep -E 'prototype-first|skool-api|office-hours'
```

Representative skill loads:

- `skill_view("prototype-first")`
- `skill_view("skool-api")`
- `skill_view("office-hours")`

Use at least one simple skill and one skill with supporting scripts/references.

## Backup Note

If the user has a GitHub-backed Hermes config backup repo, sync and commit the config change after verification. The valuable durable artifact is the config pointing to the mirror; the symlink mirror itself can be recreated from the source library and manifest pattern.
