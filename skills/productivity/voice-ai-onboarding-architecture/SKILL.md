---
name: voice-ai-onboarding-architecture
description: Review and design the ACQ Vantage Voice AI onboarding system using ElevenLabs, Supabase, GitHub repos, and Karpathy-style compiled memory.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [voice-ai, onboarding, elevenlabs, supabase, memory, github]
---

# Voice AI Onboarding Architecture

Use this when Kevin asks about the ACQ Vantage voice AI onboarding project, data ingestion, data output, ElevenLabs capabilities, or persistent member memory.

## Core Context

- Repo: `kevinACQ/voice-onboarding-mvp`
- Related app repo: `kevinACQ/ACQ_Vantage`
- Current voice quality blocker correction: Alex voice quality is good enough.
- Real blocker: high-quality data ingestion, high-quality output, persistent member memory, and backend database sync.
- Preferred answer style: concise executive summary, clear next move.

## Known Architecture

Current stack / source-of-truth warning:
- Historical/main repo docs describe ElevenLabs Conversational AI + Twilio + Google Apps Script / Google Sheet.
- A newer Claude worktree may contain a Retell migration and Vance/V2/V3 agent work: `/Users/kevin/projects/voice-onboarding-mvp/.claude/worktrees/*`.
- Always inspect both the main repo and any `.claude/worktrees/*` state-transfer docs before recommending changes; the active platform may be Retell even when main README/SOP still says ElevenLabs.
- ACQ_Vantage may have split integration paths: `/api/onboarding-call` can use Retell while `/api/zapier-trigger` may still use ElevenLabs Alex/Leila.
- Google Apps Script / Google Sheet is demo/debug capture; Supabase/backend should become production source of truth.

ElevenLabs capabilities confirmed from docs:
- Dynamic variables can inject runtime values into system prompt, first message, tools, and headers.
- Server tools can call external APIs during a conversation.
- Knowledge base is for static/domain knowledge, not per-member memory.
- Data Collection can extract structured fields after calls, with 25–40 item limits depending on plan.
- Post-call webhooks can send extracted data to external systems.

## Recommended System Design

Use ElevenLabs for the live call experience, but make Supabase the long-term memory and source of truth.

Flow:
1. Before call: identify member by phone/email/member_id.
2. Fetch member profile, past forms, prior calls, and enrichment from backend.
3. Send concise dynamic variables to ElevenLabs:
   - name / pronunciation
   - known business facts
   - missing priority fields
   - call goal
4. Agent asks only missing high-value questions.
5. During call: agent listens first, asks backstop questions only for missing priority fields.
6. After call: save transcript, recording URL, call metadata, extracted fields, confidence, and source.
7. Run a backend extraction/merge pass over the transcript to fill all possible fields.
8. Update member profile memory so the next call starts with context.

## Karpathy-Style Memory Rule

Do not treat the latest LLM output as the source of truth.

Keep three layers:
- Raw layer: transcript, recording, webhook payload, form answers.
- Compiled layer: clean member profile / business profile.
- Schema layer: field definitions, priority, extraction rules, confidence rules.

Every profile field should track:
- value
- source: form, call transcript, enrichment, manual edit
- source_id or conversation_id
- confidence
- updated_at

## Prompt Strategy

Prompt should not ask 40 questions.

It should:
- Start with what the agent already knows.
- Ask a broad opener.
- Listen and infer fields from natural speech.
- Ask missing priority fields one at a time.
- Confirm the synthesized business profile before closing.
- Set expectations for what happens next.

High-priority fields should be separated from optional fields. Optional fields should be filled opportunistically, not asked directly unless needed.

## Knowledge Base Strategy

Use ElevenLabs Knowledge Base for:
- ACQ onboarding playbook.
- Definitions of fields.
- Examples of good answers.
- Questioning strategy.
- Product expectations / next steps.

ElevenLabs docs best practices:
- Keep KB content clear, well-structured, relevant, and regularly updated.
- Break large documents into smaller focused pieces.
- Review transcripts to find knowledge gaps and add missing static context.
- Enable RAG for large static docs so only relevant chunks enter the model context instead of loading full documents into the prompt.
- Use Prompt-mode documents sparingly; too many always-included docs can exceed context limits.

Do not use it for:
- Per-member memory.
- Sensitive member profile data.
- Frequently changing database state.

