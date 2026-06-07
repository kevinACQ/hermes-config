---
name: session-close
description: Use when Kevin asks to wrap up, close the session, or run /session-close in Hermes. Summarizes the session and saves only Hermes-owned durable facts; never writes to ~/.claude.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [session-close, memory, hermes-only]
    related_skills: [claude-code-skills]
---

# Hermes Session Close

This is the Hermes-safe replacement for Claude Code's `session-close` skill.

## Hard boundary

Never write to `/Users/kevin/.claude`, `~/.claude/memory`, Claude `CLAUDE.md`, or Claude session trace files from Hermes session close.

Hermes session close may only use:

- Hermes `memory` tool for durable user/environment facts
- Hermes skills under `/Users/kevin/.hermes/skills`
- Hermes scripts/workspace under `/Users/kevin/.hermes`
- User-facing final summary in chat

## When to run

Run when Kevin says:

- `/session-close`
- "wrap it up"
- "close this session"
- "save what matters"

## Steps

1. Identify what changed this session.
2. Save only durable, future-useful facts to Hermes memory.
   - Do not save stale task progress, commit SHAs, temporary status, or one-off outcomes.
   - If memory is full, report the fact instead of forcing a messy replacement.
3. Actively review the session for skill-library updates before closing.
   - Treat user corrections to style, format, workflow, or sequence as first-class skill signals.
   - Prefer patching the skill that was in play; otherwise update an existing class-level umbrella skill.
   - Use `references/` for session-specific technical detail rather than creating narrow one-off skills.
   - Say `Nothing to save.` only when the session truly produced no durable workflow or preference learning.
4. If a reusable workflow was created or corrected, save/update a Hermes skill under `~/.hermes/skills`.
5. Give Kevin a concise closeout:
   - what changed
   - where it lives
   - what is protected
   - next step, if any

## Output format

```text
Session close:
- Changed: ...
- Protected: ...
- Saved: ...
- Next: ...
```
