# Desktop `session not found` with existing stored session

## Situation

Kevin reported Hermes Desktop showing red `session not found` errors when sending in an existing Desktop session. Running:

```bash
hermes sessions list
```

showed the stored session existed, and:

```bash
hermes --resume <stored_session_id>
```

worked in CLI but did not fix Desktop.

## Diagnosis

This is a layer mismatch, not necessarily data loss.

- `hermes --resume <id>` proves the durable transcript exists in `~/.hermes/state.db`.
- Desktop keeps an in-memory mapping from stored session ID to live gateway/runtime session ID.
- Restarting or replacing the gateway can invalidate that live runtime session.
- Desktop may still call `prompt.submit` with the stale runtime ID, and the gateway responds `session not found`.

The stored session exists; Desktop's live runtime pointer is stale.

## Recommended fix sequence

1. In Desktop: press **Cmd+R** to reload the renderer.
2. Click/reselect the affected stored session.
3. Send again.
4. If still broken, fully quit and reopen Hermes Desktop.
5. Only then inspect logs/code.

## Useful source paths

- Desktop prompt submission: `apps/desktop/src/app/session/hooks/use-prompt-actions.ts`
- Desktop session resume/create mapping: `apps/desktop/src/app/session/hooks/use-session-actions.ts`
- Session state cache/runtime mapping: `apps/desktop/src/app/session/hooks/use-session-state-cache.ts`
- TUI/gateway session errors may also appear in `tui_gateway/server.py`

## Communication pattern

Say this plainly:

> CLI resume proves the saved transcript exists. Desktop still errors because it has a stale live runtime session pointer. Reload Desktop with Cmd+R, reselect the session, then send again.

Avoid saying that CLI resume is the fix for Desktop; it is only a diagnostic.
