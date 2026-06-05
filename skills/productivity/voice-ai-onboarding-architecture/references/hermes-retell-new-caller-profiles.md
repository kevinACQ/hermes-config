# Hermes Retell new-caller profile pattern

Use this when Kevin wants the Hermes Retell phone agent to support callers besides Kevin, detect new phone numbers, or keep caller-specific context separate.

## Goal

A new caller should not inherit Kevin's memories. The voice agent should ask for the caller's name early, then create or update a fresh profile keyed by phone number.

## Fast implementation pattern

1. Update the Retell LLM prompt first, because that changes live behavior immediately:
   - If the caller sounds like someone other than Kevin, or the call appears to be from a new/unknown phone number, ask: “Before we jump in, what should I call you?”
   - For a new caller, do not assume Kevin's memories apply.
   - Treat the caller as a clean-slate profile until they identify themselves.
2. Persist the profile in the post-call webhook:
   - Add a `Hermes User Profiles` tab.
   - Key rows by normalized `phone_number`.
   - Track `user_name`, `profile_status` (`known` or `needs_name`), `call_count`, `last_call_id`, `last_call_at`, `context_summary`, and notes.
3. On `call_analyzed`, derive the human caller phone number carefully:
   - inbound: prefer `from_number`
   - outbound: prefer `to_number`
   - fallback: `from_number || to_number`
4. Extract `user_name` from Retell custom analysis data if available; otherwise use a lightweight transcript regex such as “my name is X”, “this is X”, “I’m X”.
5. If the phone number is unseen, append a fresh profile row. If name is missing, set `profile_status` to `needs_name`.
6. When appending memory candidates, include the caller name/phone note so review does not accidentally promote another person's fact as Kevin's memory.

## Verification

- `node --check hermes-v3/webhook-hermes-memory.js`
- Existing memory bridge tests: `python -m unittest hermes-v3/test_memory_bridge.py`
- Verify Retell prompt was updated by GETting the LLM and checking for the new-caller phrase, without printing secrets.

## Deployment pitfall

Hermes's Google Workspace OAuth may have Sheets/Drive access but lack Apps Script management scope. In that case Hermes can update local webhook source and Sheets, but cannot push Apps Script code directly. Ship the live prompt update first, then give Kevin the exact Apps Script file to paste/deploy or redo Google OAuth with Apps Script management scope.
