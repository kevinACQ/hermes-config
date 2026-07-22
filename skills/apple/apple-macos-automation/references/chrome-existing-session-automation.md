# Automating an Existing Signed-In Chrome Session on macOS

Use this when the isolated browser profile lacks the user's existing Gmail, Slack, payment-extension, or site login state and the user explicitly wants the already-open Chrome profile used.

## Prerequisite

Chrome must have **View → Developer → Allow JavaScript from Apple Events** enabled. This setting is in the macOS menu bar, not `chrome://settings`.

If desktop UI automation cannot enable it, give layperson directions:
1. Move the pointer to the very top of the screen.
2. Click **View** in the macOS menu bar.
3. Hover over **Developer**.
4. Click **Allow JavaScript from Apple Events**.

## Discovery

List open tabs without reading page content unnecessarily:

```applescript
tell application "Google Chrome"
  repeat with w in windows
    repeat with t in tabs of w
      log ((title of t as text) & tab & (URL of t as text))
    end repeat
  end repeat
end tell
```

## Targeting

Do not assume the active tab stays fixed; the user may switch tabs while automation runs. Find the target by stable URL/title criteria on every action, then execute JavaScript against that tab directly.

```applescript
tell application "Google Chrome"
  repeat with w in windows
    repeat with t in tabs of w
      if URL of t contains "example.com/checkout" then
        return execute t javascript "document.body.innerText"
      end if
    end repeat
  end repeat
end tell
```

To bring a target tab forward, loop by numeric tab index and set `active tab index of w`; do not try to set an individual tab object's `index`.

## SPA Interaction

For React/Slack-style apps:
- Prefer stable IDs, `aria-label`, `data-*` attributes, or direct channel/resource URLs.
- For controlled inputs, use the native property setter and dispatch bubbling `input` and `change` events.
- If a synthetic `.click()` does not navigate, extract the stable resource ID and navigate directly.
- Re-read URL and visible body text after every state-changing action.

## Financial/Irreversible Actions

Before confirming cancellation or purchase:
1. Extract the exact dates, amount, fee, deadline, and policy from the final confirmation UI.
2. Ensure the action element is visible (`offsetParent !== null`) and scoped to the modal/form, not a duplicate background button.
3. Execute only when the user has authorized that class of action.
4. Verify the resulting success page and capture confirmation/cancellation numbers.
5. Stop before a new charge unless the user has explicitly approved the exact final amount.

Never expose card data, authentication secrets, or unrelated page content in logs or chat.