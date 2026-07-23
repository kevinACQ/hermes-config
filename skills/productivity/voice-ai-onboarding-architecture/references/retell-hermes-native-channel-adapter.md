# Retell as a native Hermes phone channel

Use when Kevin wants the Retell number to behave like Desktop, CLI, Discord, or Telegram—with the real Hermes runtime, tools, canonical sessions, and persistent memory.

## Core architectural rule

Do not solve channel parity by expanding the Retell prompt, knowledge base, or static memory briefing.

Retell should own:
- telephony and audio transport
- speech recognition and synthesis
- turn detection, interruption, and hang-up controls

Hermes should own:
- reasoning and context assembly
- canonical session history
- memory retrieval and writes
- skills and tools
- permissions, execution, and receipts

Target flow:

```text
Retell custom-LLM WebSocket
→ thin phone-channel adapter
→ Hermes API Server Sessions API
→ real AIAgent runtime + tools + state.db
→ streamed response back to Retell
```

Keep the existing Sheets/GBrain transcript archive as review, audit, recovery, and backfill infrastructure—not as the live intelligence layer.

## Hermes API Server integration

Preferred surface for the prototype:

1. Enable the API Server in `~/.hermes/.env`:
   - `API_SERVER_ENABLED=true`
   - `API_SERVER_KEY=<strong random secret>`
2. Restart the macOS gateway with launchd `bootout` / `bootstrap` / `kickstart`.
3. Verify `GET http://127.0.0.1:8642/health`.
4. Create a canonical session with `POST /api/sessions`.
5. Send each completed voice turn to:
   - `POST /api/sessions/{session_id}/chat/stream`
6. Authenticate with `Authorization: Bearer <API_SERVER_KEY>`.
7. Send a stable memory scope:
   - `X-Hermes-Session-Key: agent:main:retell:dm:kevin`
8. Consume SSE events:
   - `assistant.delta`
   - `tool.started` / `tool.completed` / `tool.failed`
   - `run.completed`
9. Verify canonical persistence with:
   - `GET /api/sessions/{session_id}/messages`

Use one Retell call ID as the transcript/session ID for an MVP. The stable session key preserves caller-level memory scope across calls. A later first-class `RetellAdapter(BasePlatformAdapter)` is the path to literal gateway parity, including gateway hooks, slash commands, queueing, and authorization behavior.

## Retell custom-LLM WebSocket contract

The adapter hosts a public `wss://` endpoint. Retell sends:
- `call_details`
- `response_required`
- `reminder_required`
- `update_only`

Send an initial config frame requesting call details and reconnect support.

For generated speech, stream frames containing:
- `response_type: response`
- matching `response_id`
- incremental `content`
- `content_complete`
- `end_call`

Rules:
- Only respond to `response_required` and `reminder_required`.
- Use `update_only` to synchronize transcript state and cancel stale generation.
- Cancel the old generation when a newer `response_id` arrives.
- Stream phrase-sized chunks; do not resend accumulated text.
- Set `end_call: true` only on the final completed frame after a deterministic hang-up intent.
- Do not close the socket as the normal hang-up mechanism.

Official starting points:
- https://docs.retellai.com/guide/llm-websocket
- https://github.com/RetellAI/retell-custom-llm-python-demo
- https://github.com/RetellAI/retell-custom-llm-node-demo

Recheck current official docs before production wiring because protocol fields and API paths can evolve.

## Prototype implementation pattern

Current prototype files:

```text
/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/retell_hermes_adapter.py
/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/test_retell_hermes_adapter.py
/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/RETELL_HERMES_RUNBOOK.md
```

The adapter should provide:
- `/health`
- high-entropy WebSocket token authentication
- no secret logging
- caller/call ID normalization without phone leakage
- canonical Hermes session creation
- streaming Hermes responses
- cancellation on interruption
- deterministic hang-up
- honest failure language
- tool events kept out of spoken text unless summarized safely

## Truthfulness invariant

Never let the phone agent say “I checked,” “I sent,” “I created,” “I booked,” or “I’ll remember” unless Hermes returned a corresponding successful tool or memory-write event. Advice, intent capture, and action completion are different states.

## TDD and verification

Write protocol tests before production code. Minimum tests:
- query/path token authentication
- secret and phone-number non-leakage
- call/session ID normalization
- SSE parsing
- stable Hermes session-key header
- interruption cancellation
- response-ID matching
- voice chunk boundaries
- deterministic hang-up with `end_call` only on final frame
- honest failure response

Then run a real local smoke test:

1. Create a Hermes API session.
2. Ask Hermes to execute a harmless terminal command with a known marker.
3. Verify the marker in the result.
4. Fetch session messages.
5. Confirm persisted roles include user, assistant/tool call, tool result, and final assistant response.

Do not call the prototype complete merely because unit tests pass.

## External-action boundary

Do not overwrite the live Retell production agent while prototyping. Create a separate test agent using `response_engine.type = custom-llm` and the public secure WebSocket URL only after the local adapter passes.

Starting a long-running local server or public tunnel can trigger an approval gate. If blocked, report the exact completed state and request approval; do not retry through a disguised command or alternative mechanism.

## Production hardening

Before wider use, add:
- TLS and a redacted public reverse proxy/tunnel
- Retell call verification after `call_details`
- caller authentication or step-up PIN for sensitive tools
- per-tool phone permissions
- action idempotency
- dropped-call resume
- session/call/tool trace IDs
- latency budgets and truthful progress messages
- automated regression evals built from archived transcript failures

## Pass/fail evals

Prototype must prove:
1. One live Retell turn reaches the real Hermes runtime.
2. One harmless Hermes tool executes and returns a verified result by voice.
3. The same canonical session can be fetched and resumed outside the call.
4. No fabricated tool-use or completion claim occurs.
5. “Hang up” produces a real final `end_call` frame.

Final parity should test bidirectional cross-channel recall, action receipts, interruption handling, dropped-call resume, and semantic equivalence against Desktop for a representative task matrix.
