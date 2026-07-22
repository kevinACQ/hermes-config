# Authenticated Browser Workflows: Receipts and Calendar Verification

Use when a task spans an already signed-in browser profile, a financial confirmation page, local receipt retention, and calendar cleanup.

## Authenticated Profile Continuity

- Prefer the user's existing signed-in browser profile when the isolated automation browser lacks the required Gmail, Slack, booking, or Calendar sessions.
- On macOS, JavaScript can be executed in an existing Chrome tab via AppleScript after Chrome's **View → Developer → Allow JavaScript from Apple Events** setting is enabled.
- Treat every navigation, autofill, room/rate reselection, and payment-extension action as potentially resetting form state. Re-read the authoritative page state after each one.
- Do not copy session URLs, payment tokens, or secure iframe contents into notes or final reports.

## Receipt Capture Fallback

When a site's native Download control does not produce a discoverable file:

1. Open the site's official printable confirmation/receipt page.
2. Verify the source page visibly contains the booking/order number, item or room, guest, dates, taxes, and grand total.
3. Save a local HTML copy when practical as a fallback.
4. Render the printable page to PDF using a browser print-to-PDF or headless Chrome workflow.
5. Verify the output exists, is non-empty, begins with a PDF signature, and—when text extraction is available—contains the expected confirmation number and total.
6. Report the exact local path. Do not call a screenshot a receipt when an official printable confirmation exists.

## Calendar Replacement Pattern

1. Search Calendar for the old property/reservation name before editing.
2. Multi-day all-day events may appear as one search row per day even though they are one underlying event. Open a row and determine whether it is a single multi-day event before deleting.
3. Delete the old event once, then reload the search and require **no events found** for the old name.
4. Create one replacement all-day event with title, correct inclusive stay dates, location, confirmation number, guest, room/fare, total, contact number, and receipt location or Drive link.
5. After clicking Save, independently search by the new property name or confirmation number.
6. Verify the persisted result's title, every displayed stay date, all-day status, and location. Reopen it if the description also needs verification.

## Completion Evidence

A concise completion report should include:

- Cancellation/booking confirmation handles without payment secrets.
- Exact receipt path and backup path, if any.
- Old calendar search result after deletion.
- New calendar search result after saving.
- Precise financial language: cancellation fee, eligibility, and settled refund are separate facts.