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

Current stack:
- ElevenLabs Conversational AI for voice calls.
- Twilio phone routing.
- Google Apps Script / Google Sheet for demo data capture.
- Supabase / backend should become source of truth.
- ACQ_Vantage has `/api/onboarding-call` and `/api/zapier-trigger` routes.

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
