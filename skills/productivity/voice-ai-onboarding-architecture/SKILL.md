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

When Kevin asks to “start” or “autoplan each phase” for the Hermes/Retell voice advisor, treat it as an execution prep task, not just a recommendation.

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

External-action boundary:
- Creating the actual Retell agent calls the external Retell API and depends on `RETELL_WEBHOOK_URL`, Retell keys, and voice IDs. Prepare scripts first; run the API creation only after webhook deployment/env readiness is clear.
- Recommended next order after prep: deploy Apps Script, set `HERMES_MEMORY_SHEET_ID`, run `testHermesWebhook()`, set `RETELL_WEBHOOK_URL`, then run `./create-hermes-agent.sh` and `./call-hermes.sh`.

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
