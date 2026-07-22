---
name: apple-macos-automation
description: "Use when automating Apple and macOS user-facing apps: Messages/iMessage, Notes, Reminders, Find My, and background desktop control. Provides class-level choice rules plus CLI-specific subsections."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [apple, macos, automation, messages, notes, reminders, findmy, computer-use]
    related_skills: [google-workspace, himalaya]
---

# Apple & macOS Automation

## Overview

Use this umbrella for macOS-native tasks that interact with Apple apps or the desktop: sending/reading iMessage/SMS, creating/searching Apple Notes, managing Reminders, checking Find My devices/AirTags, and driving GUI apps in the background with `computer_use`/cua-driver.

Prefer purpose-built CLIs when the task is semantic data access; use background computer control when the task is visual, GUI-only, or requires operating an app that has no reliable CLI.

## When to Use

- User asks to send/read iMessage or SMS from the Mac.
- User asks to add, search, update, or inspect Apple Notes.
- User asks to add/list/complete Reminders.
- User asks where an Apple device or AirTag is.
- User asks you to operate a macOS app, inspect a window, or click/type/scroll without stealing focus.

Do not use for cloud productivity apps when a first-party API skill exists (Google Workspace, Notion, Airtable), or for web pages where browser automation is sufficient.

## Tool Choice

| Task class | Preferred route | Notes |
|---|---|---|
| Messages/iMessage/SMS | `imsg` CLI | Never infer recipients; confirm before sending sensitive/high-impact messages. |
| Notes | `memo` CLI | Use for create/search/edit; preserve note titles and folders. |
| Reminders | `remindctl` CLI | Include due dates/timezones explicitly when provided. |
| Find My | FindMy.app automation | Treat location data as sensitive; report only what the user asked for. |
| GUI operation | `computer_use` | Capture SOM first, click by element index, verify after state changes. |

## iMessage/SMS

- Use the macOS Messages-backed `imsg` workflow for send/read operations.
- Resolve the recipient unambiguously before sending; if multiple contacts match, ask.
- Draft messages exactly as requested; do not add unsolicited context.
- Do not type passwords, verification codes, payment data, or secrets into Messages.

## Apple Notes

- Use the `memo` workflow for Notes create/search/edit.
- Search before creating when the user references an existing note.
- Preserve user wording for note titles unless the user asks for cleanup.
- For large edits, summarize the intended diff before writing if the content is user-authored or sensitive.

## Apple Reminders

- Use `remindctl` for add/list/complete operations.
- Normalize due dates with explicit timezone when the user gives a time.
- If a reminder list is ambiguous, prefer the default list rather than asking unless list choice changes the outcome.

## Find My

- Use FindMy.app/macOS automation for device and AirTag location checks.
- Treat location as private. Report concise status: device/item name, last seen time if visible, and approximate location.
- Never change lost-mode, erase, or notification settings unless explicitly requested.

## Background Desktop Control

- Use `computer_use(action='capture', mode='som', app='…')` first.
- Click by element index, not coordinates, whenever possible.
- Use `capture_after=true` or recapture after state-changing actions.
- Do not click permission dialogs, password prompts, payment UI, or anything outside the user's request.

## Existing Signed-In Chrome Sessions

When the isolated browser profile lacks the user's existing login state or extensions and the user explicitly wants the already-open Chrome profile, use Chrome AppleScript automation rather than asking them to sign in again. Load `references/chrome-existing-session-automation.md` for the prerequisite toggle, stable tab targeting, SPA interaction patterns, and financial-action verification rules.

Key pitfalls:
- **Allow JavaScript from Apple Events** is under the macOS **View → Developer** menu, not Chrome Settings; explain this in layman's terms when needed.
- Never assume the active tab remains fixed. Re-find the target by URL/title before every read or action.
- After cancellation, booking, or another irreversible action, read the resulting success page and capture the confirmation handle before reporting completion.

## Package Notes

Detailed legacy package content was consolidated from the former narrow skills: `imessage`, `apple-notes`, `apple-reminders`, `findmy`, and `macos-computer-use`. If a low-level CLI flag or cua-driver install recipe is missing here, restore the archived package and promote the specific reusable detail into this umbrella's references.

## Verification Checklist

- [ ] Selected CLI/API vs GUI control intentionally.
- [ ] Resolved recipients, note/reminder targets, or devices unambiguously.
- [ ] Avoided secrets, permissions, payment UI, and unrelated windows.
- [ ] Verified any create/send/edit/complete action with real output or a follow-up capture.
