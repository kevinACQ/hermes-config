---
name: claude-code-skills
description: Use when Kevin asks for a Claude Code skill, slash skill name, or wants Hermes to reuse a workflow from ~/.claude/skills. Token-efficient index only; mirrored Claude skills stay disabled until explicitly loaded.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude-code, skills, mirror, token-efficient]
    related_skills: [hermes-agent]
---

# Claude Code Skills Index

Hermes can read Kevin's Claude Code skills without copying them into Hermes.

## Source of truth

- Claude skills source: `/Users/kevin/.claude/skills`
- Hermes mirror: `/Users/kevin/.hermes/external-repos/claude-code-skills`
- Mirror manifest: `/Users/kevin/.hermes/external-repos/claude-code-skills/MANIFEST.md`
- Refresh script: `/Users/kevin/.hermes/scripts/refresh_claude_skill_mirror.py`

## Token policy

The mirrored Claude skills are intentionally disabled in Hermes config so they do not appear in the always-on skill catalog and burn prompt tokens invisibly.

When Kevin explicitly asks for a Claude skill or names one:

1. Read the mirrored skill file directly:
   - `/Users/kevin/.hermes/external-repos/claude-code-skills/<skill-name>/SKILL.md`
2. Follow it as authoritative workflow context for that task.
3. Do not write to Claude-owned paths unless Kevin explicitly asks.

If native `skill_view("<skill-name>")` behavior is required for one skill, temporarily remove that skill name from `skills.disabled`, reload skills, use it, then disable it again if it should stay out of the always-on catalog.

## Write-boundary policy

Hermes must not write session memory, architecture notes, or lifecycle output into `/Users/kevin/.claude`.

- Do not run Claude memory skills such as `remember-fact`, `state-transfer`, or Claude's original `session-close` inside Hermes.
- Use Hermes-native memory (`memory` tool) or files under `/Users/kevin/.hermes` for Hermes state.
- If a mirrored Claude skill instructs writing to `~/.claude/memory`, reinterpret that as read-only context unless Kevin explicitly asks to edit Claude's memory.

## Maintenance

After adding/removing Claude skills, run:

```bash
python3 /Users/kevin/.hermes/scripts/refresh_claude_skill_mirror.py
```

Then restart Hermes or use `/reload-skills` in a fresh-capable interface.
