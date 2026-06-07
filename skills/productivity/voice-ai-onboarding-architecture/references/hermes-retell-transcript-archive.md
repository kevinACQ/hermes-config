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
- Prefer local polling/fetching of Retell calls over exposing Kevin's Mac as a public webhook target.
- Match Kevin's phone with exact or redacted-safe patterns like `+173****4101`.
- Store raw transcript and raw JSON first; create a structured session page second.
- Optional `--gbrain-sync` should run import/embed after files are written.

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
