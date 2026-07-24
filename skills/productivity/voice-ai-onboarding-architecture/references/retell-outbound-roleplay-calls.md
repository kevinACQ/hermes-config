# Retell Outbound Role-Play Calls

Use this pattern when Kevin asks Hermes Voice to call a private/test number and simulate a real-world conversation such as a reservation, sales inquiry, or vendor call.

## Workflow

1. Resolve the scenario before calling: business/location, date, time, party size, name, desired outcome, and fallback constraints. Ask only for facts whose ambiguity changes the conversation.
2. Research the real business from its official site. Capture only operational facts useful in the call: correct venue name, location, current hours, phone/context, and relevant policies. Never invent availability, fees, confirmation numbers, dress codes, or policies.
3. Confirm the live voice configuration without exposing secrets. For the Hermes V3 Retell project, read `/Users/kevin/projects/voice-onboarding-mvp/.env`; print key names or safe IDs only. Verify the agent backup/current config identifies the intended custom voice and model.
4. Decide whether dynamic prompt injection is enough:
   - Use `retell_llm_dynamic_variables.memory_briefing` when the existing prompt and fixed opening are compatible.
   - If the fixed `begin_message` would break the simulation, create a temporary Retell LLM and temporary agent using the existing custom voice. Give it a scenario-specific prompt and opening line.
5. Trigger `POST https://api.retellai.com/v2/create-phone-call` with the configured Retell from-number, private destination number, and `override_agent_id`.
6. Verify the call exists by polling `POST /v2/list-calls` or `GET /v2/get-call/{call_id}`. Do not report success merely because the request was submitted; confirm status is at least `registered`/`ongoing`.
7. Poll until the call ends, then delete any temporary agent and LLM. Keep production agents unchanged.

## Temporary Agent Prompt Shape

The one-off prompt should state:

- Who the voice is pretending to be and who the callee will role-play.
- The exact goal and required facts.
- Allowed fallback range or negotiation boundary.
- What to ask only if needed.
- Grounded business facts from research.
- A prohibition on inventing availability, policies, fees, or confirmation details.
- A natural confirmation-and-close sequence.
- Short, conversational turns with no mention of AI/testing unless the user ends the exercise.

## Safety and Privacy

- Treat destination numbers as private contacts. Resolve aliases from Hermes memory where available and avoid repeating full numbers in chat or logs.
- Never print Retell API keys. Source the project `.env` inside the subprocess.
- A private-number simulation is not a real reservation. Never call the real business or create a binding booking unless Kevin explicitly asks for that external action.
- For real financial bookings, follow Kevin's reversible-prep rule and leave any charge to him.

## Pitfalls

- Do not assume a venue from a partial name when several locations exist.
- Do not forget the reservation date; if omitted in a clearly immediate test, explicitly ground the scenario to “tonight” using the live system date.
- A dynamic briefing cannot replace a fixed `begin_message`. Use a temporary agent when the opening must be scenario-specific.
- Do not patch the production LLM just to run a one-off simulation; that can affect inbound calls and creates a restore race.
- Do not leave temporary Retell agents/LLMs behind. Cleanup is part of completion.
- Background process output may lag. Independently list recent calls and match metadata to verify the call is live.

## Verification Receipt

Report only safe details: destination alias, business/location, scenario facts, researched hours, call status, and optionally the call ID. Never include credentials or unnecessarily restate the full destination number.
