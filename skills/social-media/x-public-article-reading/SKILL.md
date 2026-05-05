---
name: x-public-article-reading
description: Read and summarize public X/Twitter posts or Articles when API auth is unavailable or page snapshots are truncated.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [x, twitter, article, browser, summarization]
    related_skills: [xurl]
---

# X Public Article Reading

Use this when the user asks to read, summarize, fact-filter, or explain a public X/Twitter post or Article.

## Workflow

1. If available, load `xurl` first and try safe read-only access.
2. If `xurl` is unavailable, unauthenticated, rate-limited, or blocked, use the browser tools.
3. Open the X URL with `browser_navigate`.
4. If the compact snapshot is truncated, call `browser_snapshot(full=true)`.
5. If the full snapshot is still truncated or misses article text, extract visible page text with:

```javascript
document.body.innerText
```

using `browser_console`.

6. If X offers a Focus mode article link, try it only as a convenience. If it fails with “Something went wrong. Try reloading,” go back to the normal status page; the normal page may still expose the full article body.
7. Strip noise before summarizing:
   - login/signup prompts
   - trending modules
   - reply counts and engagement UI
   - “Relevant people” blocks
   - footer/legal text
   - replies unless the user asked for them
8. Preserve useful provenance:
   - title
   - author handle
   - date/time if visible
   - article body
   - image/media captions if relevant

## Output Pattern for Kevin

When Kevin asks for a simplification:

1. Start with what to ignore: hype, unsupported stats, credentials, or irrelevant flexing.
2. Explain the remaining signal in simple chapters.
3. Use plain language, short bullets, and fifth-grade reading level.
4. End with a brief executive summary tied to Kevin’s actual projects and Hermes workflows.

## Pitfalls

- Do not ask Kevin to paste the text until both API and browser extraction fail.
- Do not treat visible X claims as verified facts; label unsupported numbers or career claims as noise unless independently verified.
- Do not perform write actions such as like, repost, reply, follow, bookmark, or DM without explicit approval.
