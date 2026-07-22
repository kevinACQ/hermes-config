---
name: productivity-integrations
description: "Use when operating productivity SaaS and document tools: Google Workspace, Airtable, Notion, email, maps, Office/PDF/OCR documents, and meeting-summary pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, google-workspace, airtable, notion, documents, email, maps, meetings]
    related_skills: [apple-macos-automation]
---

# Productivity Integrations

## Overview

Umbrella for user-facing productivity systems and document workflows. It consolidates SaaS APIs (Google Workspace, Airtable, Notion), document tools (PowerPoint, PDF editing, OCR), location utilities, and meeting-summary pipelines.

## When to Use

- User asks to read/write Gmail, Calendar, Drive, Docs, Sheets, Contacts.
- User asks to query or update Airtable/Notion.
- User asks to create/edit PowerPoint, PDF text, or extract text from scans/PDFs.
- User asks for geocoding, POIs, routes, or timezones.
- User asks to operate a Teams meeting-summary pipeline.

## Safety Rules

- Never send email, create/delete calendar events, mutate SaaS records, or publish documents without user confirmation unless explicitly pre-approved.
- Check authentication before first use.
- Return handles (record IDs, document IDs, event IDs, file paths, URLs) after side effects.
- Treat personal email, contacts, calendar, location, and meeting data as sensitive.

### Travel bookings and other financial checkouts

- Do all reversible preparation, but leave the final charge or booking submission to the user unless they explicitly authorize that exact transaction after reviewing the final state.
- Before cancelling an existing reservation, first verify replacement availability, dates, occupancy, total price, and cancellation policy. For the old reservation, capture the no-fee deadline and the exact fee shown in the final cancellation dialog.
- Distinguish **free cancellation** from a **settled refund**. A successful cancellation with a $0 fee proves no cancellation penalty; it does not prove that a prior card charge has posted back. Capture the cancellation number, confirmation email, and later verify the card ledger when a refund is expected.
- Treat browser autofill and payment-extension interactions as state-changing events. Immediately afterward, re-read and compare room/rate, stay dates, guest count, taxes, grand total, guest identity, and cancellation terms. Sites can silently switch room types or totals during navigation/autofill.
- Card fields in cross-origin PCI iframes may be unreadable from page automation. Do not claim card verification from parent-page DOM; ask the user to confirm the card/last four shown by the payment extension, then verify every non-card field and the final total before submission.
- Never copy or expose full card numbers, CVVs, or payment tokens. Stop if the room, total, cancellation policy, guest identity, or billing identity differs from the approved values.

## Service Modes

### Google Workspace

Use Hermes-managed OAuth and `gws`/Python wrappers for Gmail, Calendar, Drive, Sheets, Docs, and Contacts. Prefer Gmail app-password email skill only when email-only setup is desired.

### Airtable & Notion

Inspect schema/database fields before writing. Use filters/upserts cautiously and verify changed record IDs.

### Documents

For PowerPoint/PDF/OCR work, keep original files backed up, write output to a new path when possible, and verify by reopening/extracting text.

### Maps

Use OpenStreetMap/OSRM-style tools for geocoding/routes/timezones. Include units, timestamp, and ambiguity notes.

### Meeting Pipelines

For Teams summaries, inspect pipeline status before replaying jobs or manipulating subscriptions.

### Travel Reservations and Financial Changes

For hotel/flight replacement, cancellation, refund, or booking tasks, load `references/travel-reservation-financial-safeguards.md`. Verify replacement availability and its all-in price/policy before cancelling the original, inspect the final cancellation fee text, capture cancellation and booking confirmation handles, and stop before any new charge until the user approves the exact total. Never equate a successful no-fee cancellation with a settled card refund unless the payment ledger confirms it.

## Verification Checklist

- [ ] Auth checked.
- [ ] User approved high-impact mutations.
- [ ] Output IDs/URLs/paths captured.
- [ ] Documents were opened/read back or text-extracted after edits.
- [ ] No secrets or unrelated personal data exposed.
- [ ] For travel/checkout: room or item, dates, guest/quantity, taxes, grand total, cancellation/refund terms, and billing identity were rechecked after autofill and immediately before submission.
- [ ] Cancellation number was captured; any promised refund was verified separately from the cancellation confirmation.

## Consolidated Legacy Skills

Absorbed `google-workspace`, `airtable`, `notion`, `himalaya`, `maps`, `powerpoint`, `nano-pdf`, `ocr-and-documents`, and `teams-meeting-pipeline`.
