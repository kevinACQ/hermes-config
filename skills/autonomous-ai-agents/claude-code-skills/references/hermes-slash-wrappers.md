# Hermes Slash Wrappers for Claude Code Skills

## Learned workflow

Kevin wants his Claude Code skills to be callable in Hermes with the same slash-command muscle memory, e.g. `/boardroom`, while Claude remains the source of truth.

The durable pattern is:

1. Keep Claude source skills under `/Users/kevin/.claude/skills`.
2. Keep the token-efficient symlink mirror under `/Users/kevin/.hermes/external-repos/claude-code-skills`.
3. Keep mirrored Claude source skills disabled from Hermes's always-on catalog to avoid hidden token burn.
4. Generate small local Hermes wrapper skills under `/Users/kevin/.hermes/skills/claude-code/<skill-name>/SKILL.md`.
5. Let those wrappers register Hermes slash commands and instruct Hermes to read the mirrored Claude `SKILL.md` at runtime.

## Commands

Refresh source mirror:

```bash
python3 /Users/kevin/.hermes/scripts/refresh_claude_skill_mirror.py
```

Regenerate Hermes wrapper skills:

```bash
python3 /Users/kevin/.hermes/scripts/generate_claude_skill_wrappers.py
```

Then run in Hermes:

```text
/reload-skills
```

or restart the CLI/gateway.

## Safety boundaries

Do not mirror or run Claude memory/session-writer skills against Hermes state unless Kevin explicitly asks. Known blocked names:

- `remember-fact`
- `state-transfer`

Claude's original `session-close` should remain excluded in favor of Hermes-native `/session-close`.

Prefer Hermes-native implementations for ambiguous duplicates such as `codex`; the Claude mirror should not override them.

## Verification recipe

After regeneration, verify at least one expected Claude command and one blocked command:

```bash
cd /Users/kevin/.hermes/hermes-agent
./venv/bin/python - <<'PY'
from agent.skill_commands import scan_skill_commands, build_skill_invocation_message
cmds = scan_skill_commands()
for key in ['/boardroom', '/prototype-first', '/remember-fact', '/state-transfer', '/codex']:
    print(key, key in cmds, cmds.get(key, {}).get('skill_dir', ''))
msg = build_skill_invocation_message('/boardroom', 'review this test plan')
print('boardroom_invocation_message=', bool(msg))
print('contains_source_path=', '/Users/kevin/.hermes/external-repos/claude-code-skills/boardroom' in (msg or ''))
PY
```

Expected shape:

- `/boardroom` true, points to `~/.hermes/skills/claude-code/boardroom`
- `/prototype-first` true, points to `~/.hermes/skills/claude-code/prototype-first`
- `/remember-fact` false
- `/state-transfer` false
- `/codex` true, points to Hermes-native `autonomous-ai-agents/codex`
- boardroom invocation message contains the mirrored Claude source path