Per-member memory belongs in Supabase and should be injected as a short dynamic-variable briefing or fetched by server tools.

## Boardy-Style V3 Voice Agent Pattern

When Kevin asks whether Hermes can create a new voice agent from Boardy.ai / transcript analysis context, recommend a separate test agent rather than overwriting production agents.

Preferred approach:
1. Build a separate V3 "Founder Advisor Intake" agent (often Vance V3) using the existing voice stack/settings.
2. Do not overwrite Alex/Leila or wire Zapier until V3 passes manual eval.
3. Use Boardy-derived behavior rules:
   - ask one high-leverage question at a time
   - treat "I'm not sure" as diagnostic signal
   - reframe surface problem into root bottleneck
   - challenge premature solutions like hiring when process/ownership/context may be the real issue
   - use vivid founder-friendly metaphors sparingly
   - close with one continuity/bottleneck summary
4. Keep the original five onboarding fields, but add optional extraction fields for:
   - current_goal
   - biggest_bottleneck
   - bottleneck_category
   - support_needed
   - advisor_summary
   - confidence
5. Validate with 3-5 manual calls and Kevin pass/fail critique before routing real members.

Fast deliverables:
- `agent-prompt-v3-boardy.md`
- Retell/voice-platform extraction schema for bottleneck fields
- 5-call manual eval rubric
- optional create/update script copied from the existing V2 pattern

## Hermes V3 Retell Agent Build Pattern

Current verified Hermes V3 state as of 2026-06-05:
- Retell agent exists: `Hermes V3 — Kevin Voice Advisor`, agent ID `agent_5fd02629f0ee9491a55d6f87bb`, LLM ID `llm_60eb98cc38fb9e8e4e4b370cf7e1`.
- Retell phone/from number: `+17159998518`.
- Voice: custom ElevenLabs v3 voice (`custom_voice_17e84ee17f6d4992a42e8b4bd8`, `eleven_v3`). Retell API exposes the voice ID/model, not the human-readable clone name.
- Retell LLM response engine is `retell-llm`; current model observed as `gpt-5.5`.
- Webhook events include `call_started`, `call_ended`, and `call_analyzed`; post-call schema and webhook are working.
- `/Users/kevin/projects/voice-onboarding-mvp/.env` contains the active Retell and webhook values; do not expose or repeat API keys in chat.
- During prompt iteration, do not change schema, webhook URL, voice, or agent-level settings unless Kevin explicitly asks.

When Kevin asks to “start” or “autoplan each phase” for the Hermes/Retell voice advisor, treat it as an execution prep or self-improvement task, not just a recommendation.

Default implementation path:
1. Load this skill plus `plan`/`google-workspace` if Sheets or eval setup is involved.
2. Read the saved plan if provided, usually `/Users/kevin/My Drive/Claude Code/retell-hermes-voice-agent-plan.md`.
3. Validate against Karpathy guidelines if requested: `/Users/kevin/.claude/skills/karpathy-guidelines/SKILL.md`.
4. Inspect both main repo and Claude worktrees. If `search_files` misses hidden worktree files, use a small Python `os.walk`/`execute_code` scan under `/Users/kevin/projects/voice-onboarding-mvp/.claude/worktrees`.
5. Create an isolated folder only: `/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/`.
6. Prepare, but do not externally execute, the Retell/API steps until Apps Script webhook/env values are ready.

Reusable Hermes V3 deliverables:
- `README.md` — states Hermes V3 is separate from Alex/Leila/Vance.
- `.env.example` — placeholders only, no secrets.
- `AUTOPLAN.md` — phase-by-phase goals, deliverables, verification, pass bars.
- `agent-prompt-hermes-v3.md` — voice-native Hermes prompt, no `[pause]` tags, one-question discipline, memory-safe language.
- `post-call-analysis-schema.json` — Retell fields for topic, stated goal, surface problem, inferred bottleneck, bottleneck category, next step, open loop, memory candidate, people/projects, follow-up, confidence, call quality summary.
- `webhook-hermes-memory.js` — Google Apps Script webhook creating `Hermes Calls`, `Hermes Memory Candidates`, `Hermes Evals`, and `Hermes Weekly Trend` tabs.
- `eval-rubric.md` — weighted 10-criterion eval; most important manual field is `top_issue`.
- `create-hermes-agent.sh` — copied/adapted from Retell V2 script; writes IDs to `.env`, not repo files.
- `call-hermes.sh` — outbound test call script using `RETELL_AGENT_ID_HERMES`.
- `karpathy-validation.md` — validates scope, simplicity, surgical changes, and verification.

