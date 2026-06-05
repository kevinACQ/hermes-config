# Hermes Desktop ↔ Retell outbound call connector

Use this when Kevin says outbound Hermes/Retell calling worked in CLI but stopped after moving to Hermes Desktop.

## Durable pattern

Do not solve this by requesting broad macOS folder permissions. Reconnect via the existing project connector/API path:

- project: `/Users/kevin/projects/voice-onboarding-mvp`
- Retell/env source: `/Users/kevin/projects/voice-onboarding-mvp/.env`
- memory bridge: `hermes-v3/memory_bridge.py`
- connector wrapper: `~/.hermes/scripts/call_hermes_retell.sh`

The wrapper should:

1. `cd /Users/kevin/projects/voice-onboarding-mvp`
2. `source .env` with `set -a` / `set +a`
3. invoke Hermes's Python 3.11 venv, not macOS system Python:
   - `/Users/kevin/.hermes/hermes-agent/venv/bin/python`
4. run:
   - `hermes-v3/memory_bridge.py --call`

## Why

Hermes Desktop may not inherit the project `.env`, so Retell keys can appear "missing" from Desktop even though the old CLI/project setup still works. The right repair is a scoped connector wrapper that loads only the voice project env and calls Retell's API.

## Verification before placing a real call

Run a dry payload/briefing check from the project directory using the Hermes venv Python:

```bash
cd /Users/kevin/projects/voice-onboarding-mvp
set -a; source .env; set +a
/Users/kevin/.hermes/hermes-agent/venv/bin/python hermes-v3/memory_bridge.py --print-briefing
/Users/kevin/.hermes/hermes-agent/venv/bin/python hermes-v3/memory_bridge.py --print-payload >/tmp/hermes_retell_payload.json
/Users/kevin/.hermes/hermes-agent/venv/bin/python -m py_compile hermes-v3/memory_bridge.py
```

Expected:

- briefing prints without exposing secrets
- payload contains `from_number`, `to_number`, `override_agent_id`, and `retell_llm_dynamic_variables`
- `retell_llm_dynamic_variables.memory_loaded` is `true`
- `briefing_chars` is nonzero

Only place the outbound call after Kevin explicitly asks, e.g. "call me now".

## Safety rules

- Never print or repeat the Retell API key.
- Prefer project/env/API connectors over macOS Documents/Desktop access.
- Do not ask for broad local folder permissions to fix a cloud connector problem.
- Treat Retell API calls as external side effects; dry-run first, then call only on explicit user request.
