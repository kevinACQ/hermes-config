# Voice interview gate pattern

Use when Kevin wants a creative or low-friction Prototype-First interview and already has Hermes/voice infrastructure available.

## Pattern

1. Treat the voice call as Gate 1 — INTERVIEW, not as implementation.
2. Write a call script before calling. The script should extract:
   - `Done = ___` in one sentence
   - the real moment of use / workflow movie
   - top dropped-ball or failure risks
   - current capture surfaces
   - preferred source of truth
   - notification tolerance
   - one-card/project-card schema
   - anti-requirements / what not to build
   - cheapest prototype
   - prototype evals and final-product evals
3. Prefer one high-leverage question at a time on voice. Do not stack questions.
4. If an existing voice agent can safely place the call with dynamic call context, use it for the first interview instead of creating a separate one-off agent. Split into a dedicated interviewer agent only after the prototype proves the mode will recur.
5. Archive the transcript and use the transcript as the Gate 1 input for prototype design.
6. After transcript ingestion, extract structured fields before proposing the cheap prototype.

## Script shape

Opening: set the frame: “I’m interviewing you like a product strategist, not a therapist. We’re designing the thinnest system that keeps you on task without becoming another thing to manage.”

Core questions:
1. Walk through the last real context-switching failure like a movie.
2. Name the three things you are most afraid of dropping.
3. Where are you physically/digitally when a new task or thought hits?
4. When returning to a project, what do you need to see first to restart?
5. How should attention be ranked, and what deserves interruption?
6. What should the daily interaction feel like?
7. Which existing tool should this lean on so it does not become a new habit?
8. What should we deliberately not build?
9. What would make tomorrow’s prototype obviously useful?

Closing synthesis:
“Here’s what I heard. Your real pain is [bottleneck], not just task tracking. The system needs to help you [job-to-be-done]. The thin prototype should be [prototype shape]. The first eval is: if [real scenario] happens, Hermes should [observable behavior]. Done equals [one sentence]. Did I get that right?”

## Pitfalls

- Do not jump from “voice call requested” to “create a new voice agent.” Preserve the thin-harness principle: reuse existing infrastructure unless separation is needed.
- Do not ask a long form over voice. Voice interviews should feel conversational and adaptive.
- Do not treat the transcript as durable memory wholesale. Extract decisions, preferences, open loops, and evals; keep raw transcript as provenance.