Verification before reporting done:
- `bash -n hermes-v3/create-hermes-agent.sh hermes-v3/call-hermes.sh`
- `python3 -m json.tool hermes-v3/post-call-analysis-schema.json >/dev/null`
- `node --check hermes-v3/webhook-hermes-memory.js`
- scan prompt for `[pause` / vocal tags.
- `git status --short hermes-v3` to confirm only V3 files are in the intended folder.

Google Sheets OAuth bootstrap:
- When Kevin says Google Workspace OAuth is complete, first run `python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py --check` and verify `AUTHENTICATED`.
- If the Apps Script webhook is not deployed yet, use the Sheets API/Python client to create the Hermes memory/eval spreadsheet directly: create tabs `Hermes Calls`, `Hermes Memory Candidates`, `Hermes Evals`, `Hermes Weekly Trend`; write headers; add `Hermes Evals` weighted-score formulas; append one synthetic validation row; then write `HERMES_MEMORY_SHEET_ID=<sheet_id>` to `/Users/kevin/projects/voice-onboarding-mvp/.env`.
- Patch `hermes-v3/webhook-hermes-memory.js` to default to the created Sheet ID instead of `PASTE_SHEET_ID_HERE`, while still allowing `PropertiesService.getScriptProperties().getProperty('HERMES_MEMORY_SHEET_ID')` to override it.
- Phone numbers written through Sheets API can be interpreted as formulas if they start with `+`; write them as text by prefixing an apostrophe, e.g. `"'+173****4101"`.
- Verify Sheets setup with `google_api.py sheets get <sheet_id> "Hermes Calls!A1:E3"` or equivalent Python Sheets API read.

External-action boundary:
- Creating the actual Retell agent calls the external Retell API and depends on `RETELL_WEBHOOK_URL`, Retell keys, and voice IDs. Prepare scripts first; run the API creation only after webhook deployment/env readiness is clear.
- Hermes's current Google Workspace OAuth scopes include Sheets/Drive read but do not include Apps Script deployment scopes, so Hermes can create/verify the Sheet but cannot automatically deploy the Apps Script webhook unless those scopes are added. If blocked, give Kevin the exact file to paste/deploy and ask only for the Web App URL.
- Recommended next order after prep: deploy Apps Script, set `HERMES_MEMORY_SHEET_ID`, run `testHermesWebhook()`, set `RETELL_WEBHOOK_URL`, then run `./create-hermes-agent.sh` and `./call-hermes.sh`.

Hermes V3 self-improvement call loop:
1. Trigger an outbound call with the Retell API using values from `/Users/kevin/projects/voice-onboarding-mvp/.env`; do not paste or print the API key. If `hermes-v3/call-hermes.sh` contains redacted auth text, bypass it with a small Python `urllib.request` POST to `https://api.retellai.com/v2/create-phone-call` using `RETELL_PHONE_NUMBER`, Kevin's test number, and `RETELL_AGENT_ID_HERMES`.
2. Poll `GET https://api.retellai.com/v2/get-call/{call_id}` until `call_status` is ended and both transcript and `call_analysis` are present. Save the full JSON under `hermes-v3/last-call-{call_id}.json` for private analysis.
3. Read the full transcript, not just extracted fields. Score the 10 rubric criteria: useful_diagnosis, one_question_discipline, boardy_flow, memory_capture, conciseness, turn_taking, latency, next_step_quality, tone_fit, would_call_again.
4. Calculate weighted score with weights: 20%, 10%, 10%, 15%, 10%, 10%, 5%, 10%, 5%, 5% respectively.
5. Identify one top issue only and one minimal `fix_action`; do not batch fixes.
6. Append an eval row to `Hermes Evals!A:R` using the Google Workspace Sheets API. Column Q is left blank for Kevin's PASS/FAIL; Kevin's note overrides Hermes's self-diagnosis.
7. Report concise results: call ID, duration/status, weighted score, top issue, proposed fix, extracted memory candidate, and ask Kevin for `PASS` or `FAIL: reason`.
8. Patch the Retell LLM prompt only after Kevin gives FAIL or explicitly approves the fix. Always GET the current Retell LLM prompt before PATCHing. Never change schema, webhook URL, voice, or agent-level settings during prompt iteration.

