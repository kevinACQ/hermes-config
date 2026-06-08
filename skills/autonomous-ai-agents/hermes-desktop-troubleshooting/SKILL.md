---
name: hermes-desktop-troubleshooting
description: Diagnose Hermes Desktop app issues where the UI, gateway runtime, and stored session database disagree — e.g. Desktop says "session not found" even though `hermes sessions list` shows the session, stale runtime pointers after gateway restart, duplicated optimistic messages, or Desktop-only send/resume failures.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, desktop, gateway, sessions, troubleshooting]
    related_skills: [hermes-agent, hermes-debug]
---

# Hermes Desktop Troubleshooting

Use this when Kevin reports a Hermes Desktop UI problem, especially when the CLI and Desktop disagree.

## Core model

Hermes Desktop has three relevant layers:

1. **Stored session DB** — durable transcripts in `~/.hermes/state.db`, visible via `hermes sessions list` and resumable with `hermes --resume <stored_session_id>`.
2. **Gateway/runtime session** — live backend session IDs used by Desktop JSON-RPC calls such as `prompt.submit`.
3. **Desktop renderer state** — in-memory mappings from stored session IDs to runtime session IDs, plus optimistic messages and route state.

A stored session can exist while Desktop still errors if its live runtime pointer is stale.

## Workflow

1. **Confirm the symptom location.** Ask or infer whether the error appears in Desktop, CLI, or a gateway platform. Do not assume `hermes --resume` fixes Desktop state.
2. **Check stored-session existence.** Run or ask Kevin to run:
   ```bash
   hermes sessions list
   ```
   If the stored session appears, the transcript exists and the issue is likely runtime/UI state, not missing data.
3. **Check gateway health.** Use the Hermes Agent skill/gateway commands when available:
   ```bash
   hermes gateway status
   ```
   On Kevin's macOS, prefer launchd-aware gateway controls over raw `pkill`.
4. **Explain the layer mismatch clearly.** If CLI resume works but Desktop still says `session not found`, say: the stored transcript exists, but Desktop is probably submitting to a stale live runtime session ID.
5. **Low-risk user fix first.** Tell Kevin to reload Desktop with **Cmd+R**, reselect the session, and send again.
6. **Escalate only if reload fails.** Fully quit/reopen Hermes Desktop so the renderer forgets stale runtime mappings and calls `session.resume` fresh.
7. **Only then investigate code/logs.** Search for the specific Desktop/gateway RPC path and inspect `tui_gateway/server.py`, `apps/desktop/src/app/session/hooks/*`, and gateway logs.

## Pitfalls

- **Do not present CLI resume as the Desktop fix.** CLI resume validates stored data, but it starts a separate runtime session and does not repair the Desktop renderer's in-memory mapping.
- **Do not over-diagnose from “session not found” alone.** The same phrase can come from OAuth session polling/cancel endpoints, MCP tool server sessions, Desktop gateway runtime sessions, or TUI gateway routes.
- **Do not delete session data as a first step.** If `hermes sessions list` shows the session, preserve the DB and reset only the Desktop/gateway runtime state first.
- **Be concise.** Kevin is usually trying to get unstuck in the UI; lead with the fix, then explain the stored-vs-runtime distinction in one short paragraph.

## References

- `references/desktop-session-not-found.md` — concrete stale-runtime-pointer case from a Desktop `session not found` incident.
