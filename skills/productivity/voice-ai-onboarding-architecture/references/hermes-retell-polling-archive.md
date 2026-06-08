# Hermes Retell polling archive pattern

Use this when Kevin wants Retell/Hermes Voice calls archived into local GBrain without exposing his Mac through a public webhook tunnel.

## Decision

Prefer a local polling archive job over a public tunnel/local webhook server unless real-time GBrain sync is explicitly required.

Reason: the operational memory path already lands in Google Sheets through Apps Script. GBrain is the durable local archive/search layer and can be eventually consistent. Polling removes the fragile chain:

`Retell -> Apps Script -> tunnel -> local Mac server -> subprocess -> GBrain`

and replaces it with:

`Retell/Scripts -> Sheets immediately` plus `local launchd poller -> Retell API -> ~/.hermes/brain -> gbrain sync`.

## Architecture

1. Apps Script continues to write call analysis to Google Sheets as the immediate source of truth.
2. A local launchd job runs hourly.
3. The job calls `memory_bridge.py --archive-recent-retell-calls --gbrain-sync`.
4. The bridge lists recent Retell calls, skips already-seen IDs, fetches completed calls, archives Kevin calls, and updates a sentinel.
5. GBrain imports/embeds only after at least one call was ingested.

## Files from the working implementation

- Project: `/Users/kevin/projects/voice-onboarding-mvp`
- Bridge: `hermes-v3/memory_bridge.py`
- Tests: `hermes-v3/test_memory_bridge.py`
- Poller script: `hermes-v3/archive-recent-retell-calls.sh`
- launchd plist: `~/Library/LaunchAgents/ai.hermes.retell-archive.plist`
- State sentinel: `~/.hermes/state/retell-archive-state.json`
- Logs: `~/.hermes/logs/retell-archive.out.log`, `~/.hermes/logs/retell-archive.err.log`

## Implementation notes

Add bridge functions for:

- `list_retell_calls(api_key, limit=50)` using Retell `POST /v2/list-calls`.
- `load_archive_state(state_path)` and `save_archive_state(...)` for the sentinel.
- `select_calls_to_archive(calls, state)` to skip old IDs/statuses and preserve oldest-first ingest order.
- `archive_recent_retell_calls(...)` to fetch, archive, optionally sync GBrain, and update state.

Sentinel should store both:

- `last_archived_started_at`
- recent `archived_call_ids`

Important pitfall: mark skipped non-Kevin calls as processed too. Otherwise the poller repeatedly selects the same latest non-Kevin call forever.

## launchd pattern

Use a user LaunchAgent rather than cron on Kevin's Mac:

```xml
<key>Label</key>
<string>ai.hermes.retell-archive</string>
<key>ProgramArguments</key>
<array>
  <string>/bin/bash</string>
  <string>/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/archive-recent-retell-calls.sh</string>
</array>
<key>StartInterval</key>
<integer>3600</integer>
<key>RunAtLoad</key>
<true/>
```

Bootstrap with:

```bash
mkdir -p ~/.hermes/logs ~/.hermes/state
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.retell-archive.plist 2>/dev/null || true
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.retell-archive.plist
launchctl kickstart -k gui/$(id -u)/ai.hermes.retell-archive
launchctl print gui/$(id -u)/ai.hermes.retell-archive
```

## Verification

Minimum verification before reporting done:

```bash
python3 -m unittest hermes-v3/test_memory_bridge.py -v
./hermes-v3/archive-recent-retell-calls.sh
./hermes-v3/archive-recent-retell-calls.sh
```

Expected first live run: may archive historical Kevin calls and sync GBrain.
Expected second run: `selected: 0`, `archived: 0` once sentinel is current.

Also inspect:

```bash
cat ~/.hermes/state/retell-archive-state.json
launchctl print gui/$(id -u)/ai.hermes.retell-archive
```

## Guided manual eval pattern

When Kevin asks to manually eval this system, do not hand him a long list of commands. Hermes should run every non-human step and ask Kevin to do only the physical/manual part: make the test call.

Flow:

1. Hermes checks launchd baseline: `launchctl print gui/$(id -u)/ai.hermes.retell-archive` should show `last exit code = 0` and `run interval = 3600 seconds`.
2. Hermes runs baseline archive: `./hermes-v3/archive-recent-retell-calls.sh`; expected before the call is usually `selected: 0`, `archived: 0`.
3. Ask Kevin to call the Retell number and say a unique code word/phrase. Give exactly one phrase to say, then ask him to reply `done`.
4. After Kevin replies `done`, Hermes runs the archive script again. Pass condition: `archived: 1` for the new call.
5. Hermes reads the returned `raw_transcript` file and answers Kevin's code-word question from the transcript.
6. Hermes verifies GBrain indexing with `GBRAIN_HOME="$HOME/.hermes" PATH="$HOME/.bun/bin:$HOME/.local/bin:$PATH" gbrain search "<code word>"`. Plain `gbrain` may be missing from launch shell PATH; set `GBRAIN_HOME` and prepend Bun/local bins.
7. Hermes immediately re-runs the archive script. Pass condition: `selected: 0`, `archived: 0` to prove idempotency.
8. Hermes checks `~/.hermes/logs/retell-archive.err.log`; pass condition: empty/no new errors.

Reporting style for Kevin:
- Give a tiny status update first: baseline pass, waiting on manual call, or eval pass/fail.
- Put the condensed numbered checklist/key actions near the bottom, not only pass/fail criteria.
- If Kevin asks “what code word did I say?”, answer directly from the archived transcript first, then give eval status.

## When to use a tunnel instead

Only revisit Cloudflare/ngrok if Kevin proves a concrete need for GBrain to update within seconds after a call. If real-time is required, add a durable queue/retry layer first; do not rely on Apps Script forwarding directly to a local server with no replay.