Observed failure to remember for prompt iteration:
- When Kevin asks about to-dos, memory, prior context, or what Hermes remembers, the voice agent should answer in one sentence. It should say that the current voice call only has context injected into this call and persistent cross-call memory is the next system layer. It should not explain architecture unless Kevin asks, and if Kevin says “just say got it,” obey exactly.

Hermes V3 pass/fail eval rule:
- Kevin corrected that numbered rankings are prone to hallucinations. Treat PASS/FAIL criteria as the source of truth; numeric scores are optional secondary trend diagnostics only.
- A call is PASS only if all must-pass checks pass and no critical fail appears.
- Must-pass checks: useful response to the real ask; concise by default; one-question discipline; accurate memory behavior; turn-taking/direct-instruction obedience; advisor value; tone fit.
- Critical fails: hallucinated memory or claimed access it did not have; revealed/asked for secrets; ignored Kevin's direct instruction to stop/be brief/hang up; repeated the same corrected behavior from the prior failed call; failed to capture the obvious durable memory candidate.
- Preferred Sheet columns for pass/fail evals: overall_verdict, useful_response_pass, concise_pass, one_question_pass, memory_behavior_pass, turn_taking_pass, advisor_value_pass, tone_fit_pass, critical_fail, top_issue, fix_action, kevin_notes.
- Local criteria doc: `/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/pass-fail-eval-criteria.md`.

Hermes V3 persistent Retell memory bridge:
Hermes V3 persistent Retell memory bridge:
- Use this when Kevin asks Retell/Hermes Voice to remember past calls, reconnect outbound calling after Desktop/CLI migration, support callers besides Kevin, detect new phone numbers, trigger a Retell call from Hermes, or archive Retell transcripts into long-term memory. The reusable implementation is `/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/memory_bridge.py` with tests in `hermes-v3/test_memory_bridge.py`.
- Desktop reconnection reference: `references/hermes-desktop-retell-connector.md`. Prefer the scoped connector wrapper (`~/.hermes/scripts/call_hermes_retell.sh`) that sources the voice project `.env` and calls Retell via API over asking for broad macOS Documents/Desktop permissions.
- New-caller/profile reference: `references/hermes-retell-new-caller-profiles.md`. Ship the Retell prompt rule first so live behavior changes immediately, then deploy/paste the Apps Script webhook persistence if Apps Script management scope is unavailable.
- Transcript archive references: `references/hermes-retell-transcript-archive.md` for raw transcript/GBrain structure and `references/hermes-retell-polling-archive.md` for the preferred local poller implementation and guided manual eval pattern. When Kevin explicitly wants full Retell call memory, save raw transcript + raw JSON into GBrain markdown first, then create structured session pages and only promote approved/high-confidence facts to compiled memory.
- Default archive architecture: keep Apps Script/Sheets as the immediate operational memory path, then run a local launchd poller hourly to fetch completed Retell calls and sync GBrain. Avoid public tunnel/local webhook server by default; use it only if Kevin proves second-level GBrain freshness is needed and add durable retry/queue semantics first.
- Design rule: Retell is the voice interface, not the memory source of truth. Google Sheets is review/approval UI; GBrain is durable semantic memory and raw transcript archive; Retell receives a compact briefing.
- Apps Script / Sheets cannot directly write to Kevin's local `~/.hermes/brain`; prefer local polling/fetching of Retell calls over exposing Kevin's Mac as a public webhook target. Mark non-Kevin/skipped calls as processed in the poller sentinel too, otherwise the latest skipped call can be selected forever.
- The bridge compiles approved rows from `Hermes Memory Candidates` plus recent call context into a concise memory briefing. Approved memories are durable; recent call context must be labeled as not-yet-durable truth.
- Outbound calls created by Hermes should use `memory_bridge.py --call`, which sends `retell_llm_dynamic_variables.memory_briefing` in the `POST /v2/create-phone-call` payload.
- Inbound calls need a fallback because dynamic variables may not be present. Run `memory_bridge.py --sync-retell-prompt` to upsert a bounded `Persistent memory snapshot for inbound calls` into the Retell LLM prompt.
- To archive one completed Retell call locally, use `./hermes-v3/archive-retell-call.sh call_xxx --gbrain-sync` or `memory_bridge.py --fetch-retell-call call_xxx --brain-root /Users/kevin/.hermes/brain --kevin-phone '+173****4101' --gbrain-sync`. The archive writes `raw/retell-calls/{date}-{call_id}.md`, `raw/retell-calls/{date}-{call_id}.json`, and `sessions/retell/{date}-{call_id}.md`.
- Multi-caller safety: if a caller is new/unknown or not Kevin, the Retell prompt should ask for their first name immediately (“Before we jump in, what should I call you?”) and treat them as a clean-slate profile. Do not apply Kevin's memories to unknown callers. When matching Kevin's phone in local archive code, support exact and redacted-safe matching like `+173****4101`.
- Profile persistence: the Apps Script webhook should maintain `Hermes User Profiles`, keyed by caller phone number, with `profile_status` (`known`/`needs_name`), `call_count`, last-call fields, and a bounded context summary. Memory candidates for non-Kevin callers should include caller identity/phone context for review.
- Always test first when changing the bridge: `python3 -m unittest hermes-v3/test_memory_bridge.py -v`, `python3 -m py_compile hermes-v3/memory_bridge.py`, `bash -n hermes-v3/call-hermes.sh hermes-v3/archive-retell-call.sh`, and `node --check hermes-v3/webhook-hermes-memory.js`.
- Verify Retell state by GETting the LLM and checking that the prompt contains both `{{memory_briefing}}` and `Persistent memory snapshot for inbound calls`; never print the API key.
- Seed/approve only explicit user-stated durable memories. Current seed examples: Kevin wants Hermes Voice to remember prior conversations across calls; Kevin dislikes over-explaining and prefers concise useful voice answers; current project goal is persistent long-term memory for RetellAI/Hermes Voice.
- Karpathy validation doc for this build: `/Users/kevin/projects/voice-onboarding-mvp/hermes-v3/karpathy-memory-validation.md`.

