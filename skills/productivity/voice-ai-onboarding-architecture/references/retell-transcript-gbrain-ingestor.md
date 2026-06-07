# Retell Transcript → GBrain Ingestor Pattern

Use when Kevin wants Hermes Voice / RetellAI calls saved into persistent memory without prematurely moving to Supabase/Postgres.

## Recommended architecture

- Retell is the voice interface, not the memory store.
- Google Sheets remains the review/approval UI for extracted memory candidates.
- GBrain markdown is the local durable source of truth for raw transcripts + structured session pages.
- Supabase/Postgres/pgvector comes later after the local memory loop is validated.

## Done condition

A completed Retell `call_analyzed` payload can produce all of these locally:

- `~/.hermes/brain/raw/retell-calls/{YYYY-MM-DD}-{call_id}.md` — verbatim transcript with YAML frontmatter.
- `~/.hermes/brain/raw/retell-calls/{YYYY-MM-DD}-{call_id}.json` — raw payload for audit/migration.
- `~/.hermes/brain/sessions/retell/{YYYY-MM-DD}-{call_id}.md` — structured session page linking to raw files.

## Implementation location

Project:

```text
/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/
```

Bridge:

```text
hermes-v3/memory_bridge.py
```

Core CLI shape:

```bash
python3 hermes-v3/memory_bridge.py \
  --ingest-retell-json /path/to/retell-call.json \
  --brain-root /Users/kevin/.hermes/brain \
  --kevin-phone "+173****4101" \
  --gbrain-sync
```

## Key behavior

1. Normalize Retell webhook/call JSON.
2. Detect caller phone using direction-aware logic:
   - inbound → `from_number`
   - outbound → `to_number`
3. If Kevin phone is configured, skip non-Kevin callers instead of mixing profiles.
4. Save full transcript word-for-word in markdown fenced text.
5. Save raw JSON payload next to the transcript.
6. Create structured session markdown with extraction fields:
   - topic
   - stated_goal
   - surface_problem
   - inferred_bottleneck
   - bottleneck_category
   - recommended_next_step
   - open_loop
   - memory_candidate
   - confidence
7. Optionally run GBrain import/embed after writing files.

## Prototype-first lesson

Do not build Supabase first. The cheapest safe prototype is a local ingestor that proves the raw-to-compiled memory loop. Supabase migration becomes straightforward only after the file shapes and approval flow are stable.

## Boardroom conclusions

- Elon: delete the backend for v1; prove local archival first.
- Karpathy: deterministic code must write/archive transcripts; LLMs may suggest memory candidates but must not be the source of truth.
- Garry Tan: keep Retell thin and move durable memory into GBrain/backend.
- Hamel: eval is binary — one payload creates raw transcript, raw JSON, structured session page, and skips non-Kevin callers.
- Hormozi: verbatim transcript archive is critical; without it future memory is lossy and unauditable.

## Verification

Run from `/Users/kevin/projects/voice-onboarding-mvp`:

```bash
python3 -m unittest hermes-v3/test_memory_bridge.py -v
python3 -m py_compile hermes-v3/memory_bridge.py
bash -n hermes-v3/call-hermes.sh
node --check hermes-v3/webhook-hermes-memory.js
```

Expected: all unit tests pass and syntax checks return cleanly.

## Caveat

The deployed Retell webhook may be Google Apps Script, which cannot directly write to Kevin's local `~/.hermes/brain`. Prefer a local Hermes-side poll/fetch/ingest job for raw transcript archiving rather than exposing Kevin's Mac as a public webhook target.