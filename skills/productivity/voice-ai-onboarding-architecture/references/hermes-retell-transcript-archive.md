# Hermes Retell transcript archive pattern

Use when Kevin wants Hermes Voice / Retell calls saved into durable long-term memory.

## Class-level architecture

Retell should remain the voice interface, not the memory database.

Recommended layers:

1. Retell: call handling, recording, transcript, call analysis.
2. Google Sheets: human review / approval inbox for memory candidates.
3. Local GBrain markdown repo: private raw archive + searchable session pages.
4. Later Supabase/Postgres/pgvector: production backend after the local loop is proven.

## Raw vs compiled memory rule

Save the full transcript verbatim, but do not automatically promote every extracted fact into durable compiled memory.

- Raw memory: exact transcript + raw Retell JSON, stored for audit/search.
- Structured session page: topic, stated goal, open loop, memory candidate, links to raw files.
- Compiled durable memory: only explicit, useful, approved/high-confidence facts.

This avoids lossy memory while preventing speculative call details from becoming permanent truth.

## Current implementation paths

Project root:

```text
/Users/kevin/projects/voice-onboarding-mvp
```

Core bridge:

```text
hermes-v3/memory_bridge.py
```

Manual archive wrapper:

```text
hermes-v3/archive-retell-call.sh
```

Local brain destinations:

```text
/Users/kevin/.hermes/brain/raw/retell-calls/{YYYY-MM-DD}-{call_id}.md
/Users/kevin/.hermes/brain/raw/retell-calls/{YYYY-MM-DD}-{call_id}.json
/Users/kevin/.hermes/brain/sessions/retell/{YYYY-MM-DD}-{call_id}.md
```

## Commands

Fetch and archive one Retell call by ID:

```bash
cd /Users/kevin/projects/voice-onboarding-mvp
source .env
./hermes-v3/archive-retell-call.sh call_xxx --gbrain-sync
```

Equivalent direct command:

```bash
python3 hermes-v3/memory_bridge.py \
  --fetch-retell-call call_xxx \
  --brain-root /Users/kevin/.hermes/brain \
  --kevin-phone '+173****4101' \
  --gbrain-sync
```

Ingest an already-saved Retell JSON payload:

```bash
python3 hermes-v3/memory_bridge.py \
  --ingest-retell-json hermes-v3/last-call-call_xxx.json \
  --brain-root /Users/kevin/.hermes/brain \
  --kevin-phone '+173****4101'
```

## Required behavior

- Never print Retell API keys.
- Treat Apps Script / Sheets as cloud review UI; it cannot directly write to Kevin's local `~/.hermes/brain` files.
- Prefer local polling/fetching of Retell calls over exposing Kevin's Mac as a public webhook target when scheduled or manual archive is acceptable.
- If Kevin explicitly wants after-call/event-triggered archival, use a tiny deterministic local webhook server behind a tunnel + shared secret, not an LLM-agent webhook, for local file/GBrain side effects.
- Match Kevin's phone with exact or redacted-safe patterns like `+173****4101`.
- Store raw transcript and raw JSON first; create a structured session page second.
- Optional `--gbrain-sync` should run import/embed after files are written.

## Event-triggered local archive pattern

Use this when the requirement is “archive immediately after each Retell call” rather than “poll later.”

Recommended flow:

```text
Retell call_analyzed webhook
→ Google Apps Script logs/normalizes the payload in Sheets
→ Apps Script forwards the payload to a public tunnel URL
→ local deterministic archive server receives `/retell-archive`
→ `memory_bridge.py` ingests transcript/raw JSON/session page
→ optional GBrain import/embed sync
```

Implementation notes:

- Keep the server narrow: accept Retell-style JSON, validate the optional shared secret, call the archive bridge, return JSON status.
- Keep secrets in the project `.env` or Apps Script properties; never paste API keys or tunnel secrets in chat.
- Google Apps Script cannot reach `127.0.0.1` on Kevin's Mac; it needs a public forwarding layer such as Cloudflare Tunnel/ngrok/Tailscale Funnel.
- Verify locally first with `curl http://127.0.0.1:<port>/health` and a synthetic `/retell-archive` POST before wiring Apps Script.
- Use an event-driven server only for this immediate-after-call requirement; otherwise the lower-exposure local polling/fetch path remains preferred.

## Verification

After editing this flow, run:

```bash
cd /Users/kevin/projects/voice-onboarding-mvp
python3 -m unittest hermes-v3/test_memory_bridge.py -v
python3 -m py_compile hermes-v3/memory_bridge.py
bash -n hermes-v3/call-hermes.sh hermes-v3/archive-retell-call.sh
node --check hermes-v3/webhook-hermes-memory.js
```

For GBrain verification:

```bash
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
cd /Users/kevin/.hermes/brain
gbrain import /Users/kevin/.hermes/brain --no-embed
gbrain embed --stale
gbrain search "Retell call transcript"
```