## Backend Work to Look For

In ACQ_Vantage, inspect:
- `app/api/onboarding-call/route.js`
- `app/api/zapier-trigger/route.js`
- `app/api/members/[id]/route.js`
- `app/api/members/[id]/enrichment/route.js`
- `app/api/members/data/route.js`
- Supabase migration/schema files if present.

Likely next build items:
- `member_voice_profiles` or equivalent compiled profile table.
- `voice_calls` log table.
- `voice_profile_fields` / JSONB field store with confidence/source metadata.
- webhook endpoint to ingest ElevenLabs post-call payload into Supabase.
- backend extraction pass for all 40 fields.

## Pitfalls

- Do not call Alex voice quality the blocker unless Kevin says it changed.
- Do not rely only on ElevenLabs Data Collection for all 40 fields.
- Do not store long-term memory only inside ElevenLabs.
- Do not put sensitive per-member data in a static knowledge base.
- Do not request broad macOS folder permissions to restore Retell/Hermes voice behavior; first look for the existing project `.env`, Retell API scripts, webhook config, and connector wrapper.
- Dynamic variables need test placeholders/defaults or dashboard testing can break.
- Treat Google Sheets as demo/debug output, not production source of truth.

## Context Window / Memory Improvement Pattern

Do not try to solve memory by making the ElevenLabs prompt bigger.

Use this pattern:
1. Static docs -> Knowledge Base with RAG enabled when large.
2. Per-call member context -> short dynamic-variable briefing, not raw history.
3. Fresh or detailed data -> server tools that fetch from Supabase on demand.
4. Full history -> raw transcript/recording/webhook payload stored in backend.
5. Durable profile -> compiled member memory summary updated after each call.
6. Extraction -> ElevenLabs Data Collection for key fields plus a backend extraction/merge pass for broader schema completion.

Recommended variable categories:
- member_name
- business_name
- member_id
- known_summary
- missing_fields
- call_goal
- last_call_summary
- priority_questions

Use secret__ dynamic variables for auth tokens/private IDs that should only go in headers and not be sent to the LLM.

## Good Final Recommendation

The best solution is: ElevenLabs handles the call; Supabase handles memory. Use dynamic variables and server tools for live context, post-call webhooks plus a backend extraction pass for clean data, RAG for large static knowledge, and a Karpathy-style raw-to-compiled profile system for persistent member memory.
