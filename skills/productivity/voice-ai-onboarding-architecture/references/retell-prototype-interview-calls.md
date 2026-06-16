# Retell prototype interview calls

Use this when Hermes Voice is being used to interview Kevin for a Prototype-First gate, product discovery call, or any long-form context-gathering call.

## Lesson from 2026-06-16 context-switching harness interview

Kevin received the call, but the default Hermes V3 voice settings were wrong for a discovery interview:

- `max_call_duration_ms: 900000` ended the call at ~15 minutes with `disconnection_reason: max_duration_reached`.
- `interruption_sensitivity: 0.8` was too aggressive; Kevin felt the agent was cutting him off and not listening.
- `responsiveness: 0.9` made the agent jump in too quickly during long answers.
- `backchannel_frequency: 0.55` added too much verbal clutter.

For interview calls, tune the agent to listen longer and interrupt less before placing the call.

## Recommended interview-mode Retell agent settings

Patch the existing Hermes V3 agent, or create a temporary interview clone, with:

```json
{
  "max_call_duration_ms": 1800000,
  "interruption_sensitivity": 0.25,
  "responsiveness": 0.45,
  "backchannel_frequency": 0.25,
  "reminder_trigger_ms": 20000
}
```

Notes:
- 30 minutes is a better default for discovery interviews than 15 minutes.
- Lower interruption sensitivity means Kevin can speak in long, messy context dumps without the agent talking over him.
- Lower responsiveness makes the agent wait before speaking.
- Lower backchannel frequency reduces “yep / got it” clutter.
- Longer reminder trigger avoids prompting too soon while Kevin is thinking.

## Interview call pattern

1. Write the call script first, ideally into `/Users/kevin/My Drive/Claude Code/`.
2. Inject the script as `retell_llm_dynamic_variables.memory_briefing` for the outbound Retell call.
3. Tell the voice agent explicitly:
   - Ask one question at a time.
   - Let Kevin riff.
   - Do not stack questions.
   - Do not summarize while Kevin is mid-answer.
   - End by synthesizing: bottleneck, job-to-be-done, thin prototype, first eval, and `Done = ___`.
4. Poll `GET /v2/get-call/{call_id}` after the call until `call_status` is ended and transcript is present.
5. Archive the transcript with `memory_bridge.py --fetch-retell-call <call_id> --gbrain-sync`.
6. Use the transcript as Gate 1 input for Prototype-First.

## Fallback when the normal `memory_bridge.py --call` path is blocked

If `memory_bridge.py --call` fails before creating the call because it cannot build the Sheets-backed memory briefing, do not abandon the call. For a one-off interview, build a minimal dynamic briefing from the saved call script and POST directly to Retell:

```python
import os, json, urllib.request
from pathlib import Path

script = Path('/Users/kevin/My Drive/Claude Code/context-switching-prototype-interview-call-script.md').read_text()
briefing = """Memory briefing for Kevin:
This call is a Prototype-First interview. Follow the script below. Ask one question at a time. Let Kevin riff. At the end, summarize bottleneck, job-to-be-done, thin prototype, first eval, and Done = one sentence.

""" + script

payload = {
  'from_number': os.environ['RETELL_PHONE_NUMBER'],
  'to_number': os.environ['HERMES_TEST_TO_NUMBER'],
  'override_agent_id': os.environ['RETELL_AGENT_ID_HERMES'],
  'retell_llm_dynamic_variables': {
    'user_name': 'Kevin',
    'memory_loaded': 'true',
    'memory_briefing': briefing[:9000],
  }
}
req = urllib.request.Request(
  'https://api.retellai.com/v2/create-phone-call',
  data=json.dumps(payload).encode(),
  headers={'Authorization': 'Bearer ' + os.environ['RETELL_API_KEY'], 'Content-Type': 'application/json'},
  method='POST',
)
with urllib.request.urlopen(req, timeout=30) as r:
  print(json.dumps(json.loads(r.read().decode()), indent=2))
```

Never print or paste the Retell API key. Use the project `.env` and redact phone numbers in user-facing output.
