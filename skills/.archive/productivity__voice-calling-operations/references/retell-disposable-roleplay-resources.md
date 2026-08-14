# Retell Disposable Resources for One-Off Role-Play Calls

Use this pattern when a simulation needs a scenario-specific opening that the production agent's fixed `begin_message` cannot support.

## Resource lifecycle

1. Fetch the production Retell LLM and agent as configuration references only.
2. Create a temporary LLM from a minimal allowlist of supported fields.
3. Replace `general_prompt` and `begin_message` with the simulation scenario.
4. Remove production tools, states, webhooks, and any capability that could create external side effects.
5. Create a temporary agent using the configured custom voice and the temporary LLM response engine.
6. Place the call through `POST /v2/create-phone-call` with the configured from-number, private destination, and `override_agent_id` set to the temporary agent.
7. Verify initiation using the returned `call_id` and status. If subprocess output is delayed, query `POST /v2/list-calls` and match the temporary agent ID plus a recent timestamp.
8. Poll `GET /v2/get-call/{call_id}` until `ended` or `error`, inspect the disconnect reason/transcript, then delete the temporary agent and LLM in a `finally` cleanup path.

## Retell configuration coupling

Retell rejects an agent payload containing `stt_mode: custom` without `custom_stt_config`. Copy the complete pair or omit both. More generally, avoid reposting an entire GET response into a create endpoint: read-only fields and conditionally required settings can make the payload invalid.

A safe minimal temporary-agent payload centers on:

- `agent_name`
- `voice_id`
- `response_engine: {type: "retell-llm", llm_id: ...}`
- only explicitly needed voice/conversation settings

A safe temporary-LLM payload centers on:

- `model`
- `general_prompt`
- `begin_message`
- only explicitly needed latency/temperature settings

## Privacy and verification

- Do not print API keys, full destination numbers, or transcripts unnecessarily.
- Avoid putting raw private numbers in long-lived scripts, filenames, or normal chat.
- Do not report completion from submission alone. `registered` or `ongoing` proves initiation; `ended` plus transcript/disconnect evidence supports a completion claim.
- Never modify the production agent for a one-off demo; this avoids affecting concurrent inbound/outbound calls and eliminates restore races.
