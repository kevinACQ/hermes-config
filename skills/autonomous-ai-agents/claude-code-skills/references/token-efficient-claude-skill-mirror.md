# Token-efficient Claude skill mirror pattern

Use this reference when Kevin asks Hermes to reuse Claude Code skills exactly as designed without turning the Hermes skill catalog into a hidden token sink.

## Architecture

- Claude remains source of truth: `/Users/kevin/.claude/skills`.
- Hermes mirror lives at: `/Users/kevin/.hermes/external-repos/claude-code-skills`.
- Mirror entries are symlinks, not copies, to avoid drift.
- Mirror manifest lives at: `/Users/kevin/.hermes/external-repos/claude-code-skills/MANIFEST.md`.
- Refresh script lives at: `/Users/kevin/.hermes/scripts/refresh_claude_skill_mirror.py`.

## Operating model

1. Keep mirrored Claude skills disabled by default in `skills.disabled` to avoid loading their descriptions into Hermes's always-on skill catalog.
2. Keep this small Hermes-native index skill enabled so Hermes knows where to look.
3. When Kevin names a Claude skill, read the symlinked file directly:
   - `/Users/kevin/.hermes/external-repos/claude-code-skills/<skill-name>/SKILL.md`
4. Treat the content as explicit workflow context for the current task.
5. Prefer direct reads over temporarily enabling the skill. Temporarily enable only when native `skill_view()` behavior is specifically needed.

## Safety boundaries

Do not mirror or execute Claude lifecycle/memory skills inside Hermes:

- `session-close`
- `remember-fact`
- `state-transfer`

Reason: these may write to Claude-owned memory/session architecture such as `~/.claude/memory`, Claude `CLAUDE.md`, or Claude session traces. Hermes should use Hermes-native memory, skills, workspace files, and Hermes's own `/session-close` instead.

## Conflict handling

If a Claude skill name conflicts with a useful Hermes-native skill, keep the Hermes-native skill enabled and skip/disable the Claude duplicate unless Kevin explicitly chooses otherwise. Example: keep Hermes-native `codex` enabled.

If a Hermes-native skill is ambiguous, low-value, or superseded by Claude's source-of-truth skill, archive it rather than keeping both active. Example pattern: move to `~/.hermes/skills/.archive/<name>-hermes-builtin` after explicit approval for destructive/archive actions.

## Verification checklist

After refreshing the mirror, verify:

- The mirror path exists.
- `MANIFEST.md` was updated.
- Expected regular Claude workflow skills are present as symlinks.
- Claude lifecycle/memory skills are absent from the mirror.
- Mirrored Claude skills are disabled in Hermes config.
- The small `claude-code-skills` index remains enabled.
- Hermes-native `/session-close` remains enabled.
- Any useful Hermes-native conflict winners, such as `codex`, remain enabled.

## Important pitfall

Disabled mirrored skills cannot be loaded with `skill_view("<skill-name>")`; that failure is expected. Read the mirrored `SKILL.md` file directly unless there is a specific reason to temporarily enable native skill loading.
