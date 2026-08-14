# Private Contacts and Simulated Business Calls

## Durable lessons

- Kevin may intentionally choose Hermes internal memory instead of Apple Contacts so he can use a name or alias in a new chat without reposting the number. Respect the selected storage layer.
- Normalize stored US numbers to E.164. Keep one explicit primary/default and retain prior numbers as alternates unless deletion is requested.
- Resolve the number from memory at execution time and avoid rendering it back into normal chat.
- A request to “call me and pretend you are making a reservation” means the user's phone is the destination and the business is scenario context only. No call should reach the real business and no reservation should be created.
- Realism requires the exact business location and reservation date, not just a business name and clock time. Research current hours and business-specific details only after those are resolved.

## Minimal simulation scenario sheet

- Destination alias (never raw number in the sheet)
- Voice/agent
- Explicit simulation marker
- Exact business and location
- Reservation date, time, party size
- Current opening hours for that date
- Likely host questions
- Known guest answers
- One fallback time
- Boundaries: no real booking, payment, or external contact

## Reporting standard

Report initiation only with a provider call ID. Report completion only after checking final provider status or transcript evidence. Refer to the recipient by alias and keep raw numbers and credentials out of the response.
