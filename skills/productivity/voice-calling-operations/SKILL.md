---
name: voice-calling-operations
description: Operate outbound AI voice calls, realistic call simulations, and private contact aliases. Use when Kevin asks Hermes to call someone, role-play a phone scenario, use Alex's voice, save a phone number for later reference, or select a default number.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [voice, outbound-calls, contacts, retell, privacy]
---

# Voice Calling Operations

## Purpose

Run outbound voice calls safely and realistically while keeping phone numbers out of ordinary chat. This skill governs contact resolution, call preflight, scenario research, execution, and verification. It does not recreate or redesign the underlying voice agent.

## Private Contact Aliases

- When Kevin explicitly asks to save a number in Hermes internal memory, honor that choice; do not redirect him to Apple Contacts.
- Store the contact as a compact private-memory fact with: alias/name, relationship or identity, normalized E.164 number, and primary/default status.
- When a second number becomes the default, preserve the former number as an alternate unless Kevin asks to delete it.
- In later chats, resolve phrases such as “me,” “my number,” or the saved alias from memory.
- Do not repeat a full stored phone number in chat unless Kevin explicitly asks to see or verify it. Refer to it by alias and masked suffix when disambiguation is necessary.
- Never place raw phone numbers, API keys, or other contact PII in this skill or its support files.

## Call Preflight

Before dialing, resolve these fields:

1. **Recipient** — saved alias or explicit number; use the stored primary/default number when no number is specified.
2. **Call type** — real-world action or simulation/role-play.
3. **Voice/agent** — use the requested voice, such as Alex, and the configured outbound calling provider.
4. **Objective** — what outcome the call should pursue.
5. **Scenario facts** — business/location, date, time, party size, constraints, and fallback choices.

Retrieve any saved contact or project context before asking Kevin to repeat it. Ask only for facts that materially change the call. A single batched clarification is preferable when both location and date are missing.

## Realistic Business Simulations

For a simulation in which Hermes calls Kevin while pretending to contact a business:

- Dial Kevin’s stored number, not the business.
- State internally and in provider metadata that the call is a simulation; do not create a real reservation or contact the real business.
- Research the exact business location using current sources before dialing. Confirm its name, address/city, current hours for the requested date, reservation norms, cuisine/service details, and likely questions.
- If the business name is ambiguous (for example, multiple locations or a possible spelling variant), resolve the exact location before research and dialing.
- Resolve the reservation date as well as the time; “7pm” alone is incomplete for a realistic reservation conversation.
- Build a compact scenario sheet rather than reading a rigid script. Include likely host questions, plausible answers, one fallback time, seating preference only if known, and a natural close.
- Never claim a real booking was made from a simulated call.

## Execution

1. Resolve the private contact without displaying the full number.
2. Confirm that the configured voice agent/provider is available and that the requested voice is selected.
3. Research current scenario facts when the call references a real business.
4. Prepare the agent prompt with role, objective, known facts, boundaries, and fallback behavior.
5. Initiate the outbound call through the configured provider.
6. Capture the provider’s verifiable call ID and initial status.
7. Poll or inspect the completed call status, transcript, and error fields when available.

Do not say a call was placed unless the provider returned a real call identifier. Do not say it succeeded unless completion status or transcript evidence supports that claim.

## Safety and Privacy

- Treat all saved numbers and call transcripts as sensitive.
- Avoid exposing numbers in chat, logs, skill files, screenshots, or summaries.
- Confirm scope before any call that could create a reservation, purchase, cancellation, legal commitment, or reputational impact.
- For simulations, keep all external side effects disabled.
- Never repeat provider credentials in chat.

## Supporting Reference

See `references/private-contact-and-simulation-preflight.md` for the privacy-safe contact pattern, simulation interpretation, scenario-sheet fields, and reporting standard.

## Verification Checklist

- [ ] Recipient resolved from explicit input or private memory.
- [ ] Correct default/alternate number selected.
- [ ] Real call versus simulation clearly distinguished.
- [ ] Exact business location and reservation date resolved when relevant.
- [ ] Current hours and scenario details researched.
- [ ] Requested voice selected.
- [ ] Provider returned a call ID.
- [ ] Final status/transcript checked before reporting success.
- [ ] No full phone number or credential exposed unnecessarily.
